# Simulated Round 275: Customer-Acknowledged Usage True-Up Cash Release Lockbox

Date: 2026-05-30 Europe/Warsaw

Current real gates: working Zero To One `>=85`; fresh Zero To One `>=85`.

## Search Bias For This Round

Recent recovery mandates failed when recoverable value was ambiguous, when platform/debtor decisions were opaque, or when collecting would damage a live customer relationship. The closest recent cash candidate was `API Usage True-Up Recovery Lockbox`, which scored 81. Its main weakness was not the cash shape; it was that many claims would be disputed, commercially waived, or relationship-damaging.

Round 275 therefore tests only payment-release files where the customer has already acknowledged the amount, signed a renewal/amendment/true-up statement, approved a PO, or issued AP/procurement acknowledgement. The startup does not argue entitlement. It converts already-acknowledged contract cash into invoice acceptance, payment scheduling, remittance, or written no-go.

## Raw Candidate Control Table

| # | Raw candidate | Buyer | Acute trigger | Transferable control point inside 60 days | Internal cap result |
|---:|---|---|---|---|---|
| 1 | Customer-acknowledged SaaS usage true-up cash release | Usage-priced B2B SaaS/API vendors | Customer accepted true-up but AP/procurement has not paid | Signed mandate, customer acknowledgement, contract, usage statement, PO/invoice/AP trail | Advance |
| 2 | Contract-backed API underbilling recovery | B2B SaaS/API vendors | Logs show unpaid overages | Vendor mandate, contract, usage logs, corrected invoice | Capped: relationship damage and ambiguous clauses |
| 3 | SaaS annual indexation arrears release | SaaS vendors | CPI/indexation was contractually missed | Contract clause, customer notification, revised invoice | Capped: customer blowback and low urgency |
| 4 | SaaS minimum-commit shortfall collection | Data/API vendors | Customer used below/above commit and owes minimum/overage | Signed contract, usage/commit statement, AP case | Capped unless customer has already accepted |
| 5 | Reseller revenue-share true-up recovery | Software vendors with channel contracts | Reseller under-reported end-customer sales | Reseller statement, agreement, corrected report | Capped: partner relationship and proof gaps |
| 6 | Referral commission cash release | Agencies/consultants owed commissions | Vendor acknowledges closed deal but unpaid commission | Referral agreement, deal registration, vendor acknowledgement | Capped: small/lumpy and legal boundary |
| 7 | Implementation milestone acceptance cash release | B2B services firms | Signed milestone acceptance but invoice unpaid | Acceptance certificate, invoice, AP trail | Capped: generic AR/AP and disputes |
| 8 | Customer-approved cloud overage rebill release | Cloud/MSP resellers | Customer approved consumption overage invoice | Consumption export, customer email, PO/invoice | Advance as backup |
| 9 | Telecom wholesale usage reconciliation release | Voice/SMS aggregators | Counterparty accepted CDR difference | CDR statement, counterparty ack, invoice | Capped: telecom trust, fraud, low margins |
| 10 | Data-license seat true-up release | Data vendors | Customer accepted seat count but AP needs evidence | Access logs, signed seat statement, invoice | Advance as backup |
| 11 | Marketplace private-offer payout release | SaaS vendors | Marketplace payout missing | Offer ID, payout report, support case | Capped: prior failed platform remittance |
| 12 | Microsoft incentive claim release | MSP/CSP partners | Visible Partner Center claim stuck | Claim IDs, POE, support case | Capped: prior failed portal incumbent path |
| 13 | Customer-acknowledged late fee / SLA offset release | SaaS vendors | Net payment due after accepted offset | Signed netting statement, invoice | Capped: low value and legal/commercial sensitivity |
| 14 | Advertising spend rebate cash release | Agencies | Platform/vendor approved rebate not paid | Approval, spend statement, vendor ack | Capped: platform/channel incumbents |
| 15 | Affiliate network approved commission cash-out | Publishers/agencies | Approved balance unpaid | Network statement, advertiser approval | Capped: small, fraud-prone, platform-controlled |
| 16 | Software maintenance reinstatement fee release | ISVs | Customer approved reinstatement/arrears | Renewal quote, signed order, invoice | Capped: generic renewal ops |
| 17 | Enterprise support usage true-up release | Support vendors | Customer consumed extra blocks and approved | Ticket/time ledger, signed statement | Capped: relationship and time-ledger disputes |
| 18 | Training seat overage invoice acceptance | B2B training vendors | Customer accepted extra learners | LMS logs, signed roster, PO | Capped: small and easy to internalize |
| 19 | API reseller pass-through tax/fee correction | API vendors | Customer accepted tax/fee correction | Contract, invoice, tax review | Capped: tax/legal boundaries |
| 20 | Cloud marketplace co-sell fee correction | ISVs | Partner acknowledged co-sell fee | Partner report, statement, claim | Capped: platform partner ops |
| 21 | OEM support credit cash release | Equipment resellers | OEM accepted support credit | OEM statement, reseller invoice | Capped: channel incumbents |
| 22 | Annual true-up amendment AP release | B2B SaaS vendors | Signed amendment exists; AP needs package | Amendment, PO, invoice, procurement trail | Advance |
| 23 | Customer-approved usage no-go audit | SaaS vendors | Candidate true-ups screened before customer contact | CFO-approved no-go/release register | Capped: report/advisory not cash movement |
| 24 | SaaS acquisition QoR true-up screen | PE/acquirers | Target may have unbilled usage | Diligence memo, contract/log review | Capped: trust-heavy diligence |
| 25 | Customer-approved renewal uplift cash release | SaaS vendors | Renewal signed, uplift invoice stuck | Signed order, AP workflow, invoice | Capped: generic collections unless usage-specific |
| 26 | Consumption-billing migration leakage lockbox | SaaS vendors migrating billing tools | Historical missed true-ups found | Old/new ledger, customer approvals | Capped: RevOps/billing consultants |
| 27 | Paid proof of customer acknowledgement register | SaaS CFOs | Need exact evidence before invoicing | Customer acceptance trail, invoice pack | Capped: service/report unless tied to cash |
| 28 | Data-provider API excess-call statement release | Data vendors | Client accepted excess-call report | Call logs, signed usage statement, PO | Advance |
| 29 | Customer-approved sandbox-to-production usage fee release | Developer tool vendors | Pilot exceeded free/pilot usage and customer approved | Pilot terms, logs, signed conversion/true-up | Capped: customer goodwill risk |
| 30 | Renewal desk for accepted true-up templates | RevOps consultants | They have signed true-ups but no AP follow-through | Partner-routed case flow, direct billing | Capped: partner can internalize |

