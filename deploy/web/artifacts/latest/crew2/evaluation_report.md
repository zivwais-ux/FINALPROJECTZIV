# Evaluation Report

## Split
- Method: StratifiedGroupKFold(5), first fold is the test set
- Stratified on: Churn
- Grouped by: duplicate_group
- Random state: 42
- Train rows: 4504
- Test rows: 1126
- Test share: 0.2 (20%)
- Train churn rate: 16.85%
- Test churn rate: 16.79%
- Duplicate groups on both sides: 0 (no leakage)

## Candidates

| Model                 | CV PR-AUC Mean | CV PR-AUC Std | Test PR-AUC | Test Recall | Test Precision | Test ROC-AUC |
|-----------------------|----------------|---------------|-------------|-------------|----------------|--------------|
| HistGradientBoosting   | 0.8167         | 0.0364        | 0.8636      | 0.6667      | 0.9            | 0.9497       |
| RandomForest          | 0.8132         | 0.0335        | 0.8447      | 0.5185      | 0.9159         | 0.9411       |

## Selected Model
- Model: HistGradientBoosting
- Selection rule: Highest mean PR-AUC over 5-fold stratified group cross-validation on the training split

### Confusion Matrix at decision threshold 0.5 (in understandable terms):
- Churners caught (True Positives): 126
- Churners missed (False Negatives): 63
- Loyal customers flagged by mistake (False Positives): 14
- Loyal customers correctly identified (True Negatives): 923

## Quality Thresholds
- Thresholds: PR-AUC ≥ 0.8, Recall ≥ 0.6
- Selected model test PR-AUC: 0.8636 (meets threshold)
- Selected model test Recall: 0.6667 (meets threshold)
- Baseline PR-AUC (test churn rate): 0.1679
- The model's PR-AUC is substantially higher than the baseline, indicating strong predictive performance.

## Feature Importance (by permutation importance, described as model reliance)
The model relies most on these features for its predictions:
1. Tenure (largest impact on PR-AUC when permuted)
2. Complain
3. NumberOfAddress
4. SatisfactionScore
5. WarehouseToHome
6. CityTier
7. PreferedOrderCat = Laptop & Accessory
8. DaySinceLastOrder
9. PreferredLoginDevice = Computer
10. MaritalStatus = Single

These features are critical for the model's ability to distinguish churners from non-churners, though this does not imply causation.