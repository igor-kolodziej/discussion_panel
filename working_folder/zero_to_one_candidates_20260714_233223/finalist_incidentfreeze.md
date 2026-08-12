# Zero-to-One Candidate: IncidentFreeze

## One-Sentence Thesis

Build the telemetry-preservation and reconstruction layer that automatically freezes the physiological signals, device state, software versions, and audit evidence needed when a connected medical wearable receives a potentially reportable complaint.

## Founder Fit

The founder’s biosignal, data-science, anomaly-analysis, and automation skills fit physiological telemetry reconstruction, timestamp alignment, device-state lineage, and structured evidence packaging.

The founder does not decide clinical causality, complaint reportability, root cause, corrective action, or regulatory submissions. Those responsibilities remain with the manufacturer’s quality, medical, safety, and regulatory personnel. A senior medical-device QA/RA contractor defines the initial scope and reviews delivery.

The initial product can be demonstrated using founder-owned devices, simulated complaints, synthetic telemetry, and customer-provided sandbox exports without clinical access or a finished regulated product.

## Customer, Pain, and Current Workaround

The beachhead customer is a 20–250-person European manufacturer of a CE-marked connected medical wearable with:

- physiological sensors;
- a mobile application or cloud platform;
- firmware or algorithm releases;
- a small quality/post-market team;
- no dedicated telemetry-forensics function.

Its inside view is: “A complaint has arrived and the reporting clock may already be running. The QMS has the case, but the raw signal window, app logs, device configuration, firmware version, algorithm version, calibration state, connectivity history, and user annotations are distributed across systems with different retention periods.”

The painful event is a potential serious incident, recurring complaint, field safety investigation, or trend signal where delayed evidence assembly creates:

- incomplete investigation;
- avoidable regulatory uncertainty;
- inability to reproduce the device output;
- repeated engineering effort;
- disagreement between quality, software, and clinical teams;
- loss of ephemeral telemetry before preservation.

Current workarounds include manual tickets, engineering log searches, screenshots, cloud queries, support-system exports, spreadsheets, and generic QMS complaint records. QMS platforms coordinate complaint workflow, but the decision-critical hypothesis is that smaller connected-device manufacturers lack an installed, biosignal-aware evidence freeze across their device, app, cloud, and algorithm stack.

## Product Wedge

The first paid product is an **Incident Freeze Rehearsal and Standby Pack**:

- map one product’s complaint-to-telemetry path;
- define the minimum evidence manifest;
- install a read-only snapshot/export component in a sandbox or staging environment;
- simulate a complaint and evidence-preservation trigger;
- freeze a bounded event window with hashes and timestamps;
- record device, firmware, app, SDK, algorithm, configuration, and calibration versions;
- reconstruct the displayed or transmitted output from preserved evidence;
- generate a QMS-ready evidence index;
- add a signed SOP annex routing covered complaint preservation through IncidentFreeze;
- provide 12 months of prepaid standby for the covered product.

The product preserves evidence. It does not determine reportability, diagnose a patient, submit a vigilance report, or replace the manufacturer’s QMS.

## Commercial Insight or Market Gap

**Evidence:** MDR vigilance obligations can require rapid reporting, manufacturers must investigate incidents and trends, and established QMS/PMS vendors already sell complaint routing, CAPA, reporting, and post-market workflows.

**Hypothesis:** The unowned gap is the first technical hour after complaint awareness, when volatile physiological and software evidence must be frozen before legal or clinical interpretation begins.

The commercially valuable control point is not a complaint dashboard. It is an installed preservation step in the manufacturer’s SOP, backed by product-specific telemetry mappings and an external reconstruction environment.

## Underused Momentum

- MDR vigilance and trend-reporting duties create time-sensitive investigation events.
- Connected medical wearables increasingly depend on device firmware, mobile apps, cloud services, and algorithm versions.
- EUDAMED increases the visibility and structure of device, actor, vigilance, and market-surveillance workflows.
- QMS platforms have made complaint workflows more structured, creating a practical integration point for a specialized evidence-preservation layer.
- Cloud logs and raw telemetry often have operational retention periods far shorter than product-lifecycle or regulatory evidence needs.

The last point is a customer-specific hypothesis requiring verification during the first paid rehearsal.

## Beachhead Market

European connected medical-wearable OEMs with:

