"""Deterministic tools for the Data Analyst Crew.

Agents decide and explain; these functions compute. Each public function
is plain Python (tested without an LLM) and has a thin CrewAI @tool
wrapper at the bottom of the file.
"""
from __future__ import annotations

import base64
import io
import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402
from crewai.tools import tool  # noqa: E402

from churn_pipeline.contract.duplicates import duplicate_counts, duplicate_groups  # noqa: E402
from churn_pipeline.contract.models import DatasetContract  # noqa: E402
from churn_pipeline.contract.validator import file_sha256, validate_against_contract  # noqa: E402

SHEET = "E Comm"
TARGET = "Churn"
ID_COLUMN = "CustomerID"
OUTLIER_IQR_FACTOR = 3.0

# Team decisions from docs/contract_spec.md: units the data dictionary
# states, plus three units that are assumed because the source omits them.
UNITS: dict[str, tuple[str, str]] = {
    "Churn": ("flag", "data_dict"),
    "Tenure": ("months", "assumed"),
    "CityTier": ("tier", "data_dict"),
    "WarehouseToHome": ("km", "assumed"),
    "HourSpendOnApp": ("hours", "data_dict"),
    "NumberOfDeviceRegistered": ("count", "data_dict"),
    "SatisfactionScore": ("score", "data_dict"),
    "NumberOfAddress": ("count", "data_dict"),
    "Complain": ("flag (last month)", "data_dict"),
    "OrderAmountHikeFromlastYear": ("percent", "data_dict"),
    "CouponUsed": ("count (last month)", "data_dict"),
    "OrderCount": ("count (last month)", "data_dict"),
    "DaySinceLastOrder": ("days", "data_dict"),
    "CashbackAmount": ("INR (last month average)", "assumed"),
}


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _r(x: float, ndigits: int = 4) -> float:
    return round(float(x), ndigits)


def read_raw(raw_path: str | Path) -> pd.DataFrame:
    return pd.read_excel(raw_path, sheet_name=SHEET)


def read_clean(output_dir: str | Path) -> pd.DataFrame:
    return pd.read_csv(Path(output_dir) / "clean_data.csv")


# ---------------------------------------------------------------- profiling

