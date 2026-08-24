# Shadow Finalist SFIN-02 — D-008

Shadow-only diagnostic artifact. It is not eligible for downstream routing and cannot alter the frozen live cohort.

## Frozen Level-2 Dossier

# Level-2 D-008 — Retail Deduction Recovery Queue

## Problem And Payer Evidence

The payer is a supplier’s controller, finance director, or fractional CFO responsible for retailer accounts receivable. The relevant denominator is not all retailers or all suppliers, but suppliers with recurring retailer short-pays, accessible remittance evidence, and deductions too small or fragmented for existing staff to pursue economically. No public source found establishes that denominator for Europe or the share writing off at least €2,000 per month in supportable claims.

The workflow itself is verified. Oracle describes customer short-pays becoming claims that must be assigned, researched, classified as valid or invalid, approved, and settled. Its current documentation says deductions may represent 5–15% of revenue and that 5.1–10% may be invalid or unauthorized, but attributes those figures only to unspecified “market surveys”; they are directional vendor evidence, not a representative denominator. The UK Groceries Code Adjudicator records that smaller suppliers may decline to defend claims because of resource cost or fear of retaliation, and that supporting agreements, sales data, and calculation methodology are necessary to challenge deductions.

Direct willingness proxies exist but are not representative. ClearChain advertises an end-to-end service at US$5,000 per month for brands with roughly US$5 million or more in retail revenue. Deduction Clerk advertises a US$189-per-month packet-building product while leaving portal submission to the supplier. These purchases and offers verify paid substitutes; they do not verify European demand, typical recoveries, or the proposed threshold.

Counterevidence is material. Oracle and other ERP suites already provide centralized claim ownership, research, approval, settlement, and write-off workflows. Suppliers may therefore solve the problem through configuration, an internal analyst, or a managed-service provider. Some deductions are contractually valid, lack proof, have expired, or are uneconomic to dispute. A vendor’s claimed recovery rate cannot establish typical collectible value.

## Proposed Transaction

The initial transaction is a read-only historical deduction audit followed by a recovery queue. The supplier provides exports of remittances, invoices, purchase orders, promotion agreements, delivery evidence, credit memos, and its open-deduction ledger. The service returns:

- A line-level queue classified as supportable, unsupported, apparently valid, expired, duplicate, or requiring staff adjudication.
- The applicable reason code, evidence checklist, deadline, retailer process, and proposed dispute packet.
- A reconciliation record connecting submission, retailer response, credit memo, remittance, and cash receipt.

The paid event should be narrowly defined: a low fixed monthly access fee plus an outcome fee only when a retailer-issued credit is matched to a disputed deduction and is received or applied in the supplier’s ledger. Written-off deductions, merely submitted disputes, pending credits, and claims the supplier adjudicates as valid carry no outcome fee. The supplier retains the final validity decision and submission authority.

Plausible, interpreted pilot economics are €300–€1,000 monthly plus 10–20% of verified credits received. A manual historical audit could instead cost €500–€2,000 for one retailer account. At one to four analyst hours per contested claim cluster, plausible delivery cost is €100–€600 per cluster before automation. A private proof can remain below €5,000; a secure multi-customer product with ingestion, audit logs, access controls, and outcome reconciliation plausibly requires €30,000–€80,000. These are operating hypotheses, not observed European prices.

Sensitivity is dominated by supportable value and collection latency. At €2,000 monthly supportable value, a 25% recovery rate and 15% outcome fee generate only €75 in outcome revenue; the fixed fee must cover service cost. At €10,000 supportable value and 50% recovery, the same fee produces €750. Sixty-to-ninety-day retailer response cycles can defer outcome revenue and require several months of working capital.

## Acquisition Route

The first-customer route is through fractional CFOs, EDI consultants, outsourced bookkeepers, and trade-promotion advisers who already see supplier remittances and unresolved retailer balances. The offer is not an ERP replacement: it is a bounded audit of deductions the supplier has already abandoned.

A concrete first engagement would involve one supplier, one retailer, three to twelve months of history, and no portal write access. The partner introduces the service, the supplier exports the records, and supplier staff adjudicate every proposed claim. A paid continuation is requested only after the audit identifies unexpired, evidence-supported value.

The closest substitutes are an internal deduction analyst, ERP claim modules, spreadsheets, outsourced recovery firms, and retailer-specific packet tools. Their incumbent route-around persists because internal staff hold commercial context, retailer relationships, and portal credentials. The proposed service must therefore reduce evidence assembly time without demanding that a supplier surrender control of retailer communications.

Exact access should initially be limited to supplier-authorized document exports and read-only accounting data. Portal credentials should not be collected. Submission should occur through a named supplier employee unless the retailer expressly permits an authorized third party and the supplier grants written agency. Processing personal data requires a controller–processor agreement, documented instructions, confidentiality, security controls, deletion terms, and an approved subprocessor list. Retailer portal terms, dispute authority, contingency-fee treatment, and any activity that could constitute regulated debt collection require jurisdiction-specific counsel.

