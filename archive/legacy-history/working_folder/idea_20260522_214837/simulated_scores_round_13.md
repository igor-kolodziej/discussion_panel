# Simulated Scores Round 13 - KSeF Churn Shield

## Idea Scored

KSeF Churn Shield is a 7-business-day failure-drill and customer-evidence pack for Polish vertical SaaS vendors whose customers now issue or receive mandatory KSeF invoices through their product and are opening support tickets, threatening churn, delaying renewal, or refusing onboarding because invoice flows fail or feel unsafe. The first beachhead is not generic ERP, not big accounting systems, and not tax consulting. It is 10-80 person Polish vertical SaaS vendors in categories such as clinic/veterinary systems, field-service software, property-management tools, gym/membership systems, e-commerce/warehouse tools, B2B service CRMs, and appointment/POS systems. These vendors have enough customers to suffer KSeF support pain but are often too small to have mature compliance QA, incident-response evidence, and accountant-facing runbooks. The product activates only on a live KSeF integration trigger: schema or FA(3) validation failures, token/certificate/authorization expiry, failed sends or UPO/status confusion, offline/outage fallback uncertainty, correction/advance/final invoice edge cases, buyer NIP or customer-master-data mismatches, accounting-office export/import confusion, or customer asks for proof/runbook before renewal/onboarding. The founder ingests anonymized KSeF XMLs, API status/error logs, support tickets, sandbox scripts, and customer/accountant objections. Deliverable: vendor-specific failure-mode map, reproducible KSeF regression test suite, support triage macros, customer-facing runbook, accountant handoff FAQ, incident-drill report usable in renewal/onboarding, monitoring checklist, and explicit not-supported/tax-adviser-required edge-case list. It is not KSeF implementation, tax advice, legal advice, generic compliance consulting, or a dashboard. It sells reduced churn/support load and renewal evidence for software vendors with live KSeF pain. Pricing: 8,000-18,000 PLN urgent drill, 2,500-6,000 PLN/month aftercare. Primary control point: privileged access to anonymized live vendor support logs, customer objections, KSeF XML/API failures, reusable scripts, and accepted proof artifacts from multiple vertical SaaS workflows. Two-month proof: 3 paid urgent drills, 200 anonymized error/status/support cases, one reusable FA(3)/KSeF failure corpus and regression harness per vertical, one aftercare retainer, and one documented customer renewal/onboarding/accounting-office handoff unblocked.

## Scores

- Boole: `80/100`
- Kant: `76/100`
- Pasteur: `74/100`

## Common Objections

- The acute KSeF pain may decay after the 2026 rollout unless the product becomes a durable recurring evidence layer.
- Data access to live XMLs, logs, support tickets, and customer objections is the bottleneck.
- "Not tax advice" is a fragile boundary because correction, advance/final invoices, offline mode, and accountant handoffs can become interpretive.
- KSeF API/gateway/infrastructure vendors can copy the report using deeper telemetry.
- "Vertical SaaS" is still too broad; one vertical would be needed for first execution.

## Decision

Failed the lowered `82` simulated threshold. Do not send to real Zero To One. The shape is profitable but not defensible enough: it needs a deeper owned workflow than a post-integration failure drill.