- one to five marketed product families;
- physiological raw or near-raw data in a controlled device, app, or cloud environment;
- at least two firmware, application, or algorithm releases per year;
- an internal quality lead but limited telemetry-forensics capacity;
- authority to amend their complaint-preservation SOP;
- no requirement that IncidentFreeze make regulatory or medical decisions.

Initial modalities include ambulatory ECG, seizure monitoring, respiratory monitoring, connected sleep devices, fall-detection wearables, and medical-grade movement monitoring.

Exclude implantables, life-support systems, customers unable to provide a sandbox, and products where evidence access requires an unspecified third-party platform agreement.

## Business Model and Unit Economics

All prices, costs, response volumes, and margins are hypotheses.

| Offer | Price | Direct cost | Hypothesized contribution |
|---|---:|---:|---:|
| Initial rehearsal and 12-month standby | 30,000–45,000 PLN | 14,000–22,000 PLN | 35–60% |
| Mature product activation | 40,000–65,000 PLN | 15,000–25,000 PLN | 45–70% |
| Annual product-line retainer | 100,000–150,000 PLN | 25,000–45,000 PLN | 60–80% |
| Standard covered incident package | 40,000–75,000 PLN | 15,000–30,000 PLN | 50–75% |
| Complex reconstruction | Separate approved scope | Scope-dependent | Minimum 50% target |

The annual retainer includes:

- maintained telemetry and version mappings;
- quarterly preservation tests;
- a defined number of standard incident hours;
- response-time SLA;
- evidence-template updates;
- one annual SOP/tabletop refresh.

Target mature CAC is 20,000–40,000 PLN, recovered through activation plus the first retainer. Severe incidents and clinical or legal expert work require separately contracted specialists and are not absorbed into the base price.

## First 10 and 100 Customers

First 10:

1. Use EUDAMED device and actor information, national field-safety-notice pages, CE-marked product directories, and public product documentation to identify 120 connected-wearable OEMs.
2. Prioritize companies with multiple app/firmware releases, an owned cloud platform, a small QA team, and no visible telemetry-preservation workflow.
3. Publish a simulated incident showing how the same output becomes unreconstructable when one firmware, calibration, or timestamp record is missing.
4. Send technical, event-specific outreach to heads of quality, post-market surveillance, regulatory affairs, and software.
5. Offer a prepaid 30,000–40,000 PLN rehearsal covering one product and one simulated complaint.

Customers 11–100:

- expand from one product line to the manufacturer’s portfolio;
- publish anonymized evidence-loss and reconstruction benchmarks;
- maintain adapters for recurring device-cloud and QMS patterns;
- integrate with QMS platforms without depending on exclusivity;
- later sell through medical-device QA consultants or cybersecurity firms only after direct CAC and retention are established.

## Primary Control Point

At the first sale, the manufacturer signs an operational annex that:

- inserts IncidentFreeze into the evidence-preservation step for covered complaints;
- defines the covered product, systems, data fields, and response times;
- prepays 12 months of standby;
- permits the installed read-only snapshot/export component;
- grants IncidentFreeze ownership of generic extraction, hashing, reconstruction, and evidence-packaging methods;
- keeps all customer data and confidential product logic segregated.

Within 12 months and 100,000 PLN founder capital, control proof is:

- three paid manufacturers;
- two signed SOP routing annexes;
- three installed product mappings;
- two successful repeated preservation drills;
- one real, historical, or independently designed incident reconstruction;
- reusable code covering at least 60% of the third activation.

The contract routes technical preservation, not regulatory authority.

## Cold Start and Resource Bootstrap

Required resources:

- a safe read-only snapshot agent or export orchestrator;
- an incident evidence manifest;
- a reconstruction sandbox;
- a senior QA/RA reviewer;
- legal, privacy, security, and liability boundaries.

Bootstrap:

1. Buy or use legitimately owned connected wearables with accessible developer or export interfaces.
2. Create a mock device-app-cloud telemetry pipeline.
3. Simulate firmware, clock, calibration, connectivity, and algorithm-version discrepancies.
4. Demonstrate that a frozen package can reproduce a displayed output.
5. Map the package into a generic complaint record.
6. Obtain fixed-scope QA/RA and legal review.
7. Require a deposit before integrating a customer sandbox or QMS.

No clinic, patient cohort, regulator relationship, device-OEM partnership, or speculative data right is needed.

## Distribution Advantage

