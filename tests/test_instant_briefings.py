"""The precomputed tables behind the app's instant briefing match the pipeline's own rules."""
import json
from pathlib import Path

from churn_pipeline.tools.briefing_tools import all_situation_queries, customer_risk_profile

ROOT = Path(__file__).resolve().parents[1]
INSTANT = ROOT / "artifacts" / "latest" / "instant"


def _tables():
    return (json.loads((INSTANT / "customers.json").read_text()),
            json.loads((INSTANT / "rag_hits.json").read_text()))


def test_every_customer_is_scored():
    customers, _ = _tables()
    clean_rows = sum(1 for _ in open(ROOT / "artifacts" / "latest" / "crew1" / "clean_data.csv")) - 1
    assert len(customers["customers"]) == clean_rows == 5630


def test_rag_results_cover_every_query_the_code_can_ask():
    customers, hits = _tables()
    assert set(all_situation_queries()) <= set(hits)
    assert {s["query"] for s in customers["situations"]} <= set(hits)
    assert all(len(h) >= 2 and h[0]["cite_as"].endswith("]") for h in hits.values())


def test_table_matches_the_live_profile_tool():
    customers, _ = _tables()
    for cid in (51809, 50230, 50036, 50001, 55630):
        live = customer_risk_profile(cid)
        score, band, out_of_sample, facts, refs = customers["customers"][str(cid)]
        assert (score, band, bool(out_of_sample)) == (live["risk_score"], live["risk_band"],
                                                      live["scored_out_of_sample"])
        assert facts == list(live["key_facts"].values())
        assert [customers["situations"][r]["query"] for r in refs] == [s["query"] for s in live["situations"]]
