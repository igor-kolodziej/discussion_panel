# Simulated Round 300: CAPE IEEPA Refund Batch Desk

Date: 2026-05-31 Europe/Warsaw

Gate policy:

- Simulated score must be strictly greater than 87 before real Zero To One validation.
- Working-chat and fresh-chat Zero To One gates are both >=85.
- Internal scoring caps are used only in this simulation note, not in the validation prompt.

## Why This Branch

Round 299 failed fresh validation because PSE PV compensation is a public official workflow where O&M firms and asset managers sit closer to the necessary data. Current cash was not enough when the workflow was public, local incumbents could absorb it, and the batching mechanic already existed in the official process.

Round 300 tests a larger and more acute refund queue: U.S. Customs and Border Protection's CAPE process for IEEPA duty refunds. The narrow validated version is not customs law, tariff advice, or filing by an unlicensed intermediary. It is a broker-routed data-prep and status-control desk for importers and customs brokers with current refundable-duty batches.

Official/current source check:

- CBP announced that on April 20, 2026 it would launch the first phase of CAPE inside the ACE Secure Data Portal for IEEPA duty refund requests.
- CBP says CAPE consolidates IEEPA duty refunds including interest instead of processing entry-by-entry refunds.
- CBP says IORs and authorized customs brokers submit CAPE declarations, and once accepted CBP removes the IEEPA HTS number, recalculates duties, updates the entry, and liquidates/reliquidates.
- CBP says CAPE Phase 1 is limited to certain unliquidated entries and entries within 80 days of liquidation, implying entry screening and exception classification are operationally important.

Source:

- `https://content.govdelivery.com/accounts/USDHSCBP/bulletins/4126a9c`

## Raw Candidate Control Table

