# Contract Review

## Verdict
The contract validation PASSED with no violations. Modeling may start.

## Target
- Contract version: 1.0.0  
- Row count: 5,630  
- Target: Churn  
- Expected churn rate: 0.1684

## Features
| Feature Name           | Type     | Unit                      | Unit Source  |
|-----------------------|----------|---------------------------|--------------|
| Tenure                | int      | months                    | assumed      |
| PreferredLoginDevice   | category | (none)                    | (none)       |
| CityTier              | int      | tier                      | data_dict    |
| WarehouseToHome       | int      | km                        | assumed      |
| PreferredPaymentMode   | category | (none)                    | (none)       |
| Gender                | category | (none)                    | (none)       |
| HourSpendOnApp        | int      | hours                     | data_dict    |
| NumberOfDeviceRegistered | int    | count                     | data_dict    |
| PreferedOrderCat      | category | (none)                    | (none)       |
| SatisfactionScore     | int      | score                     | data_dict    |
| MaritalStatus         | category | (none)                    | (none)       |
| NumberOfAddress       | int      | count                     | data_dict    |
| Complain              | binary   | flag (last month)         | data_dict    |
| OrderAmountHikeFromlastYear | int | percent                   | data_dict    |
| CouponUsed            | int      | count (last month)        | data_dict    |
| OrderCount            | int      | count (last month)        | data_dict    |
| DaySinceLastOrder     | int      | days                      | data_dict    |
| CashbackAmount        | float    | INR (last month average)  | assumed      |

## Excluded columns
- CustomerID: Forbidden to avoid leakage and identification.

## Duplicates
"1,112 rows are exact copies of another row except for their id (556 of them repeat an earlier row under a new id). Counting copies with one value changed as well, 3,472 rows form 1,736 groups of at most 2 rows, each row with its own id."

This means there are many duplicate or near-duplicate rows differing only by CustomerID or one value. Care must be taken to keep each duplicate group entirely in either train or test split to avoid leakage.

## Assumptions and Leakage Notes
- No imputation was performed on missing values; missing values are preserved as in the raw data.
- No merging or renaming of categorical values was done; category spellings are kept exactly as in the raw data.
- Outliers are retained without any clipping or removal.
- Duplicate rows are kept; 1,112 rows are exact or near-exact copies of another row except for their CustomerID, forming 1,736 groups of duplicates.
- Units are assumed as follows: Tenure in months, WarehouseToHome in kilometers, CashbackAmount in Indian Rupees (INR).
- The churn window is undefined, so features labeled as 'last month' such as Complain, CouponUsed, OrderCount, CashbackAmount, and PreferedOrderCat may leak information about churn.
- Different spellings of similar categories (e.g., 'Mobile Phone' vs 'Phone', 'COD' vs 'Cash on Delivery', 'Mobile' vs 'Mobile Phone') have different churn rates and may cause leakage.
- Duplicate rows leak information between train and test sets unless each group of duplicates is kept entirely on one side of the split.