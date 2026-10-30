# Retention Briefing for Customer 50471

## Customer snapshot
- Tenure: 20.0 months
- Complaint flag: 1 (complained in last month)
- Preferred Payment Mode: Debit Card
- Preferred Order Category: Others
- Satisfaction Score: 4
- Days Since Last Order: 8.0
- Order Count: 13.0
- Cashback Amount: 292.46 INR

## Churn risk
- Risk score: 0.77 (high risk band, high >= 0.7)
- Score note: The model never saw this customer during training (scored_out_of_sample: true)

## Recommended action
- Contact priority: This customer is high risk and has complained in the last month. According to the playbook, customers with complaints are contacted before others regardless of risk score, and high-risk customers are contacted newest first. So this customer is a top priority for outreach. [retention_playbook.md > Who we contact first]
- Contact channel: Use a phone call by a retention agent for high-risk customers. [retention_playbook.md > Channels]
- Complaint handling: Resolve the complaint fully before offering any coupon or discount. Sending a coupon while the complaint is open can increase churn. [retention_playbook.md > Customers who complained]
- After complaint resolution, consider retention offers within policy limits. [retention_playbook.md > Customers who complained]

## Offer
- Discount limits: Maximum discount per customer per month is INR 500 or 15% of the next order, whichever is lower.
- Cashback offers capped at INR 300 per customer per month, paid to wallet.
- Customer has already received cashback of INR 292.46 this month, close to the cashback cap.
- Approval levels: Retention agent can approve discounts up to INR 300; above that requires team lead approval.
- Since the customer pays by Debit Card (not COD), cashback offers are applicable.
- Only one retention offer per 30 days allowed.
- Recommend offering a coupon or cashback up to INR 300 initially, with team lead approval if higher discount is considered, but not exceeding INR 500 total discount. [discount_policy.md > Limits per customer], [discount_policy.md > Approval levels]

## Do not
- Do not offer any discount or coupon before the complaint is resolved.
- Do not exceed discount or cashback limits.
- Do not contact the customer more than twice in 14 days. [retention_playbook.md > Channels]

## Market now (last 48 hours)
- [Google's 'best smartwatch yet' just scored a historic discount, weeks before Black Friday](https://news.google.com/rss/articles/CBMiigFBVV95cUxNb0Z2S3dzOGI2NEV2TkRPRkRSSVBqNFFqVHkzcDlKSjk3YjhmbW9sbW1sdDZzNWZ1TkJ3MWttaExUQXhGdVhPb1NjdExTOVF3aUZHUzZaVGFOZEw0NzEySnBTaVNOT3J1QV9ETHFkU2hKMkNQYkp3QUEta29xa1BmMTQ0dDVvU2xZQlE?oc=5) - Android Police, 2026-10-30  
  May increase customer expectations for discounts and deals in ecommerce.
- [Klarna expands Lands’ End deal to Europe](https://news.google.com/rss/articles/CBMiowFBVV95cUxOdm5ZcDUxOVJ2YnFUTUR1NXNkS090emFzMUhHanJqZ0IxUEZDdVFldnpyWFRRWFQxclM3RjdNUjlSRDF5V05KMG14aE5vOGFsc3dlQmpFVnRxQkF2OG1IeHBwOGR1SU9WcjFBb3N6UUZYMm45TmE4ejExQmNnQ3pSZlc5MjhNX19ubERfcll6NVV4Y2VsQ25VLUlDdmRUenBnSGk4?oc=5) - The Paypers, 2026-10-30  
  Expansion of payment deals may influence customer payment preferences and retention strategies.
- [The Google Pixel 11 Pro is now cheaper than it’s ever been at Amazon](https://news.google.com/rss/articles/CBMimgFBVV95cUxNdlA0M3hlOTZQNVIzWDA5eTdyMy1yNWdFVi1Qckp3Rk9EbzdHVXNqMFJObG5GblVHcGtYTWh4Y0RwQUVZaW9GTUF2c3BNb3JKaUF2OUw5bkd5d3hVYWZySlRyMUJkb3B4X0xDSzk1LWRIcHUwNTViSTdMLURBcGt2em8xOVRYVGZ4aDhjNkZlaHNzNTN3SU04T29B?oc=5) - Android Police, 2026-10-30  
  Competitive pricing in electronics may raise customer expectations for deals in other categories.

## Sources
- [retention_playbook.md > Who we contact first]
- [retention_playbook.md > Channels]
- [retention_playbook.md > Customers who complained]
- [discount_policy.md > Limits per customer]
- [discount_policy.md > Approval levels]
- [past_campaigns.md > Campaign "Sorry We Missed" (complaints)]