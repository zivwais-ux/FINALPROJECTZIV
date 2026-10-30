# Contract Review

## Verdict
The contract validation PASSED with no violations. Modeling may start.

## Target
- Contract version: 1.0.0  
- Row count: 5,630  
- Target: Churn  
- Expected churn rate: 0.1684

## Features
Usable features with type and unit (units marked as assumed where applicable):

| Feature                | Type      | Unit                   | Unit Source  | Expected Nulls |
|------------------------|-----------|------------------------|--------------|----------------|
| Tenure                 | int       | months                 | assumed      | 264            |
| PreferredLoginDevice    | category  | -                      | -            | 0              |
| CityTier               | int       | tier                   | data_dict    | 0              |
| WarehouseToHome        | int       | km                     | assumed      | 251            |
| PreferredPaymentMode    | category  | -                      | -            | 0              |
| Gender                 | category  | -                      | -            | 0              |
| HourSpendOnApp         | int       | hours                  | data_dict    | 255            |
| NumberOfDeviceRegistered| int       | count                  | data_dict    | 0              |
| PreferedOrderCat       | category  | -                      | -            | 0              |
| SatisfactionScore      | int       | score                  | data_dict    | 0              |
| MaritalStatus          | category  | -                      | -            | 0              |
| NumberOfAddress        | int       | count                  | data_dict    | 0              |
| Complain               | binary    | flag (last month)      | data_dict    | 0              |
| OrderAmountHikeFromlastYear | int  | percent                | data_dict    | 265            |
| CouponUsed             | int       | count (last month)     | data_dict    | 256            |
| OrderCount             | int       | count (last month)     | data_dict    | 258            |
| DaySinceLastOrder      | int       | days                   | data_dict    | 307            |
| CashbackAmount         | float     | INR (last month average)| assumed     | 0              |

## Excluded columns
- CustomerID: Forbidden feature (likely due to privacy or leakage risk).

## Duplicates
"1,112 rows are exact copies of another row except for their id (556 of them repeat an earlier row under a new id). Counting copies with one value changed as well, 3,472 rows form 1,736 groups of at most 2 rows, each row with its own id."

This means there is a significant presence of duplicate rows and near-duplicates. For the train/test split, it is critical that each group of duplicate copies is kept entirely on one side of the split to avoid leakage.

## Assumptions and leakage
- No imputation was performed on missing values; missing data is preserved as-is.
- No merging or renaming of categorical values was done; categories are kept exactly as in the raw data.
- Outliers are retained without any clipping or removal.
- Duplicate rows are kept, including rows repeated under a new CustomerID either exactly or with one value changed.
- Units are assumed as follows: Tenure in months, WarehouseToHome in kilometers, CashbackAmount in Indian Rupees (INR).
- The churn window is undefined, so features labeled as "last month" such as Complain, CouponUsed, OrderCount, CashbackAmount, and PreferedOrderCat may leak information about churn.
- Different spellings of similar categories with different churn rates (e.g., "Mobile Phone" vs "Phone", "COD" vs "Cash on Delivery") are kept separate and may cause leakage.
- Duplicate rows leak information between train and test sets unless each group of duplicate copies is kept entirely on one side of the data split.

---

This detailed review confirms the dataset matches the contract and highlights important considerations for modeling and data splitting.