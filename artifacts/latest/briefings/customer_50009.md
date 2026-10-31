# Retention briefing: customer 50009

Customer 50009 has a medium churn risk, recently complained, and prefers the Mobile category. The main retention focus is to resolve the complaint before offering any discount or cashback within policy limits.

## Customer snapshot
- Tenure 13.0 · Complain 1 · PreferredPaymentMode E wallet · PreferedOrderCat Mobile · SatisfactionScore 3 · DaySinceLastOrder 2.0 · OrderCount 1.0 · CashbackAmount 126.83

## Churn risk
- Risk score: 0.68 (medium risk band: 0.40 to 0.70). The model never saw this customer during training.

## Plan (decided in code from the playbook and the discount policy)
- **Contact:** Yes, priority 2 (complained in the last month, whatever the score). Customers who complained in the last month are contacted regardless of risk score, prioritizing their retention. [retention_playbook.md > Who we contact first]
- **Channel:** App push notification, then email after 2 days without response. Medium risk customers are contacted first by app push notification, then email if no response after 2 days. [retention_playbook.md > Channels]
- **Frequency:** At most twice in 14 days. Customers are contacted at most twice in 14 days to avoid over-contacting and potential annoyance. [retention_playbook.md > Channels]
- **Complaint:** Close the complaint before any coupon or offer. Complaints must be resolved before any coupon or offer is given to avoid increasing churn. [retention_playbook.md > Customers who complained]
- **Offer:** Only after the complaint is closed. Offers are only made after the complaint is closed, following the 'resolve before you reward' rule. [retention_playbook.md > Customers who complained]
- **Offer type:** Discount or wallet cashback within the limits. Discounts or wallet cashback are allowed within the limits set by the discount policy. [discount_policy.md > Limits per customer]
- **Limits:** Up to INR 500 or 15% of the next order, whichever is lower; cashback up to INR 300; one offer per 30 days. Offers are limited to INR 500 or 15% of the next order, cashback up to INR 300, and one offer per 30 days. [discount_policy.md > Limits per customer]
- **Approval:** Agent up to INR 300; team lead for INR 301 to 500; never above INR 500. Agent approval is required up to INR 300; team lead approval for INR 301 to 500; never above INR 500. [discount_policy.md > Approval levels]

## Do not
- Do not tell the customer their churn score [retention_playbook.md > What we never do]

## Market now (last 48 hours)
- [Oppo Find X10 review: The competition, our verdict, pros and cons](https://news.google.com/rss/articles/CBMiZ0FVX3lxTE5RMWZhb1lXTXRuUHdEbVMyZFZKcUxNZ183bGtleU43RkxSZk1MWmsxN05TWVF2VU52LVJONlN4bi1kQmRhWkx2TmU4dXVtQ05vQ25nbXZDLWlVSGNHLWs5Z0xCeW5jTEU?oc=5), GSMArena.com, 2026-10-31 02:24 UTC. New smartphone reviews may influence customer interest and retention in the Mobile category.
- [Why Google’s Pixel 11 Pro Holds Firm Beside Galaxy S26 Ultra and iPhone 18 Pro](https://news.google.com/rss/articles/CBMijgFBVV95cUxNQm1XNm1xVTMxdElkMy01eFg4Mk9fc2VkdjE0Y2JpSld0LV9Zb1VfZE8zeG1NVnhEeDdRRnVENGh3Z3dTLWIwUzVJTlN4RjFLUERHckJzSmxTWTlIYjl6ZDlyVDM0OEFBT1pXS09XX0t3MnIzMXpTeEJidDF0VHBCNkQ3d1pTR1E3NlBNTVdn?oc=5), TechEBlog -, 2026-10-30 22:52 UTC. Competitive smartphone offers may increase churn risk if not matched by retention efforts.
- [Samsung Galaxy Z series foldables are breaking pre-order records in the US and Korea](https://news.google.com/rss/articles/CBMijgFBVV95cUxPTGRzVU5HUkpWQlpMLW41Y210Mlk1TXJlbEstTFh2TDZnSWhjejlZcTk5YjF5TERBdUt5dDAxUWZUVmtLaVp6STg5LU4xRGdLWGxuTVBvQ1h1ZEpCZ08tTFZqMEFobHNNNWoyaTIzdE9GQWlwLUpvbGtnRldMRnB4S2didmt6eW93MnRxOXVB?oc=5), Mashable, 2026-10-30 22:00 UTC. Record pre-orders for foldable phones indicate strong market interest, relevant for Mobile category retention.

## Sources
[discount_policy.md > Approval levels] · [discount_policy.md > Limits per customer] · [retention_playbook.md > Channels] · [retention_playbook.md > Customers who complained] · [retention_playbook.md > What we never do] · [retention_playbook.md > Who we contact first]
