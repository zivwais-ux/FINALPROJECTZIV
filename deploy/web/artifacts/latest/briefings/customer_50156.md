# Retention briefing: customer 50156

Customer 50156 has a low churn risk but filed a complaint in the last month and prefers the Grocery category. The main retention focus is to resolve the complaint through support before offering any discounts, as offers are not funded for low-risk Grocery customers.

## Customer snapshot
- Tenure 26.0 · Complain 1 · PreferredPaymentMode Credit Card · PreferedOrderCat Grocery · SatisfactionScore 3 · DaySinceLastOrder 3.0 · OrderCount 1.0 · CashbackAmount 275.84

## Churn risk
- Risk score: 0.00 (low risk band: below 0.40). The model never saw this customer during training.

## Plan (decided in code from the playbook and the discount policy)
- **Contact:** Yes, priority 2 (complained in the last month, whatever the score). Customers who complained in the last month are contacted regardless of their low risk score, prioritizing complaint resolution. [retention_playbook.md > Who we contact first]
- **Channel:** Follow-up by the support team to close the complaint. Low risk customers with recent complaints receive follow-up by the support team to close the complaint before retention offers. [retention_playbook.md > Channels]
- **Frequency:** At most twice in 14 days. The playbook limits contact frequency to at most twice in 14 days to avoid customer fatigue. [retention_playbook.md > Channels]
- **Complaint:** Close the complaint before any coupon or offer. The policy mandates closing complaints before any coupons or offers to prevent increased churn. [retention_playbook.md > Customers who complained]
- **Offer:** None: offers to customers below 0.40 are not funded. Offers are not funded for customers with risk scores below 0.40, especially in the Grocery category with low churn and thin margins. [discount_policy.md > Offers that need extra care]

## Do not
- Do not tell the customer their churn score [retention_playbook.md > What we never do]

## Market now (last 48 hours)
- [A Closer Look Into a Landmark Grocery Delivery Deal](https://news.google.com/rss/articles/CBMifEFVX3lxTE80dFI1LWxGbjZWVy1Sd3hFb2UwUnRkMG5KcHBYT0ZKby1NYXBjTDA2b1pqZzZIY0RPdVpQMFR6Z3o5ZFo4QlYxNXZEZ2o1bHZKa3F0cDZFZzdsbENBZG0xelB3V1I1a0xHSjlqNE9LaVJ2R2hZYzNxaG02RUg?oc=5), Progressive Grocer, 2026-10-30 15:21 UTC. A major grocery delivery deal may increase competition, impacting customer retention strategies.
- [DoorDash's $17 Billion Instacart Deal Creates a Grocery Ad Giant](https://news.google.com/rss/articles/CBMijwFBVV95cUxOUXdXbXEtLUVlaXNMczVFUERBX3NlQnBBZlZKdXdTNE9WZF81TUJMckdtSVdpVUFOQVNTVU5PZ3ZMaVhwdWVoazdVN1BYNExtbENjYmprbWdBQzlZSlFYWTRFenM5dE5vMTgzREcwQWoxTVc0YXBrNVpKWHdIbTF5R2FSUFRsam52UTdjWHpnbw?oc=5), DesignRush, 2026-10-30 14:57 UTC. The creation of a grocery ad giant could shift market dynamics, affecting customer loyalty.
- [New Grocery Delivery Service](https://news.google.com/rss/articles/CBMigwFBVV95cUxNMTBMTloyMUl0ODBBaHRDT0M3Y2xSTVA5VmFtaHZKQ0Myb0NJOTNDVXFVV3dHeUtFSUZoR1h2U1VGdWhOOWI1NGZRSE9XZ2JjVFNsekZJbHVsTFQtWjZmNkVUb3AtMXhpaFJlQWY1bERSQUhhS1NsOTdqelZNcVlxckZZOA?oc=5), CTV News, 2026-10-30 14:49 UTC. New grocery delivery services may increase options for customers, influencing retention efforts.

## Sources
[discount_policy.md > Offers that need extra care] · [retention_playbook.md > Channels] · [retention_playbook.md > Customers who complained] · [retention_playbook.md > What we never do] · [retention_playbook.md > Who we contact first]
