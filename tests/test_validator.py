"""The real data passes the contract, and each check catches its own breakage."""
from pathlib import Path

import pandas as pd
import pytest
from pydantic import ValidationError

from churn_pipeline.contract import (
    DatasetContract,
    file_sha256,
    load_contract,
    validate_against_contract,
)

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "E Commerce Dataset.xlsx"
CONTRACT = Path(__file__).parent / "fixtures" / "contract_v1.json"


@pytest.fixture(scope="session")
def raw_df() -> pd.DataFrame:
    return pd.read_excel(RAW, sheet_name="E Comm")


@pytest.fixture
def df(raw_df) -> pd.DataFrame:
    return raw_df.copy()


@pytest.fixture
def contract() -> DatasetContract:
    return load_contract(CONTRACT)


def checks(violations) -> set[tuple[str, str | None]]:
    return {(v.check, v.column) for v in violations}


def test_real_data_passes(df, contract):
    assert validate_against_contract(df, contract) == []


def test_renamed_column(df, contract):
    df = df.rename(columns={"Tenure": "tenure_months"})
    v = validate_against_contract(df, contract)
    assert ("columns", "Tenure") in checks(v)
    assert ("columns", "tenure_months") in checks(v)
    assert "possible rename" in next(x for x in v if x.column == "Tenure").message


def test_fractional_value_in_int_column(df, contract):
    df["OrderCount"] = df["OrderCount"].astype(float)
    df.loc[df["OrderCount"].notna().idxmax(), "OrderCount"] += 0.5
    assert ("dtype", "OrderCount") in checks(validate_against_contract(df, contract))


def test_text_in_numeric_column(df, contract):
    df["SatisfactionScore"] = df["SatisfactionScore"].astype(str)
    assert ("dtype", "SatisfactionScore") in checks(validate_against_contract(df, contract))


def test_silent_imputation_changes_null_count(df, contract):
    df["Tenure"] = df["Tenure"].fillna(df["Tenure"].median())
    assert ("nulls", "Tenure") in checks(validate_against_contract(df, contract))


def test_unknown_category(df, contract):
    df.loc[0, "PreferredLoginDevice"] = "Tablet"
    v = validate_against_contract(df, contract)
    assert ("allowed_values", "PreferredLoginDevice") in checks(v)


def test_merged_category_not_caught_by_allowed_values(df, contract):
    # Known gap: merging Phone into Mobile Phone keeps every value inside
    # allowed_values, so no column check sees it. On this data the merge makes
    # one more row a copy of another, so the duplicate check notices, without
    # naming the column.
    df["PreferredLoginDevice"] = df["PreferredLoginDevice"].replace({"Phone": "Mobile Phone"})
    found = checks(validate_against_contract(df, contract))
    assert ("allowed_values", "PreferredLoginDevice") not in found
    assert ("duplicates", None) in found


def test_removed_duplicates(df, contract):
    deduped = df.drop_duplicates(subset=[c for c in df.columns if c != "CustomerID"])
    violations = [v for v in validate_against_contract(deduped, contract) if v.check == "duplicates"]
    assert [(v.expected, v.actual) for v in violations] == [(556, 0), (3472, 2360)]


def test_changed_value_in_a_duplicate_pair(df, contract):
    # Same row count and the value stays in range; only the duplicate counts move.
    data = df.drop(columns="CustomerID")
    i = data.index[data.duplicated()][0]
    df.loc[i, "CashbackAmount"] = df.loc[i, "CashbackAmount"] + 0.01
    assert ("duplicates", None) in checks(validate_against_contract(df, contract))


def test_out_of_range(df, contract):
    df.loc[0, "NumberOfAddress"] = -1
    assert ("range", "NumberOfAddress") in checks(validate_against_contract(df, contract))


def test_unit_change_is_reported(df, contract):
    df["CashbackAmount"] = df["CashbackAmount"] * 100
    v = validate_against_contract(df, contract)
    assert ("mean_drift", "CashbackAmount") in checks(v)
    assert ("range", "CashbackAmount") in checks(v)
    drift = next(x for x in v if x.check == "mean_drift")
    assert "possible unit change" in drift.message


def test_small_drift_beyond_tolerance(df, contract):
    df["CashbackAmount"] = df["CashbackAmount"] * 0.97
    v = validate_against_contract(df, contract)
    drift = next(x for x in v if x.check == "mean_drift")
    assert "possible unit change" not in drift.message


def test_dropped_rows(df, contract):
    v = validate_against_contract(df.iloc[:-100], contract)
    assert ("row_count", None) in checks(v)


def test_target_rate_change(df, contract):
    churners = df.index[df["Churn"] == 1][:50]
    df.loc[churners, "Churn"] = 0
    assert ("target_rate", "Churn") in checks(validate_against_contract(df, contract))


def test_duplicate_id(df, contract):
    df.loc[1, "CustomerID"] = df.loc[0, "CustomerID"]
    assert ("unique", "CustomerID") in checks(validate_against_contract(df, contract))


def test_sha256_mismatch(df, contract, tmp_path):
    path = tmp_path / "clean_data.csv"
    df.to_csv(path, index=False)
    contract.dataset.sha256 = file_sha256(path)
    assert validate_against_contract(df, contract, file_path=path) == []

    df.loc[0, "CashbackAmount"] += 0.01
    df.to_csv(path, index=False)
    assert ("sha256", None) in checks(validate_against_contract(df, contract, file_path=path))


def test_all_violations_reported_together(df, contract):
    df = df.rename(columns={"Tenure": "tenure_months"})
    df["CashbackAmount"] = df["CashbackAmount"] * 100
    df.loc[0, "Gender"] = "Unknown"
    found = {check for check, _ in checks(validate_against_contract(df, contract))}
    assert {"columns", "mean_drift", "allowed_values"} <= found


def test_contract_rejects_category_without_allowed_values():
    data = CONTRACT.read_text()
    bad = data.replace('"allowed_values": [\n        "Female",\n        "Male"\n      ]', '"allowed_values": null')
    assert bad != data
    with pytest.raises(ValidationError):
        DatasetContract.model_validate_json(bad)


def test_contract_rejects_unknown_target(contract):
    payload = contract.model_dump()
    payload["target"]["name"] = "NotAColumn"
    with pytest.raises(ValidationError):
        DatasetContract.model_validate(payload)
