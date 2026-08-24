# Zero-to-One Candidate: PhysioVault Replay Archive

## One-Sentence Thesis

Build the waveform-specific, vendor-exit-proof archive that preserves not only clinical-trial wearable data, but also the exact executable path from raw signals to reported endpoints for future inspection and reproduction.

## Founder Fit

The founder’s neuroscience, biosignal, data-science, and automation background fits raw physiological formats, timestamp integrity, transformation pipelines, and reproducibility testing. The initial product can be built alongside employment using existing storage infrastructure, open container standards, and fixed-scope GxP/legal review.

The founder does not claim clinical, regulatory, or archival authority. PhysioVault preserves and replays customer-provided evidence; the sponsor remains responsible for determining which records are essential, validating production use, and satisfying regulatory obligations.

## Customer, Pain, and Current Workaround

The beachhead customer is a small or mid-sized European biotech sponsor that has completed, is closing, or is migrating a study using actigraphy, ECG, EEG, sleep, PPG, or another wearable-derived endpoint.

Its inside view is: “I can retain files for 25 years, but I may not be able to prove what firmware, export logic, filtering, units, time-zone handling, algorithm version, or computational environment produced the submitted endpoint after the original vendor or software disappears.”

The painful events are:

- study closeout and transfer into long-term retention;
- termination or replacement of a wearable/DHT vendor;
- acquisition, insolvency, or product retirement affecting the original platform;
- inspection, resubmission, licensing transaction, or due diligence requiring old endpoint reproduction;
- discovery that archived files omit audit trails, metadata, computational methods, or readable formats.

Current workarounds include retaining vendor exports, PDFs, SAS outputs, source code fragments, eTMF documents, and storage snapshots across separate systems. General archives protect files and documents, but the decision-critical hypothesis is that many do not continuously prove that a physiological endpoint can still be regenerated from the archived inputs.

## Product Wedge

The first paid product is a fixed-scope **Wearable Exit-and-Replay Pack** for one completed study:

- inventory of raw, intermediate, derived, and reported data;
- device, firmware, app, SDK, algorithm, units, time-zone, and configuration manifest;
- immutable hashes and chain-of-custody record;
- documented mapping from raw signals to reported variables;
- containerized or otherwise portable replay environment;
- expected-output regression tests;
- missing-component and future-obsolescence report;
- one successful independent replay;
- 12 months of prepaid mirror custody and one restoration drill.

The initial pack is a non-production computational-evidence mirror unless the customer separately validates and designates it for regulated archival use. It complements rather than replaces the sponsor’s eTMF, official archive, QMS, or regulatory responsibilities.

## Commercial Insight or Market Gap

**Evidence:** EU clinical-trial rules require long retention, and FDA computerized-systems guidance explicitly addresses discontinued or incompatible systems, preservation of computational methods, and validated migration.

**Hypothesis:** The commercially valuable unit is not storage capacity. It is a verified, executable endpoint package that survives vendor exit and can regenerate an agreed result without the original cloud platform.

A generic archive can store files. PhysioVault must own the narrow technical workflow for reconstructing high-frequency physiological data: timestamp interpretation, packet-loss metadata, calibration, signal transformations, algorithm versions, and reported endpoint reconciliation.

## Underused Momentum

- EU Clinical Trials Regulation Article 58 requires the clinical trial master file to be archived for at least 25 years.
- DHTs and wearables create more high-frequency, vendor-dependent evidence than document-centric archive workflows were designed around.
- FDA guidance states that sponsors must retain the ability to retrieve data from discontinued systems and preserve relevant extraction logic and computational methods.
- Containerization, open file formats, object-lock storage, and automated regression testing make executable preservation more affordable for smaller sponsors.

These facts demonstrate regulatory and technical momentum. They do not prove willingness to pay for a separate replay layer.

## Beachhead Market

European biotech sponsors with:

- one to ten active or recently completed clinical trials;
- a wearable or physiological endpoint in at least one study;
- no large internal clinical-data engineering group;
- a study closeout, vendor migration, transaction, or inspection-readiness event inside nine months;
- access to complete exports under their existing vendor agreement.