def profile_raw_data(raw_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    """Quality report of the raw sheet; writes quality_report.json."""
    df = read_raw(raw_path)
    y = df[TARGET]
    nulls_per_row = df.isna().sum(axis=1)

    missing = []
    for col in df.columns:
        m = df[col].isna()
        if m.any():
            missing.append({
                "column": col,
                "missing": int(m.sum()),
                "share": _r(m.mean()),
                "churn_rate_when_missing": _r(y[m].mean()),
                "churn_rate_when_present": _r(y[~m].mean()),
            })

    categories = {}
    for col in df.select_dtypes(exclude="number").columns:
        g = df.groupby(col)[TARGET].agg(["count", "mean"])
        categories[col] = [
            {"value": str(v), "count": int(r["count"]), "churn_rate": _r(r["mean"])}
            for v, r in g.iterrows()
        ]

    outliers = []
    for col in df.select_dtypes(include="number").columns:
        if col in (TARGET, ID_COLUMN):
            continue
        s = df[col].dropna()
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        lo, hi = q1 - OUTLIER_IQR_FACTOR * (q3 - q1), q3 + OUTLIER_IQR_FACTOR * (q3 - q1)
        out = s[(s < lo) | (s > hi)]
        if len(out):
            outliers.append({
                "column": col,
                "rule": f"outside Q1-{OUTLIER_IQR_FACTOR:g}*IQR .. Q3+{OUTLIER_IQR_FACTOR:g}*IQR",
                "fence": [_r(lo), _r(hi)],
                "count": int(len(out)),
                "values": sorted({_r(v) for v in out}),
                "median": _r(s.median()),
            })

    report = {
        "source": str(raw_path),
        "sheet": SHEET,
        "rows": int(len(df)),
        "columns": int(df.shape[1]),
        "duplicate_rows": int(df.duplicated().sum()),
        "id_unique": bool(df[ID_COLUMN].is_unique),
        # duplicate_rows compares whole rows, and the id makes every row unique;
        # these counts ignore the id. See contract/duplicates.py.
        "duplicates_ignoring_id": {
            **duplicate_counts(df, [ID_COLUMN]),
            "churn_rate_in_duplicate_groups": _r(y[pd.Series(
                duplicate_groups(df, [ID_COLUMN])).duplicated(keep=False).to_numpy()].mean()),
        },
        "rows_with_any_missing": int((nulls_per_row > 0).sum()),
        "max_missing_per_row": int(nulls_per_row.max()),
        "target": {"name": TARGET, "positives": int(y.sum()), "rate": _r(y.mean())},
        "missing": missing,
        "categories": categories,
        "outliers": outliers,
    }
    _write_json(Path(output_dir) / "quality_report.json", report)
    return report


# ------------------------------------------------------------------- export

def export_clean_data(raw_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    """Write clean_data.csv unchanged and prove it matches the raw sheet cell by cell."""
    raw = read_raw(raw_path)
    out = Path(output_dir) / "clean_data.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    raw.to_csv(out, index=False)

    back = pd.read_csv(out)
    differences = []
    if list(back.columns) != list(raw.columns):
        differences.append({"column": None, "issue": "column names or order differ"})
    if len(back) != len(raw):
        differences.append({"column": None, "issue": f"row count {len(back)} vs {len(raw)}"})
    if not differences:
        for col in raw.columns:
            a, b = raw[col], back[col]
            null_diff = int((a.isna() != b.isna()).sum())
            both = a.notna() & b.notna()
            if pd.api.types.is_numeric_dtype(a) and pd.api.types.is_numeric_dtype(b):
                value_diff = int((a[both].astype(float) != b[both].astype(float)).sum())
            else:
                value_diff = int((a[both].astype(str) != b[both].astype(str)).sum())
            if null_diff or value_diff:
                differences.append({"column": col, "missing_changed": null_diff, "values_changed": value_diff})

    return {
        "output": str(out),
        "rows": int(len(back)),
        "columns": int(back.shape[1]),
        "missing_values_kept": int(back.isna().sum().sum()),
        "identical_to_raw": not differences,
        "differences": differences,
        "sha256": file_sha256(out),
    }


# ---------------------------------------------------------------------- EDA

def _fig_to_img(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight", metadata={"Software": None})
    plt.close(fig)
    return f'<img alt="chart" src="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}">'


def _churn_by(df: pd.DataFrame, col: str) -> list[dict[str, Any]]:
    g = df.groupby(col, dropna=False, observed=True)[TARGET].agg(["count", "mean"])
    return [
        {"group": "missing" if pd.isna(v) else (str(int(v)) if isinstance(v, float) and v.is_integer() else str(v)),
         "count": int(r["count"]), "churn_rate": _r(r["mean"])}
        for v, r in g.iterrows()
    ]


def run_eda(output_dir: str | Path) -> dict[str, Any]:
    """Descriptive stats and charts from clean_data.csv; writes eda_report.html."""
    df = read_clean(output_dir)
    sns.set_theme(style="whitegrid")
    categorical = list(df.select_dtypes(exclude="number").columns)
    discrete = ["CityTier", "SatisfactionScore", "Complain", "NumberOfDeviceRegistered", "HourSpendOnApp"]
    numeric = [c for c in df.select_dtypes(include="number").columns
               if c not in (TARGET, ID_COLUMN, *discrete)]

    tenure_bins = pd.cut(df["Tenure"], bins=[-0.1, 1, 5, 10, 20, 61],
                         labels=["0-1", "2-5", "6-10", "11-20", "21+"])
    tenure_bins = tenure_bins.cat.add_categories("missing").fillna("missing")
    churn_by_group = {c: _churn_by(df, c) for c in categorical + discrete}
    churn_by_group["Tenure (months, binned)"] = _churn_by(df.assign(_t=tenure_bins), "_t")

    sections = []
    overall = df[TARGET].mean()
    sections.append(f"<h2>Overview</h2><p>{len(df):,} customers, {df.shape[1]} columns. "
                    f"Churn rate {overall:.2%} ({int(df[TARGET].sum())} churned).</p>")
    sections.append("<h2>Descriptive statistics</h2>" +
                    df.drop(columns=[ID_COLUMN]).describe().T.round(2).to_html(classes="tbl"))

    miss = df.isna().sum()
    miss = miss[miss > 0].sort_values()
    fig, ax = plt.subplots(figsize=(7, 3.2))
    miss.plot.barh(ax=ax, color="#7a8fb3")
    ax.set_title("Missing values per column (kept as missing)")
    ax.set_xlabel("rows")
    sections.append("<h2>Missing values</h2>" + _fig_to_img(fig))

    sections.append("<h2>Churn rate by group</h2>")
    for col in categorical + discrete:
        rows = pd.DataFrame(churn_by_group[col])
        fig, ax = plt.subplots(figsize=(7, 0.45 * len(rows) + 1.2))
        sns.barplot(data=rows, y="group", x="churn_rate", ax=ax, color="#4c72b0", orient="h")
        ax.axvline(overall, color="#c44e52", ls="--", lw=1, label=f"overall {overall:.1%}")
        ax.set_title(col)
        ax.set_xlabel("churn rate")
        ax.set_ylabel("")
        ax.legend(loc="lower right")
        sections.append(_fig_to_img(fig) + rows.to_html(index=False, classes="tbl"))

    sections.append("<h2>Distributions by churn</h2>")
    for col in numeric:
        fig, ax = plt.subplots(figsize=(7, 3))
        sns.histplot(data=df, x=col, hue=TARGET, stat="density", common_norm=False,
                     element="step", ax=ax, bins=30)
        ax.set_title(f"{col} (missing values excluded)")
        sections.append(_fig_to_img(fig))

    corr = df.drop(columns=[ID_COLUMN]).select_dtypes(include="number").corr()
    # Drawn with plain matplotlib: seaborn.heatmap calls Colormap.set_bad, which
    # is deprecated in matplotlib 3.11, and the deprecation warning crashes under
    # CrewAI's patched warnings.warn.
    fig, ax = plt.subplots(figsize=(9, 7))
    im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr)), corr.columns, rotation=90, fontsize=7)
    ax.set_yticks(range(len(corr)), corr.index, fontsize=7)
    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, f"{corr.iat[i, j]:.2f}", ha="center", va="center", fontsize=5)
    ax.grid(False)
    fig.colorbar(im, ax=ax, shrink=0.8)
    ax.set_title("Correlation (pairwise, missing values excluded)")
    sections.append("<h2>Correlations</h2>" + _fig_to_img(fig))

    html = ("<!doctype html><html lang='en'><head><meta charset='utf-8'><title>EDA report</title>"
            "<style>body{font-family:sans-serif;max-width:900px;margin:auto;padding:16px}"
            "img{max-width:100%}.tbl{border-collapse:collapse;font-size:12px;margin:8px 0 20px}"
            ".tbl td,.tbl th{border:1px solid #ccc;padding:3px 6px}</style></head><body>"
            "<h1>E-commerce churn: exploratory analysis</h1>" + "".join(sections) + "</body></html>")
    out = Path(output_dir) / "eda_report.html"
    out.write_text(html, encoding="utf-8")
    return {"report": str(out), "rows": int(len(df)), "overall_churn_rate": _r(overall),
            "churn_by_group": churn_by_group,
            "duplicates_ignoring_id": duplicate_counts(df, [ID_COLUMN])["summary"]}


