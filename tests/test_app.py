"""The web app: every page renders, and the contract checker catches each break."""
import io
import subprocess
import sys
from pathlib import Path

import pytest

from churn_pipeline.scenarios import SCENARIOS
from churn_pipeline.web.app import create_app, parse_report

ROOT = Path(__file__).resolve().parents[1]


NEWS = {"query": "q", "window": "last 48 hours", "source": "Google News", "error": None,
        "articles": [{"title": "Festive phone sale begins", "url": "https://news.google.com/x",
                      "source": "Example Times", "published": "2026-10-30 10:00 UTC"}]}


@pytest.fixture(scope="module")
def client():
    # The committed artifacts of the latest run and the break-it scenarios; no network.
    app = create_app(ROOT / "artifacts", ROOT / "contracts" / "dataset_contract.lock.json")
    app.config["NEWS_SEARCH"] = lambda query: {**NEWS, "query": query}
    return app.test_client()


@pytest.mark.parametrize("path, text", [
    ("/", "refuses to run on bad data"), ("/architecture", "The RAG pipeline"), ("/analyst", "The dataset contract"),
    ("/scientist", "Two models, compared"),
    ("/briefings", "Agent-written briefings"), ("/briefing", "Type any CustomerID"), ("/code", "The code behind"),
    ("/runs", "Break-it scenarios"), ("/checker", "Contract checker"),
    ("/analyst/eda", "exploratory analysis"),
])
def test_pages_render(client, path, text):
    response = client.get(path)
    assert response.status_code == 200
    assert text in response.get_data(as_text=True)


def test_overview_shows_the_gates_of_the_last_run(client):
    html = client.get("/").get_data(as_text=True)
    for gate in ("crew1_artifacts", "contract_vs_data", "locked_contract", "required_features", "model_quality"):
        assert gate in html


def test_runs_lists_every_break_it_scenario(client):
    html = client.get("/runs").get_data(as_text=True)
    for name in [*SCENARIOS, "raw_unit_change"]:
        assert name in html


def test_unknown_briefing_is_404(client):
    response = client.get("/briefings/1")
    assert response.status_code == 404
    assert "not part of the pipeline" in response.get_data(as_text=True)


def test_architecture_lists_every_agent_with_its_tool(client):
    html = client.get("/architecture").get_data(as_text=True)
    for role, tool in [("Data Quality Inspector", "profile_raw_data"), ("Contract Steward", "build_contract"),
                       ("Model Trainer &amp; Evaluator", "train_and_evaluate"),
                       ("Retention Briefing Writer", "search_internal_docs")]:
        assert role in html and f"{tool}()" in html


def test_overview_maps_the_course_requirements(client):
    html = client.get("/").get_data(as_text=True)
    assert "RAG over the company" in html and "Web search for the latest news" in html
    assert "Not built" not in html


def test_briefings_show_each_customers_score(client):
    html = client.get("/briefings").get_data(as_text=True)
    assert "0.95" in html and "high risk" in html


def test_checker_passes_the_clean_handoff(client):
    html = client.post("/checker", data={"scenario": "clean"}).get_data(as_text=True)
    assert "PASSED" in html and "hand it to Crew 2" in html


@pytest.mark.parametrize("name", list(SCENARIOS))
def test_checker_catches_every_scenario(client, name):
    html = client.post("/checker", data={"scenario": name}).get_data(as_text=True)
    assert "FAILED" in html
    expected = SCENARIOS[name].expected_text.replace("'", "&#39;")
    assert expected in html or name == "missing_feature" and "Complain" in html


def test_checker_reads_an_uploaded_file(client):
    clean = (ROOT / "artifacts" / "latest" / "crew1" / "clean_data.csv").read_bytes()
    html = client.post("/checker", data={"file": (io.BytesIO(clean), "clean_data.csv")},
                       content_type="multipart/form-data").get_data(as_text=True)
    assert "PASSED" in html

    broken = clean.replace(b"Debit Card", b"debit card", 1)
    html = client.post("/checker", data={"file": (io.BytesIO(broken), "broken.csv")},
                       content_type="multipart/form-data").get_data(as_text=True)
    assert "FAILED" in html and "debit card" in html


def test_checker_rejects_an_unknown_scenario(client):
    assert client.post("/checker", data={"scenario": "../etc"}).status_code == 400


def test_parse_report_reads_gates_and_problems():
    report = parse_report((ROOT / "artifacts" / "broken" / "unit_change" / "validation_report.md").read_text())
    assert report["verdict"] == "FAILED"
    failed = [g["name"] for g in report["gates"] if not g["passed"]]
    assert failed == ["contract_vs_data"]
    assert any("possible unit change" in p for p in report["problems"]["contract_vs_data"])


def test_app_does_not_load_crewai():
    code = "import sys, churn_pipeline.web.app; print(any(m.startswith('crewai') for m in sys.modules))"
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    assert out.stdout.strip() == "False"


def test_instant_briefing_for_any_customer(client):
    html = client.get("/briefing?id=51809").get_data(as_text=True)
    assert "0.95" in html and "high churn risk" in html
    # The situations the code decided, each with the section the RAG found.
    assert "Complained in the last month" in html
    assert "[retention_playbook.md &gt; Customers who complained]" in html
    assert "[retention_playbook.md &gt; Cash on delivery (COD) customers]" in html
    assert "agent-written briefing for customer 51809" in html


def test_instant_briefing_for_a_customer_without_an_agent_briefing(client):
    html = client.get("/briefing?id=50001").get_data(as_text=True)
    assert "churn risk" in html and "Source:" in html


def test_instant_briefing_explains_bad_input(client):
    assert "is not in the data" in client.get("/briefing?id=1").get_data(as_text=True)
    assert "is not a CustomerID" in client.get("/briefing?id=abc").get_data(as_text=True)


def test_instant_briefing_refuses_without_an_approved_model(tmp_path):
    import shutil
    shutil.copytree(ROOT / "artifacts" / "latest", tmp_path / "latest")
    (tmp_path / "latest" / "crew2" / "model_approved.json").unlink()
    app = create_app(tmp_path, ROOT / "contracts" / "dataset_contract.lock.json")
    html = app.test_client().get("/briefing?id=51809").get_data(as_text=True)
    assert "No briefing" in html and "0.95" not in html


def test_code_page_shows_the_gates_and_the_validator(client):
    html = client.get("/code").get_data(as_text=True)
    assert "def run_handoff_gates" in html and "def validate_against_contract" in html
    assert "possible unit change" in html


def test_instant_briefing_shows_market_news(client):
    html = client.get("/briefing?id=51809").get_data(as_text=True)
    assert "news from the last 48 hours" in html and "Festive phone sale begins" in html
    assert "smartphone" in html  # the query follows the customer's category


def test_instant_briefing_still_works_without_news():
    app = create_app(ROOT / "artifacts", ROOT / "contracts" / "dataset_contract.lock.json")
    app.config["NEWS_SEARCH"] = lambda query: {**NEWS, "articles": [], "error": "news search unavailable: blocked"}
    html = app.test_client().get("/briefing?id=51809").get_data(as_text=True)
    assert "not available right now" in html and "0.95" in html
