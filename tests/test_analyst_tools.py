"""Data Analyst Crew tools, tested without an LLM."""
import json
from pathlib import Path

import pandas as pd
import pytest

from churn_pipeline.contract import load_contract
from churn_pipeline.tools.analyst_tools import (
    build_contract,
    export_clean_data,
    finalize_contract,
    profile_raw_data,
    run_eda,
)

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "E Commerce Dataset.xlsx"
SPEC = Path(__file__).parent / "fixtures" / "contract_v1.json"


@pytest.fixture(scope="module")
def out(tmp_path_factory) -> Path:
    d = tmp_path_factory.mktemp("crew1")
    export_clean_data(RAW, d)
    build_contract(d)
    return d


def _descriptions(out: Path) -> dict[str, str]:
    numbers = json.loads((out / "contract_numbers.json").read_text())
    return {c["name"]: f"Description of {c['name']}" for c in numbers["columns"]}


def test_profile_matches_data_profile(tmp_path):
    report = profile_raw_data(RAW, tmp_path)
    assert (tmp_path / "quality_report.json").is_file()
    assert report["rows"] == 5630
    assert report["duplicate_rows"] == 0
    assert report["id_unique"] is True
    assert report["rows_with_any_missing"] == 1856
    assert report["max_missing_per_row"] == 1
    assert report["target"] == {"name": "Churn", "positives": 948, "rate": 0.1684}
    missing = {m["column"]: m["missing"] for m in report["missing"]}
    assert missing == {"Tenure": 264, "WarehouseToHome": 251, "HourSpendOnApp": 255,
                       "OrderAmountHikeFromlastYear": 265, "CouponUsed": 256,
                       "OrderCount": 258, "DaySinceLastOrder": 307}
    phone = next(c for c in report["categories"]["PreferredLoginDevice"] if c["value"] == "Phone")
    assert phone == {"value": "Phone", "count": 1231, "churn_rate": 0.2242}


def test_export_is_identical_to_raw(out):
    result = export_clean_data(RAW, out)
    assert result["identical_to_raw"] is True
    assert result["differences"] == []
    assert result["missing_values_kept"] == 1856
    clean = pd.read_csv(out / "clean_data.csv")
    raw = pd.read_excel(RAW, sheet_name="E Comm")
    assert sorted(clean["PreferredPaymentMode"].unique()) == sorted(raw["PreferredPaymentMode"].unique())


def test_export_is_deterministic(out, tmp_path):
    assert export_clean_data(RAW, tmp_path)["sha256"] == export_clean_data(RAW, out)["sha256"]


def test_build_contract_numbers_match_the_spec(out):
    numbers = json.loads((out / "contract_numbers.json").read_text())
    spec = load_contract(SPEC)
    assert numbers["dataset"]["row_count"] == spec.dataset.row_count
    assert numbers["target"]["expected_rate"] == spec.target.expected_rate
    for col in numbers["columns"]:
        expected = spec.column(col["name"])
        assert col["role"] == expected.role, col["name"]
        assert col["dtype"] == expected.dtype, col["name"]
        assert col["expected_null_count"] == expected.expected_null_count, col["name"]
        assert col.get("allowed_values") == expected.allowed_values, col["name"]
        if expected.range:
            assert col["range"] == expected.range.model_dump(), col["name"]
        if expected.expected_mean is not None:
            assert col["expected_mean"] == pytest.approx(expected.expected_mean, abs=1e-4), col["name"]
            assert col["unit"] == expected.unit, col["name"]
            assert col["unit_source"] == expected.unit_source, col["name"]


def test_finalize_contract_writes_a_contract_that_passes(out):
    contract = finalize_contract(out, _descriptions(out), ["No imputation"], ["Churn window undefined"])
    assert (out / "dataset_contract.json").is_file()
    assert contract.dataset.sha256
    assert contract.column("Tenure").description == "Description of Tenure"


def test_finalize_contract_requires_every_description(out):
    descriptions = _descriptions(out)
    del descriptions["Tenure"]
    with pytest.raises(ValueError, match="Tenure"):
        finalize_contract(out, descriptions, ["a"], ["b"])


def test_finalize_contract_refuses_data_changed_after_build(tmp_path):
    export_clean_data(RAW, tmp_path)
    build_contract(tmp_path)
    df = pd.read_csv(tmp_path / "clean_data.csv")
    df["CashbackAmount"] = df["CashbackAmount"] * 100
    df.to_csv(tmp_path / "clean_data.csv", index=False)
    with pytest.raises(ValueError, match="possible unit change"):
        finalize_contract(tmp_path, _descriptions(tmp_path), ["a"], ["b"])
    assert not (tmp_path / "dataset_contract.json").exists()


def test_run_eda_writes_report(out):
    result = run_eda(out)
    html = (out / "eda_report.html").read_text()
    assert html.count("<img") >= 10
    assert result["overall_churn_rate"] == 0.1684
    tenure = result["churn_by_group"]["Tenure (months, binned)"]
    assert [g["group"] for g in tenure] == ["0-1", "2-5", "6-10", "11-20", "21+", "missing"]
    assert sum(g["count"] for g in tenure) == 5630