# ----------------------------------------------------------------- contract

def build_contract(output_dir: str | Path) -> dict[str, Any]:
    """Compute every number of the contract from clean_data.csv; writes contract_numbers.json."""
    path = Path(output_dir) / "clean_data.csv"
    df = pd.read_csv(path)
    columns = []
    for col in df.columns:
        s = df[col]
        values = s.dropna()
        spec: dict[str, Any] = {"name": col, "expected_null_count": int(s.isna().sum())}
        if col == ID_COLUMN:
            spec.update(role="id", dtype="int", unique=True,
                        range={"min": _r(values.min()), "max": _r(values.max())})
        elif not pd.api.types.is_numeric_dtype(s):
            spec.update(role="feature", dtype="category",
                        allowed_values=sorted(values.astype(str).unique().tolist()))
        else:
            is_int = bool((values == values.round()).all())
            binary = is_int and set(values.unique()) <= {0, 1}
            spec.update(role="target" if col == TARGET else "feature",
                        dtype="binary" if binary else ("int" if is_int else "float"),
                        range={"min": _r(values.min()), "max": _r(values.max())},
                        expected_mean=_r(values.mean()), expected_std=_r(values.std()))
            if col in UNITS:
                spec["unit"], spec["unit_source"] = UNITS[col]
        columns.append(spec)

    numbers = {
        "dataset": {"name": "ecommerce_churn", "file": "clean_data.csv",
                    "sha256": file_sha256(path), "row_count": int(len(df)),
                    **{k: v for k, v in duplicate_counts(df, [ID_COLUMN]).items()
                       if k in ("duplicate_rows_ignoring_id", "rows_in_duplicate_groups")}},
        "target": {"name": TARGET, "positive_class": 1, "expected_rate": _r(df[TARGET].mean())},
        "tolerances": {"mean_rel": 0.01, "target_rate_rel": 0.01, "unit_change_factor": 10},
        "forbidden_features": [ID_COLUMN],
        "columns": columns,
    }
    _write_json(Path(output_dir) / "contract_numbers.json", numbers)
    return numbers


