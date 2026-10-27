# Validation report

- Verdict: **PASSED**
- Time (UTC): 2026-10-27 20:46:45
- Next step: model approved (model_approved.json written)

| Gate | Result | Summary |
|---|---|---|
| crew1_artifacts | PASS | all 8 Crew 1 artifacts present |
| contract_vs_data | PASS | clean_data.csv matches dataset_contract.json |
| locked_contract | PASS | dataset_contract.json matches the locked contract |
| required_features | PASS | all 18 required features available |
| model_quality | PASS | hist_gradient_boosting passes: pr_auc 0.8636 (min 0.80), recall 0.6667 (min 0.60) |
