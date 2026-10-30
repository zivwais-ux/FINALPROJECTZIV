# Retention Briefing for Customer 50230

## Customer snapshot
- Tenure: 3.0 months
- Complaint flag: 1 (complained in last month)
- Preferred payment mode: COD (Cash on Delivery)
- Preferred order category: Laptop & Accessory
- Satisfaction score: 3
- Days since last order: 2.0
- Order count: 2.0
- Cashback amount: 147.36

## Churn risk
- Risk score: 0.51 (medium risk band)
- Score note: The model never saw this customer during training (scored_out_of_sample: true)

## Recommended action
- Contact priority: Customers who filed a complaint in the last month are contacted before medium risk customers regardless of score [retention_playbook.md > Who we contact first].
- Contact channel: For medium risk customers, use app push notification first, then email after 2 days without response. Do not exceed two contacts in 14 days [retention_playbook.md > Channels].
- Complaint resolution: Resolve the customer's complaint first before offering any coupon or reward. Sending coupons before complaint resolution may increase churn [retention_playbook.md > Customers who complained].
- Complaint handling: Support agents must close the complaint before retention team offers coupons [retention_playbook.md > Customers who complained].
- Payment mode considerations: Since the customer pays COD, cashback offers are ineffective. Use free-delivery vouchers or a small discount printed on the next invoice instead. Encourage but do not require switching to UPI or card payment [retention_playbook.md > Cash on delivery (COD) customers].

## Offer
- Maximum discount per customer per month is INR 500 or 15% of the next order, whichever is lower [discount_policy.md > Limits per customer].
- Cashback offers capped at INR 300 per month and paid to wallet, not applicable for COD customers [discount_policy.md > Limits per customer].
- Free delivery vouchers are preferred for COD customers [discount_policy.md > Offers that need extra care].
- Approval levels: Up to INR 300 discount can be decided by the retention agent; INR 301 to 500 requires team lead approval [discount_policy.md > Approval levels].
- No discount offers in Grocery category (not applicable here) [discount_policy.md > Offers that need extra care].
- Only one retention offer per 30 days allowed [discount_policy.md > Limits per customer].

## Do not
- Do not offer coupons or discounts before the complaint is resolved [retention_playbook.md > Customers who complained].
- Do not use cashback offers for COD customers [retention_playbook.md > Cash on delivery (COD) customers].
- Do not contact the customer more than twice within 14 days [retention_playbook.md > Channels].

## Market now (last 48 hours)
- [HP Ryzen 9 8945HX and RTX 5070 gaming laptop with OLED display drops by 18% with Amazon offer](https://news.google.com/rss/articles/CBMiwAFBVV95cUxPa1ZYXy1QRFlKVUNCX3VoN01tTXlsazVoVjd5NTYxZGp6bGtjMU5SeDhIeTBodk54azIweDZ2VUFNNDJtY1U0aTRhZ2hIWjRyeGFPbVgwOERMNkRNVUpUbm5zVjJsTnhsaS1vaWg2LUNxNTFnaXlSanpPQllEeUJkSnlFVUN2Z2hiZ3VIMlQ5NWpnNjJ0RDJMNVVUczIwV2tyUy15amtXcmpCdWJRYjI5TTFWV0ttbEx2RVVpZGU3Qmg?oc=5) (PC Guide, 2026-10-30)  
  May increase customer interest in laptops and accessories category.
- [Upgrade for Less: Save Over $350 Off This Powerful Lenovo Laptop Today](https://news.google.com/rss/articles/CBMilgFBVV95cUxOS2tlX3FVUTh2b1Z2QWdxV1RhcWVjU0xrbDdxTkY4TVhOcTRzd20yNHoxOENqWjN0cEUzUEd2RWxPRHZfRjIwSFYzMVdYUGZIM3hfMTVCc2dleWIycUNHXzFiQXRUMTh1MzJSWGNMUXFLV0FWaXJKX0FQSXNTRWhzdVVWY1RlZm9CUzdJalFTajF0cU1lbHc?oc=5) (PCMag, 2026-10-30)  
  Competitive pricing on laptops could influence retention positively if matched.
- [These 2 laptop deals start at $417.99 for Lenovo and Microsoft models](https://news.google.com/rss/articles/CBMiogFBVV95cUxPaEo2Vl9zUlBvSmJ4WFJEcE9EUlYyTk1ZSmtSek1vZDdOczdGRW9BS1VEWDZmMk5qRllHT1ZMVzdOUG04SHptOGlFZkhLc2ptNHpYNk5ULXRoWXFGUEhRUWhpaEZROVhmaWdkRFlJOElILU5BekZzaEpHeWZmMmpxX3ZWUlI1MHNZaEpIS192cE0zcHB5aGM4TU5uVXN6V0xSNEE?oc=5) (Technobezz, 2026-10-30)  
  More laptop deals in the market may increase churn risk if Harbor & Vale does not remain competitive.

## Sources
- [retention_playbook.md > Who we contact first]
- [retention_playbook.md > Channels]
- [retention_playbook.md > Customers who complained]
- [retention_playbook.md > Cash on delivery (COD) customers]
- [discount_policy.md > Limits per customer]
- [discount_policy.md > Approval levels]
- [discount_policy.md > Offers that need extra care]