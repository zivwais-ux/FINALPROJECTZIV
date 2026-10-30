# Validation report

- Verdict: **FAILED**
- Time (UTC): 2026-10-30 17:37:14
- Next step: Crew 2 did not run: fix the data or Crew 1, or update the locked contract on purpose, then run again

| Gate | Result | Summary |
|---|---|---|
| crew1_artifacts | PASS | all 8 Crew 1 artifacts present |
| contract_vs_data | FAIL | clean_data.csv breaks dataset_contract.json (3 violations) |
| locked_contract | PASS | dataset_contract.json matches the locked contract |
| required_features | PASS | all 18 required features available |

## contract_vs_data

- CashbackAmount ranges 0..32499, contract allows 0..324.99
- CashbackAmount mean is 17,722.30, contract expects 177.22 (±1%); about 100x off, possible unit change (contract unit: INR (last month average))
- clean_data.csv has changed since the contract was written
