# Retention briefing: customer 50032

Customer 50032 is a new customer with zero tenure, medium churn risk, and a preference for laptops and accessories. They have made one order and have a cashback balance, with a medium risk score requiring prioritized retention contact.

## Customer snapshot
- Tenure 0.0 · Complain 0 · PreferredPaymentMode Credit Card · PreferedOrderCat Laptop & Accessory · SatisfactionScore 3 · DaySinceLastOrder 0.0 · OrderCount 1.0 · CashbackAmount 161.32

## Churn risk
- Risk score: 0.42 (medium risk band: 0.40 to 0.70). The model never saw this customer during training.

## Plan (decided in code from the playbook and the discount policy)
- **Contact:** Yes, priority 3 (risk 0.40 to 0.70). Customers with a risk score between 0.40 and 0.70 are contacted after high risk and recent complainants, per the retention playbook. [retention_playbook.md > Who we contact first]
- **Channel:** App push notification, then email after 2 days without response. Medium risk customers are contacted first by app push notification, then by email after 2 days without response. [retention_playbook.md > Channels]
- **Frequency:** At most twice in 14 days. The playbook limits contact frequency to at most twice in 14 days to avoid over-contacting customers. [retention_playbook.md > Channels]
- **New customer:** Welcome call within 3 days plus a follow-up email; no discount on this first contact. New customers flagged by the model receive a welcome call within 3 days plus a follow-up email without a discount on first contact. [retention_playbook.md > New customers (tenure 0 to 1 months)]
- **Offer:** Not on the first contact; only if still at risk a week later. Discounts are not offered on the first contact for new customers; only if still at risk a week later. [retention_playbook.md > New customers (tenure 0 to 1 months)]
- **Offer type:** Discount or wallet cashback within the limits. Offers can be discounts or wallet cashback within the policy limits. [discount_policy.md > Limits per customer]
- **Limits:** Up to INR 500 or 15% of the next order, whichever is lower; cashback up to INR 300; one offer per 30 days. Discounts are limited to INR 500 or 15% of the next order, cashback up to INR 300, and one offer per 30 days. [discount_policy.md > Limits per customer]
- **Approval:** Agent up to INR 300; team lead for INR 301 to 500; never above INR 500. Agents can approve offers up to INR 300; higher amounts require team lead approval, never exceeding INR 500. [discount_policy.md > Approval levels]

## Do not
- Do not tell the customer their churn score [retention_playbook.md > What we never do]

## Market now (last 48 hours)
- [Everything You Need To Know About Black Friday 2026: The Biggest Sales, the Best Deals, and More](https://news.google.com/rss/articles/CBMinAFBVV95cUxQNlhENTR0ckIxeDdRSzJGVUU1S2ZjWXo5RWVCV1FwRENuZjJYNm9HYm9BdGZlYVA5Z2dYUzFRc253MHFYS0M0MTVQYm5nTVNXTmd2a1M2UGRzTjBaT3c0akh2UTljb2p2dnptVHU2Wld0dFduY05qT1FzUXU5WGMwWjR0VnJySmowT2VVM3lsOVFSWGhpd24zTi1CRnI?oc=5), PCMag, 2026-10-31 05:46 UTC. Upcoming Black Friday sales may increase customer interest in electronics, aiding retention efforts.
- [Amazon's dropped the price of our favourite laptop for graphic designers by $160 in early Black Friday deal](https://news.google.com/rss/articles/CBMi2wFBVV95cUxQOUdLaW03QWx4WUJkMDNubDdmSHNUem5VTmtFUUwyMFloZWR2cmhJVWtUNUx3ME9YYmY4a05BNXBCTHBEM0VNUDJEQ3lQcmk0dFJwU3NKRkJoLXZBOUNhdVRwT2NTZTY4V203Z3ZobEI4Z0h4LWs5Y180aHZxTVlCcW8xcURWR09rLWx4TDBBb202SjM0MTNReWdKNmNCdmFZU1RKb1AyZDlJSjJqWkw1RElCY2JBMTQwV3F2U2dhSlA1eUF0ZHlLOXgtbGJQNW94NktKSUJPeXMxOFU?oc=5), Creative Bloq, 2026-10-31 05:00 UTC. Early Black Friday laptop discounts may influence this customer's purchase decisions and retention.
- [Deal | HP OmniBook 3 with Wildcat Lake processor drops below $500](https://news.google.com/rss/articles/CBMipAFBVV95cUxOOTJYNVY5NHUtS2NjMDNaVWIyeHRjaHFlZ2dkc0I1aDBaNmFsOWlsTURmWWFDVVMwSXR6TnRxOUFMVUloWUhDVXlTd0QyUmlqeXNvOWdtdG8tdFM5Mk9Oa2FFS2piRWNLYWY1RXo0eUtSV0RlTVdPTjBBem5XaHlZd3dVcEo3VVBCbkw5S0F3eGJmSGVJc0kwTnlUak9zeEg3b2Q5SQ?oc=5), Notebookcheck, 2026-10-31 03:26 UTC. Price drops on laptops like the HP OmniBook may increase competitive pressure but also customer interest.

## Sources
[discount_policy.md > Approval levels] · [discount_policy.md > Limits per customer] · [retention_playbook.md > Channels] · [retention_playbook.md > New customers (tenure 0 to 1 months)] · [retention_playbook.md > What we never do] · [retention_playbook.md > Who we contact first]
