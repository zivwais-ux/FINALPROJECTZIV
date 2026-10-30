"""The customers picked for agent-written briefings follow the stated rules."""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("pick_customers", ROOT / "scripts" / "pick_briefing_customers.py")
pick_customers = importlib.util.module_from_spec(_spec)
sys.modules["pick_customers"] = pick_customers
_spec.loader.exec_module(pick_customers)

CUSTOMERS = ROOT / "artifacts" / "latest" / "instant" / "customers.json"


def test_pick_is_deterministic_out_of_sample_and_per_band():
    already = {51809, 50230, 50036}
    first = pick_customers.pick(CUSTOMERS, already)
    assert first == pick_customers.pick(CUSTOMERS, already)
    assert len(first) == sum(pick_customers.PER_BAND.values()) == 20
    assert not already & set(first)
    rows = json.loads(CUSTOMERS.read_text())["customers"]
    assert all(rows[str(c)][2] for c in first)  # all from the test set
    bands = [rows[str(c)][1] for c in first]
    assert {b: bands.count(b) for b in set(bands)} == pick_customers.PER_BAND


def test_pick_covers_every_category():
    data = json.loads(CUSTOMERS.read_text())
    cat = data["key_facts"].index("PreferedOrderCat")
    picked = pick_customers.pick(CUSTOMERS, set())
    categories = {data["customers"][str(c)][3][cat] for c in picked}
    assert categories == {"Mobile", "Mobile Phone", "Laptop & Accessory", "Fashion", "Grocery", "Others"}