Exclude sponsors that cannot legally provide the required data, expect PhysioVault to recover inaccessible proprietary source code, or require immediate qualification as their sole official GxP archive.

## Business Model and Unit Economics

All prices, costs, attachment rates, and margins are hypotheses.

| Offer | Price | Direct cost | Hypothesized contribution |
|---|---:|---:|---:|
| Initial one-study Exit-and-Replay Pack | 30,000–45,000 PLN | 14,000–22,000 PLN | 35–60% |
| Mature study migration and replay package | 120,000–180,000 PLN | 35,000–60,000 PLN | 55–75% |
| Annual custody, integrity checks, and replay | 45,000–75,000 PLN per study | 10,000–20,000 PLN | 65–85% |
| Additional inspection/restoration drill | 20,000–40,000 PLN | 6,000–12,000 PLN | 60–80% |
| Customer-funded device/vendor adapter | 25,000–80,000 PLN | Scope-dependent | Minimum 50% target |

Storage is passed through transparently or bundled with a controlled allowance. Pricing is based on study complexity and evidence risk, not gigabytes alone.

Target mature CAC is 20,000–45,000 PLN per sponsor, recovered through the initial migration. A sponsor with several studies should produce materially better economics than separate one-study sales.

## First 10 and 100 Customers

First 10:

1. Search CTIS and public trial registries for completed or closing European trials mentioning actigraphy, wearable ECG, EEG, sleep, PPG, accelerometry, or DHTs.
2. Prioritize small sponsors with a visible trial completion, terminated technology provider, licensing transaction, acquisition, or new data-management hire.
3. Build a named list of 120 sponsor data, quality, and clinical-operations leaders.
4. Publish a technical demonstration showing that a deliberately obsolete wearable pipeline can be reconstructed from a self-contained evidence package.
5. Offer a 30,000–40,000 PLN one-study pack with a 50% deposit and explicit exclusions.

Customers 11–100:

- expand within paying sponsors from one archived study to the portfolio;
- publish anonymized format-obsolescence and replay-failure benchmarks;
- productize adapters for common ECG, actigraphy, EEG, and wearable-export formats;
- sell directly to additional sponsors and specialist CROs;
- use archive vendors and clinical-data consultants only as non-exclusive channels after direct economics work.

No archive-provider partnership is required for the first sale or foundational control point.

## Primary Control Point

The first-sale control point is a signed agreement that:

- designates the delivered package as the study’s canonical computational replay reference;
- places a complete customer-authorized data and metadata copy in PhysioVault custody;
- prepays 12 months of integrity monitoring and one replay;
- grants PhysioVault ownership of generic parsers, schemas, replay tools, and non-customer-specific test methods;
- requires customer-specific adapters and confidentiality to remain segregated.

Within 12 months and 100,000 PLN of founder capital, the target proof is:

- three paid study packages from at least two sponsors;
- two different physiological modalities or vendor formats;
- one successful repeat replay at least three months after migration;
- reusable adapters covering at least 60% of the second project;
- no reliance on proprietary rights that the customer cannot contractually provide.

This is a workflow and installed-history control point, not regulatory exclusivity.

## Cold Start and Resource Bootstrap

The initial resource is an owned replay harness rather than a full regulated archive platform.

Bootstrap steps:

1. Use public or founder-generated biosignal data to create a deliberately versioned raw-to-endpoint pipeline.
2. Package raw files, metadata, environment, transformation logic, hashes, and expected results.
3. Demonstrate restoration on a clean machine without the original development environment.
4. Use standard cloud object lock, encryption, customer-specific keys, and documented access controls.
5. Obtain fixed-scope GxP, privacy, and contract review.
6. Require a deposit before adding any customer-specific vendor adapter or production environment.

Prepaid customer work, not speculative inventory or data acquisition, finances the first specialized adapter.

## Distribution Advantage

CTIS and other registries expose sponsors, trial status, therapeutic area, and timing. Technical publications, trial protocols, vendor case studies, and job postings can reveal wearable use and migration events.

This supports low-social-energy, event-driven outbound. Each completed migration creates:

- a reusable format adapter;
- a documented failure mode;
- a new restoration benchmark;
- an expansion route into the sponsor’s other studies.

