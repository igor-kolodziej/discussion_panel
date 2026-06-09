# Simulated Round 315: CBAM Authorised Declarant Import-Release Mandate

## Gate Setup

- Simulation gate: strictly >87.
- Real working-chat gate: >=85.
- Real fresh-chat gate: >=85.
- Search branch: broker-routed hard customs/status gate with current cash at risk.

## Raw Candidate Control Table

| # | Candidate | Buyer | Acute Trigger | 60-Day Control Proof | Internal Score | Decision |
|---|---|---|---|---|---:|---|
| 1 | CBAM Authorised Declarant Import-Release Mandate | SME importers/customs reps above CBAM threshold | Broker says CBAM goods cannot be released/imported because authorised-declarant status, timely application proof, threshold proof, or TARIC document code is missing | Signed importer/broker mandate, CBAM/PUESC status evidence, ACD application trail, broker declaration acceptance or clean no-go | 89.0 | Advance |
| 2 | CBAM Supplier Emissions Default-Cost Recovery | Importers with suppliers overcharging CBAM default costs | Supplier price disputes over embedded emissions/default values | Contract, emissions data, recovered credit | 79.0 | Reject: legal/commercial dispute |
| 3 | CBAM Certificate Purchase Cash-Flow Desk | Importers preparing 2027 certificate purchase | Certificate cost forecast/payment planning | Forecast, treasury plan | 72.0 | Reject: advisory/no current release |
| 4 | CBAM Quarterly Declaration Correction Desk | Importers with historical reporting errors | Prior declaration errors need correction | Portal correction, accepted filing | 80.5 | Reject: accounting/compliance advisory |
| 5 | CBAM Broker Client Continuity Memo | Brokers serving SME importers | Need proactive exposure memo | Broker-branded memo | Existing confirmed theme |
| 6 | CBAM Steel Shipment Code Fix Desk | Customs brokers | Declaration rejected due wrong CBAM TARIC/doc code | Correct code accepted, release | 86.5 | Strong subset but too narrow |
| 7 | CBAM Threshold Proof File | Low-volume importers near 50-ton threshold | Customs/broker requires threshold evidence | Mass ledger, accepted exemption code | 85.5 | Subset of #1 |
| 8 | CBAM ACD Application Completion Sprint | Importers missing application | Need application submitted before next shipment | Submitted application/status | 87.0 | Merge into #1 |
| 9 | CBAM Indirect Representative Mandate Switch | Importer needs customs rep to act | Broker/rep switch blocks release | Mandate, release | 82.0 | Legal/representation risk |
| 10 | CBAM Iron/Steel Supplier Evidence RFI Desk | Importers missing supplier emissions | Supplier RFI and default exposure | Supplier data/no-go | Existing confirmed theme |
| 11 | ICS2 ENS Error Release Desk | Forwarders/carriers | Entry summary rejects block shipment | ENS accepted | 70.0 | Already failed branch |
| 12 | F-gas Licence Release Desk | Importers | HFC import licence/quota issue | licence/status | 72.0 | Prior fail |
| 13 | CPSC eFiling Entry Release | EU sellers/importers | US entry blocked by certificate data | Broker packet | 70.0 | Prior fail |
| 14 | EUDR DDS Import Release | CEE importers/brokers | DDS/reference data blocks PO/shipment | DDS packet | 72.0 | Prior fail |
| 15 | Organic COI Release Desk | Importers | COI/TRACES issue blocks release | COI accepted | 73.0 | Customs/incumbents |
| 16 | CATCH Fish Import Release | Seafood importers | Catch certificate issue blocks import | accepted certificate | 68.0 | Prior fail |
| 17 | Russia Origin MTC Customs Release | Importers | Metal origin certificate question | customs response | 72.0 | Prior fail/legal |
| 18 | FuelEU Pooling Release | Ship operators | pooling compliance/payment | contract proof | 58.0 | Prior fail |
| 19 | Methane Import Report Workpaper | Energy importers | future methane data | workpaper | 62.0 | Prior fail |
| 20 | De Minimis Tariff Reclassification Refund | US ecommerce importers | tariff change/overpayment | refund claim | 77.0 | legal/customs |
| 21 | CAPE Tariff Refund Batch | US importers | IEEPA refund | claim | 82.0 | prior near miss, legal |
| 22 | Customs Broker CBAM Overflow Desk | Brokers | too many ACD/status cases | accepted broker cases | 87.2 | channel expression of #1 |
| 23 | CBAM Customer PO Hold Release | Importer customer demands ACD proof before PO | ACD/status proof accepted | buyer acceptance | 84.0 | buyer acceptance outside customs |
| 24 | CBAM Bank LC Condition Release | Bank asks CBAM proof before LC/payment | bank accepts evidence | payment release | 79.0 | bank/legal/trade finance |
| 25 | CBAM Warehouse Inventory Release | Goods in customs warehouse need status | status or no-go | release/no-go | 86.0 | subset |
| 26 | CBAM Application Evidence Escrow | Importer pays only after application/status | application/status | 86.5 | mechanism only |
| 27 | CBAM Broker-Branded Application Packet | Broker resells ACD application/status pack | submitted packet | 88.0 | channel for #1 |
| 28 | CBAM Default-Value Price Quote Desk | importers quote CBAM surcharge to customers | quote | 74.0 | advisory |
| 29 | CBAM Annual Declaration Prep | importers preparing 2027 declaration | draft declaration | 76.0 | compliance/advisory |
| 30 | CBAM Supplier Contract Addendum Desk | importers add emissions clauses | contract wording | 70.0 | legal |

