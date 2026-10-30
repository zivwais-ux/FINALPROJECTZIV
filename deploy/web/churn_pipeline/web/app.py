"""Flask app that shows the pipeline's results and checks CSV files against the contract.

It reads the files the pipeline already wrote; it never runs a crew and never
calls an LLM, so it imports nothing from crewai.

    uv run web            # http://127.0.0.1:5000
"""
from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any

import markdown
import pandas as pd
from flask import Flask, abort, render_template, request, send_file
from markupsafe import Markup

from churn_pipeline.contract.models import load_contract
from churn_pipeline.contract.validator import validate_against_contract
from churn_pipeline.run_history import fetch_runs
from churn_pipeline.scenarios import SCENARIOS

ROOT = Path(__file__).resolve().parents[3]
MAX_UPLOAD_MB = 10


def _read(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.is_file() else None


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def render_md(text: str | None) -> Markup | None:
    """Markdown written by the pipeline's agents, rendered as HTML."""
    if text is None:
        return None
    return Markup(markdown.markdown(text, extensions=["tables", "fenced_code"]))


def parse_report(text: str | None) -> dict[str, Any] | None:
    """The verdict, time, next step and gate rows of a validation_report.md."""
    if text is None:
        return None
    field = lambda name: (re.search(rf"- {name}: (.+)", text) or [None, ""])[1].strip("* ")
    gates = [{"name": m[0], "passed": m[1] == "PASS", "summary": m[2]}
             for m in re.findall(r"^\| (\w+) \| (PASS|FAIL) \| (.+) \|$", text, re.M)]
    problems: dict[str, list[str]] = {}
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        name, *lines = block.splitlines()
        problems[name.strip()] = [l[2:] for l in lines if l.startswith("- ")]
    return {"verdict": field("Verdict"), "time": field(r"Time \(UTC\)"), "next_step": field("Next step"),
            "gates": gates, "problems": problems}


def check_dataframe(df: pd.DataFrame, file_path: Path, lock_path: Path) -> dict[str, Any]:
    """Validate a handoff file against the locked contract, as the pipeline's gates would."""
    contract = load_contract(lock_path)
    violations = [v.to_dict() for v in validate_against_contract(df, contract, file_path=file_path)]
    required = [c.name for c in contract.columns
                if c.role == "feature" and c.name not in contract.forbidden_features]
    missing = [n for n in required if n not in df.columns]
    return {"rows": len(df), "columns": len(df.columns), "violations": violations,
            "missing_features": missing, "passed": not violations and not missing}


def create_app(artifacts_dir: str | Path | None = None, lock_path: str | Path | None = None) -> Flask:
    artifacts = Path(artifacts_dir or os.getenv("ARTIFACTS_DIR") or ROOT / "artifacts")
    lock = Path(lock_path or os.getenv("CONTRACT_LOCK") or ROOT / "contracts" / "dataset_contract.lock.json")
    latest, crew1, crew2 = artifacts / "latest", artifacts / "latest" / "crew1", artifacts / "latest" / "crew2"

    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024

    @app.context_processor
    def nav():
        return {"nav": [("index", "Overview"), ("analyst", "Data Analyst"), ("scientist", "Data Scientist"),
                        ("briefings", "Briefings"), ("runs", "Runs"), ("checker", "Contract Checker")]}

    @app.route("/")
    def index():
        metrics = _json(crew2 / "evaluation_metrics.json")
        return render_template("index.html", report=parse_report(_read(latest / "validation_report.md")),
                               metrics=metrics, contract=_json(crew1 / "dataset_contract.json"),
                               approved=(crew2 / "model_approved.json").is_file(),
                               log=_read(latest / "pipeline.log"))

    @app.route("/analyst")
    def analyst():
        return render_template("analyst.html", contract=_json(crew1 / "dataset_contract.json"),
                               quality=_json(crew1 / "quality_report.json"),
                               summary=render_md(_read(crew1 / "quality_summary.md")),
                               insights=render_md(_read(crew1 / "insights.md")),
                               has_eda=(crew1 / "eda_report.html").is_file())

    @app.route("/analyst/eda")
    def eda_report():
        path = crew1 / "eda_report.html"
        if not path.is_file():
            abort(404)
        return send_file(path)

    @app.route("/scientist")
    def scientist():
        return render_template("scientist.html", metrics=_json(crew2 / "evaluation_metrics.json"),
                               features=_json(crew2 / "feature_spec.json"),
                               approved=(crew2 / "model_approved.json").is_file(),
                               evaluation=render_md(_read(crew2 / "evaluation_report.md")),
                               card=render_md(_read(crew2 / "model_card.md")))

    @app.route("/briefings")
    @app.route("/briefings/<int:customer_id>")
    def briefings(customer_id: int | None = None):
        files = sorted((latest / "briefings").glob("customer_*.md"))
        ids = [int(f.stem.split("_")[1]) for f in files]
        if customer_id is None and ids:
            customer_id = ids[0]
        if customer_id is not None and customer_id not in ids:
            abort(404)
        text = _read(latest / "briefings" / f"customer_{customer_id}.md") if customer_id else None
        return render_template("briefings.html", ids=ids, current=customer_id, briefing=render_md(text))

    @app.route("/runs")
    def runs():
        broken = artifacts / "broken"
        scenarios = []
        for d in sorted(p for p in broken.glob("*") if p.is_dir()):
            report = parse_report(_read(d / "validation_report.md"))
            if report:
                scenarios.append({"name": d.name, "report": report, "log": _read(d / "pipeline.log"),
                                  "description": SCENARIOS[d.name].description if d.name in SCENARIOS
                                  else "full run on a broken raw file (Crew 1 included)"})
        return render_template("runs.html", latest=parse_report(_read(latest / "validation_report.md")),
                               latest_log=_read(latest / "pipeline.log"), scenarios=scenarios,
                               history=fetch_runs())

    @app.route("/checker", methods=["GET", "POST"])
    def checker():
        result, source, error = None, None, None
        if request.method == "POST":
            scenario = request.form.get("scenario")
            upload = request.files.get("file")
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "handoff.csv"
                if scenario:
                    if scenario != "clean" and scenario not in SCENARIOS:
                        abort(400)
                    df = pd.read_csv(crew1 / "clean_data.csv")
                    if scenario != "clean":
                        df = SCENARIOS[scenario].change(df)
                        source = f"clean_data.csv broken by {scenario}: {SCENARIOS[scenario].description}"
                    else:
                        source = "clean_data.csv as Crew 1 wrote it"
                    df.to_csv(path, index=False)
                elif upload and upload.filename:
                    upload.save(path)
                    source = f"uploaded file {upload.filename}"
                else:
                    error = "Choose a CSV file or a scenario."
                if source:
                    try:
                        df = pd.read_csv(path)
                        result = check_dataframe(df, path, lock)
                    except (pd.errors.ParserError, UnicodeDecodeError, ValueError) as e:
                        error, source = f"Could not read the file as CSV: {e}", None
        return render_template("checker.html", scenarios=SCENARIOS, result=result, source=source,
                               error=error, max_mb=MAX_UPLOAD_MB)

    @app.errorhandler(413)
    def too_large(_):
        return render_template("checker.html", scenarios=SCENARIOS, result=None, source=None,
                               error=f"The file is larger than {MAX_UPLOAD_MB} MB.", max_mb=MAX_UPLOAD_MB), 413

    return app


def main() -> None:
    create_app().run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)


if __name__ == "__main__":
    main()