EUDAMED, product pages, release notes, app-store histories, field-safety notices, technical documentation, and quality/regulatory hiring create a finite, observable prospect set.

The product can be sold at a concrete operational event:

- market launch;
- new algorithm or firmware release;
- QMS upgrade;
- post-market audit preparation;
- field-safety event;
- insurer or notified-body review.

Each activation adds reusable modality, system, and failure-pattern knowledge. The founder can use precise written technical outreach rather than constant networking or a personal brand.

## Competitive Advantage and Expansion Path

Greenlight Guru, MasterControl, Veeva, Wipro, and other QMS/PMS providers already control complaint workflow, quality records, CAPA, and reporting. IncidentFreeze should integrate with those systems, not recreate them.

Differentiation:

- raw and near-raw physiological telemetry preservation;
- device-app-cloud version lineage;
- algorithm-output reconstruction;
- event-window integrity;
- product-specific preservation drills;
- evidence frozen before interpretation.

Expansion path:

1. One connected medical wearable and one complaint path.
2. Full product portfolio within the OEM.
3. Cross-product trend evidence and repeated preservation testing.
4. Remote-monitoring platforms and connected diagnostic equipment.
5. Field-safety corrective-action evidence packaging.
6. Insurer, legal-hold, or acquisition diligence support after sufficient product history exists.

IncidentFreeze must not become a generic regulatory consulting or complaint-processing service.

## Poland/EU or Local Adaptation Defense

Poland provides cost-efficient biosignal, cloud, software, and medical-device QA talent within the EU. A Polish base supports local-language delivery to CEE manufacturers and EU-based data processing.

MDR terminology, EUDAMED workflows, EU privacy requirements, and local QA/RA support create an execution advantage. They do not prevent global QMS, device-cloud, or consulting companies from entering.

Defense depends on installed SOP routing, product-specific mappings, accumulated reconstruction patterns, response performance, and lower-cost specialist delivery.

## Compounding Advantage

Each product activation can create:

- reusable telemetry extractors;
- firmware, app, SDK, and algorithm lineage schemas;
- event-window reconstruction logic;
- calibration and timestamp checks;
- QMS evidence templates;
- failure signatures;
- recurring standby revenue;
- switching costs from historical preservation baselines.

Confidential customer evidence remains isolated. Only generic methods and explicitly permitted non-identifying failure derivatives compound.

## Founder Wealth Model

All figures are hypotheses. Equity values are net of debt. Founder distributions include only distributed cash not retained in the business. Founder capital is capped at 100,000 PLN; larger scale capital comes only after paid proof from retained profit, customers, non-dilutive sources, debt supported by contracts, or external investors.

| Scenario | Customers, incidents, and pricing | Revenue and margins | Capital, ownership, reinvestment | Value, liabilities, and founder wealth | Timing |
|---|---|---|---|---|---|
| Conservative | Year 8: 30 retained OEM product lines at 120,000 PLN/year; 18 incidents at 50,000 PLN; 8 activations at 35,000 PLN. | 4.78m PLN revenue; 70% gross margin; 28% operating margin; 1.34m PLN EBIT. | 700k PLN cumulative scale capital, primarily customer-funded/non-dilutive; founder contributes no more than 100k; 12% team/angel dilution leaves 88%. Reinvest 95% while employed; optional distributions ≤5%. | At 4.25× EBIT less 150k debt, equity value is about 5.54m PLN; founder share about 4.88m. Add 800k PLN post-transition distributions not retained in the business: about 5.68m PLN founder net worth. Response, insurance, and data-custody liabilities are included in operating costs. | Paid rehearsal by month 6; 4 retainers year 2; 14 year 4; target around year 8. |
| Expected success | Year 7: 60 retained product lines at 140,000 PLN/year; 40 incidents at 60,000 PLN; 15 activations at 45,000 PLN. | 11.48m PLN revenue; 76% gross margin; 36% operating margin; 4.13m PLN EBIT. | 2m PLN cumulative scale capital; 20% dilution leaves 80% founder ownership; founder contribution remains capped at 100k. Reinvest 95% while employed; optional distributions ≤5%. | At 5× EBIT less 400k debt, equity value is about 20.25m PLN; founder share about 16.2m. Add 1.5m PLN post-transition distributions: about 17.7m PLN founder net worth. | 3 activations year 1; 12 retainers year 3; repeatable EU acquisition year 4; target exceeded by years 5–7. |
| Strong success | Year 8: 160 retained product lines at 170,000 PLN/year; 120 incidents at 70,000 PLN; 35 activations at 50,000 PLN. | 37.35m PLN revenue; 80% gross margin; 42% operating margin; 15.69m PLN EBIT. | Up to 8m PLN later growth capital after recurring proof; 38% dilution leaves 62% founder ownership; founder contributes no more than the original 100k. Reinvest 100% until scale; no employment-period distributions. | At 5.5× EBIT less 1.5m debt, equity value is about 84.8m PLN; founder share about 52.6m. No distributions are added. | CEE product-line coverage year 3; broader EU integrations year 5; connected-device expansion by year 8. |

