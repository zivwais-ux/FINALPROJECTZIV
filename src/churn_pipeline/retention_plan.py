"""What the retention team should do for one customer, decided in code.

The retention playbook and the discount policy (knowledge/harbor_vale/) are
rules, so they are applied here, not by the LLM. Each decision carries the
document section it comes from. The briefing agent only explains these
decisions; the briefing states them exactly as decided here, so an agent can
no longer contradict the playbook (for example by telling the team not to
contact a customer who complained).

No crewai, no model: the web app uses it for the instant briefing too.
"""
from __future__ import annotations

from typing import Any

PLAYBOOK = "retention_playbook.md"
POLICY = "discount_policy.md"


def _cite(doc: str, section: str) -> str:
    return f"[{doc} > {section}]"


WHO_FIRST = _cite(PLAYBOOK, "Who we contact first")
CHANNELS = _cite(PLAYBOOK, "Channels")
NEW_CUSTOMERS = _cite(PLAYBOOK, "New customers (tenure 0 to 1 months)")
COMPLAINED = _cite(PLAYBOOK, "Customers who complained")
COD = _cite(PLAYBOOK, "Cash on delivery (COD) customers")
NEVER = _cite(PLAYBOOK, "What we never do")
LIMITS = _cite(POLICY, "Limits per customer")
APPROVALS = _cite(POLICY, "Approval levels")
EXTRA_CARE = _cite(POLICY, "Offers that need extra care")

COD_MODES = ("COD", "Cash on Delivery")


def retention_plan(band: str, facts: dict[str, Any]) -> dict[str, Any]:
    """The decisions for a customer in risk band (high, medium, low) with these facts.

    facts needs Tenure, Complain, PreferredPaymentMode and PreferedOrderCat;
    a missing value counts as unknown, never as a yes.
    """
    tenure = facts.get("Tenure")
    complained = facts.get("Complain") == 1
    new = tenure is not None and tenure <= 1 and band != "low"  # the playbook covers flagged new customers
    cod = facts.get("PreferredPaymentMode") in COD_MODES
    grocery = facts.get("PreferedOrderCat") == "Grocery"

    decisions: list[dict[str, Any]] = []

    def add(key: str, label: str, value: str, *cites: str) -> None:
        decisions.append({"id": key, "label": label, "value": value, "cites": list(cites)})

    # Contact, priority and channel.
    if band == "high":
        add("contact", "Contact", "Yes, priority 1 (risk 0.70 or higher)", WHO_FIRST)
        add("channel", "Channel", "Phone call by a retention agent", CHANNELS)
    elif complained:
        add("contact", "Contact", "Yes, priority 2 (complained in the last month, whatever the score)", WHO_FIRST)
        if band == "medium":
            add("channel", "Channel", "App push notification, then email after 2 days without response", CHANNELS)
        else:
            add("channel", "Channel", "Follow-up by the support team to close the complaint", CHANNELS)
    elif band == "medium":
        add("contact", "Contact", "Yes, priority 3 (risk 0.40 to 0.70)", WHO_FIRST)
        add("channel", "Channel", "App push notification, then email after 2 days without response", CHANNELS)
    else:
        add("contact", "Contact", "No individual outreach; the customer stays in the regular newsletter", WHO_FIRST)
    contact = band != "low" or complained
    if contact:
        add("frequency", "Frequency", "At most twice in 14 days", CHANNELS)

    # What to do first.
    if complained:
        add("complaint", "Complaint", "Close the complaint before any coupon or offer", COMPLAINED)
    if new:
        add("welcome", "New customer", "Welcome call within 3 days plus a follow-up email; "
            "no discount on this first contact", NEW_CUSTOMERS)

    # The offer: when, what and who approves it.
    if band == "low":
        add("offer", "Offer", "None: offers to customers below 0.40 are not funded", EXTRA_CARE)
    else:
        if complained:
            when = "Only after the complaint is closed"
        elif new:
            when = "Not on the first contact; only if still at risk a week later"
        else:
            when = "Allowed now"
        add("offer", "Offer", when, COMPLAINED if complained else (NEW_CUSTOMERS if new else LIMITS))
        if grocery:
            add("offer_type", "Offer type", "No discount in the Grocery category", EXTRA_CARE)
        elif cod:
            add("offer_type", "Offer type", "Free-delivery voucher or a small invoice discount; no wallet cashback",
                COD)
        else:
            add("offer_type", "Offer type", "Discount or wallet cashback within the limits", LIMITS)
        add("limits", "Limits", "Up to INR 500 or 15% of the next order, whichever is lower; cashback up to "
            "INR 300; one offer per 30 days", LIMITS)
        add("approval", "Approval", "Agent up to INR 300; team lead for INR 301 to 500; never above INR 500",
            APPROVALS)

    # What the plan already rules out (no cashback, no coupon yet, the frequency cap) is not repeated here.
    never = [{"value": "Do not tell the customer their churn score", "cites": [NEVER]}]

    return {"band": band, "contact": contact, "decisions": decisions, "never": never}


def all_citations(plan: dict[str, Any]) -> set[str]:
    return {c for d in plan["decisions"] + plan["never"] for c in d["cites"]}
