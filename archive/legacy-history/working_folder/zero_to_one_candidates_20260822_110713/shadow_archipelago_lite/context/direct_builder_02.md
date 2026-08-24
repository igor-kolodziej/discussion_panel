# Shadow Direct Builder Packet 2

Agent `shadow-direct-builder-02`; stage `direct_concept`.

Read only this packet. Do not browse or inspect any other file. Produce exactly twelve direct concepts, one for every assigned problem, in the exact ID mapping below. Do not score, rank, select, compare with past ideas, or add a shared solution grammar.

Neutral founder constraints: unknown solo Warsaw founder; strong data/AI capability; five hours/day alongside employment; about 100,000 PLN available before proof; contractors allowed; local renewable-installer route is available but optional; no camera-led distribution; all proof must be lawful and part-time feasible.

For each concept use a heading `## D-NNN — title` and record: parent problem ID; buyer, payer, and desired outcome; value-capture event; delivery primitive; initial acquisition route; possible compounding asset; first falsifiable assumption; safety/legal boundary; evidence and hypothesis IDs. Distinguish evidenced facts from hypotheses. End each card with one minified JSON object on its own line using exactly: `{"record_type":"mapping","raw_id":"D-NNN","concept_type":"direct","parent_ids":["P-..."],"creator_agent_id":"shadow-direct-builder-02"}`.

## Required ID mapping

- `D-013` ← `P-operational_failure-01`
- `D-014` ← `P-operational_failure-02`
- `D-015` ← `P-operational_failure-03`
- `D-016` ← `P-operational_failure-04`
- `D-017` ← `P-operational_failure-05`
- `D-018` ← `P-operational_failure-06`
- `D-019` ← `P-incumbent_economics_channels-01`
- `D-020` ← `P-incumbent_economics_channels-02`
- `D-021` ← `P-incumbent_economics_channels-03`
- `D-022` ← `P-incumbent_economics_channels-04`
- `D-023` ← `P-incumbent_economics_channels-05`
- `D-024` ← `P-incumbent_economics_channels-06`

## Assigned problem cards

## P-operational_failure-01 — Last-minute elective-operation cancellation

