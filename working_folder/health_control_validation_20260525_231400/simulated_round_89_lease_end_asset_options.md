# Simulated Round 89: Lease-End Asset Option Spreads

Created: 2026-05-27

## Pivot From Round 88

Approved Carrier Credit Lockbox failed working-chat at `64 / 100`. The evaluator accepted the debtor-acknowledged framing but rejected the idea because the pool of large, clean, approved-but-unmonetized credits is unproven and likely too fragmented.

Round 89 tests a different hard-control category:

- expiring lease-end purchase options;
- exact physical commercial assets with serial/VIN/condition records;
- signed option/control before expiry;
- buyer deposit before buyout;
- title transfer or payoff path inside 60 days;
- no broad brokerage, listings, or random inventory.

## Raw Candidate Table

| # | Candidate | Buyer | Acute trigger | Transferable control point | Signed/titled/assigned/prepaid inside 60 days | First acquisition mechanism | Margin and payback logic | Copy risk | Why incumbents cannot copy before control is secured | Why it is not a service/report/app/dashboard/marketplace/broker |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | Forklift Lease-End Option Buyout With Buyer Deposits | Warehouses, 3PLs, used forklift dealers | Lease-end purchase option expires; lessee does not want to buy | Signed lessee option/authorization, leasing payoff, serial/condition/battery records, buyer deposit | 1 option, 1 buyer deposit, payoff/title | Accountants, leasing brokers, forklift service firms | Residual below buyer price; 8k-20k PLN spread | Medium-high: dealers | Exact expiring option and deposit controlled before dealers see it | Owns option/title, not brokerage |
| 2 | Commercial Van Lease-End Buyout Spread | Trades/fleet buyers/dealers | Van lease buyout below market | Lessee option, VIN, payoff, buyer deposit | 1 van option and deposit | Accountants/fleet admins | 5k-20k spread | High: dealers | Exact lessee option controlled | Asset transaction |
| 3 | Refrigerated Van Lease-End Buyout | Food/pharma logistics | Reefer van lease ends | Option + reefer service records + buyer deposit | 1 vehicle | Fleet brokers | Higher spread, compliance risk | Medium | Exact unit controlled | Asset transaction |
| 4 | Electric Pallet-Stacker Lease-End Lot | Warehouses | Stackers returned or buyout option ignored | Small fleet option + buyer deposit | 3 units | Forklift service firms | Lower capital, easier | Medium | Exact lot controlled | Asset sale |
| 5 | Scissor Lift Lease-End Buyout | Contractors/facility firms | Access platform lease ends | Option + UDT/service records + deposit | 1 unit | Rental firms | High value but inspection risk | Medium | Exact option controlled | Asset sale |
| 6 | Cleaning Scrubber Lease-End Buyout | Facilities/cleaning firms | Floor machine lease ends | Option + service records + deposit | 2 units | Cleaning contractors | Low-medium ticket | Medium | Exact option controlled | Asset sale |
| 7 | Commercial Laundry Machine Lease-End | Hotels/laundries | Laundry equipment lease ends | Option + service records + buyer | 2 units | Laundries/hotels | Niche margin | Medium | Exact machines controlled | Asset sale |
| 8 | Restaurant Combi-Oven Lease-End Buyout | Restaurants/caterers | Kitchen lease ends; business closes | Option/title + buyer deposit | 2 ovens | Leasing brokers | Good demand but closure chaos | Medium | Exact units controlled | Asset sale |
| 9 | Coffee Machine Lease-End Buyout | Offices/cafes | Operator/lease ends | Option + service records | 5 units | Office coffee operators | Commodity | High | Exact lot controlled | Asset sale |
| 10 | Vending Machine Lease-End + Location Option | Operators | Machine lease/location handoff | Asset plus location consent | 3 machines | Vending operators | Better if location transfers | Medium | Location consent controlled | Asset + account |
| 11 | Office Printer Fleet Lease-End | SMEs/dealers | Copier lease ends | Option + meter/service records | 5 units | Office admins | Commodity/low margin | High | Exact fleet controlled | Asset sale |
| 12 | Industrial Compressor Lease-End Buyout | Factories/service firms | Compressor lease/rental ends | Option + service records + buyer | 1 unit | Compressor service firms | High value but Data Act adjacent | Medium | Exact unit controlled | Asset sale |
| 13 | Mini Excavator Lease-End Buyout | Contractors/dealers | Equipment lease ends | Option + service hours + deposit | 1 unit | Construction accountants | High ticket/capital | Medium-high | Exact option controlled | Asset sale |
| 14 | Skid-Steer Loader Lease-End | Contractors/farms | Lease ends | Option + service records | 1 unit | Equipment brokers | High capital | Medium | Exact unit controlled | Asset sale |
| 15 | Small Trailer Lease-End Buyout | Logistics/trades | Trailer lease ends | Option + VIN + buyer deposit | 2 trailers | Fleet admins | Medium | High | Exact options controlled | Asset sale |
| 16 | E-bike Courier Fleet Lease-End | Courier operators | Fleet replacement | Title/option + buyer deposit | 20 bikes | Courier fleets | Battery condition risk | Medium | Exact fleet controlled | Asset sale |
| 17 | Gym Equipment Lease-End Lot | Gyms/hotels | Gym closes/lease ends | Option/title + buyer deposit | 10 units | Leasing brokers | Low-medium | High | Exact lot controlled | Asset sale |
| 18 | Industrial Sewing Machine Lease-End | Apparel shops | Workshop lease ends | Option + buyer deposit | 5 machines | Tailor/manufacturing networks | Niche | Medium | Exact lot controlled | Asset sale |
| 19 | CNC/Router Lease-End Buyout | Shops/makers | Lease ends | Option + inspection + buyer | 1 machine | CNC service firms | High margin but technical | Medium | Exact machine controlled | Asset sale |
| 20 | Laser Cutter Lease-End | Sign makers | Lease ends | Option + buyer deposit | 1 unit | Service firms | Technical risk | Medium | Exact unit controlled | Asset sale |
| 21 | POS/Fiscal Device Lease-End Lot | Retail/restaurants | Lease changes | Option + buyer | 20 units | Fiscal service firms | Low ticket/authorized service | High | Exact lot controlled | Asset sale |
| 22 | CCTV/Security Equipment Lease-End | HOAs/SMEs | Contract ends | Equipment title + site consent | 5 sites | Installers | Privacy/security risk | High | Site consent controlled | Asset/account |
| 23 | Server/IT Lease-End Buyout | SMEs/dealers | Hardware lease ends | Option + data wipe cert + buyer | 10 servers | MSPs | Data risk/commodity | High | Exact lot controlled | Asset sale |
| 24 | MacBook/Phone Fleet Lease-End | SMEs/dealers | Device fleet refresh | Option + MDM release + buyer | 30 devices | MSPs | Commodity | High | Exact lot controlled | Asset sale |
| 25 | Industrial Racking Lease-End Lot | Warehouses | Warehouse closes/lease ends | Title + removal rights + buyer deposit | One racking lot | Warehouse closures | Logistics-heavy | Medium | Exact racking lot controlled | Asset sale |
| 26 | Retail Refrigeration Cabinet Lease-End | Shops | Store closure/lease end | Option/title + buyer | 5 cabinets | Store fitout firms | Refrigerant/service risk | Medium | Exact lot controlled | Asset sale |
| 27 | Container Office Lease-End Buyout | Construction firms | Site project ends | Option/title + buyer | 2 containers | Leasing firms | Low-medium | Medium | Exact units controlled | Asset sale |
| 28 | Event Tent/Floor Lease-End Lot | Event firms | Season/fleet refresh | Option + buyer deposit | One lot | Event rentals | Seasonal | Medium | Exact lot controlled | Asset sale |
| 29 | Scaffold Lot Lease-End | Contractors | Fleet refresh | Title + buyer deposit | One lot | Scaffold firms | Safety/cert risk | Medium | Exact lot controlled | Asset sale |
| 30 | Used Tool Fleet Lease-End | Contractors | Tool leasing ends | Title + buyer | 100 tools | Rental firms | Low ticket | High | Exact lot controlled | Asset sale |
| 31 | Medical Device Lease-End Buyout | Clinics | Equipment lease ends | Option + buyer | 1 unit | Clinics | Health/regulatory risk | Medium | Exact unit controlled | Reject health |
| 32 | Dental Chair Lease-End | Clinics | Chair lease ends | Option + buyer | 1 unit | Dentists | Health/regulatory risk | Medium | Exact unit controlled | Reject health |
| 33 | Heat-Pump Installer Equipment Lease-End | Installers | Tool/vehicle lease ends | Option + buyer | 1 unit | Installers | Energy-family duplicate | High | Exact option controlled | Weak |
| 34 | EV Charger Lease-End Buyout | HOAs/fleets | Charger lease/account ends | Asset + account transfer | 3 chargers | Installers | Account/service risk | Medium | Asset/account controlled | Asset + account |
| 35 | Agricultural Implement Lease-End | Farmers/dealers | Lease ends | Option + buyer | 1 implement | Agri dealers | Seasonal/capital | Medium | Exact option controlled | Asset sale |
| 36 | Forklift Battery Lease-End Pack | Warehouses | Battery lease/replacement | Battery test + deposit | 5 batteries | Forklift service | Battery condition risk | Medium | Exact tested batteries controlled | Asset sale |
| 37 | Payment Terminal Lease-End Lot | Retailers | Terminal provider changes | Terminal lot | 50 terminals | PSPs | Provider locks/low value | High | Weak | Reject |
| 38 | Solar Inverter Lease-End Spares | Installers | Lease/fleet refresh | Title + buyer | 10 units | Installers | Energy/compatibility | High | Exact lot controlled | Asset sale |
| 39 | Generic Lease-End Marketplace | Asset owners | Lease ends | Listings only | None | SEO | Weak | Very high | No control | Reject |
| 40 | Lease Audit Advisory | SMEs | Overpay lease | No asset | Audit fee | Accountants | Service-like | High | No control | Reject |

