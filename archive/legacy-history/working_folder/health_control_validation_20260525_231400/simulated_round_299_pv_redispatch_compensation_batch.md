# Simulated Round 299: PV Redispatch Compensation Batch Desk

Date: 2026-05-31 Europe/Warsaw

Gate policy:

- Simulated score must be strictly greater than 87 before real Zero To One validation.
- Working-chat and fresh-chat Zero To One gates are both >=85.
- Internal scoring caps are used only in this simulation note, not in the validation prompt.

## Why This Branch

The KSeF/payment-release branch produced repeated working-chat passes and fresh-chat failures. The fresh failure pattern was consistent: the evaluator saw KSeF cases as transition-wave admin with too many filters and nearby incumbents.

This round moves to a different hard-cash rail: PSE non-market redispatch compensation for PV installations. It has current official events, published application mechanics, and a claim/payment object that an owner can authorize inside 60 days.

Official/current source check:

- PSE announced that PV owners whose installations executed reduction orders on 20, 21, and 22 February 2026 generally have a right to financial compensation, and it points to PSE calculation rules and current application forms.
- PSE's PV page says the recommended submission route is the WOZE portal, gives an emergency email route, and explicitly allows entities handling many applicants to send many compensation applications covering many applicants and dates until bulk WOZE functionality is implemented.
- PSE's PV page lists many 2026 PV non-market redispatch notices, including repeated dates in May 2026.

Sources:

- `https://www.pse.pl/-/komunikat-dotyczacy-prawa-do-rekompensaty-za-redysponowanie-nierynkowe-instalacji-fotowoltaicznych-w-dniach-20-21-i-22-lutego-2026`
- `https://www.pse.pl/instalacje-pv`

## Raw Candidate Control Table

