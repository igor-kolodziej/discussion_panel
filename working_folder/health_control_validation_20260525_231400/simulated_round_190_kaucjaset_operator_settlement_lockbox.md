# Simulated Round 190: KaucjaSet Operator Settlement Lockbox

Date: 2026-05-29
Real browser gates: working Zero To One `>=85`, fresh Zero To One `>=85`

## Search Frame

Recent failures show that "signed route," "slot," "option," or "evidence file" is not enough when the payor can ignore the founder or incumbents already own the channel. This round tests a live Polish cash-settlement transition: the deposit-return system launched in October 2025 and has been scaling through 2026, with retailers and collection points receiving operator-side cash for customer deposit refunds and handling activity.

The lead candidate is not a DRS compliance advisory. It only advances if the control object is a named retailer/collection-point settlement batch: operator agreement, return-count logs, bag/RVM/POS evidence, accepted line items, payment direction or mandate, and first cash from the operator.

## Raw Candidate Control Table

| # | Candidate | Buyer/payor | Acute trigger | Transferable control point | 60-day proof | Acquisition | Economics | Copy risk | Why incumbent cannot copy exact stream first | Why not service/report/app/broker | Internal score |
|---:|---|---|---|---|---|---|---|---|---|---|---:|
| 1 | KaucjaSet operator settlement lockbox | small retail chains / DRS collection points | operator settlement delayed or mismatched | operator agreement, return logs, accepted settlement, payment mandate | 15 sites, operator acknowledgement, first paid batch | retail accountants/franchisees | fee on settlement/recovery | operators/POS/accountants | exact batch/payment direction controlled | current settlement cash | 88.1 |
| 2 | Retailer DRS reimbursement claim purchase | shops | deposit-refund reimbursement delayed | assigned operator claim | operator acknowledgement | convenience store groups | discount | assignment may be barred | assigned claim | receivable purchase | 83 |
| 3 | DRS handling-fee recovery desk | collection points | handling fee underpaid | return-count logs, operator claim | first fee correction | store associations | success fee | operators fix portals | current claim | recovery | 80 |
| 4 | DRS RVM uptime credit recovery | retailers with machines | service credits missed | RVM contract/incident logs | first credit | RVM service users | recovery share | RVM vendors | current credit | credit recovery | 73 |
| 5 | DRS glass-crate deposit float reclaim | shops | reusable glass deposits not reconciled | crate/bottle ledger | first refund | beverage distributors | fee | distributors | exact ledger | claim | 70 |
| 6 | DRS event collection settlement rail | event operators | temporary points owed refunds/fees | event contract, count logs | first payout | festivals/venues | fee | operators | event batch | settlement cash | 74 |
| 7 | DRS franchisee operator contract transfer | franchise chains | site closures/changeover | contract assignment + first settlement | current batch | franchise admins | admin fees | chains internalize | specific sites | contract transfer | 72 |
| 8 | Deposit-mark SKU onboarding release | beverage producers | products missing mark/contract | operator enrollment file | paid sprint | producers | fee | compliance firms | current SKU file | evidence/service | 68 |
| 9 | DRS unclaimed deposit VAT settlement review | producers/operators | first annual settlement confusion | accounting workpapers | refund/correction | tax advisers | fee | tax firms | no hard control | tax service | 58 |
| 10 | POS deposit-line correction release | retailers | receipts/POS wrong deposit split | POS evidence + vendor ticket | corrected rollout | POS vendors | fee | POS vendors | current ticket | implementation support | 60 |
| 11 | RVM packaging rejection claim | retailers | machine rejects valid items | machine logs + operator claim | first operator correction | retailers | recovery | RVM vendors | exact logs | claim | 67 |
| 12 | Deposit packaging count audit | operators/retailers | count discrepancies | bag seals/RVM/POS logs | first adjusted batch | collection points | fee | operators | batch files | audit/recovery | 75 |
| 13 | DRS cash-float advance for microshops | small shops | consumer refunds before operator payout | operator acknowledgement | first repayment | microshops | financing margin | lending/licensing | repayment right | receivable finance | 62 |
| 14 | Municipal DRS public-point settlement | municipalities | public collection points owed operator funds | operator agreement, count logs | first payout | municipalities | fee | slow procurement | batch controlled | settlement support | 60 |
| 15 | DRS fraud/no-go triage desk | operators | suspicious return claims | evidence review | no-go fee | operators | fee | operators internalize | case file | service | 55 |
| 16 | EPR packaging registration release | marketplace sellers | EPR evidence blocks listing | provider evidence | listing progress | agencies | fee | EPR providers | current case | evidence desk | 76 |
| 17 | BDO DPR/EDPR allocation | recyclers/buyers | document allocation value | source mandate | paid allocation | waste sources | fee/spread | failed 62 | source stream | regulated doc | 62 |
| 18 | UCO locked route | recyclers/restaurants | UCO route value | site contracts | paid pickup | kitchens | spread | failed 56 | route | physical stream | 56 |
| 19 | Pallet deposit ledger reclaim | distributors | deposit balances stranded | ledger assignment | first refund | warehouses | discount | pool operators | exact ledger | claim | 71 |
| 20 | Returnable IBC deposit reclaim | food/chemical SMEs | IBC deposits stuck | title/account ledger | first refund | warehouses | spread | container firms | exact IBCs | claim/lot | 70 |
| 21 | Gas-cylinder deposit reclaim | Horeca | cylinder deposits unused | cylinder title/deposit docs | first supplier refund | restaurant closures | spread | suppliers | exact cylinders | lot/claim | 63 |
| 22 | Keg deposit reclaim | bars/breweries | dormant kegs | title/deposit docs | first refund | bar closures | spread | brewers | exact kegs | lot/claim | 64 |
| 23 | Utility deposit refund purchase | closed SMEs | deposit refund ignored | assigned refund | utility acknowledgement | liquidators | discount | low ticket | exact refund | receivable | 62 |
| 24 | Commercial lease deposit reclaim | SMEs leaving premises | landlord deposit held | assigned deposit claim | landlord acknowledgement | relocation firms | discount | lawyers | exact deposit | claim purchase | 70 |
| 25 | Security deposit account sweep | franchise networks | many small deposits | claim batch | first refund | franchise accountants | fee | accountants | batch | recovery | 66 |
| 26 | Court-deposit reclaim purchase | SMEs/insolvencies | money in deposit account | assigned claim | court acknowledgement | lawyers | discount | legal friction | exact claim | claim purchase | 58 |
| 27 | Bailiff overpayment refund | creditors/debtors | overpaid enforcement costs | refund order | first payment | lawyers/accountants | fee | legal | exact refund | legal-adjacent | 55 |
| 28 | Insurance premium return lockbox | businesses changing policies | return premium due | insurer statement | first refund | brokers | fee | brokers | exact receivable | claim | 62 |
| 29 | Software marketplace withholding release | SaaS vendors | payout mismatch | support case + mandate | first payout | SaaS accountants | fee | platforms | case | platform recovery | 64 |
| 30 | App store tax/VAT payout correction | app vendors | payout tax mismatch | store reports | credit | app accountants | fee | app accountants | claim | recovery | 60 |
| 31 | Payment gateway reserve maturity release | merchants | reserve due | processor acknowledgement | first release | risky merchants | fee | PSP/admin | failed 70 | reserve | recovery | 70 |
| 32 | COD courier remittance recovery | ecommerce sellers | COD remittance gaps | parcel remittance claims | first payout | sellers | recovery | couriers | failed 64 | claim | recovery | 64 |
| 33 | OTA VCC settlement recovery | hotels | virtual card/commission mismatch | PMS/OTA claim | first credit | hotels | recovery | revenue managers | failed 76 | claim | recovery | 76 |
| 34 | Public grant claim release | SMEs | grant tranche delayed | claim correction | payment | grant advisers | fee | failed 76 | case | cash release | 76 |
| 35 | Warranty/RMA credit queue | installers | credits unpaid | RMA cases | first credit | PV/HVAC installers | recovery | OEM portals | failed 72 | claim | recovery | 72 |
| 36 | Merchant acquirer residual buyout | agents | residual stream transfer | payor approval | first residual | agents | cashflow buyout | failed 64 | stream | asset purchase | 64 |
| 37 | Retail EDI book buyout | suppliers | order flow continuity | customer-approved payment transfer | prepaid continuity | micro-EDI sellers | recurring | failed 73 | book | micro-acquisition | 73 |
| 38 | Shopify app continuity buyout | merchants | app seller exits | listing/source/billing | first payout | app sellers | MRR | failed 72 | listing | app asset | 72 |
| 39 | AIQ partner ticket book | SOC2/fCISO partners | AI buyer blockers | partner routing/prepay | paid tickets | partners | fees | failed 82/67 variants | slots | expert service | 67 |
| 40 | Cyber subjectivity case book | brokers/MSPs | bind/renewal blocker | case routing/payment | paid cases | brokers | fee | failed 70/82 | case book | evidence artifact | 70 |

