# Exploratory Data Analysis Insights for Harbor & Vale Retention Team

---

## Executive Summary
- Customers using "Phone" as PreferredLoginDevice churn at 22.42%, higher than "Mobile Phone" users at 12.59%, despite similar naming.
- "COD" (Cash on Delivery) payment mode customers churn at 28.77%, notably higher than "Cash on Delivery" spelled out at 15.44%.
- Single customers have a high churn rate of 26.73%, compared to Married customers at 11.52%.
- Customers with missing values in key columns like Tenure and WarehouseToHome have significantly higher churn rates than those with present values.
- There are 1,112 rows that are exact copies of another row except for their CustomerID, and 3,472 rows forming 1,736 groups with minor differences; each copy is counted as a separate customer in group sizes and churn rates.
- The churn window is undefined, so last-month columns may describe customers after they churned.

---

## Who Churns?

### By Device
- **Phone** users: 1,231 customers, churn rate 22.42%
- **Mobile Phone** users: 2,765 customers, churn rate 12.59%
- **Computer** users: 1,634 customers, churn rate 19.83%

### By Payment Mode
- **COD**: 365 customers, churn rate 28.77%
- **Cash on Delivery**: 149 customers, churn rate 15.44%
- **E wallet**: 614 customers, churn rate 22.80%
- **Credit Card**: 1,501 customers, churn rate 12.86%
- **Debit Card**: 2,314 customers, churn rate 15.38%
- **CC**: 273 customers, churn rate 21.61%
- **UPI**: 414 customers, churn rate 17.39%

### By Marital Status
- **Single**: 1,796 customers, churn rate 26.73%
- **Married**: 2,986 customers, churn rate 11.52%
- **Divorced**: 848 customers, churn rate 14.62%

### By Preferred Order Category
- **Mobile Phone**: 1,271 customers, churn rate 27.54%
- **Mobile**: 809 customers, churn rate 27.19%
- **Laptop & Accessory**: 2,050 customers, churn rate 10.24%
- **Fashion**: 826 customers, churn rate 15.50%
- **Grocery**: 410 customers, churn rate 4.88%
- **Others**: 264 customers, churn rate 7.58%

### By Gender
- **Male**: 3,384 customers, churn rate 17.73%
- **Female**: 2,246 customers, churn rate 15.49%

### By SatisfactionScore (score values, no direction implied)
- Score 5: 1,108 customers, churn rate 23.83%
- Score 4: 1,074 customers, churn rate 17.13%
- Score 3: 1,698 customers, churn rate 17.20%
- Score 2: 586 customers, churn rate 12.63%
- Score 1: 1,164 customers, churn rate 11.51%

### Missing Values with Different Churn Rates
- **Tenure missing**: 264 customers, churn rate 30.68% vs present 16.16%
- **WarehouseToHome missing**: 251 customers, churn rate 33.47% vs present 16.06%
- **HourSpendOnApp missing**: 255 customers, churn rate 22.75% vs present 16.56%
- **OrderAmountHikeFromlastYear missing**: 265 customers, churn rate 5.28% vs present 17.41%
- **CouponUsed missing**: 256 customers, churn rate 3.12% vs present 17.49%
- **OrderCount missing**: 258 customers, churn rate 6.98% vs present 17.31%
- **DaySinceLastOrder missing**: 307 customers, churn rate 17.59% vs present 16.80%

### Duplicates Ignoring CustomerID
"1,112 rows are exact copies of another row except for their id (556 of them repeat an earlier row under a new id). Counting copies with one value changed as well, 3,472 rows form 1,736 groups of at most 2 rows, each row with its own id."

Every copy is counted as a separate customer in the group sizes and churn rates above.

---

## Budget Implications

- Focus discount budget on high churn groups with substantial size:
  - Customers using **COD** payment mode (365 customers, 28.77% churn) and **E wallet** users (614 customers, 22.80% churn).
  - Customers with **Phone** as PreferredLoginDevice (1,231 customers, 22.42% churn).
  - **Single** customers (1,796 customers, 26.73% churn).
  - Customers ordering in **Mobile Phone** and **Mobile** categories (1,271 and 809 customers respectively, both ~27% churn).
- Consider that some groups with missing data have very high churn rates (e.g., missing Tenure and WarehouseToHome), which may indicate a need for targeted engagement or data quality improvement.
- Groups with similar spellings but different churn rates (e.g., COD vs Cash on Delivery, Mobile Phone vs Phone) should be treated separately in budget allocation due to their differing churn behaviors.

---

## Data Caveats

- The churn window is undefined; last-month columns may describe customers after they churned.
- SatisfactionScore and other scores have no documented direction; scores are reported as values only.
- Similar category spellings are kept separate because their churn rates differ; no assumptions are made about data entry errors or behavioral similarity.
- Missing values in several columns have churn rates that differ substantially from present values; this may reflect data collection patterns rather than customer behavior.
- Duplicate rows with different CustomerIDs exist as described above; each is counted separately in churn rates and group sizes.

---

For detailed statistics and charts, please refer to the full EDA report at:  
/home/user/FINALPROJECTZIV/artifacts/latest/crew1/eda_report.html