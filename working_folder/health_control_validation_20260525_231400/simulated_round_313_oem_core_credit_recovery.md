# Simulated Round 313: OEM Core Credit Recovery Mandate

## Gate Setup

- Simulation gate: strictly >87.
- Real working-chat gate: >=85.
- Real fresh-chat gate: >=85.
- Search branch: recovery mandate / already-charged deposits and credits.

## Raw Candidate Control Table

| # | Candidate | Buyer | Acute Trigger | 60-Day Control Proof | Internal Score | Decision |
|---|---|---|---|---|---:|---|
| 1 | OEM Core Credit Recovery Mandate | Truck/agri/construction equipment/industrial repair chains, parts distributors, remanufacturers | Refundable core charges/exchange deposits charged but not credited after returned parts | Signed mandate, supplier account statement, RMA/core tags, PODs, portal claims, first credit memo/cash | 88.4 | Advance |
| 2 | Industrial Gas Cylinder Deposit Recovery | Labs, food plants, machine shops | Cylinder rental/deposit credits missing | Supplier ledger, cylinder serials, return slips, credit | 84.0 | Reject: site work and supplier leverage |
| 3 | EUR Pallet/RTI Deposit Recovery | Food/retail warehouses | Returned pallets/totes not credited | Statements, return notes, supplier credit | 82.2 | Reject: low ticket and commodity |
| 4 | IBC/Drum Deposit Recovery | Chemical distributors | Returnable packaging deposits stuck | Lot IDs, pickup notes, credit memo | 82.5 | Reject: lower margin, hazardous scope |
| 5 | Battery Core Deposit Recovery | Auto/equipment service chains | Lead-acid/lithium battery deposits not credited | Return docs, supplier claim, credit | 83.8 | Merge into #1 only if safe/non-hazardous admin |
| 6 | Tire Casing Credit Recovery | Truck tire dealers/retreaders | Casing credits not issued | Casing IDs, condition records, claim credits | 83.0 | Reject: condition disputes |
| 7 | Printer Cartridge Core Credit Recovery | Office resellers | Empty cartridge credits unpaid | Return proofs, supplier credit | 77.0 | Reject: low value |
| 8 | Medical Device Loaner Return Credit Recovery | Hospitals/distributors | Loaner/deposit credits stuck | Return proofs, supplier credit | 76.5 | Reject: health/procurement boundary |
| 9 | Tooling Deposit Refund Mandate | Manufacturers | Tooling deposits not released | Contract, acceptance docs, refund | 78.0 | Reject: legal/commercial disputes |
| 10 | Warranty Parts Credit Recovery | Authorized service centers | OEM warranty reimbursements unpaid | Claim IDs, portal disputes, credit | 77.5 | Reject: warranty branch failed |
| 11 | Fleet Telematics Hardware Deposit Recovery | Fleets | Device deposits after vehicle churn not refunded | Serial list, returns, credit | 81.5 | Reject: telecom/contract disputes |
| 12 | Uniform/Laundry Deposit Recovery | Factories/hospitality | Garment deposits and losses overcharged | Wearer lists, return notes, credit | 78.0 | Reject: small/operational |
| 13 | Propane/LPG Tank Deposit Recovery | Horeca/industrial | Tank/cylinder deposits missing | Account statement, returns, credit | 80.0 | Reject: site/safety |
| 14 | Forklift Battery Rental Credit Recovery | Warehouses | Battery rental/return credits missing | Contract, serials, returns, credit | 81.0 | Reject: narrow, condition disputes |
| 15 | IT Hardware RMA Credit Recovery | MSPs/resellers | Vendor credits missing after RMA returns | RMA IDs, PODs, credit | 82.0 | Reject: generic RMA |
| 16 | Network Equipment Advance Replacement Credit | MSPs/telcos | Advance replacement units billed, returns uncredited | Serial/POD, vendor cases, credit | 83.5 | Potential future, but lower than #1 |
| 17 | POS Terminal Return Credit Recovery | Retailers/resellers | Terminal deposits/returns uncredited | Serial returns, processor/vendor credit | 78.0 | Reject: payments/processor complexity |
| 18 | Coffee Machine Lease Deposit Recovery | Horeca operators | Lease deposits not credited after returns | Contract, pickup, credit | 75.0 | Reject: low value |
| 19 | Aircraft Rotable Core Credit Recovery | MROs | Exchange rotables not credited | Serial/8130/EASA docs, supplier credit | 86.5 | Too regulated/credibility heavy |
| 20 | Rail Component Exchange Deposit Recovery | Rail maintenance suppliers | Exchange credits stuck | Serial docs, return acceptance, credit | 85.0 | Too slow/regulated |
| 21 | Marine Engine Core Credit Recovery | Boat yards/dealers | Engine/gearbox core credits missing | RMA, serials, credit | 83.0 | Seasonal/narrow |
| 22 | Hydraulic Cylinder Exchange Credit Desk | Industrial service depots | Returned exchange units not credited | Job cards, tags, PODs, credit | 84.5 | Subset of #1 |
| 23 | Turbocharger Injector Core Recovery | Truck/agri repair networks | Core credits missing after returns | Supplier ledger, core tags, credit | 85.5 | Strong subset of #1 |
| 24 | EV Battery Module Exchange Credit | EV service networks | High-value module deposits uncredited | Serial returns, hazardous docs, credit | 80.0 | Reject: safety/regulatory uncertainty |
| 25 | Copier Lease Equipment Return Credit | Office equipment dealers | Returned machines still billed | Asset list, pickup, credit | 80.5 | Reject: lease dispute |
| 26 | Construction Formwork Deposit Recovery | Contractors | Formwork returns/deposits not reconciled | Return notes, damage claims, credit | 78.5 | Reject: bulky/damage disputes |
| 27 | Scaffold Component Deposit Recovery | Contractors | Missing deposit credits after return | Return records, damage deductions | 77.5 | Reject: disputed condition |
| 28 | Beverage Keg Deposit Credit Recovery | Brewers/distributors | Keg deposits not credited | Keg IDs, returns, credit | 82.0 | Reject: existing keg tracking + low margin |
| 29 | Vending Machine Asset Deposit Recovery | Operators | Hardware deposits after route exits | Serial returns, credit | 78.0 | Reject: low repeat |
| 30 | Fire Extinguisher Cylinder Exchange Credit | Service firms | Cylinder/exchange credits missing | Serial/return records, credit | 79.0 | Reject: small and regulated service |
| 31 | Industrial Sensor Advance Replacement Credit | Automation MSPs | Advance-replacement units billed after returns | Serial returns, vendor credit | 83.0 | Reject: generic RMA |
| 32 | Refurbished Laptop Buyback Credit Recovery | MSPs/ITAD sellers | Buyback credits missing | Asset list, pickup, credit | 78.0 | Reject: ITAD incumbents |
| 33 | Packaging Equipment Spare Exchange Credits | Food plants/service firms | Exchange deposits on high-value spares not credited | Serial returns, supplier credit | 84.0 | Subset of #1 |
| 34 | Heavy Equipment Reman Credit Recovery | Dealers/fleet workshops | Reman engine/transmission/hydraulic deposits stuck | Core ledger, return POD, supplier credit | 86.0 | Strong subset of #1 |
| 35 | Refrigeration Compressor Core Credit Recovery | HVAC wholesalers/service chains | Compressor cores not credited | RMA tags, supplier account, credits | 85.0 | Good subset, but seasonal |

