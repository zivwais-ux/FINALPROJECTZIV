# Retention briefing: customer 51809

This customer is new with zero tenure, has complained recently, prefers mobile category products, and pays cash on delivery. The retention plan prioritizes a welcome call, complaint resolution before offers, and limited discount options due to payment mode and risk level.

## Customer snapshot
- Tenure 0.0 · Complain 1 · PreferredPaymentMode COD · PreferedOrderCat Mobile · SatisfactionScore 1 · DaySinceLastOrder 0.0 · OrderCount 1.0 · CashbackAmount 123.4

## Churn risk
- Risk score: 0.95 (high risk band: 0.70 or higher). The model never saw this customer during training.

## Plan (decided in code from the playbook and the discount policy)
- **Contact:** Yes, priority 1 (risk 0.70 or higher). Customers with a risk score of 0.70 or higher are contacted first, prioritizing newest customers. [retention_playbook.md > Who we contact first]
- **Channel:** Phone call by a retention agent. High-risk customers are contacted by phone call from a retention agent. [retention_playbook.md > Channels]
- **Frequency:** At most twice in 14 days. Customers are contacted at most twice in 14 days to avoid over-contacting. [retention_playbook.md > Channels]
- **Complaint:** Close the complaint before any coupon or offer. Complaints must be resolved before any coupon or offer is given to avoid increasing churn. [retention_playbook.md > Customers who complained]
- **New customer:** Welcome call within 3 days plus a follow-up email; no discount on this first contact. New customers receive a welcome call within 3 days plus a follow-up email; no discount on first contact. [retention_playbook.md > New customers (tenure 0 to 1 months)]
- **Offer:** Only after the complaint is closed. Offers are only made after the complaint is closed to ensure effectiveness. [retention_playbook.md > Customers who complained]
- **Offer type:** Free-delivery voucher or a small invoice discount; no wallet cashback. Cash on delivery customers get free-delivery vouchers or small invoice discounts, not wallet cashback. [retention_playbook.md > Cash on delivery (COD) customers]
- **Limits:** Up to INR 500 or 15% of the next order, whichever is lower; cashback up to INR 300; one offer per 30 days. Discounts are limited to INR 500 or 15% of next order, cashback up to INR 300, and one offer per 30 days. [discount_policy.md > Limits per customer]
- **Approval:** Agent up to INR 300; team lead for INR 301 to 500; never above INR 500. Agents approve offers up to INR 300; team leads approve INR 301 to 500; above INR 500 is not allowed. [discount_policy.md > Approval levels]

## Do not
- Do not tell the customer their churn score [retention_playbook.md > What we never do]

## Market now (last 48 hours)
- [Oppo Find X10 review: The competition, our verdict, pros and cons](https://news.google.com/rss/articles/CBMiZ0FVX3lxTE5RMWZhb1lXTXRuUHdEbVMyZFZKcUxNZ183bGtleU43RkxSZk1MWmsxN05TWVF2VU52LVJONlN4bi1kQmRhWkx2TmU4dXVtQ05vQ25nbXZDLWlVSGNHLWs5Z0xCeW5jTEU?oc=5), GSMArena.com, 2026-10-31 02:24 UTC. New smartphone reviews may influence customer interest in mobile products.
- [Why Google’s Pixel 11 Pro Holds Firm Beside Galaxy S26 Ultra and iPhone 18 Pro](https://news.google.com/rss/articles/CBMijgFBVV95cUxNQm1XNm1xVTMxdElkMy01eFg4Mk9fc2VkdjE0Y2JpSld0LV9Zb1VfZE8zeG1NVnhEeDdRRnVENGh3Z3dTLWIwUzVJTlN4RjFLUERHckJzSmxTWTlIYjl6ZDlyVDM0OEFBT1pXS09XX0t3MnIzMXpTeEJidDF0VHBCNkQ3d1pTR1E3NlBNTVdn?oc=5), TechEBlog -, 2026-10-30 22:52 UTC. Strong competitor phone offers increase retention risk for mobile category customers.
- [Samsung Galaxy Z series foldables are breaking pre-order records in the US and Korea](https://news.google.com/rss/articles/CBMijgFBVV95cUxPTGRzVU5HUkpWQlpMLW41Y210Mlk1TXJlbEstTFh2TDZnSWhjejlZcTk5YjF5TERBdUt5dDAxUWZUVmtLaVp6STg5LU4xRGdLWGxuTVBvQ1h1ZEpCZ08tTFZqMEFobHNNNWoyaTIzdE9GQWlwLUpvbGtnRldMRnB4S2didmt6eW93MnRxOXVB?oc=5), Mashable, 2026-10-30 22:00 UTC. Record pre-orders for foldable phones may shift customer preferences in mobile category.

## Sources
[discount_policy.md > Approval levels] · [discount_policy.md > Limits per customer] · [retention_playbook.md > Cash on delivery (COD) customers] · [retention_playbook.md > Channels] · [retention_playbook.md > Customers who complained] · [retention_playbook.md > New customers (tenure 0 to 1 months)] · [retention_playbook.md > What we never do] · [retention_playbook.md > Who we contact first]
