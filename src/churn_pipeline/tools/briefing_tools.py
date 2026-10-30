"""Deterministic tools for the retention briefing.

customer_risk_profile scores one customer with the approved churn model and
returns the facts a briefing may quote. Like the playbook says, it refuses to
score anything unless the latest pipeline run passed every gate.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from crewai.tools import tool

from churn_pipeline.news import news_query, search_recent_news
from churn_pipeline.tools.scientist_tools import split_indices

ROOT = Path(__file__).resolve().parents[3]
CREW1 = ROOT / "artifacts" / "latest" / "crew1"
CREW2 = ROOT / "artifacts" / "latest" / "crew2"
REPORT = ROOT / "artifacts" / "latest" / "validation_report.md"

# Risk bands from knowledge/harbor_vale/retention_playbook.md ("Who we contact first").
HIGH_RISK = 0.70
MEDIUM_RISK = 0.40


def require_approved_model(crew2_dir: str | Path = CREW2, report_path: str | Path = REPORT) -> None:
    """Raise unless the last run approved the model and its validation report says PASSED."""
    report = Path(report_path)
    if not (Path(crew2_dir) / "model_approved.json").is_file():
        raise ValueError("no approved model: the last pipeline run did not pass the quality gate")
    if not report.is_file() or "**PASSED**" not in report.read_text(encoding="utf-8"):
        raise ValueError(f"the latest validation report ({report.name}) does not say PASSED")


# The attributes a briefing shows, in this order; the rest stay in the tool output.
KEY_FACTS = ["Tenure", "Complain", "PreferredPaymentMode", "PreferedOrderCat", "SatisfactionScore",
             "DaySinceLastOrder", "OrderCount", "CashbackAmount"]


def risk_band(score: float) -> str:
    return "high" if score >= HIGH_RISK else "medium" if score >= MEDIUM_RISK else "low"


def situations(band: str, attributes: dict[str, Any]) -> list[dict[str, str]]:
    """What applies to this customer, each with the search query that finds its policy.

    Built in code so the briefing always looks up the rules that matter
    (a complaint, a new customer, cash on delivery), not whatever the agent
    happens to search for.
    """
    out = [{"situation": f"{band} churn risk",
            "query": f"who we contact first and which channel for {band} risk customers"}]
    tenure = attributes.get("Tenure")
    # The playbook's new-customer rule covers customers the model flagged, not low-risk ones.
    if tenure is not None and tenure <= 1 and band != "low":
        out.append({"situation": "new customer (tenure 0 to 1 months)",
                    "query": "new customers in their first months welcome call first contact discount"})
    if attributes.get("Complain") == 1:
        out.append({"situation": "complained in the last month",
                    "query": "customer complained coupon resolve before you reward"})
    if attributes.get("PreferredPaymentMode") in ("COD", "Cash on Delivery"):
        out.append({"situation": "pays cash on delivery",
                    "query": "cash on delivery customers cashback free delivery voucher"})
    category = attributes.get("PreferedOrderCat")
    if category in ("Mobile", "Mobile Phone"):
        out.append({"situation": f"prefers the {category} category",
                    "query": "competitor offers for phone buyers mobile category"})
    elif category == "Grocery":
        out.append({"situation": "prefers the Grocery category", "query": "discounts in the Grocery category"})
    if band != "low":
        out.append({"situation": "an offer may be made",
                    "query": "discount limits per customer and approval levels"})
    return out


def all_situation_queries() -> list[str]:
    """Every search query situations() can produce, for every band and attribute that matters."""
    queries: dict[str, None] = {}
    for band, tenure, complain, payment, category in itertools.product(
            ("high", "medium", "low"), (0, 5), (0, 1), ("COD", "UPI"), ("Mobile", "Grocery", "Fashion")):
        for s in situations(band, {"Tenure": tenure, "Complain": complain,
                                   "PreferredPaymentMode": payment, "PreferedOrderCat": category}):
            queries[s["query"]] = None
    return list(queries)


def _plain(v: Any) -> Any:
    """A JSON-friendly value: NaN becomes None, floats are rounded to 2 places."""
    if pd.isna(v):
        return None
    v = v.item() if hasattr(v, "item") else v
    return round(v, 2) if isinstance(v, float) else v


def all_customer_profiles(crew1_dir: str | Path = CREW1, crew2_dir: str | Path = CREW2,
                          report_path: str | Path = REPORT) -> dict[str, Any]:
    """Score every customer at once, with the same rules as customer_risk_profile.

    The web app shows an instant briefing for any CustomerID from this table,
    so it needs neither scikit-learn nor the model file.
    """
    require_approved_model(crew2_dir, report_path)
    crew2_dir = Path(crew2_dir)
    bundle = joblib.load(crew2_dir / "model.joblib")
    spec = json.loads((crew2_dir / "feature_spec.json").read_text(encoding="utf-8"))
    metrics = json.loads((crew2_dir / "evaluation_metrics.json").read_text(encoding="utf-8"))
    features = pd.read_csv(crew2_dir / "features.csv")
    clean = pd.read_csv(Path(crew1_dir) / "clean_data.csv").set_index(spec["id_columns"][0])
    scores = bundle["model"].predict_proba(features[bundle["feature_columns"]])[:, 1]
    test = set(split_indices(features, spec)[1])

    customers = {}
    for i, (customer_id, score) in enumerate(zip(features[spec["id_columns"][0]], scores)):
        attributes = {c: _plain(v) for c, v in clean.loc[customer_id].items() if c != spec["target"]}
        band = risk_band(float(score))
        customers[str(int(customer_id))] = {
            "score": round(float(score), 2), "band": band, "out_of_sample": i in test,
            "facts": [attributes.get(c) for c in KEY_FACTS],
            "situations": [s["situation"] for s in situations(band, attributes)],
            "queries": [s["query"] for s in situations(band, attributes)],
        }
    return {"model": metrics["selected_model"], "key_facts": KEY_FACTS,
            "band_rule": {"high": HIGH_RISK, "medium": MEDIUM_RISK}, "customers": customers}


def customer_risk_profile(customer_id: int, crew1_dir: str | Path = CREW1, crew2_dir: str | Path = CREW2,
                          report_path: str | Path = REPORT) -> dict[str, Any]:
    require_approved_model(crew2_dir, report_path)
    crew2_dir = Path(crew2_dir)
    bundle = joblib.load(crew2_dir / "model.joblib")
    spec = json.loads((crew2_dir / "feature_spec.json").read_text(encoding="utf-8"))
    metrics = json.loads((crew2_dir / "evaluation_metrics.json").read_text(encoding="utf-8"))
    features = pd.read_csv(crew2_dir / "features.csv")
    clean = pd.read_csv(Path(crew1_dir) / "clean_data.csv")
    id_col = spec["id_columns"][0]

    rows = features.index[features[id_col] == int(customer_id)]
    if len(rows) == 0:
        raise ValueError(f"customer {customer_id} is not in the data")
    i = rows[0]
    score = float(bundle["model"].predict_proba(features.loc[[i], bundle["feature_columns"]])[:, 1][0])
    _, test_idx = split_indices(features, spec)

    raw = clean.loc[clean[id_col] == int(customer_id)].iloc[0]
    attributes = {c: (None if pd.isna(v) else
                      round(v.item(), 2) if isinstance(v.item() if hasattr(v, "item") else v, float) else
                      (v.item() if hasattr(v, "item") else v))
                  for c, v in raw.items() if c not in (id_col, spec["target"])}
    return {
        "customer_id": int(customer_id),
        "risk_score": round(score, 2),
        "risk_band": risk_band(score),
        "risk_band_rule": f"high >= {HIGH_RISK}, medium >= {MEDIUM_RISK}, otherwise low (retention playbook)",
        "scored_out_of_sample": bool(i in set(test_idx)),
        "score_note": ("the model never saw this customer during training"
                       if i in set(test_idx) else
                       "this customer was in the training data, so the score is optimistic about the model"),
        "key_facts": {c: attributes.get(c) for c in KEY_FACTS},
        "missing_facts": [c for c in KEY_FACTS if attributes.get(c) is None],
        "situations": situations(risk_band(score), attributes),
        "news_query": news_query(attributes.get("PreferedOrderCat")),
        "model": {"name": metrics["selected_model"], "test_pr_auc": metrics["selected_test_metrics"]["pr_auc"],
                  "test_recall": metrics["selected_test_metrics"]["recall"],
                  "top_features": [t["feature"] for t in metrics["top_features_by_permutation"][:5]]},
    }


@tool("customer_risk_profile")
def customer_risk_profile_tool(customer_id: int) -> str:
    """Score one customer (by CustomerID) with the approved churn model. Returns as JSON the risk
    score, the playbook's risk band, whether the score is out of sample, the customer's key facts
    (tenure in months, complaint flag, payment mode, preferred category and more), the situations
    that apply to the customer with a search query for each, and the model's test metrics.
    Refuses if the latest pipeline run did not pass every gate."""
    return json.dumps(customer_risk_profile(customer_id), ensure_ascii=False)


@tool("search_recent_news")
def search_recent_news_tool(query: str) -> str:
    """Search the web for news from the last 48 hours (Google News, English-language news in India).
    Pass the news_query from customer_risk_profile exactly as given. Returns JSON with up to five
    articles (title, url, source, published) newest first, or an error when the search failed."""
    return json.dumps(search_recent_news(query), ensure_ascii=False)