## Finalist Scoring

| Finalist | Simulated score | Decision | Main rationale |
|---|---:|---|---|
| Forklift Lease-End Option Buyout With Buyer Deposits | 88 | Advance to real Zero To One | Best mix of exact physical asset, expiry trigger, buyer deposit, industrial buyer demand, manageable ticket under 100k PLN, and clear option/title control. |
| Electric Pallet-Stacker Lease-End Lot | 86 | No advance | Lower capital and easier logistics but lower ticket and more commodity. |
| Refrigerated Van Lease-End Buyout | 85 | No advance | Higher spread potential but vehicle/refrigeration compliance and dealer competition are stronger. |
| Scissor Lift Lease-End Buyout | 84 | No advance | Similar logic but UDT/service/inspection risk and higher capital. |
| Restaurant Combi-Oven Lease-End Buyout | 83 | No advance | Good closure supply but lower durability and commodity resale. |
| Vending Machine Lease-End + Location Option | 82 | No advance | Interesting if location transfers, but account/location trust creates service-book risk. |

## Lead Candidate: Forklift Lease-End Option Buyout With Buyer Deposits

### Buyer

Primary buyers:

- small and mid-sized warehouses needing one known-history electric forklift, stacker, reach truck, or pallet truck;
- used forklift dealers who want off-market units with service records;
- 3PLs, manufacturers, wholesalers, and installers replacing or adding material-handling equipment;
- forklift service firms that can inspect, repair, and resell units.

