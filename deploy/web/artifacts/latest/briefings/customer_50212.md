# Retention briefing: customer 50212

Customer 50212 is a medium-risk churn customer who complained in the last month and prefers the Mobile category. The main retention focus is to close the complaint before offering any discount or coupon.

## Customer snapshot
- Tenure missing · Complain 1 · PreferredPaymentMode UPI · PreferedOrderCat Mobile · SatisfactionScore 5 · DaySinceLastOrder 7.0 · OrderCount 1.0 · CashbackAmount 121.19

## Churn risk
- Risk score: 0.67 (medium risk band: 0.40 to 0.70). The model never saw this customer during training.

## Plan (decided in code from the playbook and the discount policy)
- **Contact:** Yes, priority 2 (complained in the last month, whatever the score). Customers who complained in the last month are contacted regardless of their risk score, as they are a high priority. [retention_playbook.md > Who we contact first]
- **Channel:** App push notification, then email after 2 days without response. Medium risk customers are contacted first by app push notification, then by email if no response after 2 days. [retention_playbook.md > Channels]
- **Frequency:** At most twice in 14 days. Customers are contacted at most twice in 14 days to avoid over-contacting and potential annoyance. [retention_playbook.md > Channels]
- **Complaint:** Close the complaint before any coupon or offer. The playbook mandates closing the customer's complaint before any coupon or offer is given to avoid increasing churn. [retention_playbook.md > Customers who complained]
- **Offer:** Only after the complaint is closed. Offers are only made after the complaint is resolved, following the 'resolve before you reward' rule. [retention_playbook.md > Customers who complained]
- **Offer type:** Discount or wallet cashback within the limits. Discounts or wallet cashback are allowed within policy limits to retain customers effectively. [discount_policy.md > Limits per customer]
- **Limits:** Up to INR 500 or 15% of the next order, whichever is lower; cashback up to INR 300; one offer per 30 days. Discounts are limited to INR 500 or 15% of the next order, cashback up to INR 300, and one offer per 30 days. [discount_policy.md > Limits per customer]
- **Approval:** Agent up to INR 300; team lead for INR 301 to 500; never above INR 500. Retention agents can approve offers up to INR 300; higher amounts require team lead approval, never exceeding INR 500. [discount_policy.md > Approval levels]

## Do not
- Do not tell the customer their churn score [retention_playbook.md > What we never do]

## Market now (last 48 hours)
- [All the phones T-Mobile is giving away for free: Shop iPhone 17, Samsung Galaxy Z Fold 8, and Google Pixel 11](https://news.google.com/rss/articles/CBMilwFBVV95cUxOM3R4UVpTQ3VETVVrR1JRODkwaW9SMFFORGJpU2ZieC1udFJuakxXTVVpRHZ1TGI5eV9YelVrM0NVZVkwLWtpSmFtY2ExXzhGLTJpS1lzU3pQTmdIMGsxUlR5RGl6Z2VsdDVocGtzWG5yUG10VG5uVzVIbWJJSm9hWmFXRVZBUTMxUWNhTXpVSGFkLXB1dXhV?oc=5), Mashable, 2026-10-30 22:00 UTC. T-Mobile's free phone giveaways may increase competitive pressure on this mobile-preferring customer.
- [Apple announces iPhone 18 Pro and iPhone 18 Pro Max with major camera upgrades](https://news.google.com/rss/articles/CBMifkFVX3lxTE1YVmViNGNPMllaa0J5cFpzRGkxcHUyMjFJZTRXbENGaXdwUDk5azJnMFQyNHRhOU00ejdwek91ZnR1T0FHUDhiNnNSUWlGNEJ4ZUNNOWdrQS1wTlU5aUV0VmpXeTBVcXlxVktUbG54OTl6MVJ3S3hfTXluQk9YUQ?oc=5), Mashable, 2026-10-30 22:00 UTC. Apple's new iPhone 18 Pro launch could influence this customer's purchase decisions in the Mobile category.
- [Why Google’s Pixel 11 Pro Holds Firm Beside Galaxy S26 Ultra and iPhone 18 Pro](https://news.google.com/rss/articles/CBMijgFBVV95cUxNQm1XNm1xVTMxdElkMy01eFg4Mk9fc2VkdjE0Y2JpSld0LV9Zb1VfZE8zeG1NVnhEeDdRRnVENGh3Z3dTLWIwUzVJTlN4RjFLUERHckJzSmxTWTlIYjl6ZDlyVDM0OEFBT1pXS09XX0t3MnIzMXpTeEJidDF0VHBCNkQ3d1pTR1E3NlBNTVdn?oc=5), TechEBlog -, 2026-10-30 22:52 UTC. Google Pixel 11 Pro's strong market position may affect this customer's brand preference in smartphones.

## Sources
[discount_policy.md > Approval levels] · [discount_policy.md > Limits per customer] · [retention_playbook.md > Channels] · [retention_playbook.md > Customers who complained] · [retention_playbook.md > What we never do] · [retention_playbook.md > Who we contact first]