def finalize_contract(output_dir: str | Path, column_descriptions: dict[str, str],
                      assumptions: list[str], leakage_notes: list[str],
                      version: str = "1.0.0") -> DatasetContract:
    """Merge the steward's text into the tool's numbers, validate, write dataset_contract.json.

    Raises ValueError when a description is missing or the contract does not
    match clean_data.csv.
    """
    output_dir = Path(output_dir)
    numbers = json.loads((output_dir / "contract_numbers.json").read_text(encoding="utf-8"))
    names = [c["name"] for c in numbers["columns"]]
    missing = [n for n in names if not column_descriptions.get(n, "").strip()]
    if missing:
        raise ValueError(f"contract steward gave no description for: {missing}")
    columns = [{**c, "description": column_descriptions[c["name"]].strip()} for c in numbers["columns"]]

    contract = DatasetContract.model_validate({
        "contract_version": version, **numbers, "columns": columns,
        "assumptions": assumptions, "leakage_notes": leakage_notes,
    })
    clean = output_dir / "clean_data.csv"
    violations = validate_against_contract(pd.read_csv(clean), contract, file_path=clean)
    if violations:
        raise ValueError("new contract does not match clean_data.csv: "
                         + "; ".join(v.message for v in violations))
    (output_dir / "dataset_contract.json").write_text(
        contract.model_dump_json(indent=2) + "\n", encoding="utf-8")
    return contract


# ------------------------------------------------------- CrewAI tool wrappers

@tool("profile_raw_data")
def profile_raw_data_tool(raw_path: str, output_dir: str) -> str:
    """Profile the raw Excel dataset (sheet "E Comm"): missing values with churn rates,
    category spellings with counts and churn rates, outliers, duplicates and target rate.
    Writes quality_report.json to output_dir and returns the report as JSON."""
    return json.dumps(profile_raw_data(raw_path, output_dir), ensure_ascii=False)


@tool("export_clean_data")
def export_clean_data_tool(raw_path: str, output_dir: str) -> str:
    """Write clean_data.csv to output_dir as an unchanged copy of the raw sheet "E Comm",
    re-read it and compare it to the raw data cell by cell. Returns the comparison result
    (identical_to_raw, differences) and the file's sha256 as JSON."""
    return json.dumps(export_clean_data(raw_path, output_dir), ensure_ascii=False)


@tool("run_eda")
def run_eda_tool(output_dir: str) -> str:
    """Run exploratory analysis on output_dir/clean_data.csv. Writes eda_report.html with
    statistics and charts, and returns churn rates by group as JSON."""
    return json.dumps(run_eda(output_dir), ensure_ascii=False)


@tool("build_contract")
def build_contract_tool(output_dir: str) -> str:
    """Compute every number of the dataset contract (types, ranges, means, null counts,
    allowed values, row count, target rate, sha256) from output_dir/clean_data.csv.
    Writes contract_numbers.json and returns it as JSON. Descriptions are not included."""
    return json.dumps(build_contract(output_dir), ensure_ascii=False)
