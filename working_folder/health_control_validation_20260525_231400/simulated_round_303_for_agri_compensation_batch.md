# Simulated Round 303: FOR Agri Compensation Batch Desk

Date: 2026-05-31 Europe/Warsaw

Real gates: working Zero To One >=85 and fresh Zero To One >=85.
Simulation gate: advance only if simulated score is strictly above 87.

Internal scoring caps are applied here only. They are not included in the Zero To One prompt.

## Search Frame

Round 302 failed because the buyer gate was technical installer acceptance. Round 303 tests a neutral official compensation queue with current cash: Poland's Fundusz Ochrony Rolnictwa compensation for agricultural producers and producer groups that sold agricultural products to an insolvent buyer and were not paid.

The May 2026 rule change adds a second annual application window and simplifies part of the process. The candidate only works as a group/batch desk for producer groups, cooperatives, and clusters with many unpaid invoices from one insolvent buyer. It is not individual farmer grant consulting, debt collection, litigation, insolvency claims, tax advice, or general AR recovery.

Current source check:

- Ministry of Agriculture, 18 May 2026: the new rules have applied since 13 May 2026 and applications can be filed twice a year, 1 February-31 March and 1 July-31 August.
- The same notice says compensation is for agricultural producers and producer groups that were not paid for sold agricultural products by an insolvent entity conducting purchase, storage, treatment, or processing of agricultural products.
- KOWR announced the 2026 FOR application intake earlier in 2026.

Sources:

- https://www.gov.pl/web/rolnictwo/nowe-terminy-skladania-wnioskow-o-rekompensaty-z-funduszu-ochrony-rolnictwa
- https://www.gov.pl/web/kowr/rusza-nabor-wnioskow-w-ramach-for

## Raw Candidate Control Table

