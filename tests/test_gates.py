"""Validation gates, and the flow's routing, tested without an LLM."""
import json
import shutil
from pathlib import Path

import pandas as pd
import pytest

import churn_pipeline.main as main
from churn_pipeline.gates import (
    gate_locked_contract,
    gate_model_quality,
    gate_required_features,
    run_handoff_gates,
)
from churn_pipeline.tools.analyst_tools import (
    build_contract,
    export_clean_data,
    finalize_contract,
    profile_raw_data,
    run_eda,
)
from churn_pipeline.tools.scientist_tools import build_features, train_and_evaluate

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "E Commerce Dataset.xlsx"
LOCK = ROOT / "contracts" / "dataset_contract.lock.json"


@pytest.fixture(scope="module")
def crew1_template(tmp_path_factory) -> Path:
    """All eight Crew 1 artifacts: tool outputs plus stand-ins for the agents' markdown."""
    d = tmp_path_factory.mktemp("crew1")
    profile_raw_data(RAW, d)
    export_clean_data(RAW, d)
    run_eda(d)
    numbers = build_contract(d)
    finalize_contract(d, {c["name"]: f"Description of {c['name']}" for c in numbers["columns"]},
                      ["No imputation"], ["Churn window undefined"])
    for name in ("quality_summary.md", "preparation_log.md", "insights.md"):
        (d / name).write_text("agent text\n")
    return d


@pytest.fixture
def crew1(crew1_template, tmp_path) -> Path:
    d = tmp_path / "crew1"
    shutil.copytree(crew1_template, d)
    return d


def _edit_csv(d: Path, change) -> None:
    df = pd.read_csv(d / "clean_data.csv")
    df = change(df)
    df.to_csv(d / "clean_data.csv", index=False)


def _failed(gates) -> dict[str, list[str]]:
    return {g.name: g.problems for g in gates if not g.passed}


def test_real_handoff_passes_every_gate(crew1):
    gates = run_handoff_gates(crew1, LOCK)
    assert [g.name for g in gates] == ["crew1_artifacts", "contract_vs_data", "locked_contract",
                                       "required_features"]
    assert _failed(gates) == {}


def test_missing_artifact_stops_the_other_gates(crew1):
    (crew1 / "insights.md").unlink()
    gates = run_handoff_gates(crew1, LOCK)
    assert len(gates) == 1
    assert _failed(gates) == {"crew1_artifacts": ["insights.md is missing or empty"]}


def test_unit_change_after_the_contract(crew1):
    _edit_csv(crew1, lambda df: df.assign(CashbackAmount=df["CashbackAmount"] * 100))
    failed = _failed(run_handoff_gates(crew1, LOCK))
    assert list(failed) == ["contract_vs_data"]
    assert any("possible unit change" in p for p in failed["contract_vs_data"])


def test_contract_rebuilt_on_broken_data_is_caught_by_the_lock(crew1):
    # Crew 1 run on broken raw data writes a contract that matches the broken
    # file, so only the comparison with the locked contract can see the change.
    _edit_csv(crew1, lambda df: df.assign(CashbackAmount=df["CashbackAmount"] * 100))
    numbers = build_contract(crew1)
    finalize_contract(crew1, {c["name"]: "d" for c in numbers["columns"]}, ["a"], ["b"])
    failed = _failed(run_handoff_gates(crew1, LOCK))
    assert list(failed) == ["locked_contract"]
    assert "columns.CashbackAmount.expected_mean: locked 177.223, new 17722.303" in failed["locked_contract"]


def test_agent_text_does_not_trip_the_lock(crew1):
    contract = json.loads((crew1 / "dataset_contract.json").read_text())
    contract["assumptions"] = ["worded differently"]
    contract["columns"][0]["description"] = "worded differently"
    (crew1 / "dataset_contract.json").write_text(json.dumps(contract))
    assert gate_locked_contract(crew1, LOCK).passed


def test_dropped_feature(crew1):
    _edit_csv(crew1, lambda df: df.drop(columns="Complain"))
    failed = _failed(run_handoff_gates(crew1, LOCK))
    assert "contract_vs_data" in failed
    assert failed["required_features"] == ["required feature 'Complain' is not in clean_data.csv"]


def test_feature_marked_forbidden_in_a_new_contract(crew1):
    contract = json.loads((crew1 / "dataset_contract.json").read_text())
    contract["forbidden_features"].append("Tenure")
    (crew1 / "dataset_contract.json").write_text(json.dumps(contract))
    assert not gate_required_features(crew1, LOCK).passed
    assert not gate_locked_contract(crew1, LOCK).passed


# ------------------------------------------------------------ flow routing

class FakeScientistCrew:
    """Stands in for Crew 2: runs its tools without agents and writes stand-in markdown."""

    thresholds: dict | None = None
    runs = 0

    def crew(self):
        return self

    def kickoff(self, inputs):
        FakeScientistCrew.runs += 1
        out = Path(inputs["output_dir"])
        build_features(inputs["input_dir"], out)
        metrics = train_and_evaluate(out)
        if self.thresholds:
            metrics["quality_thresholds"] = self.thresholds
            (out / "evaluation_metrics.json").write_text(json.dumps(metrics))
        for name in ("contract_review.md", "feature_log.md", "evaluation_report.md", "model_card.md"):
            (out / name).write_text("agent text\n")


def _run_flow(crew1: Path, monkeypatch, thresholds=None) -> tuple[dict, Path]:
    FakeScientistCrew.runs = 0
    FakeScientistCrew.thresholds = thresholds
    monkeypatch.setattr(main, "ScientistCrew", FakeScientistCrew)
    out = crew1.parent
    result = main.ChurnPipelineFlow().kickoff(inputs={
        "from_gate": True, "output_dir": str(crew1), "crew2_output_dir": str(out / "crew2"),
        "report_path": str(out / "validation_report.md")})
    return result, out


def test_flow_passes_and_approves_the_model(crew1, monkeypatch):
    result, out = _run_flow(crew1, monkeypatch)
    assert result["status"] == "passed"
    assert FakeScientistCrew.runs == 1
    assert (out / "crew2" / "model_approved.json").is_file()
    assert "**PASSED**" in (out / "validation_report.md").read_text()


def test_flow_stops_before_crew2_on_a_broken_handoff(crew1, monkeypatch):
    _edit_csv(crew1, lambda df: df.assign(CashbackAmount=df["CashbackAmount"] * 100))
    result, out = _run_flow(crew1, monkeypatch)
    assert result["status"] == "handoff_failed"
    assert FakeScientistCrew.runs == 0
    assert not (out / "crew2").exists()
    report = (out / "validation_report.md").read_text()
    assert "**FAILED**" in report and "possible unit change" in report


def test_flow_rejects_a_model_below_the_thresholds(crew1, monkeypatch):
    result, out = _run_flow(crew1, monkeypatch, thresholds={"pr_auc": 0.95, "recall": 0.60})
    assert result["status"] == "model_rejected"
    assert not (out / "crew2" / "model_approved.json").exists()
    assert "below the threshold 0.95" in (out / "validation_report.md").read_text()
    assert not gate_model_quality(out / "crew2").passed
