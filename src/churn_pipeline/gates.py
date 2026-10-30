"""Validation gates of the churn pipeline flow.

Plain Python, no LLM: each gate returns a GateResult, and the flow routes on
them. The handoff gates run between Crew 1 and Crew 2; the quality gate runs
after Crew 2.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from churn_pipeline.contract.models import DatasetContract, load_contract
from churn_pipeline.contract.validator import validate_against_contract

CREW1_ARTIFACTS = [
    "quality_report.json",
    "quality_summary.md",
    "clean_data.csv",
    "preparation_log.md",
    "eda_report.html",
    "insights.md",
    "contract_numbers.json",
    "dataset_contract.json",
]

CREW2_ARTIFACTS = [
    "contract_review.md",
    "features.csv",
    "feature_spec.json",
    "feature_log.md",
    "model.joblib",
    "evaluation_metrics.json",
    "evaluation_report.md",
    "model_card.md",
]

# Written by the agents, so they change wording from run to run; the lock
# compares every number and rule, not this text.
TEXT_FIELDS = {"description", "assumptions", "leakage_notes"}


@dataclass
class GateResult:
    name: str
    passed: bool
    summary: str
    problems: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _missing_files(directory: str | Path, names: list[str]) -> list[str]:
    d = Path(directory)
    return [f for f in names if not (d / f).is_file() or (d / f).stat().st_size == 0]


# ------------------------------------------------------------ handoff gates

def gate_crew1_artifacts(crew1_dir: str | Path) -> GateResult:
    missing = _missing_files(crew1_dir, CREW1_ARTIFACTS)
    if missing:
        return GateResult("crew1_artifacts", False, f"{len(missing)} Crew 1 artifacts missing or empty",
                          [f"{f} is missing or empty" for f in missing])
    return GateResult("crew1_artifacts", True, f"all {len(CREW1_ARTIFACTS)} Crew 1 artifacts present")


def gate_contract_vs_data(crew1_dir: str | Path) -> GateResult:
    d = Path(crew1_dir)
    data = d / "clean_data.csv"
    violations = validate_against_contract(
        pd.read_csv(data), load_contract(d / "dataset_contract.json"), file_path=data)
    if violations:
        return GateResult("contract_vs_data", False,
                          f"clean_data.csv breaks dataset_contract.json ({len(violations)} violations)",
                          [v.message for v in violations])
    return GateResult("contract_vs_data", True, "clean_data.csv matches dataset_contract.json")


def _without_text(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _without_text(v) for k, v in value.items() if k not in TEXT_FIELDS}
    if isinstance(value, list):
        return [_without_text(v) for v in value]
    return value


def _diff(locked: Any, current: Any, path: str) -> list[str]:
    if isinstance(locked, dict) and isinstance(current, dict):
        out = []
        for key in sorted(set(locked) | set(current)):
            sub = f"{path}.{key}" if path else key
            if key not in current:
                out.append(f"{sub} is in the locked contract but missing from the new one")
            elif key not in locked:
                out.append(f"{sub} is new: {current[key]!r} (not in the locked contract)")
            else:
                out += _diff(locked[key], current[key], sub)
        return out
    if locked != current:
        return [f"{path}: locked {locked!r}, new {current!r}"]
    return []


def gate_locked_contract(crew1_dir: str | Path, lock_path: str | Path) -> GateResult:
    """Compare the contract Crew 1 just wrote with the approved, locked one.

    Columns are matched by name, so a renamed or dropped column is reported
    by name rather than as a shifted list.
    """
    locked = _without_text(json.loads(Path(lock_path).read_text(encoding="utf-8")))
    current = _without_text(json.loads((Path(crew1_dir) / "dataset_contract.json").read_text(encoding="utf-8")))
    for c in (locked, current):
        c["columns"] = {col["name"]: col for col in c.get("columns", [])}
    problems = _diff(locked, current, "")
    if problems:
        return GateResult("locked_contract", False,
                          f"dataset_contract.json differs from the locked contract ({len(problems)} differences)",
                          problems)
    return GateResult("locked_contract", True, "dataset_contract.json matches the locked contract")


def gate_required_features(crew1_dir: str | Path, lock_path: str | Path) -> GateResult:
    """Every feature the locked contract promises must be in clean_data.csv and usable."""
    locked = load_contract(lock_path)
    required = [c.name for c in locked.columns
                if c.role == "feature" and c.name not in locked.forbidden_features]
    columns = set(pd.read_csv(Path(crew1_dir) / "clean_data.csv", nrows=0).columns)
    contract: DatasetContract = load_contract(Path(crew1_dir) / "dataset_contract.json")
    usable = {c.name for c in contract.columns
              if c.role == "feature" and c.name not in contract.forbidden_features}
    problems = [f"required feature {n!r} is not in clean_data.csv" for n in required if n not in columns]
    problems += [f"required feature {n!r} is not a usable feature in dataset_contract.json"
                 for n in required if n in columns and n not in usable]
    if problems:
        return GateResult("required_features", False,
                          f"{len(problems)} of {len(required)} required features unavailable", problems)
    return GateResult("required_features", True, f"all {len(required)} required features available")


def run_handoff_gates(crew1_dir: str | Path, lock_path: str | Path) -> list[GateResult]:
    """Gates between Crew 1 and Crew 2. Stops after the first gate whose
    failure makes the later ones meaningless (missing files)."""
    first = gate_crew1_artifacts(crew1_dir)
    if not first.passed:
        return [first]
    return [
        first,
        gate_contract_vs_data(crew1_dir),
        gate_locked_contract(crew1_dir, lock_path),
        gate_required_features(crew1_dir, lock_path),
    ]


# -------------------------------------------------------------- quality gate

def gate_model_quality(crew2_dir: str | Path) -> GateResult:
    d = Path(crew2_dir)
    missing = _missing_files(d, CREW2_ARTIFACTS)
    if missing:
        return GateResult("model_quality", False, f"{len(missing)} Crew 2 artifacts missing or empty",
                          [f"{f} is missing or empty" for f in missing])
    metrics = json.loads((d / "evaluation_metrics.json").read_text(encoding="utf-8"))
    test = metrics["selected_test_metrics"]
    problems = [f"test {k} is {test[k]:.4f}, below the threshold {v:.2f}"
                for k, v in metrics["quality_thresholds"].items() if test[k] < v]
    if metrics["split"]["duplicate_groups_on_both_sides"]:
        problems.append(f"{metrics['split']['duplicate_groups_on_both_sides']} duplicate groups "
                        "are in both train and test, so the test scores are inflated")
    scores = ", ".join(f"{k} {test[k]:.4f} (min {v:.2f})" for k, v in metrics["quality_thresholds"].items())
    if problems:
        return GateResult("model_quality", False, f"{metrics['selected_model']} fails: {scores}", problems)
    return GateResult("model_quality", True, f"{metrics['selected_model']} passes: {scores}")


# ---------------------------------------------------------------- reporting

def write_validation_report(path: str | Path, gates: list[GateResult], verdict: str,
                            next_step: str, when: datetime | None = None) -> None:
    when = when or datetime.now(timezone.utc)
    lines = [
        "# Validation report",
        "",
        f"- Verdict: **{verdict}**",
        f"- Time (UTC): {when.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- Next step: {next_step}",
        "",
        "| Gate | Result | Summary |",
        "|---|---|---|",
    ]
    lines += [f"| {g.name} | {'PASS' if g.passed else 'FAIL'} | {g.summary} |" for g in gates]
    for g in gates:
        if g.problems:
            lines += ["", f"## {g.name}", ""] + [f"- {p}" for p in g.problems]
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
