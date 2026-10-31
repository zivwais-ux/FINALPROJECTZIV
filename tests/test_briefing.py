"""Retention briefing tools and checks, tested without an LLM."""
import json
from pathlib import Path

import pytest

from churn_pipeline.crews.briefing_crew.briefing_crew import check_notes, render_briefing
from churn_pipeline.crews.briefing_crew.outputs import BriefingNotes, DecisionNote, MarketItem
from churn_pipeline.retention_plan import retention_plan
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


def test_profile_carries_a_news_query_for_the_category(approved):
    profile = customer_risk_profile(51809, **approved)
    assert profile["news_query"].startswith("smartphone")


def _profile(band="low", score=0.29, **facts):
    facts = {"Tenure": 0.0, "Complain": 1, "PreferredPaymentMode": "COD", "PreferedOrderCat": "Mobile", **facts}
    return {"customer_id": 50013, "risk_score": score, "risk_band": band,
            "risk_band_rule": "high >= 0.7, medium >= 0.4, otherwise low (retention playbook)",
            "score_note": "the model never saw this customer during training",
            "key_facts": facts, "plan": retention_plan(band, facts)}


ARTICLE = {"title": "Phone sale starts", "url": "https://news.google.com/a", "source": "Example News",
           "published": "2026-10-30 10:00 UTC"}


def _notes(profile, **override):
    notes = {"summary": "A new customer who complained last month and pays cash on delivery.",
             "decisions": [DecisionNote(id=d["id"], why="The playbook says so for this case.")
                           for d in profile["plan"]["decisions"]],
             "market": [MarketItem(url=ARTICLE["url"], relevance="Competitors are cutting phone prices.")]}
    return BriefingNotes(**{**notes, **override})


def test_good_notes_render_the_plan_word_for_word():
    profile = _profile()
    notes = _notes(profile)
    assert check_notes(notes, profile, {ARTICLE["url"]: ARTICLE}) == []
    text = render_briefing(profile, notes, {ARTICLE["url"]: ARTICLE})
    for d in profile["plan"]["decisions"]:
        assert f"- **{d['label']}:** {d['value']}." in text
    assert "Risk score: 0.29 (low risk band: below 0.40)" in text
    assert "[Phone sale starts](https://news.google.com/a), Example News" in text
    # The 50013 case: a low-risk customer who complained is contacted.
    assert "**Contact:** Yes, priority 2" in text and "no individual outreach" not in text.lower()


def test_notes_must_explain_every_decision_and_nothing_else():
    profile = _profile()
    notes = _notes(profile)
    notes.decisions = notes.decisions[1:] + [DecisionNote(id="discount_now", why="x")]
    problems = check_notes(notes, profile, {ARTICLE["url"]: ARTICLE})
    assert any("missing ids: ['contact']" in p for p in problems)
    assert any("'discount_now'" in p for p in problems)


def test_an_explanation_that_walks_back_the_contact_decision_is_rejected():
    profile = _profile()
    notes = _notes(profile)
    notes.decisions[0].why = "Low risk, so no individual outreach; keep them in the regular newsletter."
    assert any("contradicts the plan" in p for p in check_notes(notes, profile, {ARTICLE["url"]: ARTICLE}))


def test_an_invented_news_link_is_rejected():
    profile = _profile()
    notes = _notes(profile, market=[MarketItem(url="https://made-up.example/x", relevance="r")])
    assert any("did not come from search_recent_news" in p for p in check_notes(notes, profile, {}))


def test_no_news_renders_a_plain_statement():
    profile = _profile()
    text = render_briefing(profile, _notes(profile, market=[]), {})
    assert "No market news from the last 48 hours was available." in text


def test_a_briefing_longer_than_a_page_is_rejected():
    profile = _profile()
    notes = _notes(profile, summary="word " * 650)
    problems = check_notes(notes, profile, {ARTICLE["url"]: ARTICLE})
    assert any("longer than 650 words" in p for p in problems)
    assert any("summary is longer than" in p for p in problems)


def test_profile_carries_the_plan(approved):
    profile = customer_risk_profile(51809, **approved)
    assert profile["plan"]["decisions"][0]["id"] == "contact"
    assert profile["plan"] == retention_plan(profile["risk_band"], profile["key_facts"])


def test_the_frequency_rule_is_not_mistaken_for_a_contradiction():
    profile = _profile()
    notes = _notes(profile)
    for n in notes.decisions:
        if n.id == "frequency":
            n.why = "The customer should not be contacted more than twice in 14 days; do not contact the customer more often."
    assert check_notes(notes, profile, {ARTICLE["url"]: ARTICLE}) == []


def test_a_summary_that_walks_back_the_contact_decision_is_rejected():
    profile = _profile()
    notes = _notes(profile, summary="Low risk, so this customer stays in the regular newsletter.")
    assert any("summary contradicts" in p for p in check_notes(notes, profile, {ARTICLE["url"]: ARTICLE}))
