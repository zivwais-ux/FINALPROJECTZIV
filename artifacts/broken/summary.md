# break_it results

| Scenario | Break | Caught | Failed gates | Crew 2 ran | Problem reported |
|---|---|---|---|---|---|
| `unit_change` | CashbackAmount switched from INR to paise (x100), the Harbor & Vale incident | yes | contract_vs_data | no | CashbackAmount mean is 17,722.30, contract expects 177.22 (±1%); about 100x off, possible unit change (contract unit: INR (last month average)) |
| `rename_column` | Tenure renamed to TenureMonths upstream | yes | contract_vs_data, required_features | no | column 'Tenure' is in the contract but not in the data; possible rename to one of ['TenureMonths'] |
| `out_of_range` | one SatisfactionScore of 6 on a 1-5 scale | yes | contract_vs_data | no | SatisfactionScore ranges 1..6, contract allows 1..5 |
| `bad_category` | a new payment spelling, 'credit card', that the contract does not allow | yes | contract_vs_data | no | PreferredPaymentMode has values not allowed by the contract: ['credit card'] |
| `missing_feature` | the Complain column dropped from the handoff file | yes | contract_vs_data, required_features | no | required feature 'Complain' is not in clean_data.csv |
