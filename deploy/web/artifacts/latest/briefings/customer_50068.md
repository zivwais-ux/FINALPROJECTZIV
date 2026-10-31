# Retention briefing: customer 50068

This customer is new with zero months tenure, has recently complained, and prefers laptops and accessories. They have a high churn risk score of 0.97, making timely and careful retention efforts critical.

## Customer snapshot
- Tenure 0.0 · Complain 1 · PreferredPaymentMode Debit Card · PreferedOrderCat Laptop & Accessory · SatisfactionScore 3 · DaySinceLastOrder 1.0 · OrderCount 1.0 · CashbackAmount 159.16

## Churn risk
- Risk score: 0.97 (high risk band: 0.70 or higher). The model never saw this customer during training.

## Plan (decided in code from the playbook and the discount policy)
- **Contact:** Yes, priority 1 (risk 0.70 or higher). Customers with a risk score of 0.70 or higher are contacted first, prioritizing newest customers like this one. [retention_playbook.md > Who we contact first]
- **Channel:** Phone call by a retention agent. High risk customers are contacted by phone call from a retention agent for personalized outreach. [retention_playbook.md > Channels]
- **Frequency:** At most twice in 14 days. No customer should be contacted more than twice in 14 days to avoid over-contacting. [retention_playbook.md > Channels]
- **Complaint:** Close the complaint before any coupon or offer. Complaints must be resolved before offering coupons, as unresolved complaints increase churn risk. [retention_playbook.md > Customers who complained]
- **New customer:** Welcome call within 3 days plus a follow-up email; no discount on this first contact. New customers receive a welcome call within 3 days and a follow-up email, with no discount on first contact. [retention_playbook.md > New customers (tenure 0 to 1 months)]
- **Offer:** Only after the complaint is closed. Offers are only made after complaints are closed to avoid ineffective retention efforts. [retention_playbook.md > Customers who complained]
- **Offer type:** Discount or wallet cashback within the limits. Discounts or wallet cashback are allowed within policy limits to incentivize retention. [discount_policy.md > Limits per customer]
- **Limits:** Up to INR 500 or 15% of the next order, whichever is lower; cashback up to INR 300; one offer per 30 days. Discounts capped at INR 500 or 15% of next order; cashback capped at INR 300; one offer per 30 days. [discount_policy.md > Limits per customer]
- **Approval:** Agent up to INR 300; team lead for INR 301 to 500; never above INR 500. Agents can approve offers up to INR 300; higher amounts require team lead approval, never exceeding INR 500. [discount_policy.md > Approval levels]

## Do not
- Do not tell the customer their churn score [retention_playbook.md > What we never do]

## Market now (last 48 hours)
- [Everything You Need To Know About Black Friday 2026: The Biggest Sales, the Best Deals, and More](https://news.google.com/rss/articles/CBMinAFBVV95cUxQNlhENTR0ckIxeDdRSzJGVUU1S2ZjWXo5RWVCV1FwRENuZjJYNm9HYm9BdGZlYVA5Z2dYUzFRc253MHFYS0M0MTVQYm5nTVNXTmd2a1M2UGRzTjBaT3c0akh2UTljb2p2dnptVHU2Wld0dFduY05qT1FzUXU5WGMwWjR0VnJySmowT2VVM3lsOVFSWGhpd24zTi1CRnI?oc=5), PCMag, 2026-10-31 05:46 UTC. Upcoming Black Friday sales hype may increase customer expectations and retention urgency.
- [Amazon's dropped the price of our favourite laptop for graphic designers by $160 in early Black Friday deal](https://news.google.com/rss/articles/CBMi2wFBVV95cUxQOUdLaW03QWx4WUJkMDNubDdmSHNUem5VTmtFUUwyMFloZWR2cmhJVWtUNUx3ME9YYmY4a05BNXBCTHBEM0VNUDJEQ3lQcmk0dFJwU3NKRkJoLXZBOUNhdVRwT2NTZTY4V203Z3ZobEI4Z0h4LWs5Y180aHZxTVlCcW8xcURWR09rLWx4TDBBb202SjM0MTNReWdKNmNCdmFZU1RKb1AyZDlJSjJqWkw1RElCY2JBMTQwV3F2U2dhSlA1eUF0ZHlLOXgtbGJQNW94NktKSUJPeXMxOFU?oc=5), Creative Bloq, 2026-10-31 05:00 UTC. Early Black Friday laptop discounts may increase this customer's price sensitivity and retention challenge.
- [Deal | HP OmniBook 3 with Wildcat Lake processor drops below $500](https://news.google.com/rss/articles/CBMipAFBVV95cUxOOTJYNVY5NHUtS2NjMDNaVWIyeHRjaHFlZ2dkc0I1aDBaNmFsOWlsTURmWWFDVVMwSXR6TnRxOUFMVUloWUhDVXlTd0QyUmlqeXNvOWdtdG8tdFM5Mk9Oa2FFS2piRWNLYWY1RXo0eUtSV0RlTVdPTjBBem5XaHlZd3dVcEo3VVBCbkw5S0F3eGJmSGVJc0kwTnlUak9zeEg3b2Q5SQ?oc=5), Notebookcheck, 2026-10-31 03:26 UTC. Price drops on laptops like the HP OmniBook could sway this customer's buying decisions and retention.

## Sources
[discount_policy.md > Approval levels] · [discount_policy.md > Limits per customer] · [retention_playbook.md > Channels] · [retention_playbook.md > Customers who complained] · [retention_playbook.md > New customers (tenure 0 to 1 months)] · [retention_playbook.md > What we never do] · [retention_playbook.md > Who we contact first]