| # | Candidate | Buyer/payor | Acute trigger | Transferable control point | 60-day signed/titled/assigned/prepaid proof | First acquisition | Economics/payback | Copy risk | Why incumbents cannot copy before control | Why not service/report/app/broker | Internal score |
|---:|---|---|---|---|---|---|---|---|---|---|---:|
| 1 | FOR agri compensation batch desk | producer groups/co-ops/unpaid producers | insolvent buyer left unpaid agricultural invoices; July-August window | signed group mandate, invoice/delivery files, insolvency basis, KOWR/FOR application tracker, accepted claims | 3 group mandates, 80 producer/invoice files, 30 submissions, 2 accepted/status outcomes | producer groups, co-ops, agri accountants | batch fee plus small success fee | agri advisors/accountants | exact buyer/event/group claim file controlled | compensation batch operation | 88.1 |
| 2 | Individual farmer FOR application helper | unpaid farmers | missed window | application docs | submissions | farm outreach | low | public help/advisors | none | form filling | 55 |
| 3 | Insolvent buyer debt collection | farmers | unpaid invoices | legal claim | claim filed | lawyers | success | lawyers | legal | legal recovery | 40 |
| 4 | Agricultural direct payment application desk | farmers | annual ARiMR payments | crop/land docs | application | advisors | low | many advisors | none | grant form | 45 |
| 5 | Organic/eco subsidy correction | farmers | rejected payment | ARiMR file | correction | advisors | low | advisors | exact file | public grant | 55 |
| 6 | Agri insurance claim batch | farmers | hail/frost loss | insurer claim | payout | brokers | fee | insurers/brokers | exact claim | insurance | 52 |
| 7 | Grain buyer payment assignment | farmers | buyer slow-pays | receivable assignment | payment | factors | finance | legal/factors | exact receivable | finance | 58 |
| 8 | Milk co-op quality deduction recovery | dairy farms | co-op deductions | lab/settlement files | credit | farm accountants | success | co-ops/advisors | exact batch | dispute | 62 |
| 9 | Slaughterhouse weight/class settlement recovery | livestock producers | carcass settlement disputed | weight/class docs | credit | agri advisors | success | buyers/lawyers | exact claim | dispute | 60 |
| 10 | Fertilizer subsidy claim desk | farms | subsidy window | invoices/docs | application | advisors | low | advisors | none | public grant | 50 |
| 11 | Drought aid application batch | farmers | disaster payment | yield/land docs | application | advisors | low | public advisors | none | public aid | 48 |
| 12 | CAP eco-scheme evidence rescue | farms | rejected eco-scheme | evidence file | correction | advisors | fee | advisors | exact file | advisory | 56 |
| 13 | Producer group unpaid-buyer evidence room | co-ops | buyer insolvency | shared evidence room | member files | co-ops | fee | accountants | exact group event | subset of lead | 84 |
| 14 | Agri storage warehouse receipt recovery | farmers | warehouse failure | warehouse receipts | claim | lawyers | success | legal | exact receipt | legal/insolvency | 58 |
| 15 | Fruit/vegetable processor unpaid invoice batch | producer groups | processor insolvency | invoices/delivery docs | FOR filings | groups | batch fee | advisors | exact processor event | subcase | 86 |
| 16 | Milk processor unpaid invoice batch | dairy suppliers | dairy insolvency | milk delivery/invoices | FOR filings | producer groups | batch fee | advisors | exact event | subcase | 85 |
| 17 | Grain elevator unpaid invoice batch | farms/groups | elevator insolvency | invoices/storage/delivery | FOR filings | co-ops | batch fee | advisors | exact event | subcase | 86 |
| 18 | Agricultural input rebate recovery | farms | supplier rebate unpaid | contracts/invoices | credit | accountants | success | suppliers | exact claim | commercial dispute | 58 |
| 19 | Crop processor retention release | producers | quality holdback | lab/contract docs | payment | lawyers/advisors | success | buyers | exact claim | dispute | 57 |
| 20 | Export phytosanitary certificate desk | exporters | shipment held | cert file | release | brokers | fee | exporters/brokers | exact shipment | regulatory | 60 |
| 21 | EU school fruit/milk payment batch | suppliers | public program payment | delivery docs | payment | suppliers | fee | public admin | exact invoice | public admin | 58 |
| 22 | Intervention storage payment claim | warehouses | public storage compensation | inventory docs | payment | agri admins | fee | specialists | exact file | public admin | 62 |
| 23 | Food-chain unfair-practice claim prep | producers | buyer delays/abuses | evidence file | complaint | lawyers | legal | lawyers | exact case | legal | 45 |
| 24 | Agri VAT refund support | farms | VAT refund delayed | tax file | refund | accountants | fee | tax advisors | exact file | tax | 45 |
| 25 | Farm fuel excise refund batch | farms | annual refund | invoices | application | communes/advisors | low | advisors | none | form filling | 42 |
| 26 | Agri leasing insurance refund | farms | cancelled policy | policy file | refund | brokers | fee | brokers | exact policy | insurance | 50 |
| 27 | Producer group claim no-go audit | groups | unsure FOR eligibility | invoice/event file | no-go | co-ops | fixed fee | advisors | exact event | triage only | 68 |
| 28 | Insolvent buyer watchlist for producers | producers | avoid bad buyers | database | subscription | producer orgs | low | public registries | none | database | 35 |
| 29 | Agri compensation class-action routing | producers | unpaid buyer | lawyer referral | claims | lawyers | referral | legal | none | legal broker | 30 |
| 30 | Warehouse KPO/byproduct settlement rail | agri processors | waste/byproduct docs | BDO docs | payment | waste advisors | fee | prior waste failures | exact docs | waste admin | 55 |

## Finalists

| Finalist | Internal simulated score | Advance? | Rationale |
|---|---:|---|---|
| FOR Agri Compensation Batch Desk | **88.1** | **Yes** | Best version starts from a named insolvent buyer and group-level unpaid invoice batch, not individual form filling. Payor is a neutral statutory fund and proof is accepted applications/status/payment. |
| Fruit/vegetable processor unpaid invoice batch | 86 | No | Strong subcase but too narrow if separated. |
| Grain elevator unpaid invoice batch | 86 | No | Strong subcase but supply is event-lumpy. |
| Milk processor unpaid invoice batch | 85 | No | Same, but sector-specific and co-op structures may already handle. |
| Producer group unpaid-buyer evidence room | 84 | No | Helpful but becomes a document room unless tied to filed compensation applications. |

