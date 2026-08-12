# Zero-to-One Candidate: CarrierPromise

## One-Sentence Thesis

CarrierPromise is a real-time copilot for CEE freight forwarders that turns human carrier-negotiation calls into confirmed, structured commercial commitments before ambiguous rates, accessorials, equipment requirements, or loading windows become booking and invoice disputes.

## Founder Fit

**Evidence**

- Freight operations are phone-heavy and increasingly digitized, creating a technically accessible human–AI interface problem rather than a capital-intensive logistics business.
- The product can begin as a software-assisted service without owning trucks, freight, or regulated transport infrastructure.

**Hypothesis**

- The founder’s data-science and AI background is sufficient to build the extraction, contradiction-detection, and outcome-analysis layer with a contract engineer.
- A Warsaw base is useful for Polish and CEE road-freight specialization.
- Direct owner and operations-manager outreach can be batched and partly delegated, avoiding influencer-led distribution or constant networking.
- The initial phase is executable in 20–25 founder hours per week while retaining employment.

## Customer, Pain, and Current Workaround

The beachhead customer is a Polish freight-forwarding or brokerage office with approximately 5–50 dispatchers that procures cross-border European road capacity by phone.

Customer inside-view:

> “My dispatcher agreed a rate, but the carrier heard a different currency, free-time allowance, pallet obligation, or delivery window. The problem appears only after the load is moving or the invoice arrives.”

Painful events include:

- rate or currency disagreement;
- unrecorded toll, ferry, fuel, or temperature surcharge;
- unclear loading and delivery appointments;
- detention or demurrage terms omitted from the TMS;
- wrong equipment, pallet-exchange, or cargo-handling assumption;
- carrier saying it never accepted the load;
- dispatcher retyping call terms incorrectly;
- manager reconstructing a dispute from memory, chat, and fragmented notes.

Current workarounds are handwritten notes, personal spreadsheets, email recaps, TMS free-text fields, call recordings searched only after a dispute, and asking the carrier to reconfirm details manually.

**Evidence**

HappyRobot’s Circle Logistics case study describes carrier sales as involving high volumes of calls, rate negotiation, booking confirmation, and compliance checks. Transporeon already supports electronic offers and acceptance, showing that structured digital commitment is commercially normal once the transaction reaches a platform.

**Hypothesis**

A 5–50-dispatcher forwarder loses enough through corrections, unbilled accessorials, booking rework, and disputes to pay 2,500–3,500 PLN per month for a system that captures commitments at the call boundary.

## Product Wedge

The initial product augments human dispatchers rather than replacing them.

A dispatcher calls through a CarrierPromise SIP number, softphone, or desktop dialer. During the call, the product extracts:

- carrier and dispatcher identity;
- route and load reference;
- rate, currency, and VAT treatment;
- equipment and cargo requirements;
- pickup and delivery windows;
- free waiting time and detention rate;
- pallet exchange;
- toll, ferry, fuel, temperature, and other accessorial terms;
- conditional language and unresolved contradictions.

The dispatcher sees a live, editable commitment card. Nothing is sent until the dispatcher confirms it.

Immediately after the call, CarrierPromise sends a bilingual confirmation by email, SMS, or link. The carrier can accept, correct, or reject individual terms. The final event is exported as email, PDF, CSV, or structured JSON. Early pilots do not require a TMS integration.

CarrierPromise does not autonomously book freight, authorize payments, or make binding commercial decisions. The human dispatcher remains the decision-maker.

## Commercial Insight or Market Gap

The market is moving in two directions:

1. digital freight platforms remove calls by structuring offers and acceptance;
2. voice-agent vendors replace repetitive carrier calls with autonomous agents.

The overlooked middle remains commercially important: difficult, relationship-sensitive, multilingual, or exception-heavy calls that forwarders still want humans to handle.

The customer does not primarily need another transcript. The desired outcome is a defensible commercial commitment that survives the transition from speech to booking, execution, and settlement.

CarrierPromise therefore sits at a transaction boundary:

```text
Human negotiation → structured commitment → counterparty confirmation → booking → settlement outcome
```

