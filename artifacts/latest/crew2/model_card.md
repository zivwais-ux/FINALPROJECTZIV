# Model Card for Harbor & Vale Retention Team

---

## Model Details

- **Selected Model:** HistGradientBoosting
- **Decision Threshold:** 0.5
- **Model File Location:** /home/user/FINALPROJECTZIV/artifacts/latest/crew2/model.joblib

The model was selected based on the highest mean PR-AUC over 5-fold stratified group cross-validation on the training split.

---

## Intended Use

This model is intended to rank customers by their risk of churn to enable targeted retention discounts and campaigns. It supports prioritizing outreach efforts to customers most likely to churn.

**Out of Scope:**  
The model should not be used to make automated decisions about individual customers without human review. It is designed for ranking and prioritization, not for sole decision-making on single cases.

---

## Training Data

- **Source File:** clean_data.csv
- **SHA256 Hash:** e0c951d4a9a94a650ff514da4c0152b473b1ab026aeddf0662ced46e5f847019
- **Number of Rows:** 5,630
- **Churn Rate:** 16.84%
- **Contract Version:** 1.0.0

**Duplicate Rows:**  
"1,112 rows are exact copies of another row except for their id (556 of them repeat an earlier row under a new id). Counting copies with one value changed as well, 3,472 rows form 1,736 groups of at most 2 rows, each row with its own id."

The data split uses StratifiedGroupKFold(5) with stratification on churn and grouping by duplicate groups to ensure no duplicate groups appear in both train and test sets, preventing leakage.

---

## Features

- **Number of Features:** 34 (after encoding)
- **Encoding:**  
  - Categorical features are one-hot encoded (e.g., PreferredLoginDevice, PreferredPaymentMode, Gender, PreferedOrderCat, MaritalStatus).  
  - Numerical features are kept unchanged.
- **Missing Values:** Missing values are preserved as in the raw data; no imputation was performed.
- **Forbidden Columns:** CustomerID is excluded to avoid leakage and identification.

---

## Metrics

| Metric           | Value  | Baseline | Quality Threshold | Pass/Fail |
|------------------|--------|----------|-------------------|-----------|
| Test PR-AUC      | 0.8636 | 0.1679   | 0.8               | Pass      |
| Test Recall      | 0.6667 | -        | 0.6               | Pass      |
| Test Precision   | 0.9    | -        | -                 | -         |
| Test ROC-AUC     | 0.9497 | -        | -                 | -         |

The model substantially outperforms the baseline PR-AUC (equal to the churn rate) indicating strong predictive performance.

---

## Assumptions

- Units are assumed as follows:  
  - Tenure in months  
  - WarehouseToHome in kilometers  
  - CashbackAmount in Indian Rupees (INR, last month average)
- No imputation or modification of missing values; missing values remain as in the raw data.
- No merging or renaming of categorical values; category spellings are preserved exactly as in the raw data.
- Outliers are retained without clipping or removal.
- Duplicate rows are kept, forming 1,736 groups of duplicates.
- The churn window is undefined; features labeled as "last month" (e.g., Complain, CouponUsed, OrderCount, CashbackAmount, PreferedOrderCat) may leak information about churn.
- Different spellings of similar categories (e.g., "Mobile Phone" vs "Phone", "COD" vs "Cash on Delivery") have different churn rates and may cause leakage.
- The contract must pass validation before the model is used on new data.

---

## Risks and Limitations

- **Undefined Churn Window:** The lack of a defined churn window means some "last month" features may leak future information, potentially inflating performance metrics.
- **Category Spelling Variations:** Different spellings of similar categories with varying churn rates may introduce bias or leakage.
- **Duplicates:** The presence of many duplicate or near-duplicate rows requires careful handling to avoid leakage; the data split ensures no duplicate groups cross train/test boundaries.
- **Model Use:** The model is designed for ranking customers by churn risk and should not be used for automated decisions on individual customers without human oversight.
- **Contract Compliance:** The model should only be applied to data that passes the contract validation to ensure assumptions and data quality are met.

---

This model card summarizes the key details, assumptions, and limitations to guide Harbor & Vale's retention team in responsibly using the churn risk model for customer retention efforts.