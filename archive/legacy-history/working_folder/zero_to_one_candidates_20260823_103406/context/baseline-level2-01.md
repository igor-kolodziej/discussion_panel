# Immutable Baseline Level-2 Research Packet

## Identity And Allocation

- Scope: `baseline-w01`
- Arm: `matched_baseline`
- Stage: `level2`
- Agent ID: `baseline-level2-01`
- Role: `level2_researcher`
- Model: `gpt-5.6-sol`
- Reasoning: `high`
- Required return path: `/Users/igor/Desktop/discussion_panel/working_folder/zero_to_one_candidates_20260823_103406/agent_returns/baseline-level2-01.json`
- Assigned/output IDs in exact order: `DIR-004, DIR-015, DIR-013, DIR-001, DIR-009, DIR-006, DIR-003, DIR-014, DIR-012, DIR-016, DIR-007, DIR-002`
- Per-candidate query cap: `12`; use exactly two calls per candidate and leave ten unused.
- Per-candidate caps: 10,000 uncached input tokens, 500 output tokens, 12 elapsed minutes.

Read no other file. For each candidate in exact assigned order, make exactly one individual web search call, then exactly one individual open call for one result from that search. Complete all 24 calls in candidate order; do not batch candidates into one call. Focus on payer denominator or budget proxy, closest substitute/route-around, realistic price/cost/capital sensitivity, first-customer route, critical dependencies, exact access/right claimed, and contradictory evidence. Public research only. Do not contact a person or chatbot, execute a private proof, buy anything, evaluate, validate, pivot, promote, regenerate, or create a confirmation artifact.

Keep the return exceptionally compact so exact provider output can remain inside the registered 500-token opportunity per candidate after deterministic partitioning. Each rendered dossier must contain 60–220 words including headings; target 85–120 words total. State unknowns honestly and do not use numeric merit ratings.

Return one JSON object using exactly these top-level keys: `agent_id`, `assigned_ids`, `output_ids`, `files_read`, `candidates`. Identity and ID arrays must exactly match this packet. `files_read` is exactly `["context/baseline-level2-01.md"]`. `candidates` contains one object per ID in the same order, with exactly:

```json
{
  "concept_id": "DIR-001",
  "search_text": "the exact search query used",
  "opened_url": "https://...",
  "source_title": "...",
  "source_date": "YYYY-MM-DD or concise published date or unknown",
  "proposition": "decision-relevant fact supported by the opened source",
  "status": "verified or interpreted or counsel-required or unknown or contradicted",
  "contradiction": "source limitation or counterevidence",
  "cheapest_resolving_test": "future hypothetical test only; do not execute it",
  "dossier": {
    "problem_and_payer_evidence": "...",
    "proposed_transaction": "...",
    "acquisition_route": "...",
    "decision_critical_unknowns": "...",
    "evidence_and_sources": "cite the evidence ID placeholder EV-B-L2-NNN and opened URL"
  }
}
```

Use `EV-B-L2-001` through `EV-B-L2-012` in assigned order. All strings must be nonempty. Add no other fields. Create the return using one file-creation patch and do not run a post-write command.

## Masked Equal-Field Cards