This differs from generic conversation intelligence because the output is a freight-specific transaction record tied to later economic outcomes.

## Underused Momentum

**Evidence**

- HappyRobot and FleetWorks show that voice AI is already being applied to freight calls.
- Transporeon demonstrates automated freight assignment, structured offer exchange, and electronic acceptance.
- The EU eFTI framework is standardizing digital freight information. Full application is scheduled for 9 July 2027.
- Real-time speech recognition, translation, and structured extraction are now available through usage-priced APIs.

**Hypothesis**

- Forwarders not ready for autonomous negotiation will accept a human-augmentation layer sooner.
- eFTI and TMS digitization increase the value of converting spoken commitments into structured data.
- Polish, Ukrainian, German, Czech, Slovak, and English freight terminology remains less well served than English-language US logistics.
- An EEA-hosted, freight-specific product can win regional customers before broad conversation-intelligence vendors localize deeply.

## Beachhead Market

The beachhead is Polish road-freight forwarders with:

- 5–50 dispatchers;
- frequent carrier procurement by phone;
- at least several hundred calls per month;
- cross-border EU lanes;
- an existing TMS but inconsistent call-to-TMS capture;
- owner-led or operations-manager-led purchasing;
- no requirement for enterprise-wide procurement approval to run a five-seat pilot.

The first use case is spot and exception-heavy carrier procurement. It excludes shipper tenders, full transport execution, autonomous booking, freight payment, and regulated eFTI-platform certification.

The initial buyer is the forwarding-company owner, carrier-sales manager, or head of operations. Dispatchers are users; finance and claims teams are downstream beneficiaries.

## Business Model and Unit Economics

### Pricing hypothesis

| Offer | Price | Included scope |
|---|---:|---|
| Paid proof pilot | 3,000 PLN for 30 days | Up to 5 users, 300 analyzed calls, manual onboarding and review |
| Core office | 2,490 PLN/month | 5 users, standard call allowance, commitment cards and exports |
| Additional dispatcher | 249 PLN/month | One additional seat |
| Multi-office/API | From 5,900 PLN/month | Multiple teams, analytics, API and custom controls |
| Onboarding | 2,500 PLN once | Vocabulary, templates, routing and data configuration |

Expected mature blended revenue is 2,800 PLN per customer per month.

### Expected customer-level economics — hypotheses

| Metric | Monthly amount |
|---|---:|
| Blended revenue | 2,800 PLN |
| Telephony, transcription, translation, and model usage | 250 PLN |
| Storage, monitoring, and security allocation | 70 PLN |
| Customer support and quality-review allocation | 300 PLN |
| Onboarding amortization | 50 PLN |
| Gross profit | 2,130 PLN |
| Gross margin | 76% |

Additional hypotheses:

- direct-acquisition CAC after repeatability: 4,000–7,000 PLN;
- CAC payback: two to four months of gross profit;
- annual gross logo retention: at least 88%;
- expansion comes from additional dispatchers, offices, and confirmation volume;
- payment is monthly or annual in advance;
- the company never finances freight or assumes carrier-payment risk.

## First 10 and 100 Customers

### First 10

1. Build a list of 100 Polish forwarders with 5–50 dispatchers using public TSL directories, company registries, freight-association lists, and LinkedIn.
2. Produce a 90-second mock-call replay showing an ambiguous rate and accessorial becoming a bilingual confirmation card.
3. Send a personalized message to the owner or operations manager naming one visible lane or operating specialty.
4. Offer a 20-minute workflow audit and a fixed 3,000 PLN pilot, not a free trial.
5. Target 15 qualified demonstrations and at least two paid pilots by day 150.
6. Use paid-pilot results to pursue eight additional customers from the remaining list and referrals.

The assumed outbound-to-paid conversion is a hypothesis. It is not required for the first paid proof; only one independent paying customer is required within 180 days.

### First 100

- 15 customers from direct founder outreach and referrals from the first cohort;
- 60 customers from a repeatable outbound sequence run by a part-time Polish/CEE sales contractor;
- 15 customers from freight-specific comparison pages, call-error calculators, and anonymized outcome case studies;
- 10 customers from optional TMS, telephony, and logistics-consultant referrals.