## Finalists

| Finalist | Simulated score | Reason |
|---|---:|---|
| Customer-Acknowledged Usage True-Up Cash Release Lockbox | 88.5 | Removes the main weakness of the prior 81-point usage recovery idea: no entitlement argument before customer acknowledgement. Current cash, named AP case, and before-state proof are measurable. |
| Customer-Approved Cloud Overage Rebill Release | 86.2 | Similar cash shape but more likely to be absorbed by MSP/cloud billing teams. |
| Data-License Seat True-Up Release | 85.8 | Clearer logs but more substitutable by RevOps and legal teams. |
| Annual True-Up Amendment AP Release | 85.0 | Clean payment proof, but too generic without the metered-usage wedge. |
| Data-Provider API Excess-Call Statement Release | 84.6 | Good niche but too close to generic usage true-up. |
| Reseller Revenue-Share True-Up Recovery | 82.0 | Relationship and legal proof gaps remain too high. |

## Selected Candidate

**Customer-Acknowledged Usage True-Up Cash Release Lockbox**

## Internal Simulation

### Why It Could Clear

- It is not a speculative audit. Entry requires customer acknowledgement, signed amendment/order form, AP/procurement acknowledgement, or customer-approved usage statement.
- It directly addresses the prior `API Usage True-Up Recovery Lockbox` objections: the founder does not surprise the customer, interpret ambiguous clauses, or decide if the vendor should pursue the claim.
- The first proof is cash movement: AP acceptance, payment schedule, remittance, bank receipt, or written no-go after an acknowledged true-up.
- The buyer pain is high when a 100,000+ PLN signed usage true-up sits between CFO, RevOps, sales ops, procurement, and customer AP.
- Founder fit is stronger than technical service queues: structured contract/usage/invoice evidence, AP wording, before-state tracking, and no production access.

### Internal Objections

- Clean acknowledged cases may be easy enough for CFO/AR teams to handle.
- If cases are not truly acknowledged, it falls back into the failed usage-recovery branch.
- Customer AP may ignore a third-party coordinator.
- RevOps, billing-platform consultants, fractional CFOs, and finance ops teams can copy.
- Some "acknowledged" amounts can still be delayed by PO mismatch, budget owner turnover, procurement policy, tax, legal-entity mapping, or relationship politics.

### Internal Caps Applied

- Capped below 82 for any lead without customer-side acknowledgement or signed amendment/order form.
- Capped below 85 if the buyer is asking for revenue leakage audit, pricing design, billing implementation, or contract interpretation.
- Capped below 87 if payment proof is only "identified value" rather than AP acceptance, scheduled payment, remittance, bank receipt, or written no-go.
- Capped below 87 unless minimum acknowledged receivable is at least 100,000 PLN per customer or a bundled queue exceeds 300,000 PLN.

Internal simulated score: **88.5 / 100**

Advance to working-chat Zero To One validation because simulated score is strictly above 87 and the candidate materially tightens the strongest recent cash-control branch by requiring customer acknowledgement before the startup touches the file.
