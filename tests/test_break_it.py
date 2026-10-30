"""Every break_it scenario stops the flow before Crew 2, at the right gate."""
import importlib.util
import sys
from pathlib import Path

import pytest

import churn_pipeline.main as main

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("break_it", ROOT / "scripts" / "break_it.py")
break_it = importlib.util.module_from_spec(_spec)
sys.modules["break_it"] = break_it  # @dataclass looks the module up while it loads
_spec.loader.exec_module(break_it)


class NoScientistCrew:
    def crew(self):
        raise AssertionError("Crew 2 must not run after a broken handoff")


@pytest.mark.parametrize("name", list(break_it.SCENARIOS))
def test_scenario_is_caught_before_crew2(name, crew1_template, tmp_path, monkeypatch):
    monkeypatch.setattr(main, "ScientistCrew", NoScientistCrew)
    result = break_it.run_scenario(name, source=crew1_template, out_root=tmp_path)
    scenario = break_it.SCENARIOS[name]

    assert result["status"] == "handoff_failed"
    assert result["caught"] is True
    assert scenario.expected_gate in result["failed_gates"]
    assert scenario.expected_text in result["problem"]
    assert result["crew2_ran"] is False
    report = (tmp_path / name / "validation_report.md").read_text()
    assert "**FAILED**" in report and scenario.expected_text in report
    assert "break_it scenario" in (tmp_path / name / "pipeline.log").read_text()


def test_source_handoff_is_not_changed(crew1_template, tmp_path, monkeypatch):
    monkeypatch.setattr(main, "ScientistCrew", NoScientistCrew)
    before = (crew1_template / "clean_data.csv").read_bytes()
    break_it.run_scenario("unit_change", source=crew1_template, out_root=tmp_path)
    assert (crew1_template / "clean_data.csv").read_bytes() == before


def test_summary_lists_every_scenario(tmp_path):
    rows = [{"scenario": "unit_change", "description": "x100", "caught": True,
             "failed_gates": ["contract_vs_data"], "crew2_ran": False, "problem": "a | b"}]
    break_it.write_summary(rows, tmp_path / "summary.md")
    text = (tmp_path / "summary.md").read_text()
    assert "| `unit_change` | x100 | yes | contract_vs_data | no | a / b |" in text
