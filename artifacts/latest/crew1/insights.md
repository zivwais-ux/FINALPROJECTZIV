# Exploratory Data Analysis Insights for Harbor & Vale Retention Team

---

## Executive Summary
- Customers using "Phone" as PreferredLoginDevice have the highest churn rate (22.42%) among device groups, with 1,231 customers.
- The "COD" (Cash on Delivery) payment mode group has a notably high churn rate of 28.77% compared to "Cash on Delivery" at 15.44%, despite similar naming.
- Customers preferring "Mobile" and "Mobile Phone" order categories both show very high churn rates (~27%), much higher than other categories like Grocery (4.88%) or Laptop & Accessory (10.24%).
- Missing values in key columns such as Tenure and WarehouseToHome correspond to substantially higher churn rates (e.g., Tenure missing churn rate 30.68% vs present 16.16%).
- There are 1,112 rows that are exact copies of another row except for their CustomerID (556 repeat an earlier row under a new id). Counting copies with one value changed as well, 3,472 rows form 1,736 groups of at most 2 rows, each row with its own id. Every copy is counted as a separate customer in the group sizes and churn rates reported.

---

## Who Churns?

### By PreferredLoginDevice
- Phone: 1,231 customers, churn rate 22.42%
- Computer: 1,634 customers, churn rate 19.83%
- Mobile Phone: 2,765 customers, churn rate 12.59%  
(Note: "Mobile Phone" and "Phone" are kept separate because their churn rates differ by 9.83 percentage points.)

### By PreferredPaymentMode
- COD: 365 customers, churn rate 28.77%
- E wallet: 614 customers, churn rate 22.80%
- CC: 273 customers, churn rate 21.61%
- Cash on Delivery: 149 customers, churn rate 15.44%
- Debit Card: 2,314 customers, churn rate 15.38%
- Credit Card: 1,501 customers, churn rate 12.86%
- UPI: 414 customers, churn rate 17.39%  
(Note: "COD" and "Cash on Delivery" are kept separate because their churn rates differ by 13.33 percentage points.)

### By PreferedOrderCat
- Mobile Phone: 1,271 customers, churn rate 27.54%
- Mobile: 809 customers, churn rate 27.19%
- Laptop & Accessory: 2,050 customers, churn rate 10.24%
- Grocery: 410 customers, churn rate 4.88%
- Fashion: 826 customers, churn rate 15.50%
- Others: 264 customers, churn rate 7.58%  
(Note: "Mobile" and "Mobile Phone" are kept separate because their churn rates differ by 0.35 percentage points.)

### By Gender
- Male: 3,384 customers, churn rate 17.73%
- Female: 2,246 customers, churn rate 15.49%

### By MaritalStatus
- Single: 1,796 customers, churn rate 26.73%
- Divorced: 848 customers, churn rate 14.62%
- Married: 2,986 customers, churn rate 11.52%

### Missing Values with Different Churn Rates
- Tenure missing (264 customers): churn rate 30.68% vs present 16.16%
- WarehouseToHome missing (251 customers): churn rate 33.47% vs present 16.06%
- HourSpendOnApp missing (255 customers): churn rate 22.75% vs present 16.56%
- OrderAmountHikeFromlastYear missing (265 customers): churn rate 5.28% vs present 17.41%
- CouponUsed missing (256 customers): churn rate 3.12% vs present 17.49%
- OrderCount missing (258 customers): churn rate 6.98% vs present 17.31%
- DaySinceLastOrder missing (307 customers): churn rate 17.59% vs present 16.80%

### Duplicate Rows
- "1,112 rows are exact copies of another row except for their id (556 of them repeat an earlier row under a new id). Counting copies with one value changed as well, 3,472 rows form 1,736 groups of at most 2 rows, each row with its own id."
- Every copy is counted as a separate customer in the group sizes and churn rates above.

---

## Budget Implications

- Focus discount budget on customers using "Phone" as login device and those paying with "COD" payment mode, as these groups have the highest churn rates.
- The "Mobile" and "Mobile Phone" order categories also show very high churn and could be targeted for retention incentives.
- Single customers have a high churn rate (26.73%) and may benefit from targeted retention efforts.
- Missing data groups with high churn rates (e.g., missing Tenure or WarehouseToHome) might indicate customers with incomplete profiles who are at risk; consider outreach or data enrichment.
- Groups with similar category names but different churn rates (e.g., COD vs Cash on Delivery) should be treated separately in budget allocation due to their differing churn behaviors.

---

## Data Caveats

- The churn window is undefined, so last-month columns may describe customers after they churned.
- SatisfactionScore and other score columns have no documented direction; scores are reported as "score 1" through "score 5" without implying better or worse.
- Category spellings that look similar but differ in churn rates are kept separate; no assumptions are made about data entry errors or behavioral similarity.
- Duplicate rows with different CustomerIDs inflate group sizes and churn counts; each row is treated as a separate customer.
- Outliers and missing values were preserved as in the original data without imputation or removal.

---

For detailed statistics and charts, please refer to the full EDA report:  
[/home/user/FINALPROJECTZIV/artifacts/latest/crew1/eda_report.html]