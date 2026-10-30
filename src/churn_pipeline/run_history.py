"""Run history in Supabase: one row per pipeline run or break_it scenario.

The pipeline writes with SUPABASE_SECRET_KEY (it bypasses row level security);
the web app reads with SUPABASE_PUBLISHABLE_KEY, which may only select. Both
also need SUPABASE_URL. Without them, recording is skipped and the app falls
back to the report files, so the pipeline never fails because of history.

Standard library only, so the web app stays light.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

TABLE = "pipeline_runs"
TIMEOUT_SECONDS = 10


def run_row(run_at: str, kind: str, scenario: str | None, status: str, verdict: str,
            gates: list[dict], next_step: str, metrics: dict | None) -> dict[str, Any]:
    """The table row for one finished run. metrics is evaluation_metrics.json when Crew 2 ran."""
    ran_quality_gate = any(g["name"] == "model_quality" for g in gates)
    test = (metrics or {}).get("selected_test_metrics", {}) if ran_quality_gate else {}
    return {
        "run_at": run_at,
        "kind": kind,
        "scenario": scenario,
        "verdict": verdict,
        "status": status,
        "failed_gates": [g["name"] for g in gates if not g["passed"]],
        "gates": [{"name": g["name"], "passed": g["passed"], "summary": g["summary"],
                   "problems": g.get("problems", [])} for g in gates],
        "selected_model": metrics.get("selected_model") if metrics and ran_quality_gate else None,
        "pr_auc": test.get("pr_auc"),
        "recall": test.get("recall"),
        "next_step": next_step,
    }


def _request(url: str, key: str, method: str = "GET", body: Any = None,
             extra_headers: dict[str, str] | None = None) -> Any:
    headers = {"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json",
               **(extra_headers or {})}
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
        text = response.read().decode("utf-8")
    return json.loads(text) if text else None


def record_run(row: dict[str, Any]) -> str:
    """Insert a row; returns what happened, for the pipeline log. Never raises."""
    url, key = os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SECRET_KEY")
    if not url or not key:
        return "run history skipped: SUPABASE_URL or SUPABASE_SECRET_KEY not set"
    try:
        _request(f"{url.rstrip('/')}/rest/v1/{TABLE}", key, "POST", row,
                 {"Prefer": "return=minimal"})
        return f"run history recorded in Supabase ({row['kind']}, {row['verdict']})"
    except (urllib.error.URLError, TimeoutError, ValueError) as e:
        return f"run history not recorded: {e}"


def fetch_runs(limit: int = 50) -> list[dict[str, Any]] | None:
    """Latest runs, newest first; None when Supabase is not configured or unreachable."""
    url, key = os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_PUBLISHABLE_KEY")
    if not url or not key:
        return None
    try:
        return _request(f"{url.rstrip('/')}/rest/v1/{TABLE}?select=*&order=run_at.desc&limit={int(limit)}", key)
    except (urllib.error.URLError, TimeoutError, ValueError):
        return None
