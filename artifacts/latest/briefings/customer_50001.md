# Retention briefing: customer 50001

Customer 50001 is a medium-risk churn customer with a recent complaint and low satisfaction, preferring laptops and debit card payments. The retention focus is on resolving the complaint before offering any discount or cashback within policy limits.

## Customer snapshot
- Tenure 4.0 · Complain 1 · PreferredPaymentMode Debit Card · PreferedOrderCat Laptop & Accessory · SatisfactionScore 2 · DaySinceLastOrder 5.0 · OrderCount 1.0 · CashbackAmount 159.93

## Churn risk
- Risk score: 0.64 (medium risk band: 0.40 to 0.70). The model never saw this customer during training.

## Plan (decided in code from the playbook and the discount policy)
- **Contact:** Yes, priority 2 (complained in the last month, whatever the score). Customers who complained in the last month are contacted regardless of risk score, as they are a top priority. [retention_playbook.md > Who we contact first]
- **Channel:** App push notification, then email after 2 days without response. Medium risk customers are contacted first by app push notification, then email if no response after 2 days. [retention_playbook.md > Channels]
- **Frequency:** At most twice in 14 days. Customers are contacted at most twice in 14 days to avoid over-contacting and potential churn increase. [retention_playbook.md > Channels]
- **Complaint:** Close the complaint before any coupon or offer. The complaint must be resolved before any coupon or offer is given to avoid worsening churn risk. [retention_playbook.md > Customers who complained]
- **Offer:** Only after the complaint is closed. Offers are only made after complaint closure to ensure the coupon is seen as a reward, not an apology. [retention_playbook.md > Customers who complained]
- **Offer type:** Discount or wallet cashback within the limits. Discounts or wallet cashback are allowed within the limits set by the discount policy. [discount_policy.md > Limits per customer]
- **Limits:** Up to INR 500 or 15% of the next order, whichever is lower; cashback up to INR 300; one offer per 30 days. Offers are limited to INR 500 or 15% of next order, cashback up to INR 300, and one offer per 30 days. [discount_policy.md > Limits per customer]
- **Approval:** Agent up to INR 300; team lead for INR 301 to 500; never above INR 500. Agent approval is allowed up to INR 300; higher amounts require team lead approval, never exceeding INR 500. [discount_policy.md > Approval levels]

## Do not
- Do not tell the customer their churn score [retention_playbook.md > What we never do]

## Market now (last 48 hours)
- [Amazon's dropped the price of our favourite laptop for graphic designers by $160 in early Black Friday deal](https://news.google.com/rss/articles/CBMi2wFBVV95cUxQOUdLaW03QWx4WUJkMDNubDdmSHNUem5VTmtFUUwyMFloZWR2cmhJVWtUNUx3ME9YYmY4a05BNXBCTHBEM0VNUDJEQ3lQcmk0dFJwU3NKRkJoLXZBOUNhdVRwT2NTZTY4V203Z3ZobEI4Z0h4LWs5Y180aHZxTVlCcW8xcURWR09rLWx4TDBBb202SjM0MTNReWdKNmNCdmFZU1RKb1AyZDlJSjJqWkw1RElCY2JBMTQwV3F2U2dhSlA1eUF0ZHlLOXgtbGJQNW94NktKSUJPeXMxOFU?oc=5), Creative Bloq, 2026-10-31 05:00 UTC. Recent laptop discounts may increase customer interest and improve retention chances if offered timely.
- [Alienware’s RTX 5070 laptop with a 240Hz OLED screen drops to $1,949.99](https://news.google.com/rss/articles/CBMigAFBVV95cUxQcVF1Mm9sdHNTelNIdWtPaFlwUjNIeC0tVjFKMGlkR3BzOE9oVkxBNHRScTItQ3ppUjFyRGFOUldaNzFETV9BSGNXWTJxc1NmWVFvaTR5WHFKVXlmOXlXVE92RkdneWZNZEVBUmNXSVU2VVlyd3NEUElJVlZWNGdQNA?oc=5), MIXED News, 2026-10-30 20:48 UTC. New high-performance laptops entering the market may raise customer expectations for product offerings.
- [Dell targets MacBook Neo and launches the XPS 13 laptop](https://news.google.com/rss/articles/CBMiqgFBVV95cUxPUVBNOS1LTzRmQUR6LW9KaFdSbGFoQ0hVR3d5TlNJQ3dlSmJya09iSnkwRElMZUhoWnRZYXJVbmpGQVhYal9IbnRVVHdscHFaeHk1Nno3dXZWY3l1cV9XUEU4WlRlbEhqOUY2Q0UwWUdxLWVxR25Qa2tha0tiZHdIVG1PaHpMRUFwMTlHQ2I4dXhFck84Y3MxbzgwNmlHREpBTmx4NEhpQ1gtQQ?oc=5), آي-فون إسلام, 2026-10-30 17:42 UTC. Dell's new laptop launch could influence customer preferences and retention strategies in the laptop category.

## Sources
[discount_policy.md > Approval levels] · [discount_policy.md > Limits per customer] · [retention_playbook.md > Channels] · [retention_playbook.md > Customers who complained] · [retention_playbook.md > What we never do] · [retention_playbook.md > Who we contact first]