## Finalists

1. **OEM Core Credit Recovery Mandate**: highest because the credit object is specific, monetary, documented, and already charged; many businesses lose money in the gap between parts/service operations and AP.
2. **Turbocharger/Injector Core Recovery**: strong narrow beachhead inside truck/agri repair, but less expansive as standalone.
3. **Heavy Equipment Reman Credit Recovery**: high-ticket version for engines/transmissions/hydraulics, but slower and more condition-sensitive.
4. **Network Equipment Advance Replacement Credit**: compact and documented, but too close to generic RMA.
5. **Aircraft/Rail Rotable Core Credit**: high-ticket but regulated and credibility-heavy for a Warsaw solo founder.

## Selected Candidate

**OEM Core Credit Recovery Mandate**

## Internal Score: 88.4

Why it clears simulation:

- Starts from already charged cash: core charges, exchange deposits, advance-replacement deposits, and remanufactured-part credits already sitting on supplier statements.
- First proof is monetary: credit memo, account offset, refund, or supplier acknowledgement of returned-core credit.
- The control object is specific and auditable: supplier account statement, part numbers, core IDs/tags, job cards, RMA numbers, return authorizations, shipment proof, supplier portal claims, and credit memos.
- Buyers have poor internal ownership because parts counters, service advisors, warehouse staff, AP, and supplier portals each hold different pieces of the return-credit trail.
- This is narrower and more defensible than generic invoice recovery, freight audit, warranty claims, or AP portal chasing because it requires part/core return pattern memory by OEM/supplier and a rebuilt core ledger.
- Copy risk exists, but after the mandate the startup controls the particular account reconciliation, supplier claim file, and credit chronology.

## Internal Concerns

- Condition disputes can destroy recoverability; cases must exclude damaged, late, missing, or untagged cores unless supplier policy allows credit.
- Large dealer groups may already have parts/AP teams.
- Suppliers may deny old claims or impose strict time limits.
- The first data rebuild can be labor-intensive.
- Some categories may require hazardous-goods or regulated handling; the startup should stay on documentation and credit recovery, not physical returns.

## 60-Day Proof Standard

- 4-6 signed mandates from repair chains, parts distributors, heavy-equipment service firms, or remanufacturing customers.
- At least 1,500,000 PLN in open core/exchange/advance-replacement credit value identified.
- At least 250,000 PLN in supplier-acknowledged credits, credit memos, offsets, refunds, or clean no-go decisions.
- At least 80,000 PLN collected in prepaid rebuild fees and success fees.
- Rejection log above 50% for condition disputes, missing PODs, stale claims, undocumented returns, low value, hazardous/regulated handling, and supplier policy exclusions.

## Why This Is Not A Duplicate

- Not warranty labor reimbursement: the claim is a refundable core/exchange deposit already charged to the buyer, not warranty adjudication.
- Not generic credit memo recovery: the startup reconstructs the returned-core ledger and files supplier/OEM return-credit claims.
- Not freight audit, AP portal release, Amazon recovery, supplier rebate, MDF, or retail deductions.
- Not a broker or marketplace: it controls a signed recovery mandate over specific supplier accounts and returned-core evidence.
