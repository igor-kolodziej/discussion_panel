# Shadow Evidence-First Problem Cards

Frozen after all six independent scouts completed. Each island contains exactly six cards and no business solution. Full source and query traces are preserved below.

# Evidence Island 1

## P-customer_workarounds-01

- **Actor / desired outcome:** Residential solar installer or EPC operations lead wants complete, accurate site-survey, design, permit, and interconnection information so contracted systems reach installation without repeated visits or paperwork loops.
- **Observable loss event:** Incomplete measurements, photographs, structural details, or jurisdiction-specific documents cause resubmissions, repeat surveys, and stalled projects. NLR reports that permitting and interconnection can add weeks or months; its analysis covers more than 200,000 US projects. A February 2025 New Jersey report documents applications outstanding since early 2024 and municipalities requiring separate surveys or irrelevant documentation. **Frequency:** recurring but jurisdiction-dependent. **Magnitude status:** delay duration is substantiated; installer-level labor cost, cancellation rate, and Polish incidence remain unmeasured.
- **Current workaround / substitute:** Roof and attic measurements, photographs, clipboards, emailed files, home-grown templates, separate proposal/design tools, and staff manually adapting packages to each authority. One installer platform explicitly markets against “I’ll email you the photos later,” indicating the workaround it replaces.
- **Payer / budget evidence:** Installers already pay for workflow software. SolarPro lists $149/month for two users with survey integration and permit packages, or $250/month for its contractor tier.
- **Counterevidence:** The burden varies sharply by jurisdiction; standardized or instant permitting can materially shorten it. Mature platforms already combine surveys, designs, proposals, and permit packages, so the residual problem may be local rule variability rather than absent software.
- **Unknowns:** Repeat-visit percentage; staff hours per package; cancellation or margin loss; willingness to replace incumbent tools; European and Polish authority heterogeneity; whether installers can obtain reliable local templates.
- **Metadata:** island `customer_workarounds`; creator `shadow-scout-01`; evidence `CW-E01–CW-E05`.

## P-customer_workarounds-02

- **Actor / desired outcome:** Small construction contractor or subcontractor wants field hours assigned accurately to jobs and cost codes before payroll, billing, and profitability review.
- **Observable loss event:** Missing or late timecards force owners or office staff to reconstruct hours, correct clock-outs, and manually consolidate records. Incorrect job allocation obscures estimated-versus-actual labor and job profitability. **Frequency:** every pay period for affected crews; commenters describe forgotten entries as persistent even after adopting apps. **Magnitude status:** administrative recurrence is substantiated, but no independent per-company cost estimate was found.
- **Current workaround / substitute:** Paper timecards, Friday reminders, calendar invitations, texts, phone apps, managers entering time in batches, and separate timekeeping/job-costing software alongside the main project-management system.
- **Payer / budget evidence:** BuildKeeper publishes $4/month per timecard-entry user, $6 per manager, and $8 per full user. A contractor discussion reports purchasing Workyard separately because project-management packages bundle or surcharge timekeeping and job costing.
- **Counterevidence:** One contractor reported using paper timecards for more than 30 years without problems. Apps do not eliminate forgotten clock-ins or inaccurate allocations, and some contractors consider vertical software overpriced or inflexible.
- **Unknowns:** Percentage of timecards needing intervention; payroll correction hours; financial impact of wrong cost codes; adoption by very small crews; offline and multilingual requirements; whether the pain is behavior rather than tooling.
- **Metadata:** island `customer_workarounds`; creator `shadow-scout-01`; evidence `CW-E06–CW-E09`.

## P-customer_workarounds-03

- **Actor / desired outcome:** Freight forwarder, importer, broker, or drayage operator wants to determine quickly whether detention-and-demurrage invoices are valid and assemble timely supporting evidence for disputes.
- **Observable loss event:** A billed party pays charges for inaccessible containers, incorrect free-time calculations, or carrier/terminal mismatches, or spends months contesting them. The FMC says nine carriers collected approximately $15.4 billion between April 2020 and March 2025. One 2025 forwarder account describes two $3,600 disputes continuing for months; another shipment incurred $574 for one day. **Frequency:** aggregate charges are large, but erroneous-invoice incidence is not independently established. **Magnitude status:** aggregate collections and anecdotes are substantiated; vendor error-rate claims are not.
- **Current workaround / substitute:** Staff manually reconcile carrier invoices, contracts, terminal availability, free-time dates, emails, and supporting documents, then draft and repeatedly pursue disputes. Some parties simply pay because the effort and account-suspension risk outweigh the charge.
- **Payer / budget evidence:** D&D Defense publishes $149/month for up to 50 invoices, $399 for 250, and $899 for 1,000. Other returned providers advertise fixed fees, invoice-volume pricing, or success fees.
- **Counterevidence:** FMC data show billed and collected amounts declined in Q1 2025. The 2024 rule improved invoice requirements and deadlines. The FMC also states that a compliant invoice remains payable, so much D&D expenditure is not recoverable error.
- **Unknowns:** Share of invoices invalid or overstated; recovery rate after dispute; staff time per case; regional applicability outside US FMC jurisdiction; availability and reliability of terminal-event data; retaliation or account-suspension exposure.
- **Metadata:** island `customer_workarounds`; creator `shadow-scout-01`; evidence `CW-E10–CW-E13`.

## P-customer_workarounds-04

- **Actor / desired outcome:** Independent dental-practice owner or front-desk manager wants patients to attend, cancel early, or reschedule soon enough to refill the chair.
- **Observable loss event:** A patient fails to appear without notice, leaving production capacity unused and triggering calls to refill the slot. Planet DDS reported a 6.2% no-show rate across more than 5,200 practices in its 2025 mid-year dataset, versus a cited 7.4% 2024 industry average. **Frequency:** measurable and recurring. **Magnitude status:** rate is substantiated; an independent monetary loss per appointment was not found.
- **Current workaround / substitute:** Manual reminder calls, standalone text services, multi-channel reminder sequences, confirmation requests, rescheduling links, and waitlist calls. A dental professional reported that an eight-location group’s no-shows fell from 11% to 5% after adding a reminder service, but this is anecdotal.
- **Payer / budget evidence:** ShowUp advertised $49/month early-access pricing. VCare lists $299/month for 1–3 providers and $599/month for 4–10 providers.
- **Counterevidence:** The measured 6.2% average is lower than the 18–30% figures promoted in some vendor or anecdotal material. The reminder market is mature, and the reported fall from 7.4% to 6.2% suggests existing practices may already be improving the baseline.
- **Unknowns:** Revenue lost by appointment type; fraction of no-shows preventable by reminders; cancellation-to-backfill conversion; integration costs; patient consent and messaging preferences; performance of deposits or overbooking, which this trace did not substantiate.
- **Metadata:** island `customer_workarounds`; creator `shadow-scout-01`; evidence `CW-E14–CW-E17`.

## P-customer_workarounds-05

- **Actor / desired outcome:** Multifamily property manager handling master-metered or submetered buildings wants to allocate monthly utility costs accurately, post them promptly, and explain charges to residents.
- **Observable loss event:** Invoice entry, meter-read alignment, allocation exceptions, vacancies, move-outs, and resident disputes delay billing or leave costs unrecovered. **Frequency:** monthly billing cycle. One August 2026 operator account says a spreadsheet takes about one hour when nothing breaks and bills go out within two days. **Magnitude status:** recurrence is substantiated; independent error, complaint, and cost-recovery rates are not.
- **Current workaround / substitute:** Pull the master invoice and submeter readings on the same day, calculate allocations in a spreadsheet, export charges into property software, use RUBS or flat fees, and answer resident complaints manually. Outsourced billing bureaus are the principal substitute.
- **Payer / budget evidence:** A July 30, 2026 pricing analysis places software-only billing at $0.50–$2 per unit/month and full-service outsourcing at $3–$8, with $500–$2,000 setup fees. It estimates more than $30,000 annually for a 500-unit property at $5/unit.
- **Counterevidence:** For at least one operator, the spreadsheet process takes only about an hour per cycle. Resident complaints may focus on the administrative fee rather than billing accuracy. RUBS can be operationally simpler than submetering, although residents may view it as unfair.
- **Unknowns:** Portfolio size in the one-hour account; exception rate; unrecovered utility spend; legal variation by locality; resident-dispute cost; availability of clean meter and tenancy data; value below several hundred units.
- **Metadata:** island `customer_workarounds`; creator `shadow-scout-01`; evidence `CW-E18–CW-E21`.

## P-customer_workarounds-06

- **Actor / desired outcome:** Food manufacturer, importer, distributor, or technical-quality team wants current supplier specifications, allergens, ingredients, certificates, and approved label data to remain synchronized.
- **Observable loss event:** Staff re-key or copy obsolete supplier information, resulting in incorrect allergen declarations, quarantine, code changes, relabelling, or recall. Bidfood’s October 2025 supplier charter charges £1,650 per product for incorrect allergen information, rising to £1,750 after more than three errors in 12 months; full-recall administration starts at £2,250 per product. **Frequency:** the charter defines escalation thresholds but does not disclose incidence. **Magnitude status:** contractual event-level charges are substantiated; industry-average frequency and total losses are unknown.
- **Current workaround / substitute:** Supplier specification sheets in PDF, Word, or Excel; emailed questionnaires and certificates; manually maintained allergen matrices; spreadsheet versioning; periodic re-checks when recipes or suppliers change.
- **Payer / budget evidence:** Foodflou publishes €89/month for document management and €129/month for a small-company tier with supplier questionnaires, risk assessment, and supplier management. SoftSpec claims spreadsheet replacement saves 15 hours/week, but this is unverified vendor marketing.
- **Counterevidence:** Small venues can buy narrower allergen-matrix and label tools for £15/month, suggesting comprehensive specification systems may be unnecessary for limited catalogs. The 15-hour saving lacks disclosed methodology, and the 2024 UK sampling report does not establish manufacturer-level incident frequency.
- **Unknowns:** Staff hours by SKU and supplier count; frequency of changed specifications; error-to-incident conversion; integration with retailer portals; supplier participation; liability allocation; whether small manufacturers face enough recurring volume to justify dedicated expenditure.
- **Metadata:** island `customer_workarounds`; creator `shadow-scout-01`; evidence `CW-E22–CW-E27`.

## Evidence ledger