## Decision-Critical Unknowns

- **VERIFIED:** Retail deductions require research, proof validation, ownership, approval, and settlement; invalid claims exist.
- **VERIFIED:** Direct paid substitutes range from low-cost packet tools to high-price managed recovery.
- **INTERPRETED:** A fixed fee plus a percentage of received credits can align payment with realized value while funding baseline service.
- **INTERPRETED:** One retailer, read-only exports, and supplier-controlled submission are compatible with a part-time private proof.
- **UNKNOWN:** The number of European suppliers with recurring, addressable deductions.
- **UNKNOWN:** Whether a typical target supplier has at least €2,000 per month of unexpired, supportable abandoned claims.
- **UNKNOWN:** Typical invalidity, dispute success, credit issuance, cash collection, and elapsed-time distributions.
- **UNKNOWN:** Partner introduction-to-pilot conversion and willingness to pay the proposed fixed and outcome fees.
- **UNKNOWN:** Whether retailer reason codes, deadlines, and portal procedures can be maintained accurately with part-time operations.
- **UNKNOWN:** Whether suppliers can provide consistent links among remittances, promotions, orders, delivery evidence, credits, and receipts.
- **CONTRADICTED:** A premise that third-party portal automation is universally available; at least one direct substitute explicitly avoids it because portal terms restrict automated third-party logins.
- **CONTRADICTED:** A premise that deductions are generally recoverable; Oracle documents valid claims, claims without proof, approvals, settlements, and write-offs.
- **COUNSEL-REQUIRED:** Retailer portal terms, supplier agency, outcome-fee enforceability, debt-collection characterization, cross-border processing, retention, and professional-liability language.

The cheapest private proof is to audit one supplier’s abandoned deductions without submitting anything. Supplier staff must classify validity, evidence availability, deadline status, collectible amount, and whether they would authorize a dispute. Proof requires actual credits received, not modeled recoveries or vendor testimony.

## Evidence And Sources

Dated direct-URL ledger:

- 2026-08-22 — Oracle, current deductions and settlement overview: [https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26a/faccm/deductions-and-settlement.html](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26a/faccm/deductions-and-settlement.html)
- 2026-08-22 — Oracle, claims research, ownership, approval, and settlement workflow: [https://docs.oracle.com/cd/E18727-01/doc.121/e16295/T544851T544854.htm](https://docs.oracle.com/cd/E18727-01/doc.121/e16295/T544851T544854.htm)
- 2026-08-22 — UK Groceries Code Adjudicator, supplier evidence and recovery-audit practices: [https://www.gov.uk/government/publications/best-practice-statement-forensic-auditing/best-practice-statement-forensic-auditing](https://www.gov.uk/government/publications/best-practice-statement-forensic-auditing/best-practice-statement-forensic-auditing)
- 2026-08-22 — ClearChain, direct managed-service scope, price, and stated timing: [https://useclearchain.com/faq](https://useclearchain.com/faq)
- 2026-08-22 — Deduction Clerk, direct product price, packet workflow, data controls, and portal restriction: [https://deductionclerk.com/](https://deductionclerk.com/)
- 2026-08-22 — Attain Consulting Group, 2021 customer-deduction survey: [https://attainconsultinggroup.com/wp-content/uploads/2021/07/Attain-Survey-2021_05.pdf](https://attainconsultinggroup.com/wp-content/uploads/2021/07/Attain-Survey-2021_05.pdf)
- 2026-08-22 — European Data Protection Board, Article 28 controller–processor obligations: [https://www.edpb.europa.eu/system/files/2024-10/edpb_opinion_202422_relianceonprocessors-sub-processors_en.pdf](https://www.edpb.europa.eu/system/files/2024-10/edpb_opinion_202422_relianceonprocessors-sub-processors_en.pdf)

### Query trace

1. `retail supplier deductions manual reconciliation invalid deductions recovery official documentation`
2. `site:help.spscommerce.com deductions remittance retailer supplier claims documentation`
3. `site:docs.oracle.com retail deductions claims settlement supplier`
4. `site:learn.microsoft.com deduction management customer payments claims`
5. `retailer supplier deduction portal dispute requirements official vendor guide`
6. `Amazon vendor shortage claim dispute documentation official`
7. `Walmart supplier deductions dispute documentation official`
8. `retail supplier chargeback deduction recovery pricing percentage recovered`
9. `accounts receivable deduction management pricing monthly supplier recovery service`
10. `retail deductions write offs benchmark survey supplier finance`
11. `EU retailer supplier payment deductions claims law late payments official`
12. `GDPR processor accounts receivable documents supplier official guidance`

## Frozen Fact Closure

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