The conservative scenario reaches the wealth target through founder equity plus post-transition distributions. The expected route supports the target without relying on strong success.

## Reinvestment and Compounding Model

Conservative and expected scenarios reinvest 95% of after-tax distributable cash while the founder remains employed. Optional employment-period founder distributions remain at or below 5%.

Reinvestment priorities:

1. security and privacy controls;
2. response insurance and contractual safeguards;
3. reusable device-cloud and QMS adapters;
4. reconstruction automation;
5. QA/RA expert capacity;
6. monitored response coverage;
7. event-driven technical acquisition.

Strong success reinvests 100% until scale. Retained cash is not counted separately from equity value.

Post-transition distributions begin only after response liabilities, insurance, contractor capacity, customer data obligations, and 12 months of company runway are funded.

## Reachability and 180-Day Paid-Proof Plan

Days 1–30:

- define non-clinical, non-regulatory scope;
- build the incident evidence manifest;
- obtain initial QA/RA and legal review;
- spend up to 9,000 PLN.

Days 31–60:

- create a mock device-app-cloud pipeline;
- build the read-only freeze and hashing workflow;
- simulate lost firmware, timestamps, calibration, and telemetry;
- cumulative spend up to 19,000 PLN.

Days 61–90:

- demonstrate reconstruction of a displayed output;
- prepare SOP annex, security description, and fixed-scope offer;
- build 120 named OEM accounts;
- cumulative spend up to 27,000 PLN.

Days 91–150:

- offer a 30,000–40,000 PLN rehearsal and 12-month standby with a 50% deposit;
- qualify sandbox access, legal authority, and internal sponsor;
- do not promise live 24/7 response before paid capacity exists.

Days 151–180:

- deliver one paid rehearsal;
- install the sandbox/staging preservation route;
- execute the simulated complaint;
- obtain the signed SOP routing annex and standby activation.

Maximum pre-proof founder spend: **35,000 PLN**. Paid proof is an independent manufacturer’s deposit or prepayment, not a free audit, grant, interview, or regulator introduction.

## Capital Tranches and Maximum Loss

1. Up to 9,000 PLN: scope, architecture, and initial expert review.
2. Up to 19,000 PLN: mock telemetry and freeze feasibility.
3. Up to 35,000 PLN total: polished rehearsal and acquisition before paid proof.
4. Up to 60,000 PLN only after deposit, lawful sandbox access, and successful rehearsal.
5. Up to 100,000 PLN only after two independent manufacturers, positive contribution margin, and at least one signed annual standby contract.
6. No further founder or family capital. Expansion beyond 100,000 PLN must be funded by customer prepayment, retained profit, non-dilutive funding, contract-backed debt, or external investment after recurring proof.

## Critical Dependency Map

| Dependency | Evidence or direct test | Veto condition |
|---|---|---|
| Manufacturer controls required telemetry | Sandbox access and system map before acceptance | Critical evidence sits with an uncontracted third party |
| Evidence can be frozen without changing device behavior | Read-only rehearsal and security review | Integration introduces unacceptable product or cybersecurity risk |
| SOP routing is contractable | Signed annex and prepaid standby | Buyers purchase a memo but refuse operational routing |
| Manufacturer pays before a real incident | Rehearsal deposit | Interest exists only after rare emergencies |
| Product stays outside regulatory decision-making | Counsel and QA/RA scope | Customer expects reportability, causality, or clinical conclusions |
| Adapter reuse supports margin | Delivery-hour ledger across first three products | Each activation remains bespoke and expert-heavy |
| Liability is insurable | Broker and contract review | Coverage is unavailable or uneconomic |
| QMS incumbents do not already solve the gap | Customer workflow comparison | Existing platform captures and reconstructs the same telemetry at no incremental cost |

