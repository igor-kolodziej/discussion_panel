# Simulated Round 170: OpenMRN Transit Guarantee Release Desk

Date: 2026-05-29
Real gate: working Zero To One >=85, fresh Zero To One >=85
Simulation gate: strictly >87

## Source Checks

- GOV.UK NCTS guarantee guidance says if a trader reaches the limit of its guarantee, NCTS will not allow new movements until the guarantee reference amount is available again or topped up.
- European Commission NCTS pages describe MRNs, destination control results, office of departure write-off, guarantee release, and enquiry procedure when feedback is missing.
- GOV.UK transit manual guidance says IE045/write-off notification tells the departure trader a transit movement has been discharged, and that the guarantee reference amount reserved against the movement is credited back to the guarantee balance.
- GOV.UK March 2024 NCTS Phase 5 guidance says uncleared movements may cause some or all of a transit guarantee to be held until enquiries conclude, and manual closure can create longer processing times.

## 34 Raw Candidates Forced Through Hard-Control Table

| # | Candidate | Buyer | Acute trigger | Transferable control point | 60-day signed/titled/assigned/prepaid proof | Internal score/cap reason |
|---|---|---|---|---|---|---|
| 1 | OpenMRN Transit Guarantee Release Desk | small customs agents/forwarders | NCTS guarantee balance locked by open MRNs | MRN-specific mandate, proof packet, customs enquiry submissions | IE045/write-off, credited guarantee balance, first fee | 88.5: live guarantee capacity and official release artifact |
| 2 | EMCS Excise Movement Guarantee Discharge Desk | excise warehousekeepers | undischarged e-AD guarantee risk | ARC file and consignee proof | discharge confirmation | 81: excise/alcohol/tobacco complexity |
| 3 | ATA Carnet Deposit Release Desk | exporters/event suppliers | carnet not discharged, deposit held | carnet file, re-import/export proof | guarantee association release | 82: niche, slower, legal-ish |
| 4 | Temporary Admission Deposit Refund Mandate | importers | cash deposit held by customs | customs decision and proof of re-export | refund credited | 80: customs brokers own |
| 5 | Transit Duplicate MRN Cancellation Desk | customs agents | duplicate declaration tying guarantee | cancellation request | guarantee released | 79: too simple, agents do it |
| 6 | Customs Warehouse Discharge Proof Desk | warehouse operators | goods not discharged from special procedure | stock movement proof | discharge accepted | 77: warehouse customs teams own |
| 7 | Port Health Inspection Fee Refund | food importers | duplicate fees/failed release | authority claim | refund | 70: regulated health/food |
| 8 | Border Inspection CHED Correction Desk | importers | CHED mismatch blocks release | TRACES correction | release | 74: brokers/vets, source docs |
| 9 | Freight Demurrage Claim Mandate | importers | wrong demurrage billed | carrier claim | credit | 73: recovery incumbents |
| 10 | Container Deposit Release Desk | importers/NVOCCs | container deposits held | return proof | deposit released | 75: forwarders already handle |
| 11 | Pallet Exchange Debt Release | hauliers | pallet balances disputed | CMR/pallet note evidence | settlement | 68: low-margin |
| 12 | POD Payment Release Desk | trucking subcontractors | broker withholds invoice | signed CMR/POD | invoice paid | 70: factoring/TMS pattern |
| 13 | Marketplace Reserve Release | ecommerce sellers | funds held | platform case | release | 76: platform opacity |
| 14 | Retailer Operational Chargeback Recovery | CPG vendors | deductions taken | retailer portal disputes | reversal | 78: PromoLeak-adjacent |
| 15 | 3PL Overbilling Recovery | ecommerce brands | invoice mismatches | contract/WMS claim | credit | 71: failed pattern |
| 16 | Freight Invoice Credit Recovery | importers/exporters | accessorial errors | claim packet | credit memo | 74: freight-audit incumbents |
| 17 | Letter of Credit Discrepancy Cure Desk | exporters | bank refuses docs | LC doc-set mandate | waiver/payment | 80: bank/trade finance expertise |
| 18 | Public Works Retention Release Mandate | contractors | warranty/security release due | final acceptance + release letter | cash returned | 83: credible cash but legal/admin incumbents |
| 19 | Bank Guarantee Fee Stop-Loss Desk | contractors | guarantee keeps accruing fees | release letter | guarantee cancelled | 81: fee value may be low |
| 20 | Lease Security Deposit Recovery | commercial tenants | deposit not returned | lease/inspection proof | refund | 72: legal/property consultants |
| 21 | Utility Connection Deposit Release | RES developers | connection cancelled/expired | DSO file | deposit returned | 75: energy law/consultants |
| 22 | Import VAT Deferment Guarantee Cleanup | importers | guarantee line tied | customs decision | line released | 76: tax/customs brokers |
| 23 | Customs Duty Overpayment Refund | importers | classification/value error | repayment claim | refund | 74: customs brokers and slow |
| 24 | Origin Preference Refund Desk | importers | proof of origin arrives late | post-clearance claim | duty refund | 77: customs brokers |
| 25 | Rejected Export MRN Closure Desk | exporters | AES/ECS open export | exit proof | MRN closed | 78: brokers |
| 26 | ICS2 Filing Error Release Desk | carriers | ENS errors block movement | corrected filing | movement accepted | 74: carrier systems |
| 27 | EORI/ORI Reactivation Desk | importers | account disabled | authority case | reactivation | 68: simple admin |
| 28 | AEO Suspension Rescue | logistics firms | AEO status questioned | corrective plan | status restored | 72: consultants/legal |
| 29 | CITES Permit Release Desk | luxury/wood/instrument traders | shipment held | permit proof | release | 70: regulated, low volume |
| 30 | Sanctions False-Positive Release | importers/exporters | bank/carrier hold | screening evidence | release | 76: legal/compliance sensitive |
| 31 | Insurance Cargo Claim Mandate | importers | damaged shipment | survey/claim | payout | 70: adjusters/brokers |
| 32 | Returned Goods Relief Refund Desk | ecommerce brands | duties paid on returns | RGR claim | refund | 77: customs brokers, data heavy |
| 33 | Inward Processing Discharge Sprint | manufacturers | discharge deadline | bill of discharge | duty suspension preserved | 78: customs teams |
| 34 | TIR Carnet Claim Prevention Desk | hauliers | TIR discharge issue | carnet proof | association confirmation | 79: associations own gate |

