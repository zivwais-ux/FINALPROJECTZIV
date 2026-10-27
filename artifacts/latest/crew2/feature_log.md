# Feature Log

## Inputs
- Input directory: /home/user/FINALPROJECTZIV/artifacts/latest/crew1
- Output directory: /home/user/FINALPROJECTZIV/artifacts/latest/crew2
- Source file: clean_data.csv
- Rows processed: 5,630

## Features
- Total feature columns created: 34
- Numeric features were kept unchanged with their missing values preserved:
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
- Categorical features were one-hot encoded with one 0/1 column per distinct category spelling:
  - PreferredLoginDevice: 3 columns (Computer, Mobile Phone, Phone)
  - PreferredPaymentMode: 7 columns (CC, COD, Cash on Delivery, Credit Card, Debit Card, E wallet, UPI)
  - Gender: 2 columns (Female, Male)
  - PreferedOrderCat: 6 columns (Fashion, Grocery, Laptop & Accessory, Mobile, Mobile Phone, Others)
  - MaritalStatus: 3 columns (Divorced, Married, Single)

## Missing Values
- Total missing values across all features: 1,856
- Missing values were kept as-is because both models handle missing data natively.
- No imputation was performed on any feature.

## Categories
- Each distinct category spelling was preserved as its own feature column.
- No merging or normalization of category spellings was done to maintain differences in churn rates across spellings.

## Excluded Columns
- CustomerID was excluded from the features as it is an identifier and can cause data leakage.
- duplicate_group is not a feature but a split key labeling rows that are copies or near-duplicates under different CustomerIDs.

## Leakage Risk
- Features labeled as "last month" (Complain, CouponUsed, OrderCount, CashbackAmount, PreferedOrderCat) remain in the dataset by team decision despite potential leakage risk.
- Duplicate rows and near-duplicates exist (1,736 duplicate groups containing 3,472 rows), which can leak information between train and test sets unless groups are kept intact during splitting.

This feature set fully complies with the contract and team decisions, enabling modeling to proceed with traceability and awareness of leakage risks.