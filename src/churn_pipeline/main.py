#!/usr/bin/env python
"""Churn pipeline flow.

Step 3 version: runs the Data Analyst Crew only. Validation gates and the
Data Scientist Crew are added in step 5.
"""
import json
from pathlib import Path

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from churn_pipeline.crews.analyst_crew.analyst_crew import AnalystCrew

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


class PipelineState(BaseModel):
    raw_data_path: str = str(ROOT / "data" / "raw" / "E Commerce Dataset.xlsx")
    output_dir: str = str(ROOT / "artifacts" / "latest" / "crew1")
    crew1_artifacts: list[str] = []


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
        out = Path(self.state.output_dir)
        missing = [f for f in CREW1_ARTIFACTS if not (out / f).is_file() or (out / f).stat().st_size == 0]
        if missing:
            raise RuntimeError(f"Data Analyst Crew did not produce: {missing}")
        self.state.crew1_artifacts = [str(out / f) for f in CREW1_ARTIFACTS]
        return {"status": "crew1_complete", "artifacts": self.state.crew1_artifacts}


def kickoff():
    result = ChurnPipelineFlow().kickoff()
    print(json.dumps(result, indent=2))
    return result


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
