# Feature Log

## Inputs
- Input directory: /home/user/FINALPROJECTZIV/artifacts/latest/crew1
- Output directory: /home/user/FINALPROJECTZIV/artifacts/latest/crew2
- Input file: clean_data.csv with 5,630 rows
- Target: Churn

## Features
- Total feature columns created: 34
- Numeric features kept unchanged with missing values preserved:
  - Tenure (264 missing)
  - CityTier (0 missing)
  - WarehouseToHome (251 missing)
  - HourSpendOnApp (255 missing)
  - NumberOfDeviceRegistered (0 missing)
  - SatisfactionScore (0 missing)
  - NumberOfAddress (0 missing)
  - Complain (0 missing)
  - OrderAmountHikeFromlastYear (265 missing)
  - CouponUsed (256 missing)
  - OrderCount (258 missing)
  - DaySinceLastOrder (307 missing)
  - CashbackAmount (0 missing)
- Categorical features one-hot encoded with one column per exact category spelling:
  - PreferredLoginDevice: 3 columns (Computer, Mobile Phone, Phone)
  - PreferredPaymentMode: 7 columns (CC, COD, Cash on Delivery, Credit Card, Debit Card, E wallet, UPI)
  - Gender: 2 columns (Female, Male)
  - PreferedOrderCat: 6 columns (Fashion, Grocery, Laptop & Accessory, Mobile, Mobile Phone, Others)
  - MaritalStatus: 3 columns (Divorced, Married, Single)

## Missing values
- Missing values are kept in all numeric features as is, totaling 1,856 missing values across features.
- No imputation was performed because both models handle missing values natively.

## Categories
- Each category spelling has its own dedicated column.
- No merging or renaming of category spellings was done to preserve differences in churn rates associated with different spellings.

## Excluded columns
- CustomerID is excluded from the features to avoid leakage and identification.
- duplicate_group is not a feature but a split key labeling rows that are copies of each other under different CustomerIDs.
- There are 1,736 duplicate groups containing 3,472 rows that are exact or near-exact copies differing only by CustomerID or one value.

## Leakage risk
- Last-month columns Complain, CouponUsed, OrderCount, CashbackAmount, and PreferedOrderCat remain in the features by team decision despite potential leakage risk.
- Duplicate groups must be kept entirely in either train or test split to avoid leakage between splits.
- Different spellings of categories with different churn rates may cause leakage but are preserved as is per team decision.