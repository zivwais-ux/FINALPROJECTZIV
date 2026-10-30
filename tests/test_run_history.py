"""Run history rows and the Supabase client, tested without the network."""
import io
import json

import churn_pipeline.run_history as history

GATES = [{"name": "contract_vs_data", "passed": False, "summary": "3 violations", "problems": ["x100"]},
         {"name": "locked_contract", "passed": True, "summary": "matches", "problems": []}]
METRICS = {"selected_model": "hist_gradient_boosting",
           "selected_test_metrics": {"pr_auc": 0.8636, "recall": 0.6667}}


def test_failed_handoff_row_has_no_model_metrics():
    row = history.run_row("2026-10-30T12:00:00+00:00", "scenario", "unit_change", "handoff_failed",
                          "FAILED", GATES, "Crew 2 did not run", METRICS)
    assert row["failed_gates"] == ["contract_vs_data"]
    assert row["gates"][0]["problems"] == ["x100"]
    # Crew 2 did not run, so the metrics on disk belong to another run.
    assert row["selected_model"] is None and row["pr_auc"] is None


def test_passed_run_row_carries_the_model_metrics():
    gates = [{"name": "model_quality", "passed": True, "summary": "passes"}]
    row = history.run_row("2026-10-30T12:00:00+00:00", "pipeline", None, "passed", "PASSED",
                          gates, "approved", METRICS)
    assert (row["selected_model"], row["pr_auc"], row["recall"]) == ("hist_gradient_boosting", 0.8636, 0.6667)


def test_without_supabase_settings_nothing_is_sent(monkeypatch):
    for name in ("SUPABASE_URL", "SUPABASE_SECRET_KEY", "SUPABASE_PUBLISHABLE_KEY"):
        monkeypatch.delenv(name, raising=False)
    assert "skipped" in history.record_run({"kind": "pipeline"})
    assert history.fetch_runs() is None


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def test_record_and_fetch_use_the_right_key(monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_SECRET_KEY", "secret")
    monkeypatch.setenv("SUPABASE_PUBLISHABLE_KEY", "publishable")
    sent = []

    def fake_urlopen(req, timeout):
        sent.append(req)
        return FakeResponse(b"" if req.get_method() == "POST" else json.dumps([{"verdict": "PASSED"}]).encode())

    monkeypatch.setattr(history.urllib.request, "urlopen", fake_urlopen)
    assert "recorded" in history.record_run({"kind": "pipeline", "verdict": "PASSED"})
    assert history.fetch_runs(5) == [{"verdict": "PASSED"}]
    post, get = sent
    assert post.get_method() == "POST" and post.headers["Apikey"] == "secret"
    assert post.full_url == "https://example.supabase.co/rest/v1/pipeline_runs"
    assert get.headers["Apikey"] == "publishable" and "limit=5" in get.full_url


def test_unreachable_supabase_does_not_raise(monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_SECRET_KEY", "secret")
    monkeypatch.setenv("SUPABASE_PUBLISHABLE_KEY", "publishable")

    def refuse(req, timeout):
        raise history.urllib.error.URLError("connection refused")

    monkeypatch.setattr(history.urllib.request, "urlopen", refuse)
    assert "not recorded" in history.record_run({"kind": "pipeline", "verdict": "PASSED"})
    assert history.fetch_runs() is None
