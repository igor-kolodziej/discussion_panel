# Shadow Finalist SFIN-01 — D-009

Shadow-only diagnostic artifact. It is not eligible for downstream routing and cannot alter the frozen live cohort.

## Frozen Level-2 Dossier

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

## Frozen Fact Closure

# Fact Closure D-009

## Findings

- **verified —** Organizations with material freight activity exist. Eurostat reports 246,000 medium and 53,000 large EU enterprises for 2023, while Polish-registered vehicles performed 20.3% of EU road-freight tonne-kilometres. These figures establish a broad commercial base, not the proposed payer denominator.

- **unknown —** No located public source counts European or Polish organizations that both process at least 100 freight invoices monthly and spend approximately €0.5 million annually on freight.

- **verified —** Polish businesses can enter contracts through their registered representatives or duly authorized proxies. Poland’s official business portal states that a written general power covers ordinary-management activities such as contracting, while a specific or category power can authorize defined transactions.

- **interpreted —** A controller, transport manager, or procurement lead is a plausible operational sponsor, but job title alone does not prove authority to sign the first contract. The signer’s KRS/CEIDG representation or internal delegation must be checked for each payer.

- **verified —** Current public budget proxies include AuditCargo’s €499 90-day audit, €999 human-reviewed audit, €300–€1,500 monthly continuous service, and optional 20% recovery fee. VaernFlow advertises service from €299 monthly plus 8–15% of recoveries.

- **unknown —** Public prices do not establish completed purchases, Polish willingness to pay, renewal behavior, or acceptance of the proposed 2–8 PLN per-invoice price.

- **verified —** UPS’s Technology Agreement permits electronic billing data to pass through a defined “Billing Data Service Provider,” makes the customer responsible for that provider, and prohibits using a UPS account without authorization.

- **contradicted —** An NDA, data-processing agreement, or ordinary customer login does not by itself establish unrestricted entitlement to receive or use UPS electronic billing data. Carrier-specific contractual authorization may be required.

- **verified —** Microsoft Dynamics 365 already supports manual and automatic freight-bill reconciliation, required and optional matching fields, tolerances, variance reasons, approval, and invoice-journal posting.

- **verified —** The Microsoft workflow confirms an incumbent route-around that can absorb much of the proposed matching function when the payer already maintains estimated freight bills and matching data in its TMS.

- **interpreted —** A purchased historical audit can limit initial external cash exposure to approximately €499–€999 plus customer review time. That does not establish the cost of building a secure, reusable service.

- **unknown —** Public evidence does not establish implementation labor, analyst minutes per exception, false-positive burden, dispute labor, or the working capital required before recovery fees are collected.

- **counsel-required —** Where invoice and shipment files contain personal data, GDPR Article 28 can require documented processing instructions, confidentiality, security measures, subprocessor controls, and a binding controller–processor arrangement.

- **counsel-required —** Carrier terms, portal delegation, dispute representation, claim assignment, tax treatment, outcome-fee enforceability, and the permitted role of a billing-data service provider require contract- and jurisdiction-specific review.

## Decision-Critical Evidence

1. **Payer existence and denominator**

   - **verified —** Freight-active businesses and direct commercial audit offers establish the existence of a plausible payer class.
   - **unknown —** The count of organizations meeting the fixed invoice-volume and spend thresholds remains unclosed.

2. **First-contract authority**

   - **verified —** A registered representative or properly empowered proxy can bind a Polish business within the applicable authority.
   - **interpreted —** Finance, procurement, or transport staff can sponsor and adjudicate a pilot, but signing authority must be confirmed separately.

3. **Direct willingness or budget proxy**

   - **verified —** European-facing vendors publicly request fixed audit fees, recurring retainers, and recovery shares.
   - **unknown —** Actual transactions, conversion, retention, and willingness at the proposed Polish prices remain private facts.

4. **Claimed access or rights**

   - **verified —** UPS recognizes a controlled billing-data-provider route and requires authorized account use.
   - **contradicted —** Universal third-party access through customer credentials or an NDA alone is not supported.
   - **counsel-required —** Each carrier agreement must be checked before billing data, portal access, or dispute functions are delegated.

5. **Incumbent route-around**

   - **verified —** Existing TMS functionality can calculate expected freight, match invoices, apply tolerances, classify variances, route approval, and post journals.
   - **interpreted —** The candidate must work where payer data or configuration makes the incumbent module incomplete, uneconomic, or unavailable.

6. **Capital exposure**

   - **verified —** A public 90-day audit offer at €499 and human-reviewed report at €999 provide low-cash external proof options.
   - **unknown —** Secure in-house processing cost and manual exception cost remain unverified.
   - **unknown —** The proposed 15,000–40,000 PLN proof budget is neither validated nor directly refuted by a non-equivalent commercial audit price.

