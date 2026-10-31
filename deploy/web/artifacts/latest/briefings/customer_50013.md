# Retention briefing: customer 50013

Customer 50013 is a new customer with zero months tenure who recently complained and prefers the Mobile category, paying by cash on delivery. The main retention focus is to resolve their complaint through support without offering discounts due to their low churn risk score.

## Customer snapshot
- Tenure 0.0 · Complain 1 · PreferredPaymentMode COD · PreferedOrderCat Mobile · SatisfactionScore 3 · DaySinceLastOrder 2.0 · OrderCount 2.0 · CashbackAmount 134.41

## Churn risk
- Risk score: 0.29 (low risk band: below 0.40). The model never saw this customer during training.

## Plan (decided in code from the playbook and the discount policy)
- **Contact:** Yes, priority 2 (complained in the last month, whatever the score). Customers who complained in the last month are contacted regardless of their low churn risk score, prioritizing complaint resolution. [retention_playbook.md > Who we contact first]
- **Channel:** Follow-up by the support team to close the complaint. Low risk customers with recent complaints receive follow-up by the support team to close the complaint, with no retention offer. [retention_playbook.md > Channels]
- **Frequency:** At most twice in 14 days. The playbook limits contact frequency to at most twice in 14 days to avoid customer fatigue. [retention_playbook.md > Channels]
- **Complaint:** Close the complaint before any coupon or offer. The policy mandates closing complaints before offering coupons, as unresolved complaints with coupons increase churn. [retention_playbook.md > Customers who complained]
- **Offer:** None: offers to customers below 0.40 are not funded. Offers are not funded for customers with a risk score below 0.40, so no discount is provided to this low-risk customer. [discount_policy.md > Offers that need extra care]

## Do not
- Do not tell the customer their churn score [retention_playbook.md > What we never do]

## Market now (last 48 hours)
- [Oppo Find X10 review: The competition, our verdict, pros and cons](https://news.google.com/rss/articles/CBMiZ0FVX3lxTE5RMWZhb1lXTXRuUHdEbVMyZFZKcUxNZ183bGtleU43RkxSZk1MWmsxN05TWVF2VU52LVJONlN4bi1kQmRhWkx2TmU4dXVtQ05vQ25nbXZDLWlVSGNHLWs5Z0xCeW5jTEU?oc=5), GSMArena.com, 2026-10-31 02:24 UTC. New smartphone reviews highlight competitive features that may influence this customer's interest in mobile products.
- [Why Google’s Pixel 11 Pro Holds Firm Beside Galaxy S26 Ultra and iPhone 18 Pro](https://news.google.com/rss/articles/CBMijgFBVV95cUxNQm1XNm1xVTMxdElkMy01eFg4Mk9fc2VkdjE0Y2JpSld0LV9Zb1VfZE8zeG1NVnhEeDdRRnVENGh3Z3dTLWIwUzVJTlN4RjFLUERHckJzSmxTWTlIYjl6ZDlyVDM0OEFBT1pXS09XX0t3MnIzMXpTeEJidDF0VHBCNkQ3d1pTR1E3NlBNTVdn?oc=5), TechEBlog -, 2026-10-30 22:52 UTC. Google Pixel 11 Pro's strong market position may affect customer retention in the mobile category.
- [Samsung Galaxy Z series foldables are breaking pre-order records in the US and Korea](https://news.google.com/rss/articles/CBMijgFBVV95cUxPTGRzVU5HUkpWQlpMLW41Y210Mlk1TXJlbEstTFh2TDZnSWhjejlZcTk5YjF5TERBdUt5dDAxUWZUVmtLaVp6STg5LU4xRGdLWGxuTVBvQ1h1ZEpCZ08tTFZqMEFobHNNNWoyaTIzdE9GQWlwLUpvbGtnRldMRnB4S2didmt6eW93MnRxOXVB?oc=5), Mashable, 2026-10-30 22:00 UTC. Record pre-orders for Samsung Galaxy Z foldables indicate strong consumer interest in premium mobile devices.

## Sources
[discount_policy.md > Offers that need extra care] · [retention_playbook.md > Channels] · [retention_playbook.md > Customers who complained] · [retention_playbook.md > What we never do] · [retention_playbook.md > Who we contact first]