The business must not depend on a channel partnership. Direct acquisition remains sufficient if partners do not materialize.

A plausible three-year route is:

- year 1: 10 recurring customers;
- year 2: 35–50;
- year 3: 75–100.

## Primary Control Point

The primary control point is the freight commitment-to-settlement graph created when customer calls and confirmation events pass through CarrierPromise.

Each event can contain:

- normalized negotiated terms;
- human corrections;
- carrier acceptance, correction, or rejection;
- final booking terms;
- later invoice adjustments;
- detention or accessorial disputes;
- load cancellation or completion outcome.

Pilot and subscription agreements must explicitly grant CarrierPromise the right to retain anonymized, aggregated event and outcome data for product improvement. Raw audio is not the intended moat and should be deleted or retained only under customer-configured policies.

This control point is independently securable because it requires:

- a founder-controlled telephony or softphone layer;
- direct contracts with paying customers;
- data-processing agreements;
- explicit outcome-data rights;
- a freight-specific event schema;
- no exclusive TMS, carrier, or industry-association partnership.

Within 12 months and 100,000 PLN, the target proof is:

- 10 independent paying customers;
- calls routed through CarrierPromise by active dispatchers;
- at least 3,000 normalized call events;
- at least 500 carrier confirmation responses;
- at least 300 events paired with booking, correction, invoice, or dispute outcomes.

These volumes are hypotheses, not established demand.

## Cold Start and Resource Bootstrap

### Required resource

The foundational resource is not a generic call corpus. It is a permissioned dataset connecting spoken freight terms to human corrections, counterparty confirmation, and commercial outcomes.

### Bootstrap sequence

1. Founder purchases SIP numbers and controls the routing, event database, and domain.
2. A freight-domain contractor defines the first term ontology from public documents and synthetic calls.
3. The prototype uses synthetic and founder-recorded calls before any customer data is processed.
4. Paid-pilot contracts include data-processing, retention, and anonymized outcome-use clauses.
5. Customers export final booking and correction outcomes by CSV during the pilot; no TMS integration is required.
6. Human review creates high-quality labels while volumes remain small.
7. Confirmed events become evaluation cases for subsequent releases.

### Why an unknown founder can secure it

- The founder does not need access to carrier marketplaces or freight ownership.
- Each customer can independently authorize use of its own routing and operational records.
- The product can demonstrate value on five seats without enterprise procurement.
- Customer data is produced only after a paid agreement rather than acquired speculatively.
- Synthetic demonstrations allow sales before the proprietary dataset exists.

## Distribution Advantage

The initial distribution advantage is narrow problem specificity.

The sales message is not “AI for logistics.” It is:

> “Prevent carrier-call terms from changing between the phone, booking, and invoice.”

The demo can show the entire economic event in under two minutes. This makes founder-led outbound possible without a personal brand.

Distribution can compound through:

- customer-specific savings reports;
- anonymized “promise leakage” benchmarks;
- freight-language templates for specific lane pairs;
- carrier confirmation links that expose new forwarders to the product;
- referral incentives for operations consultants and TMS implementers;
- low-friction pilots that avoid full TMS integration.

Carrier-facing confirmation links are a potential distribution loop, but they are not assumed to create a viral network effect.

## Competitive Advantage and Expansion Path

### Existing alternatives

- HappyRobot and FleetWorks automate calls.
- Transporeon structures electronic offers and assignments.
- TMS vendors store booking terms.
- Generic conversation-intelligence platforms transcribe and summarize calls.
- Telephony providers can add extraction features.

### Proposed advantage

CarrierPromise focuses on the gap between live human negotiation and later settlement. Its advantage compounds through:

- a freight-specific commercial-term ontology;
- multilingual correction patterns;
- confirmed counterparty behavior;
- booking and invoice outcomes;
- customer-specific clause and accessorial rules;
- historical audit and search;
- embedded dispatcher habits.

### Expansion path

1. Spot carrier-procurement calls.
2. Carrier onboarding and compliance-call capture.
3. Track-and-trace exception commitments.
4. Detention and accessorial evidence.
5. Automated invoice reconciliation against confirmed terms.
6. Shipper procurement and contract-carrier workflows.
7. Intermodal, rail, customs, and temperature-controlled freight.

