# Feature Log

## Inputs
- Input directory: /home/user/FINALPROJECTZIV/artifacts/latest/crew1
- Output directory: /home/user/FINALPROJECTZIV/artifacts/latest/crew2
- Source file: clean_data.csv
- Rows processed: 5,630
- Target variable: Churn
- Duplicate groups: 1,736 groups containing 3,472 rows (rows that are exact or near duplicates under different CustomerIDs)

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
- Categorical features were one-hot encoded with one binary column per distinct category spelling, preserving all spellings separately:
  - PreferredLoginDevice: 3 columns (Computer, Mobile Phone, Phone)
  - PreferredPaymentMode: 7 columns (CC, COD, Cash on Delivery, Credit Card, Debit Card, E wallet, UPI)
  - Gender: 2 columns (Female, Male)
  - PreferedOrderCat: 6 columns (Fashion, Grocery, Laptop & Accessory, Mobile, Mobile Phone, Others)
  - MaritalStatus: 3 columns (Divorced, Married, Single)

## Missing values
- Total missing values kept across all features: 1,856
- Missing values were not imputed or filled; they remain as in the original data.
- Both modeling approaches handle missing values natively, so no imputation was performed.

## Categories
- Each distinct category spelling was preserved as its own feature column.
- No merging or normalization of category spellings was done to avoid masking differences in churn rates between similar but differently spelled categories.
- Examples include separate columns for "Mobile Phone" and "Phone" or "COD" and "Cash on Delivery".

## Excluded columns
- CustomerID was excluded from the features as per team decision due to privacy and leakage risk.
- The duplicate_group column is not a feature but a split key to identify groups of duplicate or near-duplicate rows under different CustomerIDs.

## Leakage risk
- Features labeled as "last month" (Complain, CouponUsed, OrderCount, CashbackAmount, PreferedOrderCat) remain in the dataset by team decision despite potential leakage risk.
- Duplicate rows and near-duplicates under different CustomerIDs pose a leakage risk if not kept entirely on one side of the train/test split.
- Different spellings of similar categories with different churn rates may also cause leakage but are preserved as-is per team instructions.

---

This feature engineering strictly follows the contract and team decisions: no imputation, no category merging, outliers kept, CustomerID excluded, and careful documentation of missing values and leakage risks.