The distribution advantage remains a hypothesis until named-event outbound produces deposits at acceptable CAC.

## Competitive Advantage and Expansion Path

Arkivum, Veeva, SureClinical, and other archives already provide strong retention, integrity, and inspection-readiness capabilities. PhysioVault cannot win as a cheaper generic archive.

The differentiation must be:

- physiological waveform specialization;
- executable endpoint replay;
- vendor-version and algorithm lineage;
- independent restoration testing;
- cross-vendor migration;
- evidence that the final reported endpoint remains reproducible.

Expansion path:

1. One wearable study exit-and-replay pack.
2. Multi-study sponsor portfolio.
3. Annual automated restoration and integrity testing.
4. Cross-vendor endpoint migration and equivalence evidence.
5. Additional high-dimensional modalities such as imaging-derived measurements, audio biomarkers, and connected-device data.
6. Licensed replay tooling for established archives or CROs if direct custody becomes trust-limited.

## Poland/EU or Local Adaptation Defense

Poland offers cost-efficient data-engineering, validation, cybersecurity, and biosignal talent within the EU legal environment. European hosting, EU-standard contracts, local-language support, and familiarity with CTIS/MDR/GDPR workflows can reduce adoption friction for CEE and smaller European sponsors.

There is no statutory moat. A global archive provider can build the same capability. The defense must come from accumulated physiological adapters, replay histories, lower-cost specialist delivery, and faster handling of small sponsor portfolios.

## Compounding Advantage

Each project can add:

- reusable raw-data and metadata parsers;
- device, firmware, and algorithm lineage templates;
- endpoint-specific validation tests;
- failure signatures for timestamps, units, missing packets, calibration, and transformations;
- restoration procedures;
- installed recurring custody revenue.

Customer data remain isolated. Compounding depends on retaining generic methods and format knowledge contractually, not pooling sensitive trial data.

## Founder Wealth Model

All figures are hypotheses. Business values are equity values net of stated debt. Founder distributions include only cash actually distributed and exclude retained earnings already reflected in business value. Founder capital is capped at 100,000 PLN; later capital comes from customers, retained profit, non-dilutive funding, debt after recurring revenue, or external investors.

| Scenario | Customers, studies, and pricing | Revenue and margins | Capital, ownership, reinvestment | Value, liabilities, and founder wealth | Timing |
|---|---|---|---|---|---|
| Conservative | Year 9: 45 retained studies at 50,000 PLN/year; 12 migrations at 140,000 PLN; 8 drills at 25,000 PLN. | 4.13m PLN revenue; 68% gross margin; 27% operating margin; 1.12m PLN EBIT. | 600k PLN cumulative scale capital, mostly customer-funded and non-dilutive; founder contributes no more than 100k; 12% team/angel dilution leaves 88% ownership. While employed, 95% of after-tax distributable cash is reinvested and optional distributions remain ≤5%. | At 4.5× EBIT less 150k debt, equity value is about 4.88m PLN; founder share about 4.29m. Add 1.1m PLN cumulative post-transition founder distributions not retained in the business: about 5.39m PLN founder net worth. Contract-performance and storage liabilities are funded within operating costs. | Paid proof by month 6; 5 retained studies by year 2; 18 by year 4; employment exit only after transition gate; target reached around year 9. |
| Expected success | Year 8: 90 retained studies at 60,000 PLN/year; 20 migrations at 160,000 PLN; 18 drills at 30,000 PLN. | 9.14m PLN revenue; 75% gross margin; 35% operating margin; 3.20m PLN EBIT. | 1.5m PLN cumulative capital from retained profit, non-dilutive funding, and limited equity; 20% total dilution leaves 80% founder ownership; founder cash remains capped at 100k. Reinvest 95% while employed, with optional distributions ≤5%. | At 5× EBIT less 300k debt, equity value is about 15.7m PLN; founder share about 12.6m. Add 1.5m PLN post-transition distributions: about 14.1m PLN founder net worth. | 3 studies year 1; 15 year 3; portfolio expansion year 4; target exceeded by years 6–8. |
| Strong success | Year 8: 220 retained studies at 75,000 PLN/year; 45 migrations at 190,000 PLN; 50 drills at 35,000 PLN. | 26.8m PLN revenue; 80% gross margin; 40% operating margin; 10.72m PLN EBIT. | Up to 6m PLN growth capital after repeatable proof; 35% dilution leaves 65% founder ownership; founder contributes no more than the original 100k. Reinvest 100% of available after-tax cash through scale; no employment-period distributions. | At 5.5× EBIT less 1m debt, equity value is about 58.0m PLN; founder share about 37.7m. No distributions are added. | European portfolio archive by year 4; licensed delivery and additional modalities by year 6; scale reached around year 8. |

