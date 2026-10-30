# Validation report

- Verdict: **FAILED**
- Time (UTC): 2026-10-30 14:43:15
- Next step: Crew 2 did not run: fix the data or Crew 1, or update the locked contract on purpose, then run again

| Gate | Result | Summary |
|---|---|---|
| crew1_artifacts | PASS | all 8 Crew 1 artifacts present |
| contract_vs_data | PASS | clean_data.csv matches dataset_contract.json |
| locked_contract | FAIL | dataset_contract.json differs from the locked contract (5 differences) |
| required_features | PASS | all 18 required features available |

## locked_contract

- columns.CashbackAmount.dtype: locked 'float', new 'int'
- columns.CashbackAmount.expected_mean: locked 177.223, new 17722.303
- columns.CashbackAmount.expected_std: locked 49.207, new 4920.7036
- columns.CashbackAmount.range.max: locked 324.99, new 32499.0
- dataset.sha256: locked 'e0c951d4a9a94a650ff514da4c0152b473b1ab026aeddf0662ced46e5f847019', new '0229971d31dd465dfc7a253408c5ef95cd703f78e46eca8a24fb24941b9b9d23'