Source sellers:

- SMEs whose forklift/electric pallet truck lease or long-term rental is ending;
- lessees with an expiring purchase option who do not want to use cash or arrange resale;
- accountants, leasing brokers, and forklift service technicians who see lease-end customers before dealers do.

### Acute Trigger

A lessee's forklift/stacker/reach-truck lease-end purchase option expires in 7-45 days. The lessee can either:

- return the equipment and risk return/restoration charges;
- buy the machine and spend time reselling it;
- ignore a residual purchase option that may be below resale value;
- let the leasing/rental firm remarket the unit.

The founder only acts if a downstream buyer or dealer has paid a deposit against that exact serial-numbered machine after condition review.

### Transferable Control Point

Control requires:

- leasing-company payoff or purchase-option statement with expiry date and residual amount;
- lessee authorization or option agreement allowing the founder/new buyer to fund and complete the buyout path;
- serial/VIN, year, model, mast type, lift capacity, battery type/age, charger, hours, service records, UDT/inspection status where applicable, photos, and defect notes;
- independent forklift technician inspection or buyer inspection;
- buyer/dealer deposit tied to that exact serial number before final payoff;
- clean title transfer path, invoice/VAT treatment, and no undisclosed liens;
- written rule that the founder does not certify safety, UDT status, or suitability for a specific workplace.

### Sixty-Day Proof

