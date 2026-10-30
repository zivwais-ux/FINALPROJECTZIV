"""Retention briefing tools and checks, tested without an LLM."""
import json
from pathlib import Path

import pytest

from churn_pipeline.crews.briefing_crew.briefing_crew import check_briefing
from churn_pipeline.tools.briefing_tools import (
    customer_risk_profile,
    require_approved_model,
    risk_band,
    situations,
)
from churn_pipeline.tools.scientist_tools import build_features, train_and_evaluate


@pytest.fixture(scope="module")
def approved(crew1_template, tmp_path_factory) -> dict:
    """Crew 2 outputs from the tools, plus the approval and a PASSED report."""
    d = tmp_path_factory.mktemp("crew2")
    build_features(crew1_template, d)
    train_and_evaluate(d)
    (d / "model_approved.json").write_text("{}")
    report = d / "validation_report.md"
    report.write_text("- Verdict: **PASSED**\n")
    return {"crew1_dir": crew1_template, "crew2_dir": d, "report_path": report}


def test_risk_bands_follow_the_playbook():
    assert [risk_band(s) for s in (0.95, 0.70, 0.69, 0.40, 0.39)] == ["high", "high", "medium", "medium", "low"]


def test_situations_come_from_the_customer():
    found = situations("high", {"Tenure": 0.0, "Complain": 1, "PreferredPaymentMode": "COD",
                                "PreferedOrderCat": "Mobile"})
    assert [s["situation"] for s in found] == [
        "high churn risk", "new customer (tenure 0 to 1 months)", "complained in the last month",
        "pays cash on delivery", "prefers the Mobile category", "an offer may be made"]


def test_low_risk_new_customer_gets_no_new_customer_or_offer_situation():
    found = [s["situation"] for s in situations("low", {"Tenure": 0.0, "Complain": 0})]
    assert found == ["low churn risk"]


def test_profile_scores_a_customer(approved):
    profile = customer_risk_profile(51809, **approved)
    assert 0 <= profile["risk_score"] <= 1
    assert profile["risk_band"] == risk_band(profile["risk_score"])
    assert isinstance(profile["scored_out_of_sample"], bool)
    assert profile["key_facts"]["PreferredPaymentMode"] == "COD"
    assert "Churn" not in json.dumps(profile["key_facts"])
    assert profile["situations"][0]["situation"].endswith("churn risk")


def test_unknown_customer_is_refused(approved):
    with pytest.raises(ValueError, match="not in the data"):
        customer_risk_profile(1, **approved)


def test_no_briefing_without_an_approved_model(approved, tmp_path):
    with pytest.raises(ValueError, match="no approved model"):
        require_approved_model(tmp_path, approved["report_path"])
    failed = tmp_path / "validation_report.md"
    failed.write_text("- Verdict: **FAILED**\n")
    with pytest.raises(ValueError, match="does not say PASSED"):
        require_approved_model(approved["crew2_dir"], failed)


PROFILE = {"risk_score": 0.95, "risk_band": "high"}
CITABLE = {"retention_playbook.md > Customers who complained", "discount_policy.md > Approval levels"}
NEWS = {"https://news.example.com/sale"}
GOOD = """## Churn risk
- Risk score: 0.95 (high)
## Recommended action
- Resolve the complaint first [retention_playbook.md > Customers who complained]
## Market now (last 48 hours)
- [Phone sale starts](https://news.example.com/sale), Example News, 2026-10-30
## Sources
- [discount_policy.md > Approval levels]
"""


def test_check_accepts_a_good_briefing():
    assert check_briefing(GOOD, PROFILE, CITABLE, NEWS) == []


def test_check_rejects_a_wrong_score_and_an_invented_citation():
    bad = GOOD.replace("0.95", "0.90").replace("Approval levels]", "Approval rules]")
    problems = check_briefing(bad, PROFILE, CITABLE, NEWS)
    assert any("0.95" in p for p in problems)
    assert any("discount_policy.md > Approval rules" in p for p in problems)


def test_check_rejects_a_briefing_longer_than_a_page():
    problems = check_briefing(GOOD + "word " * 520, PROFILE, CITABLE, NEWS)
    assert any("words" in p for p in problems)


def test_check_rejects_an_invented_news_link():
    invented = GOOD.replace("https://news.example.com/sale", "https://made-up.example.com/story")
    problems = check_briefing(invented, PROFILE, CITABLE, NEWS)
    assert any("did not come from search_recent_news" in p for p in problems)


def test_check_requires_the_market_section():
    problems = check_briefing(GOOD.replace("## Market now (last 48 hours)", "## Other"), PROFILE, CITABLE, NEWS)
    assert any("Market now" in p for p in problems)


def test_profile_carries_a_news_query_for_the_category(approved):
    profile = customer_risk_profile(51809, **approved)
    assert profile["news_query"].startswith("smartphone")
