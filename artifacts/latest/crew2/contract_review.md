# Contract Review

## Verdict
The contract validation **PASSED** with no violations. Modeling may start based on this dataset and contract.

## Target
- Contract version: 1.0.0  
- Row count: 5,630  
- Target: Churn  
- Expected churn rate: 0.1684

## Features
Usable features with type and unit (units marked as assumed where applicable):

| Feature                | Type      | Unit                     | Unit Source  | Expected Nulls |
|------------------------|-----------|--------------------------|--------------|----------------|
| Tenure                 | int       | months                   | assumed      | 264            |
| PreferredLoginDevice    | category  | -                        | -            | 0              |
| CityTier               | int       | tier                     | data_dict    | 0              |
| WarehouseToHome        | int       | km                       | assumed      | 251            |
| PreferredPaymentMode    | category  | -                        | -            | 0              |
| Gender                 | category  | -                        | -            | 0              |
| HourSpendOnApp         | int       | hours                    | data_dict    | 255            |
| NumberOfDeviceRegistered| int       | count                    | data_dict    | 0              |
| PreferedOrderCat       | category  | -                        | -            | 0              |
| SatisfactionScore      | int       | score                    | data_dict    | 0              |
| MaritalStatus          | category  | -                        | -            | 0              |
| NumberOfAddress        | int       | count                    | data_dict    | 0              |
| Complain               | binary    | flag (last month)        | data_dict    | 0              |
| OrderAmountHikeFromlastYear | int  | percent                  | data_dict    | 265            |
| CouponUsed             | int       | count (last month)       | data_dict    | 256            |
| OrderCount             | int       | count (last month)       | data_dict    | 258            |
| DaySinceLastOrder      | int       | days                     | data_dict    | 307            |
| CashbackAmount         | float     | INR (last month average) | assumed      | 0              |

## Excluded columns
- CustomerID: Forbidden as it is an identifier and can cause data leakage.

## Duplicates
"1,112 rows are exact copies of another row except for their id (556 of them repeat an earlier row under a new id). Counting copies with one value changed as well, 3,472 rows form 1,736 groups of at most 2 rows, each row with its own id."

This means there are many duplicate rows and near-duplicates in the dataset. For train/test splitting, it is critical to keep all rows in each duplicate group entirely on one side of the split to avoid leakage.

## Assumptions and Leakage
- No imputation was performed on missing values; missing data is preserved as in the raw dataset.
- No merging or renaming of categorical values was done; categories are kept exactly as in the raw data.
- Outliers are retained as-is without clipping or removal.
- Duplicate rows are kept, including those repeated under a new CustomerID either exactly or with one value changed; counts of duplicates are provided above.
- Units are assumed as follows: Tenure in months, WarehouseToHome in kilometers, CashbackAmount in Indian Rupees (INR).
- The churn window is undefined, so features labeled as 'last month' such as Complain, CouponUsed, OrderCount, CashbackAmount, and PreferedOrderCat may leak information about churn.
- Different spellings of similar categories with significantly different churn rates are kept separate, which may cause leakage.
- Duplicate rows leak information between train and test sets unless each group of duplicate copies is kept entirely on one side of the data split.

---

This detailed review confirms the dataset matches the contract and highlights critical points for modeling and data splitting to avoid leakage.