| # | Candidate | Buyer / payer | Acute trigger | Transferable control point | 60-day signed/titled/assigned/prepaid proof | First acquisition mechanism | Gross margin and payback logic | Copy risk | Why incumbents cannot copy before control | Why not service/report/app/dashboard/marketplace/broker |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | CAPE IEEPA refund batch desk | Importers of record and customs brokers | CAPE opened for IEEPA refunds; brokers/importers have many eligible entries | IOR/broker mandate, ACE entry exports, CAPE-ready entry batch, filed declaration status, refund ledger | 3 broker/IOR mandates, 500 entries screened, 100 accepted declarations, first refund/status outcomes | Trade groups, US customs brokers, CEE brands with US IORs | 1k-5k USD setup + per-entry + small success; huge refund values | customs brokers, trade lawyers, Big4, tariff consultants | exact ACE/export/refund batch and authority controlled | cash refund operations, not law or software |
| 2 | EIT Manufacturing beneficiary claim packet | EIT beneficiaries | liquidation claims deadline | beneficiary claim file and French translation | 10 claim files | EIT project networks | decent but one-off/legal | lawyers/grant consultants | exact claim controlled | legal liquidation risk |
| 3 | Polish FOR agri unpaid-invoice compensation desk | farmers/groups | July/Aug 2026 FOR compensation window | invoices and insolvent buyer evidence | 20 farmer mandates | producer groups | low/medium | agri advisors | exact claims | public form/low fee |
| 4 | EUIPO SME Fund reimbursement desk | SMEs with vouchers | voucher claim before expiry | EUIPO voucher and invoice files | 30 reimbursements | IP firms | low | IP reps | exact vouchers | admin low ticket |
| 5 | FDA/CBP duty drawback catch-up | US importers/exporters | unused drawback periods | broker/export records | 5 mandates | customs brokers | high but mature | drawback specialists | exact entry/export set | legal/customs |
| 6 | Section 301/232 exclusion refund queue | US importers | exclusions/refunds available | entry data and exclusion basis | 5 mandates | brokers | high but mature | trade lawyers | exact entries | legal/customs |
| 7 | Post-Brexit UK import VAT C79 recovery desk | importers | missed postponed VAT entries | VAT/C79 data | 10 files | accountants | medium | accountants | exact VAT files | tax advice risk |
| 8 | German electricity price brake clawback support | energy users | government support reconciliation | invoices/reconciliation | 5 files | energy accountants | medium | advisors | exact claim | public/tax |
| 9 | EU ETS free allocation correction queue | installations | allocation/account correction | Union Registry/operator file | 3 cases | ETS advisers | high but specialist | consultants | exact registry | regulated |
| 10 | UK plastic packaging tax refund correction | importers/manufacturers | overpaid PPT | tax files | 8 cases | accountants | medium | tax advisors | exact return | tax |
| 11 | EU CBAM importer authorisation fallback | importers | authorisation pending, import continuity | importer file | 5 cases | brokers | high but duplicate | CBAM firms | exact shipment | duplicate/CBAM |
| 12 | US FDA import hold reconditioning refund | food/device importers | goods held/reexported | FDA/CBP hold file | 4 cases | brokers | high but specialist | FDA brokers | exact hold | regulated health/food |
| 13 | Amazon low-inventory placement fee dispute recovery | FBA sellers | new fee misapplication | seller reports/cases | 8 cases | Amazon agencies | medium | agencies | exact account | platform discretion |
| 14 | Walmart deductions shortage recovery queue | vendors | deduction register | portal access/claims | 8 cases | vendor agencies | medium | incumbents | exact claims | similar retail deductions |
| 15 | TikTok Shop reserve release | sellers | payout reserve/policy hold | seller account case | 8 cases | agencies | medium | agencies | exact account | platform discretion |
| 16 | Booking.com DAC7 payout release | hosts/hotels | tax verification payout hold | account docs/case | 10 cases | property managers | medium | OTAs/PMs | exact account | platform KYC |
| 17 | EU travel package airline refund batch | agencies | cancelled flights/groups | booking/claim file | 20 claims | travel agencies | low | claim firms | exact bookings | mature |
| 18 | Commercial card interchange settlement claims | merchants | settlement claim deadline | merchant records | 20 claims | merchant services | medium | claim admins | exact merchant file | legal/class action |
| 19 | Visa/Mastercard assessment fee refund | merchants | acquirer acknowledged error | merchant statement | 8 cases | payment consultants | medium | consultants | exact MID | payments incumbent |
| 20 | Overwithheld marketplace tax refund queue | sellers | platform tax overwithheld | seller tax/payment docs | 8 cases | accountants | medium | accountants | exact account | tax |
| 21 | SaaS reseller partner rebate release | software partners | vendor rebate held | partner portal/PO data | 6 cases | channel consultants | medium | partner ops | exact portal | previous failed branch |
| 22 | Telecom USF/surcharge refund desk | enterprise telecom buyers | surcharge misapplication | bills/contracts | 6 cases | telecom auditors | medium | auditors | exact bills | mature audit |
| 23 | Utility closed-account deposit refund | multi-site businesses | deposits stranded | account closure data | 20 accounts | facility managers | low | accountants | exact accounts | low ticket/failed style |
| 24 | Commercial lease CAM audit cashout | tenants | reconciliations due | lease/CAM statements | 5 tenants | lease auditors | medium | auditors/lawyers | exact lease | mature |
| 25 | Insurance audit return premium release | businesses | premium audit finalized | broker/insurer file | 5 cases | brokers | medium | brokers | exact file | prior branch failed |
| 26 | Customs broker CAPE white-label status desk | small customs brokers | CAPE claim backlog | broker mandate, ACE exports, status ledger | 2 brokers, 300 entries | broker associations | strong | brokers internalize | exact broker queue | back-office operations |
| 27 | Surety-paid IEEPA refund direction desk | import sureties | refunds may go to importers not sureties | surety/importer evidence | 3 cases | surety firms | high but legal | surety lawyers | exact paid duty file | legal dispute |
| 28 | Foreign-trade-zone IEEPA exception triage | FTZ importers | CAPE phase exclusions | FTZ entry sets | 3 cases | FTZ advisors | high but specialist | FTZ consultants | exact zone data | legal/customs |
| 29 | De minimis parcel duty refund batch | e-commerce importers | tariff reform/claims | parcel entry data | 10 cases | brokers | medium | parcel brokers | exact data | uncertain |
| 30 | IOSS VAT overpayment recovery | EU ecommerce sellers | VAT/import mismatch | IOSS and platform data | 8 cases | VAT reps | medium | tax reps | exact IOSS | tax |
| 31 | Export VAT blocked refund file | Polish exporters | missing export confirmation | VAT/JPK/export docs | 8 cases | accountants | medium | tax advisors | exact VAT file | tax/legal |
| 32 | Split-payment VAT account release | Polish businesses | VAT account funds trapped | bank/tax file | 10 cases | accountants | medium | tax advisors | exact tax file | legal/tax |
| 33 | Renewable certificate account correction | RES owners | registry/certificate mismatch | registry mandate | 5 cases | energy advisors | medium | advisors | exact account | narrow |
| 34 | Product recall cost reimbursement queue | distributors | OEM approved reimbursement | serial/invoice file | 6 cases | distributors | medium | OEM dealers | exact serial claims | warranty incumbents |
| 35 | Channel MDF approved-claim cashout | resellers | approved MDF not paid | portal/PO proof | 8 cases | channel agencies | medium | channel ops | exact portal | prior failed MDF |
| 36 | Rail freight damage accepted-claim cashout | shippers | carrier accepted claim but unpaid | carrier claim file | 8 cases | freight auditors | medium | auditors | exact claim | mature freight |