The company should remain a commitment and evidence layer rather than attempt to become a full TMS.

## Poland/EU or Local Adaptation Defense

The local defense is operational rather than regulatory exclusivity:

- Polish-first onboarding and support;
- freight terminology across Polish, English, German, Ukrainian, Czech, and Slovak;
- CEE road-freight accessorial and pallet-exchange conventions;
- EUR and PLN currency handling;
- EEA hosting and customer-configurable retention;
- GDPR-oriented data-processing controls;
- export schemas compatible with TMS and future eFTI workflows;
- pricing accessible to regional forwarders below enterprise size.

This is not a permanent barrier. Global voice-AI and TMS vendors can localize. CarrierPromise must convert its early regional workflow into an outcome dataset and switching cost before that happens.

## Compounding Advantage

Every routed transaction can improve:

- critical-term extraction;
- ambiguity detection;
- language-specific vocabulary;
- counterparty confirmation UX;
- prediction of likely disputes;
- customer-specific templates;
- automated booking and invoice checks.

As customers accumulate history, switching costs rise because CarrierPromise becomes the searchable record of what was negotiated, corrected, accepted, and ultimately paid.

The strongest potential compounding asset is the paired commitment-to-settlement dataset. Raw transcripts alone would not create meaningful defensibility.

## Founder Wealth Model

All scenarios below are hypotheses rather than market evidence.

Common assumptions:

- maximum founder cash committed before repeat demand: 100,000 PLN;
- no family capital;
- later expansion funded from prepaid subscriptions and retained earnings;
- no retained earnings counted separately from business value;
- valuation is based on normalized EBIT and excludes excess cash;
- no material personal liabilities attributable to the business;
- no company net debt at the measurement date;
- founder ownership reflects team-option or cofounder dilution;
- personal distributions are counted only after applicable company and dividend taxes;
- valuation multiples are illustrative private-company hypotheses, not promised exit prices.

| Scenario | Conservative | Expected | Strong |
|---|---:|---:|---:|
| Measurement year | Year 6 | Year 6 | Year 7 |
| Recurring customers | 80 | 180 | 500 |
| Average monthly revenue/customer | 2,400 PLN | 2,800 PLN | 3,400 PLN |
| Annual revenue | 2.304m PLN | 6.048m PLN | 20.400m PLN |
| Gross margin | 68% | 76% | 80% |
| Gross profit | 1.567m PLN | 4.596m PLN | 16.320m PLN |
| Operating margin | 12% | 27% | 32% |
| EBIT | 0.276m PLN | 1.633m PLN | 6.528m PLN |
| Initial founder capital | Up to 100k PLN | Up to 100k PLN | Up to 100k PLN |
| Later growth capital | Retained revenue | Retained revenue | Retained revenue |
| Founder ownership | 90% | 85% | 80% |
| Dilution | 10% team pool | 15% team/cofounder pool | 20% team/cofounder pool |
| External equity capital | None | None | None assumed |
| EBIT valuation multiple | 3× | 4× | 5× |
| Enterprise/equity value with zero net debt | 0.829m PLN | 6.532m PLN | 32.640m PLN |
| Founder-owned equity value | 0.747m PLN | 5.552m PLN | 26.112m PLN |
| Cumulative personal after-tax distributions | 0.020m PLN | 0.100m PLN | 1.000m PLN |
| Attributable liabilities | 0 | 0 | 0 |
| Estimated founder net worth contribution | 0.767m PLN | 5.652m PLN | 27.112m PLN |

### Interpretation

- The conservative case does not reach the 5m PLN objective.
- The expected case reaches it through 180 CEE customers, 1.63m PLN EBIT, 85% ownership, and a 4× EBIT valuation.
- The route does not require venture financing, an acquisition, or double-counting retained cash.
- The critical scale assumption is that 180 regional forwarders can be acquired at approximately 2,800 PLN monthly ARPA while maintaining 76% gross margin and 27% operating margin.

### Timing milestones — expected case

