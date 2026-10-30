# Validation report

- Verdict: **FAILED**
- Time (UTC): 2026-10-30 17:37:14
- Next step: Crew 2 did not run: fix the data or Crew 1, or update the locked contract on purpose, then run again

| Gate | Result | Summary |
|---|---|---|
| crew1_artifacts | PASS | all 8 Crew 1 artifacts present |
| contract_vs_data | FAIL | clean_data.csv breaks dataset_contract.json (3 violations) |
| locked_contract | PASS | dataset_contract.json matches the locked contract |
| required_features | FAIL | 1 of 18 required features unavailable |

## contract_vs_data

- column 'Tenure' is in the contract but not in the data; possible rename to one of ['TenureMonths']
- column 'TenureMonths' is in the data but not in the contract
- clean_data.csv has changed since the contract was written

## required_features

- required feature 'Tenure' is not in clean_data.csv
