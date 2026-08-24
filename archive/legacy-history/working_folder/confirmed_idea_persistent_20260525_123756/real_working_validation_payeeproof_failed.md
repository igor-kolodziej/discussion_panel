# Real Working-Chat Validation: PayeeProof Failed

Created: 2026-05-25

## Idea Sent

PayeeProof Polish VoP Benchmark And Pre-Check. Non-euro PSPs face SEPA instant Verification of Payee duties in 2027, but Polish legal names, sole proprietor names, NIP/KRS variants, diacritics, and invoice/payee mismatches create false positives. PayeeProof secures rights-cleared historical payment mismatch logs from accounting offices and small PSPs plus synthetic edge cases, then sells benchmark/pre-check APIs. The 2-month proof target is 3-5 data-contribution agreements, 10,000 named edge cases, two paid pilots or committed paid evaluations, and measured false-positive reduction versus public registry/string matching.

Simulated Zero To One-style score: **88/100**.

## Real Working-Chat Score

Real working-chat Zero To One score: **74/100**.

## Key Objections

- The regulatory trigger is real, but the product may be non-authoritative: final VoP responses are generated through PSP/RVM infrastructure and payee PSP records.
- The control point is plausible but fragile. It is not obvious that an unknown solo founder can secure, license, label, and prove a useful rights-cleared mismatch corpus in 2 months.
- Anonymization may destroy the value of the corpus because the valuable signal is in real names, aliases, account-holder strings, NIP/KRS/CEIDG fields, and outcomes.
- Accounting offices may not have the right labels: invoice names and aliases do not necessarily include bank-account-holder strings or verified false-positive/false-negative outcomes.
- Existing VoP/RVM vendors are already active and can capture the infrastructure layer.
- Paid pilots are possible but aggressive because regulated buyers have slow procurement, legal, vendor-risk, and data-sharing processes.
- If public registry normalization plus Polish string rules solve most cases, the proprietary corpus becomes a nice dataset, not a company.

## Useful Pivot Direction From Feedback

The strongest narrowed version is not "VoP compliance" or a broad API. It is:

**Polish VoP false-warning reduction and payee-name data-quality benchmark for payment-workflow vendors and PSPs preparing for 2027.**

The real gate still failed because this remains the same fragile data-rights shape unless the founder can actually secure:

- 3 contribution/licensing agreements;
- 10,000 useful labeled/name-variant cases;
- one paid pilot collected plus one signed LOI/prepaid evaluation;
- measured reduction in false positives against a public-registry/string baseline.

## Decision

Do not write a confirmed idea file for PayeeProof. Do not send to fresh-chat validation. The real working-chat score is below the required `>=82` threshold.

Continue the persistent search with a materially different control point. Avoid similar data-benchmark ideas unless the first resource is already a signed, exclusive, buyer-funded corpus or live transaction feed.
