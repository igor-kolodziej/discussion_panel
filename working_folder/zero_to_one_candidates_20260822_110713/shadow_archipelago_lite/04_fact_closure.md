# Shadow Fact Closure

## Closure batch 1

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

# Fact Closure D-008

## Findings

- **verified —** The UK Groceries Code Adjudicator’s 2025 survey covered suppliers to 14 designated large retailers; 17% reported inadequate processes for promptly resolving invoice discrepancies and 11% reported payment delays.

- **verified —** The GCA separately reports continuing recovery-audit issues representing thousands of claims and millions of pounds annually, including invalid claims and claims that smaller suppliers may not defend because of resource costs or fear of retaliation.

- **unknown —** These UK grocery-sector observations do not establish the number of European suppliers with at least €2,000 monthly in unexpired, supportable, abandoned deductions.

- **verified —** A Polish business can contract through its registered representative or a proxy acting within a written general, category, or specific authorization.

- **interpreted —** The supplier’s controller or finance director is the appropriate operational owner for data access, validity decisions, and reconciliation; the legal signer must still be verified through corporate representation or delegation.

- **verified —** OverDeduct publishes $49 and $99 monthly self-service tiers, a free analyzer, and a 25% fee on recovered amounts for done-for-you service.

- **unknown —** Public vendor prices do not prove completed sales, European acceptance, recoveries, retention, or willingness to pay the proposed €300–€1,000 fixed fee plus 10–20%.

- **verified —** Oracle’s current Deductions and Settlement workflow creates a claim from a short-pay, assigns ownership, supports research, approval, credit memos, write-offs, settlement, aging, and root-cause analysis.

- **verified —** Oracle therefore supplies a direct incumbent route-around for organizations that already have the module, clean remittance data, and staff able to operate it.

- **verified —** GCA best practice expects relevant supply agreements, promotion documents, terms, sales data, and calculation methodology to be made available to suppliers so claims can be understood and challenged.

- **unknown —** Supplier entitlement to appoint a third party to access a particular retailer portal was not established by the official Amazon-focused query.

- **contradicted —** A universal third-party portal-automation premise is unsupported and directly adverse to the packet’s cited substitute that avoids automated third-party logins because of portal restrictions.

- **verified —** Directive (EU) 2019/633 applies to specified agricultural and food supply relationships, using supplier and buyer turnover bands, where either party is established in the Union.

- **verified —** The Directive establishes payment-period protections and prohibits specified unfair practices; requested payments for certain buyer-supplied services require written estimates and a cost basis.

- **counsel-required —** Directive coverage, national transposition, retailer-specific rules, agency, portal use, debt-collection characterization, and outcome-fee enforceability must be mapped to the supplier, product, buyer, and jurisdiction.

- **interpreted —** Cash exposure for an initial document-only proof can be near zero externally through a free analyzer or limited to a small self-service subscription, but supplier review time remains a real cost.

- **unknown —** Typical retailer response time, credit issuance time, cash receipt time, analyst hours, and total working-capital exposure remain unclosed.

## Decision-Critical Evidence

1. **Payer existence and denominator**

   - **verified —** The GCA survey establishes suppliers experiencing invoice-discrepancy and payment-resolution problems.
   - **unknown —** The fixed European denominator and the share exceeding €2,000 monthly in supportable abandoned deductions remain unestablished.

2. **First-contract authority**

   - **verified —** A registered representative or properly authorized proxy can bind the supplier.
   - **interpreted —** The controller or finance director should own the pilot operationally because the service requires accounting exports, validity adjudication, and reconciliation.
   - **unknown —** A controller or fractional CFO’s job title alone does not establish signing or claim-submission authority.

3. **Direct willingness or budget proxy**

   - **verified —** Current substitutes publicly request monthly software fees, recovery percentages, or both.
   - **unknown —** Actual European willingness, conversion, retention, and the proposed fee combination remain private evidence.

4. **Claimed access or rights**

   - **verified —** GCA best practice supports the supplier receiving agreements, supporting documents, sales data, and calculation methodology needed to assess claims.
   - **unknown —** That supplier access does not establish a third party’s right to enter or automate any retailer portal.
   - **counsel-required —** Written supplier agency and retailer-specific portal permission are required before third-party submission or credentialed access is assumed.

5. **Incumbent route-around**

   - **verified —** Oracle already centralizes deduction ownership, research, approval, settlement, credit memos, write-offs, aging, and root-cause analysis.
   - **interpreted —** The proposed queue must address abandoned claims, evidence assembly, or operational capacity that the configured ERP and internal team do not already handle.

6. **Capital exposure**

   - **verified —** A free analysis tier, $49–$99 monthly self-service tier, and pure-contingency service provide low-upfront-cost alternatives.
   - **unknown —** External fee minimization does not close internal analyst cost, response latency, or working-capital exposure.
   - **interpreted —** GCA’s 60-day resolution objective is a useful UK grocery-process proxy, not a general European recovery-time distribution.

7. **Relevant binding rule**

   - **verified —** Directive (EU) 2019/633 covers defined agricultural and food supply relationships and sets protected turnover pairings.
   - **verified —** The Directive includes 30- and 60-day payment protections for covered products and transactions.
   - **verified —** The UK Groceries Supply Code requires designated retailers to pay suppliers according to the supply agreement and within a reasonable time.
   - **counsel-required —** Applicability depends on product, turnover, establishment, national implementation, buyer designation, and contract date.

8. **Cheapest remaining private proof**

   - **interpreted —** Start with one supplier, one retailer, and three to twelve months of abandoned deductions using exported remittances, invoices, purchase orders, promotion agreements, delivery evidence, credits, and the open-deduction ledger.
   - **interpreted —** Use no portal credentials and submit nothing during the first pass; require supplier staff to label validity, evidence sufficiency, deadline status, collectible amount, and willingness to authorize a dispute.
   - **interpreted —** Falsify the addressable-value premise immediately if the audit does not identify at least €2,000 per month of unexpired, evidence-supported abandoned claims.
   - **interpreted —** If that threshold clears, have the supplier submit only the smallest high-value approved batch and match retailer credits to the original deductions and ledger receipts.
   - **interpreted —** Count recovery only when the credit is received or applied; exclude drafts, submissions, pending credits, write-offs, and claims the supplier accepts as valid.

## Remaining Unknowns

