"""Write retention briefings: `uv run brief 51809 50230`.

Runs the Retention Briefing Crew once per customer and writes
artifacts/latest/briefings/customer_<id>.md. Refuses unless the latest
pipeline run approved the model. Exits with 1 if any briefing failed.
"""
import sys
from pathlib import Path

from churn_pipeline.crews.briefing_crew.briefing_crew import BriefingCrew

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "artifacts" / "latest" / "briefings"


def main() -> None:
    ids = sys.argv[1:]
    if not ids:
        sys.exit("usage: uv run brief <CustomerID> [<CustomerID> ...]")
    failed = []
    for customer_id in ids:
        try:
            BriefingCrew().crew().kickoff(inputs={"customer_id": customer_id, "output_dir": str(OUTPUT_DIR)})
            print(f"briefing written: {OUTPUT_DIR / f'customer_{customer_id}.md'}")
        except Exception as e:  # one customer's failure should not stop the others
            failed.append(customer_id)
            print(f"briefing for {customer_id} failed: {e}")
    if failed:
        sys.exit(1)
