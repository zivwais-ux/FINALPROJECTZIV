"""Deterministic tools for the Data Scientist Crew.

The crew's only inputs are clean_data.csv and dataset_contract.json from
Crew 1. Agents decide and explain; these functions compute. Each public
function is plain Python (tested without an LLM) and has a thin CrewAI
@tool wrapper at the bottom of the file.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from crewai.tools import tool
from sklearn.base import clone
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

from churn_pipeline.contract.models import DatasetContract, load_contract
from churn_pipeline.contract.validator import validate_against_contract

# Team decisions for step 4: 80/20 split stratified on the target, fixed seed,
# and two model families that handle missing values natively (no imputation).
TEST_SIZE = 0.2
RANDOM_STATE = 42
CV_FOLDS = 5
THRESHOLD = 0.5
ONE_HOT_SEP = "="


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _r(x: float, ndigits: int = 4) -> float:
    return round(float(x), ndigits)


def _models() -> dict[str, Any]:
    return {
        "hist_gradient_boosting": HistGradientBoostingClassifier(random_state=RANDOM_STATE),
        "random_forest": RandomForestClassifier(n_estimators=300, random_state=RANDOM_STATE, n_jobs=-1),
    }


def _load_inputs(input_dir: str | Path) -> tuple[pd.DataFrame, DatasetContract, Path]:
    input_dir = Path(input_dir)
    path = input_dir / "clean_data.csv"
    return pd.read_csv(path), load_contract(input_dir / "dataset_contract.json"), path


# ----------------------------------------------------------- contract review

def review_contract(input_dir: str | Path) -> dict[str, Any]:
    """Validate clean_data.csv against dataset_contract.json and list what modeling may use."""
    df, contract, path = _load_inputs(input_dir)
    violations = validate_against_contract(df, contract, file_path=path)
    features = [c for c in contract.columns
                if c.role == "feature" and c.name not in contract.forbidden_features]
    return {
        "contract_version": contract.contract_version,
        "rows": int(len(df)),
        "passes": not violations,
        "violations": [v.to_dict() for v in violations],
        "target": {"name": contract.target.name, "expected_rate": contract.target.expected_rate},
        "forbidden_features": contract.forbidden_features,
        "features": [
            {"name": c.name, "dtype": c.dtype, "unit": c.unit, "unit_source": c.unit_source,
             "expected_null_count": c.expected_null_count,
             "allowed_values": c.allowed_values}
            for c in features
        ],
        "assumptions": contract.assumptions,
        "leakage_notes": contract.leakage_notes,
    }


# --------------------------------------------------------------- features

def build_features(input_dir: str | Path, output_dir: str | Path) -> dict[str, Any]:
    """Write features.csv: id, target and model features built only from the contract.

    Numeric features are copied unchanged, missing values included. Each
    category column becomes one 0/1 column per allowed value in the contract,
    so different spellings stay separate. Refuses to run when the data does
    not match the contract.
    """
    df, contract, path = _load_inputs(input_dir)
    violations = validate_against_contract(df, contract, file_path=path)
    if violations:
        raise ValueError("clean_data.csv does not match dataset_contract.json: "
                         + "; ".join(v.message for v in violations))

    id_cols = [c.name for c in contract.columns if c.role == "id"]
    target = contract.target.name
    out = df[id_cols + [target]].copy()
    sources = []
    for spec in contract.columns:
        if spec.role != "feature" or spec.name in contract.forbidden_features:
            continue
        if spec.dtype == "category":
            created = []
            for value in spec.allowed_values or []:
                name = f"{spec.name}{ONE_HOT_SEP}{value}"
                out[name] = (df[spec.name].astype(str) == value).astype(int)
                created.append(name)
            sources.append({"source": spec.name, "encoding": "one-hot", "columns": created})
        else:
            out[spec.name] = df[spec.name]
            sources.append({"source": spec.name, "encoding": "unchanged",
                            "missing_kept": int(df[spec.name].isna().sum())})

    feature_columns = [c for c in out.columns if c not in id_cols + [target]]
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_dir / "features.csv", index=False)
    summary = {
        "output": str(output_dir / "features.csv"),
        "rows": int(len(out)),
        "id_columns": id_cols,
        "target": target,
        "feature_count": len(feature_columns),
        "feature_columns": feature_columns,
        "missing_values_kept": int(out[feature_columns].isna().sum().sum()),
        "excluded": contract.forbidden_features,
        "sources": sources,
    }
    _write_json(output_dir / "feature_spec.json", summary)
    return summary


# --------------------------------------------------------- train & evaluate

def _test_metrics(y: pd.Series, proba: np.ndarray) -> dict[str, Any]:
    pred = (proba >= THRESHOLD).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    return {
        "pr_auc": _r(average_precision_score(y, proba)),
        "recall": _r(recall_score(y, pred, zero_division=0)),
        "precision": _r(precision_score(y, pred, zero_division=0)),
        "roc_auc": _r(roc_auc_score(y, proba)),
        "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
    }


def train_and_evaluate(output_dir: str | Path) -> dict[str, Any]:
    """Train both models on features.csv, pick one by cross-validated PR-AUC, evaluate on test.

    The model is chosen on the training split only; the test split is used
    once, after the choice, so test scores are an honest estimate. Writes
    model.joblib and evaluation_metrics.json.
    """
    output_dir = Path(output_dir)
    spec = json.loads((output_dir / "feature_spec.json").read_text(encoding="utf-8"))
    data = pd.read_csv(output_dir / "features.csv")
    X, y = data[spec["feature_columns"]], data[spec["target"]]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE)

    cv = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    candidates = {}
    fitted = {}
    for name, model in _models().items():
        scores = cross_val_score(clone(model), X_train, y_train, cv=cv, scoring="average_precision")
        model.fit(X_train, y_train)
        fitted[name] = model
        candidates[name] = {
            "cv_pr_auc_mean": _r(scores.mean()),
            "cv_pr_auc_std": _r(scores.std()),
            "test": _test_metrics(y_test, model.predict_proba(X_test)[:, 1]),
        }
    selected = max(candidates, key=lambda n: candidates[n]["cv_pr_auc_mean"])
    best = fitted[selected]

    imp = permutation_importance(best, X_test, y_test, scoring="average_precision",
                                 n_repeats=5, random_state=RANDOM_STATE, n_jobs=-1)
    order = np.argsort(imp.importances_mean)[::-1][:10]
    top = [{"feature": X.columns[i], "pr_auc_drop": _r(imp.importances_mean[i])} for i in order]

    joblib.dump({"model": best, "model_name": selected, "feature_columns": spec["feature_columns"],
                 "target": spec["target"], "threshold": THRESHOLD}, output_dir / "model.joblib")
    metrics = {
        "split": {"test_size": TEST_SIZE, "stratified_on": spec["target"], "random_state": RANDOM_STATE,
                  "train_rows": int(len(X_train)), "test_rows": int(len(X_test)),
                  "train_churn_rate": _r(y_train.mean()), "test_churn_rate": _r(y_test.mean())},
        "selection_rule": f"highest mean PR-AUC over {CV_FOLDS}-fold stratified CV on the training split",
        "threshold": THRESHOLD,
        "baseline_pr_auc": _r(y_test.mean()),
        "candidates": candidates,
        "selected_model": selected,
        "selected_test_metrics": candidates[selected]["test"],
        "top_features_by_permutation": top,
        "model_file": str(output_dir / "model.joblib"),
    }
    _write_json(output_dir / "evaluation_metrics.json", metrics)
    return metrics


def read_model_facts(input_dir: str | Path, output_dir: str | Path) -> dict[str, Any]:
    """Everything the model card needs: contract text, feature summary and metrics."""
    contract = load_contract(Path(input_dir) / "dataset_contract.json")
    output_dir = Path(output_dir)
    return {
        "contract_version": contract.contract_version,
        "dataset": contract.dataset.model_dump(),
        "target": contract.target.model_dump(),
        "assumed_units": {c.name: c.unit for c in contract.columns if c.unit_source == "assumed"},
        "assumptions": contract.assumptions,
        "leakage_notes": contract.leakage_notes,
        "features": json.loads((output_dir / "feature_spec.json").read_text(encoding="utf-8")),
        "metrics": json.loads((output_dir / "evaluation_metrics.json").read_text(encoding="utf-8")),
    }


# ------------------------------------------------------- CrewAI tool wrappers

@tool("review_contract")
def review_contract_tool(input_dir: str) -> str:
    """Validate input_dir/clean_data.csv against input_dir/dataset_contract.json.
    Returns as JSON whether it passes, every violation, the target, the usable
    features with units, the forbidden features, assumptions and leakage notes."""
    return json.dumps(review_contract(input_dir), ensure_ascii=False)


@tool("build_features")
def build_features_tool(input_dir: str, output_dir: str) -> str:
    """Build output_dir/features.csv from input_dir/clean_data.csv using only the contract:
    numeric features unchanged (missing values kept), one 0/1 column per allowed category
    value. Refuses if the data does not match the contract. Returns the feature summary as JSON."""
    return json.dumps(build_features(input_dir, output_dir), ensure_ascii=False)


@tool("train_and_evaluate")
def train_and_evaluate_tool(output_dir: str) -> str:
    """Train HistGradientBoosting and RandomForest on output_dir/features.csv (80/20 stratified
    split), select one by cross-validated PR-AUC on the training split, evaluate it on the test
    split and save model.joblib. Returns all metrics as JSON."""
    return json.dumps(train_and_evaluate(output_dir), ensure_ascii=False)


@tool("read_model_facts")
def read_model_facts_tool(input_dir: str, output_dir: str) -> str:
    """Return as JSON everything a model card needs: the contract's dataset, target, assumed
    units, assumptions and leakage notes, the feature summary and the evaluation metrics."""
    return json.dumps(read_model_facts(input_dir, output_dir), ensure_ascii=False)
