# Exploratory Data Analysis Insights for Harbor & Vale Retention Team

## Executive Summary
- Customers with very short tenure (0-1 months) have the highest churn rate at 51.84%, indicating new customers are most at risk.
- Preferred payment modes "COD" (Cash on Delivery) and "Cash on Delivery" have notably different churn rates of 28.77% and 15.44% respectively, despite similar naming.
- Customers who have complained show a much higher churn rate (31.67%) compared to those who have not (10.93%).
- Missing values in key columns such as Tenure and HourSpendOnApp correspond to higher churn rates than when values are present.
- Mobile-related order categories ("Mobile" and "Mobile Phone") have the highest churn rates (~27%), suggesting these customers are more likely to churn.
- The overall churn rate is 16.84%, with significant variation across customer groups.

---

## Who Churns?

### By Tenure (months, binned)
- 0-1 months: 1198 customers, churn rate 51.84%
- 2-5 months: 769 customers, churn rate 8.84%
- 6-10 months: 1127 customers, churn rate 5.86%
- 11-20 months: 1519 customers, churn rate 6.71%
- 21+ months: 753 customers, churn rate 1.33%
- Missing Tenure: 264 customers, churn rate 30.68%

### By Preferred Payment Mode
- COD: 365 customers, churn rate 28.77%
- Cash on Delivery: 149 customers, churn rate 15.44%
- E wallet: 614 customers, churn rate 22.80%
- CC: 273 customers, churn rate 21.61%
- Debit Card: 2314 customers, churn rate 15.38%
- Credit Card: 1501 customers, churn rate 12.86%
- UPI: 414 customers, churn rate 17.39%

### By Preferred Login Device
- Phone: 1231 customers, churn rate 22.42%
- Computer: 1634 customers, churn rate 19.83%
- Mobile Phone: 2765 customers, churn rate 12.59%

### By Prefered Order Category
- Mobile Phone: 1271 customers, churn rate 27.54%
- Mobile: 809 customers, churn rate 27.19%
- Fashion: 826 customers, churn rate 15.50%
- Laptop & Accessory: 2050 customers, churn rate 10.24%
- Grocery: 410 customers, churn rate 4.88%
- Others: 264 customers, churn rate 7.58%

### By Marital Status
- Single: 1796 customers, churn rate 26.73%
- Divorced: 848 customers, churn rate 14.62%
- Married: 2986 customers, churn rate 11.52%

### By Gender
- Male: 3384 customers, churn rate 17.73%
- Female: 2246 customers, churn rate 15.49%

### By Satisfaction Score
- Score 5: 1108 customers, churn rate 23.83%
- Score 4: 1074 customers, churn rate 17.13%
- Score 3: 1698 customers, churn rate 17.20%
- Score 2: 586 customers, churn rate 12.63%
- Score 1: 1164 customers, churn rate 11.51%

### By Complaint Status
- Complained (1): 1604 customers, churn rate 31.67%
- No Complaint (0): 4026 customers, churn rate 10.93%

### Missing Values with Different Churn Rates
- Tenure missing: 264 customers, churn rate 30.68% vs present 16.16%
- WarehouseToHome missing: 251 customers, churn rate 33.47% vs present 16.06%
- HourSpendOnApp missing: 255 customers, churn rate 22.75% vs present 16.56%
- OrderAmountHikeFromlastYear missing: 265 customers, churn rate 5.28% vs present 17.41%
- CouponUsed missing: 256 customers, churn rate 3.12% vs present 17.49%
- OrderCount missing: 258 customers, churn rate 6.98% vs present 17.31%
- DaySinceLastOrder missing: 307 customers, churn rate 17.59% vs present 16.80%

---

## Budget Implications

- The highest churn rates are among new customers (0-1 month tenure) and those with missing tenure data, suggesting retention efforts and discounts should prioritize onboarding and early engagement.
- Customers using "COD" payment mode have a high churn rate (28.77%) compared to "Cash on Delivery" (15.44%), so these groups should be treated distinctly in retention strategies and discount allocation.
- Customers who have complained have a churn rate nearly three times higher than those who have not (31.67% vs 10.93%), indicating that resolving complaints effectively could reduce churn.
- Mobile-related order categories ("Mobile" and "Mobile Phone") have churn rates around 27%, higher than other categories, suggesting targeted retention campaigns or discounts for these customers.
- Missing values in key behavioral metrics (e.g., WarehouseToHome, HourSpendOnApp) correspond to higher churn rates, so efforts to improve data completeness or target these customers may be beneficial.
- Lower churn rates in categories like Grocery (4.88%) and Married customers (11.52%) suggest these groups are more stable and may require less discount budget focus.

---

## Data Caveats

- The churn window is undefined, so columns describing last-month behavior may include data from after customers churned, which could affect interpretation.
- Similar category spellings such as "COD" and "Cash on Delivery" are kept separate because their churn rates differ significantly (28.77% vs 15.44%). No assumption is made about the cause of this difference.
- SatisfactionScore and other score columns have no documented direction; scores are reported as "score X" without implying better or worse satisfaction.
- Missing values are preserved as in the original data; their differing churn rates may reflect data collection patterns rather than customer behavior.
- Outliers in numeric columns were retained without modification and may influence some statistics.

---

The detailed EDA report with charts and statistics is available at:  
/home/user/FINALPROJECTZIV/artifacts/latest/crew1/eda_report.html