- **Actor/outcome:** NHS acute-trust theatre operations manager; complete scheduled elective procedures without non-clinical cancellation or a >28-day rebooking breach.
- **Observable loss/frequency/magnitude:** **Official measured.** NHS England recorded 21,249 last-minute non-clinical cancellations in Q2 2024/25, 1.0% of elective activity; 4,825 patients were not treated within 28 days. Royal Devon separately reported 7,836 cancellations in 2023/24, including 1,804 attributed to staffing, 371 to theatre capacity/list overrun, 176 to equipment failure, and 1,102 to booking/admin error. [E-OF-001: NHS England, November 2024](https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2024/11/QMCO-Statistical-Commentary-Q2-2024-25-V2.pdf), [E-OF-002: Royal Devon FOI, 11 June 2024](https://www.royaldevon.nhs.uk/media/po5jxwa5/foi-rdf2584-24-cancelled-elective-operations-for-non-clinical-reasons.pdf)
- **Existing workaround:** Prioritise emergencies, overrun or reassemble later lists, rebook within 28 days, and manually inspect free-text cancellation records.
- **Payer/budget evidence:** Acute trusts and NHS commissioners carry the rescheduling and unused-capacity burden. The NHS standard says a hospital must offer a binding date within 28 days or fund treatment at the time and hospital chosen by the patient. [E-OF-003: NHS Standards Directory, updated 1 December 2025](https://standards.nhs.uk/published-standards/quarterly-monitoring-of-cancelled-operations-return)
- **Counterevidence:** Cancellations were only 1.0% of elective activity. One trust did not submit Q2 data. Royal Devon warns that “other” and admin categories can include corrections or clinical/patient events rather than true cancellations.
- **Unknowns:** Incremental cost per cancellation; nationwide share specifically caused by instrument availability; recoverable theatre time; distribution by specialty and trust; quality of local reason coding.
- **Metadata:** `island_id=operational_failure`; `creator_id=shadow-scout-03`; `evidence_ids=E-OF-001,E-OF-002,E-OF-003`.

## P-operational_failure-02 — Medicine-shortage handling consumes pharmacy capacity

- **Actor/outcome:** Community-pharmacy owner or responsible pharmacist; dispense the prescribed medicine promptly without uncompensated sourcing work or dispensing at a loss.
- **Observable loss/frequency/magnitude:** **Large survey, self-reported.** In England, 99% of surveyed pharmacy teams encountered supply problems at least weekly and 72% multiple times daily; 94% of owners said sourcing time had increased. One operator reported one to two extra staff-hours daily. In Ireland, 2025 respondents reported six hours 22 minutes per week, up from four hours 37 minutes in 2024; 20% spent more than 30 hours per month. [E-OF-004: CPE findings reported 9 May 2024](https://pharmaceutical-journal.com/article/news/more-than-90-of-pharmacies-say-medicines-shortages-have-got-worse-over-the-past-year), [E-OF-005: IPU survey, May 2025](https://ipu.ie/ipu-review-article/ipu-medicine-shortages-survey-2025/)
- **Existing workaround:** Repeatedly check wholesaler portals; call wholesalers, manufacturers and prescribers; borrow from another pharmacy; source an exempt medicinal product; substitute strength or product; hold extra inventory.
- **Payer/budget evidence:** Pharmacy owners absorb staff time and sometimes unreimbursed exempt-product cost. An NHS-commissioned economic review estimated a £409,000–£573,000 mean full economic cost per pharmacy in 2023/24; 47% of branches were not profitable at EBITDA level. [E-OF-006: economic analysis, published 9 October 2024 and updated 31 March 2025](https://cpe.org.uk/funding-and-reimbursement/pharmacy-funding/independent-economic-review/)
- **Counterevidence:** Only about 3% of medicines reimbursed by the NHS were reported in shortage, and the vast majority of more than one billion primary-care prescription items were dispensed without issue. The Irish survey also found a smaller percentage reporting significant deterioration than in 2024. [E-OF-007: Royal Pharmaceutical Society, 2024](https://www.rcpharm.org/policies/medicines-shortages-solutions-for-empty-shelves-2024/)
- **Unknowns:** Audited labour cost per shortage; variation by pharmacy size; proportion resolved without patient delay; shortage-level stock visibility; whether economically stressed owners have discretionary operating budget.
- **Metadata:** `island_id=operational_failure`; `creator_id=shadow-scout-03`; `evidence_ids=E-OF-004,E-OF-005,E-OF-006,E-OF-007`.

## P-operational_failure-03 — Trucks detained at shipper and receiver docks

- **Actor/outcome:** For-hire carrier dispatcher, driver and facility dock manager; complete pickup or delivery within planned dwell time while preserving legal driving hours.
- **Observable loss/frequency/magnitude:** **Industry estimate plus observed logs.** ATRI research reported approximately $11.5 billion of lost productivity and $3.6 billion of direct expense in 2023. MIT FreightLab analysis of roughly 310,000 driver-days found only 6.5–7 hours driven against an 11-hour legal maximum; its small shipper study put live-load detention around 2–2.5 hours, with destinations often taking two to four hours. [E-OF-008: ATRI results reported September 2024](https://www.overdriveonline.com/business/article/15683714/how-detention-time-impacted-trucking-companies-drivers-in-2023), [E-OF-009: MIT FreightLab account](https://www.thescxchange.com/articles/9298-are-you-your-truckers-keeper)
- **Existing workaround:** Drop-and-hook loads, appointment scheduling, detention clauses, manual timestamp documentation, higher freight bids for slow facilities, and driver/facility wait-time tracking.
- **Payer/budget evidence:** Carriers lose equipment and driver utilisation; shippers pay through freight rates and detention charges. Contractual detention is commonly tracked after stipulated free time. A 2026 federal analysis cites hourly fees of $50–$100 or charges based on shipment value, while a 2024 industry account cites $1.1–$1.3 billion in reduced annual driver earnings. [E-OF-010: Trucking Dive, 25 March 2024](https://www.truckingdive.com/spons/how-to-keep-the-dominos-from-falling-using-data-to-mitigate-the-decades-ol/711030/), [E-OF-011: Federal Register, 10 August 2026](https://www.govinfo.gov/content/pkg/FR-2026-08-10/pdf/FR-2026-08-10.pdf)
- **Counterevidence:** ATRI reported detention frequency 6.5 percentage points lower in 2023 than in 2014. MIT’s shipper focus group was small, while its electronic-log data covered 2016–2020 and cannot attribute every unused hour to detention.
- **Unknowns:** Facility-level loss distribution; collection rate on detention invoices; European comparability; legitimate loading versus avoidable waiting; responsibility when appointment or arrival data conflict.
- **Metadata:** `island_id=operational_failure`; `creator_id=shadow-scout-03`; `evidence_ids=E-OF-008,E-OF-009,E-OF-010,E-OF-011`.

## P-operational_failure-04 — Industrial equipment downtime remains expensive despite maintenance activity

- **Actor/outcome:** Plant maintenance or operations manager; keep production assets available and meet production and delivery commitments.
- **Observable loss/frequency/magnitude:** **Vendor-sponsored survey estimates.** MaintainX’s 2024 survey of 1,165 maintenance and operations professionals estimated about $25,000 per downtime hour, exceeding $500,000 in large organisations. ABB’s 2023 survey of 3,215 decision-makers found more than two-thirds experienced an unplanned outage at least monthly and reported a median $125,000 hourly cost. [E-OF-012: Facilities Dive, 14 August 2024](https://www.facilitiesdive.com/news/maintainx-preventive-maintenance-industrial-facilities-management-2024-downtime-costs/724230/), [E-OF-013: ABB, 11 October 2023](https://new.abb.com/news/detail/107660/abb-survey-reveals-unplanned-downtime-costs-125-000-per-hour)
- **Existing workaround:** Preventive maintenance, run-to-failure for selected assets, spare-parts inventories, replacement of aging equipment, staff training and reactive repair.
- **Payer/budget evidence:** Maintenance is an established plant budget: 60% of ABB respondents planned to increase reliability and maintenance investment within three years, with one-third planning an increase above 10%.
- **Counterevidence:** MaintainX found 85.2% reported stable or decreasing incident counts, and 86.8% already used preventive maintenance. ABB explicitly says its cost figures came from questionnaires, not audited accounting records.
- **Unknowns:** Plant-specific contribution margin lost per hour; asset criticality; failure modes; spare-part lead times; planned-versus-unplanned classification; applicability of global estimates to smaller Polish plants.
- **Metadata:** `island_id=operational_failure`; `creator_id=shadow-scout-03`; `evidence_ids=E-OF-012,E-OF-013`.

## P-operational_failure-05 — Sewer blockages trigger recurring clearing cost and overflow events

- **Actor/outcome:** Wastewater-network operations manager; keep sewers flowing without customer flooding, environmental discharge or prolonged emergency excavation.
- **Observable loss/frequency/magnitude:** **Operator-reported cost plus regulatory counts.** Yarra Valley Water reported nearly A$1 million annually to clear about 1,200 blockages; Barwon Water reported approximately A$600,000 annually, and South East Water nearly A$770,000 for about 1,000 fat/wipe-related blockages. In England, 2,469 sewerage pollution incidents occurred in 2024, up from 1,902 in 2023. [E-OF-014: ABC News, 29 November 2024](https://www.abc.net.au/news/2024-11-29/victoria-fatbergs-sewerage-system-melbourne-blockage-cost/104649474), [E-OF-015: Environment Agency, 23 October 2025](https://www.gov.uk/government/publications/water-and-sewerage-companies-in-england-environmental-performance-report-2024/water-and-sewerage-companies-in-england-environmental-performance-report-for-2024)
- **Existing workaround:** Reactive high-pressure clearing, multi-day excavation, regular rubbish removal, customer education and staffed or alarmed pumping/treatment sites.
- **Payer/budget evidence:** Clearing is paid from water-utility operating budgets and ultimately ratepayer revenue. England allocated £4.8 billion for environmental enhancements during 2020–2025; pollution performance can have financial consequences. Ofwat also proposed £168 million in penalties against three companies in August 2024. [E-OF-016: Ofwat, 6 August 2024](https://www.ofwat.gov.uk/thames-yorkshire-and-northumbrian-water-face-168-million-penalty-following-sewage-investigation/)
- **Counterevidence:** Victoria’s overall blockage rate fell 4.9% between 2021/22 and 2022/23. In England, 98.8% of permitted treatment outlets complied with numeric discharge conditions in 2024; blockages are only one of several causes of pollution incidents.
- **Unknowns:** Preventable share of blockages; cost by blockage type; location-level recurrence; proportion detected internally; relationship between blockage response and pollution penalties.
- **Metadata:** `island_id=operational_failure`; `creator_id=shadow-scout-03`; `evidence_ids=E-OF-014,E-OF-015,E-OF-016`.

## P-operational_failure-06 — Renewable projects queue for, or are refused, grid connection

- **Actor/outcome:** Polish renewable-project developer and DSO connection team; obtain usable connection conditions on a predictable timeline so a committed project can proceed.
- **Observable loss/frequency/magnitude:** **Official aggregate, duplicate-prone.** URE recorded 6,259 refusals for renewable-source connection conditions in 2024, nominally representing 42.4 GW; refusal count rose nearly 5%. URE also processed 1,244 electricity disputes dominated by grid-connection refusals. Across the EU, small-PV connection can take up to a year in some regions, while utility-scale projects average about four years and reach eight years in congested areas. [E-OF-017: URE, 16 May 2025](https://www.ure.gov.pl/pl/urzad/informacje-ogolne/aktualnosci/12656%2CPodsumowanie-dzialan-URE-w-2024-r-postulaty-deregulacji-i-nowe-kompetencje-Regul.html), [E-OF-018: URE National Report 2025](https://www.ure.gov.pl/download/2/778/NationalReport2025.pdf), [E-OF-019: OECD, 2025](https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/10/diagnostic-toolkit-for-reducing-regulatory-barriers-to-solar-wind-and-pumped-hydro-storage-in-the-european-union_acd0b286/15f4aed4-en.pdf)
- **Existing workaround:** Submit the project at multiple possible locations, resubmit after refusal, pursue a URE dispute, escalate missed dates, or seek shared connection. In Poland’s first cable-pooling year, 130 applications produced 62 connection-condition grants, 47 refusals, 49 agreements and 12 completed shared connections. [E-OF-020: URE, 31 December 2025](https://www.ure.gov.pl/en/communication/news/494%2CThe-President-of-the-URE-summarises-the-first-year-of-cable-pooling-in-Poland.html)
- **Payer/budget evidence:** Developers carry application, development and financing exposure; European queues increasingly require developer fees or guarantees. Polish DSO spending capacity is indirect: URE approved regulated revenues of PLN 128.9 billion across transmission, distribution and energy trading activities in 2024. No Polish evidence located quantified willingness to pay for shorter processing.
- **Counterevidence:** URE explicitly warns that the 42.4 GW total is not unique rejected capacity because developers may submit the same project several times. Only two Polish micro-installation connection-refusal disputes were processed in 2024. Most EU member states report small-PV connection below six months.
- **Unknowns:** Unique projects and MW affected; refusal versus delay split; sunk development cost; installer cash-flow impact; processing time by Polish DSO; whether refusals are primarily technical, economic or incomplete-application failures.
- **Metadata:** `island_id=operational_failure`; `creator_id=shadow-scout-03`; `evidence_ids=E-OF-017,E-OF-018,E-OF-019,E-OF-020`.

## P-incumbent_economics_channels-01

**Actor / outcome:** Residential photovoltaic owner whose original installer has failed or withdrawn support; keep a 20–25-year system operating, monitored, and eligible for warranty repairs.

**Observable loss, frequency, and magnitude status:**

- Loss is observable as unavailable monitoring, unresolved software or communications faults, inverter failure, wiring faults, roof leaks, and delayed warranty work.
- A 2024 US installer survey reported that 46% of active solar companies received service enquiries daily or weekly; 7% said their service enquiries came only from owners whose original installer had failed. Only 15% of serviced repairs were paid directly by the homeowner; the rest were generally assigned to warranties or insurance. These are measured, self-reported US figures, not Polish incidence.
- European evidence identifies a growing but uncounted population of orphaned residential systems following installer insolvencies. Europe added 65.1 GW in 2025 while losing 40,000 solar jobs, but neither statistic measures orphaned systems directly.
- European residential installation is fragmented: a 2024 study counted approximately 6,300 installers in Germany, 3,100 in Italy, and 2,900 in the UK. No comparable Polish service-failure count was found.

**Current workaround:** Owners contact component manufacturers, warranty or insurance administrators, or unrelated local installers. Active installers may take over servicing and monitoring; the US survey found 96% had at least partial monitoring access and 63% checked customer systems at least quarterly.

**Payer / budget evidence:** The immediate budget can sit with the homeowner, manufacturer warranty, installer warranty, or third-party insurer. The homeowner paid in only 15% of surveyed repair cases, demonstrating that payment authority and service responsibility are frequently separated. Local installers control access to field labour, while manufacturers or insurers may control authorization and reimbursement.

**Counterevidence:**

- Equipment failures were described as uncommon relative to software and setup problems.
- Monitoring coverage among surviving installers was high.
- The service-frequency and payer figures are US data; European evidence establishes fragmentation and insolvency pressure but not Polish frequency or loss per household.
- Standardized European O&M practices exist and apply to systems of all sizes.

**Unknowns:**

- Number and age distribution of orphaned Polish residential systems.
- Annual fault incidence and lost generation per unsupported system.
- Median response time, truck-roll cost, and warranty rejection rate.
- Whether Polish manufacturers and distributors consistently authorize third-party warranty labour.
- Proportion of installers willing to service systems they did not install.

**Dated source trace:**

- `E-incumbent_economics_channels-01-A` — SolarReviews, *2024 Solar Industry Survey* (2024): [direct PDF](https://frontend-cdn.solarreviews.com/2024-solarreviews-solar-industry-survey-report.pdf)
- `E-incumbent_economics_channels-01-B` — EUPD Research, European residential installer landscape (25 June 2024): [direct page](https://eupd-group.com/eupd-research-reveals-top-european-residential-solar-markets-and-most-impacting-installers-amidst-booming-market-growth/)
- `E-incumbent_economics_channels-01-C` — SolarPower Europe, *O&M Best Practice Guidelines Version 6.0* (18 February 2025): [direct page](https://www.solarpowereurope.org/insights/thematic-reports/operation-and-maintenance-best-practice-guidelines-version-6-0-1)
- `E-incumbent_economics_channels-01-D` — pv magazine, European orphaned rooftop systems (8 July 2026): [direct page](https://www.pv-magazine.com/2026/07/08/who-maintains-europes-orphaned-rooftop-solar/)

**Query trace:**

1. `site:gov.uk solar installer insolvency warranty consumers report 2024`
2. `site:mcscertified.com installer ceased trading solar warranty consumer protection`
3. `Europe residential solar operations maintenance market fragmented installers report warranty failures`

**Identity:** `island_id=incumbent_economics_channels`; `creator_id=shadow-scout-04`; `evidence_ids=E-incumbent_economics_channels-01-A..D`

## P-incumbent_economics_channels-02

**Actor / outcome:** Small or medium-sized merchant accepting card payments; maintain uninterrupted acceptance while paying a transparent, competitive total merchant service charge.

**Observable loss, frequency, and magnitude status:**

- Loss appears in higher transaction charges, staff time spent interpreting non-comparable tariffs, and foregone savings when merchants do not compare, negotiate, or switch.
- The UK Payment Systems Regulator found that Mastercard and Visa core scheme and processing fees had risen by at least 25% since 2017, imposing at least £170 million of additional annual cost on UK businesses. This is a regulator estimate at market level, not an amount attributable to each merchant.
- A 2021 regulator review found robust evidence of poor outcomes for merchants with annual card turnover between £15,000 and £50 million.
- Polling cited in that review found 61% of 1,210 independent and symbol retailers had neither compared nor switched acquirers during the preceding three years. Among merchants that considered switching but stayed, 25% reported receiving a better incumbent offer.
- POS-terminal contracts can run for three or five years, renew automatically, and impose termination charges equal to remaining payments. Existing terminals are typically not portable to a new acquirer.

**Current workaround:** Merchants periodically request alternative quotes, threaten to switch, or renegotiate with the incumbent. Some use payment facilitators whose reader is bought upfront, avoiding a separate long terminal lease. The evidence shows that incumbent retention offers can reduce charges without a completed switch.

**Payer / budget evidence:** The merchant pays the merchant service charge from its payment-acceptance or operating budget. The charge combines interchange, scheme fees, and acquirer revenue. The owner, finance lead, or payments/procurement manager normally has purchasing authority; the acquirer and card schemes determine substantial upstream components that the merchant cannot negotiate separately.

**Counterevidence:**

- The regulator found no evidence of malfunction for the largest merchants with more than £50 million in annual card turnover.
- Low engagement can reflect satisfaction or a considered preference for the incumbent, not only confusion or lock-in.
- Minimum terminal commitments may fund lower monthly prices.
- Gateway contracts were found unlikely to restrict switching.
- Findings are UK-specific, and regulatory remedies introduced after the 2021 review may have altered current behavior.

**Unknowns:**

- Current effective charge distribution and switching rate among Polish SMEs.
- Savings net of terminal replacement, integration, downtime, and staff effort.
- How many Polish contracts combine acquiring, gateway, terminal, and POS software.
- Frequency and size of undisclosed commissions paid to independent sales organizations.
- Whether merchants can reliably reconstruct effective rates from current statements.

**Dated source trace:**

- `E-incumbent_economics_channels-02-A` — UK Payment Systems Regulator, *Card-acquiring market review: Final report* (November 2021): [direct PDF](https://www.psr.org.uk/media/p1tlg0iw/psr-card-acquiring-market-review-final-report-november-2021.pdf)
- `E-incumbent_economics_channels-02-B` — European Commission, study of post-2018 card-market and merchant-service-charge developments (2024 publication record): [direct page](https://op.europa.eu/en/publication-detail/-/publication/ed0da3f4-c57a-11ee-95d9-01aa75ed71a1)
- `E-incumbent_economics_channels-02-C` — UK Payment Systems Regulator, final scheme-and-processing-fee findings (2025): [direct page](https://www.psr.org.uk/mr22-1-10-scheme-and-processing-fees-final-report/)
- `E-incumbent_economics_channels-02-D` — National Bank of Poland, acquirer survey and Polish merchant-service-charge history (2012): [direct PDF](https://nbp.pl/wp-content/uploads/2024/03/interchange_fee.pdf)

**Query trace:**

4. `site:federalreserve.gov small business merchant card processing fees switching processors survey`
5. `European Commission card acquiring merchant fees SME transparency switching payment service provider study`
6. `UK Payment Systems Regulator card-acquiring market review SMEs switching fees 2021`
7. `Poland merchant card acceptance fees small business terminal acquiring market report`

**Identity:** `island_id=incumbent_economics_channels`; `creator_id=shadow-scout-04`; `evidence_ids=E-incumbent_economics_channels-02-A..D`

## P-incumbent_economics_channels-03

**Actor / outcome:** Dentist, dental-practice owner, and contracted dental laboratory; deliver a laboratory-made crown that is clinically acceptable on the first attempt.

**Observable loss, frequency, and magnitude status:**

- Observable loss consists of rejected restorations, another patient appointment, repeated impressions or scans, additional laboratory fabrication, delayed completion, and consumed chair and technician capacity.
- A US practice-based study of 205 dentists and 3,750 crowns measured a 3.8% remake rate. Individual practitioner rejection rates ranged from 0% to 42%; proximal misfit, marginal errors, and esthetic failures were the leading causes.
- A 2026 multicentre audit of 40,344 restorations made by seven Riyadh laboratories found 2,612 remakes, or 6.5% overall. Rates included 6.9% for crowns, 7.5% for veneers, and 4.8% for bridges. The data covered July 2022–July 2023.
- In that audit, 92.9% of remade cases had paper-based dentist–laboratory communication. The association is observable, but the study does not establish paper communication as the causal factor.
- No dependable Polish cost per remake was found. Monetary magnitude therefore remains unverified.

**Current workaround:** The practice and laboratory refabricate the restoration, repeat or correct impressions or scans, perform chairside adjustments, and communicate case-specific corrections. Procurement may shift between laboratories, but a large dentist survey reported that price was not an important laboratory-selection factor.

**Payer / budget evidence:** The dental practice purchases laboratory work from procedure revenue and controls laboratory selection. The laboratory incurs additional fabrication labour and material; the practice loses chair capacity. Evidence did not establish how often Polish laboratories absorb the remake versus rebilling the dentist or patient. One practice-network study reported an average of 18 crowns per clinician per month, confirming a recurring laboratory purchasing flow.

**Counterevidence:**

- In the US crown study, 58% of participating clinicians rejected no crowns.
- A separate survey found 59% of dentists reported remake rates below 2%, although 17% reported rates above 4%.
- The 3.8% study is US-based and the 6.5% audit is from Riyadh; neither establishes Polish incidence.
- Digital workflows may differ materially from the predominantly paper-based audit population.
- Remakes can result from preparation, impression, patient, laboratory, material, or esthetic factors; responsibility is not confined to one party.

**Unknowns:**

- Polish remake rate by restoration type, laboratory, and digital workflow.
- Cost allocation and dispute frequency between laboratory and dental practice.
- Chair minutes, technician hours, courier cost, and delayed cash collection per remake.
- Whether laboratories record structured reason codes consistently.
- Concentration and switching patterns in Polish dental-laboratory procurement.

**Dated source trace:**

- `E-incumbent_economics_channels-03-A` — National Dental Practice-Based Research Network, impression evaluation and laboratory utilization (2017): [direct article](https://pmc.ncbi.nlm.nih.gov/articles/PMC5793929/)
- `E-incumbent_economics_channels-03-B` — McCracken et al., crown remake rates (published online 22 November 2018; journal issue February 2019): [PubMed record](https://pubmed.ncbi.nlm.nih.gov/30412320/)
- `E-incumbent_economics_channels-03-C` — Multicentre fixed-prosthodontics remake audit (2026; observations from July 2022–July 2023): [direct article](https://pmc.ncbi.nlm.nih.gov/articles/PMC12901796/)
- `E-incumbent_economics_channels-03-D` — Association of Dental Distributors in Europe, distribution and laboratory-outsourcing coverage (2025–2026 edition): [direct page](https://adde.info/adde-survey-2025-2026)

**Query trace:**

8. `dental laboratory remake rate cost survey dentists 2023`
9. `peer reviewed dental prosthesis remake rate laboratory cost dentist chair time`
10. `dental laboratory market fragmented dentists choose laboratory procurement survey Europe`

**Identity:** `island_id=incumbent_economics_channels`; `creator_id=shadow-scout-04`; `evidence_ids=E-incumbent_economics_channels-03-A..D`

## P-incumbent_economics_channels-04

**Actor / outcome:** Commercial-vehicle dealer, independent garage, parts distributor, or fleet service manager; obtain the correct replacement part at the required time and a controlled acquisition cost.

**Observable loss, frequency, and magnitude status:**

- Observable loss consists of delayed repair completion, repeated supplier searches, unavailable parts, and price increases passed through the service channel.
- A 2026 aftermarket study covering more than 260 US dealers, distributors, garages, and parts stores identified parts availability as the leading 2025 challenge. When asked where manufacturers should provide support, 34% cited availability.
- Cost and pricing pressure ranked third, but 38% requested greater manufacturer support with that pressure.
- Average parts prices rose 4.0% in 2025 after a 10.2% rise in 2022. These are measured channel-level changes, not vehicle-level repair losses.
- Genuine original-equipment parts represented more than 60% of parts purchased for resale or installation, showing that procurement remains materially dependent on incumbent manufacturer channels.

**Current workaround:** Buyers search across original-equipment dealers, engine distributors, heavy-duty specialists, independent garages, and aftermarket brands. As vehicles age, leave warranty, or change owner, purchasing shifts away from original-equipment channels toward distributors and independent garages.

**Payer / budget evidence:** Dealers, distributors, garages, and fleet operators purchase parts either for resale or installation. The original-equipment channel held 53% of purchases associated with first owners and 46% for subsequent owners. Parts or service managers hold practical procurement authority, while warranty terms can keep the vehicle owner dependent on an original-equipment channel.

**Counterevidence:**

- Original-equipment supply remains the dominant channel, so multiple suppliers do not by themselves prove dysfunctional fragmentation.
- Only 34% identified availability as the manufacturer-support priority; it was not universal.
- The measured sample is US-based.
- The research did not quantify downtime hours, missed jobs, emergency freight, or revenue loss per unavailable part.
- Some channel switching reflects normal vehicle aging rather than procurement failure.

**Unknowns:**

- Equivalent availability, price, and channel-share figures for Poland and Central Europe.
- Fill rate and lead time by vehicle make and part category.
- Cost of downtime attributable specifically to parts sourcing.
- Frequency of incompatible catalog data, superseded part numbers, and incorrect deliveries.
- Commission, rebate, and warranty incentives affecting garage recommendations.
- Which party controls purchasing when fleet maintenance is outsourced.

**Dated source trace:**

- `E-incumbent_economics_channels-04-A` — MacKay & Company/DataMac distribution study, reported by *Trucks, Parts, Service* (2026; 2025 channel data): [direct page](https://www.truckpartsandservice.com/business/outlook-and-benchmarking/article/15827920/mackay-co-2026-datamac-distribution-report-released)

**Query trace:**

11. `fleet vehicle downtime cost per day maintenance survey 2024 official`
12. `commercial fleet maintenance procurement fragmented repair network parts availability report`
13. `site:geotab.com fleet downtime cost survey maintenance 2025`

**Identity:** `island_id=incumbent_economics_channels`; `creator_id=shadow-scout-04`; `evidence_ids=E-incumbent_economics_channels-04-A`

## P-incumbent_economics_channels-05

**Actor / outcome:** Condominium or housing association, its manager, and individual co-owners; approve, finance, procure, and complete a multifamily energy renovation with an understood allocation of costs and benefits.

**Observable loss, frequency, and magnitude status:**

- Observable loss appears as years of delayed collective decisions, repeated technical and financial work, stalled resolutions, fragmented contractor coordination, and unrealized energy savings.
- A 2025 European condominium study reported that collective decisions can take years. Among co-owners without renovation plans, nearly half considered the investment not worthwhile and 81% said their condominium lacked sufficient funds.
- A 2021 European Commission assessment estimated that about 11% of EU building stock receives some renovation annually, but only about 1% receives an energy renovation and only 0.2% receives a deep renovation reducing consumption by at least 60%.
- Sixteen member states identified split incentives as a major barrier: the owner bears renovation cost while a tenant receives lower energy bills.
- The Commission also documented a fragmented supply chain in which owners must work separately with technology suppliers, builders, finance providers, certifiers, and public authorities.
- Polish workforce research found missing coordination across audits, contractor acquisition, permits, financing, quality verification, insulation, heating, heat pumps, and photovoltaics.

**Current workaround:** Associations commission audits, seek grants or loans, obtain owner resolutions, contract separate specialists, and appoint managers or external advisers to coordinate work and verify completion. Central and Eastern European financing ranges from full public grants to market-based loans, leaving materially different owner contributions.

**Payer / budget evidence:** Co-owners or the condominium association fund common works, sometimes using reserves, owner assessments, loans, or subsidies. Formal voting controls procurement authority; significant works may require a qualified majority or unanimity. Where units are rented, the owner commonly pays while the tenant captures energy savings. The association manager handles day-to-day administration, but evidence reports frequent ambiguity over responsibility for a long renovation program.

**Counterevidence:**

- Some financing and technical-assistance programs already exist.
- Eleven percent of the stock receives some form of renovation annually, even though the energy-specific and deep-renovation rates are much lower.
- Barriers and ownership law vary substantially by country.
- Public financing can reduce the private burden, but unstable programs can also suppress participation.
- The 81% funding figure comes from a European condominium study and is not a Polish national estimate.

**Unknowns:**

- Number and value of Polish projects abandoned after audit, owner vote, or tender.
- Decision duration and professional cost by association size.
- Authority split among association board, property manager, owners, lender, and subsidy administrator.
- Bid comparability and change-order rates across contractor packages.
- Difference between projected and realized energy savings.
- Prevalence of undisclosed installer, auditor, financing, or equipment commissions.
- Availability of association-level credit and reserve funds in Warsaw and surrounding municipalities.

**Dated source trace:**

- `E-incumbent_economics_channels-05-A` — European Commission, EPBD impact assessment and renovation-barrier evidence (15 December 2021): [direct EUR-Lex page](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=SWD%3A2021%3A0453%3AFIN)
- `E-incumbent_economics_channels-05-B` — Energy Poverty Advisory Hub, Central and Eastern European multifamily financing (28 February 2024): [direct page](https://energy-poverty.ec.europa.eu/observatory/publications/comact-policy-brief-financing-models-adapted-needs-energy-poor-households)
- `E-incumbent_economics_channels-05-C` — KAPE/BUPS II Poland, skills and coordination barriers (2024 publication): [direct PDF](https://bups.kape.gov.pl/wp-content/uploads/2024/09/BUPS-II-Poland-D4.4.-SQA-Final-verson-EN.pdf)
- `E-incumbent_economics_channels-05-D` — CondoReno, *Summary for Policymakers* (11 December 2025): [direct PDF](https://build-up.ec.europa.eu/system/files/2025-12/zyhg8ezulC_11_12_2025_161749.pdf)

**Query trace:**

14. `EU building renovation split incentives multi apartment owners procurement barrier report 2024`
15. `Poland multifamily building heat pump renovation housing association procurement barriers`
16. `European Commission building renovation one stop shop fragmented supply chain transaction costs condominium`

**Identity:** `island_id=incumbent_economics_channels`; `creator_id=shadow-scout-04`; `evidence_ids=E-incumbent_economics_channels-05-A..D`

## P-incumbent_economics_channels-06

**Actor / outcome:** Polish or other EU road-freight carrier and its dispatcher or transport manager; secure revenue-producing cargo for both outbound and return legs.

**Observable loss, frequency, and magnitude status:**

- An empty vehicle still consumes driver time, fuel, vehicle capacity, and road access while producing no freight revenue.
- Eurostat measured 21.8% of EU heavy-road-freight vehicle-kilometres as empty in 2023. The Polish figure was 22.4%.
- Empty running was higher in domestic transport, 25.9%, than international transport, 13.1%.
- Polish-registered vehicles produced 20.3% of EU road-freight tonne-kilometres in 2023, making the issue materially exposed to the Polish carrier base.
- These are measured vehicle-kilometre shares, not avoidable-loss estimates. The dataset excludes light goods vehicles and lacks complete coverage for Italy, Malta, and Romania.
- European Commission analysis attributes some empty running to dedicated equipment and necessary travel to the loading point, but says fragmented markets and failure to arrange return loads are often responsible.

**Current workaround:** Dispatchers search for return loads through existing shipper relationships, freight forwarders, brokers, and load-matching channels; carriers also accept repositioning or combine partial backloads. The official statistics do not quantify use, fees, or effectiveness of each workaround.

**Payer / budget evidence:** The carrier bears the direct operating cost of empty kilometres and controls dispatch acceptance, subject to driver hours, equipment type, route, and customer commitments. Shippers or freight procurers control the original load award; brokers or forwarders may control access to fragmented spot demand and earn a spread or commission. No reliable current EU road-broker commission distribution was found.

**Counterevidence:**

- Some empty running is structurally unavoidable for tankers, specialized equipment, and travel to the next collection point.
- International empty running is substantially lower than domestic empty running.
- Country outcomes vary widely: approximately 7.8% in Denmark and 10.8% in Lithuania versus more than 30% in several countries, showing that one EU-wide rate conceals route and market differences.
- The statistics do not identify which empty kilometres could have carried a commercially compatible load.
- Adding a backload can increase waiting time, detour distance, handling, or delivery risk.

**Unknowns:**

- Avoidable share of Poland’s 22.4% empty vehicle-kilometres.
- Cost per empty kilometre by vehicle, fuel, wage, toll, and finance profile.
- Broker spreads, forwarder commissions, and payment terms in Polish road freight.
- Search time and acceptance rate by route and equipment class.
- Which procurement actors hold return-load demand before it reaches public or private load channels.
- Incidence of delayed payment, chargebacks, double brokerage, and bad debt.
- Whether apparent empty kilometres include repositioning that improves a later, higher-value load.

**Dated source trace:**

- `E-incumbent_economics_channels-06-A` — Eurostat, *Key figures on European transport — 2024 edition* (2023 road-freight data): [direct PDF](https://ec.europa.eu/eurostat/documents/15216629/20875401/KS-01-24-021-EN-N.pdf)
- `E-incumbent_economics_channels-06-B` — European Commission, Sustainable and Smart Mobility Strategy staff working document (9 December 2020), paragraphs 490–493: [direct EUR-Lex page](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A52020SC0331)
- `E-incumbent_economics_channels-06-C` — European Commission/DG MOVE, road-transport fragmentation and company-size evidence (2025 final report): [direct PDF](https://www.europarl.europa.eu/meetdocs/2024_2029/plmrep/COMMITTEES/TRAN/DV/2025/06-24/Final-Report-SSPAs_MOVEC1SER2023-138_EN.pdf)

**Query trace:**

17. `EU road freight empty running percentage fragmented carriers SME report 2024`
18. `European road freight shipper broker commission payment delays carrier procurement authority report`

**Identity:** `island_id=incumbent_economics_channels`; `creator_id=shadow-scout-04`; `evidence_ids=E-incumbent_economics_channels-06-A..C`