- **unknown —** European and Polish supplier denominator at the fixed monthly supportable-value threshold.
- **unknown —** Representative invalidity, deadline survival, dispute success, credit issuance, collection, and elapsed-time distributions.
- **unknown —** Actual willingness to pay fixed fees, recovery shares, or both.
- **unknown —** Partner introduction-to-audit and audit-to-paid-continuation conversion.
- **unknown —** Retailer-by-retailer reason codes, evidence rules, deadlines, portal procedures, and change frequency.
- **unknown —** Whether target suppliers can consistently link remittances, invoices, orders, promotions, delivery evidence, credits, and cash receipts.
- **unknown —** Whether official retailer terms permit third-party portal access, automated logins, or submission for each intended account.
- **unknown —** Analyst time per claim cluster and the cost of resolving ambiguous commercial context.
- **unknown —** Recovery attribution when internal finance staff, retailer corrections, or ordinary account reconciliation overlap.
- **unknown —** Typical cash-conversion delay after a retailer accepts a claim.
- **counsel-required —** Supplier agency, portal restrictions, outcome fees, debt-collection characterization, GDPR roles, cross-border processing, retention, and liability language.

## Indispensable-Premise Check

- **interpreted —** No indispensable premise of the read-only, supplier-controlled candidate is directly contradicted by the located public evidence.

- **contradicted —** Universal third-party portal automation is directly adverse evidence, but it is not indispensable because the fixed proof can use exports and supplier-controlled submission.

- **verified —** The underlying workflow, supplier burden, incumbent alternatives, and paid commercial substitutes all exist.

- **unknown —** The indispensable economic premise—at least €2,000 monthly in unexpired, supportable abandoned deductions with collectible credits sufficient to fund delivery—remains unproven.

- **unknown —** The indispensable evidence-linkage premise remains unproven until one supplier’s records connect deductions to agreements, delivery evidence, credits, and receipts.

## Query And Source Trace

1. `D-008 site:gov.uk Groceries Code Adjudicator annual survey suppliers deductions number respondents 2025`
2. `D-008 site:biznes.gov.pl pełnomocnictwo zawieranie umów odzyskiwanie należności przedsiębiorca`
3. `D-008 retail deduction recovery service pricing monthly percentage recovered supplier`
4. `D-008 site:vendorcentral.amazon.com deduction dispute authorized third party portal terms`
5. `D-008 site:docs.oracle.com deductions settlement claims write-off approval workflow 2026`
6. `D-008 retail deduction dispute response time working capital recovery case study supplier direct`
7. `D-008 site:eur-lex.europa.eu Directive 2019/633 payment deductions supplier buyer official`
8. `D-008 site:gov.uk forensic auditing retailer deductions supplier evidence agreements sales data methodology`