7. **Relevant binding rule**

   - **verified —** GDPR Article 28 governs processor arrangements when personal data are processed for a controller.
   - **verified —** Carrier technology and billing agreements can independently restrict account use and third-party billing-data disclosure.
   - **counsel-required —** The actual GDPR role, lawful basis, carrier authorization, dispute authority, and outcome-fee treatment depend on the engagement.

8. **Cheapest remaining private proof**

   - **interpreted —** Use one payer, one carrier, 100–300 historical invoices, the effective contract and rate annexes, and the matching shipment evidence; use customer-supplied exports only and avoid portal access.
   - **interpreted —** Have an authorized customer employee adjudicate every flag before any carrier contact.
   - **interpreted —** Submit only the smallest approved high-value subset through the customer and count only matched credit notes, corrected invoices, or written carrier acceptance.
   - **interpreted —** Falsify the economic premise if confirmed credits do not exceed both 0.5% of audited spend and three times the complete audit cost, or if median manual review cannot fit the proposed invoice price.
   - **interpreted —** An external €499 audit or free sample scan can benchmark findings cheaply, but it cannot replace measuring the candidate’s own parsing, review burden, and attribution.

## Remaining Unknowns

- **unknown —** Polish and European payer denominator at the fixed volume and spend thresholds.
- **unknown —** Representative invoice-error, supportable-discrepancy, carrier-acceptance, and confirmed-credit distributions.
- **unknown —** Whether a normal 90-day export contains all effective dates, shipment events, dimensional data, accessorial approvals, currencies, and contract amendments.
- **unknown —** Parser coverage and exception rates across European carriers and transport modes.
- **unknown —** Customer acceptance of per-invoice charges, monthly minimums, onboarding fees, recovery shares, and caps.
- **unknown —** Average carrier response time and the proportion of accepted variances that become usable credits.
- **unknown —** Attribution of credits between the audit, ordinary accounts-payable work, carrier corrections, and commercial renegotiation.
- **unknown —** Whether carriers other than UPS permit equivalent billing-data-provider or delegated-access arrangements.
- **unknown —** The searched DHL material did not publicly close a generally applicable European invoice-dispute deadline.
- **unknown —** The manual-review burden after routine invoices are automatically cleared.
- **counsel-required —** Representation, claim assignment, contingency fees, portal delegation, retention, cross-border processing, and professional-liability language.

## Indispensable-Premise Check

- **interpreted —** No indispensable premise is directly contradicted by the located public evidence.

- **contradicted —** Unrestricted third-party access to carrier billing data is directly adverse to UPS’s controlled-access terms, but unrestricted portal access is not indispensable to a customer-export, read-only proof.

- **unknown —** The indispensable economic premise—supportable credits above both thresholds after all review and dispute labor—remains unproven.

- **unknown —** The indispensable file-sufficiency premise remains unproven until one payer supplies contract-complete historical data.

## Query And Source Trace

1. `D-009 site:ec.europa.eu/eurostat Poland freight transport enterprises number enterprises 2024`
2. `D-009 site:biznes.gov.pl pełnomocnictwo zawieranie umów przedsiębiorca reprezentacja spółki`
3. `D-009 Europe freight invoice audit pricing per invoice contingency fee`
4. `D-009 site:ups.com terms authorized user account invoice data third party access`
5. `D-009 site:learn.microsoft.com Dynamics 365 transportation freight invoice matching route-around`
6. `D-009 freight invoice audit manual review implementation cost security storage pricing Europe`
7. `D-009 site:eur-lex.europa.eu GDPR Article 28 processor contract personal data official`
8. `D-009 site:dhl.com Europe freight invoice dispute time limit terms conditions supporting documents`

- **verified —** 2026-08-22 accessed; published 2024-12-05: [Eurostat — EU enterprises by size](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20241205-1).

- **verified —** 2026-08-22 accessed: [Eurostat — road-freight measurement metadata and available enterprise statistics](https://ec.europa.eu/eurostat/cache/metadata/en/road_go_esms.htm).

- **verified —** 2026-08-22 accessed: [Biznes.gov.pl — authority and powers of attorney for entrepreneurs](https://biznes.gov.pl/pl/portal/00151).

- **verified —** 2026-08-22 accessed: [AuditCargo — published freight-audit pricing](https://auditcargo.com/pricing).

- **verified —** 2026-08-22 accessed: [VaernFlow — European freight-invoice audit offer](https://www.vaernflow.com/).

- **verified —** 2026-08-22 accessed: [UPS Technology Agreement — authorized accounts and billing-data providers](https://www.ups.com/assets/resources/media/en_US/UTA_with_EUR.pdf).

- **verified —** 2026-08-22 accessed: [Microsoft — freight reconciliation in Dynamics 365](https://learn.microsoft.com/en-us/dynamics365/supply-chain/transportation/reconcile-freight-transportation-management).

- **verified —** 2026-08-22 accessed: [EUR-Lex — GDPR Article 28](https://eur-lex.europa.eu/eli/reg/2016/679/art_28/oj).