| Time | Operational milestone |
|---|---|
| Day 180 | At least one paid pilot and one completed economic-value comparison |
| Month 12 | 10 recurring customers and approximately 28k PLN MRR |
| Year 2 | 35 customers, approximately 98k PLN MRR, positive contribution economics |
| Year 3 | 75 customers, approximately 210k PLN MRR, possible full-time transition |
| Year 4 | 120 customers and a small multilingual sales/support team |
| Year 6 | 180 customers, 6.05m PLN revenue, approximately 1.63m PLN EBIT |

## Reinvestment and Compounding Model

### Conservative scenario

- While employed, 95% of after-tax business cash available for distribution is reinvested.
- Up to 5% may be distributed to the founder.
- Reinvestment funds product reliability, language coverage, and direct acquisition.
- Estimated cumulative personal after-tax distributions by year 6: 20,000 PLN.
- Founder continues employment longer because the full-time transition threshold may not be reached.

### Expected scenario

- While employed, 95% of after-tax business cash available for distribution is reinvested.
- Optional distributions remain capped at 5%.
- Reinvestment priorities are engineering, legal/security work, customer onboarding, and a part-time outbound contractor.
- Estimated cumulative personal after-tax distributions by year 6: 100,000 PLN.
- After the full-time transition, the company continues prioritizing reinvestment until the 180-customer operating model is established.

### Strong scenario

- While employed, 100% of after-tax business cash available for distribution is reinvested.
- No founder distributions occur before the full-time transition.
- After transition and establishment of 12 months of company runway, the company may distribute a minority of cash while continuing to fund CEE expansion.
- Estimated cumulative personal after-tax distributions by year 7: 1.0m PLN.
- The strong case assumes no external capital; team equity causes the modeled dilution.

## Reachability and 180-Day Paid-Proof Plan

### Proof objective

Obtain at least one 3,000 PLN paid pilot from an independent freight forwarder and demonstrate that captured or corrected commitments create measurable value exceeding the pilot fee.

### Days 1–30

- Interview public documentation and construct the freight-term ontology without contacting live prospects.
- Create 50 synthetic Polish/English/German call scenarios.
- Obtain Polish privacy and telecommunications legal advice.
- Define recording notice, retention, deletion, and data-processing options.
- Build the clickable commitment-card demonstration.

### Days 31–60

- Implement SIP call routing and post-call extraction.
- Keep the first version post-call rather than latency-sensitive.
- Implement dispatcher correction, bilingual confirmation, and PDF/CSV export.
- Test critical-term extraction on synthetic calls.
- Prepare fixed pilot terms and a data-processing agreement.

### Days 61–100

- Build the 100-account qualified list.
- Begin direct outreach.
- Demonstrate using synthetic calls only.
- Require payment before live customer-call processing.
- Avoid TMS integration; use email and CSV.

### Days 101–150

- Onboard the first paid pilot.
- Process up to 300 calls.
- Manually review every critical commercial field.
- Measure corrections, carrier response, booking rework, and dispute-prevention value.

### Days 151–180

- Produce a paid-pilot outcome report.
- Seek conversion to recurring subscription.
- Pursue a second independent paid customer.
- Release further capital only if contribution economics and repeat use are visible.

### Maximum pre-proof budget

| Item | Budget |
|---|---:|
| Contract prototype engineering | 18,000 PLN |
| Polish privacy, telecommunications, and contract review | 6,000 PLN |
| Telephony, speech, model, and translation APIs | 3,500 PLN |
| Hosting, logging, security, and backups | 3,000 PLN |
| Acquisition materials and limited travel | 2,500 PLN |
| Contingency | 5,000 PLN |
| Total | 38,000 PLN |

## Capital Tranches and Maximum Loss

| Tranche | Release condition | Incremental spend | Cumulative exposure |
|---|---|---:|---:|
| A | Synthetic prototype and legal feasibility | 15,000 PLN | 15,000 PLN |
| B | Working call flow and at least five qualified demonstrations booked | 13,000 PLN | 28,000 PLN |
| C | Signed 3,000 PLN paid pilot | 10,000 PLN | 38,000 PLN |
| D | Pilot delivered with measurable value and positive contribution margin | 32,000 PLN | 70,000 PLN |
| E | At least three independent recurring customers | 15,000 PLN | 85,000 PLN |
| F | Repeatable acquisition signal or ten recurring customers | 15,000 PLN | 100,000 PLN |