## Lead Candidate

**FOR Agri Compensation Batch Desk**

### Internal Simulated Score

88.1 / 100

### Why It Advances

- It is current cash tied to a named official compensation program, not debt collection against an insolvent buyer.
- The buyer is not individual farmers in isolation. The first buyer is a producer group, cooperative, farm accountant, or cluster administrator with many member claims from one insolvency event.
- The proof object is a submitted/accepted compensation application, status update, deficiency narrowing, or payment, not advisory interest.
- The 2026 second application window creates a concrete July-August urgency.
- The founder can reject legal/insolvency disputes and accept only cases where unpaid sale, buyer insolvency, invoices/delivery docs, and producer authority are documented.

### Control Point

- Signed mandate from producer group/co-op/authorized administrator and individual member authorizations where required.
- Named insolvent buyer event.
- Invoice, delivery, quantity, product, payment-due, unpaid balance, bank, producer identity, and application files.
- KOWR/FOR application tracker, deficiency response log, status evidence, and payment tracker.
- Fee right tied to filed/accepted/status-advanced applications or compensation paid.

### 60-Day Proof

1. Three group/co-op/administrator mandates.
2. At least 80 producer/invoice files screened for one or more named insolvent buyers.
3. Thirty compensation applications filed or prepared for the next application window.
4. Two accepted/status-advanced applications, deficiency narrowings, or official no-go outcomes.
5. 40,000-100,000 PLN collected in batch fees and success-linked receivables.
6. One agri accountant or compensation-program reviewer retained.
7. Rejection/no-go rate above 30% to avoid bad cases.

### 6-Month POC

- 10-20 group or administrator mandates.
- 500-1,500 producer/invoice files screened.
- 250-800 applications filed/prepared.
- 80+ accepted/status-advanced/payment/no-go outcomes.
- 180,000-600,000 PLN revenue.
- 3 repeat producer-group/co-op/accountant channels.
- Gross margin above 60%.
- Kill if most cases are one-off low-value individual applications or if official free help/advisors eliminate willingness to pay.

### Economics

Charge 2,000-6,000 PLN for group intake and eligibility triage, 150-400 PLN per producer/invoice file in batch, plus 2-5% of compensation collected above a threshold, capped and disclosed. For producer groups with many unpaid invoices from one buyer, the fee is justified by speed, completeness, status tracking, and avoiding missed application windows. Avoid low-value individual claims.

### Copy Risk

Agricultural advisers, accountants, producer groups, lawyers, chambers, and public support channels can copy the process. The defense is event-specific batch control: signed group mandate, member authorities, shared buyer-insolvency file, invoice/delivery dataset, application tracker, deficiency memory, and status/payment follow-through.

### Why It Is Not A Service, Report, App, Dashboard, Database, Marketplace, Or Generic Broker

The startup controls a named compensation batch for a producer group or co-op and is paid on filed/accepted/status-advanced applications or compensation outcomes. It does not sell a public form guide, farm advisory subscription, legal claim, debt collection, marketplace, or database.

### Duplicate Risk

- Not PSE PV compensation: agricultural unpaid-buyer compensation under FOR, not electricity redispatch compensation.
- Not TraceFaktura: not municipal event-to-invoice routing.
- Not public grant applications generally: only producer-group batches tied to one insolvent buyer and unpaid sale invoices.
- Not DORA, REDBlocked, BioSignal, HeritageDoor, PromoLeak, CBAM, Data Act, GreenTender, BatteryFit, HeatQuiet, or health/Rx/clinical routes.

## Internal Cap Notes

- Not capped below 82: 60-day control proof is concrete through signed group mandates, producer files, submitted applications, status outcomes, and current compensation.
- Not capped below 85: generic advisers can copy forms, but not a controlled group/event batch once mandates and member files are assembled.
- Not capped below 87: economics work only at group/co-op batch scale and with July-August urgency.
- Capped at 88.1, not higher, because public/free help, agri advisers, legal/insolvency edge cases, and low-value individual claims can collapse the model.

## Gate Decision

Advance Round 303 to working Zero To One validation because the simulated score is strictly greater than 87.
