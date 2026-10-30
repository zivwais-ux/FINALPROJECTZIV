"""Pick customers for agent-written briefings, by rule rather than by hand.

Only customers from the test set (the model never saw them in training), a
fixed number per risk band, chosen so that together they cover every
situation the briefing knows (complaint, new customer, cash on delivery,
each category) before repeating one. Ties go to the lowest CustomerID, so
the pick is the same on every run.

    uv run python scripts/pick_briefing_customers.py            # prints the IDs
    uv run brief $(uv run python scripts/pick_briefing_customers.py)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PER_BAND = {"high": 8, "medium": 6, "low": 6}


def pick(customers_json: Path, already: set[int], per_band: dict[str, int] = PER_BAND) -> list[int]:
    data = json.loads(customers_json.read_text(encoding="utf-8"))
    category = data["key_facts"].index("PreferedOrderCat")
    chosen: list[int] = []
    for band, count in per_band.items():
        pool = sorted((int(cid), row) for cid, row in data["customers"].items()
                      if row[1] == band and row[2] and int(cid) not in already)
        covered: set[str] = set()
        for _ in range(count):
            def gain(item):
                cid, row = item
                tags = {data["situations"][r]["situation"] for r in row[4]} | {f"category {row[3][category]}"}
                return len(tags - covered), -cid
            if not pool:
                break
            best = max(pool, key=gain)
            pool.remove(best)
            cid, row = best
            covered |= {data["situations"][r]["situation"] for r in row[4]} | {f"category {row[3][category]}"}
            chosen.append(cid)
    return chosen


def main() -> int:
    already = {int(p.stem.split("_")[1]) for p in (ROOT / "artifacts" / "latest" / "briefings").glob("customer_*.md")}
    print(" ".join(map(str, pick(ROOT / "artifacts" / "latest" / "instant" / "customers.json", already))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