| # | Candidate | Buyer / payer | Acute trigger | Transferable control point | 60-day signed/titled/assigned/prepaid proof | First acquisition mechanism | Gross margin and payback logic | Copy risk | Why incumbents cannot copy before control | Why not service/report/app/dashboard/marketplace/broker |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | PV redispatch compensation batch desk | PV farm SPVs, small portfolio owners, O&M/accounting admins | PSE non-market redispatch days create compensation applications | Owner authorization, WOZE/application file, SCADA/meter data, submitted WoR acknowledgements | 6 signed mandates, 20 applications, 2 PSE/portal acknowledgements, first invoice | Target 2-20 MW PV owners and O&M/accounting firms seeing many May/June events | 4k-12k PLN setup plus 6-12% success fee; high margin after reviewer | O&M, asset managers, energy lawyers, accountants | Once owner authorizes a named installation/date batch and data export, the exact claim file is locked | Current cash-claim batch, not advice or software |
| 2 | Wind redispatch compensation queue | Wind-farm owners | PSE wind curtailment events | Owner mandate and production baseline workpaper | 3 mandates, 8 applications | Renewable asset managers | Larger tickets but fewer events | O&M/energy consultants | Exact turbine/date data controlled | Claim file |
| 3 | OSD-connected PV curtailment compensation packet | Smaller PV connected to distribution grids | DSO/PSE reduction orders | Generator mandate and DSO event evidence | 8 mandates, 20 event files | Local PV operators | Medium ticket, higher admin | O&M/accountants | Named events and portal access controlled | Claim prep |
| 4 | PPA negative-price curtailment settlement review | C&I PV owners | Offtaker settlement deducts negative-price/curtailment amounts | PPA settlement file and mandate | 5 live settlements | Energy brokers | Good if cash withheld | Lawyers/offtakers | Exact PPA and settlement controlled | Cash settlement challenge |
| 5 | Guarantee-of-origin missing-issuance recovery | RES producers | GOs not issued or sold because metering/account data missing | Registry/account mandate | 6 live GO batches | GO traders | Medium margin | GO brokers | Exact registry account controlled | Issuance recovery |
| 6 | Green certificate legacy settlement cleanup | Older RES generators | certificate obligation/settlement mismatch | URE/TGE account and invoice evidence | 3 mandates | Energy accountants | Niche | Specialists | Exact account controlled | Settlement cleanup |
| 7 | Capacity-market availability penalty evidence file | DSR/units | Penalty or withheld capacity payment | Certified unit data and operator file | 3 active cases | DSR aggregators | High but specialist | Aggregators/lawyers | Exact unit file controlled | Too legal/technical |
| 8 | DSR event settlement release | DSR aggregators and large sites | Event performance payment disputed | Metering/event data and aggregator acknowledgement | 5 sites | DSR providers | Good if payment pending | Aggregators internalize | Exact event file controlled | Cash settlement |
| 9 | Balancing-market invoice exception desk | small balancing responsible parties | imbalance invoice mismatch | settlement data and mandate | 4 cases | energy traders | High expertise | BRP incumbents | exact settlement data | Too specialist |
| 10 | Renewable auction support underpayment workpaper | auction-supported RES SPVs | monthly support settlement mismatch | auction support statements and mandate | 4 cases | RES accountants | Medium | advisors | exact SPV data | Cash correction |
| 11 | Prosumer net-billing correction batch | prosumer aggregators | miscalculated deposit/value of energy | customer authorization | 30 cases | PV installers | Low ticket | utilities/installers | customer cases controlled | Consumer admin |
| 12 | Commercial reactive-energy charge correction | factories/warehouses | reactive-energy penalties after compensation fault | invoice/meter data and DSO complaint | 8 mandates | energy auditors | Medium | energy consultants | exact meter/invoice controlled | Recovery claim |
| 13 | DSO connection-fee refund desk | C&I energy users | connection project cancelled/reduced | DSO agreement and payment evidence | 3 cases | electrical designers | Good but slow | lawyers/designers | exact agreement controlled | Refund file |
| 14 | Metering data gap invoice release | RES/industrial sites | invoice or settlement delayed by missing meter data | supplier/DSO query and meter logs | 8 cases | energy accountants | Medium | suppliers | exact query controlled | Payment release |
| 15 | Heat tariff overcharge recovery | district-heating commercial users | tariff/meter class mismatch | invoices and building data | 8 cases | facility managers | Medium | energy auditors | exact building account | Audit recovery |
| 16 | Power-factor compensation warranty payment release | installers | buyer withholds payment until penalties fall | DSO invoices before/after and buyer acceptance | 5 jobs | installer channels | Good but hardware/remediation | electrical firms | exact buyer payment hold | Payment-release proof |
| 17 | Rooftop PV grid-trip loss claim pack | C&I PV owners | inverter trips from grid parameters and production loss | SCADA logs and DSO complaint | 5 cases | PV O&M firms | Medium | O&M/lawyers | exact logs controlled | Claim/evidence |
| 18 | RfG settings acceptance pack | small generators | DSO acceptance delayed by settings/evidence | installer/DSO checklist | 6 cases | installers | Medium | installers | exact project controlled | Technical acceptance |
| 19 | CSIRE migration defect cash release | energy suppliers/ESCOs | customer switch/billing blocked by CSIRE data migration | defect ticket and billing hold | 6 cases | energy suppliers | Timely but enterprise | IT vendors | exact defect controlled | Too software/process |
| 20 | OIRE/CSIRE supplier onboarding ticket book | market participants | access/test defect blocks go-live | participant authorization and test ticket | 5 cases | energy IT firms | Good but incumbents | IT vendors | exact account controlled | Platform ticket |
| 21 | Energy broker commission release from supplier | brokers | commissions withheld due customer-switch evidence | customer/supplier ledger | 6 mandates | broker groups | Medium | brokers internalize | exact commission ledger | Cash recovery |
| 22 | Heat pump subsidy reimbursement release | installers/customers | grant reimbursement delayed | application and install evidence | 12 cases | installers | Lower ticket | grant admins | exact applications | Grant admin |
| 23 | EV charger AFIR tender claim release | CPO/installers | tender/payment held by accessibility/payment evidence | tender file and commissioning proof | 4 cases | EV installers | Medium | consultants | exact project | Evidence too generic |
| 24 | EV charge roaming settlement recovery | CPOs/eMSPs | roaming invoices/OCPI settlement mismatch | CDRs and contracts | 5 cases | CPOs | Good but data-heavy | platforms/consultants | exact CDR data | Cash settlement |
| 25 | Solar inverter warranty batch reimbursement | O&M firms | OEM service credits missing for serials | warranty portal and serial claim | 8 cases | O&M firms | Medium | distributors | exact serials | Warranty recovery |
| 26 | Tracker underperformance warranty claim queue | PV owners | tracker fault creates liquidated damages/warranty claim | SCADA/event logs and warranty file | 3 cases | O&M/owners | High but technical/legal | O&M/lawyers | exact asset data | Too technical |
| 27 | Curtailment insurance parametric claim pack | RES owners | policy pays for named curtailment/loss event | policy and event data | 3 cases | brokers | High but insurance | brokers/lawyers | exact policy | Claims-handling risk |
| 28 | Corporate PPA REC/GO delivery true-up | corporate buyers/sellers | GO/REC delivery shortfall blocks annual settlement | PPA and registry data | 4 cases | PPA brokers | Good but lawyer-adjacent | brokers | exact contract | Settlement file |
| 29 | Battery dispatch revenue allocation correction | BESS co-owners | aggregator settlement mismatch | telemetry and contract | 3 cases | BESS owners | High but immature | aggregators | exact telemetry | Complex finance |
| 30 | Ancillary-service qualification evidence pack | BESS/DSR operators | payment/qualification blocked by test data | test report and operator query | 4 cases | aggregators | Good but specialist | aggregators | exact test controlled | Too technical |
| 31 | Offshore-wind supplier milestone evidence release | suppliers | milestone payment blocked by document trail | contract milestone and buyer request | 4 cases | suppliers | High but enterprise | EPC/admin | exact milestone | Generic payment evidence |
| 32 | Grid-connection deposit release mandate | developers | project cancelled, deposit/refund pending | connection agreement and release request | 5 cases | developers | Medium | lawyers/designers | exact agreement | Refund admin |
| 33 | Land-lease indexation true-up collection | RES land lessors | rent indexation unpaid | lease and payment direction | 6 cases | landowner networks | Medium | lawyers/accountants | exact lease | Small collections |
| 34 | EPC retention release for PV farms | EPC subcontractors | retention due after acceptance | acceptance/protocol and debtor acknowledgement | 4 cases | EPC subs | Good but construction incumbents | lawyers/PMs | exact retention | Already failed retention-like |
| 35 | Transformer oil test warranty release | operators | warranty/acceptance delayed by lab oil report | lab result and commissioning file | 5 cases | electrical contractors | Medium | labs/OEMs | exact transformer | Evidence-only |
| 36 | Curtailment tax/accounting memo for SPVs | PV owners | accounting treatment blocks booking compensation | accounting file | 5 cases | accountants | Low | accountants | exact SPV | Report, not hard cash |

