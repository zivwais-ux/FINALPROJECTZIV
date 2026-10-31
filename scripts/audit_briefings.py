"""Check agent-written briefings against the decisions of the retention plan.

For briefings written before the plan existed, it looks for statements that
contradict the plan (a customer who must be contacted told "no outreach", a
welcome call for a customer the rule does not cover, wallet cashback for a
cash-on-delivery customer, an offer to a customer below 0.40). For briefings
rendered from the plan, it checks that the Plan section states every decision
exactly as retention_plan made it.

    uv run python scripts/audit_briefings.py      # exits 1 if any briefing contradicts its plan
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from churn_pipeline.retention_plan import retention_plan

ROOT = Path(__file__).resolve().parents[1]
BRIEFINGS = ROOT / "artifacts" / "latest" / "briefings"
CUSTOMERS = ROOT / "artifacts" / "latest" / "instant" / "customers.json"

NEGATION = re.compile(r"\b(no|not|never|cannot|can't|don't|do not|without|none)\b", re.I)


def _lines(text: str, heading: str) -> list[str]:
    """The lines under a "## heading" up to the next heading."""
    m = re.search(rf"^## {re.escape(heading)}.*?$(.*?)(?=^## |\Z)", text, re.M | re.S | re.I)
    return [l.strip() for l in m.group(1).splitlines() if l.strip()] if m else []


def audit(text: str, plan: dict, facts: dict) -> list[str]:
    problems = []
    plan_lines = _lines(text, "Plan")
    if plan_lines:  # rendered from the plan: every decision must be there, word for word
        for d in plan["decisions"]:
            if not any(d["value"] in l and l.startswith(f"- **{d['label']}:**") for l in plan_lines):
                problems.append(f"Plan does not state {d['label']}: {d['value']}")
        return problems

    lower = text.lower()
    action = " ".join(_lines(text, "Recommended action") + _lines(text, "Offer")).lower()
    if plan["contact"] and re.search(r"no individual outreach|do not contact this customer|not be contacted|"
                                     r"remain in the regular newsletter", action):
        problems.append("says not to contact a customer the playbook says to contact")
    if not any(d["id"] == "welcome" for d in plan["decisions"]):
        for l in action.split("- "):
            if "welcome call" in l and not NEGATION.search(l.split("welcome call")[0][-40:]):
                problems.append("recommends a welcome call the new-customer rule does not cover")
                break
    if facts.get("PreferredPaymentMode") in ("COD", "Cash on Delivery"):
        for l in action.split("- "):
            if "cashback" in l and not NEGATION.search(l):
                problems.append("offers wallet cashback to a cash-on-delivery customer")
                break
    if plan["band"] == "low":
        offer = " ".join(_lines(text, "Offer")).lower()
        if re.search(r"\b(offer|provide|give)\b[^.]*\b(discount|voucher|coupon|cashback)", offer) \
                and not NEGATION.search(offer):
            problems.append("makes an offer to a customer below 0.40, which the budget does not fund")
    if "risk score" not in lower:
        problems.append("does not state the risk score")
    return problems


def main() -> int:
    data = json.loads(CUSTOMERS.read_text(encoding="utf-8"))
    bad = 0
    files = sorted(BRIEFINGS.glob("customer_*.md"))
    for f in files:
        cid = f.stem.split("_")[1]
        score, band, _, facts, _ = data["customers"][cid]
        facts = dict(zip(data["key_facts"], facts))
        problems = audit(f.read_text(encoding="utf-8"), retention_plan(band, facts), facts)
        bad += bool(problems)
        print(f"{cid} {band:6} {'OK' if not problems else 'CONTRADICTS'}"
              + "".join(f"\n    - {p}" for p in problems))
    print(f"\n{len(files) - bad} of {len(files)} briefings agree with their retention plan")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
