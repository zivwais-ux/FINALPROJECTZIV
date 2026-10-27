# Model Card for Harbor & Vale Retention Team

---

## Model Details

- **Selected Model:** HistGradientBoosting
- **Decision Threshold:** 0.5
- **Model File Location:** `/home/user/FINALPROJECTZIV/artifacts/latest/crew2/model.joblib`
- **Selection Criterion:** Highest mean PR-AUC over 5-fold stratified group cross-validation on the training split

---

## Intended Use

This model is designed to rank customers by their risk of churn to enable targeted retention discounts. It supports prioritizing outreach efforts to customers most likely to churn.

**Out of Scope:**  
The model should **not** be used to make decisions about individual customers without human review. It is intended for aggregate ranking and prioritization only.

---

## Training Data

- **Source File:** `clean_data.csv`
- **SHA256 Checksum:** `e0c951d4a9a94a650ff514da4c0152b473b1ab026aeddf0662ced46e5f847019`
- **Number of Rows:** 5,630
- **Churn Rate:** 16.84%
- **Contract Version:** 1.0.0

### Duplicate Rows

> "1,112 rows are exact copies of another row except for their id (556 of them repeat an earlier row under a new id). Counting copies with one value changed as well, 3,472 rows form 1,736 groups of at most 2 rows, each row with its own id."

The train/test split uses a StratifiedGroupKFold (5 folds) method stratified on churn and grouped by duplicate groups to ensure no duplicate groups appear in both train and test sets, preventing leakage.

---

## Features

- **Number of Features:** 34 (excluding forbidden columns)
- **Encoding:**  
  - Numerical features kept unchanged  
  - Categorical features encoded as one-hot vectors  
- **Missing Values:** 1,856 missing values are preserved as-is (no imputation performed)
- **Forbidden Columns:**  
  - `CustomerID` (excluded to prevent data leakage)

### Feature Examples and Units (assumed where noted)

| Feature                | Encoding      | Missing Values Kept | Unit (Assumed)           |
|------------------------|---------------|---------------------|-------------------------|
| Tenure                 | Unchanged     | 264                 | months (assumed)        |
| PreferredLoginDevice    | One-hot       | 0                   | -                       |
| WarehouseToHome        | Unchanged     | 251                 | km (assumed)            |
| CashbackAmount         | Unchanged     | 0                   | INR (last month average) (assumed) |
| Complain               | Unchanged     | 0                   | flag (last month)       |

---

## Metrics

| Metric           | Value   | Threshold | Pass/Fail |
|------------------|---------|-----------|-----------|
| Test PR-AUC      | 0.8636  | ≥ 0.8     | Pass      |
| Test Recall      | 0.6667  | ≥ 0.6     | Pass      |
| Test Precision   | 0.9     | N/A       | N/A       |
| Test ROC-AUC     | 0.9497  | N/A       | N/A       |
| Baseline PR-AUC  | 0.1679  | N/A       | N/A       |

The model exceeds quality thresholds for PR-AUC and Recall, with a PR-AUC substantially higher than the baseline churn rate.

---

## Assumptions

- Missing values are preserved as in the raw dataset; no imputation was performed.
- Categorical values are kept exactly as in the raw data without merging or renaming.
- Outliers are retained without clipping or removal.
- Duplicate rows, including exact duplicates and near-duplicates under different CustomerIDs, are kept.
- Units are assumed as follows:  
  - Tenure in months  
  - WarehouseToHome in kilometers  
  - CashbackAmount in Indian Rupees (INR)
- The churn window is undefined; features labeled as "last month" (e.g., Complain, CouponUsed, OrderCount, CashbackAmount, PreferedOrderCat) may leak information about churn.
- Different spellings of similar categories with significantly different churn rates are kept separate.

---

## Risks and Limitations

- **Undefined Churn Window:** The lack of a defined churn window means some "last month" features may leak future information, potentially inflating performance metrics.
- **Category Spellings:** Variations in category spellings with different churn rates are not merged, which may cause leakage or bias.
- **Duplicates:** Duplicate rows and near-duplicates exist in the dataset. Leakage is prevented only if all rows in each duplicate group are kept entirely on one side of the train/test split.
- **Contract Compliance:** The model must only be used on new data that passes the same contract validation to ensure data consistency and prevent leakage.
- **Individual Decisions:** The model is not intended for automated decisions on individual customers without human oversight.

---

This model card provides a comprehensive overview for the Harbor & Vale retention team to understand the model's capabilities, data provenance, and limitations before deployment.