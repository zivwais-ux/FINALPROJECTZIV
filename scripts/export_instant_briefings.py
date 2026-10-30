"""Precompute what the web app needs for an instant briefing on any customer.

The app has no LLM, no scikit-learn and no embeddings key. This script does
the heavy parts once, with the approved model and the RAG index:

- artifacts/latest/instant/customers.json: score, band, key facts and
  situations for all customers (all_customer_profiles)
- artifacts/latest/instant/rag_hits.json: the RAG search results for every
  query the situations can produce (all_situation_queries); there are only a
  handful, because the code decides the queries

    uv run python scripts/export_instant_briefings.py   # needs OPENAI_API_KEY for the RAG queries

Run it after the pipeline approves a new model, then rebuild deploy/web.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from churn_pipeline.rag import default_index
from churn_pipeline.tools.briefing_tools import all_customer_profiles, all_situation_queries

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "latest" / "instant"


def main() -> int:
    profiles = all_customer_profiles()
    # Each (situation, query) pair is stored once; customers refer to it by index.
    pairs: list[tuple[str, str]] = []
    customers = {}
    for customer_id, c in profiles["customers"].items():
        refs = []
        for pair in zip(c["situations"], c["queries"]):
            if pair not in pairs:
                pairs.append(pair)
            refs.append(pairs.index(pair))
        customers[customer_id] = [c["score"], c["band"], int(c["out_of_sample"]), c["facts"], refs]

    index = default_index()
    hits = {q: index.search(q) for q in all_situation_queries()}

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "customers.json").write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model": profiles["model"],
        "band_rule": profiles["band_rule"],
        "key_facts": profiles["key_facts"],
        "fields": ["score", "band", "out_of_sample", "facts", "situations"],
        "situations": [{"situation": s, "query": q} for s, q in pairs],
        "customers": customers,
    }, separators=(",", ":")) + "\n", encoding="utf-8")
    (OUT / "rag_hits.json").write_text(json.dumps(hits, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    sizes = {p.name: f"{p.stat().st_size / 1024:.0f} KB" for p in OUT.glob("*.json")}
    print(f"{len(customers)} customers, {len(pairs)} situations, {len(hits)} RAG queries: {sizes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
