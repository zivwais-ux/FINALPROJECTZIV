# Retention briefing: customer 51337

Customer 51337 has a medium churn risk and recently filed a complaint. They prefer fashion purchases paid via e-wallet and have a tenure of 13 months with moderate satisfaction.

## Customer snapshot
- Tenure 13.0 · Complain 1 · PreferredPaymentMode E wallet · PreferedOrderCat Fashion · SatisfactionScore 5 · DaySinceLastOrder 0.0 · OrderCount 2.0 · CashbackAmount 208.54

## Churn risk
- Risk score: 0.68 (medium risk band: 0.40 to 0.70). The model never saw this customer during training.

## Plan (decided in code from the playbook and the discount policy)
- **Contact:** Yes, priority 2 (complained in the last month, whatever the score). Customers who complained in the last month are contacted regardless of risk score, prioritizing their retention. [retention_playbook.md > Who we contact first]
- **Channel:** App push notification, then email after 2 days without response. Medium risk customers are contacted first by app push notification, then by email if no response. [retention_playbook.md > Channels]
- **Frequency:** At most twice in 14 days. Customers are contacted at most twice in 14 days to avoid over-contacting. [retention_playbook.md > Channels]
- **Complaint:** Close the complaint before any coupon or offer. Complaints must be resolved before any coupon or offer is given to avoid increasing churn. [retention_playbook.md > Customers who complained]
- **Offer:** Only after the complaint is closed. Offers are only made after the complaint is closed to ensure effectiveness. [retention_playbook.md > Customers who complained]
- **Offer type:** Discount or wallet cashback within the limits. Discounts or wallet cashback are allowed within specified limits for retention offers. [discount_policy.md > Limits per customer]
- **Limits:** Up to INR 500 or 15% of the next order, whichever is lower; cashback up to INR 300; one offer per 30 days. Offers are limited to INR 500 or 15% of next order, cashback up to INR 300, and one offer per 30 days. [discount_policy.md > Limits per customer]
- **Approval:** Agent up to INR 300; team lead for INR 301 to 500; never above INR 500. Retention agents can approve offers up to INR 300; higher amounts require team lead approval. [discount_policy.md > Approval levels]

## Do not
- Do not tell the customer their churn score [retention_playbook.md > What we never do]

## Market now (last 48 hours)
- [Sephora Sale 2026: Our Editors Picks](https://news.google.com/rss/articles/CBMif0FVX3lxTFB5WVZ2TG51LTk4SDNFNl9FaFE5c2dWaWR1ZzZISUZfTFZIdGhRc0JDOXRTTlZESlpQcER0dGhXWmRXOWhJYlpaRmJmTFFEWWFXWUNxSC1kNTZrTTdUZVlzbnI5aXV1NDR1WjFkSHBkalI3LWpmTXZNSlVNQU9kSUE?oc=5), FASHION Magazine, 2026-10-31 07:18 UTC. Current fashion sales promotions may increase customer engagement and retention opportunities.
- [Shoppers snap up 10 thermal tops a minute as M&S cosy layers go on sale](https://news.google.com/rss/articles/CBMilgFBVV95cUxQTE5naDV1SV9ObTVQWnB6cDZsMG1uTXpBUnFBcnlXamoweWE5MVZhaU9SMFJyWVhWeFQtV0w2SWlHS0pvdXViODdaNHBEcEYyUDRkM3FBRDEtLWxjbm12XzdDWGpIejVDOTFWSUZyb09Ea3hiRnlOSWN0YXpwN193N1BTVjlFLTlHQlh6NUVuMVEzcTVsQmc?oc=5), malverngazette.co.uk, 2026-10-31 03:07 UTC. Increased demand for thermal tops suggests seasonal buying trends relevant to fashion customers.
- [Armani CEO Giuseppe Marsocci Weighs Who Gets the First 15 Percent of the House](https://news.google.com/rss/articles/CBMiigFBVV95cUxOOEdCX0x6emRCMWxQT0pjNVVmTU1hNjQtRm5DaHl4UjhqTHRkM1VuUEJxVzBvOFhsV212YVpLS2x4QnA2TVpkblFJenV5ejE2RGJXaW5fSzM2SUxHTjhVNzVfSVhRY1pKLWdYdjBDcFI4bGdkZnB1cHpLZldYQ2NZSHNKTFowRGdlNXc?oc=5), Observer, 2026-10-31 00:30 UTC. Leadership insights on fashion industry priorities may influence market conditions affecting customer retention.

## Sources
[discount_policy.md > Approval levels] · [discount_policy.md > Limits per customer] · [retention_playbook.md > Channels] · [retention_playbook.md > Customers who complained] · [retention_playbook.md > What we never do] · [retention_playbook.md > Who we contact first]