## Finalists

| Finalist | Internal simulated score | Advance? | Reason |
|---|---:|---|---|
| KaucjaSet Operator Settlement Lockbox | **88.1** | **Yes** | Most current and hard-cash version: new national system, live operator settlements, named return-count batches, payment direction, and first operator cash rather than generic compliance. |
| Retailer DRS Reimbursement Claim Purchase | 83 | No | Similar but too close to factoring and likely blocked by operator assignment rules. |
| DRS Handling-Fee Recovery Desk | 80 | No | Real but likely admin recovery that operators/POS/accountants can internalize. |
| Deposit Packaging Count Audit | 75 | No | Useful but service-like unless tied to payment direction. |
| Pallet/IBC Deposit Reclaim | 70-71 | No | Lower urgency, smaller tickets, known incumbents. |

## Lead Candidate

**KaucjaSet Operator Settlement Lockbox**

### Internal Score Rationale

This clears simulation only in the strict operator-acknowledged version. It is not DRS readiness, POS implementation, packaging registration, VAT advice, or a retailer dashboard. It controls a named cash settlement batch between a collection point and a deposit-system operator.

The first wedge is a retailer, franchisee, food-service collection point, or small retail chain that already has:

- operator agreement;
- return-point activity;
- bag/RVM/POS count logs;
- consumer refund records;
- operator portal/statement;
- missing, delayed, or mismatched operator reimbursement or handling-fee cash.

The founder accepts only cases where the operator's settlement path is visible and the retailer authorizes payment direction, mandate, or lockbox handling for a current batch. The proof is first operator cash, not a reconciliation report.

Main internal doubts:

- operators may prohibit assignment or third-party payment direction;
- accountants, POS vendors, operators, and franchise HQs may own the workflow;
- batch values may be small;
- fraud/count disputes can kill trust;
- the system may stabilize quickly as portals improve;
- a founder can get stuck in count reconciliation and customer-refund admin.

If Zero To One treats this as ordinary DRS admin or low-margin receivables chasing, kill the branch.

## Gate Decision

Advance Round 190 to working Zero To One validation.
