# Retention briefing: customer 51556

This customer is new with zero months tenure, prefers the fashion category, and has a high churn risk score of 0.86. The retention agent should prioritize a welcome call within 3 days and a follow-up email, focusing on experience without offering a discount initially.

## Customer snapshot
- Tenure 0.0 · Complain 0 · PreferredPaymentMode Credit Card · PreferedOrderCat Fashion · SatisfactionScore 1 · DaySinceLastOrder 8.0 · OrderCount 9.0 · CashbackAmount 204.0

## Churn risk
- Risk score: 0.86 (high risk band: 0.70 or higher). The model never saw this customer during training.

## Plan (decided in code from the playbook and the discount policy)
- **Contact:** Yes, priority 1 (risk 0.70 or higher). Customers with a risk score of 0.70 or higher are contacted first, prioritizing newest customers like this one. [retention_playbook.md > Who we contact first]
- **Channel:** Phone call by a retention agent. High risk customers are contacted by phone call from a retention agent for personalized outreach. [retention_playbook.md > Channels]
- **Frequency:** At most twice in 14 days. No customer should be contacted more than twice in 14 days to avoid over-contacting. [retention_playbook.md > Channels]
- **New customer:** Welcome call within 3 days plus a follow-up email; no discount on this first contact. New customers flagged by the model get a welcome call within 3 days plus a follow-up email, with no discount on first contact. [retention_playbook.md > New customers (tenure 0 to 1 months)]
- **Offer:** Not on the first contact; only if still at risk a week later. Discounts are withheld on first contact for new customers; offered only if risk persists a week later. [retention_playbook.md > New customers (tenure 0 to 1 months)]
- **Offer type:** Discount or wallet cashback within the limits. Offers can be discounts or wallet cashback, adhering to company retention budget policies. [discount_policy.md > Limits per customer]
- **Limits:** Up to INR 500 or 15% of the next order, whichever is lower; cashback up to INR 300; one offer per 30 days. Discounts capped at INR 500 or 15% of next order; cashback capped at INR 300; one offer per 30 days. [discount_policy.md > Limits per customer]
- **Approval:** Agent up to INR 300; team lead for INR 301 to 500; never above INR 500. Retention agents approve offers up to INR 300; higher amounts require team lead approval. [discount_policy.md > Approval levels]

## Do not
- Do not tell the customer their churn score [retention_playbook.md > What we never do]

## Market now (last 48 hours)
- [Charli XCX and Chris Horan Turn Stylist Vinted Sale Into Tour Wardrobe](https://news.google.com/rss/articles/CBMiU0FVX3lxTE9vUTBTVE5MTkw0S09xbm1nMTB6WDROeUJ3Rm5KUEVwNlJIeVhRUEI0YjktUmVObGNUQldubHotNmdHWWhjN2c5VEtXLXhFX2E4bHlF?oc=5), شبكة تواصل الإخبارية, 2026-10-31 07:40 UTC. Fashion sales events like Vinted's tour wardrobe sale may increase customer interest in fashion category retention.
- [Sephora Sale 2026: Our Editors Picks](https://news.google.com/rss/articles/CBMif0FVX3lxTFB5WVZ2TG51LTk4SDNFNl9FaFE5c2dWaWR1ZzZISUZfTFZIdGhRc0JDOXRTTlZESlpQcER0dGhXWmRXOWhJYlpaRmJmTFFEWWFXWUNxSC1kNTZrTTdUZVlzbnI5aXV1NDR1WjFkSHBkalI3LWpmTXZNSlVNQU9kSUE?oc=5), FASHION Magazine, 2026-10-31 07:18 UTC. Sephora's fashion sale highlights ongoing promotional activity in fashion ecommerce, relevant for retention timing.
- [Mango advances its digital business style by migrating to the cloud, increasing efficiencies and sales](https://news.google.com/rss/articles/CBMiaEFVX3lxTE4waTNtOEJrRV9adjlSbExnakh3dll1Yk0xY2dnODRrR2pmd044LXdObmg3OEFhb2FmYkpiQmpfdU42NXRnRk1udGpLU0V2UEZWLUduYWM3Ri12bXVEZWd2aXpKdDdrNTA2?oc=5), NTT Data, 2026-10-31 01:50 UTC. Mango's digital business growth may indicate increased competition and customer expectations in fashion ecommerce.

## Sources
[discount_policy.md > Approval levels] · [discount_policy.md > Limits per customer] · [retention_playbook.md > Channels] · [retention_playbook.md > New customers (tenure 0 to 1 months)] · [retention_playbook.md > What we never do] · [retention_playbook.md > Who we contact first]
