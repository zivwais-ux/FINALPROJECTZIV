# Retention briefing: customer 50471

Customer 50471 is a high-risk churn customer with a recent complaint, prefers debit card payments, and has moderate satisfaction. The retention agent must prioritize complaint resolution before offering any discount or cashback within policy limits.

## Customer snapshot
- Tenure 20.0 · Complain 1 · PreferredPaymentMode Debit Card · PreferedOrderCat Others · SatisfactionScore 4 · DaySinceLastOrder 8.0 · OrderCount 13.0 · CashbackAmount 292.46

## Churn risk
- Risk score: 0.77 (high risk band: 0.70 or higher). The model never saw this customer during training.

## Plan (decided in code from the playbook and the discount policy)
- **Contact:** Yes, priority 1 (risk 0.70 or higher). Customers with a risk score of 0.70 or higher are contacted first as a priority according to the retention playbook. [retention_playbook.md > Who we contact first]
- **Channel:** Phone call by a retention agent. High risk customers are contacted by phone call from a retention agent to maximize engagement. [retention_playbook.md > Channels]
- **Frequency:** At most twice in 14 days. The playbook limits contact frequency to at most twice in 14 days to avoid customer fatigue. [retention_playbook.md > Channels]
- **Complaint:** Close the complaint before any coupon or offer. Complaints must be resolved before any coupon or offer is given to avoid increasing churn. [retention_playbook.md > Customers who complained]
- **Offer:** Only after the complaint is closed. Offers are only made after complaints are closed, following the 'resolve before you reward' rule. [retention_playbook.md > Customers who complained]
- **Offer type:** Discount or wallet cashback within the limits. Discounts or wallet cashback are allowed within the specified limits per customer. [discount_policy.md > Limits per customer]
- **Limits:** Up to INR 500 or 15% of the next order, whichever is lower; cashback up to INR 300; one offer per 30 days. Discounts are capped at INR 500 or 15% of the next order, cashback up to INR 300, and one offer per 30 days. [discount_policy.md > Limits per customer]
- **Approval:** Agent up to INR 300; team lead for INR 301 to 500; never above INR 500. Retention agents can approve offers up to INR 300; higher amounts require team lead approval. [discount_policy.md > Approval levels]

## Do not
- Do not tell the customer their churn score [retention_playbook.md > What we never do]

## Market now (last 48 hours)
- [Luvme Hair Kicks Off Black Friday 2026 With Up to $120 Off](https://news.google.com/rss/articles/CBMiyAFBVV95cUxPc2o3MllDRXJmRVlHczVnV1ZENEJJdURmSVpBN3FvZ0VWT2x3c1hWOHR2ZzBSU3k1VFFmTHkyUC1ybnJHOTBfNTJvcXlLM1BYSkdWQ1lZTGlMZGFGNXFTMUZZQzV5Q2NSTWx5Yjg3ZWRMWTFydTZTclNNUnVCMjJJWTBnSGpERDJUS3p3MVRyS2syWmhCYkNLWmpSRThyNWhBd2FSUVFTTEhqbml3cF9Hb2V4RkxvY3FPV29XdmtXQ3JVQ19nUWQzaw?oc=5), GlobeNewswire, 2026-10-31 06:52 UTC. Black Friday discounts in ecommerce may increase customer expectations for deals, impacting retention strategies.
- [Webinar: Is Your Ecommerce Business Ready for 2027?](https://news.google.com/rss/articles/CBMihwFBVV95cUxNWUwwN2h2ZDNzYlN1R2RTTHlRaDVPV1V0c3NtSDQwbXhjZmNZclZyaGVfai0tbHJ6RkxwMzZCWllQYnVMN0lGMHI3ZXJFSWNQWlhYSDYzTFNaNUlFd204RUgxNUM5dmJFMDZzU3hKOEF4UUFQc2R1d3pybVBEck9QOG95QlRfNXc?oc=5), Tamebay, 2026-10-30 19:49 UTC. Webinar on ecommerce readiness for 2027 may offer insights to improve retention approaches.
- [Google's 'best smartwatch yet' just scored a historic discount, weeks before Black Friday](https://news.google.com/rss/articles/CBMiigFBVV95cUxNb0Z2S3dzOGI2NEV2TkRPRkRSSVBqNFFqVHkzcDlKSjk3YjhmbW9sbW1sdDZzNWZ1TkJ3MWttaExUQXhGdVhPb1NjdExTOVF3aUZHUzZaVGFOZEw0NzEySnBTaVNOT3J1QV9ETHFkU2hKMkNQYkp3QUEta29xa1BmMTQ0dDVvU2xZQlE?oc=5), Android Police, 2026-10-30 17:05 UTC. Historic discounts on tech products may influence customer expectations for competitive offers.

## Sources
[discount_policy.md > Approval levels] · [discount_policy.md > Limits per customer] · [retention_playbook.md > Channels] · [retention_playbook.md > Customers who complained] · [retention_playbook.md > What we never do] · [retention_playbook.md > Who we contact first]
