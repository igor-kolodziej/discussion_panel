# Fact-Closure Report — W2-L2-006

**Candidate:** Stationary-battery passport custodian  
**Research date:** 2026-08-22 CEST  
**Overall status:** `interpreted`

## Closure finding

The legal and operational basis for third-party custody is verified: the responsible economic operator may authorize another operator in writing, passport information must remain current, and an authorized operator may store and process it subject to strict access, use, continuity, and interoperability rules.

Commercial evidence shows two sharply different markets:

- Commodity self-service software is advertised from free to €149/month, with no onboarding fee.
- A managed provider advertises €5,000 per organization annually, €50 activation per industrial battery, and €10 annual maintenance per live industrial-battery passport.

A Siemens Energy proof of concept also required data-readiness analysis, API integration, supplier onboarding, workflow definition, training, and implementation support—work materially beyond QR-code hosting.

However, no public fact establishes that a Polish importer, private-label distributor, or integrator will authorize and pay this particular independent custodian. The actual Polish payer denominator, buyer budget, granted access to upstream/BMS data, and acquisition conversion through installers remain private premises.

**Is the indispensable premise directly contradicted?** **No.**  
It is commercially plausible and supported by advertised managed-service pricing, but it is not directly verified by a signed buyer, disclosed contract, or paid deployment.

## Exact public facts closed

| Fact | Status | Closure |
|---|---|---|
| Covered industrial batteries above 2 kWh require passports from 18 February 2027 | `verified` | Directly stated in Article 77. |
| The placing operator remains responsible for accuracy, completeness, and currency | `verified` | Responsibility cannot be transferred to the custodian merely by contract. |
| Another operator may act under written authorization | `verified` | The proposed contractual role is legally contemplated. |
| Authorized operators may store and process passport data | `verified` | Article 78 expressly allows this role. |
| Authorized processors cannot sell, reuse, or process the data outside the service | `verified` | Data enclosure and unrelated analytics are unavailable as defensibility. |
| The passport must remain available after the responsible operator ceases activity | `verified` | Continuity is a real continuing service obligation. |
| Access, update rights, integrity, security, privacy, and interoperability are required | `verified` | Custody entails continuing operational controls, not merely static hosting. |
| The responsible party is the operator placing the finished battery on the market | `verified` | Component suppliers and ordinary installers are not automatically the payer. |
| The Commission describes a decentralized system with data maintained by the responsible operator | `verified` | An independent custodian is possible, but there is no mandatory central vendor. |
| Commodity software is advertised at €0–€449/month for up to 25,000 passports | `verified` | Bare hosting and issuance face severe price pressure. |
| A managed provider advertises €5,000/year per organization, €50 activation, and €10/year per live industrial passport | `verified` | There is a public commercial offer for long-lived service well above commodity unit pricing. |
| Siemens Energy ran a supported pilot covering readiness, APIs, supplier onboarding, workflows, passports, and training | `verified` | Managed implementation work exists in practice, although no price or external buyer contract was disclosed. |
| An EU DPP implementation procurement carries an estimated €250,000 budget | `verified` | This proves budget for DPP implementation work generally, but it concerns construction products and is not direct battery-customer willingness to pay. |
| BDO exposes a register filter for entities placing batteries or accumulators on the market | `verified` | A company-list construction route exists. |
| Aggregate Polish placing-operator count | `unknown` | The BDO result did not provide an aggregate, and its direct open failed. |
| A regional Ostrów Wielkopolski installer advertises storage systems from Solplanet, BYD/Fronius, Huawei, SolarEdge, and Sofar | `verified` | Local installer-to-brand chains can be identified, but the responsible Polish placing entities were not established. |
| Final Article 77(9) legitimate-interest access instrument | `unknown` | The Regulation states the adoption deadline, but this query did not locate and verify the final instrument. |
| Whether the custodian can obtain every needed BMS or restricted field under customer authorization | `counsel-required` | Written authority exists in principle, but field-specific access, purchaser rights, IP restrictions, and the final access instrument must be mapped. |