## Finalists

| Candidate | Internal simulated score | Advance? | Rationale |
|---|---:|---|---|
| PV redispatch compensation batch desk | **88.6** | **Yes** | Current official cash rail, repeated 2026 events, published application forms, bulk-submission allowance, and owner-authorized claim batches. Stronger than generic energy consulting because the first proof is submitted compensation applications and portal/PSE acknowledgements. |
| Wind redispatch compensation queue | 86.4 | No | Same logic but fewer accessible cases and more institutional owners. |
| PPA negative-price curtailment settlement review | 84.5 | No | Real cash but contract interpretation and off-taker dispute risk make it lawyer-heavy. |
| Reactive-energy charge correction | 83.8 | No | Cash recovery but energy-audit incumbents and commodity audit dynamics cap it. |
| EV charge roaming settlement recovery | 83.2 | No | Cash claim but CDR/platform data and incumbent CPO/eMSP operations weaken founder control. |
| Solar inverter warranty reimbursement | 82.9 | No | Serial cash recovery but warranty portals and distributors can internalize. |

## Lead Candidate

Idea name: **ReDispatchCash PV Compensation Batch Desk**

### Buyer

Polish PV farm SPVs, small RES portfolio owners, and O&M/accounting administrators managing 1-20 MW PV installations affected by PSE non-market redispatch orders.

