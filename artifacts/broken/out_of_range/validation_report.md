# Validation report

- Verdict: **FAILED**
- Time (UTC): 2026-10-30 14:43:34
- Next step: Crew 2 did not run: fix the data or Crew 1, or update the locked contract on purpose, then run again

| Gate | Result | Summary |
|---|---|---|
| crew1_artifacts | PASS | all 8 Crew 1 artifacts present |
| contract_vs_data | FAIL | clean_data.csv breaks dataset_contract.json (2 violations) |
| locked_contract | PASS | dataset_contract.json matches the locked contract |
| required_features | PASS | all 18 required features available |

## contract_vs_data

- SatisfactionScore ranges 1..6, contract allows 1..5
- clean_data.csv has changed since the contract was written