```json
[
  {
    "cheapest_falsification": "Interview five importers and five HVAC or refrigeration operators with screenshots of current workflows, then request one prepaid, narrowly scoped report, label, or portal remediation engagement.",
    "concept_id": "DIR-004",
    "current_workaround_and_persistence": "Likely workarounds include ERP exports, spreadsheets, consultants, packaging bureaus, customs brokers, and manual portal use. Annual deadlines, product changes, rule versions, and shipment exceptions can recur, although simplification or capable incumbents may limit persistence.",
    "decisive_assumptions_and_contradictions": [
      "A reachable segment has mandatory work but insufficient internal data operations and will buy a bounded draft or readiness service.",
      "The source establishes obligations but no evidence of inadequate incumbent tools or willingness to outsource.",
      "Annual reporting, label publishing, and shipment-linked portal remediation have distinct payers, paid units, owners, and channels."
    ],
    "explicit_unknowns": [
      "Reachable entity count, case frequency, current provider coverage, and willingness to pay.",
      "Exact authorization, security, and portal-access arrangements for a third-party operator.",
      "Whether rule simplification or incumbent packaging and customs tools remove enough pain to prevent repeat demand."
    ],
    "founder_constraint_tension": "Structured reconciliation and versioned rules fit the founder's data skills and can begin manually with controlled downside. Deadline spikes, portal exceptions, rule maintenance, and responsibility-sensitive outputs may require availability and domain counsel beyond a five-hour daily limit.",
    "initial_acquisition_route": "Use deadline and exception referrals from customs brokers and environmental advisers for reporting, packaging bureaus and distributors for labels, and freight forwarders or customs brokers for portal cases.",
    "possible_compounding_mechanism": "Accumulate ERP-to-report mappings, versioned label rules, portal states and rejection cases, and defect taxonomies by product category. Reuse must preserve customer confidentiality and never substitute generated values for source evidence.",
    "problem_payer_evidence": "Refrigerant and equipment economic operators may face rejected annual reports, relabelling, blocked registrations, or delayed shipments when regulated data and portal evidence are incomplete. The Commission source establishes changed F-gas formats, labels, certification, and portal controls, but not demand for external operations; payer candidates span regulatory affairs, finance, packaging, product compliance, and trade compliance.",
    "proposed_transaction_paid_event": "Sell one reporting-year reconciliation and draft, one product-family label generation and print validation, or one registration, renewal, or portal-remediation pack. The economic operator retains attestation, submission, and market-placement duties.",
    "sources": [
      "EV-B-DISC-002 \u2014 https://climate.ec.europa.eu/news-other-reads/news/f-gases-new-rules-labelling-reporting-certification-and-the-f-gas-portal-2024-09-20_en"
    ]
  },
  {
    "cheapest_falsification": "Interview ten Polish SME finance owners with overdue invoices and request one real paid manual case; test buyer diligence, licensed funding, and procurement variants only with separate named transactions and explicit fee terms.",
    "concept_id": "DIR-015",
    "current_workaround_and_persistence": "Likely workarounds include accountants, internal finance teams, collections, credit reports, invoice-finance brokers, bookkeepers, and conventional procurement. Repeated invoices and buyer processes may sustain demand, while substantive disputes, established finance products, country variation, or low transaction values may prevent viable margins.",
    "decisive_assumptions_and_contradictions": [
      "A material share of payment loss is operationally correctable and customers will pay at submission, resolution, diligence, funding, or sourcing triggers.",
      "The source supports late-payment prevalence but not Polish willingness to pay, segment economics, or causation by documentation defects.",
      "The five variants alternate payer and owner and span evidence services, intelligence, regulated financing, and buyer procurement, so they cannot share one assumed business model."
    ],
    "explicit_unknowns": [
      "Polish segment-specific delay causes, case values, correction rates, and willingness to pay.",
      "Availability and economics of licensed funding partners, fraud controls, and verified invoice acceptance.",
      "Whether buyer reports and prompt-pay sourcing achieve sufficient trust, repeat volume, and lawful data access."
    ],
    "founder_constraint_tension": "Manual document reconciliation and structured data fit the founder's skills and can begin with low capital through accountant channels. Healthcare data, success-fee collection, financing regulation, fraud controls, and marketplace liquidity add time, liability, and working-capital complexity.",
    "initial_acquisition_route": "Use construction or medical accountants for claim and exception cases, search and export or finance advisers for buyer reports, bookkeeping practices for funding referrals, and focused direct outreach or chambers for buyer-side prompt-pay sourcing.",
    "possible_compounding_mechanism": "Build payer rejection and acceptance patterns, buyer workflow intelligence, verified supplier experiences, invoice performance, and supplier-buyer behavior graphs. Data must be permissioned, verifiable, non-defamatory, and protected against duplicate assignment or hidden conflicts.",
    "problem_payer_evidence": "Contractors, healthcare providers, and small suppliers may face rejected claims, payment friction, delayed receivables, or expensive working capital. The Commission source establishes widespread late payment and collection burden, but payment performance varies by country and it does not prove Polish demand for any of the proposed interventions.",
    "proposed_transaction_paid_event": "Charge for assembling one milestone claim, resolving one rejected healthcare invoice batch, selling one prospective-buyer report, closing funding on one accepted invoice through a licensed partner, or completing a buyer-funded prompt-pay sourcing sprint. The relevant buyer, payer, provider, supplier, or licensed funder retains approval and regulated authority.",
    "sources": [
      "EV-B-DISC-009 \u2014 https://single-market-economy.ec.europa.eu/smes/challenges-and-resilience/late-payment/eu-payment-observatory/observatory-analysis_en?prefLang=lt"
    ]
  },
  {
    "cheapest_falsification": "Show distinct offers to three industrial heat users and three renewable developers, and seek a conditional letter of intent tied to a named project, buyer cohort, or site before committing option capital.",
    "concept_id": "DIR-013",
    "current_workaround_and_persistence": "Current work likely sits with energy auditors, equipment vendors, brokers, banks, developers, land agents, and internal teams. Fragmented evidence and small transaction sizes may persist, while program simplification, weak project economics, grid uncertainty, or established originators may remove the fee pool.",
    "decisive_assumptions_and_contradictions": [
      "Evidence assembly or aggregation, rather than underlying technical or economic infeasibility, is the binding cause of enough failed projects.",
      "The source combines active and proposed mechanisms and emphasizes simplification, so future intermediary demand is uncertain.",
      "Factory finance packaging, multi-party PPA origination, and optioned site-rights assignment differ in payer, capital risk, legal structure, and transaction owner."
    ],
    "explicit_unknowns": [
      "Pipeline size, transaction duration, close probability, fee tolerance, and partner economics.",
      "Whether guarantee channels accept aggregation and whether public data can screen fatal grid constraints.",
      "Land-option terms, assignability, permitting risk, and capital loss rate."
    ],
    "founder_constraint_tension": "The family renewable network is a credible regional sourcing advantage and evidence packaging matches data skills. Long cycles, multi-party negotiation, regulated boundaries, and especially land-option capital can exceed the founder's time and preferred downside despite available savings.",
    "initial_acquisition_route": "Source heat projects through equipment-service partners, buyers through energy-cost reviews and broker or bank channels, and land through a regional renewable-installer and landowner network focused on one grid area.",
    "possible_compounding_mechanism": "Build process-heat baselines, vendor and award data, buyer load and credit-readiness maps, deal-failure patterns, and parcel-level grid, permit, landowner, and developer-demand intelligence. Keep client funds and regulated credit activities outside the service unless separately authorized.",
    "problem_payer_evidence": "Factories and renewable developers may lose viable projects because finance evidence, buyer aggregation, grid screening, land rights, and counterparties are costly to assemble individually. The Commission source reports industrial decarbonization mechanisms, but some measures were proposed and it does not establish demand for these origination services.",
    "proposed_transaction_paid_event": "Charge for a metered process-heat feasibility packet plus a larger fee at financing close, an origination milestone when an aggregated buyer cohort signs a bankable PPA term sheet, or an assignment fee when a developer accepts an optioned site after a defined diligence review.",
    "sources": [
      "EV-B-DISC-007 \u2014 https://commission.europa.eu/document/download/ae2ea9ea-d037-4920-bbf6-a4183b747e34_en?filename=COM_2025_378_1_EN_ACT_part1_v5.pdf"
    ]
  },
  {
    "cheapest_falsification": "Show a one-page control prototype to ten EU platform, clinic, and agency operations leads, ask each to map one live workflow and accountable party, and request a prepaid fixed-scope pilot without claiming certification.",
    "concept_id": "DIR-001",
    "current_workaround_and_persistence": "Likely workarounds are manual labels, ad hoc legal or compliance review, vendor-specific checks, and last-minute campaign remediation. Their prevalence and inadequacy are not established, but changing formats, multilingual interfaces, recurring releases, and fragmented workflow ownership could make the problem persistent.",
    "decisive_assumptions_and_contradictions": [
      "Covered customers need controls beyond visible labels or existing platform tooling and will pay to outsource a bounded part of the workflow.",
      "The source establishes obligations but not that every proposed use case is covered; applicability, exemptions, and allocation of duties require case-specific verification.",
      "Platform integration, clinic monitoring, and campaign clearance have different payers, triggers, owners, and routes and must not be treated as one proven transaction."
    ],
    "explicit_unknowns": [
      "Which configurations are legally in scope and which party bears each duty.",
      "Current tool adequacy, purchase urgency, acceptable price, and procurement cycle by customer segment.",
      "Whether machine-readable metadata survives customers' actual downstream transformations."
    ],
    "founder_constraint_tension": "A manual, fixed-scope pilot can fit part-time work and the founder's AI fluency, while partner channels reduce public-facing distribution. Continuous clinic monitoring, broad legal coverage, or urgent campaign work could exceed five focused hours daily and require specialist legal review.",
    "initial_acquisition_route": "Use targeted outreach around imminent EU releases, with referrals from digital-asset-management integrators, medical-software implementers, and production studios. The three channels should remain distinct because their buyers and transaction owners differ.",
    "possible_compounding_mechanism": "Accumulate permissioned cross-format compatibility results, multilingual disclosure test cases, campaign precedents, and observed release failure modes. Repeated cases could improve checklists and automation without implying regulator approval or tamper-proof provenance.",
    "problem_payer_evidence": "EU-facing AI-content platforms, clinics, agencies, and brands may incur rework, launch delay, complaints, or enforcement exposure when generated or interactive content lacks required marking or disclosure. The cited Commission source establishes new transparency requirements and enforcement timing, but not outsourcing demand; plausible payers are platform compliance, clinic digital operations, and agency or brand production budgets.",
    "proposed_transaction_paid_event": "Sell a bounded release-control engagement: integration and validation for one production content type, a baseline scan of one live clinic chatbot, or a fixed-fee clearance pack for one imminent synthetic-media campaign. The responsible provider, deployer, agency, or brand retains classification and release authority.",
    "sources": [
      "EV-B-DISC-001 \u2014 https://digital-strategy.ec.europa.eu/en/news/commission-starts-enforcing-ai-act-rules-and-new-transparency-requirements-2-august"
    ]
  },
  {
    "cheapest_falsification": "Show a one-page mock deliverable to five Polish payroll or employment-law partners, then seek one paid payroll mapping, ATS configuration, or live-request case while counsel verifies applicable Polish law.",
    "concept_id": "DIR-009",
    "current_workaround_and_persistence": "Likely workarounds include spreadsheets, payroll and HRIS reports, recruiter approvals, email, and outside counsel. National implementation, recurring hiring and requests, fragmented systems, and weak job descriptions may sustain demand, but incumbent HR, payroll, ATS, or law-firm tooling may absorb it.",
    "decisive_assumptions_and_contradictions": [
      "Manual coordination is sufficiently costly that employers or agencies will pay for fixed-scope operational help before buying software.",
      "National transposition, enforcement, reporting schedules, and edge cases may differ, and the source does not require any intermediary.",
      "Cohort analysis, vacancy release gating, and employee-request handling have distinct owners, triggers, channels, and privacy risks despite common employer authority."
    ],
    "explicit_unknowns": [
      "Applicable Polish duties, deadlines, thresholds, and lawful data-processing design.",
      "Employer request frequency, current workflow cost, partner appetite, and willingness to pay.",
      "Whether heterogeneous HR data supports useful, contestable outputs without excessive manual work."
    ],
    "founder_constraint_tension": "Data modeling and privacy-preserving workflows fit the founder's skills, while white-label partners reduce direct audience building. Sensitive payroll data, legal-review dependency, custom integrations, and case deadlines could create heavy trust and availability requirements.",
    "initial_acquisition_route": "Deliver white-label through payroll bureaus and employment-law partners for cohort work, ATS consultants and recruitment outsourcers for range gating, and privacy or employment counsel for live information requests.",
    "possible_compounding_mechanism": "Develop a versioned job-equivalence ontology, cross-ATS mappings, non-identifying exception patterns, privacy-preserving request schemas, aggregation checks, and decision logs, without pooling identifiable salary records.",
    "problem_payer_evidence": "Employers and recruitment operations may face disputes, rework, privacy failures, or delays when job cohorts, vacancy salary ranges, or employee pay-information responses are not reproducible. The Commission source establishes new pay-transparency duties and remedies but not demand for an intermediary; potential payers include HR, compensation, legal, talent, recruitment, and privacy operations.",
    "proposed_transaction_paid_event": "Charge for mapping one payroll export into a counsel-reviewable cohort report, configuring one ATS range-control workflow, or handling one live employee request through an approved response packet. The employer retains classification, disclosure, remediation, and legal authority.",
    "sources": [
      "EV-B-DISC-005 \u2014 https://commission.europa.eu/news-and-media/news/new-eu-rules-pay-transparency-explained-2026-06-05_en"
    ]
  },
  {
    "cheapest_falsification": "Ask five importers, five installers, and five hospital procurement or engineering leads to apply a mock gap review to a live SKU, questionnaire, or tender, then request one prepaid bounded engagement.",
    "concept_id": "DIR-006",
    "current_workaround_and_persistence": "Likely workarounds are manufacturer emails, spreadsheets, testing-lab files, tender questionnaires, security reviews, and procurement appendices. Vulnerability updates, support periods, repeated buyer questions, and new tenders may recur, but incumbent labs, consultants, or hospital teams may already perform sufficient review.",
    "decisive_assumptions_and_contradictions": [
      "Evidence gaps recur often enough and create enough commercial or operational loss to fund a per-event service.",
      "Official sources establish obligations and reporting infrastructure but not that importers, installers, or hospitals need this intermediary.",
      "The regulated importer, bidding installer, and hospital loss bearer have different authority, triggers, routes, budgets, and liability boundaries."
    ],
    "explicit_unknowns": [
      "Final product-specific duties, overlap with medical-device rules, and evidence accepted by each buyer.",
      "Per-SKU, questionnaire, and tender frequency, budget, and procurement duration.",
      "Whether manufacturers provide verifiable evidence and whether laboratories or advisers will refer cases."
    ],
    "founder_constraint_tension": "Evidence normalization fits the founder's data skills and partner referrals can reduce sales overhead. Hospital procurement, device safety, confidential vulnerability evidence, and continuous lifecycle maintenance raise expertise, cycle-time, and liability burdens for a part-time founder.",
    "initial_acquisition_route": "Use testing laboratories and customs advisers for blocked SKUs, wholesalers and tender advisers for installer questionnaires, and medical-procurement or hospital cyber advisers for pending device tenders.",
    "possible_compounding_mechanism": "Develop permissioned device evidence templates, supplier-response benchmarks, normalized buyer-control graphs, vendor support contacts, and non-confidential response-quality histories, with strict separation of vulnerability details and client-confidential questionnaires.",
    "problem_payer_evidence": "Importers, installers, and hospitals may lose market access, tenders, or operational support when connected-product or supplier cyber evidence is incomplete. One source describes expanding Polish and EU cyber obligations; the CRA source establishes manufacturer reporting deadlines, but neither proves that these three buyers will fund adjacent evidence gates.",
    "proposed_transaction_paid_event": "Charge for one per-SKU evidence-gap review and supplier request pack, conversion of one live buyer questionnaire into a reusable passport, or review of one pending hospital device tender. Importers, buyers, hospitals, and manufacturers retain their respective compliance, procurement, clinical, and filing authority.",
    "sources": [
      "EV-B-DISC-003 \u2014 https://www.gov.pl/attachment/0ea50e48-bad1-4686-8406-810c8af60f0d",
      "EV-B-DISC-006 \u2014 https://digital-strategy.ec.europa.eu/en/policies/cra-reporting"
    ]
  },
  {
    "cheapest_falsification": "Interview five Polish contractors and five refrigerant or equipment firms using their current roster and training workflow, then seek one prepaid roster cleanup or cohort diagnostic linked to a live tender or season.",
    "concept_id": "DIR-003",
    "current_workaround_and_persistence": "Contractors likely use certificates, spreadsheets, dispatcher memory, wholesaler guidance, and existing vocational courses. Renewals, changing refrigerants, staff turnover, and job-specific scope may sustain repeated work, but the packet does not show that current systems are inadequate.",
    "decisive_assumptions_and_contradictions": [
      "Expanded certificate categories create operational friction and employers will pay at a tender, dispatch, or booked-job trigger.",
      "The official source shows rule changes but no evidence that affected firms lack adequate tools, training, or verification services.",
      "Dispatch eligibility infrastructure and credential-adjacent training differ in paid unit, owner, authority, and delivery burden."
    ],
    "explicit_unknowns": [
      "Member-state credential pathways, verification access, and exact job-scope rules.",
      "Frequency of misdispatch, failed tenders, and employer-funded conversion demand.",
      "Price, seasonality, and willingness of certification or school partners to distribute the service."
    ],
    "founder_constraint_tension": "The family renewable-installation network offers a low-cost regional route and a manual data pilot is compatible with part-time work. Practical training requires qualified partners, physical delivery, scheduling, and potentially more operational intensity than a software-led verification product.",
    "initial_acquisition_route": "Pilot with a regional installation firm, then use equipment wholesalers, trade associations, installer networks, vocational schools, and recognized certification partners. Keep verification and training offers separately framed.",
    "possible_compounding_mechanism": "Develop a credential-scope ontology, multilingual diagnostics, practical error patterns, and employer demand data by equipment and refrigerant category, while relying on authoritative issuers for credential validity.",
    "problem_payer_evidence": "HVAC and refrigeration employers can lose dispatches, jobs, or tenders when technician certificate scope or practical skills do not match the refrigerant and equipment involved. The Commission source establishes expanded certification scope for alternatives, but not a gap in incumbent verification or training; likely payers are contractor service operations and employer training budgets.",
    "proposed_transaction_paid_event": "Charge for importing and verifying one technician roster before dispatch, tender, or season, or for an employer-paid cohort diagnostic and preparation module tied to one recognized certificate pathway. Certification bodies retain issuance authority and employers retain job-eligibility decisions.",
    "sources": [
      "EV-B-DISC-002 \u2014 https://climate.ec.europa.eu/news-other-reads/news/f-gases-new-rules-labelling-reporting-certification-and-the-f-gas-portal-2024-09-20_en"
    ]
  },
  {
    "cheapest_falsification": "With one consenting owner in each target category, request exports from three brands and attempt one manual decision-grade report before building connectors or promising a remedy.",
    "concept_id": "DIR-014",
    "current_workaround_and_persistence": "Likely workarounds include OEM portals, manual exports, incumbent service contracts, agronomist spreadsheets, energy audits, workshop diagnostics, and bilateral warranty disputes. Recurring maintenance and claims may persist, but fragmented interfaces, trade-secret or privacy limits, and poor signal quality may keep the data unusable.",
    "decisive_assumptions_and_contradictions": [
      "Accessible raw data contains decision-grade signals and counterparties accept a neutral output sufficiently often to pay.",
      "Legal access rights do not guarantee standardized interfaces, complete history, low integration cost, or useful signal quality.",
      "Maintenance auctions, farmer-controlled benchmarks, installer certificates, and fleet claims have different payers, owners, success metrics, and regulated boundaries."
    ],
    "explicit_unknowns": [
      "Export availability, data completeness, cross-brand comparability, and integration cost.",
      "Willingness of factories, farms, installers, fleets, warrantors, and repairers to pay or accept the evidence.",
      "How to measure savings, benchmark privacy, performance attribution, and responsibility without taking unauthorized insurance or adjudication roles."
    ],
    "founder_constraint_tension": "The founder's data skills and family installer access support manual export analysis with limited upfront capital. Four unrelated verticals, field validation, partner acceptance, potentially urgent downtime cases, and warranty or insurance boundaries strain part-time focus.",
    "initial_acquisition_route": "Start manually with one machine family and maintenance partner, one crop-and-machine cohort through an agronomist, one heat-pump brand through a renewable installer, or one fleet and fault class through brokers and an independent diagnostic specialist.",
    "possible_compounding_mechanism": "Accumulate consented cross-brand signal mappings, field and weather-normalized benchmarks, commissioning and remedy records, and fault-to-repair responsibility histories. Governance must preserve owner authorization and avoid employee, driver, farm, or household re-identification.",
    "problem_payer_evidence": "Factories, farms, building owners, installers, fleets, and leasing firms may be unable to turn connected-asset data into competitive maintenance, peer benchmarks, performance remedies, or warranty responsibility. The Data Act source establishes user access and sharing rights and names relevant use cases, but not standardized access, signal quality, or purchasing demand.",
    "proposed_transaction_paid_event": "Charge on a maintenance job with contractually verified savings, a farm's season-specific benchmark report, an installer's post-commissioning performance certificate, or a fleet case with an accepted responsibility decision or competitively routed repair order. Asset owners authorize data use and relevant repair, warranty, or insurance parties retain liability decisions.",
    "sources": [
      "EV-B-DISC-008 \u2014 https://digital-strategy.ec.europa.eu/en/news/eu-data-act-gives-users-control-over-data-connected-devices"
    ]
  },
  {
    "cheapest_falsification": "Present separate one-page offers to three scrap sellers or foundries and three metal fabricators, then request a conditional paid mandate tied to one actual lot or live tender.",
    "concept_id": "DIR-012",
    "current_workaround_and_persistence": "Likely workarounds include seller declarations, buyer-side testing, discounted pricing, repeated hauling, email document collection, distributor support, and tender consultants. Variable lots and repeated tenders may sustain the need, while direct buyer-supplier relationships or simpler rules may eliminate an intermediary.",
    "decisive_assumptions_and_contradictions": [
      "Independent evidence changes lot acceptance, price, or tender completion enough to create a fee pool.",
      "The Commission communication includes proposed or consultative measures and simplification that could reduce compliance-heavy intermediation.",
      "Seller-paid physical settlement and fabricator-paid procurement acceptance have different owners, risk allocation, routes, and operational demands."
    ],
    "explicit_unknowns": [
      "Lot rejection and tender-loss frequency, price impact, and willingness to pay.",
      "Representative sampling feasibility, assay partner terms, waste-rule constraints, and regional transaction density.",
      "Whether buyer acceptance can be defined objectively and upstream suppliers will release verifiable documents."
    ],
    "founder_constraint_tension": "Manual tender normalization fits analytical, part-time work and controlled capital. A physical exchange requires local density, sampling logistics, settlement operations, and partner quality control, making it more operational and capital-sensitive than the evidence-packet variant.",
    "initial_acquisition_route": "For physical settlement, start with one mobile assay partner and scrapyards in a single foundry catchment. For tender evidence, manually serve one live exporter tender through metal distributors, advisers, or industry associations.",
    "possible_compounding_mechanism": "Accumulate permissioned material-origin, assay, contamination, accepted-price, supplier-document, expiry, mapping, and procurement-objection records. Physical-lot and tender datasets should remain distinguishable because their verification and transaction logic differ.",
    "problem_payer_evidence": "Scrap sellers, foundries, and metal fabricators may lose price, logistics time, or tenders when composition, origin, recycled content, emissions, or supporting documents are not trusted by the accepting buyer. The Commission source describes metal sustainability requirements and scrap monitoring but not demand for an assay exchange or evidence utility.",
    "proposed_transaction_paid_event": "Take a disclosed closing fee when a foundry accepts and settles an independently assayed scrap lot, or charge a bidding fabricator when its buyer accepts a supplier-backed tender evidence packet as complete. Laboratories and document issuers retain responsibility for source accuracy.",
    "sources": [
      "EV-B-DISC-007 \u2014 https://commission.europa.eu/document/download/ae2ea9ea-d037-4920-bbf6-a4183b747e34_en?filename=COM_2025_378_1_EN_ACT_part1_v5.pdf"
    ]
  },
  {
    "cheapest_falsification": "Offer manual document and registry verification on twenty live quotes through two installers, while separately asking an importer, housing operator, or lender to pay for one readiness, record, or baseline case before building software.",
    "concept_id": "DIR-016",
    "current_workaround_and_persistence": "Likely workarounds include installer advice, public registries, customs brokers, laboratories, wholesaler records, paper commissioning files, manufacturer portals, and ad hoc energy monitoring. Repeated model changes, installations, service events, and disputes may persist, but formal defects may be easily remediated and existing parties may already provide enough evidence.",
    "decisive_assumptions_and_contradictions": [
      "Each payer experiences enough avoidable loss to fund verification, evidence continuity, or bounded measurement before or after installation.",
      "The source documents mainly formal defects and explicitly does not establish deficient real-world safety or efficiency.",
      "Consumer quote review, importer compliance, portable records, and measurement-backed remedies differ in payer, trigger, owner, route, legal duty, and technical burden."
    ],
    "explicit_unknowns": [
      "Household, importer, installer, lender, and cooperative willingness to pay by transaction.",
      "Registry completeness, record recognition by warrantors, sensor sufficiency, and attribution accuracy.",
      "Whether formal-document problems recur after remediation and whether bounded remedies avoid insurance regulation."
    ],
    "founder_constraint_tension": "The family renewable firm offers a practical regional pilot channel, and document or telemetry analysis fits the founder's skills with moderate initial cost. Consumer support, onsite measurement, long monitoring periods, warranty disputes, and possible insurance boundaries may create ongoing service obligations incompatible with part-time work.",
    "initial_acquisition_route": "Use search and independent consumer advisers for quote review, customs brokers and labs for importer readiness, wholesalers and financing partners for installation records, and regional installer pilots with recent customers for performance baselines.",
    "possible_compounding_mechanism": "Build versioned model-document and requirement graphs, quote and shipment defect taxonomies, permissioned commissioning and service histories, and weather-normalized performance curves. Stored records must remain immutable and performance outputs must express attribution limits.",
    "problem_payer_evidence": "Homeowners, heat-pump importers, installers, lenders, and housing cooperatives may face bad purchase decisions, blocked shipments, missing warranty evidence, or disputed performance attribution. Polish authorities found documentation, labeling, and declaration problems in most inspected non-EU models, but the inspection was mainly formal and does not establish poor real-world safety or efficiency.",
    "proposed_transaction_paid_event": "Charge for a report on one live homeowner quote, one-model shipment-readiness review, activation of one portable installation record, or a post-installation weather-adjusted baseline study. Homeowners, importers, warranty providers, installers, lenders, and any licensed insurer retain their purchase, market-placement, claim, remedy, and underwriting decisions.",
    "sources": [
      "EV-B-DISC-010 \u2014 https://uokik.gov.pl/public/index.php/pompy-ciepla-wspolne-dzialania-uokik-ih-i-kas"
    ]
  },
  {
    "cheapest_falsification": "Interview ten municipal social-care directors and five providers using the audit findings, then seek two paid eight-week pilots with predefined administrative-hours, documentation, referral, or missed-visit outcomes.",
    "concept_id": "DIR-007",
    "current_workaround_and_persistence": "Likely workarounds include municipal case systems, paper or spreadsheet visit logs, phone calls, existing assistance registers, and informal referrals. Aging and fragmented local services may sustain the gap, but some failures may primarily require staffing, funding, or policy rather than software or a registry.",
    "decisive_assumptions_and_contradictions": [
      "Local leaders have both authority and operational capacity to act on better records or newly discovered needs.",
      "The audit covered only 19 municipalities, and national prevalence, procurement urgency, and sustainable budgets remain uncertain.",
      "Delivery-proof software and consent-based inter-institution discovery have different purposes, permissions, owners, and funding models."
    ],
    "explicit_unknowns": [
      "Local legal basis, consent design, procurement route, and budget.",
      "Whether field workers can use the workflow without reducing care time.",
      "Whether municipalities can serve additional residents identified through the discovery network."
    ],
    "founder_constraint_tension": "A bounded regional pilot and structured data work fit the founder's analytical skills and avoid public audience building. Municipal procurement, sensitive resident data, local partnership coordination, and the obligation to respond to uncovered needs may exceed part-time capacity.",
    "initial_acquisition_route": "Use municipal associations and public-sector software resellers for service-delivery proof, or secure one anchor municipality and permissioned local partners such as pharmacies, housing organizations, clinics, and senior NGOs for discovery.",
    "possible_compounding_mechanism": "Accumulate privacy-preserving service-exception and documentation taxonomies, consented referral protocols, and locality-level service-capacity maps. Avoid treating digital check-ins as proof of care quality or identifiable resident data as a commercial asset.",
    "problem_payer_evidence": "Municipalities and care providers may be unable to prove assigned home-care delivery or discover isolated seniors before crises. The NIK source reports weak identification, imprecise records, and missing quality monitoring in an audit of 19 municipalities, supporting the problem but not national prevalence or purchase urgency; payers could be municipalities, contracted providers, or grant-funded consortia.",
    "proposed_transaction_paid_event": "Sell an eight-week pilot for one care team with missed-visit and documentation measures, or a neighborhood referral-and-assessment pilot using transparent consent and human follow-up. Municipal and provider leaders retain service decisions, and residents or lawful representatives retain applicable permissions.",
    "sources": [
      "EV-B-DISC-004 \u2014 https://www.nik.gov.pl/aktualnosci/sprawy-spoleczne/gminy-nie-sa-gotowe-na-starzenie-sie-spoleczenstwa-nik-wskazuje-luki-w-opiece-nad-seniorami.html"
    ]
  },
  {
    "cheapest_falsification": "Run five structured interviews in each transaction field using a mock evidence vault or responsibility schedule, then ask for a paid setup tied to one live complaint channel or stalled procurement.",
    "concept_id": "DIR-002",
    "current_workaround_and_persistence": "Likely workarounds combine support tickets, observability logs, spreadsheets, email, security questionnaires, and counsel-authored clauses. Fragmentation may recur across model versions, complaints, and deals, but the packet does not establish that existing observability or procurement products fail often enough to support a separate purchase.",
    "decisive_assumptions_and_contradictions": [
      "Customers can lawfully retain the minimum evidence needed and see enough cost in fragmented reconstruction or negotiation to pay.",
      "An official or incumbent workflow may already cover much of the need, and the cited source does not establish outsourcing demand.",
      "Post-complaint vendor operations and two-sided pre-procurement negotiation have different owners, timing, and incentives and remain separate transaction hypotheses."
    ],
    "explicit_unknowns": [
      "Frequency and cost of failed complaint reconstruction and stalled transparency negotiations.",
      "Minimum lawful evidence set, retention period, and acceptable security architecture.",
      "Whether either side will pay a neutral intermediary and at what trigger or price."
    ],
    "founder_constraint_tension": "The founder's AI and data background suits schema design and manual pilots, and partner-led acquisition avoids constant networking. Sensitive records, two-sided coordination, legal boundaries, and potentially urgent complaint handling create privacy and time-load tension for a part-time operator.",
    "initial_acquisition_route": "Reach AI operations teams through technical content and observability partners for post-complaint evidence, and use governance consultants or vendor security-review teams to find stalled procurements for pre-deployment duty allocation.",
    "possible_compounding_mechanism": "Build normalized incident taxonomies and model-evidence schemas, plus anonymized clause-to-control and evidence-handoff mappings. The asset depends on lawful retention, permissioned reuse, and strict separation of confidential buyer and vendor information.",
    "problem_payer_evidence": "Downstream AI vendors may be unable to reconstruct model, prompt, disclosure, output, and response evidence after a complaint, while enterprise AI procurements may stall when transparency duties and evidence handoffs are unassigned. The Commission source supports the surrounding transparency obligations but does not prove these workflow failures or budgets; potential payers are SaaS trust, risk, legal, vendor-sales, or enterprise procurement operations.",
    "proposed_transaction_paid_event": "Charge for setup of one complaint channel and one model-backed product, or for one active procurement workspace that ends with an agreed responsibility schedule. The contracting parties retain legal approval, and the vendor or deployer retains responsibility for its own evidence and decisions.",
    "sources": [
      "EV-B-DISC-001 \u2014 https://digital-strategy.ec.europa.eu/en/news/commission-starts-enforcing-ai-act-rules-and-new-transparency-requirements-2-august"
    ]
  }
]
```