### Acute Trigger

PSE publishes a non-market redispatch notice for PV installations, the owner has curtailment/reduction events in its SCADA/meter/operator records, and the owner needs to submit compensation applications through WOZE or the PSE emergency/bulk route before the work becomes a delayed receivable.

### Control Point

The startup only controls a case when it has:

- signed owner or authorized manager mandate for named installations and event dates;
- WOZE/application access path or application-signing route;
- SCADA/export/meter data, installed-capacity data, owner and SPV details, PSE/OSD instruction evidence, and bank/tax invoicing details supplied by the claimant;
- fixed prepaid batch fee and success-fee entitlement;
- energy-settlement reviewer attached for calculation boundary checks;
- strict boundary that the owner remains claimant and legal/tax decision-maker.

### 60-Day Proof

- Six signed claimant mandates across at least three PV owners or O&M/accounting administrators.
- Twenty named installation/date compensation applications assembled.
- Ten applications submitted through WOZE or accepted emergency/bulk route.
- Two PSE/WOZE acknowledgements, accepted import confirmations, deficiency notices narrowed to owner data, or payment-progress outcomes.
- 40,000-90,000 PLN collected from setup fees plus documented success-fee receivables.
- One energy-settlement reviewer on paid per-case terms.

### Economics

Pricing:

- 3,000-5,000 PLN triage for one owner/installation group and event-date eligibility map.
- 6,000-12,000 PLN prepaid batch setup for up to 10 installation/date applications.
- 600-1,200 PLN per additional installation/date application.
- 6-12% success fee on collected compensation, capped or declining for larger portfolios.

The owner pays because compensation is current cash linked to official curtailment events. O&M/accounting administrators pay or resell because repeated event dates and many SPVs create a batch workload that is too operational for lawyers and too specific for generic accountants.

### Copy Risk

O&M firms, asset managers, energy lawyers, RES accountants, and larger portfolio owners can copy the workflow. The defense is not legal exclusivity; it is fast batch operation over named events, reusable installation/date workpapers, WOZE application memory, no-go patterns, reviewer checklists, and signed mandates over the current compensation queue.

### Internal Score

Simulated score: **88.6 / 100**

Reasoning:

- Acute current cash: strong. PSE notices, current 2026 event dates, published application route, and owner compensation rights make this more concrete than most evidence desks.
- Control point: reasonably hard. Mandate plus named installation/date data plus submitted applications is a real claim queue.
- CAC/payback: plausible through O&M/accounting/asset-manager channels and public PSE notice timing.
- Margin: strong if cases are batched and reviewer use is bounded.
- Copy risk: meaningful but not fatal because many incumbents either serve larger portfolios or do not want bulk admin for smaller SPVs.
- Main cap: energy-law/accounting boundary, O&M incumbents, uncertain PSE timing, and dependence on owner data quality.

### Kill Criteria

- Fewer than six signed mandates in 60 days.
- Fewer than ten submitted applications.
- More than 35% of accepted cases collapse because owner data is missing or legal/technical eligibility is disputed.
- No PSE/WOZE acknowledgement, deficiency narrowing, or payment-progress outcome.
- Gross margin below 55% after reviewer and data-cleanup costs.
- Scope drifts into legal opinions, market-price disputes, grid-code claims, tax advice, or engineering reconstruction of missing SCADA/meter truth.

## Validation Decision

Advance Round 299 to real working-chat Zero To One validation because the simulated score is strictly greater than 87 and the candidate is materially different from exhausted KSeF, AR true-up, evidence-desk, physical-lot, and generic recovery branches.
