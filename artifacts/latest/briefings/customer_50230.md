# Retention Briefing for Customer 50230

## Customer snapshot
- Tenure: 3.0 months
- Complaint flag: 1 (complained in last month)
- Preferred Payment Mode: COD (Cash on Delivery)
- Preferred Order Category: Laptop & Accessory
- Satisfaction Score: 3
- Days Since Last Order: 2.0
- Order Count: 2.0
- Cashback Amount: 147.36 INR

## Churn risk
- Risk score: 0.51 (medium risk band)
- Score note: The model never saw this customer during training (scored_out_of_sample = true)

## Recommended action
- Contact priority: This customer is prioritized after customers with complaints and those with risk score ≥ 0.7. Since they have complained in the last month, they are a high priority for contact [retention_playbook.md > Who we contact first].
- Contact channel: Use app push notification first, then email after 2 days if no response. Do not exceed two contacts in 14 days [retention_playbook.md > Channels].
- Complaint resolution: Resolve the customer's complaint before offering any coupon or reward. Sending coupons before complaint resolution can increase churn [retention_playbook.md > Customers who complained].
- For COD customers, cashback is not applicable. Use free delivery vouchers or a small discount printed on the next invoice. Encourage switching to UPI or card payments but do not require it [retention_playbook.md > Cash on delivery (COD) customers].

## Offer
- Since the complaint must be resolved first, no offer should be made until then [retention_playbook.md > Customers who complained].
- After complaint resolution, a free delivery voucher or small invoice discount can be offered, respecting the discount limits.
- Discount limits: Maximum INR 500 or 15% of the next order, whichever is lower. Only one retention offer per 30 days allowed [discount_policy.md > Limits per customer].
- Approval levels: Up to INR 300 discount can be approved by the retention agent; INR 301 to 500 requires team lead approval [discount_policy.md > Approval levels].
- Free delivery vouchers are preferred for COD customers [discount_policy.md > Offers that need extra care].

## Do not
- Do not offer cashback to this COD customer [retention_playbook.md > Cash on delivery (COD) customers].
- Do not send coupons or rewards before the complaint is resolved [retention_playbook.md > Customers who complained].
- Do not contact more than twice within 14 days [retention_playbook.md > Channels].

## Sources
- [retention_playbook.md > Who we contact first]
- [retention_playbook.md > Channels]
- [retention_playbook.md > Customers who complained]
- [retention_playbook.md > Cash on delivery (COD) customers]
- [discount_policy.md > Limits per customer]
- [discount_policy.md > Approval levels]
- [discount_policy.md > Offers that need extra care]