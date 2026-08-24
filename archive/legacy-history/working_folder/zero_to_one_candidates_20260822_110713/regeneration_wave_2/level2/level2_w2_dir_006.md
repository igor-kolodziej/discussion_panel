# W2-L2-006 — Stationary-battery passport custodian

**Research timestamp:** 2026-08-22T14:43:46+02:00  
**Founder context:** Warsaw-based solo data scientist; five hours/day while employed; approximately 100,000 PLN available; contractors, advisers and later hiring permitted; family access to a seven-person renewable installer near Ostrów Wielkopolski.  
**Concept status:** Pre-product and pre-revenue. Regulation, implementation work and competing commercial products already exist; no buyer commitment or paid usage was supplied.

## 1. Transaction

A manufacturer, importer, private-label distributor or storage integrator that places a qualifying battery on the EU market gives the custodian written authority to:

1. create the battery’s unique electronic record;
2. publish the required public and restricted-access information;
3. attach commissioning information supplied by the installer;
4. accept authorized lifecycle updates;
5. preserve provenance and an audit history;
6. keep the record accessible until recycling; and
7. provide portable export and continuity arrangements.

The first paid event is the creation and contractual handover of live passports for a commissioned batch.

This is a custody and data-operations service, not a transfer of regulatory responsibility. Under Article 77, the placing operator remains responsible for accuracy, completeness and currency, although it may authorize another operator in writing. The passport must use open, interoperable, machine-readable data, avoid vendor lock-in, preserve integrity and respect role-based access. An authorized processor may not sell or reuse passport data outside the contracted service. [Regulation (EU) 2023/1542, Articles 77–78](https://eur-lex.europa.eu/eli/reg/2023/1542/oj?locale=en)

## 2. Problem and payer evidence

### Verified evidence

From 18 February 2027, every industrial battery with capacity greater than 2 kWh placed on the market or put into service must have a battery passport. The same rule covers LMT and EV batteries. Covered passports contain both model-level and individual-battery information, including information arising from use. [Regulation, Article 77](https://eur-lex.europa.eu/eli/reg/2023/1542/oj?locale=en)

For stationary battery energy-storage systems using a BMS, performance, state-of-health and expected-lifetime data create additional implementation work. Battery Pass guidance identifies different data applicability and connectivity constraints across industrial battery types. [Battery Passport Content Guidance](https://thebatterypass.eu/assets/images/content-guidance/pdf/2023_Battery_Passport_Content_Guidance.pdf)

The passport is not merely a linked PDF. It requires a unique identifier, data carrier, structured data, access rights and interoperable transfer. CIRPASS describes third-party “DPP-as-a-Service” storage, processing and backup as an architectural role. [CIRPASS DPP System Architecture](https://cirpassproject.eu/wp-content/uploads/2024/06/D3.2v1.9.pdf)

Poland had more than 47,000 prosumer battery systems representing 258 MW at the end of 2024, plus 15.7 MW in systems above 50 kW. Capacity-market auctions had contracted 4.3 GW of BESS capacity for 2027–2029 delivery. These figures demonstrate a growing physical population but do not identify the number of placing operators or the annual number of post-February-2027 passports. [Polish Economic Institute](https://pie.net.pl/wp-content/uploads/2025/10/PEI_Weekly_EN_41-2025.pdf)

### Interpretation

The costly part for a smaller importer is likely to be obtaining reliable source data, reconciling manufacturer and installer records, controlling updates, and preserving the record through ownership and service events—not generating a QR code.

The likely initial payer is an importer or private-label distributor with several battery models and insufficient internal compliance/data infrastructure. Installers can distribute the service and supply commissioning events, but an installer that merely installs a battery already placed on the market may not own the passport obligation.

### Unknown

No evidence in the fixed source set establishes:

- current budgets allocated by Polish importers;
- willingness to pay for independent custody rather than OEM hosting;
- the number of relevant Polish placing operators;
- the annual number of newly placed Polish stationary batteries above 2 kWh;
- typical manual reconstruction cost per battery;
- whether an importer will grant a small custodian the required authority.

## 3. Incentive and power map

| Actor | Contribution | Incentive | Power or exposure |
|---|---|---|---|
| Manufacturer | Model, composition, conformity, durability and supply-chain data | Preserve EU market access; reduce repeated customer requests | Can withhold data or offer its own portal |
| Importer/private-label distributor | Placing-operator identity, models, serial batches and authorization | Meet obligations without building an internal platform | Usually selects and pays the custodian; retains responsibility |
| Storage integrator | System configuration and customer handover | Bundle compliance with a storage project | May become the placing operator depending on branding/import structure |
| Installer | Serial capture, commissioning date, site/system mapping | Faster commissioning and fewer later evidence requests | Controls the last reliable physical-data capture point |
| Custodian | Identity, record creation, validation, hosting, access control and audit trail | Setup, custody, per-passport and update revenue | Contractual control only; cannot acquire regulatory responsibility or unrestricted data rights |
| Asset owner | Usage and ownership information; authorization for some events | Warranty, service, resale and recycling evidence | May refuse telemetry or personal/site information |
| Repairer/second-life operator | Repair, repurposing and condition events | Demonstrate residual value and lawful handoff | A new placing operator after repurposing assumes passport responsibility |
| Recycler/PRO | Waste and recycling events | Trace material recovery and close the record | Responsibility can transfer at waste status; passport ends after recycling |
| Market-surveillance authority | Requests evidence and corrective action | Enforcement | Can require correction, withdrawal or recall |
| OEM or horizontal DPP vendor | Portal, identifiers and hosting | Retain account and data relationship | Can make an independent custodian unnecessary |

The power bottleneck is the placing operator’s authorization and the manufacturer’s data access. The installer has distribution and event-capture leverage but cannot cure missing upstream information.

## 4. Payer denominator

### Verified physical denominator

- More than **47,000** Polish prosumer storage systems at end-2024.
- **258 MW** of prosumer storage capacity.
- **15.7 MW** of Polish storage above 50 kW.
- **4.3 GW** contracted for delivery in 2027–2029.

These are system and capacity figures, not payer counts. Existing systems placed before the passport start date should not be assumed to require retrospective passports.

### Legal-administrative denominator

The Polish BDO site provides a public entity register, but the fixed query and opened page did not expose an aggregate for entities placing industrial batteries on the market. [BDO entity register](https://rejestr-bdo.mos.gov.pl/Registry/Index?pageNumber=289&placeType=residenceOrBusinessAddress&tables=ActivityScope5Table1)

### Planning denominators — assumptions only

| Geography/stage | Placing operators usable for planning | New covered stationary batteries/year |
|---|---:|---:|
| Initial western/central Poland channel | 20–50 | 2,000–8,000 |
| Poland after channel expansion | 100–300 | 10,000–30,000 |
| Multi-country importer and distributor portfolios | 500–1,500 | 500,000–3,000,000 |

These ranges require a separately constructed company list and shipment evidence before being used as market facts.

## 5. Offer, price and unit economics

### Proposed offer

**Paid readiness batch: 8,000–12,000 PLN**

- one placing operator;
- one or two battery models;
- source-to-commissioning data map;
- up to ten live or pre-production passports;
- written authorization template;
- public/restricted field separation;
- JSON/CSV export;
- update and continuity procedure.

**Production pricing assumption**

- onboarding: **12,000–18,000 PLN** per payer;
- annual custody minimum: **9,600–24,000 PLN**;
- managed creation: **10–30 PLN per battery**, falling with volume;
- lifecycle update: **4–10 PLN**;
- custom ERP/BMS connector: separately scoped.

This price requires human data operations, authorization controls, commissioning capture and lifecycle custody. It cannot compete as a bare QR/hosting product.

### Competitive price evidence

Batteriepasswerk advertises:

- a free plan for one model and 25 passports;
- €149/month for up to 2,000 passports;
- €449/month for up to 25,000 passports;
- enterprise service from €1,290/month;
- €0.05 for excess passports.

Its advertised effective software prices reach €0.89 and €0.22 per passport. [Batteriepasswerk pricing](https://www.batteriepasswerk.com/en/pricing)

Siemens markets an available DPP4.0 SaaS product with starter packages, integrations and tiered company licences. Public pricing was not found in the fixed search. [Siemens DPP4.0](https://www.siemens.com/en-us/industries/batteries/battery-passport/)

### Illustrative first-year customer economics

Assumptions: one importer, two models, 500 batteries and 100 lifecycle updates.

| Item | Amount |
|---|---:|
| Onboarding | 12,000 PLN |
| Annual custody | 12,000 PLN |
| 500 passports × 25 PLN | 12,500 PLN |
| 100 updates × 8 PLN | 800 PLN |
| **Revenue** | **37,300 PLN** |
| Data operations and support | 6,000 PLN |
| Hosting, monitoring and backup allocation | 2,500 PLN |
| Identifier/QR and communications allocation | 1,000 PLN |
| Security/legal allocation | 1,000 PLN |
| **Direct cost** | **10,500 PLN** |
| **Gross profit** | **26,800 PLN** |
| **Gross margin** | **71.8%** |

The direct-cost figures are operating assumptions, not supplier quotes. Founder time should be recorded at an internal cost even when no salary is drawn.

### Cash timing

- 60% of onboarding at signature; 40% at first live passport.
- Annual custody paid in advance.
- Passport batches prepaid or invoiced monthly on 14-day terms.
- Custom integration: 50% in advance, 30% at test handoff, 20% at production.
- Maintain a continuity and migration reserve rather than treating all prepaid custody revenue as immediately available cash.
- Do not finance customer integrations from unpaid future unit fees.

## 6. Founder-wealth cases

All figures are PLN and describe the stated year, not cumulative revenue. Company values are operating values excluding surplus retained cash. Founder wealth equals founder ownership times operating value plus distributions actually received; retained company cash is not added separately.

### Conservative — year 7

| Variable | Assumption |
|---|---:|
| Paying operators | 80 |
| New passports/year | 75,000 |
| Lifecycle updates/year | 50,000 |
| Annual custody: 80 × 18,000 | 1.44m |
| Passports: 75,000 × 18 | 1.35m |
| Updates: 50,000 × 6 | 0.30m |
| 25 onboardings × 12,000 | 0.30m |
| **Revenue** | **3.39m** |
| Gross margin | 68% |
| Gross profit | 2.31m |
| Operating margin | 10% |
| Operating profit | 0.34m |
| Founder capital | 90,000 |
| Debt | None |
| External equity | None |
| Founder ownership | 90% after employee/adviser equity |
| Reinvestment | 95% of after-tax distributable cash |
| Optional distributions | 5%; modeled cumulative founder receipts 0.10m |
| Operating value assumption | 1.5× revenue = 5.09m |
| **Founder wealth in year 7** | **Approximately 4.68m** |

### Expected — year 7

| Variable | Assumption |
|---|---:|
| Paying operators | 220 |
| New passports/year | 400,000 |
| Lifecycle updates/year | 250,000 |
| Annual custody: 220 × 20,000 | 4.40m |
| Passports: 400,000 × 14 | 5.60m |
| Updates: 250,000 × 5 | 1.25m |
| 60 onboardings × 15,000 | 0.90m |
| **Revenue** | **12.15m** |
| Gross margin | 75% |
| Gross profit | 9.11m |
| Operating margin | 20% |
| Operating profit | 2.43m |
| Founder capital | 100,000 |
| Outside capital | 1.5m seed/angel equity |
| Debt | Up to 0.5m working-capital facility, unused unless receivables require it |
| Founder ownership | 76% after 15% investor ownership and employee pool |
| Reinvestment | 95% of after-tax distributable cash |
| Optional distributions | 5%; modeled cumulative founder receipts 0.25m |
| Operating value assumption | 3× revenue = 36.45m |
| **Founder wealth in year 7** | **Approximately 27.95m** |

### Strong success — year 8

| Variable | Assumption |
|---|---:|
| Paying operators | 650 |
| New passports/year | 2.0m |
| Lifecycle updates/year | 1.4m |
| Annual custody: 650 × 22,000 | 14.30m |
| Passports: 2.0m × 10 | 20.00m |
| Updates: 1.4m × 4 | 5.60m |
| 150 onboardings × 18,000 | 2.70m |
| **Revenue** | **42.60m** |
| Gross margin | 80% |
| Gross profit | 34.08m |
| Operating margin | 30% |
| Operating profit | 12.78m |
| Founder capital | 100,000 |
| Outside capital | 7.0m across expansion rounds |
| Debt | Up to 2.0m receivables/working-capital facility |
| Founder ownership | 58% fully diluted |
| Reinvestment | 100% of after-tax distributable cash |
| Distributions | None modeled |
| Operating value assumption | 4× revenue = 170.40m |
| **Founder wealth in year 8** | **Approximately 98.83m** |

The valuation multiples and ownership outcomes are scenario assumptions. They are especially sensitive to recurring-revenue quality, customer concentration, standards compliance and dependence on manual services.

## 7. Acquisition route

### First ten customers

1. Use the family installer to map one complete distributor-to-installation chain.
2. Identify the placing operator for each battery brand handled by that installer.
3. Sell one paid readiness batch to the most accessible importer or private-label distributor.
4. Use the resulting commissioning workflow with two additional installer partners.
5. Approach the family firm’s renewable wholesalers for introductions to their storage-brand managers.
6. Target smaller brands lacking a Polish compliance/data team.
7. Offer a fixed-scope batch rather than a platform migration.
8. Require the placing operator—not merely the installer—to sign authorization.
9. Convert completed batches into annual custody contracts.
10. Keep the first ten customers to a small number of repeatable battery models.

Likely founder workload during employment: discovery calls, data mapping and rule logic. Contract out legal drafting, security review, front-end work and production operations.

### First one hundred customers

- White-label the commissioning workflow for regional installers and wholesalers.
- Give distributors a portfolio dashboard across several battery brands.
- Partner with conformity, LCA and supply-chain-data specialists without representing the custodian as a notified body.
- Create importer-focused implementation packs for Poland, Czechia, Slovakia and Germany.
- Build reusable mappings for common OEM documentation and BMS exports.
- Use installer referrals as the principal channel; avoid consumer marketing or founder-led media distribution.
- Employ customer-success/data-operations staff before accepting large portfolios.
- Maintain one custody contract per responsible operator even when an installer distributes the service.

## 8. Control and compounding asset

The compounding asset is the authorized, provenance-preserving lifecycle record:

- persistent product identities;
- verified model templates;
- supplier-document mappings;
- commissioning events;
- repair and ownership handoffs;
- state-of-health history;
- second-life links;
- recycler closure events;
- validation rules and exception patterns;
- installer and distributor integrations.

Control is contractual and operational, not ownership of customer data. Open export and the prohibition on secondary reuse limit lock-in. Defensibility therefore has to come from trusted custody, data quality, event coverage, integrations and continuity—not data enclosure.

## 9. Incumbent route-around

A payer can bypass the custodian by:

- using the OEM’s own passport portal;
- requiring its foreign manufacturer to operate the record;
- purchasing low-cost self-service software;
- extending an ERP/product-information system;
- using Siemens or another horizontal DPP vendor;
- retaining spreadsheets and QR-linked documents until challenged;
- placing only brands that deliver a complete passport;
- moving responsibility to a private-label or integration entity willing to operate the record.

Batteriepasswerk’s free and low-cost tiers place strong pressure on bare hosting prices. Siemens can bundle passports with industrial data infrastructure. The proposed custodian therefore needs a narrow advantage in multi-brand importer onboarding, installer commissioning capture, managed updates, export and continuity.

## 10. Rule and constraint classification

### Binding rules verified in the Regulation

- The passport applies from 18 February 2027 to industrial batteries above 2 kWh placed on the market or put into service.
- A QR code links to a unique identifier.
- The responsible placing operator must keep information accurate, complete and current.
- Another operator may act under written authorization.
- Data must be structured, searchable, machine-readable and interoperable without vendor lock-in.
- Public and restricted information require different access rights.
- Authorized data operators cannot sell or reuse data beyond the service.
- Authentication, integrity, security and privacy are required.
- Availability must survive the responsible operator ceasing activity.
- Repurposed or remanufactured batteries receive a new passport linked to the original.
- Responsibility transfers on repurposing and again at waste status as prescribed.
- The passport ceases after recycling.

Manufacturers and importers also have separate ten-year technical-documentation duties. That ten-year period should not be mistaken for a fixed passport lifetime; the passport remains relevant until recycling. [Regulation (EU) 2023/1542](https://eur-lex.europa.eu/eli/reg/2023/1542/oj?locale=en)

### Implementation-dependent constraints

- Article 77(9) called for an implementing act by 18 August 2026 specifying legitimate-interest access. The limited source set did not establish the final act’s publication or contents.
- The Commission says further delegated and implementing acts are part of the Regulation’s continuing implementation. [European Commission batteries page](https://environment.ec.europa.eu/topics/waste-and-recycling/batteries_en)
- Battery Pass’s 2023 guidance now notes that DIN-DKE-SPEC 99100 supersedes it for data attributes.
- Interoperability, identifier and registry interfaces may still alter technical work.

### Commercial constraints

- OEM cooperation is not assured.
- BMS data can be proprietary or unavailable.
- A low-volume importer may expect its manufacturer to absorb the cost.
- Long-lived availability creates liability beyond the initial subscription.
- Customer concentration can be high when one distributor accounts for many passports.
- Data quality, not storage, may dominate operating cost.

## 11. Lawful operating structure

1. Contract with the economic operator responsible under Article 77.
2. Obtain explicit written authority covering creation, storage and defined updates.
3. State that legal responsibility for accuracy remains with that operator.
4. Maintain separate data-controller/processor terms where personal or site data are involved.
5. Limit processing to the custody service; prohibit resale and unrelated analytics.
6. Record source, author, time and reason for every change.
7. Permit only role-authorized updates.
8. Provide open, documented exports and identifier-resolution continuity.
9. Maintain backup, incident response, migration and business-failure arrangements.
10. Link new passports correctly after repurposing or remanufacturing.
11. Transfer operational control at waste status under the responsible party’s instructions.
12. Close the passport only upon verified recycling.
13. Avoid statements that the custodian is a notified body or that a passport proves complete product conformity.
14. Never alter manufacturer-originated data without provenance and authorization.

## 12. Dependencies

- Written authorization from the placing operator.
- Reliable manufacturer model and conformity data.
- Serial or batch identifiers captured before or during commissioning.
- Stable identifier and QR process.
- Current data model and access-right implementation.
- OEM/BMS export or an acceptable manual update path.
- Installer adoption of the commissioning capture workflow.
- EU-hosted infrastructure, access control, audit logs and backup.
- Contractual continuity if the custodian ceases operating.
- Legal review for data protection, liability and subcontractors.
- Human data operations until common integrations become repeatable.
- Working-capital discipline for prepaid multi-year custody.

## 13. Fastest paid proof and capital at risk

### Six-week proof

- **Week 1:** Choose one importer/distributor reached through the family installer; identify one battery model and responsible operator.
- **Week 2:** Map manufacturer documents, serial data, installer commissioning fields and future event owners.
- **Week 3:** Obtain written authorization and agree on source/provenance rules.
- **Weeks 4–5:** Create up to ten records, QR links, role views, audit history and JSON/CSV export.
- **Week 6:** Commission a small batch and obtain acceptance plus payment.

### Commercial terms

- Charge **8,000–12,000 PLN**.
- Require at least 60% before technical work.
- Exclude conformity certification and unsupported manufacturer-data reconstruction.
- Offer annual custody only after the batch is accepted.

### Capital exposed

| Item | Range |
|---|---:|
| Legal authorization and service terms | 2,000–5,000 PLN |
| Hosting, identity, logging and backup | 1,000–3,000 PLN |
| Contractor implementation/security work | 2,000–7,000 PLN |
| QR/commissioning workflow and contingencies | 1,000–3,000 PLN |
| **Total first proof** | **6,000–18,000 PLN** |
| **First-year founder-funded ceiling** | **80,000 PLN** |

Keep at least 20,000 PLN of the available capital outside product development until paid renewal behavior and operational workload are known.

## 14. Kill criteria

Stop further product spending if any of the following occurs during the first focused outreach and paid batch:

- no placing operator will sign written authorization;
- three accessible importers all insist the OEM must host the passport and will not pay for independent custody;
- a customer cannot obtain mandatory upstream data for even one model;
- buyers will pay only commodity hosting prices while requiring manual collection and liability;
- one ten-passport batch consumes more than 80 founder hours after the workflow has been repeated once;
- export, role separation, provenance or continuity cannot be implemented within the first-proof capital;
- OEM portals prohibit or technically prevent the required handoff;
- buyers demand a conformity opinion or notified-body role;
- the importer/installer responsibility chain cannot be identified contractually;
- paid annual custody does not follow successful batch delivery.

## 15. Decision-critical unknowns

1. Publication and exact contents of the Article 77(9) implementing act.
2. Final registry, interoperability and identifier mechanics applicable in February 2027.
3. Exact Polish payer count and post-deadline annual unit volume.
4. Which party pays across manufacturer, importer, distributor and integrator.
5. OEM willingness to license or export model and BMS data.
6. Required update frequency for dynamic stationary-storage information.
7. Liability allocation when a customer supplies incorrect data.
8. Continuity requirements if a small custodian fails.
9. Willingness to pay for managed custody above low-cost self-service software.
10. Whether installer commissioning is sufficiently differentiated from OEM-hosted issuance.
11. Cost of obtaining carbon-footprint and supply-chain information for smaller importers.
12. Whether ownership or site information introduces material personal-data obligations.
13. Frequency of repair, resale, repurposing and recycling updates.
14. Support burden created by long-lived records.
15. Availability and economics of suitable professional indemnity and cyber insurance.

## 16. Development status

| Layer | Status evidenced in this packet |
|---|---|
| EU obligation | Enacted and directly applicable |
| Passport start date | 18 February 2027 |
| Core architecture | Described in Regulation and CIRPASS work |
| Data guidance | Extensive Battery Pass guidance exists; referenced guidance notes later DIN specification |
| Commission implementation | Ongoing; final Article 77(9) instrument not established by this source set |
| Competitor software | Low-cost self-service and enterprise products publicly marketed |
| Polish physical market | Existing prosumer base and substantial announced/contracted expansion |
| Exact payer market | Not established |
| Custodian product | Not built |
| Customer authorization | Not established |
| Paid proof | Not performed |

## 17. Research ledgers

All queries were executed on 2026-08-22 during the session completed at **14:43:46 CEST**. The search interface did not expose separate per-query clock times.

### Query ledger — exactly eight distinct queries

| ID | Query | Purpose |
|---|---|---|
| Q01 | `site:eur-lex.europa.eu Regulation (EU) 2023/1542 battery passport Article 77 industrial battery 2 kWh 18 February 2027` | Binding scope and responsibility |
| Q02 | `site:environment.ec.europa.eu batteries regulation battery passport delegated implementing act interoperability 2027` | Commission implementation status |
| Q03 | `Battery Pass content guidance battery passport industrial batteries data fields PDF` | Data and operational burden |
| Q04 | `CIRPASS battery passport technical architecture interoperability standards unique identifier access rights` | Technical architecture and service-provider role |
| Q05 | `Poland stationary battery energy storage market 2025 installed projects units industrial batteries above 2 kWh` | Physical denominator |
| Q06 | `digital battery passport software pricing per battery passport SaaS` | Price and substitute evidence |
| Q07 | `battery OEM digital battery passport portal Siemens Product Passport 2026 pricing` | Enterprise incumbent route |
| Q08 | `Poland BDO register number battery producers importers placing batteries market 2025` | Payer-register denominator |

### Source ledger — eight open attempts

| ID | Source | Type | Useful evidence and limitation |
|---|---|---|---|
| S01 | [Regulation (EU) 2023/1542](https://eur-lex.europa.eu/eli/reg/2023/1542/oj?locale=en) | Primary law | Scope, responsibility, authorization, access, interoperability, transfers and recycling closure |
| S02 | [European Commission: Batteries](https://environment.ec.europa.eu/topics/waste-and-recycling/batteries_en) | Primary authority | Implementation is continuing; page did not establish the specific Article 77(9) act |
| S03 | [Battery Passport Content Guidance](https://thebatterypass.eu/assets/images/content-guidance/pdf/2023_Battery_Passport_Content_Guidance.pdf) | Industry/technical consortium | Attribute applicability, BMS and dynamic-data complexity; guidance notes supersession by DIN specification |
| S04 | [CIRPASS DPP System Architecture](https://cirpassproject.eu/wp-content/uploads/2024/06/D3.2v1.9.pdf) | EU-funded technical work | Open architecture, identifiers, data carriers and third-party DPP service role |
| S05 | [Polish Economic Institute weekly](https://pie.net.pl/wp-content/uploads/2025/10/PEI_Weekly_EN_41-2025.pdf) | Market/public-data synthesis | Polish installed systems, capacity and contracted pipeline; no placing-operator count |
| S06 | [Batteriepasswerk pricing](https://www.batteriepasswerk.com/en/pricing) | Commercial | Public self-service prices and volume allowances; vendor claims were not independently audited |
| S07 | [Siemens DPP4.0](https://www.siemens.com/en-us/industries/batteries/battery-passport/) | Commercial | Search extract described available SaaS, integrations and licences; direct page fetch failed and no price was obtained |
| S08 | [Polish BDO register](https://rejestr-bdo.mos.gov.pl/Registry/Index?pageNumber=289&placeType=residenceOrBusinessAddress&tables=ActivityScope5Table1) | Official register | Confirms public entity-register access; opened page provided no aggregate relevant payer count |

### Evidence ledger

| Evidence ID | Claim | Source | Classification |
|---|---|---|---|
| E01 | Covered industrial batteries require passports from 18 February 2027 | S01 | Verified |
| E02 | The placing operator remains responsible and may authorize another operator in writing | S01 | Verified |
| E03 | Passports require unique identifiers, QR access and open interoperable data | S01 | Verified |
| E04 | Custodians cannot sell or reuse protected data outside the service | S01 | Verified |
| E05 | Passport availability must survive operator cessation and continue until recycling | S01 | Verified |
| E06 | Responsibility and passport relationships change at repurposing and waste status | S01 | Verified |
| E07 | Stationary BMS data creates category-specific dynamic-data work | S03 | Verified as technical guidance, not final secondary law |
| E08 | DPP-as-a-Service is an identified architectural role | S04 | Verified as architecture proposal |
| E09 | Poland had more than 47,000 prosumer systems and 258 MW at end-2024 | S05 | Verified from cited synthesis |
| E10 | Poland had 4.3 GW contracted for 2027–2029 delivery | S05 | Verified from cited synthesis |
| E11 | Bare passport software is available at sub-euro effective unit prices at volume | S06 | Verified vendor pricing |
| E12 | Siemens markets an enterprise DPP product | S07 | Verified from search extract; direct fetch unavailable |
| E13 | Exact Polish placing-operator count | S08 | Unknown |
| E14 | Managed custody can command 10–30 PLN per passport | Pricing model | Interpretation requiring paid proof |
| E15 | Installer commissioning capture provides a durable advantage | Transaction analysis | Interpretation requiring operational proof |
| E16 | Final Article 77(9) access rules available for production implementation | S01–S02 | Unknown within the fixed source set |
| E17 | Founder-wealth outcomes | Scenario model | Assumptions, not market evidence |

**Budget record:** Eight distinct web queries were run. Eight source-open attempts were made; seven returned usable page content and the Siemens direct open failed. No additional source was substituted. No local file other than the specified packet was read, and no files were edited.