## Finalists

| Candidate | Internal simulated score | Advance? | Rationale |
|---|---:|---|---|
| CAPE IEEPA refund batch desk | **88.2** | **Yes** | Massive current cash pool, official new portal, entry screening, importer/broker authority, accepted-declaration/refund-status proof. Stronger than ordinary customs consulting if sold as broker-routed data operations and status control. |
| Customs broker CAPE white-label status desk | 87.0 | No | Same branch, slightly stronger channel but too dependent on brokers that can internalize. Does not strictly exceed the simulated gate. |
| Surety-paid IEEPA refund direction desk | 84.5 | No | Potentially high-value but becomes legal dispute over refund recipient. |
| EIT Manufacturing beneficiary claim packet | 83.0 | No | Current deadline and cash, but one-off liquidation/legal process. |
| Polish FOR agri unpaid-invoice compensation desk | 81.5 | No | Current statutory compensation window, but low-ticket public forms and agri advisers make it weak. |
| Section 301/232 exclusion refund queue | 80.5 | No | Mature customs refund field with established incumbents. |

## Lead Candidate

Idea name: **CAPEClaim IEEPA Refund Batch Desk**

### Buyer

Primary buyer: importers of record that paid IEEPA duties and have eligible or potentially eligible entries in ACE/CAPE Phase 1, especially CEE/EU brands, distributors, and manufacturers with U.S. importer-of-record exposure but thin internal U.S. customs operations.

Channel buyer: small and mid-sized U.S. customs brokers whose importer clients have many CAPE-eligible entries but whose teams are overloaded by entry screening, ACH setup checks, CAPE batch preparation, status reconciliation, importer communication, and exception triage.

### Acute Trigger

CBP opened CAPE Phase 1 in ACE for IEEPA refunds on April 20, 2026. Importers and authorized customs brokers need to identify eligible entries, confirm ACE/ACH refund setup, prepare CAPE declarations, handle accepted/rejected statuses, track liquidation/reliquidation and refund dates, and reconcile actual refund amounts. Missed eligible entries or rejected declarations delay cash.

### Transferable Control Point

The startup only controls a case when it has:

