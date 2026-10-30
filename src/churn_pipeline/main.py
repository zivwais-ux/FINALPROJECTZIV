#!/usr/bin/env python
"""Churn pipeline flow.

Crew 1 (Data Analyst) -> handoff gates -> Crew 2 (Data Scientist) -> quality gate.

The gates are plain Python (churn_pipeline.gates). When a handoff gate fails,
the flow writes validation_report.md and stops before Crew 2; when the model
misses the quality thresholds, it writes the report and does not approve the
model. Either way the command exits with 1.

`uv run kickoff --from-gate` skips Crew 1 and starts at the handoff gates with
the files already in artifacts/latest/crew1, to show a broken handoff fast.
"""
import json
import logging
import sys
from pathlib import Path

from crewai.flow import Flow, listen, router, start
from pydantic import BaseModel

from churn_pipeline.crews.analyst_crew.analyst_crew import AnalystCrew
from churn_pipeline.crews.scientist_crew.scientist_crew import ScientistCrew
from churn_pipeline.gates import (
    GateResult,
    gate_model_quality,
    run_handoff_gates,
    write_validation_report,
)

ROOT = Path(__file__).resolve().parents[2]
log = logging.getLogger("churn_pipeline")


class PipelineState(BaseModel):
    raw_data_path: str = str(ROOT / "data" / "raw" / "E Commerce Dataset.xlsx")
    output_dir: str = str(ROOT / "artifacts" / "latest" / "crew1")
    crew2_output_dir: str = str(ROOT / "artifacts" / "latest" / "crew2")
    lock_path: str = str(ROOT / "contracts" / "dataset_contract.lock.json")
    report_path: str = str(ROOT / "artifacts" / "latest" / "validation_report.md")
    from_gate: bool = False
    gates: list[dict] = []
    status: str = "running"


class ChurnPipelineFlow(Flow[PipelineState]):

    def _record(self, results: list[GateResult]) -> None:
        for g in results:
            self.state.gates.append(g.to_dict())
            log.info("gate %-18s %s  %s", g.name, "PASS" if g.passed else "FAIL", g.summary)
            for p in g.problems:
                log.info("    - %s", p)

    def _finish(self, status: str, verdict: str, next_step: str) -> dict:
        self.state.status = status
        write_validation_report(self.state.report_path,
                                [GateResult(**g) for g in self.state.gates], verdict, next_step)
        log.info("%s: %s (report: %s)", verdict, next_step, self.state.report_path)
        return {"status": status, "report": self.state.report_path, "gates": self.state.gates}

    @start()
    def run_analyst_crew(self):
        if self.state.from_gate:
            log.info("--from-gate: skipping Crew 1, using %s", self.state.output_dir)
            return
        log.info("Crew 1 (Data Analyst) starting on %s", self.state.raw_data_path)
        Path(self.state.output_dir).mkdir(parents=True, exist_ok=True)
        AnalystCrew().crew().kickoff(inputs={
            "raw_data_path": self.state.raw_data_path,
            "output_dir": self.state.output_dir,
        })
        log.info("Crew 1 finished")

    @router(run_analyst_crew)
    def handoff_gates(self):
        results = run_handoff_gates(self.state.output_dir, self.state.lock_path)
        self._record(results)
        return "handoff_passed" if all(g.passed for g in results) else "handoff_failed"

    @listen("handoff_failed")
    def stop_before_crew2(self):
        return self._finish("handoff_failed", "FAILED",
                            "Crew 2 did not run: fix the data or Crew 1, or update the locked "
                            "contract on purpose, then run again")

    @listen("handoff_passed")
    def run_scientist_crew(self):
        # Crew 2 reads only Crew 1's clean_data.csv and dataset_contract.json.
        log.info("Crew 2 (Data Scientist) starting on %s", self.state.output_dir)
        ScientistCrew().crew().kickoff(inputs={
            "input_dir": self.state.output_dir,
            "output_dir": self.state.crew2_output_dir,
        })
        log.info("Crew 2 finished")

    @router(run_scientist_crew)
    def quality_gate(self):
        result = gate_model_quality(self.state.crew2_output_dir)
        self._record([result])
        approval = Path(self.state.crew2_output_dir) / "model_approved.json"
        approval.unlink(missing_ok=True)
        if not result.passed:
            return "model_rejected"
        approval.write_text(json.dumps({"model": "model.joblib", "gate": result.to_dict()}, indent=2) + "\n",
                            encoding="utf-8")
        return "model_accepted"

    @listen("model_rejected")
    def reject_model(self):
        return self._finish("model_rejected", "FAILED",
                            "the model misses the quality thresholds and is not approved")

    @listen("model_accepted")
    def approve_model(self):
        return self._finish("passed", "PASSED", "model approved (model_approved.json written)")


def _setup_logging(log_path: Path) -> None:
    # Replace earlier handlers, so several runs in one process (break_it.py)
    # each get their own log file.
    for h in list(log.handlers):
        log.removeHandler(h)
        h.close()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handlers = [logging.FileHandler(log_path, mode="w", encoding="utf-8"), logging.StreamHandler()]
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
    for h in handlers:
        h.setFormatter(fmt)
        log.addHandler(h)
    log.setLevel(logging.INFO)


def kickoff():
    # No return value: the console script passes it to sys.exit. Exit code 1
    # means a gate failed.
    from_gate = "--from-gate" in sys.argv[1:]
    _setup_logging(ROOT / "artifacts" / "latest" / "pipeline.log")
    result = ChurnPipelineFlow().kickoff(inputs={"from_gate": from_gate})
    print(json.dumps(result, indent=2))
    if result["status"] != "passed":
        sys.exit(1)


def plot():
    ChurnPipelineFlow().plot()


def run_with_trigger():
    """Run the flow with a JSON trigger payload of state overrides."""
    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")
    try:
        payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")
    return ChurnPipelineFlow().kickoff(inputs=payload)


if __name__ == "__main__":
    kickoff()