## Finalists

1. **CBAM Authorised Declarant Import-Release Mandate**: strongest because it is tied to a current binary customs/import ability event, not a readiness memo.
2. **CBAM Broker-Branded Application Packet**: strong channel expression when brokers already control customs documents.
3. **CBAM Steel Shipment Code Fix Desk**: sharp but too narrow as standalone.
4. **CBAM Threshold Proof File**: strong exemption/status subset.
5. **CBAM Warehouse Inventory Release**: useful edge case, but may be slower.

## Selected Candidate

**CBAM Authorised Declarant Import-Release Mandate**

## Internal Score: 89.0

Why it clears simulation:

- Current hard gate: CBAM definitive regime and authorised-declarant status/application requirements are operational in 2026.
- Control is concrete: importer mandate, broker collaboration, PUESC/CBAM portal evidence, threshold ledger, application/status trail, declaration code acceptance, and first customs release/no-go.
- First proof is not a memo: accepted application/status proof, valid declaration path, broker acceptance, customs release, shipment cleared, or clean no-go.
- Brokers already sit at the data bottleneck, reducing cold trust friction.
- The buyer has current cash at risk: goods cannot be imported, sold, delivered, or invoiced if release is blocked.
- It is materially distinct from the existing CBAM Import Continuity Desk because it is not a proactive broker-branded exposure triage. It starts after a named shipment/import lane is blocked by status/application/TARIC-code issues and ends with application/status/release/no-go evidence.

## Internal Concerns

- Strong duplicate risk with the confirmed CBAM Import Continuity Desk; the prompt must clearly distinguish control point and proof artifact.
- Customs brokers or indirect customs representatives may internalize after a few cases.
- ACD application, customs representation, legal status, and declaration authority boundaries must stay with importer/broker/official systems.
- Not every blocked shipment can be fixed quickly; some are clean no-go if the importer missed deadlines or lacks authorisation.
- It must not drift into emissions calculation, legal advice, CBAM declaration filing, or general CBAM consulting.

## 60-Day Proof Standard

- 4 prepaid importer/broker cases tied to named shipments, import lanes, customs-warehouse inventory, or imminent customs declarations.
- At least 6,000,000 PLN of shipment value under mandate.
- At least 100,000 PLN collected in fixed fees.
- 2 accepted ACD application/status/TARIC-code/customs-release or clean no-go outcomes.
- 1 broker sends a second case.
- Rejection log above 50% for generic CBAM readiness, emissions calculation, supplier data chasing, legal disputes, customs representation issues, and cases without a named shipment/import lane.

## Why This Is Not A Duplicate

Existing CBAM Import Continuity Desk is broker-branded exposure triage from existing import documents: CN/TARIC exposure, threshold risk, authorised-declarant readiness, supplier-emissions gaps, default-value exposure, and supplier requests.

This candidate is an urgent release/status mandate: a broker/importer already has a named shipment or import lane blocked by missing authorised-declarant status, timely-application proof, threshold proof, declaration code, or PUESC/CBAM portal status. The proof artifact is not a memo; it is application/status evidence, declaration-path acceptance, customs-release progress, shipment release, or clean no-go.
