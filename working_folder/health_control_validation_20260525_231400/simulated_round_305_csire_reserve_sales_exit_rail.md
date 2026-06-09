# Simulated Round 305 - CSIRE Reserve-Sales Exit Rail

Date: 2026-05-31 Europe/Warsaw

Current real validation gates: working Zero To One >=85; fresh Zero To One >=85. Internal simulation gate: only validate if simulated score is strictly >87.

## External Timing Check

Official sources support the timing and operational trigger:

- Poland's Ministry of Climate and Environment says CSIRE started on 1 July 2025, smaller DSOs and related sellers can join on 1 July 2025, 1 March 2026, or 1 July 2026, and larger/non-early entities join by the final date of 19 October 2026. It also says CSIRE is meant to keep retail electricity-market service uninterrupted after launch. Source: https://www.gov.pl/web/klimat/zmiany-w-zwiazku-z-wprowadzaniem-centralnego-systemu-informacji-rynku-energii
- URE says CSIRE gathers commercial and technical data needed for retail electricity-market processes including supplier switching and settlement. It also identifies entities authorised by system users to access energy-market data as CSIRE participants. Source: https://www.ure.gov.pl/pl/urzad/informacje-ogolne/aktualnosci/11758,Prezes-URE-przypomina-przedsiebiorstwom-energetycznym-o-obowiazku-zawierania-tzw.html
- URE's English reserve-sales explainer says CSIRE went online on 1 July 2025, rollout is planned to end on 19 October 2026, and reserve electricity sale can be much more expensive than regular market offers, with a statutory cap of triple the last quarterly competitive-market price. Source: https://www.ure.gov.pl/en/communication/news/451,Consumers-Knowledge-Regulated-The-terms-and-conditions-of-reserve-electricity-sa.html

## Raw Candidate Table