## Finalists

| Finalist | Internal score | Why advanced | Why not winner |
|---|---:|---|---|
| OpenMRN Transit Guarantee Release Desk | 88.5 | Current guarantee capacity is locked; official write-off/guarantee credit is a hard proof artifact; buyer pain directly blocks new transit declarations. | Customs-agent incumbents and legal/customs representation boundaries are real risks. |
| Public Works Retention Release Mandate | 83 | Current cash/security release is concrete and public-debtor workflow may be systematic. | Likely legal/admin incumbent; contractors may already track big retentions. |
| ATA Carnet Deposit Release Desk | 82 | Compact hard proof and deposit release. | Niche, slower, guarantee associations and freight forwarders own workflow. |
| EMCS Excise Guarantee Discharge Desk | 81 | Similar guarantee-release logic. | Excise/alcohol/tobacco/energy regulation is too specialized and risky. |
| Letter of Credit Discrepancy Cure Desk | 80 | Direct payment release and documentary control. | Bank/trade-finance trust barrier for unknown founder. |

## Chosen Candidate

Idea name: OpenMRN Transit Guarantee Release Desk

One-sentence thesis: Clear old undischarged NCTS transit MRNs for small customs agents and freight forwarders whose comprehensive guarantee balance is locked, selling MRN-specific discharge packets that end in official write-off notifications and credited guarantee capacity.

Exact buyer: Small EU/UK customs agents, freight forwarders, bonded logistics operators, and high-volume import/export principals that hold or use a transit comprehensive guarantee and have a queue of NCTS movements not discharged within normal timing.

Acute trigger: The buyer's NCTS guarantee balance is partly consumed by open/undischarged MRNs, and new T1/transit movements can be rejected or constrained when the guarantee reference amount is insufficient. Manual NCTS Phase 5 closures and enquiry procedures can prolong blocked capacity.

Control point: A signed MRN-specific recovery mandate plus the buyer's open-MRN export, guarantee balance evidence, TAD/CMR/POD/delivery/arrival proof, office of departure/destination details, and authority correspondence. The controlled asset is not a report; it is an assigned queue of MRNs with official discharge/write-off as the target artifact.

60-day signed/titled/assigned/prepaid proof:

