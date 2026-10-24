"""List every missing value in the raw dataset (read-only).

Writes docs/missing_values.csv with one row per missing cell:
CustomerID, column. Nothing is imputed or changed.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "E Commerce Dataset.xlsx"
OUT = ROOT / "docs" / "missing_values.csv"


def main() -> None:
    df = pd.read_excel(RAW, sheet_name="E Comm")
    missing = (
        df.set_index("CustomerID")
        .isna()
        .stack()
        .loc[lambda s: s]
        .reset_index()
        .rename(columns={"level_1": "column"})[["CustomerID", "column"]]
        .sort_values(["column", "CustomerID"])
    )
    OUT.parent.mkdir(exist_ok=True)
    missing.to_csv(OUT, index=False)
    print(f"{len(missing)} missing cells in {missing['CustomerID'].nunique()} rows -> {OUT.relative_to(ROOT)}")
    print(missing["column"].value_counts().to_string())


if __name__ == "__main__":
    main()
