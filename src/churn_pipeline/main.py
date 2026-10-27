#!/usr/bin/env python
"""Churn pipeline flow.

Step 4 version: runs the Data Analyst Crew, then the Data Scientist Crew on
Crew 1's clean_data.csv and dataset_contract.json. The validation gates and
the pass/fail router are added in step 5.
"""
import json
from pathlib import Path

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from churn_pipeline.crews.analyst_crew.analyst_crew import AnalystCrew
from churn_pipeline.crews.scientist_crew.scientist_crew import ScientistCrew

ROOT = Path(__file__).resolve().parents[2]

CREW1_ARTIFACTS = [
    "quality_report.json",
    "quality_summary.md",
    "clean_data.csv",
    "preparation_log.md",
    "eda_report.html",
    "insights.md",
    "contract_numbers.json",
    "dataset_contract.json",
]

CREW2_ARTIFACTS = [
    "contract_review.md",
    "features.csv",
    "feature_spec.json",
    "feature_log.md",
    "model.joblib",
    "evaluation_metrics.json",
    "evaluation_report.md",
    "model_card.md",
]


def _missing(directory: str, names: list[str]) -> list[str]:
    out = Path(directory)
    return [f for f in names if not (out / f).is_file() or (out / f).stat().st_size == 0]


class PipelineState(BaseModel):
    raw_data_path: str = str(ROOT / "data" / "raw" / "E Commerce Dataset.xlsx")
    output_dir: str = str(ROOT / "artifacts" / "latest" / "crew1")
    crew2_output_dir: str = str(ROOT / "artifacts" / "latest" / "crew2")
    crew1_artifacts: list[str] = []
    crew2_artifacts: list[str] = []


class ChurnPipelineFlow(Flow[PipelineState]):

    @start()
    def run_analyst_crew(self):
        Path(self.state.output_dir).mkdir(parents=True, exist_ok=True)
        AnalystCrew().crew().kickoff(inputs={
            "raw_data_path": self.state.raw_data_path,
            "output_dir": self.state.output_dir,
        })

    @listen(run_analyst_crew)
    def check_crew1_artifacts(self):
        missing = _missing(self.state.output_dir, CREW1_ARTIFACTS)
        if missing:
            raise RuntimeError(f"Data Analyst Crew did not produce: {missing}")
        self.state.crew1_artifacts = [str(Path(self.state.output_dir) / f) for f in CREW1_ARTIFACTS]

    @listen(check_crew1_artifacts)
    def run_scientist_crew(self):
        # Crew 2 reads only Crew 1's clean_data.csv and dataset_contract.json.
        ScientistCrew().crew().kickoff(inputs={
            "input_dir": self.state.output_dir,
            "output_dir": self.state.crew2_output_dir,
        })

    @listen(run_scientist_crew)
    def check_crew2_artifacts(self):
        missing = _missing(self.state.crew2_output_dir, CREW2_ARTIFACTS)
        if missing:
            raise RuntimeError(f"Data Scientist Crew did not produce: {missing}")
        out = Path(self.state.crew2_output_dir)
        self.state.crew2_artifacts = [str(out / f) for f in CREW2_ARTIFACTS]
        metrics = json.loads((out / "evaluation_metrics.json").read_text(encoding="utf-8"))
        return {
            "status": "crew2_complete",
            "selected_model": metrics["selected_model"],
            "test_metrics": metrics["selected_test_metrics"],
            "meets_quality_thresholds": metrics["meets_quality_thresholds"],
            "artifacts": self.state.crew1_artifacts + self.state.crew2_artifacts,
        }


def kickoff():
    # No return value: the console script passes it to sys.exit, and a dict exits with 1.
    result = ChurnPipelineFlow().kickoff()
    print(json.dumps(result, indent=2))


def plot():
    ChurnPipelineFlow().plot()


def run_with_trigger():
    """Run the flow with a JSON trigger payload of state overrides."""
    import sys

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")
    try:
        payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")
    return ChurnPipelineFlow().kickoff(inputs=payload)


if __name__ == "__main__":
    kickoff()