- Three buyers sign mandates assigning at least 80 open MRNs for cleanup.
- Each buyer pays a setup fee and authorizes portal/email correspondence or contractor customs-agent representation where required.
- First 15-25 MRNs receive IE045/write-off notifications, discharge letters, cancellations, or other authority confirmation that releases reserved guarantee capacity.
- First success invoices are issued against freed guarantee reference amount or per-MRN closure.

6-month POC:

- Work one corridor first: UK/EU or Poland/Germany/Benelux transit movements where language and customs-office routing can be handled.
- Process 300-500 assigned MRNs across 8-15 buyers.
- Build a repeatable evidence checklist by closure type: missing destination control result, duplicate movement, destination presented but not arrived in NCTS, manual Phase 5 closure, proof-of-destination enquiry, cancellation, or discrepancy resolution.
- Prove aggregate released guarantee capacity of 2-5 million EUR equivalent and 75,000-150,000 EUR revenue.

Economics:

- Setup fee: 750-2,000 EUR per buyer for open-MRN ledger intake and triage.
- Success fee: 150-450 EUR per discharged MRN depending on age, country pair, and required evidence, or 1-3 percent of freed guarantee capacity for high-value movements with a per-MRN cap.
- Gross margin target: 70-85 percent before founder time, using customs-agent contractors only where formal representation is needed.
- Cash conversion: setup fee before work, success fee after authority confirmation or guarantee balance credit.
- Buyer payback: if blocked guarantee capacity prevents even a small number of new transit movements, a few discharged MRNs can justify the fee.

Copy risk:

Customs agents and forwarders can do this internally, and many will for simple cases. The wedge is their backlog: old MRNs are tedious, multilingual, cross-office, and low-status until the guarantee line constrains live revenue. The POC must target buyers with a visible open-MRN queue and guarantee-capacity pain, not importers with one-off curiosity.

Why incumbents cannot copy before the founder controls the specific asset/account/case/claim/lot/payment stream:

Once the buyer assigns a queue of MRNs under mandate and pays intake, the founder controls the case ledger, evidence requests, authority correspondence chronology, and per-MRN discharge workflow. Another advisor can copy the method, but not the already-assigned MRN queue, buyer authorization, or pending authority cases.

Why it is not a service, report, app, dashboard, database, marketplace, or generic broker:

The deliverable is official closure: IE045/write-off notification, discharge letter, cancellation acceptance, or guarantee balance credit. The buyer pays for released guarantee capacity and closed MRNs, not a dashboard or advisory memo. There is no marketplace and no introduction brokerage.

Boundaries and legal/provider limits:

- The startup does not act as customs declarant, guarantee holder, or legal representative unless a properly licensed/authorized customs-agent contractor is engaged.
- The buyer remains holder of the procedure and principal for customs purposes.
- The startup does not certify customs status, alter records, or give legal advice on customs debt.
- Work is limited to evidence collection, authorized correspondence, procedural follow-up, and contractor-managed customs representation where required.

Duplicate risk:

Not CBAM Import Continuity Desk: this is not import compliance evidence for new carbon reports or live goods release. The control point is already-open NCTS transit MRNs and the economic artifact is freed guarantee capacity. Not PromoLeak or recovery of retailer deductions. Not a generic freight audit because it is tied to official customs discharge/write-off and guarantee balance release.

Strongest anticipated objections:

- Customs agents and forwarders already know how to close MRNs and may only outsource low-value messes.
- The founder may lack trust and customs authority to correspond effectively.
- Authority timelines can exceed 60 days, especially for old cross-border enquiries.
- Some MRNs may reflect real irregularities or missing goods, not clerical closure problems.
- Success fees may be hard to link to a guarantee balance release if the buyer does not have clean guarantee reporting.
- This could become tedious customs admin consulting unless the mandate, MRN queue, and official release proof are tight.

## Internal Score

Simulated score: 88.5

Reason for passing simulation gate: This is closer to the desired "ugly finance/admin-heavy control" shape than prior customs ideas: the buyer has a live guarantee balance constraint, cases are assignable by MRN, and success is an official write-off/guarantee credit rather than a nicer document pack. It stays below 90 because customs incumbents are strong and authority timing may be slow.

Gate decision: advance to working Zero To One validation.

## Kill Criteria

- Working score below 85.
- Reviewer says customs agents already own the pain and would not outsource.
- Reviewer says authority timeline makes 60-day proof unrealistic.
- Reviewer says the founder cannot legally or credibly control the case queue without becoming a customs representative.
