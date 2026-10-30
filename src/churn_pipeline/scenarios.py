"""Ways to break the Crew 1 -> Crew 2 handoff, shared by scripts/break_it.py and the web app.

No crewai import here, so the app can use the scenarios without loading agents.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import pandas as pd


@dataclass(frozen=True)
class Scenario:
    description: str
    change: Callable[[pd.DataFrame], pd.DataFrame]
    # The gate that must fail, and text its problems must contain.
    expected_gate: str
    expected_text: str


def _set(df: pd.DataFrame, column: str, value) -> pd.DataFrame:
    df = df.copy()
    df[column] = df[column].astype(object)
    df.loc[0, column] = value
    return df


SCENARIOS: dict[str, Scenario] = {
    "unit_change": Scenario(
        "CashbackAmount switched from INR to paise (x100), the Harbor & Vale incident",
        lambda df: df.assign(CashbackAmount=df["CashbackAmount"] * 100),
        "contract_vs_data", "possible unit change"),
    "rename_column": Scenario(
        "Tenure renamed to TenureMonths upstream",
        lambda df: df.rename(columns={"Tenure": "TenureMonths"}),
        "contract_vs_data", "possible rename"),
    "out_of_range": Scenario(
        "one SatisfactionScore of 6 on a 1-5 scale",
        lambda df: _set(df, "SatisfactionScore", 6),
        "contract_vs_data", "SatisfactionScore ranges 1..6"),
    "bad_category": Scenario(
        "a new payment spelling, 'credit card', that the contract does not allow",
        lambda df: _set(df, "PreferredPaymentMode", "credit card"),
        "contract_vs_data", "values not allowed by the contract: ['credit card']"),
    "missing_feature": Scenario(
        "the Complain column dropped from the handoff file",
        lambda df: df.drop(columns="Complain"),
        "required_features", "required feature 'Complain' is not in clean_data.csv"),
}
