"""Fixtures shared by the gate and break_it tests."""
from pathlib import Path

import pytest

from churn_pipeline.tools.analyst_tools import (
    build_contract,
    export_clean_data,
    finalize_contract,
    profile_raw_data,
    run_eda,
)

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "E Commerce Dataset.xlsx"


@pytest.fixture(scope="session")
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