Primary legal facts come from [Regulation (EU) 2023/1542, Articles 77–78](https://eur-lex.europa.eu/eli/reg/2023/1542/oj?locale=en). Current implementation framing comes from the [European Commission battery-passport page](https://single-market-economy.ec.europa.eu/single-market/digital-product-passport/batteries_en).

## Price, cost, capital, and sensitivity closure

The proposed 8,000–12,000 PLN readiness batch is not disproved by public pricing, but it cannot be sold as ordinary software onboarding:

- [Batteriepasswerk](https://www.batteriepasswerk.com/en/pricing) advertises no setup fee, a free 25-passport pilot, €149/month for 2,000 passports, and €449/month for 25,000.
- [EU Digital Passport Processor](https://www.eudigitalpassportprocessor.com/blog/battery-passport-maintenance-pricing-model) advertises a materially more expensive managed model: €5,000 annually per organization, €50 activation per industrial passport, and €10 annual maintenance per live industrial passport.
- For 500 newly activated industrial passports, the latter published model totals €35,000 in the first year before any exceptional integration work.
- The dossier’s first-proof cost range of 6,000–18,000 PLN against 8,000–12,000 PLN revenue produces a contribution range from **–10,000 PLN to +6,000 PLN before founder labor**.
- At 80 founder hours, readiness revenue alone is 100–150 PLN per founder hour before direct costs.
- Long-lived support, insurance, incident response, customer failure, migration, and records surviving beyond ten years remain unpriced private risks.

The public evidence therefore supports charging above commodity software only when the contract explicitly purchases reconciliation, authorization control, commissioning capture, exception handling, integrations, and continuing custody.

## Remaining private premises

- Number of Polish economic operators placing covered stationary batteries on the market after February 2027.
- Annual covered units per accessible payer.
- Which entity pays when OEM, importer, distributor, private-label brand, and integrator differ.
- Whether an accessible payer will sign written authorization with a small independent custodian.
- Whether upstream manufacturers will provide complete model, conformity, composition, and durability data.
- Availability and contractual usability of BMS exports and dynamic state-of-health data.
- Buyer willingness to pay for managed operations after seeing the low-cost alternatives.
- Actual reconstruction time, exception frequency, support burden, and lifecycle-update frequency.
- Liability allocation for incorrect customer-supplied data.
- Cost and availability of professional-indemnity, cyber, continuity, and long-duration hosting arrangements.
- Whether installer introductions reach the responsible placing operator rather than only a reseller or installer.
- Whether successful readiness work converts into prepaid annual custody.

## Cheapest resolving test

Run a paper-first paid authorization test before building production infrastructure:

1. Through the existing installer relationship, identify the exact responsible economic operator for one installed battery model using invoices, brand ownership, and import/distribution documents.
2. Offer the existing fixed-scope ten-passport readiness batch for 8,000 PLN.
3. Require before technical work:

   - signed Article 77 authorization;
   - identification of the legally responsible entity;
   - access to the manufacturer data pack and serial records;
   - agreement on installer commissioning fields;
   - permission for defined lifecycle updates;
   - a 4,800 PLN advance payment.

4. Commission legal drafting only after commercial acceptance.

This costs primarily founder time before acceptance; the first external spend is the scoped legal review. A signed authorization plus cleared advance payment directly verifies the indispensable premise for the first customer. An unpaid pilot, interview, or non-binding expression of interest would not close it.

## Lawful-structure boundary

- Contract only with, or under explicit authority from, the responsible economic operator.
- Do not represent custody as a transfer of Article 77 responsibility.
- Process passport data only for the contracted service; no resale or unrelated analytics.
- Restrict creation and updates by role and preserve source, author, time, and reason.
- Provide open, documented export and avoid vendor lock-in.
- Maintain security, integrity, privacy, backup, migration, incident-response, and operator-failure continuity.
- Treat personal or site data under separately reviewed controller/processor terms.
- Do not claim notified-body status or that a passport proves complete conformity.
- Handle repurposing, waste-status transfer, and recycling closure according to the responsible party defined by the Regulation.
- Obtain counsel confirmation on the final Article 77(9) access rules, BMS/IP access, liability allocation, GDPR roles, insurance, and continuity arrangements before production custody.

## Query ledger

Exactly eight distinct queries were executed in two batches on **2026-08-22 CEST**. The search interface did not expose reliable per-query clock times, so none are invented.

| ID | Query | Purpose | Result |
|---|---|---|---|
| Q01 | `site:eur-lex.europa.eu Article 77(9) Regulation EU 2023/1542 implementing act battery passport legitimate interest 18 August 2026` | Binding authority and access | Closed core Articles 77–78; final Article 77(9) instrument not located. |
| Q02 | `site:environment.ec.europa.eu battery passport economic operator written authorisation service provider Article 77 batteries regulation FAQ` | Responsible party and implementation status | Confirmed finished-battery placing operator and decentralized maintenance model. |
| Q03 | `site:rejestr-bdo.mos.gov.pl batteries accumulators register producers Poland BDO industrial battery importer` | Polish payer denominator | Confirmed applicable register filter; no aggregate count. |
| Q04 | `battery passport implementation tender procurement budget consultancy 2025 2026` | Direct budget proxy | Found €250,000 EU DPP implementation procurement in another product sector. |
| Q05 | `site:batteriepasswerk.com/en/pricing battery passport pricing managed data services 2026` | Closest commodity substitute | Closed free and low-cost SaaS pricing. |
| Q06 | `digital battery passport managed service pricing onboarding implementation per passport commercial 2026` | Managed-service price and recurring custody | Closed organization, activation, and annual maintenance prices. |
| Q07 | `Poland battery energy storage distributor importer home storage brands installer partnership 2026 Ostrów Wielkopolski` | Founder-accessible first-customer route | Found a regional installer and named storage brands; placing operators remain unidentified. |
| Q08 | `battery passport customer case study implementation OEM supplier data onboarding commercial 2025 2026` | Actual implementation work and route-around | Found Siemens Energy proof of concept with managed data and integration work; no price. |

No query result was transferred to another query’s purpose.

## Source ledger

Eight source-open attempts were made. One returned an internal error; the Siemens page opened but exposed no substantive extract, so its indexed commercial case-study text is treated cautiously.

| ID | Query | Source | Evidence and limitation |
|---|---|---|---|
| S01 | Q01 | [Regulation (EU) 2023/1542](https://eur-lex.europa.eu/eli/reg/2023/1542/oj?locale=en) | Primary law: scope, written authorization, responsibility, storage, access, continuity, reuse restrictions, and lifecycle transfers. |
| S02 | Q02 | [European Commission: Digital Product Passport for Batteries](https://single-market-economy.ec.europa.eu/single-market/digital-product-passport/batteries_en) | Primary authority: responsible finished-battery operator, decentralized model, implementation timeline. |
| S03 | Q03 | [Polish BDO entity register](https://rejestr-bdo.mos.gov.pl/Registry/Index?pageNumber=43&placeType=residenceOrBusinessAddress&t=1747353600157&tables=ActivityScope5Table1) | Official result identified the battery/accumulator placer filter; direct open returned an internal error and no aggregate. |
| S04 | Q04 | [EU Publications Office procurement](https://op.europa.eu/en/web/public-procurement/procurement-details/-/procurement/ae396e48-cb8f-3163-a594-5aa8ea197838) | €250,000 estimated DPP implementation framework; construction products, not battery-customer spend. |
| S05 | Q05 | [Batteriepasswerk pricing](https://www.batteriepasswerk.com/en/pricing) | Current vendor-advertised self-service pricing; no evidence of customer count or realized contracts. |
| S06 | Q06 | [EU Digital Passport Processor pricing](https://www.eudigitalpassportprocessor.com/blog/battery-passport-maintenance-pricing-model) | Current advertised managed pricing and recurring maintenance; sales and delivery performance unverified. |
| S07 | Q07 | [Brewa storage systems in Ostrów Wielkopolski](https://www.brewa.pl/produkty-i-uslugi/magazyn-energii-ostrow-wlkp.html) | Regional installer presence and named brands; does not establish importer identity or willingness to introduce. |
| S08 | Q08 | [Siemens Energy battery-passport proof of concept](https://references.siemens.com/en/reference/siemens-energy-poc-batterypassport) | Indexed case description covers readiness, APIs, supplier workflows, passport generation, and training; no disclosed price or independent placing-operator contract. |

## Evidence ledger

| ID | Evidence | Source | Status |
|---|---|---|---|
| E01 | Passport duty begins 18 February 2027 for industrial batteries above 2 kWh | S01 | `verified` |
| E02 | Passport includes model and individual-use information | S01 | `verified` |
| E03 | The placing operator must keep information accurate, complete, and current | S01 | `verified` |
| E04 | Another operator may act under written authorization | S01 | `verified` |
| E05 | Authorized operators may store passport data | S01 | `verified` |
| E06 | Authorized processors may not sell or reuse data beyond the service | S01 | `verified` |
| E07 | Passport availability must survive cessation of the responsible operator | S01 | `verified` |
| E08 | Access, update rights, authentication, integrity, security, and privacy are mandatory | S01 | `verified` |
| E09 | Responsible party is the operator placing the finished battery on the market | S02 | `verified` |
| E10 | The Commission describes decentralized passport operation | S02 | `verified` |
| E11 | Final Article 77(9) access instrument was not established in this pass | S01–S02 | `unknown` |
| E12 | BDO provides a register category for battery/accumulator placers | S03 | `verified` |
| E13 | Aggregate Polish payer count | S03 | `unknown` |
| E14 | EU DPP implementation procurement has a €250,000 estimated value | S04 | `verified` |
| E15 | That procurement is a direct battery-payer budget proxy | S04 | `contradicted` |
| E16 | Free and low-cost battery-passport SaaS is publicly advertised | S05 | `verified` |
| E17 | Managed recurring custody pricing above commodity SaaS is publicly advertised | S06 | `verified` |
| E18 | Advertised managed pricing proves realized willingness to pay | S06 | `unknown` |
| E19 | Local installer-to-brand chains exist around Ostrów Wielkopolski | S07 | `verified` |
| E20 | That route reaches the responsible placing operator | S07 | `unknown` |
| E21 | A major battery-storage organization has performed a managed passport pilot | S08 | `verified` |
| E22 | Data readiness, APIs, supplier onboarding, workflows, and training are real implementation tasks | S08 | `verified` |
| E23 | Polish smaller importers will buy the same managed work from an independent custodian | S05–S08 | `unknown` |
| E24 | Written authority guarantees access to all manufacturer, restricted, and BMS data | S01 | `counsel-required` |
| E25 | The indispensable premise is directly contradicted | S01–S08 | `unknown`; no public source directly contradicts it |

**Research-control record:** exactly eight web queries; eight source-open attempts; no contacts; no file edits.