The conservative route reaches the 5m PLN target only through patient compounding and post-transition distributions. The expected route supports the target without requiring the strong scenario.

## Reinvestment and Compounding Model

In conservative and expected scenarios, 95% of after-tax business cash available for distribution is reinvested while the founder remains employed. Optional founder distributions are capped at 5%.

Reinvestment priorities are:

1. security and validation;
2. reusable device and format adapters;
3. automated restoration tests;
4. insurance and contractual risk controls;
5. technical delivery capacity;
6. direct event-driven acquisition.

The strong scenario reinvests 100% until scale. Retained earnings are not separately added to founder net worth when already represented in business value.

After the full-time transition gate, distributions are permitted only after customer-custody liabilities, storage commitments, insurance, and at least 12 months of company operating runway are funded.

## Reachability and 180-Day Paid-Proof Plan

Days 1–30:

- build the open replay demonstrator;
- select object-lock and encryption architecture;
- define customer-data exclusions and scope;
- spend up to 10,000 PLN.

Days 31–60:

- complete one clean-machine restoration;
- obtain fixed-scope privacy, GxP-positioning, and contract review;
- prepare the canonical package specification;
- cumulative spend up to 22,000 PLN.

Days 61–100:

- build a list of 120 closing or completed wearable-enabled studies;
- publish the technical demonstration;
- offer a 30,000–40,000 PLN Exit-and-Replay Pack with 50% deposit;
- cumulative spend capped at 30,000 PLN.

Days 101–150:

- close one prepaid project;
- receive the customer-authorized export;
- build only the required adapter;
- execute the first independent replay.

Days 151–180:

- deliver the package;
- activate 12-month prepaid custody;
- schedule the first restoration drill;
- seek expansion to a second study or sponsor.

Maximum founder spend before paid proof: **38,000 PLN**. Paid proof is a deposit or full prepayment from an independent sponsor, not an interview, grant, partnership, or unpaid demonstration.

## Capital Tranches and Maximum Loss

1. Up to 10,000 PLN: technical replay feasibility.
2. Up to 22,000 PLN: secure architecture and professional review.
3. Up to 38,000 PLN total: polished demonstration and acquisition before paid proof.
4. Up to 65,000 PLN total only after deposit, lawful data transfer, and successful first replay.
5. Up to 100,000 PLN total only after two independent paying sponsors or three paid studies, positive contribution margin, and one contracted repeat replay.
6. No additional founder or family capital. Later expansion must be financed by revenue, non-dilutive funding, working-capital debt supported by contracts, or external capital after repeatable demand.

## Critical Dependency Map

| Dependency | Evidence or direct test | Veto condition |
|---|---|---|
| Sponsor possesses complete exports and necessary rights | Contract and sample inventory before acceptance | Essential raw data, metadata, or algorithm logic cannot be lawfully obtained |
| Replay can reproduce an agreed endpoint | Clean-machine technical test | Output cannot be reconciled within a pre-agreed tolerance |
| Buyer pays separately for replay | Deposit from an independent sponsor | Buyers consistently treat generic storage or internal packaging as sufficient |
| Production positioning is insurable and contractable | Counsel and insurer review | Liability cannot be bounded within attainable pricing |
| Adapters are reusable | Hours and code reuse across first three studies | Each study remains bespoke with less than 40% reusable delivery |
| Recurring custody attaches | Prepaid 12-month term and renewal | Customers purchase only a one-off report with no replay or custody |
| Acquisition is repeatable | Named-event outbound metrics | Fewer than four qualified calls from 120 relevant accounts |

## Full-Time Transition Gate

The founder remains employed until all are true:

- at least five independent paying sponsors or ten contracted studies;
- positive contribution margin on three completed migrations;
- at least three annual custody contracts;
- one successful delayed restoration replay;
- repeatable acquisition beyond personal contacts;
- no single sponsor represents more than 35% of contracted next-12-month gross profit;
- company and personal runway each cover at least 12 months;
- security, insurance, and contractual controls are operating.

## Failure Recovery and Reusable Assets

If sponsors do not buy independent custody, the replay harness, format adapters, and restoration tests can be:

- licensed to an established archive provider;
- sold as internal sponsor tooling;
- used for one-time vendor-exit migration projects;
- adapted to medical-device evidence retention or high-dimensional laboratory data.

The founder retains biosignal pipeline, reproducibility, archival, and regulated-data engineering expertise. Customer-confidential data are deleted or returned according to contract.

## Critical Evidence

- EU Clinical Trials Regulation Article 58 requires at least 25 years of clinical trial master-file archiving.
- FDA computerized-systems guidance states that sponsors must preserve retrieval from discontinued systems and retain relevant computational and extraction methods.
- FDA has formal guidance for DHT use in remote clinical-trial data acquisition.
- Arkivum explicitly offers long-term preservation of raw clinical and wearable data, proving commercial demand but also establishing a strong incumbent.
- Veeva provides long-term study-document archival and inspection access, defining the adjacent incumbent boundary.

## Critical Hypotheses

- Sponsors will pay separately for executable endpoint replay rather than treating it as part of archive migration.
- A 30,000–40,000 PLN initial pack can enter procurement within 180 days.
- Customer contracts provide sufficient exports without a speculative device-vendor agreement.
- At least 60% of adapter work becomes reusable after two projects in the same modality.
- Annual custody and restoration pricing of at least 45,000 PLN attaches to most migrated studies.
- A small unknown provider can earn custody trust through bounded scope, demonstrable replay, security controls, and professional review.
- The addressable population can support at least 45 retained studies without heroic market share.

## Kill Criteria

Kill or structurally pivot if:

- no paid deposit by day 180;
- fewer than four qualified calls from 120 named closing-study accounts;
- three qualified buyers say Arkivum, Veeva, their CRO, or internal processes already provide executable endpoint replay at no incremental budget;
- the first customer cannot lawfully provide essential data or transformation logic;
- the first replay cannot reproduce an agreed output;
- the first two projects each require more than 180 delivery hours with less than 40% reusable tooling;
- mature gross margin projects below 60%;
- customers reject prepaid custody and annual replay;
- insurance or contractual liability makes the target pricing uneconomic.

## Budget, Time, and Minimum People Stack

Pre-proof founder budget: maximum 38,000 PLN.

Total founder capital: maximum 100,000 PLN.

Founder time: 20–25 hours per week, capped at five hours per day.

Minimum people stack:

- founder: product, biosignal/data engineering, automation, and acquisition;
- contract cloud/security engineer: fixed-scope architecture review;
- GxP/clinical-data consultant: boundaries, documentation, and validation strategy;
- privacy/technology counsel: DPA, custody, IP, and liability;
- part-time delivery engineer only after paid proof.

No full-time hire, proprietary-device agreement, official archive replacement, or large production certification program is funded before repeatable paid demand.

## Research Sources

- [EU Clinical Trials Regulation, Article 58](https://eur-lex.europa.eu/legal-content/EN-DE/TXT/?uri=CELEX%3A32014R0536)
- [FDA Guidance: Computerized Systems Used in Clinical Trials](https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/fda-bioresearch-monitoring-information/guidance-industry-computerized-systems-used-clinical-trials)
- [FDA Guidance: Digital Health Technologies for Remote Data Acquisition](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/digital-health-technologies-remote-data-acquisition-clinical-investigations)
- [EMA Clinical Trials Information System](https://www.ema.europa.eu/en/human-regulatory-overview/research-development/clinical-trials-human-medicines/clinical-trials-information-system)
- [Arkivum Clinical Trial Data Archiving](https://arkivum.com/pharmaceutical-life-sciences/clinical-trial-data/)
- [Veeva SiteVault Study Archive](https://sites.veevavault.help/gr/sitevault/studies/archive-overview/)