The founder’s maximum planned cash loss is 100,000 PLN. The additional potential family capital is excluded. Spending beyond 40,000 PLN is prohibited before paid proof and successful initial delivery.

## Critical Dependency Map

| Dependency | Control level | Early proof | Fallback |
|---|---|---|---|
| Forwarders will pay for commitment capture | Partly controlled | Paid pilot before full build | Kill if only free interest appears |
| Dispatchers will route calls through the product | Partly controlled | Active-use rate during pilot | Use desktop call-assist or post-call upload |
| Critical terms can be extracted accurately | Buildable | Synthetic set, then 300 reviewed calls | Human-confirmed post-call workflow |
| Carrier counterparties will confirm terms | External behavior | Confirmation-link response rate | Dispatcher-confirmed internal ledger |
| Recording and data retention are legally workable | Externally constrained | Polish legal opinion and DPA | Ephemeral transcription; retain structured events only |
| Customers will provide settlement outcomes | Contractually securable | CSV outcome export in pilot terms | Use corrections and booking outcomes first |
| TMS integrations are available | External | Not needed for paid proof | CSV, email, clipboard, and API-independent export |
| Telephony quality is reliable | Vendor-dependent | Two-provider test | Secondary SIP provider and post-call mode |
| Incumbents do not immediately bundle the wedge | Uncontrolled | Competitor monitoring and win/loss interviews | Narrow further to CEE confirmation and settlement data |
| CAC and support remain compatible with 76% GM | Partly controlled | First ten customer economics | Raise minimum price or kill service-heavy accounts |

## Full-Time Transition Gate

The founder leaves corporate employment only after all of the following are true:

- at least 25 independent recurring customers;
- no customer supplies more than 20% of MRR;
- at least 50,000 PLN MRR for three consecutive months;
- gross margin of at least 70% after telephony, model, and routine support costs;
- positive company-level contribution economics;
- at least ten customers acquired through a repeatable channel beyond personal relationships;
- observed CAC payback below six months;
- monthly gross logo churn below 2% or equivalent evidence from completed annual renewals;
- at least 12 months of personal runway held outside the company;
- legal and security practices documented for live customer-call processing;
- a contractor or employee can handle routine support without the founder being continuously available.

## Failure Recovery and Reusable Assets

If the product fails commercially, the following assets remain reusable subject to customer contracts:

- multilingual freight-commercial-term ontology;
- synthetic and permissioned call-evaluation set;
- extraction and contradiction benchmark;
- bilingual commitment-card interface;
- SIP and post-call processing stack;
- privacy, retention, and DPA templates;
- booking and invoice reconciliation schema;
- anonymized correction and outcome data;
- list of qualified CEE forwarding accounts;
- observed objections, workflow maps, and pricing evidence.

Possible recovery routes include licensing the freight ontology and evaluation harness to a TMS or voice-AI vendor, or narrowing to post-call QA and invoice reconciliation for existing paying customers. Neither recovery route is assumed to have standalone value before evidence exists.

## Critical Evidence

1. HappyRobot reports that Circle Logistics used AI voice agents across 200,000 carrier calls and describes freight brokerage as a phone-heavy workflow involving negotiation, booking confirmation, and compliance checks. The performance figures are vendor case-study claims rather than independent research.
2. HappyRobot’s DHL case describes carrier ETA calls, customs-duty collection, invoice follow-up, and TMS updates, demonstrating that logistics-call outputs can be operationally structured.
3. FleetWorks states that its AI calls brokers and negotiates on behalf of carriers, confirming active competition in freight voice automation.
4. Transporeon provides electronic freight offers, acceptance notifications, and automated assignment, confirming that structured commitment is already accepted inside digital freight workflows.
5. The European Commission states that eFTI will require authorities to accept freight information from certified digital platforms when the regulation applies fully on 9 July 2027.

## Critical Hypotheses

