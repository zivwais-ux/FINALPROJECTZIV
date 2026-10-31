"""The retention plan applies the playbook and the discount policy, case by case."""
import pytest

from churn_pipeline.rag import split_markdown
from churn_pipeline.retention_plan import all_citations, retention_plan
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = sorted((ROOT / "knowledge" / "harbor_vale").glob("*.md"))


def _plan(band, tenure=10.0, complain=0, payment="Debit Card", category="Fashion"):
    return retention_plan(band, {"Tenure": tenure, "Complain": complain,
                                 "PreferredPaymentMode": payment, "PreferedOrderCat": category})


def _value(plan, key):
    return next((d["value"] for d in plan["decisions"] if d["id"] == key), None)


@pytest.mark.parametrize("band, complain, contact, channel", [
    ("high", 0, "Yes, priority 1", "Phone call"),
    ("high", 1, "Yes, priority 1", "Phone call"),
    ("medium", 0, "Yes, priority 3", "App push notification"),
    ("medium", 1, "Yes, priority 2", "App push notification"),
    ("low", 1, "Yes, priority 2", "Follow-up by the support team"),   # the 50013 case
    ("low", 0, "No individual outreach", None),
])
def test_who_is_contacted_and_how(band, complain, contact, channel):
    plan = _plan(band, complain=complain)
    assert _value(plan, "contact").startswith(contact)
    assert (_value(plan, "channel") or "").startswith(channel or "")
    assert plan["contact"] == (contact != "No individual outreach")


def test_welcome_call_only_for_new_customers_the_model_flagged():
    assert _value(_plan("high", tenure=0.0), "welcome")
    assert _value(_plan("medium", tenure=1.0), "welcome")
    assert _value(_plan("low", tenure=0.0), "welcome") is None      # the 50036 case
    assert _value(_plan("high", tenure=None), "welcome") is None    # missing tenure is not "new"


@pytest.mark.parametrize("kwargs, offer", [
    ({"band": "high"}, "Allowed now"),
    ({"band": "high", "complain": 1}, "Only after the complaint is closed"),
    ({"band": "medium", "tenure": 0.0}, "Not on the first contact"),
    ({"band": "high", "tenure": 0.0, "complain": 1}, "Only after the complaint is closed"),
    ({"band": "low"}, "None: offers to customers below 0.40 are not funded"),
    ({"band": "low", "complain": 1}, "None: offers to customers below 0.40 are not funded"),
])
def test_when_an_offer_is_allowed(kwargs, offer):
    assert _value(_plan(**kwargs), "offer").startswith(offer)


def test_offer_type_follows_payment_and_category():
    assert "no wallet cashback" in _value(_plan("high", payment="COD"), "offer_type")
    assert "no wallet cashback" in _value(_plan("high", payment="Cash on Delivery"), "offer_type")
    assert _value(_plan("high", payment="COD", category="Grocery"), "offer_type") == "No discount in the Grocery category"
    assert "cashback" in _value(_plan("high", payment="UPI"), "offer_type")
    assert _value(_plan("low", payment="COD"), "offer_type") is None


def test_every_citation_is_a_real_section():
    sections = {f"[{Path(c.source).name} > {c.section}]" for p in DOCS for c in split_markdown(p)}
    for band in ("high", "medium", "low"):
        for complain in (0, 1):
            for tenure in (0.0, 10.0):
                for payment in ("COD", "UPI"):
                    for category in ("Grocery", "Mobile"):
                        assert all_citations(_plan(band, tenure, complain, payment, category)) <= sections


def test_the_playbook_states_the_low_risk_complaint_rule():
    text = (ROOT / "knowledge" / "harbor_vale" / "retention_playbook.md").read_text()
    assert "A customer below 0.40 who complained is still contacted" in text
    assert "a follow-up by the support team" in text
