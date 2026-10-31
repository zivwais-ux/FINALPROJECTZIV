# Retention briefing: customer 50014

Customer 50014 is a new high-risk customer with a recent complaint and a preference for mobile products. The retention agent must prioritize resolving the complaint and conduct a welcome call without an initial discount.

## Customer snapshot
- Tenure 0.0 · Complain 1 · PreferredPaymentMode CC · PreferedOrderCat Mobile · SatisfactionScore 3 · DaySinceLastOrder 0.0 · OrderCount 1.0 · CashbackAmount 133.88

## Churn risk
- Risk score: 0.79 (high risk band: 0.70 or higher). The model never saw this customer during training.

## Plan (decided in code from the playbook and the discount policy)
- **Contact:** Yes, priority 1 (risk 0.70 or higher). High-risk customers with a score of 0.70 or higher are contacted first, prioritizing newest customers. [retention_playbook.md > Who we contact first]
- **Channel:** Phone call by a retention agent. High-risk customers are contacted by phone call from a retention agent for effective outreach. [retention_playbook.md > Channels]
- **Frequency:** At most twice in 14 days. Customers are contacted at most twice in 14 days to avoid over-contacting. [retention_playbook.md > Channels]
- **Complaint:** Close the complaint before any coupon or offer. Complaints must be resolved before offering coupons to avoid increasing churn. [retention_playbook.md > Customers who complained]
- **New customer:** Welcome call within 3 days plus a follow-up email; no discount on this first contact. New customers receive a welcome call within 3 days and no discount on first contact to fix experience first. [retention_playbook.md > New customers (tenure 0 to 1 months)]
- **Offer:** Only after the complaint is closed. Offers are only made after complaints are closed to ensure effectiveness. [retention_playbook.md > Customers who complained]
- **Offer type:** Discount or wallet cashback within the limits. Discounts or wallet cashback are allowed within policy limits for retention. [discount_policy.md > Limits per customer]
- **Limits:** Up to INR 500 or 15% of the next order, whichever is lower; cashback up to INR 300; one offer per 30 days. Discounts are limited to INR 500 or 15% of next order; cashback capped at INR 300; one offer per 30 days. [discount_policy.md > Limits per customer]
- **Approval:** Agent up to INR 300; team lead for INR 301 to 500; never above INR 500. Agents can approve offers up to INR 300; higher amounts require team lead approval. [discount_policy.md > Approval levels]

## Do not
- Do not tell the customer their churn score [retention_playbook.md > What we never do]

## Market now (last 48 hours)
- [Samsung Galaxy Z series foldables are breaking pre-order records in the US and Korea](https://news.google.com/rss/articles/CBMijgFBVV95cUxPTGRzVU5HUkpWQlpMLW41Y210Mlk1TXJlbEstTFh2TDZnSWhjejlZcTk5YjF5TERBdUt5dDAxUWZUVmtLaVp6STg5LU4xRGdLWGxuTVBvQ1h1ZEpCZ08tTFZqMEFobHNNNWoyaTIzdE9GQWlwLUpvbGtnRldMRnB4S2didmt6eW93MnRxOXVB?oc=5), Mashable, 2026-10-30 22:00 UTC. Strong pre-order records for Samsung Galaxy Z foldables indicate high market interest in premium mobile devices.
- [All the phones T-Mobile is giving away for free: Shop iPhone 17, Samsung Galaxy Z Fold 8, and Google Pixel 11](https://news.google.com/rss/articles/CBMilwFBVV95cUxOM3R4UVpTQ3VETVVrR1JRODkwaW9SMFFORGJpU2ZieC1udFJuakxXTVVpRHZ1TGI5eV9YelVrM0NVZVkwLWtpSmFtY2ExXzhGLTJpS1lzU3pQTmdIMGsxUlR5RGl6Z2VsdDVocGtzWG5yUG10VG5uVzVIbWJJSm9hWmFXRVZBUTMxUWNhTXpVSGFkLXB1dXhV?oc=5), Mashable, 2026-10-30 22:00 UTC. Free phone giveaways by T-Mobile may increase competitive pressure on mobile category customers.
- [Oppo Find X10 review: The competition, our verdict, pros and cons](https://news.google.com/rss/articles/CBMiZ0FVX3lxTE5RMWZhb1lXTXRuUHdEbVMyZFZKcUxNZ183bGtleU43RkxSZk1MWmsxN05TWVF2VU52LVJONlN4bi1kQmRhWkx2TmU4dXVtQ05vQ25nbXZDLWlVSGNHLWs5Z0xCeW5jTEU?oc=5), GSMArena.com, 2026-10-31 02:24 UTC. New smartphone reviews highlight competitive features that may influence customer retention decisions.

## Sources
[discount_policy.md > Approval levels] · [discount_policy.md > Limits per customer] · [retention_playbook.md > Channels] · [retention_playbook.md > Customers who complained] · [retention_playbook.md > New customers (tenure 0 to 1 months)] · [retention_playbook.md > What we never do] · [retention_playbook.md > Who we contact first]
