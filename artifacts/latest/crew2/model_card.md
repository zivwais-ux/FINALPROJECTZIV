# Model Card for Harbor & Vale Retention Team

---

## Model details

- **Selected model:** HistGradientBoosting
- **Decision threshold:** 0.5
- **Model file location:** /home/user/FINALPROJECTZIV/artifacts/latest/crew2/model.joblib
- **Selection criteria:** Highest mean PR-AUC over 5-fold stratified group cross-validation on the training split

---

## Intended use

This model is designed to rank customers by their risk of churn to enable targeted retention discounts and campaigns. It supports prioritizing outreach efforts to customers most likely to churn.

**Out of scope:**  
- Making decisions about an individual customer without human review.  
- Automated actions without human oversight are not recommended due to model limitations and data assumptions.

---

## Training data

- **Source file:** clean_data.csv  
- **SHA256 checksum:** e0c951d4a9a94a650ff514da4c0152b473b1ab026aeddf0662ced46e5f847019  
- **Number of rows:** 5,630  
- **Churn rate:** 16.84% (expected)  
- **Contract version:** 1.0.0  

**Duplicates summary:**  
"1,112 rows are exact copies of another row except for their id (556 of them repeat an earlier row under a new id). Counting copies with one value changed as well, 3,472 rows form 1,736 groups of at most 2 rows, each row with its own id."

**Train/test split handling of duplicates:**  
The data split used StratifiedGroupKFold with grouping by duplicate groups to ensure no duplicate groups appear in both train and test sets, preventing leakage.

---

## Features

- **Number of features:** 34  
- **Encoding:**  
  - Numerical features mostly unchanged  
  - Categorical features encoded via one-hot encoding (e.g., PreferredLoginDevice, PreferredPaymentMode, Gender, PreferedOrderCat, MaritalStatus)  
- **Missing values:** 1,856 missing values were kept as-is without imputation  
- **Forbidden columns:** CustomerID (excluded to prevent leakage and privacy issues)  

---

## Metrics

| Metric           | Value   | Baseline | Quality Threshold | Pass/Fail |
|------------------|---------|----------|-------------------|-----------|
| Test PR-AUC      | 0.8636  | 0.1679   | ≥ 0.8             | Pass      |
| Test Recall      | 0.6667  | -        | ≥ 0.6             | Pass      |
| Test Precision   | 0.9     | -        | -                 | -         |
| Test ROC-AUC     | 0.9497  | -        | -                 | -         |

**Baseline PR-AUC** corresponds to the churn rate (0.1679), showing the model substantially outperforms random guessing.

**Confusion matrix at threshold 0.5:**  
- True Positives (churners caught): 126  
- False Negatives (churners missed): 63  
- False Positives (loyal customers flagged): 14  
- True Negatives (loyal customers correctly identified): 923  

---

## Assumptions

- Units are assumed as follows:  
  - Tenure in months  
  - WarehouseToHome in kilometers  
  - CashbackAmount in Indian Rupees (INR, last month average)  
- No imputation was performed on missing values; missing data is preserved as-is.  
- No merging or renaming of categorical values; categories are kept exactly as in the raw data.  
- Outliers are retained without clipping or removal.  
- Duplicate rows are kept, including those repeated under a new CustomerID either exactly or with one value changed.  
- The churn window is undefined, so features labeled as "last month" (e.g., Complain, CouponUsed, OrderCount, CashbackAmount, PreferedOrderCat) may leak information about churn.  
- Different spellings of similar categories with different churn rates (e.g., "Mobile Phone" vs "Phone", "COD" vs "Cash on Delivery") are kept separate and may cause leakage.  
- The train/test split ensures no duplicate groups appear on both sides to prevent leakage.

---

## Risks and limitations

- **Undefined churn window:** Features referencing "last month" may leak future information, potentially inflating performance metrics. Use caution interpreting predictions.  
- **Category spelling variations:** Different spellings of similar categories with different churn rates may introduce bias or leakage.  
- **Duplicates:** Presence of many duplicate and near-duplicate rows requires careful data splitting to avoid leakage; this is handled in training but must be maintained for future data.  
- **Contract compliance:** The contract must pass validation before applying the model to new data to ensure data consistency and model validity.  
- **No causation implied:** Feature importance indicates model reliance but does not imply causal relationships.  

---

This model card provides a comprehensive overview for Harbor & Vale's retention team to understand the model's capabilities, data, and limitations before deployment and use.