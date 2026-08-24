# Level-2 D-009 — Continuous Freight Invoice Contract Audit

## Problem And Payer Evidence

The operational problem is real: freight invoices combine base rates, fuel formulas, accessorials, shipment attributes, contract-specific discounts, classifications, currencies, and changing calculation rules. UPS, for example, states that its express LTL fuel surcharge is a separate freight-bill item calculated as a percentage of net line-haul charges, while other air-freight surcharges can be per-pound, origin/destination dependent, and periodically updated. Rate increases can also change terms, definitions, and calculation methods, not merely headline prices. This verifies charge complexity, but higher or more numerous surcharges do not establish that carriers billed them incorrectly. [UPS surcharge documentation](https://www.ups.com/us/en/supplychain/tools/surcharges)

The immediate payer is the shipper or forwarder employee accountable for transportation spend—normally a finance controller, procurement lead, transport manager, or outsourced-finance provider. A practical initial segment is a European forwarder or shipper processing at least 100 invoices monthly or roughly €0.5 million or more of annual freight spend. The number of European organizations satisfying that definition is not publicly established by the researched sources; therefore the payer denominator is unknown. Older industry documentation confirms that established freight-audit-and-payment providers have operated in Europe and handled large transaction volumes, but it does not give a current count of reachable SME payers. [Freight audit provider guide](https://www.controlpay.com/assets/files/market_guide_for_freight_aud_308345.pdf)

Direct willingness proxies exist:

- VaernFlow advertises European freight-invoice auditing from €299 per month plus an 8–15% contingency fee, with a €699-plus-12% example for its Pro service. Its stated recovery and time-saving figures are vendor claims, not independently verified customer outcomes. [VaernFlow](https://www.vaernflow.com/)
- Trazai publishes $199 per month for up to 100 invoices, $499 for up to 300, and a 35% fee on recovered amounts. This is a Latin American offer, so it verifies a transaction structure rather than European acceptance. [Trazai pricing](https://trazai.lat/)
- Flatworld advertises post-audit work beginning at $10 per page. Its claimed “one in nine” adjustment incidence lacks a disclosed representative denominator and should not be used as an error-rate estimate. [Flatworld post-audit service](https://www.flatworldsolutions.com/logistics/freight-bill-post-audit.php)
- A direct European case description from Kloepfel says a client used 1.5 FTEs for manual freight-invoice auditing, later reduced to 0.5 FTE, and reported savings equal to 3% of processed freight volume. It is a single vendor-authored case, not a population recovery rate. [Kloepfel case study](https://kloepfel-consulting.com/en/case-study/outsourcing/)

The closest substitutes are internal spreadsheet review, accounts-payable matching, a transport-management system, carrier-specific invoice portals, procurement consultants, and established freight-audit-and-payment providers. An incumbent route-around is to renegotiate tariffs, require structured EDI invoices, impose purchase-order controls, or outsource the complete audit-and-payment workflow. These measures can prevent leakage without purchasing a separate continuous contract-audit layer.

## Proposed Transaction

The paid event is each invoice processed against the customer-authorized contract, rate card, and shipment evidence, with a separate outcome fee only for a credit confirmed by the carrier and attributable to a documented variance.

A plausible initial commercial range is:

- Historical, manually assisted pilot: 5–15 PLN per invoice, with a 1,500–5,000 PLN minimum for a 90-day file.
- Recurring structured audit: 2–8 PLN per invoice, normally subject to a 600–2,000 PLN monthly minimum.
- Optional outcome component: 8–15% of credits actually confirmed, not merely flagged, with a negotiated monthly cap.
- Complex contract onboarding: approximately 1,500–8,000 PLN per carrier-rate structure if normalization cannot be recovered through the recurring fee.

These are interpreted ranges derived from published substitute pricing, not verified Polish willingness-to-pay. The customer should receive a line-level reason, cited contract provision, expected-versus-billed calculation, supporting shipment evidence, confidence state, and disposition log. “Confirmed savings” should mean a carrier credit note, corrected invoice, or written acceptance—not a modeled variance.

A low-integration version can remain within approximately 15,000–40,000 PLN for a private proof, including secure storage, parsing, contractor review, and limited legal/privacy advice. A reusable multi-carrier product could consume 50,000–100,000 PLN before proof if contract normalization is attempted too broadly. The main cost sensitivity is human review: at only 2–8 PLN of revenue per invoice, even ten minutes of analyst time per invoice destroys the unit economics. Automation must therefore clear routine invoices and reserve manual work for high-value exceptions.

The decisive economic test is stricter than demonstrating discrepancies. Confirmed credits must exceed 0.5% of audited spend and at least three times the total audit fee. At €200,000 monthly freight spend, 0.5% is €1,000; a €300 monthly fee would satisfy the three-times condition only if at least €900 were confirmed. Both thresholds remain unknown.

Exact access should consist of written authority from the customer to process specified invoices, contracts, rate annexes, shipment exports, bills of lading, proofs of delivery, and credit notes; an NDA and data-processing agreement; documented retention/deletion periods; and least-privileged, read-only access. Carrier portals should be accessed only through customer-created accounts or documented delegation. Disputes should not be submitted, accepted, settled, or waived without an expressly authorized employee. Representation, assignment-of-claim, contingency-fee, tax, and jurisdiction-specific dispute activity is counsel-required.

## Acquisition Route

The first-customer route is a freight-procurement consultant or outsourced-finance team already trusted with client invoices. The offer is a read-only 90-day audit requiring:

1. Invoice exports, relevant tariff annexes, and shipment-event files for one or two carriers.
2. A jointly agreed definition of a supportable discrepancy.
3. Customer authorization for finance or procurement staff to adjudicate every proposed exception.
4. No automated dispute submission and no live payment integration.
5. A final ledger separating false positives, valid but surprising charges, unrecoverable discrepancies, and confirmed credits.

A consultant can provide several similarly structured accounts and explain contract language, while the founder supplies normalization and variance analytics. The consultant should be paid a fixed referral or delivery fee that does not depend on making legal claims unless counsel approves the arrangement.

The cheapest private falsification is 100–300 historical invoices from one payer, with all flagged items reviewed by an authorized employee. Success requires enough confirmed, recoverable value to clear both economic thresholds and a median manual-review burden compatible with the proposed invoice price. If source files omit effective dates, shipment events, dimensional data, rate annexes, or accessorial authorization, file sufficiency is falsified without building an integration.

A potential compounding asset is a customer-authorized library of carrier parsers, accessorial definitions, normalized contract clauses, effective-date rules, and final variance outcomes. Customer-specific rates and commercially sensitive terms must remain segregated; only reusable schemas and properly anonymized reason codes should cross accounts.

## Decision-Critical Unknowns

- **Verified:** Freight charges and calculation methods are structurally variable; direct vendors sell invoice-audit services using subscriptions, per-record pricing, and recovery fees.
- **Verified:** Manual review can be material. One vendor-authored European case reports 1.5 FTE before outsourcing, but this does not establish typical labor.
- **Interpreted:** European forwarders and shippers processing at least 100 monthly invoices are a workable initial payer definition.
- **Unknown:** The number of reachable European or Polish payers meeting that definition.
- **Unknown:** Broad freight-invoice error incidence and European recovery rates. Vendor estimates and isolated cases are not representative denominators.
- **Unknown:** Whether confirmed discrepancies exceed 0.5% of spend.
- **Unknown:** Whether confirmed credits exceed three times the full audit cost after review and dispute labor.
- **Unknown:** Whether a 90-day invoice, rate-card, contract, and event export is normally sufficient.
- **Unknown:** Parser coverage and the manual-review share across European carriers and modes.
- **Unknown:** Whether customers accept the proposed per-invoice fee, minimum, contingency share, and cap.
- **Unknown:** Whether credits can be attributed solely to the audit rather than routine finance work, negotiations, or carrier corrections.
- **Unknown:** Whether customers require email, EDI, TMS, ERP, or carrier-portal integration before recurring use.
- **Contradicted:** Surcharge growth, complex tariffs, or a high gross freight bill alone does not prove an erroneous invoice or recoverable credit.
- **Contradicted:** Vendor-reported savings cannot be treated as a broad market recovery rate.
- **Counsel-required:** GDPR roles, cross-border processing, portal delegation, representation in disputes, claim assignment, and outcome-fee legality for the activity actually performed.

## Evidence And Sources

Dated direct-URL ledger:

- 2026-08-22 accessed — UPS, current surcharge structures and changing calculation methods: [https://www.ups.com/us/en/supplychain/tools/surcharges](https://www.ups.com/us/en/supplychain/tools/surcharges)
- 2026-08-22 accessed — VaernFlow, European invoice-audit pricing and vendor-stated recovery model: [https://www.vaernflow.com/](https://www.vaernflow.com/)
- 2026-08-22 accessed — Kloepfel, European manual-audit case and reported savings: [https://kloepfel-consulting.com/en/case-study/outsourcing/](https://kloepfel-consulting.com/en/case-study/outsourcing/)
- 2026-08-22 accessed — Trazai, published subscription and recovery-fee structure: [https://trazai.lat/](https://trazai.lat/)
- 2026-08-22 accessed — Flatworld, post-audit workflow, source-document requirements, and advertised pricing: [https://www.flatworldsolutions.com/logistics/freight-bill-post-audit.php](https://www.flatworldsolutions.com/logistics/freight-bill-post-audit.php)
- 2026-08-22 accessed — provider-market guide, older evidence of European incumbents and transaction scale: [https://www.controlpay.com/assets/files/market_guide_for_freight_aud_308345.pdf](https://www.controlpay.com/assets/files/market_guide_for_freight_aud_308345.pdf)

### Query trace

1. `site:transportation.gov freight invoice audit overcharge complaint refund official`
2. `site:ec.europa.eu freight transport invoice surcharge complaint overcharge`
3. `freight audit pricing per invoice percentage savings Europe`
4. `UPS 2025 accessorial surcharge official rate guide`
5. `FedEx Europe surcharge official 2025 additional handling`
6. `DHL Express Europe surcharge official 2025 rate guide`
7. `freight invoice audit recoveries case study customer direct`
8. `transportation spend management freight audit invoice errors survey`
9. `freight procurement consultant invoice audit Europe`
10. `outsourced finance freight invoice audit services pricing`
11. `freight invoice audit contract rate card shipment event data requirements`
12. `carrier invoice dispute time limit official terms Europe`

