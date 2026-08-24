# Simulated Round 142: VoP Go-Live Evidence Pack

Created: 2026-05-29

Real browser gate: working Zero To One `>=85`, fresh Zero To One `>=85`.

## Source Facts Checked

- Regulation (EU) 2024/886 on instant credit transfers requires payment service providers to offer verification of payee / payee verification services on a phased timetable.
- The European Payments Council launched the Verification Of Payee scheme and rulebook to support compliance with the Instant Payments Regulation.
- Non-euro area PSP timing extends beyond the first euro-area deadlines, making 2026-2027 procurement and go-live work still relevant for CEE payment vendors.

Sources used:

- https://eur-lex.europa.eu/eli/reg/2024/886/oj
- https://www.europeanpaymentscouncil.eu/what-we-do/verification-payee
- https://www.europeanpaymentscouncil.eu/news-insights/news/european-payments-council-launches-verification-payee-vop-scheme

## Raw Candidate Sweep

| # | Raw candidate | Buyer / payer | Acute trigger | Transferable control proof | Internal cap |
|---:|---|---|---|---|---:|
| 1 | VoP go-live evidence pack for payment vendors | Payment software/name-matching vendors selling to PSPs | PSP procurement/go-live blocked by VOP evidence/test questions | Live PSP request, test logs, response matrix, submitted pack | 88 |
| 2 | VoP bulk-payment exception release desk | Corporate AP teams | Supplier-name mismatches pause payment runs | Exception batch and supplier confirmations | 68 |
| 3 | Instant-payments reachability test file | PSP vendors | SCT Inst go-live tests | Test evidence pack | 82 |
| 4 | ISO 20022 bank-message migration pack | ERP/payment vendors | Bank format cutover | Test files and bank feedback | 75 |
| 5 | PSD3 SCA evidence pack | Fintech vendors | Customer asks for SCA/fraud controls | Evidence room | 78 |
| 6 | SEPA rulebook dispute evidence | PSP ops teams | Scheme issue | Case file | 70 |
| 7 | Payment fraud false-positive diligence | Fintech buyers | Procurement decision | Test data and model memo | 76 |
| 8 | AML transaction-monitoring tuning evidence | Fintech vendors | Bank review | Reviewer pack | 74 |
| 9 | DORA renewal evidence pack | ICT vendors to finance | Bank renewal blocker | Confirmed prior idea | Already confirmed |
| 10 | NIS2 OT supplier pack | OT vendors | Customer renewal blocker | Failed at 78 | 78 |
| 11 | KSeF invoice payment release | Suppliers/AP | AP hold | Failed at 79 | 79 |
| 12 | KSeF connector acquisition | Merchants | Tax system update | Failed around 82 | 82 |
| 13 | Cloud marketplace remittance recovery | SaaS vendors | Payout mismatch | Failed at 64 | 64 |
| 14 | Grant payment release | Grant recipients | Claim stuck | Failed at 76 | 76 |
| 15 | LC discrepancy payment release | Exporters | LC payment held | Failed at 74 | 74 |
| 16 | CBAM broker import continuity | Brokers/importers | Import continuity | Confirmed prior idea | Already confirmed |
| 17 | EUDR order-release file | Wood/furniture exporters | Buyer evidence request | Failed at 74 | 74 |
| 18 | AI voice-agent diligence | Investors/procurement | Live claim decision | Failed at 76 | 76 |
| 19 | LiftLog Data Act tender file | Property managers/lift firms | Maintenance rebid | Failed at 69 | 69 |
| 20 | Payment processor reserve release | Ecommerce merchants | Funds held | Opaque processor case | 72 |
| 21 | Chargeback representment recovery | Merchants | Chargebacks | Existing incumbents | 68 |
| 22 | BNPL merchant settlement recovery | Ecommerce merchants | Payout discrepancy | Platform case | 65 |
| 23 | Open Banking API conformance pack | Fintech vendors | Bank procurement | Test logs | 78 |
| 24 | eIDAS wallet relying-party evidence pack | App vendors | Wallet integration | Too early | 74 |
| 25 | Fraud-model explainability evidence pack | Vendors to banks | Procurement blocker | Evidence matrix | 79 |
| 26 | PCI DSS v4.0 SAQ remediation pack | Ecommerce merchants | Acquirer asks | QSA/advisers dominate | 73 |
| 27 | Open finance consent audit pack | Fintech vendors | Customer review | Evidence room | 74 |
| 28 | SWIFT CSP evidence pack | Bank vendors | Annual assurance | Enterprises/advisers | 72 |
| 29 | EU AI Act bank chatbot release | AI vendors to finance | Customer go-live | Adjacent/fail | 78 |
| 30 | Bank outsourcing register-data pack | Vendors to finance | Bank register evidence | DORA duplicate | 82 |

## Selected Candidate

**VoP Go-Live Evidence Pack**

Internal simulated score: `88 / 100`

## Why It Can Clear Simulation

This is not AP exception handling. The buyer is a payment-software or name-matching vendor with a live PSP customer go-live, procurement, or renewal blocked by Verification of Payee evidence. The proof artifact is testable and current: PSP question list, API/test logs, response-code matrix, matching-threshold explanation, availability/latency evidence, audit/logging and exception-handling evidence, submitted pack, and customer progress.

It is adjacent to DORA because the buyer is still financial-sector software, but the control artifact is not operational-resilience evidence. It is a scheme/regulatory go-live response pack around a specific payment product deadline.

## Internal Cap Notes

Why not higher:

- Payments consultants, EPC scheme specialists, core-banking vendors, payment processors, and large regtech firms are credible.
- A solo unknown founder needs named payment-scheme/API reviewer credibility.
- PSP customer approval and production testing are outside founder control.
- If vendors lack real test logs or controls, the pack becomes a gap/no-go memo.
- DORA duplicate risk is non-trivial because the commercial shape is another regulated-finance vendor evidence pack.

## Gate Decision

The simulated score is strictly above 87, so write a clean Zero To One prompt and submit to the working chat.