- Human-negotiated carrier calls will remain economically important despite autonomous voice agents and digital freight marketplaces.
- A regional forwarder experiences at least several thousand PLN per month of preventable commitment leakage or rework.
- Buyers will pay approximately 2,800 PLN per month for an independent overlay.
- Dispatchers will tolerate routing or assistive software if it reduces typing.
- Counterparties will confirm enough commitments to create additional value.
- Customers can contractually provide correction, booking, and settlement outcomes.
- Polish and CEE freight-language specialization materially improves acquisition or performance.
- Critical-term extraction can exceed 97% precision and recall after human confirmation and domain tuning.
- Direct CAC can fall below 7,000 PLN.
- Support requirements will not turn the product into custom integration consulting.
- 180 paying CEE forwarders are reachable without heroic market share.
- A 4× normalized EBIT valuation is achievable for a profitable, recurring software business with low churn.
- The commitment-to-settlement graph compounds faster than TMS and voice-AI incumbents can reproduce it.

## Kill Criteria

Kill or materially change the business shape if any of the following occurs:

- no paid pilot after 100 qualified approaches and at least 15 completed demonstrations by day 150;
- legal advice concludes that the required call processing or outcome retention creates prohibitive consent or compliance friction;
- fewer than 50% of pilot dispatchers remain weekly active after four weeks;
- critical commercial-term precision or recall remains below 97% after 300 reviewed calls;
- more than 10% of calls require material manual reconstruction rather than quick confirmation;
- carrier confirmation is below 35% and the internal dispatcher ledger alone does not create measurable value;
- the pilot does not prevent or recover value equal to at least twice its fee;
- customers refuse contractual rights to retain anonymized correction and outcome data;
- expected mature gross margin falls below 65%;
- fully loaded CAC payback remains above 12 months after the first ten recurring customers;
- more than half of pilot delivery effort is customer-specific integration or manual analysis;
- a dominant TMS or freight voice-AI vendor bundles an equivalent CEE human-call commitment workflow before CarrierPromise secures ten recurring customers;
- the expected path to 180 customers requires enterprise partnerships, venture capital, or founder labor scaling approximately one-for-one with revenue.

## Budget, Time, and Minimum People Stack

### Time

- Founder: 20–25 hours per week, capped at five hours per day.
- Contract engineer: 10–15 hours per week during prototype and pilot.
- Freight-domain reviewer: approximately five hours per week during ontology design and first pilots.
- Legal specialist: 12–20 total hours initially.
- Part-time sales contractor only after paid proof and positive contribution economics.

### Minimum people stack

1. Founder: product, data, customer discovery, analytics, and commercial ownership.
2. Contract full-stack/telephony engineer.
3. Polish privacy and telecommunications lawyer.
4. Part-time freight dispatcher or forwarding-operations specialist.
5. Later, a part-time outbound and onboarding contractor funded from revenue.

### Total first-year capital ceiling

| Use | Maximum |
|---|---:|
| First 180-day proof | 38,000 PLN |
| Reliability, security, and basic integrations after paid proof | 32,000 PLN |
| Language expansion and support after recurring customers | 15,000 PLN |
| Repeatable acquisition after channel evidence | 15,000 PLN |
| Total | 100,000 PLN |

## Research Sources

- [HappyRobot — Circle Logistics customer story](https://www.happyrobot.ai/customer-story/circle)
- [HappyRobot — DHL customer story](https://www.happyrobot.ai/customer-story/dhl)
- [HappyRobot — Logistics providers](https://www.happyrobot.ai/solutions/industries/logistics-providers)
- [FleetWorks — AI-powered freight automation](https://www.fleetworks.ai/)
- [Transporeon — Transport Assignment](https://www.transporeon.com/en/platform/transport-execution-visibility-hub/carrier-lsp/transport-assignment)
- [Transporeon — Autonomous Procurement](https://www.transporeon.com/en/platform/freight-marketplace/shipper/autonomous-procurement)
- [European Commission — eFTI Regulation](https://transport.ec.europa.eu/transport-themes/logistics-and-multimodal-transport/efti-regulation_en)
- [EUR-Lex — Regulation (EU) 2020/1056 on electronic freight transport information](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32020R1056)