- importer or broker authorization for named importer-of-record accounts and entry ranges;
- ACE/exported entry data supplied by the importer or authorized broker;
- prepaid batch fee;
- broker/IOR-approved eligibility screen and exclusion map;
- CAPE declaration worklist prepared for the licensed/authorized filer;
- status ledger for accepted, rejected, pending, liquidated/reliquidated, refund-issued, and exception entries;
- success fee tied only to accepted declarations or received refunds where attribution is explicit.

The startup does not file customs declarations unless the authorized broker or IOR does so in ACE. It does not provide customs legal opinions.

### 60-Day Proof

- Three signed importer or broker mandates.
- 500 entry lines screened.
- 150 entries passed to authorized broker/IOR as CAPE-ready batches.
- 75 accepted CAPE declarations or accepted/rejected status outcomes documented.
- At least one importer refund status or refund payment event traced.
- 60,000-180,000 PLN equivalent collected in prepaid batch fees and clearly attributed success fees.
- One licensed customs broker or trade-compliance reviewer retained for boundary review.

### Economics

Pricing:

- 2,000-5,000 USD importer setup and ACE/ACH/refund-readiness screen.
- 1-3 USD per entry screened for larger batches.
- 15-50 USD per CAPE-ready entry passed to the authorized filer, depending on data quality.
- 2-6% success fee on refunds actually received only when the before-state entry list and after-state refund trace support attribution.

The importer pays because refunds are direct cash, and late or rejected CAPE declarations delay money. Brokers pay or resell because entry cleanup, importer communication, ACH readiness, status tracking, and exception ledgers are operationally heavy but not strategic legal advice.

### Copy Risk

Customs brokers, trade lawyers, Big4 customs teams, tariff-recovery specialists, and importer trade-compliance teams can copy the workflow. The defense is broker-routed batch execution, CEE/EU importer discovery, CAPE entry-screening workpapers, accepted/rejected status memory, and signed control over exact importer entry batches during a time-sensitive refund window.

### Why Incumbents Cannot Copy Before Control

Once a broker or importer authorizes a named importer account and entry date range, supplies ACE exports, approves the worklist, and pays the batch fee, the exact refund-control object is locked: entry numbers, IOR authority, ACE/ACH readiness status, CAPE declaration worklist, acceptance/rejection history, and refund-status ledger. Competitors can copy the general CAPE workflow, but they cannot access or submit the same batch without the importer or broker switching mid-process.

### Internal Score

Simulated score: **88.2 / 100**

Reasoning:

- Acute current cash: very strong. CAPE is live, refund-related, and tied to court-ordered IEEPA duty refunds.
- Control point: strong at batch level if authority, entry data, and status ledger are signed and prepaid.
- CAC/payback: plausible through small brokers, trade groups, importers with public tariff exposure, and CEE/EU companies with U.S. importer-of-record status.
- Margin: strong if work is data operations plus reviewer boundary checks, not legal disputes.
- Copy risk: high, but time-sensitive entry-batch control and broker overflow partially offset it.
- Main cap: U.S. customs credibility, broker/incumbent proximity, one-time window, and risk that many importers/brokers can use CAPE without help.

### Kill Criteria

- Fewer than three paid mandates in 60 days.
- Fewer than 150 entries prepared for authorized CAPE filing.
- Fewer than 75 accepted/rejected CAPE status outcomes.
- No refund-status or refund-payment trace.
- More than 40% of entries require legal/customs interpretation beyond supplied broker guidance.
- Gross margin below 60% after reviewer and data-cleanup costs.
- Any pressure to file as an unauthorized customs broker, provide legal tariff opinions, route refunds to the startup, or handle disputed surety/importer recipient issues.

## Validation Decision

Advance Round 300 to real working-chat Zero To One validation because the simulated score is strictly greater than 87 and the candidate is materially different from exhausted KSeF, PSE, generic evidence-desk, platform-credit, and ordinary invoice-recovery branches.
