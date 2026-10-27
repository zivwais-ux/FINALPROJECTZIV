"""Data Scientist Crew tools, tested without an LLM."""
import json
from pathlib import Path

import joblib
import pandas as pd
import pytest

from churn_pipeline.tools.analyst_tools import build_contract, export_clean_data, finalize_contract
from churn_pipeline.tools.scientist_tools import (
    QUALITY_THRESHOLDS,
    build_features,
    read_model_facts,
    review_contract,
    train_and_evaluate,
)

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "E Commerce Dataset.xlsx"


def _crew1(d: Path) -> Path:
    export_clean_data(RAW, d)
    numbers = build_contract(d)
    finalize_contract(d, {c["name"]: f"Description of {c['name']}" for c in numbers["columns"]},
                      ["No imputation"], ["Churn window undefined"])
    return d


@pytest.fixture(scope="module")
def crew1(tmp_path_factory) -> Path:
    return _crew1(tmp_path_factory.mktemp("crew1"))


@pytest.fixture(scope="module")
def crew2(crew1, tmp_path_factory) -> Path:
    d = tmp_path_factory.mktemp("crew2")
    build_features(crew1, d)
    train_and_evaluate(d)
    return d


def test_review_contract_passes_and_lists_features(crew1):
    review = review_contract(crew1)
    assert review["passes"] is True
    assert review["violations"] == []
    assert len(review["features"]) == 18
    assert review["forbidden_features"] == ["CustomerID"]
    assert review["duplicate_rows_ignoring_id"] == 556


def test_features_follow_the_contract(crew1, crew2):
    spec = json.loads((crew2 / "feature_spec.json").read_text())
    features = pd.read_csv(crew2 / "features.csv")
    assert len(features) == 5630
    assert "CustomerID" not in spec["feature_columns"]
    assert "duplicate_group" not in spec["feature_columns"]
    # Every spelling keeps its own column: nothing is merged.
    assert {"PreferredPaymentMode=COD", "PreferredPaymentMode=Cash on Delivery",
            "PreferredLoginDevice=Phone", "PreferredLoginDevice=Mobile Phone"} <= set(spec["feature_columns"])
    # Missing values stay missing: nothing is imputed.
    assert spec["missing_values_kept"] == 1856
    assert features["Tenure"].isna().sum() == 264
    assert spec["rows_in_duplicate_groups"] == 3472


def test_build_features_refuses_data_that_breaks_the_contract(tmp_path):
    d = _crew1(tmp_path / "crew1")
    df = pd.read_csv(d / "clean_data.csv")
    df["CashbackAmount"] = df["CashbackAmount"] * 100
    df.to_csv(d / "clean_data.csv", index=False)
    with pytest.raises(ValueError, match="possible unit change"):
        build_features(d, tmp_path / "crew2")
    assert not (tmp_path / "crew2" / "features.csv").exists()


def test_split_keeps_duplicates_on_one_side(crew2):
    split = json.loads((crew2 / "evaluation_metrics.json").read_text())["split"]
    assert split["duplicate_groups_on_both_sides"] == 0
    assert split["test_share"] == pytest.approx(0.2, abs=0.01)
    assert split["test_churn_rate"] == pytest.approx(0.1684, abs=0.005)


def test_model_meets_the_quality_thresholds(crew2):
    metrics = json.loads((crew2 / "evaluation_metrics.json").read_text())
    assert set(metrics["candidates"]) == {"hist_gradient_boosting", "random_forest"}
    assert metrics["selected_model"] in metrics["candidates"]
    test = metrics["selected_test_metrics"]
    assert metrics["meets_quality_thresholds"] is True
    assert test["pr_auc"] >= QUALITY_THRESHOLDS["pr_auc"]
    assert test["recall"] >= QUALITY_THRESHOLDS["recall"]
    assert test["pr_auc"] > metrics["baseline_pr_auc"]


def test_training_is_deterministic(crew1, crew2, tmp_path):
    build_features(crew1, tmp_path)
    again = train_and_evaluate(tmp_path)
    first = json.loads((crew2 / "evaluation_metrics.json").read_text())
    assert again["candidates"] == first["candidates"]


def test_saved_model_predicts_from_features(crew2):
    bundle = joblib.load(crew2 / "model.joblib")
    features = pd.read_csv(crew2 / "features.csv")
    proba = bundle["model"].predict_proba(features[bundle["feature_columns"]])[:, 1]
    assert len(proba) == 5630
    assert ((proba >= 0) & (proba <= 1)).all()


def test_model_facts_carry_contract_text_and_metrics(crew1, crew2):
    facts = read_model_facts(crew1, crew2)
    assert facts["assumed_units"] == {"Tenure": "months", "WarehouseToHome": "km",
                                      "CashbackAmount": "INR (last month average)"}
    assert facts["leakage_notes"] == ["Churn window undefined"]
    assert facts["metrics"]["selected_model"] in ("hist_gradient_boosting", "random_forest")
