# Retention Briefing for Customer 50212

## Customer snapshot
- Tenure: unknown
- Complaint flag: 1 (complained in last month)
- Preferred payment mode: UPI
- Preferred order category: Mobile
- Satisfaction score: 5
- Days since last order: 7.0
- Order count: 1.0
- Cashback amount: INR 121.19

## Churn risk
- Risk score: 0.67 (medium risk band)
- Score is out of sample; the model never saw this customer during training.

## Recommended action
- Contact priority: This customer should be contacted because they have a complaint in the last month, which takes precedence over the medium risk score [retention_playbook.md > Who we contact first].
- Contact channel: Use app push notification first, then email after 2 days if no response. Do not call as the risk is medium [retention_playbook.md > Channels].
- Complaint handling: Resolve the complaint fully before offering any coupon or reward. Sending a coupon before complaint resolution may increase churn [retention_playbook.md > Customers who complained].
- Since the customer prefers Mobile category, consider category-specific retention tactics after complaint resolution [retention_playbook.md > Customers who complained].
- Do not exceed one retention offer per 30 days and respect discount limits [discount_policy.md > Limits per customer].

## Offer
- No offer should be made until the complaint is resolved [retention_playbook.md > Customers who complained].
- After resolution, retention offers must comply with discount limits: max INR 500 or 15% of next order, whichever is lower; cashback capped at INR 300 [discount_policy.md > Limits per customer].
- Approval needed for offers above INR 300; up to INR 300 can be decided by the retention agent [discount_policy.md > Approval levels].
- For Mobile category customers, consider extended warranty on next phone accessory order as it reduced churn by 5 percentage points in past campaigns [past_campaigns.md > Campaign "Mobile Upgrade" (mobile phone buyers)].
- No free delivery vouchers or COD-specific offers apply here as payment mode is UPI.

## Do not
- Do not offer a coupon or discount before complaint resolution [retention_playbook.md > Customers who complained].
- Do not contact more than twice in 14 days [retention_playbook.md > Channels].
- Do not offer discounts outside policy limits or without required approvals [discount_policy.md > Limits per customer].

## Market now (last 48 hours)
- [Google Pixel 11 Pro Unlocked Smartphone sees price cut to $799](https://news.google.com/rss/articles/CBMimAFBVV95cUxOZXF6V0lWM2NtRWhzWWx5ZExvY05STnhjcTI0NUVCWmlXWVdub0NldTRwY1JpQUw2NnZyTUZkV1hJYXNlQjNwRkZnVEpub3FjOGdhNm5uWUZRNDRjV3VLQml4M3laRW5PVFBfajJlSnYwVjBBQzFTSHJSR3BjT3dldU9SUWtXeExCZk9NWXVpaUMxZUp5LXJnOQ?oc=5) - Technobezz, 2026-10-30: Competitors are discounting smartphones, increasing pressure on Mobile category retention.
- [DoorDash to Buy Instacart in $17bn Grocery Deal](https://news.google.com/rss/articles/CBMifEFVX3lxTFBCWDdMRTZoS2ZxRWRSSGhoa19YVlJtSmFKMXptd2M3dDdHdGpEQ1ViVi1XY2dEQTZWaWVWTkVBRWJDNExnWGZ2NU1EcmtyZU8ycE9lOVlpZTl2b0c5V1R0WGNIS1lzTUtkeWtCTWxiWEQtdlRvd1RpWXBIX2E?oc=5) - Grocery Trade News, 2026-10-30: No direct impact on Mobile category but indicates competitive market activity.
- [Google Pixel 11 Pro Fold Unlocked Smartphone now $1649, down from $1899](https://news.google.com/rss/articles/CBMiogFBVV95cUxOUUo4cklseXYyZDdxX1h4M2tkQ1FiQVhlUXdfcWlTcEhGT3g1UVAyeUxTVllCeGZ4V2hvc1Z6X1hSV1RkUkR1eWxZYV96ZDNkNnR0TDNiaWRIaXBOSXFkb013dEQteEd5WFRqcC10eVJfNDJ6aHNaZ0gwaVg4bkZhZEFzay1iNGdiSW0yOG1VZmFrN0FnVGUwSDRCcWxlWDNPR1E?oc=5) - Technobezz, 2026-10-30: Further smartphone price reductions may increase churn risk in Mobile category.

## Sources
- [retention_playbook.md > Who we contact first]
- [retention_playbook.md > Channels]
- [retention_playbook.md > Customers who complained]
- [past_campaigns.md > Campaign "Mobile Upgrade" (mobile phone buyers)]
- [discount_policy.md > Limits per customer]
- [discount_policy.md > Approval levels]