# Exploratory Data Analysis Insights for Harbor & Vale Retention Team

---

## Executive Summary
- Customers using "Phone" as PreferredLoginDevice churn at 22.42%, higher than "Mobile Phone" (12.59%) and "Computer" (19.83%).
- PreferredPaymentMode groups "COD" (28.77%) and "E wallet" (22.80%) have the highest churn rates, while "Cash on Delivery" (15.44%) and "Credit Card" (12.86%) have notably lower churn rates despite similar meanings.
- Customers preferring "Mobile" (27.19%) and "Mobile Phone" (27.54%) order categories churn significantly more than other categories like "Grocery" (4.88%) or "Laptop & Accessory" (10.24%).
- Single customers churn at 26.73%, more than double the churn rate of married customers (11.52%).
- Missing values in key columns such as Tenure and WarehouseToHome correspond to much higher churn rates (e.g., Tenure missing churn rate 30.68% vs present 16.16%).
- There are 1,112 rows that are exact copies of another row except for their CustomerID, and 3,472 rows forming 1,736 groups of at most 2 rows with one value changed, each with its own CustomerID. Every copy is counted as a separate customer in group sizes and churn rates.
- The churn window is undefined, so last-month columns may describe customers after they churned.
- SatisfactionScore values show increasing churn rates from score 1 (11.51%) to score 5 (23.83%), but the direction of the score is unknown.

---

## Who Churns?

### By Device
- Phone users: 1,231 customers, churn rate 22.42%
- Computer users: 1,634 customers, churn rate 19.83%
- Mobile Phone users: 2,765 customers, churn rate 12.59%

### By Payment Mode
- COD (Cash on Delivery abbreviation): 365 customers, churn rate 28.77%
- E wallet: 614 customers, churn rate 22.80%
- CC (Credit Card abbreviation): 273 customers, churn rate 21.61%
- Cash on Delivery (full spelling): 149 customers, churn rate 15.44%
- Credit Card (full spelling): 1,501 customers, churn rate 12.86%
- Debit Card: 2,314 customers, churn rate 15.38%
- UPI: 414 customers, churn rate 17.39%

Note: "COD" and "Cash on Delivery" are kept as separate categories because their churn rates differ substantially (28.77% vs 15.44%). Similarly, "CC" and "Credit Card" differ (21.61% vs 12.86%).

### By Order Category
- Mobile: 809 customers, churn rate 27.19%
- Mobile Phone: 1,271 customers, churn rate 27.54%
- Fashion: 826 customers, churn rate 15.50%
- Grocery: 410 customers, churn rate 4.88%
- Laptop & Accessory: 2,050 customers, churn rate 10.24%
- Others: 264 customers, churn rate 7.58%

Note: "Mobile" and "Mobile Phone" categories are separate with close churn rates (27.19% vs 27.54%).

### By Marital Status
- Single: 1,796 customers, churn rate 26.73%
- Divorced: 848 customers, churn rate 14.62%
- Married: 2,986 customers, churn rate 11.52%

### By Missing Values
- Tenure missing: 264 customers, churn rate 30.68% vs present 16.16%
- WarehouseToHome missing: 251 customers, churn rate 33.47% vs present 16.06%
- HourSpendOnApp missing: 255 customers, churn rate 22.75% vs present 16.56%
- CouponUsed missing: 256 customers, churn rate 3.12% vs present 17.49%
- OrderCount missing: 258 customers, churn rate 6.98% vs present 17.31%
- DaySinceLastOrder missing: 307 customers, churn rate 17.59% vs present 16.80%

### By SatisfactionScore
- Score 1: 1,164 customers, churn rate 11.51%
- Score 2: 586 customers, churn rate 12.63%
- Score 3: 1,698 customers, churn rate 17.20%
- Score 4: 1,074 customers, churn rate 17.13%
- Score 5: 1,108 customers, churn rate 23.83%

### Duplicates Ignoring CustomerID
"1,112 rows are exact copies of another row except for their id (556 of them repeat an earlier row under a new id). Counting copies with one value changed as well, 3,472 rows form 1,736 groups of at most 2 rows, each row with its own id."

Every copy is counted as a separate customer in the group sizes and churn rates above.

---

## Budget Implications

- Focus discount budget on customers using "Phone" devices and those preferring "COD" and "E wallet" payment modes, as these groups have the highest churn rates.
- Target customers ordering in the "Mobile" and "Mobile Phone" categories, which show churn rates above 27%.
- Single customers represent a high churn risk group and may benefit from retention incentives.
- Missing data in Tenure and WarehouseToHome is associated with higher churn; consider outreach or data quality improvement efforts here.
- Since "COD" and "Cash on Delivery" have different churn rates, treat these as distinct segments for targeted offers.
- Similarly, "CC" and "Credit Card" should be treated separately in retention strategies.
- SatisfactionScore groups with score 5 have the highest churn rate; further investigation is needed before allocating budget based on satisfaction scores due to unknown score direction.

---

## Data Caveats

- The churn window is undefined, so last-month columns may describe customers after they churned.
- The dataset contains 1,112 rows that are exact copies except for CustomerID, and 3,472 rows forming 1,736 groups with minor differences, each counted as separate customers. This may inflate group sizes and churn rates.
- Missing values in key columns have churn rates that differ from present values, which may reflect data collection issues or customer behavior differences.
- Similar category spellings (e.g., "COD" vs "Cash on Delivery") are kept separate because their churn rates differ; no assumption is made about data entry errors or behavioral similarity.
- SatisfactionScore and other score columns have no documented direction; scores are reported as-is without labeling them as "best" or "worst."

---

The full EDA report with charts and detailed statistics is available at:  
/home/user/FINALPROJECTZIV/artifacts/latest/crew1/eda_report.html