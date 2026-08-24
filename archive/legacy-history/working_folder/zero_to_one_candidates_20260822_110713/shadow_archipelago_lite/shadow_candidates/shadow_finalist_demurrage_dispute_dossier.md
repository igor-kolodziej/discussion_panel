# Shadow Finalist SFIN-06 — D-003

Shadow-only diagnostic artifact. It is not eligible for downstream routing and cannot alter the frozen live cohort.

## Frozen Level-2 Dossier

# Level-2 D-003 — D&D Dispute Dossier Builder

## Problem And Payer Evidence

Detention and demurrage charges are economically material. The U.S. Federal Maritime Commission reports that nine ocean carriers collected approximately $15.4 billion in detention and demurrage between April 2020 and March 2025. That is a charge denominator, not an erroneous-invoice denominator. [FMC detention and demurrage data](https://www.fmc.gov/detention-and-demurrage/)

Official recovery evidence also exists. In FY2024 the FMC received 189 charge complaints, investigated 130 as appropriate for the process, and reported $1,874,142 in charges voluntarily refunded or cancelled during the year. The same report includes dismissed claims, confidential settlements, and prolonged proceedings, preserving the contradiction that a disputed charge is not necessarily invalid or recoverable. [FMC FY2024 Annual Report](https://fmc.gov/wp-content/uploads/2025/04/FY-2024-Annual-Report.pdf)

Under the FMC’s U.S. rule, vessel-operating carriers and marine terminal operators generally must issue D&D invoices within 30 days of the last incurred charge; billed parties receive at least 30 days to request mitigation, refund, or waiver; and required invoice information affects payment obligations. These are U.S. rules and cannot be applied automatically to European shipments. [FMC final-rule announcement](https://www.fmc.gov/articles/fmc-publishes-final-rule-on-detention-and-demurrage-billing-practices/)

Carrier procedures illustrate the dossier burden. CMA CGM asks for the bill of lading, invoice number, detailed dispute narrative, contract evidence, interchange receipts, communications, and carefully timestamped appointment screenshots for certain disputes. It states that missing evidence can cause denial for the affected days. [CMA CGM guidance](https://www.cma-cgm.com/local/united-states/detention-and-demurrage)

The payer is normally a freight forwarder, NVOCC, customs broker, importer, exporter, consignee, or drayage operator that receives or passes through D&D invoices. The reachable European payer denominator and the number of invoices subject to supportable discrepancies are unknown. Aggregate charges and complaint recoveries demonstrate stakes, not incidence.

Published willingness proxies include:

- Drayage Shield advertises automated evidence capture and dispute PDFs beginning at $99 per month after beta. [Drayage Shield](https://www.drayageshield.com/)
- Demurly publishes $1 per generated record plus 3.5% of collected demurrage, with annual fleet tiers from $0 to $7,500. Its focus is truck-waiting demurrage rather than ocean-container invoice reconstruction, so it is only a transaction proxy. [Demurly pricing](https://www.demurly.com/pricing)
- Preventive platforms and carrier portals are substitutes. They monitor free time, calculate exposure, and retain evidence before an invoice exists.

The closest substitute is manual reconstruction by operations or finance using the bill of lading, booking, contract, tariff, discharge and gate events, empty-return evidence, customs records, appointment screenshots, and correspondence. Incumbent route-arounds include carrier dispute portals, spreadsheets, calendar alerts, preventive control towers, negotiated extra free time, paying undisputed amounts promptly, or outsourcing the entire freight audit.

## Proposed Transaction

The paid event is not an automatically generated allegation. It is an invoice dossier that an authorized customer employee accepts internally as complete and supportable. The dossier should contain:

- Invoice and billed-party identity.
- Applicable bill of lading, service contract, tariff, and free-time terms.
- Jurisdiction and procedure explicitly identified.
- Container timeline with source and timestamp for every event.
- Day-by-day free-time and charge calculation.
- Evidence of appointments, terminal availability, holds, equipment return, communications, and customer-controlled delays.
- Claimed discrepancy and requested resolution.
- Missing-evidence and limitation warnings.
- Internal approver and final carrier outcome.

A plausible commercial range is 150–500 PLN for a straightforward accepted dossier and 700–2,000 PLN for a multi-container or evidence-heavy dossier. An optional 10–20% fee on an actually recovered credit could be capped, but only where counsel confirms that the arrangement and performed activities are lawful. Clear invoices that produce no dossier should not trigger the fixed dossier fee.

Assuming five accepted dossiers each support 3,000 PLN, total disputed value is 15,000 PLN. A 400 PLN dossier fee plus a 15% recovery fee would cost 4,250 PLN if all credits were recovered. This clears a three-times gross-value relationship only narrowly and fails if recovery or attribution is materially lower. The calculation is illustrative, not a verified customer case.

Manual production could require 45 minutes for a clean, structured single-container record and three hours or more where events, contracts, or communications conflict. At those durations, fixed prices below 500 PLN require strong reuse of carrier formats and event semantics. A private proof could be completed for approximately 10,000–35,000 PLN; secure multi-carrier software, portal workflows, and active deadline coverage could consume 50,000–100,000 PLN.

Exact access requires written customer authorization to process invoices, shipment records, contracts, tariffs, customs and terminal documents, and correspondence; an NDA and data-processing agreement; scoped retention; and customer-controlled portal credentials. The service should draft evidence but should not submit, settle, waive, admit liability, or instruct payment without express authority. Jurisdiction, bill-of-lading terms, legal representation, limitation periods, and recovery fees are counsel-required.

## Acquisition Route

The first-customer path is a freight consultant or customs broker willing to provide a retrospective sample of closed invoices with known outcomes. A closed sample reduces deadline risk and lets operations staff judge supportability without changing live payment behavior.

The proof should:

1. Select one carrier, one port pair, and one customer procedure.
2. Review a small authorized sample containing both disputed and undisputed invoices.
3. Rebuild timelines using only evidence available at the time.
4. Have operations staff label every dossier complete, incomplete, unsupported, or commercially uneconomic.
5. Measure reconstruction time, missing-evidence share, carrier response, and actual credit outcome.
6. Compare the dossier with the customer’s original manual work.

The decisive test is whether more than 5% of relevant invoices contain supportable discrepancies whose expected recovery exceeds dossier and customer-review cost. “Relevant invoices” must be defined before sampling; selecting only known disputes would invalidate incidence measurement.

Carrier portals are both acquisition dependencies and substitutes. Maersk’s Spot terms, for example, require written notice of a disputed item and supporting-document request within 30 days in the described regulated-lane schedule, while also describing a 180-day acceptance waiver. Other Maersk contracts publish different periods, so the applicable contract and lane must control. [Maersk Spot terms](https://terms.maersk.com/terms-spot-booking)

The lowest-cost falsification is approximately 30–100 invoices from one partner, with customer adjudication of supportability, missing evidence, labor, and expected value. If event records cannot reconstruct free time, if procedures differ invoice by invoice, or if accepted discrepancies remain below the 5% threshold, broader automation should stop.

The compounding asset is a permissioned library of carrier and terminal formats, charge definitions, free-time semantics, procedure requirements, evidence types, and final reason codes. Customer contracts, rates, shipment identities, and correspondence must remain segregated.

## Decision-Critical Unknowns

- **Verified:** D&D charges are large in aggregate, and official complaint processes have produced refunds and cancellations.
- **Verified:** Published carrier and regulator procedures require detailed, time-sensitive evidence.
- **Verified:** Direct software vendors publish per-record, subscription, and collection-linked pricing.
- **Interpreted:** Forwarders, customs brokers, importers, and drayage operators with recurring container volume are plausible payers.
- **Unknown:** The reachable European payer denominator.
- **Unknown:** Erroneous-invoice incidence in Europe and whether more than 5% of relevant invoices contain supportable discrepancies.
- **Unknown:** Expected recovery per supportable dossier.
- **Unknown:** Timeline-reconstruction labor and the share that can be automated.
- **Unknown:** Whether retrospective exports preserve appointment availability, terminal notices, correspondence, and event timestamps.
- **Unknown:** European procedure fit across carriers, ports, governing laws, and negotiated contracts.
- **Unknown:** Customer acceptance of the proposed fixed and recovery-linked fees.
- **Unknown:** Partner referral economics and conflict rules.
- **Contradicted:** Aggregate charge volume does not establish invoice error incidence.
- **Contradicted:** A carrier delay, port congestion, or customs hold does not always invalidate D&D; responsibility depends on contract, procedure, evidence, and jurisdiction.
- **Contradicted:** U.S. FMC invoice rules cannot be represented as governing a European shipment without a jurisdiction analysis.
- **Contradicted:** A dossier can fail despite a plausible narrative when required contemporaneous evidence is missing.
- **Counsel-required:** Data-access legality, customs and correspondence confidentiality, limitation periods, governing law, representation, claim submission, settlement authority, and outcome-fee structures.

## Evidence And Sources

Dated direct-URL ledger:

- FY2024 report published 2025, 2026-08-22 accessed — FMC complaints, refunds, dismissals, and proceeding duration: [https://fmc.gov/wp-content/uploads/2025/04/FY-2024-Annual-Report.pdf](https://fmc.gov/wp-content/uploads/2025/04/FY-2024-Annual-Report.pdf)
- 2026-08-22 accessed — FMC aggregate D&D charges through 2025 Q1: [https://www.fmc.gov/detention-and-demurrage/](https://www.fmc.gov/detention-and-demurrage/)
- 2024-02-23 published, 2026-08-22 accessed — FMC final billing-rule announcement: [https://www.fmc.gov/articles/fmc-publishes-final-rule-on-detention-and-demurrage-billing-practices/](https://www.fmc.gov/articles/fmc-publishes-final-rule-on-detention-and-demurrage-billing-practices/)
- 2026-08-22 accessed — FMC carrier-audit best practices for disputes and invoices: [https://www.fmc.gov/databases-and-publications/vessel-operating-common-carrier-vocc-audit-program/](https://www.fmc.gov/databases-and-publications/vessel-operating-common-carrier-vocc-audit-program/)
- 2025-06-16 guidance update, 2026-08-22 accessed — CMA CGM evidence and deadline requirements: [https://www.cma-cgm.com/local/united-states/detention-and-demurrage](https://www.cma-cgm.com/local/united-states/detention-and-demurrage)
- 2026-08-22 accessed — Maersk Spot invoice-dispute terms and time bars: [https://terms.maersk.com/terms-spot-booking](https://terms.maersk.com/terms-spot-booking)
- 2026-07-21 edited, 2026-08-22 accessed — Forto’s Europe and Poland tariff links and event definitions: [https://help.forto.com/en/articles/3966978](https://help.forto.com/en/articles/3966978)
- 2026-08-22 accessed — Demurly direct per-record, collection, and annual pricing: [https://www.demurly.com/pricing](https://www.demurly.com/pricing)
- 2026-08-22 accessed — Drayage Shield beta scope and advertised post-beta price: [https://www.drayageshield.com/](https://www.drayageshield.com/)

### Query trace

1. `site:fmc.gov detention demurrage complaints refunds official charges`
2. `site:fmc.gov detention demurrage billing practices final rule 2024`
3. `site:ec.europa.eu demurrage detention container charges complaint`
4. `ocean carrier demurrage detention tariff Europe official`
5. `demurrage detention dispute software pricing`
6. `container demurrage invoice dispute case prolonged customer`
7. `freight forwarder demurrage detention dispute process documentation`
8. `customs broker demurrage detention audit service Europe`
9. `Maersk demurrage detention dispute invoice official terms Europe`
10. `Hapag Lloyd demurrage detention invoice dispute official`
11. `CMA CGM demurrage detention dispute claim time limit`
12. `detention demurrage invoice error incidence survey`

## Frozen Fact Closure

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

