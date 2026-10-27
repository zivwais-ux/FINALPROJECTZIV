# Quality Summary Report for E Comm Dataset

## Overview
- Total rows: 5630
- Total columns: 20
- Duplicate rows: 0
- CustomerID uniqueness: Unique (no duplicates)
- Rows with any missing values: 1856 (max 1 missing value per row)

## Missing Values
| Column                  | Missing Count | Missing Share | Churn Rate When Missing | Churn Rate When Present |
|-------------------------|---------------|---------------|-------------------------|-------------------------|
| Tenure                  | 264           | 4.69%         | 30.68%                  | 16.16%                  |
| WarehouseToHome         | 251           | 4.46%         | 33.47%                  | 16.06%                  |
| HourSpendOnApp          | 255           | 4.53%         | 22.75%                  | 16.56%                  |
| OrderAmountHikeFromlastYear | 265       | 4.71%         | 5.28%                   | 17.41%                  |
| CouponUsed              | 256           | 4.55%         | 3.12%                   | 17.49%                  |
| OrderCount              | 258           | 4.58%         | 6.98%                   | 17.31%                  |
| DaySinceLastOrder       | 307           | 5.45%         | 17.59%                  | 16.80%                  |

## Categories

### PreferredLoginDevice
| Value         | Count | Churn Rate |
|---------------|-------|------------|
| Computer      | 1634  | 19.83%     |
| Mobile Phone  | 2765  | 12.59%     |
| Phone         | 1231  | 22.42%     |

Note: "Mobile Phone" and "Phone" are kept separate because their churn rates differ by 9.83 percentage points.

### PreferredPaymentMode
| Value           | Count | Churn Rate |
|-----------------|-------|------------|
| CC              | 273   | 21.61%     |
| COD             | 365   | 28.77%     |
| Cash on Delivery | 149  | 15.44%     |
| Credit Card     | 1501  | 12.86%     |
| Debit Card      | 2314  | 15.38%     |
| E wallet        | 614   | 22.80%     |
| UPI             | 414   | 17.39%     |

Note: "COD" and "Cash on Delivery" are separate categories with churn rates differing by 13.33 percentage points.

### Gender
| Value  | Count | Churn Rate |
|--------|-------|------------|
| Female | 2246  | 15.49%     |
| Male   | 3384  | 17.73%     |

### PreferedOrderCat
| Value               | Count | Churn Rate |
|---------------------|-------|------------|
| Fashion             | 826   | 15.50%     |
| Grocery             | 410   | 4.88%      |
| Laptop & Accessory  | 2050  | 10.24%     |
| Mobile              | 809   | 27.19%     |
| Mobile Phone        | 1271  | 27.54%     |
| Others              | 264   | 7.58%      |

Note: "Mobile" and "Mobile Phone" are separate categories with churn rates differing by 0.35 percentage points.

### MaritalStatus
| Value    | Count | Churn Rate |
|----------|-------|------------|
| Divorced | 848   | 14.62%     |
| Married  | 2986  | 11.52%     |
| Single   | 1796  | 26.73%     |

## Outliers
| Column               | Outlier Count | Outlier Values                      | Median Value |
|----------------------|---------------|-----------------------------------|--------------|
| Tenure               | 2             | 60.0, 61.0                        | 9.0          |
| WarehouseToHome      | 2             | 126.0, 127.0                      | 14.0         |
| NumberOfAddress       | 4             | 19.0, 20.0, 21.0, 22.0           | 3.0          |
| CouponUsed            | 303           | 6.0 to 16.0 (various values)     | 1.0          |
| OrderCount            | 263           | 10.0 to 16.0 (various values)    | 2.0          |
| DaySinceLastOrder     | 3             | 30.0, 31.0, 46.0                 | 3.0          |

## Target (Churn)
- Total positive churn cases: 948
- Overall churn rate: 16.84%