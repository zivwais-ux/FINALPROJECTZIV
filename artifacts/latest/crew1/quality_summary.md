# Quality Summary Report for E Comm Dataset

## Overview
- Total rows: 5630
- Total columns: 20
- Duplicate rows: 0 (This holds because every row has its own unique CustomerID)
- CustomerID uniqueness: True (CustomerID is unique)
- Duplicates ignoring CustomerID:  
  "1,112 rows are exact copies of another row except for their id (556 of them repeat an earlier row under a new id). Counting copies with one value changed as well, 3,472 rows form 1,736 groups of at most 2 rows, each row with its own id."
- Churn rate in duplicate groups: 0.1947

## Missing Values
| Column                | Missing Count | Missing Share | Churn Rate When Missing | Churn Rate When Present |
|-----------------------|---------------|---------------|-------------------------|-------------------------|
| Tenure                | 264           | 4.69%         | 30.68%                  | 16.16%                  |
| WarehouseToHome       | 251           | 4.46%         | 33.47%                  | 16.06%                  |
| HourSpendOnApp        | 255           | 4.53%         | 22.75%                  | 16.56%                  |
| OrderAmountHikeFromlastYear | 265     | 4.71%         | 5.28%                   | 17.41%                  |
| CouponUsed            | 256           | 4.55%         | 3.12%                   | 17.49%                  |
| OrderCount            | 258           | 4.58%         | 6.98%                   | 17.31%                  |
| DaySinceLastOrder     | 307           | 5.45%         | 17.59%                  | 16.80%                  |

## Categories

### PreferredLoginDevice
- Computer: Count 1634, Churn Rate 19.83%
- Mobile Phone: Count 2765, Churn Rate 12.59%
- Phone: Count 1231, Churn Rate 22.42%  
(Note: "Mobile Phone" and "Phone" appear similar but have different churn rates.)

### PreferredPaymentMode
- CC: Count 273, Churn Rate 21.61%
- COD: Count 365, Churn Rate 28.77%
- Cash on Delivery: Count 149, Churn Rate 15.44%  
(Note: "COD" and "Cash on Delivery" appear similar but have different churn rates.)
- Credit Card: Count 1501, Churn Rate 12.86%
- Debit Card: Count 2314, Churn Rate 15.38%
- E wallet: Count 614, Churn Rate 22.80%
- UPI: Count 414, Churn Rate 17.39%

### Gender
- Female: Count 2246, Churn Rate 15.49%
- Male: Count 3384, Churn Rate 17.73%

### PreferedOrderCat
- Fashion: Count 826, Churn Rate 15.50%
- Grocery: Count 410, Churn Rate 4.88%
- Laptop & Accessory: Count 2050, Churn Rate 10.24%
- Mobile: Count 809, Churn Rate 27.19%
- Mobile Phone: Count 1271, Churn Rate 27.54%  
(Note: "Mobile" and "Mobile Phone" appear similar but have different churn rates.)
- Others: Count 264, Churn Rate 7.58%

### MaritalStatus
- Divorced: Count 848, Churn Rate 14.62%
- Married: Count 2986, Churn Rate 11.52%
- Single: Count 1796, Churn Rate 26.73%

## Outliers
- Tenure: 2 outliers (values 60.0, 61.0) outside [-40.0, 58.0], median 9.0
- WarehouseToHome: 2 outliers (values 126.0, 127.0) outside [-24.0, 53.0], median 14.0
- NumberOfAddress: 4 outliers (values 19.0, 20.0, 21.0, 22.0) outside [-10.0, 18.0], median 3.0
- CouponUsed: 303 outliers (values 6.0 to 16.0) outside [-2.0, 5.0], median 1.0
- OrderCount: 263 outliers (values 10.0 to 16.0) outside [-5.0, 9.0], median 2.0
- DaySinceLastOrder: 3 outliers (values 30.0, 31.0, 46.0) outside [-13.0, 22.0], median 3.0

## Target (Churn)
- Total positives (churned): 948
- Overall churn rate: 16.84%