- **verified —** 2026-08-22 accessed; published 2025-06-25: [Groceries Code Adjudicator — 2025 supplier survey results](https://www.gov.uk/government/news/gca-survey-shows-continued-improved-treatment-of-grocery-suppliers).

- **verified —** 2026-08-22 accessed: [Biznes.gov.pl — authority and powers of attorney for entrepreneurs](https://biznes.gov.pl/pl/portal/00151).

- **verified —** 2026-08-22 accessed: [OverDeduct — published deduction-management and recovery pricing](https://www.overdeduct.com/pricing).

- **verified —** 2026-08-22 accessed: [Oracle 26B — Deductions and Settlement workflow](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/fauds/how-deductions-and-settlement-works.html).

- **verified —** 2026-08-22 accessed: [EUR-Lex — Directive (EU) 2019/633](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX%3A32019L0633).

- **verified —** 2026-08-22 accessed; updated 2023-02-08: [Groceries Code Adjudicator — forensic-auditing best practice](https://www.gov.uk/government/publications/best-practice-statement-forensic-auditing/best-practice-statement-forensic-auditing).

- **verified —** 2026-08-22 accessed: [Deduction Clerk — packet-building workflow and stated portal limitation](https://deductionclerk.com/).

- **unknown —** 2026-08-22 search: the targeted official Amazon Vendor Central query returned no public source establishing general third-party portal or submission rights.

## Closure batch 2

# Fact Closure D-036

## Findings

- **verified:** Payers exist: PSE identifies owners of renewable installations that executed non-market redispatch instructions as the parties entitled to seek compensation.
- **unknown:** The payer denominator is not closed. PSE reports 26,020 MW of photovoltaic capacity and 11,175 MW of wind capacity in early 2026, while URE publishes installation registers; neither source identifies the number of curtailed, eligible, economically material, independently purchasing portfolios.
- **verified:** First-contract authority rests with the installation owner, its KRS-authorized representatives, or a properly empowered attorney. PSE permits servicing entities to operate applications, but accepting settlement information requires appropriate representative or attorney authority.
- **interpreted:** Direct commercial willingness has a current proxy: OdzyskOZE publicly offers subscriptions of €119, €699, or €2,325 per month plus a partner-law-firm fee of 5% of recovery.
- **unknown:** OdzyskOZE states that its examples are illustrative and that real case studies will be published only after it has consenting clients; the offer therefore proves a seller’s pricing hypothesis, not purchases, recoveries, or market acceptance.
- **verified:** The incumbent route-around is substantial. Owners can use PSE’s WOZE portal, current Excel forms, correction workflow, settlement information, and complaint process without buying a third-party ledger.
- **unknown:** Public sources do not establish the capital required for repeatable SCADA ingestion, multi-operator normalization, evidence exception handling, or secure portfolio operation.
- **interpreted:** The cheapest remaining proof is document-led rather than integration-led: review ten authorized assets or asset groups using existing PSE forms, notices, meter or SCADA exports, connection agreements, support records, settlements, and correspondence.

## Decision-Critical Evidence

- **verified:** PSE states that compensation is unavailable where the connection agreement does not guarantee firm delivery for balancing-related reasons. Connection-agreement screening must therefore precede onboarding.
- **verified:** Article 13(7) of Regulation (EU) 2019/943 requires compensation for non-market redispatch, subject to the non-firm-delivery exception, based on additional operating cost, foregone net day-ahead revenue, or an appropriate combination where one measure would be unjustifiably low or high.
- **verified:** PSE’s operating rules state that the compensation claim expires if the owner does not apply before 180 days have elapsed from the last day of the month in which the redispatch instruction was executed.
- **verified:** For auction-support treatment, Article 93(18) as implemented in PSE guidance requires notice to the connected operator within 14 days of the instruction. Missing it excludes the reduced energy from the support obligation and the related lost-support-revenue component; it does not extinguish every possible compensation component.
- **verified:** A deficient claim left uncorrected for 14 days may be left without examination, and an owner has 21 days to complain about rejection or settlement information.
- **verified:** WOZE is available to owners and entities servicing them. Its ordinary service roles permit preparing and viewing applications but expressly exclude acceptance of compensation.
- **verified:** PSE requires OSD authorizations and, where applicable, a power of attorney. Acceptance authority must follow KRS representation rules or a sufficient power of attorney.
- **verified:** PSE’s forms accommodate incomplete irradiance or wind data and prescribe averaging when measurements use multiple points or non-15-minute periods. Missing direct measurements are therefore an evidence-quality issue, not automatically a proven lost claim.
- **interpreted:** Direct WOZE access, operator calculation, correction, and complaint workflows mean the ledger must prove value from deadline control, evidence reconciliation, or contestable exceptions rather than merely reproducing public redispatch intervals.
- **contradicted:** A universal eligibility premise is contradicted by the non-firm-connection exception.
- **contradicted:** A claim estimate based only on curtailed MWh multiplied by an average positive wholesale price is contradicted by the governing calculation framework.
- **counsel-required:** Eligibility under individual connection agreements, PPA allocation, support treatment, complaint or litigation strategy, filing authority, outcome-linked fees, and the legal effect of each operator rule require Polish energy counsel.
- **counsel-required:** The amended Polish cybersecurity regime requires entities meeting its sectoral and size criteria to assess registration, information-security, incident, and audit obligations. Whether the ledger provider or a particular generator is covered cannot be inferred from the energy-sector label alone.

## Remaining Unknowns

- **unknown:** The number of portfolios combining actual curtailment, firm-delivery eligibility, material recoverable value, reachable ownership, and willingness to buy monitoring.
- **unknown:** Whether at least 20% of ten authorized portfolios contain a missed deadline, incomplete evidence set, or unreconciled interval with a material consequence confirmed by the owner or counsel.
- **unknown:** The distribution of realized compensation after negative prices, support rules, PPA terms, outages, availability modeling, and operator calculations.
- **unknown:** Whether customers have synchronized notices, SCADA, metering, settlement, forecast, availability, and contractual evidence.
- **unknown:** Whether a common reconciliation method works across OSDs, generation technologies, SCADA vendors, and commercial arrangements.
- **unknown:** Actual customer acceptance of subscription, setup, or outcome-linked pricing.
- **unknown:** Manual exception time and secure operating cost per asset.
- **unknown:** The cheapest proof’s cash requirement; the dossier’s PLN 25,000–60,000 range remains an unverified planning estimate.

## Indispensable-Premise Check

- **unknown:** No located public evidence directly tests the indispensable premise that enough eligible portfolios contain consequential, economically material reconciliation or deadline failures.
- **unknown:** No indispensable premise was directly contradicted in the located public record, but public absence is not affirmative proof.
- **contradicted:** Universal eligibility, automatic recoverability, and mechanical headline-price valuation are directly contradicted; none is indispensable if the service screens connection terms and records uncertain outcomes.
- **interpreted:** The decisive private test remains ten authorized assets or asset groups, with success only where at least 20% show a material consequence confirmed by the owner or qualified counsel.

## Query And Source Trace

- **verified:** 2019-06-05 — Regulation (EU) 2019/943, Article 13: [https://eur-lex.europa.eu/legal-content/en/TXT/?uri=CELEX%3A32019R0943](https://eur-lex.europa.eu/legal-content/en/TXT/?uri=CELEX%3A32019R0943)
- **verified:** Accessed 2026-08-22 — PSE compensation, eligibility, support-notice, evidence, and authority guidance: [https://www.pse.pl/pl_PL/redysponowanie-nierynkowe](https://www.pse.pl/pl_PL/redysponowanie-nierynkowe)
- **verified:** Accessed 2026-08-22 — PSE IRiESP update containing the 180-day expiry, correction, settlement, and complaint rules: [https://www.pse.pl/documents/20182/5316414280/karta_aktualizacji_nr_2_2024_final.pdf/42ad5023-4530-47ab-b419-a6f3bd592437](https://www.pse.pl/documents/20182/5316414280/karta_aktualizacji_nr_2_2024_final.pdf/42ad5023-4530-47ab-b419-a6f3bd592437)
- **verified:** Accessed 2026-08-22 — current PSE application conditions and authorization documents: [https://www.pse.pl/documents/20182/4168830618/Warunki_skladania_Wniosku_o_rekompensate.pdf](https://www.pse.pl/documents/20182/4168830618/Warunki_skladania_Wniosku_o_rekompensate.pdf)
- **verified:** Updated 2026-04-01; accessed 2026-08-22 — WOZE roles and owner/service-provider access: [https://www.pse.pl/WOZE](https://www.pse.pl/WOZE)
- **verified:** 2026-03-10 — PSE correction to calculation rules, applicable to settlements after 2026-03-03: [https://www.pse.pl/-/korekta-zasad-wyliczania-rekompensaty-za-redysponowanie-nierynkowe-instalacji-oze](https://www.pse.pl/-/korekta-zasad-wyliczania-rekompensaty-za-redysponowanie-nierynkowe-instalacji-oze)
- **verified:** Updated 2026-08-06 — URE renewable-installation register through 2026-06-30: [https://ure.gov.pl/pl/oze/potencjal-krajowy-oze/8108%2CInstalacje-odnawialnych-zrodel-energii-stan-na-30-czerwca-2026-r.html](https://ure.gov.pl/pl/oze/potencjal-krajowy-oze/8108%2CInstalacje-odnawialnych-zrodel-energii-stan-na-30-czerwca-2026-r.html)
- **interpreted:** Accessed 2026-08-22 — OdzyskOZE pricing, process, and express absence of real customer case studies: [https://odzyskoze.pl/en/](https://odzyskoze.pl/en/)
- **counsel-required:** 2026-06-05 — Ministry of Digital Affairs summary of amended KSC obligations: [https://www.gov.pl/web/cyfryzacja/nowelizacja-ustawy-o-krajowym-systemie-cyberbezpieczenstwa-ksc---obowiazki-podmiotow-kluczowych-i-waznych](https://www.gov.pl/web/cyfryzacja/nowelizacja-ustawy-o-krajowym-systemie-cyberbezpieczenstwa-ksc---obowiazki-podmiotow-kluczowych-i-waznych)

1. `site:ure.gov.pl OR site:pse.pl Poland number renewable generators photovoltaic installations redispatch 2025 payer denominator`
2. `site:pse.pl redysponowanie nierynkowe wniosek pełnomocnictwo operator właściciel instalacji rekompensata`
3. `Poland OZE curtailment compensation claims success fee customer case study OdzyskOZE`
4. `site:pse.pl redysponowanie nierynkowe dane pomiarowe SCADA dostęp właściciel operator instrukcja`
5. `site:pse.pl WOZE rekompensata redysponowanie nierynkowe samodzielnie wniosek operator calculation route`
6. `site:gov.pl OR site:ure.gov.pl OZE SCADA cyberbezpieczeństwo NIS2 operator Polska obowiązki 2026`
7. `site:eur-lex.europa.eu 2019/943 Article 13 7 non-market-based redispatching financial compensation exact rule`
8. `site:pse.pl warunki wniosku rekompensata PV FW dokumenty dane pomiarowe cheapest historical audit proof`

# Fact Closure D-020

## Findings

- **verified:** A broad payer population exists. NBP reported 649,800 Polish card-accepting merchants, 1,004,200 acceptance locations, and approximately 1.369 million POS terminals at the end of 2025 Q2.
- **unknown:** The qualified denominator remains unclosed because NBP’s aggregates do not identify existing non-promotional SMEs with PLN 500,000–5 million card turnover, above-market blended fees, actionable contract terms, and willingness to purchase an audit.
- **verified:** Provider onboarding culminates in a contract signed by the merchant. Pekao’s public process lets a business request an individualized offer and then choose and sign the agreement.
- **unknown:** Public provider material does not establish that an accountant or fee auditor can request comparable quotes or negotiate retention terms without provider-specific authorization.
- **unknown:** No located Polish case study or customer evidence verifies willingness to pay an audit or success fee.
- **interpreted:** Recurring acquiring spend, individualized provider offers, and UK regulatory findings supply budget and behavior proxies, but UK shopping and switching evidence cannot establish Polish conversion or savings.
- **verified:** The incumbent route-around is direct shopping or negotiation. Pekao invites individualized terms, eService invites direct quote requests, and merchants can terminate under their existing contractual notice periods.
- **interpreted:** The cheapest remaining proof is a manual, document-only audit of 15–25 existing merchants, followed by comparable written quote requests and first-statement verification.

## Decision-Critical Evidence

- **verified:** Regulation (EU) 2015/751 caps consumer debit interchange at 0.2% and consumer credit interchange at 0.3%; these limits apply to interchange, not the complete merchant service charge.
- **verified:** Article 9 requires acquirers to offer merchant service charges differentiated by card category and brand and to identify merchant service, interchange, and scheme fees in agreements unless the merchant requests blended charging in writing.
- **verified:** Article 12 requires transaction information including the merchant service charge and interchange amount, subject to permitted aggregation with the merchant’s prior explicit consent.
- **verified:** Pekao publishes a non-promotional reference of 0.7% plus PLN 0.04 per transaction and terminal rent of PLN 30, 40, or 50 monthly.
- **verified:** Pekao also offers individualized commercial conditions, establishing that direct bilateral repricing is available without an auditor.
- **verified:** Current subsidized offers materially weaken the proposition for new users. The Polska Bezgotówkowa rules cover terminal use and card processing for 12 months, subject to a PLN 100,000 turnover limit, while eService advertises a further 18 months of PLN 1 monthly rental.
- **verified:** eService’s termination form lists unfavorable commercial terms and a better competitor offer as termination reasons, but states that early equipment return does not shorten the contractual notice period or end fees before the contract expires.
- **interpreted:** The eService form supports the existence of switching behavior and contract friction but does not quantify termination charges, downtime, retention discounts, or realized savings.
- **interpreted:** The UK PSR found that non-published prices, inconsistent pricing structures, indefinite agreements, and terminal contracts restricted searching and switching; this validates the mechanism only in the UK.
- **unknown:** Polish fee dispersion, quote comparability, retention frequency, and post-switch savings remain publicly unverified.
- **unknown:** Public sources do not establish that at least 25% of audited Polish SMEs can realize savings exceeding twice the proposed fee after termination, equipment, training, downtime, and promotion effects.
- **counsel-required:** Whether quote solicitation, recurring negotiation, referrals, commissions, or contingent compensation constitute regulated or otherwise restricted intermediation under current Polish law requires current Polish payments counsel.
- **counsel-required:** Merchant authorization, confidentiality, GDPR allocation, retention, referral disclosure, liability for comparisons, and avoidance of cardholder-data access require contractual and privacy review.

## Remaining Unknowns

- **unknown:** The distribution of complete blended acquiring costs across Polish SMEs.
- **unknown:** The proportion paying materially more than an immediately obtainable like-for-like offer.
- **unknown:** Whether providers will give written quotes with equivalent card mix, settlement, gateway, rental, chargeback, DCC, and termination assumptions.
- **unknown:** The acceptance rate for merchant-authorized third-party quote requests.
- **unknown:** The frequency and size of incumbent retention offers.
- **unknown:** Termination charges, notice periods, terminal replacement time, training cost, settlement disruption, and downtime by provider.
- **unknown:** First-statement realized savings and persistence after promotional periods.
- **unknown:** Accountant introduction rate and merchant willingness to pay a fixed or contingent fee.
- **unknown:** The cheapest proof’s exact budget; the dossier’s PLN 5,000–15,000 estimate has no public validation.

## Indispensable-Premise Check

- **unknown:** The indispensable premise—that at least 25% of audited Polish SMEs can save more than twice the fee without disproportionate disruption—has not been directly tested by located public evidence.
- **unknown:** No indispensable premise was directly contradicted in the located public record, but public absence is not affirmative proof.
- **contradicted:** A blanket premise that Polish merchants are generally overpaying is directly contradicted by published low standard pricing, individualized offers, and substantial introductory subsidies.
- **interpreted:** The contradiction does not eliminate a targeted audit proposition if the first cohort excludes subsidized merchants and requires realized, net savings rather than unaccepted quotes.
- **interpreted:** The cheapest decisive test remains three recent statements plus the current contract for each of 15–25 existing merchants, at least two comparable offers where available, and verification against the first post-change statement.

## Query And Source Trace

- **verified:** 2025 Q2 report, published 2025 — NBP merchant, acceptance-location, and terminal counts: [https://nbp.pl/wp-content/uploads/2025/11/2025-Q2-informacja-o-kartach-platniczych.pdf](https://nbp.pl/wp-content/uploads/2025/11/2025-Q2-informacja-o-kartach-platniczych.pdf)
- **verified:** 2015-04-29 — Regulation (EU) 2015/751, interchange caps and Articles 9 and 12: [https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32015R0751](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32015R0751)
- **verified:** Accessed 2026-08-22 — Pekao standard pricing, promotional eligibility, individualized terms, and contracting process: [https://www.pekao.com.pl/przedsiebiorcy/uslugi-dodatkowe/terminal-pos](https://www.pekao.com.pl/przedsiebiorcy/uslugi-dodatkowe/terminal-pos)
- **verified:** Accessed 2026-08-22 — eService subsidized and post-subsidy offer: [https://www.eservice.pl/polska-bezgotowkowa](https://www.eservice.pl/polska-bezgotowkowa)
- **verified:** Version 15.0, accessed 2026-08-22 — Polska Bezgotówkowa operational rules: [https://api.polskabezgotowkowa.pl/uploads/Wyciag_z_Zasad_Operacyjnych_15_0_dla_akceptantow_standardowych_w_terminalach_3de8609a21.pdf](https://api.polskabezgotowkowa.pl/uploads/Wyciag_z_Zasad_Operacyjnych_15_0_dla_akceptantow_standardowych_w_terminalach_3de8609a21.pdf)
- **verified:** Accessed 2026-08-22 — eService termination form and continuing-fee warning: [https://www.eservice.pl/hubfs/Formularz%20wypowiedzenia%20umowy.pdf](https://www.eservice.pl/hubfs/Formularz%20wypowiedzenia%20umowy.pdf)
- **interpreted:** 2021-11-03 — UK PSR acquiring-market findings; UK evidence only: [https://www.psr.org.uk/publications/market-reviews/mr1818-market-review-into-the-supply-of-card-acquiring-services-final-report/](https://www.psr.org.uk/publications/market-reviews/mr1818-market-review-into-the-supply-of-card-acquiring-services-final-report/)
- **interpreted:** 2022-10-06 — UK PSR comparison and contract remedies; UK evidence only: [https://www.psr.org.uk/publications/policy-statements/ps22-2-camr-final-decision/](https://www.psr.org.uk/publications/policy-statements/ps22-2-camr-final-decision/)
- **counsel-required:** 2025-04-24 consolidation, marked expired 2026-05-11 — Polish Payment Services Act source returned by the authority query and therefore not relied upon as current binding text: [https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU20250000611](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU20250000611)

1. `site:nbp.pl 2025 liczba akceptantów terminale POS Polska Q1 merchant denominator`
2. `site:pekao.com.pl OR site:eservice.pl terminal oferta pełnomocnictwo przedsiębiorca zapytanie oferta acquiring`
3. `Poland merchant card acquiring fee audit savings case study SME success fee`
4. `site:eur-lex.europa.eu Regulation 2015/751 merchant statement interchange scheme fee information Article 9 12`
5. `site:pekao.com.pl terminal POS 0,7% 0,04 zł czynsz 30 40 50 oferta standardowa`
6. `site:eservice.pl OR site:polcard.pl terminal umowa okres wypowiedzenia opłata rozwiązanie zmiana operatora Polska`
7. `site:isap.sejm.gov.pl ustawa o usługach płatniczych agent pośrednik acquiring merchant referral authorization`
8. `site:polskabezgotowkowa.pl regulamin przedsiębiorca terminal 12 miesięcy warunki obecny akceptant`

## Closure batch 3

# Fact Closure D-006

## Findings

- **verified:** Regulation (EU) 1169/2011 creates a payer-relevant control obligation: the operator under whose name food is marketed must ensure food-information accuracy, operators must verify requirements relevant to their activities, and upstream operators must provide downstream businesses sufficient information. Ingredients and allergens are mandatory particulars. The Regulation does not prescribe automated specification comparison. [Regulation (EU) 1169/2011](https://eur-lex.europa.eu/eli/reg/2011/1169)

- **unknown:** Eurostat and Statistics Poland collect enterprise counts by detailed NACE activity and employment size, including Polish food manufacturing, but the retrieved public material does not isolate manufacturers with 50–500 SKUs, multiple emailed supplier specifications, or an internal technical buyer. The reachable Polish payer denominator remains unknown. [Eurostat Polish SBS metadata](https://ec.europa.eu/eurostat/cache/metadata/en/sbs_h_esms_pl.htm)

- **interpreted:** A manufacturer’s quality manager, technical manager, regulatory lead, or owner is the likely operational authority because the food business—not its consultant—retains the regulatory responsibility. Public evidence does not establish which role can sign the first PLN 3,000–8,000 census or a recurring subscription.

- **unknown:** No public evidence established a food-safety consultant’s introduction-to-contract conversion rate, authority to purchase on behalf of a manufacturer, or commercial incentive to introduce this service. The first contract must therefore be executed by an authorized manufacturer representative; the consultant route remains an acquisition hypothesis.

- **verified:** Adjacent software has explicit budgets. Foodflou lists document management, approval flows, audit logs, reminders, version control, and a change register from €89 per month. SupplierConnect advertises €3,000 per month for a platform covering 25 suppliers, with higher managed-approval tiers. These are direct prices for adjacent controls, not evidence that manufacturers will buy relationship-priced automated diffs. [Foodflou pricing](https://www.foodflou.com/pricing) [SupplierConnect pricing](https://www.supplierconnect.ai/)

- **interpreted:** Published adjacent prices support the existence of software budgets ranging from low hundreds to several thousand euros monthly, but they do not validate PLN 25–75 per supplier-product relationship, the proposed monthly minimum, or the onboarding fee.

- **counsel-required:** Customer possession of a supplier document does not automatically authorize every downstream use. Directive (EU) 2016/943 treats unauthorized access, copying, use, or disclosure of protected trade secrets—and breach of confidentiality or use restrictions—as unlawful. Customer authorization, supplier-contract restrictions, service-provider access, model-training exclusions, retention, and cross-customer reuse require contractual review. [Directive (EU) 2016/943, Articles 3–4](https://eur-lex.europa.eu/eli/dir/2016/943/oj)

- **verified:** Where supplier contacts or other personal data are processed on the customer’s behalf, GDPR Article 28 requires a binding processor contract, documented instructions, controls on subprocessors, and corresponding protection obligations. [GDPR, Article 28](https://eur-lex.europa.eu/eli/reg/2016/679/oj)

- **verified:** Direct route-arounds already exist. NSF TraQtion provides supplier portals, digital specifications, approval workflows, version-stamped records, allergen and formulation fields, archives, and document tracking. Foodflou provides version control and change registers. These products establish that some manufacturers can route around emailed-document comparison through structured portals or broader quality-management systems. [NSF TraQtion specification management](https://www.nsf.org/traqtion/specification-management) [Foodflou pricing](https://www.foodflou.com/pricing)

- **contradicted:** Any indispensable framing that manufacturers lack incumbent version-control or supplier-portal options is directly contradicted by the published NSF, Foodflou, TIMS, and SupplierConnect offerings. This does not establish adoption among Polish small manufacturers.

- **unknown:** Public implementation references describe onboarding in days or weeks but do not disclose labor, security, adviser, insurance, or liability costs for the proposed private-proof system. The PLN 20,000–60,000 build estimate and PLN 3,000–8,000 census estimate remain unverified capital assumptions. [Foodflou implementation information](https://www.foodflou.com/pricing)

- **verified:** BRCGS guidance requires the effects of changed raw materials to be reviewed and states that a new allergen or ingredient-declaration impact must be addressed before the changed material is used or accepted. This supports qualified review and change control, not autonomous software approval. [BRCGS supplier-change guidance](https://www.brcgs.com/media/2082504/food-safety-covid-19-guideline-unlocked.pdf)

- **interpreted:** The cheapest remaining decision-relevant private proof is a retrospective census using one authorized customer’s existing documents, not a production platform: at least 30 genuine old/new document pairs, a declared sampling period, the approved baseline, and adjudication by the customer’s competent employee.

## Decision-Critical Evidence

- **verified:** A binding food-information responsibility and upstream information duty exist under Articles 8 and 9 of Regulation 1169/2011.

- **verified:** Supplier or ingredient changes can require review of allergens, ingredient declarations, labels, shelf life, packaging, and affected finished products before acceptance.

- **verified:** Real incumbent systems already centralize supplier specifications, version histories, approvals, allergen information, and document changes.

- **verified:** Adjacent vendors publish monthly prices, demonstrating an addressable compliance-software budget category.

- **interpreted:** The first buyer must be a manufacturer representative with budget and data authority; a consultant can introduce or assist but is not publicly shown to possess contracting authority.

- **counsel-required:** Supplier-document access must be limited to uses authorized by the customer’s contracts and compatible with trade-secret, confidentiality, intellectual-property, and data-protection duties.

- **unknown:** The public record does not establish the frequency of material supplier-document changes, comparison labor, missed-change incidence, number of downstream records affected, or willingness to pay for monitoring.

- **unknown:** The public record does not establish whether relationship-based pricing maps better to budget ownership than site, supplier, SKU, or document-volume pricing.

- **interpreted:** The private proof should record material changes, previously missed changes, extraction errors, reviewer minutes, clarification cycles, and resulting label, allergen-matrix, HACCP, certificate, or baseline updates.

- **interpreted:** The private proof should stop if material changes are rare, qualified review time is not materially reduced, or the customer declines an ongoing paid monitoring arrangement.

## Remaining Unknowns

- **unknown:** Number of reachable Polish food manufacturers matching the operational profile.

- **unknown:** Identity and spending authority of the first economic buyer inside those manufacturers.

- **unknown:** Consultant introduction rate, referral economics, and perceived conflict with consulting work.

- **unknown:** Material-change frequency per 100 monitored supplier-product relationships.

- **unknown:** Median and tail reviewer time for multilingual PDF, spreadsheet, scan, and portal-export comparisons.

- **unknown:** Extraction accuracy for compound ingredients, allergens, nutrition, claims, certificate references, and ambiguous revisions.

- **unknown:** Share of changes that cause a finished-product, label, allergen-matrix, certificate, HACCP, customer-approval, or artwork action.

- **unknown:** Supplier response times and the proportion of changes that require clarification.

- **unknown:** Customer willingness to pay the proposed onboarding, relationship, or monthly-minimum prices.

- **unknown:** Real build and operating capital after secure hosting, qualified review, insurance, and liability advice.

- **counsel-required:** Professional-responsibility boundary, warranty language, limitation of liability, insurance coverage, security obligations, data location, retention, deletion, and incident response.

## Indispensable-Premise Check

- **unknown:** The indispensable demand premise—at least five material changes per month consuming more than eight staff hours for a representative 100-SKU manufacturer—remains unknown. No retrieved public evidence measures this denominator.

- **unknown:** Public silence on that frequency is not adverse evidence and is not treated as contradiction.

- **contradicted:** A universal absence of specification version-control alternatives is directly contradicted by incumbent supplier portals and quality-management platforms.

- **unknown:** No indispensable premise specific to a manual-first, customer-authorized retrospective census was directly contradicted.

## Query And Source Trace

### Dated direct-URL ledger

- **verified:** 2011-10-25 adoption; consolidated text accessed 2026-08-22 — Regulation (EU) 1169/2011, Articles 8–9: https://eur-lex.europa.eu/eli/reg/2011/1169

- **verified:** 2020 publication; accessed 2026-08-22 — BRCGS supplier-change guidance: https://www.brcgs.com/media/2082504/food-safety-covid-19-guideline-unlocked.pdf

- **verified:** 2023-02-14 metadata update; accessed 2026-08-22 — Eurostat/Statistics Poland structural-business-statistics metadata: https://ec.europa.eu/eurostat/cache/metadata/en/sbs_h_esms_pl.htm

- **verified:** Accessed 2026-08-22 — Foodflou pricing and implementation information: https://www.foodflou.com/pricing

- **verified:** Accessed 2026-08-22 — SupplierConnect published supplier-compliance pricing: https://www.supplierconnect.ai/

- **verified:** Accessed 2026-08-22 — NSF TraQtion specification-management functions: https://www.nsf.org/traqtion/specification-management

- **verified:** 2016-06-08 publication; accessed 2026-08-22 — Directive (EU) 2016/943 on trade secrets: https://eur-lex.europa.eu/eli/dir/2016/943/oj

- **verified:** 2016-04-27 adoption; accessed 2026-08-22 — Regulation (EU) 2016/679, including Article 28: https://eur-lex.europa.eu/eli/reg/2016/679/oj

### Queries

1. `site:stat.gov.pl OR site:ec.europa.eu/eurostat Poland food manufacturing enterprises PKD 10 number enterprises 2024`
2. `site:brcgs.com food safety consultant supplier specification change review manufacturer`
3. `food safety supplier approval specification management software pricing official`
4. `site:eur-lex.europa.eu supplier product specifications confidential information trade secrets GDPR processor food manufacturer`
5. `food manufacturer supplier specification version control customer portal incumbent software official`
6. `food specification document comparison implementation cost OCR pricing official`
7. `site:eur-lex.europa.eu Regulation 1169/2011 Article 8 food business operator upstream information supplier`
8. `supplier specification change audit case study food manufacturer missed changes comparison time`

# Fact Closure D-003

## Findings

- **verified:** A payer category exists. Eurostat’s NACE Rev. 2.1 class 52.26 expressly includes customs agents, transport-document activities, multimodal organization, and freight forwarding on behalf of shippers or consignees; class 52.31 includes freight-transport intermediaries. [Eurostat NACE Rev. 2.1](https://ec.europa.eu/eurostat/documents/3859598/21633320/KS-GQ-24-007-EN-N.pdf)

- **unknown:** Eurostat’s structural-business-statistics system can report enterprises by detailed activity and size, but the retrieved public evidence did not produce a European count of forwarders, NVOCCs, brokers, importers, exporters, consignees, or drayage operators that receive recurring ocean-container D&D invoices. The reachable payer denominator remains unknown. [Eurostat SBS overview](https://ec.europa.eu/eurostat/en/web/structural-business-statistics)

- **verified:** U.S. charge stakes are material: nine carriers reported approximately $15.4 billion collected between 2020-04-01 and 2025-03-31. This is a charge denominator, not an erroneous-invoice or European payer denominator. [FMC D&D data](https://www.fmc.gov/detention-and-demurrage/)

- **verified:** In FY2024 the FMC received 189 charge complaints, found 130 appropriate for investigation, and reported $1,874,142 in charges refunded or cancelled during the year. The difference between complaints received, investigations accepted, and refunds establishes that a complaint is not automatically supportable or recoverable. [FMC FY2024 Annual Report](https://fmc.gov/wp-content/uploads/2025/04/FY-2024-Annual-Report.pdf)

- **interpreted:** The initial operational buyer is most plausibly the party already responsible for approving or passing through the invoice and controlling the shipment evidence. Public evidence does not identify which European role—operations, finance, freight audit, branch management, or owner—can authorize the first retrospective engagement.

- **counsel-required:** Carrier-facing submission authority cannot be inferred from possession of an invoice. Maersk’s FMC schedule requires proof of merchant or NVOCC status in specified circumstances and a letter of authority for an appointed agent. Whether a dossier provider may submit, negotiate, settle, or charge an outcome fee depends on the customer mandate, governing contract, jurisdiction, and regulated-activity rules. [Maersk Spot terms](https://terms.maersk.com/terms-spot-booking)

- **verified:** Direct willingness proxies exist. Sellexio advertises a free invoice audit and a $29-per-month D&D information product; DemurrageIQ advertises a one-month free pilot followed by $299 per month. These are vendor offers, not verified purchase or retention data. [Sellexio pricing](https://www.sellexio.co/pricing) [DemurrageIQ](https://auditdemurrageiq.com/)

- **interpreted:** Published subscription, audit, and recovery-linked offers support a budget category for D&D controls, but they do not validate the proposed PLN 150–2,000 dossier fees or 10–20% recovery fee in Europe.

- **verified:** Carrier evidentiary requirements create the reconstruction burden. CMA CGM requires written evidence, contractual terms for free-time or rate disputes, interchange receipts for activity-date disputes, communications for incorrect-information disputes, and precisely timestamped appointment screenshots. It states that unsupported days can be denied. [CMA CGM D&D guidance](https://www.cma-cgm.com/local/united-states/detention-and-demurrage)

- **verified:** Maersk’s published Spot schedule requires written notice identifying the disputed item within 30 days when that schedule applies, while also describing a 180-day acceptance waiver. It makes governing law, bill-of-lading terms, and the applicable schedule decisive. [Maersk Spot terms](https://terms.maersk.com/terms-spot-booking)

- **counsel-required:** Maersk’s terms restrict disclosure of negotiated terms and performance information without written consent, subject to stated exceptions. Shipment contracts, tariffs, invoices, customs material, correspondence, and portal exports therefore require customer authorization and contract-specific confidentiality review.

- **verified:** Carrier tools are direct route-arounds. ONE has published a D&D calculator for Europe and Africa, while carrier portals and FMC best practices provide rate, free-time, dispute-contact, and notification functions. Preventive calculators and carrier portals can reduce or replace retrospective reconstruction for some shipments. [ONE Europe and Africa D&D calculator](https://eua.one-line.com/news/detention-and-demurrage-dd-calculator-now-live-europe-and-africa) [FMC carrier-audit best practices](https://www.fmc.gov/databases-and-publications/vessel-operating-common-carrier-vocc-audit-program/)

- **contradicted:** Any premise that a third-party dossier is the only practical route is contradicted by carrier dispute portals, carrier calculators, negotiated free time, internal freight audit, and specialist recovery vendors.

- **unknown:** Public evidence does not verify the proposed PLN 10,000–35,000 proof cost or PLN 50,000–100,000 secure-system cost. Published free audits show that initial external cash cost can be lower, but they do not disclose internal labor, security, evidence normalization, legal review, or unbiased sampling cost.

- **verified:** The FMC’s 2024 final rule imposes 30-day invoicing and request periods and required invoice contents for covered U.S. billing. The FMC expressly defines who may be billed and states that missing required information affects payment obligation. [FMC final-rule announcement](https://www.fmc.gov/articles/fmc-publishes-final-rule-on-detention-and-demurrage-billing-practices/)

- **contradicted:** Representing the FMC rule as governing European shipments is directly contradicted by the rule’s U.S. statutory and regulatory basis and by carrier terms that make the applicable contract, bill of lading, law, and jurisdiction control.

- **unknown:** The eight-query public search did not establish a harmonized EU rule equivalent to the FMC billing rule for private ocean-container D&D invoices. Public absence is not proof that no EU, national, contractual, or port-specific rule applies.

- **interpreted:** The cheapest remaining private proof is a retrospective, customer-authorized sample from one carrier, one port pair, and one contractual procedure. It must contain an unbiased denominator of relevant invoices rather than only known disputes.

## Decision-Critical Evidence

- **verified:** Aggregate D&D charges and completed refunds establish economic stakes and actual recovery events.

- **contradicted:** Aggregate collected charges do not establish invoice-error incidence.

- **verified:** Carrier procedures require contemporaneous, source-specific evidence and can deny days for which evidence is missing.

- **verified:** Direct vendors publish subscription, free-audit, and recovery-oriented offers.

- **interpreted:** The likely first contracting authority is the invoice-owning customer entity, acting through an employee authorized to disclose records, approve a dossier, and decide whether to dispute.

- **counsel-required:** Submission, negotiation, settlement, admission, payment instruction, representation, and outcome-fee authority must be separately defined.

- **verified:** Carrier calculators, portals, notifications, and existing freight-audit services are incumbent route-arounds.

- **unknown:** No reliable public denominator establishes whether more than 5% of relevant European invoices contain supportable discrepancies.

- **unknown:** No reliable public evidence establishes expected European recovery per accepted dossier, recovery timing, or attribution.

- **interpreted:** A vendor’s self-published 5–20% overcharge or error claim is a marketing assertion and cannot verify the candidate’s 5% premise without an auditable denominator and customer adjudication.

- **interpreted:** The private sample should contain approximately 30–100 consecutive relevant invoices, including clean, unsupported, disputed, and credited outcomes.

- **interpreted:** For every invoice, the proof should record available-at-the-time evidence, reconstruction minutes, missing evidence, claimed discrepancy, customer supportability decision, amount disputed, carrier response, credit outcome, and review cost.

- **interpreted:** The proof should stop if event records cannot reconstruct free time, contract and procedure cannot be determined reliably, or accepted supportable discrepancies remain below the predeclared 5% threshold.

## Remaining Unknowns

- **unknown:** Reachable European payer count and recurring-invoice volume by payer type.

- **unknown:** First-contract decision maker and maximum discretionary proof budget.

- **unknown:** Incidence of supportable discrepancies among unbiased European invoices.

- **unknown:** Expected credit value and probability of recovery per accepted dossier.

- **unknown:** Availability of historical appointment screens, terminal notices, interchange receipts, holds, return records, and communications.

- **unknown:** Reconstruction labor for clean, conflicting, multi-container, and multi-contract cases.

- **unknown:** Carrier, port, lane, tariff, and governing-law variability.

- **unknown:** Customer acceptance of fixed, subscription, or recovery-linked pricing.

- **unknown:** Partner referral economics and conflicts for freight consultants and customs brokers.

- **unknown:** Secure-system and ongoing insurance cost.

- **counsel-required:** Confidentiality, GDPR roles, customs-data restrictions, portal credentials, limitation periods, governing law, legal representation, settlement authority, and outcome-fee legality.

## Indispensable-Premise Check

- **unknown:** The indispensable premise—that more than 5% of an unbiased set of relevant European invoices contains supportable discrepancies whose expected recovery exceeds dossier and customer-review cost—remains unknown.

- **unknown:** Public vendor error-rate claims do not close that premise because their samples, geography, denominators, definitions, and adjudication methods are not disclosed.

- **contradicted:** Any indispensable premise that U.S. FMC billing rules automatically govern European shipments is directly contradicted.

- **contradicted:** Any indispensable premise that a plausible delay narrative is sufficient is directly contradicted by CMA CGM’s day-specific contemporaneous-evidence requirements.

- **unknown:** No indispensable premise specific to a retrospective, customer-authorized, one-carrier proof was directly contradicted.

## Query And Source Trace

### Dated direct-URL ledger

- **verified:** 2025-06-10 publication; accessed 2026-08-22 — Eurostat NACE Rev. 2.1 classification: https://ec.europa.eu/eurostat/documents/3859598/21633320/KS-GQ-24-007-EN-N.pdf

- **verified:** Accessed 2026-08-22 — Eurostat structural-business-statistics overview: https://ec.europa.eu/eurostat/en/web/structural-business-statistics

- **verified:** Data through 2025-03-31; accessed 2026-08-22 — FMC aggregate D&D data: https://www.fmc.gov/detention-and-demurrage/

- **verified:** 2025-04 publication; accessed 2026-08-22 — FMC FY2024 Annual Report: https://fmc.gov/wp-content/uploads/2025/04/FY-2024-Annual-Report.pdf

- **verified:** 2024-02-23 publication; accessed 2026-08-22 — FMC final billing-rule announcement: https://www.fmc.gov/articles/fmc-publishes-final-rule-on-detention-and-demurrage-billing-practices/

- **verified:** 2025-06-16 guidance update; accessed 2026-08-22 — CMA CGM D&D evidence requirements: https://www.cma-cgm.com/local/united-states/detention-and-demurrage

- **verified:** Accessed 2026-08-22 — Maersk Spot terms, confidentiality, supporting records, authority, time bars, law, and jurisdiction: https://terms.maersk.com/terms-spot-booking

- **verified:** 2021 publication; accessed 2026-08-22 — ONE Europe and Africa D&D calculator announcement: https://eua.one-line.com/news/detention-and-demurrage-dd-calculator-now-live-europe-and-africa

- **verified:** Accessed 2026-08-22 — Sellexio pricing and free-audit offer: https://www.sellexio.co/pricing

- **verified:** Accessed 2026-08-22 — DemurrageIQ pilot and monthly-price offer: https://auditdemurrageiq.com/

### Queries

1. `site:ec.europa.eu/eurostat freight transport support activities enterprises Europe NACE 52.29 number enterprises`
2. `ocean carrier detention demurrage invoice dispute procedure Europe official supporting documents`
3. `detention demurrage dispute software pricing official invoice audit`
4. `site:eur-lex.europa.eu customs broker shipment records confidentiality GDPR processor freight invoice`
5. `ocean carrier detention demurrage free time calculator portal Europe official`
6. `demurrage detention invoice audit pilot implementation cost secure document processing`
7. `site:eur-lex.europa.eu maritime demurrage detention invoice dispute regulation European Union`
8. `demurrage detention invoice error incidence study audit carrier invoices`

