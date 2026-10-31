# Retention briefing: customer 50230

Customer 50230 is a medium-risk, new customer with a recent complaint and prefers laptops with cash on delivery payment. The key retention focus is resolving the complaint before offering any discount or coupon.

## Customer snapshot
- Tenure 3.0 · Complain 1 · PreferredPaymentMode COD · PreferedOrderCat Laptop & Accessory · SatisfactionScore 3 · DaySinceLastOrder 2.0 · OrderCount 2.0 · CashbackAmount 147.36

## Churn risk
- Risk score: 0.51 (medium risk band: 0.40 to 0.70). The model never saw this customer during training.

## Plan (decided in code from the playbook and the discount policy)
- **Contact:** Yes, priority 2 (complained in the last month, whatever the score). Customers who complained in the last month are contacted regardless of risk score, as they are a high priority. [retention_playbook.md > Who we contact first]
- **Channel:** App push notification, then email after 2 days without response. Medium risk customers are contacted first by app push notification, then by email after 2 days without response. [retention_playbook.md > Channels]
- **Frequency:** At most twice in 14 days. Customers are contacted at most twice in 14 days to avoid over-contacting. [retention_playbook.md > Channels]
- **Complaint:** Close the complaint before any coupon or offer. Complaints must be resolved before any coupon or offer is given to avoid increasing churn. [retention_playbook.md > Customers who complained]
- **Offer:** Only after the complaint is closed. Offers are only made after the complaint is closed, following the 'resolve before you reward' rule. [retention_playbook.md > Customers who complained]
- **Offer type:** Free-delivery voucher or a small invoice discount; no wallet cashback. Cash on delivery customers receive free-delivery vouchers or small invoice discounts, not wallet cashback. [retention_playbook.md > Cash on delivery (COD) customers]
- **Limits:** Up to INR 500 or 15% of the next order, whichever is lower; cashback up to INR 300; one offer per 30 days. Discounts are limited to INR 500 or 15% of the next order, cashback up to INR 300, and one offer per 30 days. [discount_policy.md > Limits per customer]
- **Approval:** Agent up to INR 300; team lead for INR 301 to 500; never above INR 500. Retention agents can approve offers up to INR 300; higher amounts require team lead approval. [discount_policy.md > Approval levels]

## Do not
- Do not tell the customer their churn score [retention_playbook.md > What we never do]

## Market now (last 48 hours)
- [Everything You Need To Know About Black Friday 2026: The Biggest Sales, the Best Deals, and More](https://news.google.com/rss/articles/CBMinAFBVV95cUxQNlhENTR0ckIxeDdRSzJGVUU1S2ZjWXo5RWVCV1FwRENuZjJYNm9HYm9BdGZlYVA5Z2dYUzFRc253MHFYS0M0MTVQYm5nTVNXTmd2a1M2UGRzTjBaT3c0akh2UTljb2p2dnptVHU2Wld0dFduY05qT1FzUXU5WGMwWjR0VnJySmowT2VVM3lsOVFSWGhpd24zTi1CRnI?oc=5), PCMag, 2026-10-31 05:46 UTC. Upcoming Black Friday sales may increase customer interest in laptops, aiding retention efforts.
- [Amazon's dropped the price of our favourite laptop for graphic designers by $160 in early Black Friday deal](https://news.google.com/rss/articles/CBMi2wFBVV95cUxQOUdLaW03QWx4WUJkMDNubDdmSHNUem5VTmtFUUwyMFloZWR2cmhJVWtUNUx3ME9YYmY4a05BNXBCTHBEM0VNUDJEQ3lQcmk0dFJwU3NKRkJoLXZBOUNhdVRwT2NTZTY4V203Z3ZobEI4Z0h4LWs5Y180aHZxTVlCcW8xcURWR09rLWx4TDBBb202SjM0MTNReWdKNmNCdmFZU1RKb1AyZDlJSjJqWkw1RElCY2JBMTQwV3F2U2dhSlA1eUF0ZHlLOXgtbGJQNW94NktKSUJPeXMxOFU?oc=5), Creative Bloq, 2026-10-31 05:00 UTC. Early Black Friday laptop discounts may encourage this customer's continued purchases.
- [Deal | HP OmniBook 3 with Wildcat Lake processor drops below $500](https://news.google.com/rss/articles/CBMipAFBVV95cUxOOTJYNVY5NHUtS2NjMDNaVWIyeHRjaHFlZ2dkc0I1aDBaNmFsOWlsTURmWWFDVVMwSXR6TnRxOUFMVUloWUhDVXlTd0QyUmlqeXNvOWdtdG8tdFM5Mk9Oa2FFS2piRWNLYWY1RXo0eUtSV0RlTVdPTjBBem5XaHlZd3dVcEo3VVBCbkw5S0F3eGJmSGVJc0kwTnlUak9zeEg3b2Q5SQ?oc=5), Notebookcheck, 2026-10-31 03:26 UTC. Price drops on laptops may increase this customer's likelihood to stay and order again.

## Sources
[discount_policy.md > Approval levels] · [discount_policy.md > Limits per customer] · [retention_playbook.md > Cash on delivery (COD) customers] · [retention_playbook.md > Channels] · [retention_playbook.md > Customers who complained] · [retention_playbook.md > What we never do] · [retention_playbook.md > Who we contact first]