| # | Candidate | Buyer | Acute trigger | Transferable control point inside 60 days | First acquisition | Economics | Copy risk / cap |
|---:|---|---|---|---|---|---|---|
| 1 | CSIRE reserve-sales exit rail | Energy brokers and multi-site C&I customers | Customer is on reserve/default electricity sale or switch failed during CSIRE rollout | Signed customer authorisation, PPE list, reserve-sale notice, CSIRE/switch-status evidence, new supplier offer pack, accepted switch submission | Energy brokers with frustrated customers | 2k-12k PLN per site cluster plus broker share/success fee | Brokers can copy, but signed customer files and CSIRE error memory are concrete |
| 2 | CSIRE C&I consumption data tender pack | Energy procurement brokers | Supplier offers blocked by missing verified PPE/consumption data | Customer authorisation, meter/PPE export, tender pack, supplier acknowledgement | Brokers and outsourced energy buyers | 3k-15k PLN per portfolio | Less acute than reserve-sale exit |
| 3 | CSIRE PPE mismatch correction queue | Energy sellers and brokers | Switch/application rejected due PPE/customer/meter mismatch | Signed correction mandate, rejection code, DSO/OIRE trail, accepted correction | Broker support queues | 500-2k PLN/PPE | Can become ticket chasing |
| 4 | Reserve-sales bill overcharge review | C&I customers | Unexpected reserve-sale bills after seller termination/switch failure | Invoice/notice pack, new supplier route, no-go or correction request | Energy accountants | 15-25% recovered/avoided | Too much energy-law/billing interpretation |
| 5 | District heating final-account refund release | Closed sites | Deposit/final account balance stuck | Account authority, supplier acknowledgement, refund instruction | Property accountants | 10-20% recovered | Similar to failed utility deposits |
| 6 | Water/sewer industrial tariff correction | Food/industrial plants | Wrong tariff category or meter factor on current invoices | Site data, supplier claim, first credit | Utility auditors | 20% first-year saving | Consultants and utilities copy |
| 7 | Reactive power penalty cure evidence | Plants and facility managers | Large reactive energy penalty after capacitor installation | Before/after invoices, measurement evidence, DSO acknowledgement | Electrical contractors | 15% of avoided penalties | Energy consultants/electricians own |
| 8 | Capacity-market DSR settlement exception desk | Aggregators | Missing meter/baseline evidence blocks settlement | Site mandate, meter files, aggregator acceptance | Aggregators | Per-site fee | Aggregators internalize |
| 9 | Aggregator DSR site paid option | Aggregators | Need new accepted flexibility sites | Signed site option, meter data, preliminary acceptance | Cold site outreach | Bounty | Failed FlexMW-like lead-gen risk |
| 10 | PPA invoice settlement discrepancy rail | Corporate buyers | Renewable PPA invoices do not match meter/GoO data | Buyer mandate, invoice/data room, corrected invoice | Energy brokers | Fixed + credit share | Incumbent energy advisers |
| 11 | PPA guarantee-of-origin delivery release | Corporates | Sustainability claim/payment blocked by GoO delivery mismatch | Registry serials, delivery statement, invoice acceptance | ESG/energy advisers | 5k-20k PLN | ESG incumbents, claim risk |
| 12 | Balancing-cost pass-through credit recovery | C&I customers | Seller passes through balancing charges incorrectly | Contract/invoice claim, seller acknowledgement | Energy CFOs | 15-25% credit | Legal/contract interpretation |
| 13 | TSO/DSO curtailment compensation batch | RES owners | Non-market redispatch or grid instruction created claim | Mandate, meter data, application acknowledgement | O&M firms | Batch fee | Fresh failed adjacent PV compensation |
| 14 | Heat-pump subsidy ZUM payout release | Installers | Grant payout blocked by product/evidence mismatch | Customer mandate, ZUM/product pack, grant correction | Installers | Fixed per case | Public subsidy/admin incumbents |
| 15 | Clean-air program contractor reimbursement rail | Retrofit contractors | Subsidy tranches stuck on attachment mismatch | Customer mandate, attachment pack, portal status | Contractors | Fixed + success | Public docs and advisers |
| 16 | Public lighting EPREL correction pack | Lighting distributors | Tender/product evidence mismatch | SKU/EPREL bid pack | Distributors | 2k-8k PLN | Too close to GreenTender |
| 17 | Tyre EPREL tender evidence pack | Tyre wholesalers | Fleet/public tender asks tyre-label/EPREL proof | SKU/EPREL/tender matrix | Tyre distributors | 2k-7k PLN | GreenTender-like duplicate, lower urgency |
| 18 | HVAC refrigerant F-gas quota release | Importers | Shipment blocked by authorisation/quota issue | Shipment mandate, tCO2e file, portal path | Brokers | 10k-50k PLN | Failed F-gas-like |
| 19 | EUDR downstream registration pack | Wood/furniture traders | Buyer asks registration/reference proof | Buyer request, role map, evidence pack | Export advisers | 5k-20k PLN | EUDR timing weak, legal source-data risk |
| 20 | Battery passport buyer-release lane | E-bike/battery importers | Retailer asks DPP/Battery Regulation evidence | SKU data, responsibility map, buyer response | Compliance agencies | 8k-30k PLN | Too early and TIC incumbents |
| 21 | CRA product-security buyer unblock | Connected-device makers | Buyer asks CRA vulnerability-process proof | Buyer request, secure process pack | Embedded consultants | 10k-35k PLN | Failed CRA/cyber trust pattern |
| 22 | App store tax/KYC payout release | Indie game studios | Platform payout held for tax/KYC/bank mismatch | Platform case, tax/bank packet, payout | Game accountants | 10-20% payout | Sensitive, platforms/accountants |
| 23 | Cloud marketplace tax form payout release | SaaS vendors | AWS/Azure/Google payout hold | Marketplace case, W-8/VAT/bank docs | Marketplace advisers | Fixed + success | Prior cloud marketplace failures |
| 24 | POS acquirer reserve release | Merchants | Reserve/rolling hold not released | Acquirer notice, mandate, release proof | PSP consultants | Success fee | PSP reserve branch failed |
| 25 | Card-scheme chargeback evidence retainer | B2B SaaS merchants | Dispute ratios or high-value disputes | Case file, representment packet, first win | PSP agencies | 10-25% recovered | Incumbents/fraud sensitivity |
| 26 | Marketplace KYB disbursement release | Sellers | Payout blocked by KYB/beneficial-owner mismatch | Seller mandate, platform case, release | Ecommerce accountants | 2k-10k PLN | Marketplace KYBC failed |
| 27 | ERP-to-KSeF attachment release | Utilities/telcos/fuel | Complex invoice attachments block issue/payment | e-US attachment notice, first accepted invoice batch | ERP integrators | 20k-80k PLN | KSeF branch exhausted |
| 28 | Factor KSeF eligibility no-go desk | Factoring brokers | Funding held on KSeF/AP evidence | Factor hold, seller mandate, release/no-go | Factoring brokers | 15k-40k PLN | Fresh failures make branch exhausted |
| 29 | Supplier portal approved invoice release | Industrial suppliers | Approved invoices stuck in portal due vendor-master data | Portal status, buyer AP acknowledgement, payment direction | CFOs | Fixed + success | Ordinary AP chasing |
| 30 | Tenant fit-out allowance closeout | Retail tenants | Landlord allowance due but unpaid | Lease clause, landlord packet, payment status | Tenant reps | 10-20% | Failed at 80 |
| 31 | Public guarantee release line | Contractors | Bank guarantee/deposit remains after acceptance | Guarantee file, beneficiary route, release | Surety brokers | Fixed + success | Failed at 76 |
| 32 | Pallet pool cash direction | FMCG distributors | Deposit/returnable-asset balance unresolved | Account-period ledger, debtor acknowledgement | Logistics CFOs | Success fee | Failed at 75 |
| 33 | 3PL overbilling recovery | Ecommerce brands | Storage/pick-pack invoices mismatch WMS | Mandate, invoice/WMS claim, credit memo | Ops consultants | 20% recovery | Failed at 71 |
| 34 | Freight D&D credit mandate | Importers | Demurrage/detention/accessorial overbilled | Invoice/BOL/free-time claim, carrier case | Freight accountants | 20% credit | Freight audit incumbents |
| 35 | Building BMS final payment data room | Integrators | Retention blocked by commissioning evidence | Site data, owner acceptance, payment | BMS contractors | Fixed fee | Technical rework/acceptance risk |
| 36 | Fire-alarm test-book continuity buyout | Retiring technicians | Recurring mandatory tests/invoices transfer | Customer consents, schedule, first cash | Technicians | MRR | Licensed-provider/service-book cap |

