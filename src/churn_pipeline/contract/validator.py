"""Validate a DataFrame against a DatasetContract.

Pure pandas, no LLM. Every check runs, even after an earlier one fails,
so the report lists all violations at once.
"""
from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from churn_pipeline.contract.duplicates import duplicate_counts
from churn_pipeline.contract.models import ColumnSpec, DatasetContract


@dataclass(frozen=True)
class Violation:
    check: str
    column: str | None
    expected: Any
    actual: Any
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_against_contract(
    df: pd.DataFrame,
    contract: DatasetContract,
    file_path: str | Path | None = None,
) -> list[Violation]:
    """Return every way df disagrees with contract; empty list means it passes.

    file_path, when given, is hashed and compared with contract.dataset.sha256.
    """
    violations: list[Violation] = []
    violations += _check_columns(df, contract)
    for spec in contract.columns:
        if spec.name in df.columns:
            violations += _check_column(df[spec.name], spec, contract)
    violations += _check_dataset(df, contract)
    if file_path is not None and contract.dataset.sha256:
        actual = file_sha256(file_path)
        if actual != contract.dataset.sha256:
            violations.append(Violation(
                "sha256", None, contract.dataset.sha256, actual,
                f"{Path(file_path).name} has changed since the contract was written",
            ))
    return violations


def _check_columns(df: pd.DataFrame, contract: DatasetContract) -> list[Violation]:
    expected = [c.name for c in contract.columns]
    missing = [c for c in expected if c not in df.columns]
    extra = [c for c in df.columns if c not in expected]
    out = []
    for name in missing:
        hint = f"; possible rename to one of {extra}" if extra else ""
        out.append(Violation("columns", name, "present", "missing",
                             f"column {name!r} is in the contract but not in the data{hint}"))
    for name in extra:
        out.append(Violation("columns", name, "absent", "present",
                             f"column {name!r} is in the data but not in the contract"))
    return out


def _check_column(s: pd.Series, spec: ColumnSpec, contract: DatasetContract) -> list[Violation]:
    out = []
    nulls = int(s.isna().sum())
    if nulls != spec.expected_null_count:
        out.append(Violation("nulls", spec.name, spec.expected_null_count, nulls,
                             f"{spec.name} has {nulls} missing values, contract expects {spec.expected_null_count}"))
    values = s.dropna()

    if spec.unique and s.duplicated().any():
        n = int(s.duplicated().sum())
        out.append(Violation("unique", spec.name, "unique", f"{n} duplicates",
                             f"{spec.name} must be unique but has {n} duplicate values"))

    if spec.dtype == "category":
        bad = sorted(set(values.astype(str)) - set(spec.allowed_values or []))
        if bad:
            out.append(Violation("allowed_values", spec.name, spec.allowed_values, bad,
                                 f"{spec.name} has values not allowed by the contract: {bad}"))
        return out

    if not pd.api.types.is_numeric_dtype(s) or pd.api.types.is_bool_dtype(s):
        out.append(Violation("dtype", spec.name, spec.dtype, str(s.dtype),
                             f"{spec.name} should be numeric ({spec.dtype}) but is {s.dtype}"))
        return out
    if spec.dtype in ("int", "binary") and not (values == values.round()).all():
        out.append(Violation("dtype", spec.name, spec.dtype, "non-integer values",
                             f"{spec.name} should hold whole numbers but has fractional values"))
    if spec.dtype == "binary":
        bad = sorted(set(values.unique()) - {0, 1})
        if bad:
            out.append(Violation("allowed_values", spec.name, [0, 1], bad,
                                 f"{spec.name} is binary but has values {bad}"))

    if spec.range is not None and len(values):
        lo, hi = float(values.min()), float(values.max())
        if lo < spec.range.min or hi > spec.range.max:
            out.append(Violation("range", spec.name, [spec.range.min, spec.range.max], [lo, hi],
                                 f"{spec.name} ranges {lo:g}..{hi:g}, contract allows "
                                 f"{spec.range.min:g}..{spec.range.max:g}"))

    if spec.expected_mean is not None and len(values):
        out += _check_mean(spec, float(values.mean()), contract)
    return out


def _check_mean(spec: ColumnSpec, mean: float, contract: DatasetContract) -> list[Violation]:
    expected = spec.expected_mean
    assert expected is not None
    tol = contract.tolerances
    if expected == 0:
        drift = abs(mean)
    else:
        drift = abs(mean - expected) / abs(expected)
    if drift <= tol.mean_rel:
        return []
    message = (f"{spec.name} mean is {mean:,.2f}, contract expects {expected:,.2f} "
               f"(±{tol.mean_rel:.0%})")
    if expected != 0 and mean != 0:
        ratio = max(abs(mean / expected), abs(expected / mean))
        if ratio >= tol.unit_change_factor:
            unit = f" (contract unit: {spec.unit})" if spec.unit else ""
            message += f"; about {ratio:,.0f}x off, possible unit change{unit}"
    return [Violation("mean_drift", spec.name, expected, round(mean, 4), message)]


def _check_dataset(df: pd.DataFrame, contract: DatasetContract) -> list[Violation]:
    out = []
    expected_rows = contract.dataset.row_count
    if len(df) != expected_rows:
        out.append(Violation("row_count", None, expected_rows, len(df),
                             f"data has {len(df)} rows, contract expects {expected_rows}"))
    t = contract.target
    if t.name in df.columns and pd.api.types.is_numeric_dtype(df[t.name]):
        y = df[t.name].dropna()
        if len(y):
            rate = float((y == t.positive_class).mean())
            if abs(rate - t.expected_rate) > t.expected_rate * contract.tolerances.target_rate_rel:
                out.append(Violation("target_rate", t.name, t.expected_rate, round(rate, 4),
                                     f"{t.name} positive rate is {rate:.4f}, contract expects "
                                     f"{t.expected_rate:.4f} (±{contract.tolerances.target_rate_rel:.0%})"))
    out += _check_duplicates(df, contract)
    return out


def _check_duplicates(df: pd.DataFrame, contract: DatasetContract) -> list[Violation]:
    info = contract.dataset
    if info.duplicate_rows_ignoring_id is None and info.rows_in_duplicate_groups is None:
        return []
    ids = [c.name for c in contract.columns if c.role == "id" and c.name in df.columns]
    actual = duplicate_counts(df, ids)
    out = []
    if info.duplicate_rows_ignoring_id is not None \
            and actual["duplicate_rows_ignoring_id"] != info.duplicate_rows_ignoring_id:
        out.append(Violation("duplicates", None, info.duplicate_rows_ignoring_id,
                             actual["duplicate_rows_ignoring_id"],
                             f"data has {actual['duplicate_rows_ignoring_id']} rows that repeat another row "
                             f"under a new id, contract expects {info.duplicate_rows_ignoring_id}"))
    if info.rows_in_duplicate_groups is not None \
            and actual["rows_in_duplicate_groups"] != info.rows_in_duplicate_groups:
        out.append(Violation("duplicates", None, info.rows_in_duplicate_groups,
                             actual["rows_in_duplicate_groups"],
                             f"data has {actual['rows_in_duplicate_groups']} rows with an exact or "
                             f"one-value-different copy, contract expects {info.rows_in_duplicate_groups}"))
    return out