## Full-Time Transition Gate

The founder remains employed until:

- at least five independent retained manufacturers or eight contracted product lines;
- positive contribution margin on three activations;
- at least two signed SOP-routing renewals;
- two successful repeated preservation drills;
- a repeatable direct acquisition signal;
- insured escalation and named QA/RA capacity;
- no single manufacturer exceeds 35% of contracted next-12-month gross profit;
- personal and company runway each cover 12 months.

Live response hours must remain bounded until the business can fund formal coverage.

## Failure Recovery and Reusable Assets

If manufacturers reject external standby, reusable assets include:

- the incident evidence manifest;
- snapshot and hashing software;
- device-app-cloud lineage schemas;
- reconstruction sandbox;
- simulated failure library;
- QMS export templates;
- connected-device prospect map.

These can be licensed to an established QMS/PMS provider, medical-device consultancy, insurer, or incident-response firm. The founder retains physiological-data forensics and connected-device lifecycle expertise.

Customer data are returned or deleted according to contract; no fallback depends on reselling incident data.

## Critical Evidence

- MDR requires manufacturers to report serious incidents and certain trends within defined timelines.
- European Commission vigilance guidance provides formal terminology and reporting context.
- EUDAMED is the EU system for device, actor, vigilance, and market-surveillance information.
- Greenlight Guru already offers structured complaint, CAPA, and post-market workflows.
- Wipro offers end-to-end complaint handling, vigilance reporting, recalls, CAPA, and trend reporting, demonstrating both real budgets and strong competition.

## Critical Hypotheses

- Small connected-wearable OEMs lack an installed raw-telemetry preservation step despite having complaint-management software.
- They will prepay 30,000–40,000 PLN for a rehearsal before a live incident occurs.
- At least 100,000 PLN annual standby is supportable after proof.
- The manufacturer can contractually provide necessary sandbox and production-export access without a third-party platform agreement.
- Product-specific mapping becomes at least 60% reusable by the third activation.
- Routine retainers can maintain 60%+ gross margin without founder availability becoming the product.
- SOP routing and historical preservation baselines create meaningful switching cost.
- Thirty retained European product lines are reachable without heroic market share.

## Kill Criteria

Kill or structurally pivot if:

- no prepaid rehearsal by day 180;
- fewer than four qualified calls from 120 named OEMs;
- three qualified manufacturers state their QMS or device platform already preserves and reconstructs the full physiological evidence chain;
- buyers refuse an SOP routing annex or annual standby;
- critical telemetry is controlled by an uncontracted third party in most qualified accounts;
- customers require IncidentFreeze to determine reportability, causality, or clinical conclusions;
- first activation exceeds 160 delivery hours with less than 40% reusable tooling;
- annual willingness to pay is below 75,000 PLN;
- mature recurring gross margin projects below 60%;
- insurance, privacy, or cybersecurity liability cannot be bounded within pricing.

## Budget, Time, and Minimum People Stack

Pre-proof founder budget: maximum 35,000 PLN.

Total founder capital: maximum 100,000 PLN.

Founder time: 20–25 hours per week, capped at five hours per day.

Minimum people stack:

- founder: product, physiological-data engineering, automation, and acquisition;
- senior medical-device QA/RA contractor: scope, SOP, and delivery review;
- contract cloud/security engineer: read-only agent and threat review;
- privacy/technology counsel: DPA, evidence custody, IP, and liability;
- on-call specialist capacity only after prepaid retainers.

No full-time hire, clinical interpretation service, regulator relationship, production integration, or 24/7 commitment is funded before repeatable paid evidence.

## Research Sources

- [EU Medical Device Regulation](https://eur-lex.europa.eu/eli/reg/2017/745/oj/eng)
- [European Commission Medical-Device Guidance](https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en)
- [European Commission EUDAMED Overview](https://health.ec.europa.eu/medical-devices-eudamed/overview_en)
- [European Commission Market Surveillance and Vigilance](https://health.ec.europa.eu/medical-devices-sector/directives/market-surveillance-and-vigilance_en)
- [Greenlight Guru Complaint Management](https://www.greenlight.guru/complaint-management-software)
- [Wipro Post-Market Surveillance](https://www.wipro.com/business-process/solutions/post-market-surveillance/)