Within 60 days and under 100,000 PLN:

1. Build a source list of 80 forklift service firms, leasing brokers, accountants serving warehouses, small 3PLs, wholesalers, and manufacturers.
2. Build a buyer list of 50 used-equipment dealers, warehouses, 3PLs, and service firms.
3. Inspect 5 lease-end purchase-option opportunities.
4. Reject any unit without clean payoff, title path, service/inspection records, buyer interest, or clear condition.
5. Sign one conditional option with a lessee where the founder pays only if buyer deposit and title path are confirmed.
6. Obtain one buyer/dealer deposit of at least 10-20% of resale price for that exact serial-numbered machine.
7. Complete one payoff/title transfer/resale or escrowed back-to-back sale.
8. Prove at least 8,000 PLN gross spread after inspection, transport, minor prep, legal/accounting review, payment fees, and risk reserve.
9. Document time-to-close and repeatable source/buyer channels.

### First Acquisition Mechanism

Lessee pitch:

"Your forklift lease buyout option expires soon. If you do not want to use cash or resell it, I can arrange a conditional buyout. I only proceed if a buyer deposits against the exact machine and the leasing payoff/title path is clean. You avoid return hassle and may receive part of the upside."

Buyer pitch:

"I have a lease-end electric forklift/stacker with serial, hours, battery/charger info, service records, inspection photos, payoff/title path, and a short deadline. Deposit reserves the exact unit; installation, UDT, safety checks, and suitability stay with you and your service provider."

### Economics

Example transaction:

- residual/payoff and seller option payment: 40,000-70,000 PLN;
- inspection, transport, prep, admin, and reserve: 4,000-10,000 PLN;
- buyer resale price: 58,000-95,000 PLN;
- target gross spread: 8,000-20,000 PLN;
- no payoff unless buyer deposit and title path are confirmed.

Payback comes from one controlled back-to-back transaction, not inventory accumulation. The POC dies if residual values are usually market-priced or if buyers refuse deposits before payoff.

### Copy-Risk Defense

Forklift dealers and leasing companies already exist. The wedge is not "sell used forklifts." It is:

- hidden lease-end purchase options before dealers get the returned unit;
- conditional control of exact serial-numbered machines;
- buyer deposits before capital outlay;
- a source network among accountants/service technicians/leasing brokers who see option-expiry events;
- repeated option-expiry and buyer-demand memory.

Incumbents cannot copy a specific lessee option once the payoff path, buyer deposit, and conditional buyout agreement are signed.

### Why It Is Not A Service, Report, App, Dashboard, Marketplace, Or Generic Broker

The startup controls the purchase option/title path and downstream buyer deposit for an exact asset. It does not sell a listing site, appraisal report, lease audit, sourcing service, or generic used-equipment brokerage.

### Safety And Legal Boundaries

- Forklift technicians/service firms handle condition inspection, repairs, and UDT/safety questions.
- Buyer remains responsible for workplace suitability, operator training, UDT/inspection, maintenance, and safe use.
- The founder does not certify technical condition beyond disclosed inspection records and defects.
- Legal/accounting review covers assignment/option mechanics, VAT, invoice/title transfer, and leasing-company consent.
- No unit is acquired without clean title path and buyer deposit.

### Duplicate-Risk Check

- Not Factory Control-Spares Donor Bank: no obsolete PLC/HMI modules or line-down controls inventory.
- Not HeritageDoor/StormTile: no salvage architecture.
- Not CarrierProof or Approved Carrier Credit Lockbox: no parcel claims or receivables.
- Not DORA/CBAM/EUDR/REDBlocked/BioSignal/TraceFaktura: no evidence desk, compliance desk, marketplace account rescue, health diligence, or municipal invoice routing.

## Internal Objections Before Real Gate

- Dealers and leasing companies already monetize returned equipment.
- Residual purchase options may usually be market-priced.
- Lessees may already understand they can buy and resell.
- Buyer deposits before payoff may be hard without strong dealer trust.
- UDT/inspection/battery condition can kill margin.
- One-off asset spreads may not become a repeatable startup.
- Capital can be tied up if back-to-back sale slips.

## Simulated Verdict

Advance one prompt to working-chat validation. Simulated score `88 / 100` passes because the candidate has a concrete expiring option, exact asset control, buyer deposit, title path, and short cash-conversion test.