- `CW-E01` — NLR, undated page accessed 2026-08-22; analysis of 200,000+ projects and weeks/months of approval delay: [Permitting, inspection and interconnection timelines](https://www.nlr.gov/solar/market-research-analysis/permitting-inspection-interconnection-timelines).
- `CW-E02` — Regional Plan Association, February 2025: [Going Green in the Garden State](https://s3.us-east-1.amazonaws.com/rpa-org/general/NJ-SolarPermitting_RPA.pdf).
- `CW-E03` — customer discussion, 2025-07-04: [Typical residential solar installation timeline](https://www.reddit.com/r/solar/comments/1lrp427/what_is_the_typical_residential_install_timeline/).
- `CW-E04` — vendor page accessed 2026-08-22: [SolarPro survey workflow and pricing](https://www.solarpro.solutions/).
- `CW-E05` — practitioner forum, circa 2025: [Solar site-survey measurement requirements](https://forum.nachi.org/t/solar-site-survey/256190).
- `CW-E06` — contractor discussion, 2024-07-16: [Employees with late timesheets](https://www.reddit.com/r/smallbusiness/comments/1e4g6re/employees_with_late_time_sheets/).
- `CW-E07` — contractor discussion, 2025-02-15: [Construction-software pricing and workarounds](https://www.reddit.com/r/Construction/comments/1iqb442/construction_software_pricing_comparison_based_on/).
- `CW-E08` — vendor page accessed 2026-08-22: [BuildKeeper pricing](https://buildkeeper.com/pricing/).
- `CW-E09` — contractor discussion, August 2026: [Handling employee time across projects](https://www.reddit.com/r/AskContractors/comments/1vltpoy/how_are_you_guys_handling_employee_time_tracking/).
- `CW-E10` — FMC data through 2025-03-31: [Detention and demurrage](https://www.fmc.gov/detention-and-demurrage/).
- `CW-E11` — FMC, 2024-02-23: [Final D&D billing-practices rule](https://www.fmc.gov/articles/fmc-publishes-final-rule-on-detention-and-demurrage-billing-practices/).
- `CW-E12` — customer and forwarder discussion, 2025: [Maersk demurrage disputes](https://www.reddit.com/r/shipping/comments/1ne4pkj/has_anyone_ever_successfully_disputed_a_demurrage/).
- `CW-E13` — vendor page accessed 2026-08-22: [D&D Defense pricing and workflow](https://dnddefense.com/).
- `CW-E14` — Planet DDS, August 2025: [2025 Mid-Year Dental Industry Outlook](https://www.planetdds.com/wp-content/uploads/2025/08/2025-Mid-Year-Dental-Industry-Outlook-072525-1.pdf).
- `CW-E15` — dental-practitioner discussion, 2021: [Text reminders](https://www.reddit.com/r/Dentistry/comments/os8l30/text_reminders/).
- `CW-E16` — vendor page accessed 2026-08-22: [VCare dental reminders and pricing](https://vcare-health.com/solutions/dental-appointment-reminder).
- `CW-E17` — vendor page accessed 2026-08-22: [ShowUp](https://www.showupdental.com/).
- `CW-E18` — property-management discussion, August 2026: [In-house utility-billing process](https://www.reddit.com/r/PropertyManagement/comments/1vjs4dz/those_of_you_handling_utility_billing_inhouse/).
- `CW-E19` — Billee, 2026-07-30: [Utility-billing pricing](https://billee.ai/article/utility-billing-pricing-property-management-companies).
- `CW-E20` — vendor page accessed 2026-08-22: [Submeter Solutions billing](https://submetersolutions.com/billing-reporting/).
- `CW-E21` — resident counterevidence, 2023-03-05: [Switching from submetering to RUBS](https://www.reddit.com/r/bayarea/comments/11ivk8z/landlord_switching_water_billing_from_submetering/).
- `CW-E22` — small-business discussion, 2025: [Small food producers and allergen tracking](https://www.reddit.com/r/smallbusiness/comments/1o7l7pg/how_do_small_food_producers_handle_allergen/).
- `CW-E23` — vendor page accessed 2026-08-22: [SoftSpec](https://softspec.co.uk/).
- `CW-E24` — pricing accessed 2026-08-22: [Foodflou](https://www.foodflou.com/pricing).
- `CW-E25` — Bidfood, October 2025: [Supplier Charter](https://www.bidfoodsuppliers.co.uk/static/media/Bidfood-Supplier-Charter-October-2025.1765110d71515ba34bf8.pdf).
- `CW-E26` — UK Food Standards Agency, 2025: [Our Food 2024](https://www.food.gov.uk/sites/default/files/media/document/Our-Food-2024.pdf).
- `CW-E27` — low-cost counterexample accessed 2026-08-22: [AllerSafe pricing](https://allersafe.org/pricing).

## Complete query trace

Exactly 18 unique search queries were issued:

1. `solar installer forum manual site survey measurements proposal rework customer` → `CW-E04`, `CW-E05`.
2. `residential solar permit application paperwork delays installer survey 2025` → `CW-E01`, `CW-E02`, `CW-E03`.
3. `solar design software pricing per user site survey proposal installer` → `CW-E04`.
4. `construction subcontractor forum timesheets spreadsheet payroll job costing manual` → `CW-E06`, `CW-E08`.
5. `site:reddit.com construction company employees forget clock in job costing timesheet` → `CW-E06`, `CW-E09`.
6. `construction time tracking software pricing job costing contractor 2025` → `CW-E07`, `CW-E08`.
7. `freight forwarder demurrage detention invoice dispute spreadsheet email manual forum` → `CW-E12`.
8. `shipper demurrage detention charges annual cost disputes data 2024 2025` → `CW-E10`, `CW-E11`.
9. `demurrage detention audit software pricing invoice dispute freight forwarder` → `CW-E13`.
10. `dental practice forum no shows overbooking deposits reminder workaround` → `CW-E15`, `CW-E16`.
11. `dental appointment no show rate cost study 2024 practice` → `CW-E14`.
12. `dental reminder software pricing no show reduction practice` → `CW-E16`, `CW-E17`.
13. `property manager forum manual utility bill allocation spreadsheet tenant billing meter reads` → `CW-E18`.
14. `multifamily utility billing errors cost manual submeter reading study 2024` → `CW-E19`; no independent error-rate study was retained.
15. `property management utility billing software pricing submeter RUBS` → `CW-E19`, `CW-E20`, `CW-E21`.
16. `food manufacturer supplier specification allergen questionnaire spreadsheet manual forum` → `CW-E22`, `CW-E23`.
17. `food supplier specification management allergen errors recall cost 2024 2025` → `CW-E25`, `CW-E26`.
18. `food specification management software pricing supplier questionnaires allergen compliance` → `CW-E23`, `CW-E24`, `CW-E27`.

## Tool trace

1. Read `scout_customer_workarounds.md` with `sed`; no other filesystem path was read.
2. Issued five web-search batches containing queries `1–4`, `5–8`, `9–12`, `13–16`, and `17–18`.
3. Opened the shortlisted solar, construction, freight, dental, property-management, and food-compliance sources listed in the evidence ledger.
4. Inspected page 6 of the Planet DDS PDF to verify the no-show figure.
5. Used in-page matching—not additional search queries—to locate Foodflou’s prices and supplier-questionnaire tier and SoftSpec’s 15-hour vendor claim.
6. No repository, live-arm, history, validator/evaluator, or peer-output path was inspected.

# Evidence Island 2

Query count: exactly 18 unique web searches. Only `scout_spend_procurement.md` was read locally.

## P-spend_procurement-01 — Construction progress-claim rework and delayed payment

- **Actor / desired outcome:** Commercial manager or quantity surveyor at a subcontractor; submit an acceptable progress claim and receive the correct payment without repeated revisions.
- **Observable loss / frequency / magnitude status:** Hong Kong’s 2024 legislative material recognizes lengthy final-account settlement, adjustment disputes over quality/progress/quantity, and staff effort spent preparing and reviewing payment applications. A Procore customer reports “dozens of hours” saved monthly and avoiding two or three revision rounds, but this is vendor-selected testimony. **Status: process loss confirmed; representative financial magnitude unquantified.**
- **Current workaround:** Dedicated commercial staff, spreadsheets and PDFs, manual evidence collection, professional review, negotiation, and adjudication when amounts remain disputed.
- **Payer / budget evidence:** Payapps publicly charges subcontractors **A$65 per claim**, demonstrating transaction-level purchasing for payment-claim preparation. Procore markets a dedicated construction-payment module.
- **Dated evidence:** [Hong Kong Legislative Council paper, 3 October 2024](https://www.legco.gov.hk/yr2024/english/bc/bc05/papers/bc0520241003cb1-1296-3-e.pdf); [Payapps subcontractor pricing, accessed 22 August 2026](https://www.payapps.com/pricing-subcontractors/); [Procore construction payments, accessed 22 August 2026](https://www.procore.com/pay).
- **Counterevidence:** The Legislative Council records industry acceptance of a 60-day payment deadline as reasonable and says contractors already employ personnel for payment applications. This may be an accepted contractual workload rather than an acute unmet problem.
- **Unknowns:** Claim rejection frequency among small European contractors; cash-flow loss attributable specifically to documentation errors; willingness to pay outside larger commercial projects; prevalence of existing accounting or contractor-platform coverage.
- **IDs:** `island=spend_procurement`; `creator=shadow-scout-02`; `problem=P-spend_procurement-01`; `evidence=E-SP-01-A,E-SP-01-B,E-SP-01-C`.

## P-spend_procurement-02 — Retail suppliers abandoning or slowly disputing invoice deductions

- **Actor / desired outcome:** Accounts-receivable or finance employee at a CPG, fashion, or home-improvement supplier; determine whether retailer short-pays are valid and recover unsupported deductions before deadlines expire.
- **Observable loss / frequency / magnitude status:** SPS describes deductions caused by retailer-specific rules, EDI misalignment, denied disputes, and a customer’s unexpected **$200,000 post-audit**. Klaimback says AR teams abandon a long tail of claims below €200 because manual recovery costs exceed claim value. Both figures are vendor-reported. **Status: workflow and payment deductions observable; independent prevalence and typical magnitude not established.**
- **Current workaround:** Download remittances from retailer portals, reconcile them against invoices and promotions, locate POD/BOL/ASN/PO evidence, file disputes manually, and write off smaller deductions.
- **Payer / budget evidence:** Klaimback publishes a price of **€2,000 per month plus 20% of recovered credits**. SPS states that it uses annual flat-rate pricing based on supplier size and retailer, although the amount is not public.
- **Dated evidence:** [Klaimback deduction-management page, updated 30 July 2026](https://www.klaimback.com/retail-chargeback-software); [SPS Commerce Revenue Recovery, accessed 22 August 2026](https://www.spscommerce.com/products/revenue-recovery/).
- **Counterevidence:** Some deductions are contractually valid. The principal sources are sellers of recovery services, and the €200 abandonment threshold and $200,000 example are not neutral benchmarks.
- **Unknowns:** Deduction volume and invalidity rate among European mid-market suppliers; dispute deadlines by retailer; recovered amount net of labor and fees; retailer willingness to provide stable portal access; proportion already handled by EDI or ERP suites.
- **IDs:** `island=spend_procurement`; `creator=shadow-scout-02`; `problem=P-spend_procurement-02`; `evidence=E-SP-02-A,E-SP-02-B`.

## P-spend_procurement-03 — Shippers contesting detention, demurrage, and freight invoice charges

- **Actor / desired outcome:** Shipper, importer, freight-forwarder finance team, or logistics procurement manager; pay only contracted freight and accessorial charges and release cargo without prolonged disputes.
- **Observable loss / frequency / magnitude status:** The U.S. Federal Maritime Commission investigated **130 charge complaints in FY2024**, producing **$1,874,143** in refunds or cancelled charges; it also handled 271 informal dispute-resolution matters. The Hong Kong Shippers’ Council reported new surcharges including **$200 per container** amid unreliable 2024 schedules. **Status: official measured complaint recovery; total market incidence unknown.**
- **Current workaround:** Manually compare invoices against rate cards, shipment records, free-time calculations, BOL/POD documents, and contracts; dispute with carriers or terminals; escalate eligible U.S. matters to the FMC.
- **Payer / budget evidence:** AuditCargo lists **€499** for a 90-day audit, **€999** for a human-reviewed report, and **€300–€1,500 per month** for continuous auditing, with an optional 20% recovery fee.
- **Dated evidence:** [Federal Maritime Commission FY2024 Annual Report](https://www.govinfo.gov/content/pkg/CMR-FMC1-00195455/pdf/CMR-FMC1-00195455.pdf); [Hong Kong Shippers’ Council Annual Report 2024](https://www.hkshippers.org.hk/assets/uploads/media-uploader/2024-annualreport-compressed1754618128.pdf); [AuditCargo pricing, accessed 22 August 2026](https://auditcargo.com/pricing).
- **Counterevidence:** The FMC’s 130 complaints are a selected subset, not an error rate. Detention and demurrage can be valid when cargo or equipment remains beyond contracted free time. The pricing source is a vendor, not procurement-award evidence.
- **Unknowns:** Error rates by freight mode and carrier; European recovery rates; invoice volume required for economic significance; share already checked in transport-management systems; availability and quality of negotiated rate data.
- **IDs:** `island=spend_procurement`; `creator=shadow-scout-02`; `problem=P-spend_procurement-03`; `evidence=E-SP-03-A,E-SP-03-B,E-SP-03-C`.

## P-spend_procurement-04 — Hospital staff repeatedly appealing initially denied claims

- **Actor / desired outcome:** Hospital revenue-cycle, coding, utilization-review, or clinical staff; obtain correct insurer payment with minimal appeal effort and delay.
- **Observable loss / frequency / magnitude status:** A Premier survey covering leaders representing 516 hospitals estimated a **15% initial denial rate**, about **450 million denied claims annually**, **$43.84** administrative cost per denial, and **$19.7 billion** annual appeal cost. It found **54.3%** were eventually overturned and paid. AHA reports one system’s MA denial rate at 10.5%–15.5%, with 27.1%–46.7% of unpaid claims over 90 days. **Status: survey-derived national estimate plus one-system field report.**
- **Current workaround:** Billing and clinical employees identify denial reasons, retrieve records, correct coding, make payer calls, prepare written appeals, and repeat reviews.
- **Payer / budget evidence:** The $19.7 billion estimate represents current hospital labor and administrative expenditure fighting denials. The targeted RFP query did not surface a reliable public contract-award value.
- **Dated evidence:** [Becker’s summary of Premier research, 25 March 2024](https://www.beckershospitalreview.com/finance/claims-denials-are-costing-hospitals-nearly-20b-per-year/); [American Hospital Association brief, September 2024](https://www.aha.org/system/files/media/file/2024/09/Skyrocketing-Hospital-Administrative-Costs-Burdensome-Commercial-Insurer-Policies-Are-Impacting-Patient-Care.pdf); [U.S. Senate hearing record incorporating the Premier methodology, 9 May 2024](https://www.congress.gov/118/chrg/CHRG-118shrg55699/CHRG-118shrg55699.pdf).
- **Counterevidence:** More than half of denials are ultimately paid, so the gross denied amount is not equivalent to permanent revenue loss. Insurers distinguish claim denials from denials of care and argue prior authorization controls inappropriate spending.
- **Unknowns:** Cost and overturn rate by payer, specialty, and denial reason; data-access constraints; percentage of appeals requiring clinical judgment; procurement budgets at smaller providers; transferability outside the U.S.
- **IDs:** `island=spend_procurement`; `creator=shadow-scout-02`; `problem=P-spend_procurement-04`; `evidence=E-SP-04-A,E-SP-04-B,E-SP-04-C`.

## P-spend_procurement-05 — Small Polish PV/storage contractors assembling tender-compliant scope and BOMs

- **Actor / desired outcome:** Bid manager or owner at a Polish solar/storage EPC; submit a technically compliant, correctly costed municipal bid without avoidable rework or bid-capital strain.
- **Observable loss / frequency / magnitude status:** Polish TED notice `334566-2025` required combined design, supplies, electrical works, PV integration, batteries, energy management, wiring, and site work. It required **10,000 PLN bid security** and specified a July–November 2025 delivery window. **Status: purchasing complexity and temporary capital commitment directly observed in one tender; loss rate unquantified.**
- **Current workaround:** Manually interpret the SWZ and annexes, collect distributor quotations, maintain spreadsheet BOMs, cross-check technical equivalence, coordinate subcontractors, and arrange bid security.
- **Payer / budget evidence:** The municipal procurement was partly financed through the **European Regional Development Fund 2021–2027**. Separate installer purchasing evidence shows ENACT charging **$279/month billed annually** for proposal, pricing, and BOM functionality.
- **Dated evidence:** [TED notice 334566-2025, 2025](https://ted.europa.eu/en/notice/334566-2025/pdf); [ENACT installer pricing, accessed 22 August 2026](https://enact.solar/providers/provider-pricing/).
- **Counterevidence:** The tender explicitly allowed technically equivalent products. Bid security is normally refundable rather than an economic loss. A single municipal notice does not establish recurring pain across the Polish installer market.
- **Unknowns:** Number of comparable tenders per installer; bid rejection reasons; labor hours per response; actual contract value and margin; availability of distributor data; whether existing estimating packages already cover the work.
- **IDs:** `island=spend_procurement`; `creator=shadow-scout-02`; `problem=P-spend_procurement-05`; `evidence=E-SP-05-A,E-SP-05-B`.

## P-spend_procurement-06 — Duplicate and erroneous accounts-payable disbursements across payment channels

- **Actor / desired outcome:** AP manager, controller, or internal auditor; prevent duplicate payments while processing invoices promptly.
- **Observable loss / frequency / magnitude status:** A vendor paper quoting APQC benchmarking places duplicate or erroneous disbursements at **0.8%–2%**. A 2024 City of College Station audit observed the same invoice processed through both a purchasing card and standard check after submission through multiple channels. **Status: mechanism directly observed; benchmark is secondary/vendor-mediated.**
- **Current workaround:** ERP duplicate-number checks, PO matching, manual approval, cross-referencing p-card and AP records, periodic audits, spreadsheets, and requesting repayment or future credit from vendors.
- **Payer / budget evidence:** Quick Payable lists **$100 per user/month plus $0.50 per invoice** and shows a sample **$12,200 first-year total**. Payhouse lists **$1.25 per invoice** for construction AP processing.
- **Dated evidence:** [APQC benchmark landing page, 18 September 2024](https://www.apqc.org/resource-library/resource-listing/percentage-duplicate-disbursements-processed); [City of College Station AP audit, report 24-02](https://www.cstx.gov/media/wdsk3onh/24-02-accounts-payable-audit.pdf); [Oversight AP-risk paper](https://www.oversight.com/hubfs/assets/Resources/Whitepapers-and-Guides/Disarming-Risk-in-AP-2023.pdf?hsLang=en); [Quick Payable pricing, accessed 22 August 2026](https://quickpayable.com/pricing); [Payhouse pricing, accessed 22 August 2026](https://www.payhouse.app/).
- **Counterevidence:** The city audit explicitly concluded that it did **not** identify a high risk of duplicate payments. Many ERPs already reject identical invoice numbers, although alternate vendor records, channels, or numbering can evade simple checks.
- **Unknowns:** Duplicate-payment rate after existing controls; recoverability; false-positive review burden; minimum invoice volume supporting outside spend; integration costs; prevalence among Polish and European mid-market organizations.
- **IDs:** `island=spend_procurement`; `creator=shadow-scout-02`; `problem=P-spend_procurement-06`; `evidence=E-SP-06-A,E-SP-06-B,E-SP-06-C,E-SP-06-D,E-SP-06-E`.

## Complete query trace

1. **`2024 construction subcontractor late payments retainage survey invoice disputes`**  
   Consulted the [Hong Kong Legislative Council paper](https://www.legco.gov.hk/yr2024/english/bc/bc05/papers/bc0520241003cb1-1296-3-e.pdf) and [Procore](https://www.procore.com/pay). Confirmed payment-application labor, disputes, retention, and revision rounds; no neutral global loss estimate surfaced.

2. **`construction payment application software pricing per month subcontractor`**  
   Consulted [Payapps](https://www.payapps.com/pricing-subcontractors/), [Planyard](https://planyard.com/pricing), and [Procore](https://www.procore.com/pay). Payapps supplied the clearest public payment evidence: A$65 per claim.

3. **`public tender construction invoice payment processing budget RFP`**  
   Reviewed a [South African travel-management RFP](https://www.etenders.gov.za/home/Download/?blobName=f1c30a4d-1c10-4246-ae3b-b92b58e5353a.pdf&downloadedFileName=RFP+OW+083+2025-26+Travel+Management.pdf) mentioning PO/invoice reconciliation and discrepancy resolution. Excluded from card evidence because it was not construction-specific and disclosed no useful budget.

4. **`2024 retail supplier deductions chargebacks survey cost percentage revenue`**  
   Reviewed [SPS Revenue Recovery](https://www.spscommerce.com/products/revenue-recovery/) and SEC chargeback disclosures returned by the search. No independent CPG-wide percentage benchmark was established.

5. **`Amazon vendor chargebacks fee schedule shortage compliance 2025`**  
   Reviewed Amazon fee documentation and practitioner results concerning shortage and delivery chargebacks. Evidence was too Amazon-specific and insufficiently neutral for a separate card.

6. **`retail supplier deduction management software pricing chargebacks`**  
   Consulted [Klaimback](https://www.klaimback.com/retail-chargeback-software) and [SPS](https://www.spscommerce.com/products/revenue-recovery/). Established manual portal/evidence workflow and explicit €2,000/month plus recovery-fee pricing.

7. **`ocean freight demurrage detention charges annual report 2024 shippers costs`**  
   Consulted the [FMC FY2024 report](https://www.govinfo.gov/content/pkg/CMR-FMC1-00195455/pdf/CMR-FMC1-00195455.pdf), [Hong Kong Shippers’ Council report](https://www.hkshippers.org.hk/assets/uploads/media-uploader/2024-annualreport-compressed1754618128.pdf), and a Hapag-Lloyd annual-report result. FMC provided official complaint and refund totals.

8. **`freight invoice audit overcharges survey 2024 duplicate billing accessorials`**  
   Results described duplicate invoices, accessorials, tariffs, and manual reconciliation, but did not provide a sufficiently neutral 2024 prevalence benchmark.

9. **`freight audit payment software pricing per invoice shipper`**  
   Consulted [AuditCargo pricing](https://auditcargo.com/pricing), plus Navix and other vendor results. AuditCargo provided the clearest public price points.

10. **`2024 healthcare claims denial rate cost appeal survey hospitals`**  
    Consulted [Becker’s/Premier summary](https://www.beckershospitalreview.com/finance/claims-denials-are-costing-hospitals-nearly-20b-per-year/) and [AHA](https://www.aha.org/system/files/media/file/2024/09/Skyrocketing-Hospital-Administrative-Costs-Burdensome-Commercial-Insurer-Policies-Are-Impacting-Patient-Care.pdf). Established denial rate, appeal cost, and overturn evidence.

11. **`CMS claim denial appeal administrative burden report 2024`**  
    Consulted the [AHA brief](https://www.aha.org/system/files/media/file/2024/09/Skyrocketing-Hospital-Administrative-Costs-Burdensome-Commercial-Insurer-Policies-Are-Impacting-Patient-Care.pdf), [Senate hearing record](https://www.congress.gov/118/chrg/CHRG-118shrg55699/CHRG-118shrg55699.pdf), and CMS docket comments. Used the first two; docket comments were treated as stakeholder evidence, not neutral measurement.

12. **`claims denial management RFP contract award budget hospital`**  
    No reliable public hospital contract-award value surfaced. Recorded as an explicit payer-budget gap.

13. **`solar installer cash flow equipment procurement price volatility survey 2024`**  
    No credible quantified installer cash-flow or procurement-loss survey surfaced. The solar card therefore limits magnitude claims to observed tender requirements.

14. **`Poland photovoltaic public tender budget 2025 installation procurement`**  
    Consulted [TED notice 334566-2025](https://ted.europa.eu/en/notice/334566-2025/pdf). Confirmed Polish municipal scope, EU funding, schedule, technical purchasing language, and 10,000 PLN bid security.

15. **`solar installer software pricing proposal procurement inventory`**  
    Consulted [ENACT pricing](https://enact.solar/providers/provider-pricing/), [SolarSAAS](https://solarsaas.com/pricing), and related installer-software results. ENACT supplied the clearest public BOM/proposal purchasing price.

16. **`accounts payable duplicate payments benchmark 2024 invoice errors`**  
    Consulted [APQC](https://www.apqc.org/resource-library/resource-listing/percentage-duplicate-disbursements-processed), the [College Station audit](https://www.cstx.gov/media/wdsk3onh/24-02-accounts-payable-audit.pdf), and [Oversight](https://www.oversight.com/hubfs/assets/Resources/Whitepapers-and-Guides/Disarming-Risk-in-AP-2023.pdf?hsLang=en). Separated the official observed mechanism from the vendor-mediated benchmark.

17. **`accounts payable automation RFP award value invoice matching`**  
    Reviewed the [E&I AP automation RFP](https://www.eandi.org/wp-content/uploads/1._RFP_EI00349_-_AP_Automation_Optimization-IRR2024.11.06.pdf). It confirmed invoice-to-payment workflow purchasing language but did not expose a usable award value.

18. **`accounts payable automation software pricing per invoice`**  
    Consulted [Quick Payable](https://quickpayable.com/pricing), [Payhouse](https://www.payhouse.app/), and [Tipalti](https://tipalti.com/pricing/). Quick Payable and Payhouse supplied explicit per-user and per-invoice prices.

# Evidence Island 3

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

## Complete trace

Local access: read only `scout_operational_failure.md` using `sed -n '1,240p'`. No other local path was read. Web searches were executed in batches of `4 + 4 + 4 + 4 + 2`, totaling exactly **18 unique queries**. Subsequent web actions were page opens or in-page finds, not searches.

1. `2024 2025 hospital operating theatre cancellations equipment sterile instruments delay cost report`  
   Led to NHS cancellation statistics; no reliable nationwide sterile-instrument-only count.

2. `NHS cancelled operations non clinical reasons equipment 2024 data`  
   Produced E-OF-001 and E-OF-002.

3. `sterile services instrument shortage surgery delays hospital procurement budget 2025`  
   Supported the operational-cause sweep; no stronger dated national instrument-specific source retained.

4. `2024 pharmacy drug shortages staff hours cost survey Europe UK`  
   Produced CPE, IPU and Royal Pharmaceutical Society evidence used in E-OF-004, E-OF-005 and E-OF-007.

5. `2024 truck driver detention time distribution facilities cost report shipper survey`  
   Produced ATRI-related results and the shipper questionnaire; findings retained through E-OF-008.

6. `FMCSA driver detention lost productivity annual cost 2024`  
   Produced detention-loss reporting and the DOT/OIG figures cited through E-OF-010.

7. `2025 freight detention fees warehouse appointment delays shipper budget`  
   Produced fee evidence; commercial benchmark pages were treated as weak and not used for aggregate loss.

8. `2024 manufacturing unplanned downtime cost survey equipment failure hours`  
   Produced E-OF-012 and E-OF-013.

9. `Community Pharmacy England 2024 medicine shortages daily staff time financial loss pharmacy owners survey`  
   Produced the direct CPE report, parliamentary corroboration and E-OF-006.

10. `Ireland pharmacist medicine shortages 2025 hours monthly survey reimbursement cost`  
    Produced E-OF-005 and the six-hour-22-minute weekly estimate.

11. `2025 industrial maintenance spare parts shortage downtime survey budget maintenance spending`  
    Added parts-inventory and maintenance-spending context; no additional independent audited benchmark retained.

12. `2024 manufacturers maintenance budget reactive maintenance backlog survey unplanned downtime`  
    Added preventive/run-to-failure and investment evidence to E-OF-012/E-OF-013.

13. `2024 wastewater utility sewer blockages annual incidents cost clearing fatbergs report`  
    Produced E-OF-014.

14. `Ofwat blocked sewers 2024 performance cost wastewater companies`  
    Produced Ofwat performance and penalty material reflected in E-OF-015/E-OF-016.

15. `2025 water company sewer blockage reactive maintenance budget UK annual report`  
    Produced environmental-programme budget and performance evidence in E-OF-015.

16. `2024 solar installer grid connection delays application backlog DNO survey UK Europe`  
    Produced UK connection-queue evidence and a dated RWE delay case; used as contextual corroboration, not as Polish magnitude evidence.

17. `Poland photovoltaic grid connection refusals 2024 URE data connection capacity renewable developers`  
    Produced E-OF-017, E-OF-018 and E-OF-020.

18. `2025 solar PV grid connection application delays installer cash flow project cancellation survey Europe`  
    Produced E-OF-019; no robust installer cash-flow magnitude was located.

Access limitations recorded during validation:

- CPE’s direct 2024 PDF and MaintainX’s direct report exceeded the page-fetch size limit; their findings were checked through accessible professional/industry coverage.
- ATRI’s questionnaire PDF and two Overdrive pages returned access restrictions; accessible MIT, Trucking Dive and federal material supplied corroboration.
- Several Ofwat pages returned access restrictions; the accessible Environment Agency report supplied official performance and budget figures.
- The HSE community-pharmacy agreement redirected to a temporary website-update page; the underlying time evidence was verified on the IPU page.
- Commercial vendor pages, Reddit anecdotes, Wikipedia results and future-looking promotional claims were not used as primary magnitude evidence.

# Evidence Island 4

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

# Evidence Island 5

## P-technical_scientific_change-01

**Problem:** Digital-pathology validation and interoperability impose repeated cost and integration loss on device sponsors and pathology laboratories.

- **Actor/outcome:** Whole-slide-imaging device sponsors fund clinical validation; hospital pathology laboratories absorb integration, validation, storage, and workflow disruption when systems rely on proprietary formats. The adverse outcome is delayed deployment and duplicated validation rather than a quantified diagnostic backlog.
- **Observable loss / frequency / magnitude status:**
  - **Observed:** FDA says authorization still relies heavily on costly clinical studies and identifies missing standardized tests linking technical performance to diagnostic performance.
  - **Recurring:** Each distinct scanner, image pipeline, site configuration, or materially changed workflow may create another validation boundary.
  - **Magnitude:** Per-study and per-laboratory costs were not disclosed in the trace.
- **Current workaround:** End-to-end proprietary scanner pipelines, local validation, manual review, and costly clinical studies.
- **Technical/scientific change:** Clinical feasibility has advanced beyond the first 2017 WSI authorization. FDA records include pathology AI authorizations such as Galen Second Read on 2025-01-24 and ArteraAI Prostate on 2025-07-31. The change establishes that AI-assisted pathology can clear a clinical authorization pathway, while interoperability and generalizable technical evaluation remain unresolved.
- **Payer/budget evidence:** Sponsors repeatedly finance FDA submissions and associated studies. Ontario Health’s 2026 provincial planning direction explicitly anticipates procurement requirements for compatibility and interoperability, establishing health-system procurement as a budget owner; no contract value was exposed.
- **Counterevidence:** FDA describes digital pathology as a novel device space with few studies connecting technical and diagnostic performance. Existing authorizations establish feasibility for specific indications, not portable performance across scanners, stains, laboratories, or populations.
- **Unknowns:** Validation cost per deployment; number of laboratories blocked primarily by interoperability; effect on turnaround time; European conformity-assessment burden; whether procurement is controlled by laboratories, hospital IT, regional systems, or scanner vendors.
- **IDs:** `island_id=technical_scientific_change`; `creator_id=shadow-scout-05`; `evidence_id=E-technical_scientific_change-01`.
- **Source trace:**
  - FDA, undated living program page, accessed 2026-08-22: [Digital Pathology Program](https://www.fda.gov/medical-devices/medical-device-regulatory-science-research-programs-conducted-osel/digital-pathology-program-research-digital-pathology-medical-devices).
  - FDA, living list accessed 2026-08-22; device decisions dated 2025-01-24 and 2025-07-31: [AI-Enabled Medical Devices](https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices).
  - Ontario Health, indexed in 2026; exact publication day unavailable to the trace: [Operational Direction: Provincial Digital Pathology Planning](https://ontariohealth.ca/news/operational-direction--provincial-digital-pathology-planning).

## P-technical_scientific_change-02

**Problem:** Public water systems incur high per-sample expense and slow, laboratory-bound decision cycles when measuring PFAS at very low concentrations.

- **Actor/outcome:** Municipal water-system operators pay for collection, accredited analysis, confirmation, and performance monitoring. The loss is testing expense, delayed operational decisions, and possible repeat work after contamination of samples or blanks.
- **Observable loss / frequency / magnitude status:**
  - **Observed unit cost:** Wisconsin’s public laboratory lists $380 per EPA 537.1 sample plus $300 if the field reagent blank is analyzed; broader water analysis is $450 per sample.
  - **Observed national magnitude:** EPA’s quantified annual monitoring cost is approximately $36 million. GAO reports a revised total quantified compliance-cost estimate of $1.5 billion, including monitoring, treatment, and administration.
  - **Frequency:** Initial, continuing, confirmation, pilot, and treatment-performance sampling create repeated demand. Exact samples per utility depend on system configuration and results.
- **Current workaround:** Samples are collected with PFAS-specific handling controls and shipped to certified laboratories for solid-phase extraction and LC-MS/MS analysis. A field reagent blank travels through the sampling process to detect incidental contamination.
- **Technical/scientific change:** Validated Methods 533 and 537.1 can measure 29 PFAS in drinking water. Method 1633A extends listed laboratory offerings to 40 compounds across additional matrices. This is a material sensitivity and scope improvement over earlier monitoring whose multi-laboratory reporting level for PFBS was 90 ng/L.
- **Payer/budget evidence:** Published public-laboratory prices provide direct transaction evidence. EPA separately budgets monitoring and laboratory-analysis costs at national scale.
- **Counterevidence:** The equipment remains laboratory-bound, expensive, contamination-sensitive, and staff-intensive. EPA states that alternative techniques have not been evaluated or approved for the same monitoring uses. Newer analytical scope therefore does not establish low-cost field measurement.
- **Unknowns:** Certified-laboratory capacity by region; actual turnaround distribution; repeat-test rate; Poland/EU prices; share of expenditure attributable to preparation versus instrumentation; utility willingness to buy non-compliance screening.
- **IDs:** `island_id=technical_scientific_change`; `creator_id=shadow-scout-05`; `evidence_id=E-technical_scientific_change-02`.
- **Source trace:**
  - EPA, living page accessed 2026-08-22: [PFAS Drinking Water Laboratory Methods](https://www.epa.gov/pfas/epa-pfas-drinking-water-laboratory-methods).
  - EPA, April 2024: [Final PFAS NPDWR Technical Overview](https://19january2025snapshot.epa.gov/system/files/documents/2024-04/drinking-water-utilities-and-professionals-technical-overview-of-pfas-npdwr.pdf).
  - GAO, 2025, discussing April 2024 estimates: [GAO-25-107897](https://www.gao.gov/assets/gao-25-107897.pdf).
  - Wisconsin State Laboratory of Hygiene, prices effective 2025-11-01: [PFAS testing and prices](https://www.slh.wisc.edu/environmental/pfas/).
  - EPA, April 2024: [PFAS occurrence technical support document](https://www.epa.gov/system/files/documents/2024-04/updated-technical-support-document-on-pfas-occurrence_final508.pdf).

## P-technical_scientific_change-03

**Problem:** Excavators and buried-utility owners suffer project delays, outages, and damage because locate responses and underground records are incomplete or inaccurate.

- **Actor/outcome:** Excavators cannot begin work on time or strike a buried asset; utilities, contractors, communities, and insurers then absorb repairs, emergency response, outages, lost productivity, and construction delay.
- **Observable loss / frequency / magnitude status:**
  - **Reported:** The 2024 DIRT analysis contained 196,977 unique damage reports. Eight 811 centers showed an average 38% probability that an excavator could not start on time because locate responses were incomplete.
  - **Modeled:** CGA’s August 2026 economic report modeled 668,999 incidents in 2025 and $83.2 billion in annual impact, including $31.6 billion of business disruption and $4.9 billion of direct repair.
  - **Root-cause frequency:** Locator failure to mark, inaccurate marks, no response, and incorrect records together represent material shares of reported causes.
- **Current workaround:** 811 notification, review of legacy maps, paint and flag marking, electromagnetic locating, potholing, and outsourced subsurface-utility-engineering work.
- **Technical/scientific change:** Multichannel and stepped-frequency GPR can gather denser data in parallel; vehicle-mounted configurations scan roads at higher speed. FHWA states that parallel collection can reduce field operator hours and that multiple geophysical modalities improve completeness.
- **Payer/budget evidence:** Lexington-Fayette approved a fully budgeted, one-year underground locating contract capped at $150,000 on 2026-01-22. FHWA documents state transportation agencies procuring or piloting multichannel GPR and electromagnetic-induction capabilities.
- **Counterevidence:** GPR performance degrades in conductive or clay-rich soils; moisture, depth, utility material, clutter, calibration, and operator expertise constrain accuracy. The $83.2 billion loss is a modeled high-reporting scenario based on the 94th percentile of consistent reporters, not an audited sum of invoices.
- **Unknowns:** False-positive and missed-asset rates by terrain; economics for small municipal networks; responsibility for updating records after discovery; European damage frequency; portion of loss preventable through better sensing rather than notification and excavation practice.
- **IDs:** `island_id=technical_scientific_change`; `creator_id=shadow-scout-05`; `evidence_id=E-technical_scientific_change-03`.
- **Source trace:**
  - CGA, 2024 data published 2025-08-28: [2024 DIRT report summary](https://www.einpresswire.com/article/843655724/cga-dirt-report-highlights-concerning-levels-of-damages-to-buried-utilities-signals-need-for-industry-wide-changes).
  - CGA, published 2026-08-13: [Buried-utility economic-impact report summary](https://www.einpresswire.com/article/933922254/new-report-underground-utility-damage-costs-america-83-2-billion-a-year-nearly-triple-previous-estimate).
  - Lexington-Fayette Urban County Government, approved 2026-01-22: [Resolution R-023-2026](https://lexington.legistar.com/LegislationDetail.aspx?FullText=1&GUID=3D306DE7-6CC1-4027-A655-3600A5BB7971&ID=7795706).
  - FHWA, living technical page accessed 2026-08-22: [Underground Utilities—GPR](https://infotechnology.fhwa.dot.gov/gpr-ground-penetrating-radar-utility-general/).
  - FHWA, living implementation record accessed 2026-08-22: [Utility Investigation Technologies](https://www.fhwa.dot.gov/goshrp2/Solutions/All/R01B/Utility_Investigation_Technologies).

## P-technical_scientific_change-04

**Problem:** Food manufacturers lose saleable inventory and incur recall handling when undeclared allergens arise from cross-contact, ingredients, or labeling and packaging mistakes.

- **Actor/outcome:** Manufacturers, distributors, and retailers remove, relabel, or destroy products; consumers face possible serious allergic reactions.
- **Observable loss / frequency / magnitude status:**
  - **Observed:** RQA counted 116 allergen-related FDA recall events affecting 214 products in January–June 2025. Allergens and allergen-labeling errors represented 42% of recall events.
  - **Broader context:** FDA states that more than 83,000 FDA-regulated products were recalled between 2014 and 2024, although this includes sectors beyond food and does not measure unique allergen incidents.
  - **Magnitude:** Product volume, manufacturer-specific handling cost, lost sales, and liability were not disclosed.
- **Current workaround:** Supplier documentation, line cleaning, segregation, single-analyte testing, packaging checks, voluntary market removal, and—in limited pre-retail cases—affixing corrected allergen labels.
- **Technical/scientific change:** A 2025 USDA/FSIS procurement describes an assay that simultaneously analyzes 15 allergens on existing BioPlex instrumentation. Multiplexing changes laboratory throughput and interoperability compared with serial single-analyte checks.
- **Payer/budget evidence:** USDA/FSIS identified routine demand and an estimated $98,000 fixed-price purchase for compatible multiplex allergen kits.
- **Counterevidence:** RQA classifies 29% of H1 2025 recall events as preventable “never events,” including wrong labels and products placed in the wrong packaging. Chemical testing does not address every such failure, and testing a sample does not prove the absence of heterogeneous cross-contact throughout a batch.
- **Unknowns:** Recall cost distribution by firm size; number of lots tested per line change; test-kit consumption per facility; sensitivity in processed matrices; false-negative rates; European purchasing evidence; proportion of allergen recalls attributable to formulation data versus physical contamination.
- **IDs:** `island_id=technical_scientific_change`; `creator_id=shadow-scout-05`; `evidence_id=E-technical_scientific_change-04`.
- **Source trace:**
  - RQA Group, H1 2025 report published August 2025: [Product Recall Report H1 2025](https://www.rqa-group.com/wp-content/uploads/2025/08/RQA-Group-Product-Recall-Report-H1-2025-1.pdf).
  - FDA, updated 2025 and accessed 2026-08-22: [FDA 101: Product Recalls](https://www.fda.gov/consumers/consumer-updates/fda-101-product-recalls).
  - USDA/FSIS procurement notice issued 2025-08-05: [xMAP food-allergen assay procurement](https://www.highergov.com/contract-opportunity/xmap-food-allergen-detection-assay-allergen-test-k-123a9425p0020-u-8e344/).
  - FDA, living page accessed 2026-08-22: [Food Allergies](https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/food-allergies).

## P-technical_scientific_change-05

**Problem:** Vaccine custodians incur quarantine, investigation, and possible replacement loss when storage or shipment temperatures leave the permitted range.

- **Actor/outcome:** Stockpile operators, distributors, pharmacies, and vaccination providers must stop using affected inventory until viability is determined. Potency loss can require replacement and delay administration.
- **Observable loss / frequency / magnitude status:**
  - **Observed process loss:** Every excursion requires immediate segregation, documentation, manufacturer or program assessment, and disposition.
  - **Magnitude:** CDC explicitly identifies financial hardship from replacing vaccine that has lost potency, but the trace did not establish an excursion rate, affected-dose count, or annual dollar loss.
  - **Frequency status:** Operationally recurring but unquantified.
- **Current workaround:** Continuous digital data loggers, manual temperature-log review, alarms, “DO NOT USE” quarantine, and manufacturer review of excursion magnitude and duration. CDC instructs custodians not to discard exposed vaccine before assessment.
- **Technical/scientific change:** Current monitoring can record the complete duration and magnitude of an excursion rather than only minimum and maximum temperatures. Research published in 2024 reports an inkjet-printed flexible sensor spanning approximately −30°C to 80°C. Government procurement now specifies real-time Bluetooth, Wi-Fi, or GPS tracking for ultra-cold monitoring.
- **Payer/budget evidence:** HHS’s Strategic National Stockpile sought 7,300 devices: 4,800 standard cold-chain monitors and 2,500 units operating down to −80°C with real-time tracking. The contract value was not exposed in the accessible record.
- **Counterevidence:** An out-of-range reading does not prove potency loss. CDC requires case-specific assessment and expressly says not to discard immediately. Printed-sensor laboratory feasibility does not by itself satisfy calibration, traceability, serialization, cybersecurity, battery-life, or ±1°C procurement requirements.
- **Unknowns:** Excursion incidence; inventory value per event; proportion ultimately released; procurement value; sensor calibration drift; data-connectivity failures; liability allocation among shipper, warehouse, and recipient.
- **IDs:** `island_id=technical_scientific_change`; `creator_id=shadow-scout-05`; `evidence_id=E-technical_scientific_change-05`.
- **Source trace:**
  - CDC, July 2026: [Vaccine Storage and Handling Toolkit](https://www.cdc.gov/vaccines/hcp/downloads/storage-handling-toolkit.pdf).
  - HHS/SNS procurement, 2025: [Temperature Monitoring Devices RFP 75A50325R00010](https://www.highergov.com/contract-opportunity/rfp-75a50325r00010-temperature-monitoring-device-75a50325r00010-o-026e9/).
  - Scientific article, published 2024: [Inkjet-printed sub-zero temperature sensor for real-time monitoring of cold environments](https://www.sciencedirect.com/science/article/pii/S0141813023056738).

## P-technical_scientific_change-06

**Problem:** Renewable generators and grid operators lose energy value and incur redispatch and balancing work when distributed wind and solar output diverges from demand, forecasts, and controllable grid capacity.

- **Actor/outcome:** Generators experience curtailment or negative prices; PSE and other TSOs must procure or activate redispatch and balancing resources to maintain system balance.
- **Observable loss / frequency / magnitude status:**
  - **Observed in Poland:** From 2024-01-01 through 2024-06-15, non-market redispatch was used on 33 days; more than 60% occurred on weekends or public holidays.
  - **Event magnitude:** On 2024-05-01, redispatch ran from 07:00 to 18:00 and averaged 936 MW of onshore wind plus 3,291 MW of solar. Renewable generation exceeded 60% of demand during the event, and imbalance prices were negative for most of it.
  - **Budget magnitude:** European TSOs reported €9.999 million in 2024 platform establishment/amendment costs and €3.007 million in operating costs. PSE’s disclosed 2024 MARI-platform share was about €267,023.
- **Current workaround:** Non-market redispatch, manual and automatic frequency-restoration reserves, negative imbalance prices, generator shutdown instructions, and shared European balancing platforms.
- **Technical/scientific change:** FuXi-2.0 reports hourly global weather output and better performance than ECMWF HRES for several sector-relevant variables and wind-power forecasting. Lower computation cost and hourly resolution alter the feasibility of more frequent renewable forecasts.
- **Payer/budget evidence:** ENTSO-E itemizes TSO spending on platform IT development, hosting, monitoring, testing, project management, and external specialists. Generators are also paid to reduce production in some balancing markets, including a Spanish example where downward mFRR reached −€1,000/MWh.
- **Counterevidence:** ENTSO-E attributes excess-generation events to several factors beyond forecast error, including subsidy design, lack of controllability, congestion, and behind-the-meter assets. A 2025 study found conventional HRES forecasts consistently better than leading AI models for record-breaking heat, cold, and wind extremes.
- **Unknowns:** Avoidable share of Polish redispatch; plant-level revenue loss; access to behind-the-meter telemetry; forecast-error contribution relative to market design and network limits; integration and verification cost; performance on Polish weather and distributed-PV data.
- **IDs:** `island_id=technical_scientific_change`; `creator_id=shadow-scout-05`; `evidence_id=E-technical_scientific_change-06`.
- **Source trace:**
  - ENTSO-E, 2025: [Flexibility from Renewable Energy Sources](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/Reports/2025/251118_entso-e_flexibility_from_RES_Report.pdf).
  - ENTSO-E, 2025-06-06: [Electricity Balancing Cost Report 2025](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/Publications/2025/entso-e_Electricity_Balancing_Cost_Report_2025.pdf).
  - Chen et al., submitted 2024-09-11: [FuXi-2.0](https://arxiv.org/abs/2409.07188).
  - 2025 counter-study: [Numerical models outperform AI weather forecasts of record-breaking extremes](https://arxiv.org/abs/2508.15724).

### Complete 18-query trace

1. `2024 pathology laboratory diagnostic backlog workforce shortage error cost hospital digital pathology FDA primary source`
2. `2025 hospital pathology laboratory capital budget digital pathology spending procurement evidence`
3. `FDA 2024 AI pathology device clearance whole slide imaging interoperability technical capability`
4. `2024 PFAS drinking water laboratory testing capacity cost utilities EPA compliance budget`
5. `EPA Methods 533 537.1 PFAS laboratory equipment LC MS MS detection limits 2024 primary`
6. `2025 PFAS laboratory sample turnaround time capacity utility testing cost evidence`
7. `2024 underground utility damage frequency annual cost Common Ground Alliance DIRT report`
8. `2025 utility locating procurement budget 811 tickets public works contract cost`
9. `2024 FHWA underground utility mapping ground penetrating radar digital records accuracy research technical capability`
10. `2024 FDA food allergen recalls frequency economic loss manufacturers report`
11. `2025 food manufacturer allergen testing laboratory procurement contract budget rapid testing`
12. `2024 rapid food allergen detection biosensor accuracy multiplex research primary source`
13. `2024 pharmaceutical cold chain temperature excursion frequency product loss biologics GDP report`
14. `2025 hospital pharmacy vaccine cold chain monitoring procurement contract budget temperature data logger`
15. `2024 printable temperature sensor cold chain accuracy low cost scientific paper pharmaceutical`
16. `2025 renewable energy curtailment frequency cost grid operators Europe ENTSO-E report`
17. `2025 distribution utility grid hosting capacity data procurement budget interconnection study contract`
18. `2024 AI weather forecasting renewable power forecast accuracy scientific technical change primary source`

# Evidence Island 6

# Shadow Scout Artifact

- `island_id`: `rules_finance_assets_transitions`
- `creator_id`: `shadow-scout-06`
- `research_date`: `2026-08-22`
- `query_count`: `18 unique queries`
- Evidence boundary: primary legislation, regulators, ministries, public funds, grid operators, and state audit material. Enacted requirements are separated from administrative decisions, guidance, and proposals.

---

## P-rules_finance_assets_transitions-01 — Hourly net-billing leaves new prosumers exposed to low export credits and non-offsettable charges

- `island_id`: `rules_finance_assets_transitions`
- `creator_id`: `shadow-scout-06`
- `evidence_ids`: `E-RFAT-01-A` through `E-RFAT-01-D`
- `query_ids`: `Q01–Q03`

**Actor/outcome**

Polish household prosumers whose installations first supplied electricity after 1 July 2024 are settled using the actual hourly market price, while older prosumers can remain on monthly RCEm settlement. The household can therefore export most PV surplus during low-price midday hours but later purchase electricity at the retail price and continue paying distribution and other charges that the prosumer deposit cannot offset.

**Binding status and transition**

This is enacted law, not a proposal. The Act of 27 November 2024 was published as Dz.U. 2024 poz. 1847 and entered into force after its statutory vacatio legis. The Ministry confirms that post-1 July 2024 prosumers remain on hourly RCE, while eligible earlier prosumers may remain on RCEm. [E-RFAT-01-A: enacted amending act](https://eli.gov.pl/api/acts/DU/2024/1847/text.html) [E-RFAT-01-B: Ministry explanation](https://www.gov.pl/web/klimat/prosument-pytania)

**Loss, frequency, magnitude**

- Loss recurs with every billing period and is generated at hourly resolution.
- The URE national report records more than 1.5 million prosumers and 12.7 GW of prosumer capacity at the end of 2024; this is total system exposure, not the number demonstrably suffering a loss.
- More than one quarter of the electricity-related applications received by the URE Negotiation Coordinator in 2024 came from prosumers. Frequent allegations included export prices being too low relative to purchase prices, incorrect deposit settlement, and high bills despite a large deposit.
- Distribution charges remain payable outside the deposit. Household-level monetary loss cannot be established from the public evidence because load shape, self-consumption, tariff, installation date, and hourly prices differ. [E-RFAT-01-C: URE Negotiation Coordinator, 29 April 2025](https://koordynator.ure.gov.pl/kdn/koordynator/sprawozdania/12632%2CSprawozdanie-za-2024-r.html) [E-RFAT-01-D: URE National Report 2025](https://www.ure.gov.pl/download/9/15763/Raport2025-ostateczna.pdf)

**Existing workaround**

Eligible pre-1 July 2024 prosumers can remain on RCEm. The 2024 amendment automatically increases the credited deposit value by 23%; prosumers electing RCE can receive up to 30% of unused deposit value after the statutory period rather than the earlier 20%. Greater contemporaneous self-consumption reduces exposure, but post-1 July 2024 prosumers cannot elect monthly RCEm.

**Payer/budget evidence**

The household is the direct payer through its electricity bill. The deposit offsets only electricity-sale charges, not distribution and other regulated charges. No public reimbursement budget covers the difference between hourly export credits and the household’s later retail purchase cost.

**Counterevidence**

- Hourly settlement does not always cause loss: the Ministry states it can benefit households that align consumption and exports with hourly prices.
- The 23% deposit uplift materially softened the earlier rules.
- URE dispute applications are self-selected and cannot establish prevalence across all prosumers.
- RCEm protects the eligible older cohort from hourly-price exposure.

**Unknowns**

- Distribution of annual losses by installation size, retailer, tariff, and household load profile.
- Number of post-1 July 2024 prosumers receiving materially worse results than they would under RCEm.
- Frequency of zero-price credits and exhausted deposits by retailer.
- Whether billing-system errors or the settlement formula account for the larger share of disputed bills.

---

## P-rules_finance_assets_transitions-02 — Clean Air funding interruptions and delayed reimbursements transfer working-capital pressure to households and contractors

- `island_id`: `rules_finance_assets_transitions`
- `creator_id`: `shadow-scout-06`
- `evidence_ids`: `E-RFAT-02-A` through `E-RFAT-02-D`
- `query_ids`: `Q04–Q06`

**Actor/outcome**

Owners renovating single-family homes, and contractors relying on beneficiary reimbursements or prefinanced grants, can be left financing completed work while applications or payment claims are unavailable or delayed.

**Binding status and transition**

This was an administrative financing decision, not legislation. NFOŚiGW stopped accepting new general applications on 28 November 2024 and reopened the revised programme on 31 March 2025. The transition allowed qualifying expenditure dating back to 28 May 2024, but claims had to satisfy the revised programme conditions. [E-RFAT-02-A: NFOŚiGW pause notice, 28 November 2024](https://czystepowietrze.gov.pl/wazne-komunikaty/czas-na-remont-programu-czyste-powietrze-w-trosce-o-beneficjentow) [E-RFAT-02-B: reopening transition document, 31 March 2025](https://czystepowietrze.gov.pl/wazne-komunikaty/2025-03-31-startuje-nowe-czyste-powietrze/nowy_program_czyste_powietrze_31_03_2025_prezentacja.pdf)

**Loss, frequency, magnitude**

- The application pause lasted from 28 November 2024 until 31 March 2025.
- In NIK’s Warsaw-fund sample, 93 of 205 examined agreements received advances 60–215 days after a correct and complete payment request, despite contractual terms providing for payment within 30 days.
- NIK states that delays in 2024 included periods when NFOŚiGW lacked funds for advances.
- In 2024, the Warsaw fund completed and settled 10,337 agreements worth PLN 336.0952 million and spent PLN 636.975 million on the programme. These figures establish the scale of the payer’s budget but should not be extrapolated nationally.
- The loss is recurring per delayed claim: household or contractor capital remains tied up, and any financing cost or inability to begin subsequent work persists until payment. The public evidence does not quantify interest, contractor insolvency, or cancelled projects. [E-RFAT-02-C: NIK post-audit report, control P/25/040](https://www.nik.gov.pl/kontrole/wyniki-kontroli-nik/pobierz%2Cksi~p_25_040_202509090849061757400546~id1~01%2Ctyp%2Ckj.pdf)

**Existing workaround**

The reopened programme included a transition period for earlier expenditure. Under the revised programme, operators became mandatory for the highest subsidy level and prefinancing cases. These provisions do not reimburse financing costs already incurred during a delay.

**Payer/budget evidence**

NFOŚiGW and the provincial WFOŚiGW funds are the grant payers, drawing on NFOŚiGW, KPO, and FEnIKS resources. The Warsaw fund’s audited expenditure provides direct budget evidence. Until reimbursement, the affected household or contractor is the interim payer.

**Counterevidence**

- The November 2024 decision stopped new applications but did not formally stop processing existing files or all payments.
- NFOŚiGW stated that positively assessed applications and signed agreements within programme limits would be paid.
- The programme reopened, and by 10 July 2025 the new intake had received 14,000 applications requesting PLN 803 million and had signed agreements exceeding PLN 100 million. [E-RFAT-02-D: NFOŚiGW update, 14 July 2025](https://czystepowietrze.gov.pl/wazne-komunikaty/nowe-czyste-powietrze---trzy-miesiace-po-otwarciu-naboru-przybywa-wnioskow-i-podpisanych-umow)
- NIK positively assessed the accuracy of the Warsaw fund’s 2024 financial report and found that completed projects achieved programme objectives.

**Unknowns**

- National rather than Warsaw-only distribution of payment delays.
- Amount of contractor receivables and household bridge financing attributable to the pause.
- Number of transition-period claims rejected because revised eligibility rules differed.
- Whether payment timeliness remained impaired after the 2025 restart.

---

## P-rules_finance_assets_transitions-03 — F-gas cutovers can strand heat-pump inventory and expand installer certification burdens

- `island_id`: `rules_finance_assets_transitions`
- `creator_id`: `shadow-scout-06`
- `evidence_ids`: `E-RFAT-03-A`, `E-RFAT-03-B`
- `query_ids`: `Q07–Q09`

**Actor/outcome**

Heat-pump and air-conditioning importers, distributors, installers, service companies, technicians, and equipment owners face staggered refrigerant cutovers. Affected equipment cannot be first placed on the EU market after the applicable date, while work involving both F-gases and specified alternative refrigerants falls within expanded certification programmes.

**Binding status and transition**

Regulation (EU) 2024/573 is directly applicable EU law and entered into force in March 2024. Relevant enacted cutovers include:

- 1 January 2025: single-split systems containing less than 3 kg of Annex I gas with GWP of at least 750;
- 1 January 2027: self-contained heat pumps up to 12 kW with F-gas GWP of at least 150, and split air-to-water systems up to 12 kW with GWP of at least 150, subject to safety exceptions;
- later staged prohibitions for other split and self-contained equipment.

The Commission’s September 2024 implementing package extended mandatory certification coverage to technicians working with certain refrigerant alternatives. [E-RFAT-03-A: Regulation (EU) 2024/573](https://eur-lex.europa.eu/eli/reg/2024/573/2024-02-20/eng) [E-RFAT-03-B: Commission certification notice, 20 September 2024](https://climate.ec.europa.eu/news-other-reads/news/f-gases-new-rules-labelling-reporting-certification-and-f-gas-portal-2024-09-20_en)

**Loss, frequency, magnitude**

- Inventory exposure occurs once for every affected unit not lawfully placed on the market before its cutoff.
- Certification and refresher exposure occurs per technician and certified business. Existing certificate holders must enter refresher training or evaluation cycles; the first required refresh is no later than 12 March 2029.
- Operators of covered equipment incur recurring recordkeeping, leak-check, recovery, and service obligations.
- From 1 January 2026, virgin F-gases with GWP of at least 2,500 cannot be used to service heat pumps and air-conditioning equipment; reclaimed or recycled gas remains permitted under conditions until 2032.
- No primary source retrieved quantified Polish inventory write-downs, training costs, service-price increases, or the number of technicians requiring expanded certification.

**Existing workaround**

Existing certificates remain valid under their original conditions pending the new refresher deadlines. Parts needed to repair existing equipment may still be marketed if the work does not raise capacity or refrigerant charge or change the gas type. Lawfully pre-cutoff equipment can continue to be supplied after the first year only with proof of lawful earlier placement. Safety exceptions and Commission exemptions of up to four years can apply in defined circumstances.

**Payer/budget evidence**

The importer or distributor bears unsaleable-inventory and conformity exposure. Certified businesses and technicians bear certification and training costs unless an employer pays them. Equipment owners pay recurring leak checks, servicing, recovery, and replacement costs. The regulation establishes private obligations; no general public compensation budget is identified.

**Counterevidence**

- The rule restricts placement of specified new equipment, not the continued operation of every installed heat pump.
- Repair parts and servicing of existing equipment remain possible within stated limits.
- Safety-based derogations can preserve F-gas equipment where alternatives cannot lawfully or safely be used.
- The Commission must monitor whether F-gas scarcity endangers heat-pump deployment and can adjust quota availability.

**Unknowns**

- Polish inventory by refrigerant, GWP, power rating, and legal placement date.
- Certification capacity and current technician backlog in Poland.
- Cost and availability of reclaimed refrigerants after the 2026 servicing cutoff.
- Frequency with which safety or temporary exemptions will be granted.

---

## P-rules_finance_assets_transitions-04 — The fossil-boiler subsidy cutoff leaves households bearing full installation cost outside a narrow legacy exception

- `island_id`: `rules_finance_assets_transitions`
- `creator_id`: `shadow-scout-06`
- `evidence_ids`: `E-RFAT-04-A` through `E-RFAT-04-D`
- `query_ids`: `Q10–Q12`

**Actor/outcome**

Households planning a new stand-alone gas, oil, or coal boiler can no longer rely on newly granted public subsidies, preferential public loans, or fiscal incentives covered by Article 17(15). Contractors serving that segment lose subsidy-supported orders. A closed Polish legacy cohort of households that installed gas boilers during 2024 faced a delayed, capped catch-up process.

**Binding status and transition**

Article 17(15) of Directive (EU) 2024/1275 required Member States, by 1 January 2025, to stop financial incentives for new stand-alone fossil-fuel boilers, except investments selected before 2025 under specified EU programmes. The Commission notice is interpretive guidance; the binding obligation is in the directive. Most other EPBD provisions had a 29 May 2026 transposition deadline. [E-RFAT-04-A: Directive (EU) 2024/1275](https://eur-lex.europa.eu/legal-content/PL/TXT/?uri=CELEX%3A32024L1275) [E-RFAT-04-B: Commission guidance, 17 October 2024](https://energy.ec.europa.eu/news/commission-issues-guidance-phasing-out-financing-stand-alone-boilers-powered-fossil-fuels-2025-2024-10-17_en)

The retrieved material establishes the EU obligation and the Polish programme response but does not independently identify the complete Polish transposing legislation.

**Loss, frequency, magnitude**

- Prospective loss occurs once per otherwise subsidy-eligible boiler installation: the household bears the portion formerly covered by public aid.
- For the legacy Polish cohort, applications reopened on 15 July 2025 for installations completed between 28 May and 31 December 2024.
- The catch-up budget was PLN 70 million from FEnIKS and was expected to support about 3,000 households.
- The intake ultimately closed on 17 November 2025 or exhaustion of the budget. Household shortfalls and the number of eligible but unpaid applicants were not disclosed. [E-RFAT-04-C: Polish gas-boiler catch-up intake](https://czystepowietrze.gov.pl/wazne-komunikaty/wazna-data-wplywu-ruszyl-nabor-na-dotacje-do-kotlow-gazowych) [E-RFAT-04-D: closing notice](https://czystepowietrze.gov.pl/wazne-komunikaty/ostatni-dzwonek-na-dotacje-gazowa-nabor-konczy-sie-17-listopada)

**Existing workaround**

The directive preserves incentives selected under the specified EU funds before 2025. It also permits support for maintenance, repair, decommissioning, transition to renewable gases, and qualifying hybrid systems, with aid proportionate to the renewable component. Incentives individually granted and communicated before 1 January 2025 can still be disbursed.

**Payer/budget evidence**

Outside an exception, the household is the payer. For the Polish legacy exception, FEnIKS was the identified payer with a PLN 70 million budget. No continuing Polish budget for new stand-alone fossil-boiler installations was identified.

**Counterevidence**

- This is not a legal ban on purchasing or operating every fossil-fuel boiler.
- Public procurement at market conditions and support unrelated to installation can fall outside Article 17(15).
- Hybrid heating and legacy EU-funded investments can remain eligible.
- Poland did fund a defined 2024 installation cohort after the general cutoff.

**Unknowns**

- The complete Polish legal implementation of Article 17(15), including tax treatment.
- Number and value of rejected or unfunded legacy claims.
- Contractor revenue lost specifically because public support ended.
- Whether equipment ordered before 2025 but not individually approved qualified for any exception.

---

## P-rules_finance_assets_transitions-05 — Battery EPR and passport handoffs create liabilities for storage installers that import, own-brand, or repurpose batteries

- `island_id`: `rules_finance_assets_transitions`
- `creator_id`: `shadow-scout-06`
- `evidence_ids`: `E-RFAT-05-A` through `E-RFAT-05-C`
- `query_ids`: `Q13–Q15`

**Actor/outcome**

A Polish solar-storage installer becomes a battery “producer” when it first professionally supplies batteries in Poland from another Member State or third country, sells them under its own name, or first markets repurposed batteries. Such a firm must register and finance extended producer responsibility. From 18 February 2027, industrial batteries over 2 kWh—including typical stationary storage batteries—must also carry a maintained electronic battery passport.

**Binding status and transition**

Regulation (EU) 2023/1542 is directly applicable. Chapter VIII on waste-battery management applied from 18 August 2025. It requires producer registration in every Member State where batteries are first marketed and prohibits producers from supplying batteries there unless registered. The passport obligation begins on 18 February 2027. Battery due-diligence policies were postponed by the 2025 amendment to 18 August 2027. [E-RFAT-05-A: consolidated Batteries Regulation](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX%3A02023R1542-20250731) [E-RFAT-05-B: Commission overview](https://environment.ec.europa.eu/news/new-law-more-sustainable-circular-and-safe-batteries-enters-force-2023-08-17_en)

**Loss, frequency, magnitude**

- Registration and EPR cost recurs by country and reporting period.
- Producer contributions must cover separate collection, transport, treatment, consumer information, data gathering, and regulatory reporting.
- An unregistered producer cannot lawfully make batteries available in that Member State.
- The passport obligation applies per covered battery and requires accurate, complete, current, interoperable records that remain available through later lifecycle states.
- When a battery is repurposed, remanufactured, or becomes waste, responsibility for the passport transfers to the specified downstream economic operator, producer-responsibility organisation, or waste manager.
- Polish contribution rates, registration expenditure, passport-system costs, and the number of local installers legally classified as producers were not established.

**Existing workaround**

A producer may appoint an authorised representative or producer-responsibility organisation where the regulation permits. The statutory cost-sharing provisions prevent the original producer from bearing duplicate EPR cost when a repurposed battery acquires a second producer.

**Payer/budget evidence**

The regulation expressly assigns financial contributions to the producer. Those contributions must cover collection, transport, treatment, information, and reporting costs. The economic operator placing the battery on the market is responsible for passport accuracy and upkeep, although it may authorise another operator to act for it. These are private compliance budgets; no general public reimbursement is specified. Poland’s existing battery framework also uses product-fee and BDO mechanisms. [E-RFAT-05-C: consolidated Polish Batteries Act, 11 June 2025](https://eli.gov.pl/api/acts/DU/2025/809/text/O/D20250809.pdf)

**Counterevidence**

- A downstream installer buying a battery already lawfully placed on the Polish market is generally a distributor, not automatically the EPR payer; it must verify registration and conformity.
- Battery due diligence does not apply below EUR 40 million net turnover unless the operator belongs to a group exceeding that threshold.
- The passport requirement is a February 2027 transition, not an already-operative obligation as of the research date.
- The regulation requires producer-responsibility organisations to avoid disproportionate burdens on small-volume producers and SMEs.

**Unknowns**

- Whether all necessary Polish administrative procedures and EU passport implementing acts are operational.
- Polish EPR contribution levels for stationary lithium storage.
- Number of installers importing directly rather than sourcing from a registered Polish producer.
- Treatment of multi-component storage systems where the battery and inverter enter the market through different entities.

---

## P-rules_finance_assets_transitions-06 — Rapidly rising renewable curtailment causes lost production and compensation gaps for pay-as-produced generators

- `island_id`: `rules_finance_assets_transitions`
- `creator_id`: `shadow-scout-06`
- `evidence_ids`: `E-RFAT-06-A` through `E-RFAT-06-D`
- `query_ids`: `Q16–Q18`

**Actor/outcome**

Polish PV and wind generators ordered to curtail by PSE or a distribution operator cannot sell the ungenerated electricity. The loss is particularly direct under metered, pay-as-produced PPAs because settlement follows actual meter output. Auction-supported generators also face a separate deadline to have curtailed energy counted toward their statutory sale obligation.

**Binding status and transition**

Non-market redispatch and the minimum compensation entitlement arise under Regulation (EU) 2019/943 and current Polish operational rules. A Polish government page proposes changing compensation calculations for pay-as-produced PPAs; that page is explicitly a bill proposal and does not prove enactment. [E-RFAT-06-A: URE 2024 redispatch report, published 27 October 2025](https://www.ure.gov.pl/pl/urzad/informacje-ogolne/aktualnosci/12923%2CRynek-energii-elektrycznej-sprawozdanie-Prezesa-URE-dotyczace-mechanizmow-redysp.html) [E-RFAT-06-B: government bill record](https://www.gov.pl/web/premier/projekt-ustawy-o-zmianie-ustawy--prawo-energetyczne2)

**Loss, frequency, magnitude**

- In 2024 PSE ordered 597.26 GWh of PV curtailment, 595.17 GWh for system balancing and 2.09 GWh for network constraints. This was 2,362% more than in 2023.
- Distribution operators curtailed another 24.12 GWh of PV output, up 647% year over year.
- PSE curtailed about 125.1 GWh of wind generation, up 199%.
- The government proposal states that pay-as-produced arrangements represent about 90% of PPAs and that current settlement can leave the generator bearing the full loss on unmetered, ungenerated electricity.
- The loss recurs per curtailment interval. Aggregate compensation paid and the residual uncompensated monetary loss were not published in the retrieved evidence.

**Existing workaround**

EU rules provide a minimum compensation entitlement. PSE operates a claims and calculation process. Auction-supported generators can count operator-determined curtailed energy toward their auction obligation, but they must notify the operator within 14 days; missing the deadline means the curtailed volume is not counted. [E-RFAT-06-C: URE auction notice, 6 June 2024](https://www.ure.gov.pl/pl/oze/aukcje-oze/komunikaty/13158%2CAukcje-OZE-Redysponowanie-nierynkowe-jak-zaliczyc-zredukowana-energie-do-realiza.html) [E-RFAT-06-D: PSE compensation-rule update](https://www.pse.pl/-/zmiana-zasad-wyliczania-rekompensaty-za-redysponowanie-nierynkowe-instalacji-oze)

**Payer/budget evidence**

The generator initially bears lost sale proceeds and PPA mismatch exposure. The ordering system operator is responsible for applicable compensation. No primary source retrieved disclosed PSE/OSD aggregate compensation expenditure, claim rejection rates, or outstanding liabilities.

**Counterevidence**

- URE describes non-market renewable curtailment as a last-resort action needed for system security.
- Most PSE PV curtailment in 2024 was caused by national balancing rather than a physical network bottleneck.
- Compensation rights already exist; the identified discontinuity concerns calculation and contractual fit, not the complete absence of compensation.
- Auction rules can protect curtailed generators from failing their volume commitment if the 14-day procedure is followed.
- The government’s pay-as-produced amendment remains proposal evidence unless separately enacted.

**Unknowns**

- Current legislative status and final wording of the proposed compensation amendment.
- Aggregate claims, payments, rejection rates, and time-to-payment by PSE and each OSD.
- Net uncompensated loss by PPA structure and support scheme.
- Curtailment frequency and concentration after the June 2025 balancing-market reform.
- Extent to which small PV assets or portfolios experience the same compensation process.

---

## Complete 18-query trace

Executed once each on 22 August 2026; no additional search queries were used.

1. `Q01` — `site:gov.pl prosument net-billing RCE ustawa 2024 depozyt prosumencki 30 procent`
2. `Q02` — `site:ure.gov.pl prosument net-billing ujemne ceny energii RCE 2024 2025`
3. `Q03` — `site:sejm.gov.pl ustawa 2024 OZE net-billing RCE prosument`
4. `Q04` — `site:gov.pl "Czyste Powietrze" wstrzymanie naboru 28 listopada 2024 wznowienie 31 marca 2025`
5. `Q05` — `site:nfosigw.gov.pl "Czyste Powietrze" budżet prefinansowanie operator 2025`
6. `Q06` — `site:nik.gov.pl "Czyste Powietrze" opóźnienia wypłat wykonawcy 2024 2025`
7. `Q07` — `site:eur-lex.europa.eu Regulation EU 2024/573 heat pumps placing on market bans Annex IV fluorinated greenhouse gases`
8. `Q08` — `site:climate.ec.europa.eu fluorinated greenhouse gases heat pumps certification technicians 2024 regulation FAQ`
9. `Q09` — `site:udt.gov.pl f-gazy pompy ciepła certyfikat personelu 2024 2025 statystyki`
10. `Q10` — `site:eur-lex.europa.eu Directive EU 2024/1275 Article 17 standalone fossil fuel boilers financial incentives 1 January 2025`
11. `Q11` — `site:energy.ec.europa.eu guidance phasing out financial incentives standalone boilers 2025 EPBD`
12. `Q12` — `site:czystepowietrze.gov.pl wznowienie naboru kotły gazowe budżet 70 mln 2025 beneficjenci`
13. `Q13` — `site:eur-lex.europa.eu Regulation EU 2023/1542 stationary battery energy storage obligations battery passport 2027 producer responsibility`
14. `Q14` — `site:environment.ec.europa.eu batteries regulation guidance battery passport due diligence 2025 2027`
15. `Q15` — `site:gov.pl BDO baterie akumulatory magazyny energii rejestr producent obowiązki 2025`
16. `Q16` — `site:pse.pl redukcja fotowoltaiki OZE nierynkowe redysponowanie 2024 2025 MWh`
17. `Q17` — `site:ure.gov.pl rekompensata nierynkowe redysponowanie OZE fotowoltaika 2024 2025`
18. `Q18` — `site:gov.pl ograniczenie generacji OZE fotowoltaika rekompensata redysponowanie ustawa 2024 2025`