## Finalists

| Finalist | Control strength | Why it advanced or failed |
|---|---|---|
| CSIRE Reserve-Sales Exit Rail | Signed customer authorisation, PPE/notice/current-bill evidence, broker routing, switch submission, first completed switch or accepted no-go | Best mix of current official rollout, high current bill pain, direct economic outcome, and repeat broker channel. |
| CSIRE C&I Consumption Data Tender Pack | Customer authorisation and meter/PPE data for supplier tender | Useful but weaker because offer-quality pain is less acute than active reserve-sale/default-supply pain. |
| CSIRE PPE Mismatch Correction Queue | Exact rejected switch/correction queue | Concrete but likely low-value ticket chasing unless attached to reserve-sale or large portfolio cases. |
| Freight D&D Credit Mandate | Existing carrier invoices/claims | Higher values, but freight-audit incumbents and legal/accessorial interpretation cap it. |
| PPA GoO Delivery Release | Registry serial/payment-release artifact | Too ESG/adviser-heavy and claim-sensitive. |
| BMS Final Payment Data Room | Current cash release | Too often real technical commissioning/rework rather than evidence. |

## Internal Cap Check

- The candidate has concrete 6-month control proof: signed energy-broker routing agreement, customer authorisations, named PPE/site clusters, reserve-sale notices or switch rejection trail, offer/switch submission evidence, and first completed switch/accepted no-go.
- It is stronger than a consultant/report because the first proof is a completed market-process event that changes a customer's electricity seller or documents why it cannot be changed.
- Copy risk is real: energy brokers, sellers, and large advisers can internalise the process. The score stays below the very strongest confirmed ideas for that reason.
- Cash conversion is plausible because customers on reserve electricity supply face current bill pain and brokers have commission at stake.
- Legal/provider boundaries are manageable if the startup does not recommend tariffs, act as seller, provide legal advice, represent the customer before URE, or promise savings.
- Transition risk is real: CSIRE rollout may normalize after October 2026. The durable asset must be broker workflow lock-in and a PPE/switch-error memory library, not a one-time setup guide.

## Simulation Verdict

**Advance: CSIRE Reserve-Sales Exit Rail**

Simulated score: **88.0 / 100**

Rationale: This is not as clean as DORA or HeritageDoor, but it is stronger than the recent public-compensation and generic recovery failures because the economic trigger is live reserve/default electricity supply, the customer authorisation is a real control artifact, and the first output is a completed supplier-switch/switch-status event rather than a memo. The main risk is that energy brokers and sellers absorb the workflow after the rollout; validation should test whether Zero To One sees the broker-routed repeat queue as enough.
