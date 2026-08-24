# Simulated Round 93: Acknowledged Claim / Refund / Payout Flows

Date: 2026-05-27

## Pivot From Round 92

KSC Customer Renewal Evidence Pack failed working-chat validation at `75 / 100`.

Reason to pivot: evidence tickets keep scoring as useful but not confirmed because they lack hard payment/control. This round returns to already-owed money, but only where the debtor or payer has acknowledged the obligation and the founder can get assignment, payment direction, or collection mandate before capital is exposed.

## Raw Candidates

| # | Candidate | Buyer | Acute trigger | Transferable control point | Signed/titled/assigned/prepaid inside 60 days | First acquisition mechanism | Margin / payback logic | Copy risk and why incumbents cannot copy before control | Why not wrapper |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Approved Commercial Insurance Payout Lockbox | SMEs, repair/restoration contractors, brokers | Insurer has approved payout but cash is delayed and repair/vendor needs certainty | Assignment or payment-direction over insurer-approved non-litigated claim | Insurer approval, cedent assignment, debtor acknowledgement/payment direction | Brokers, loss adjusters, restoration contractors | 5-15% spread/fee on near-term payout | Factoring/claims firms exist; debtor acknowledgement and signed assignment lock the specific payout | Named receivable |
| 2 | Approved Cargo Insurance Payout Lockbox | Importers/forwarders | Cargo insurer approved loss payment, customer waits | Assignment over approved payout | Insurer approval, claim number, assignment | Freight brokers/adjusters | 5-15% | Claims handlers copy; must be approved, not disputed | Named claim |
| 3 | Repair-Shop Insurer Direct-Pay Book | Body shops/commercial repairers | Insurer authorizes repair but pays late | Direct payment assignment from customer/insurer | Repair approval, assignment, payment direction | Body shops | 5-12% | Crowded auto claims market | Named payout |
| 4 | Approved Warranty Credit Note Collection | Distributors | Manufacturer issued credit note but cash delayed | Assignment/mandate over credit note | Credit note, debtor acknowledgement | Accountants/distributor consultants | 10-20% | Generic credit collection | Named credit |
| 5 | Public Late-Payment Interest Assignment | Public contractors | Principal paid late; statutory interest unpaid | Assignment/mandate over interest claim | Paid invoice, payment date, debtor non-dispute | Public procurement accountants | 20-35% | Legal/debt collectors copy | Named claim |
| 6 | Customs Refund Decision Lockbox | Importers | Customs/tax decision grants refund | Assignment/payment mandate | Refund decision, authority status | Customs brokers | 5-15% | Public debtor assignment may fail | Named refund |
| 7 | Excise Deposit Refund Mandate | Fuel/alcohol/energy traders | Excise guarantee/deposit return approved | Mandate over refund | Tax decision, assignment | Tax advisors | 5-15% | Legal/accounting copy | Named refund |
| 8 | Utility Connection Fee Refund Lockbox | Developers/industrial SMEs | Utility acknowledged connection/project refund | Assignment/payment direction | Utility acknowledgement, invoices | Construction accountants | 10-20% | Legal/admin copy | Named refund |
| 9 | Warehouse Security Deposit Return Lockbox | Tenants exiting warehouse | Handover done; deposit return acknowledged | Assignment/mandate over deposit | Handover protocol, landlord email | CRE brokers | 5-15% | Low moat, legal risk | Named deposit |
| 10 | B2B Software Refund Assignment | SMEs | SaaS vendor accepted termination/refund | Assignment over accepted refund | Vendor email/credit memo | IT advisors | 10-20% | Small fragmented claims | Named refund |
| 11 | Marketplace Reserve Release Mandate | Merchants | Platform reserve approved or scheduled | Mandate/success fee on release | Platform message, payout proof | Ecommerce accountants | 10-20% | Platform ignores assignments | Named reserve |
| 12 | Carrier Approved Credit Note Lockbox | 3PLs/merchants | Carrier issued approved credit | Mandate over approved credit | Credit note, carrier portal | Freight accountants | 10-20% | Similar failed carrier credit | Named credit |
| 13 | Demurrage Deposit Refund Mandate | Importers | Container/depot deposit due | Mandate over refund | Deposit receipt, return proof | Freight forwarders | 10-20% | Small tickets | Named refund |
| 14 | Energy Supplier Overcharge Credit Lockbox | SMEs | Supplier accepted overbilling credit | Assignment/mandate | Credit note, debtor email | Energy brokers | 10-20% | Energy brokers/accountants copy | Named credit |
| 15 | Telecom SLA Credit Mandate | Enterprises | Operator accepted SLA credit | Mandate over credit/cash | SLA credit memo | Telecom brokers | 10-20% | Low ARPU/copyable | Named credit |
| 16 | Retailer Approved Deduction Reversal | FMCG brands | Retailer accepted invalid deduction | Assignment/mandate over credit/cash | Retailer credit note | Trade-spend consultants | 10-20% | PromoLeak duplicate | Named credit |
| 17 | Insurer Subrogation Recovery Share | Fleet owners | Insurer/subrogation settlement acknowledged | Assignment over recovery balance | Settlement letter | Fleet brokers | 5-15% | Legal/insurer complexity | Named recovery |
| 18 | Court Registry Deposit Refund | SMEs/law firms | Court deposit/security return approved | Mandate over refund | Court order, payment details | Lawyers/accountants | 5-15% | Legal trust; low volume | Named refund |
| 19 | Bailiff Overpayment Refund Mandate | Debtors/SMEs | Enforcement overpayment acknowledged | Mandate | Bailiff statement | Lawyers | 10-20% | Sensitive/debt/legal | Named refund |
| 20 | Construction Performance Bond Release | Contractors | Beneficiary approved bond/cash guarantee release | Assignment/payment direction | Release letter | Construction accountants | 5-15% | Banks/guarantors/retentions; similar failures | Named release |
| 21 | Warranty Retention Release Lockbox | Contractors | Retention acknowledged due | Assignment/payment direction | Handover, debtor acknowledgement | Accountants | 10-20% | Already failed 67 | Named receivable |
| 22 | Insurance Premium Return Assignment | Businesses cancelling policies | Insurer issued premium-return notice | Assignment/mandate | Insurer notice | Brokers | 5-10% | Small/copyable | Named refund |
| 23 | Fleet Total-Loss Payout Assignment | Fleet SMEs | Insurer total-loss amount approved | Assignment/payment direction | Insurer decision, title path | Fleet brokers | 5-12% | Auto claims market crowded | Named claim |
| 24 | Property Claim Progress-Payment Lockbox | Contractors | Insurer approved staged restoration payment | Payment direction for approved tranche | Insurer approval, contractor invoice | Restoration firms | 5-12% | Direct-pay contractors exist | Named tranche |
| 25 | Bank Fee Refund Mandate | SMEs | Bank accepted fee/refund complaint | Mandate over refund | Bank acknowledgement | Accountants | 10-20% | Small | Named refund |
| 26 | Card-Acquirer Reserve Release Assignment | Merchants | Acquirer has scheduled reserve release | Assignment/payment direction | Acquirer notice | PSP consultants | 5-15% | PSP anti-assignment likely | Named reserve |
| 27 | Leasing Overpayment Refund Lockbox | SMEs | Leasing company acknowledged overpayment/end settlement | Assignment/mandate | Settlement statement | Accountants | 5-15% | Small/copyable | Named refund |
| 28 | Rental Damage Deposit Refund Book | Equipment rental customers | Deposit due after return accepted | Mandate over refund | Return protocol | Rental brokers | 10-20% | Small/fragmented | Named deposit |
| 29 | Insurance Deductible Reimbursement Claim | SMEs | Third party accepted reimbursement | Assignment | Acceptance letter | Brokers | 10-20% | Legal messy | Named claim |
| 30 | Approved Grant Reimbursement Bridge | SMEs/nonprofits | Grant administrator approved reimbursement | Assignment/bridge with grant acknowledgement | Approval letter, payment status | Grant consultants | 5-12% | Factoring/legal; public payment assignment | Named receivable |
| 31 | EU Project Cost Reimbursement Lockbox | SMEs/universities | Cost reimbursement approved but paid later | Assignment/mandate | Approval, debtor status | Grant advisors | 5-12% | Public debtor, legal complexity | Named receivable |
| 32 | Approved Export Credit Insurance Payout | Exporters | Export insurer approved receivable claim | Assignment/payment direction | Insurer approval | Trade finance brokers | 5-12% | Trade finance incumbents | Named payout |
| 33 | Approved Insolvency Distribution Claim | Creditors | Insolvency trustee accepted distribution | Assignment | Distribution notice | Insolvency lawyers | 10-25% | Legal, slow/uncertain | Named claim |
| 34 | Rebate Statement Cash-Out Lockbox | Distributors | Supplier issued year-end rebate statement | Assignment | Rebate statement | Accountants | 5-15% | Similar to retailer deductions | Named rebate |
| 35 | Approved Tax Penalty Refund Claim | SMEs | Authority reversed penalty/refund due | Assignment/mandate | Decision | Tax advisors | 10-20% | Public law/assignment risk | Named refund |

## Finalists And Strict Simulated Scores

| Rank | Candidate | Simulated score | Decision | Rationale |
|---|---|---:|---|---|
| 1 | Approved Commercial Insurance Payout Lockbox | 89 | Advance | Best match to the hard-control requirement: already-approved non-litigated payout, insurer/debtor acknowledgement, signed assignment/payment direction, and near-term collection. The first transaction can prove cash conversion. |
| 2 | Property Claim Progress-Payment Lockbox | 88 | Backup | Similar but contractor/staged-payment specificity may make direct-pay channels easier. Also risks looking like ordinary restoration finance. |
| 3 | Approved Cargo Insurance Payout Lockbox | 87 | Do not real-gate | Strong but freight/cargo claims can be document-heavy and disputed; `87` fails simulated threshold. |
| 4 | Approved Grant Reimbursement Bridge | 86 | Do not real-gate | Approved reimbursement is attractive, but public grant assignment/payment restrictions likely cap it. |
| 5 | Customs Refund Decision Lockbox | 85 | Do not real-gate | A decision is hard evidence, but public debtor assignment and legal/tax risk are high. |
| 6 | Public Late-Payment Interest Assignment | 84 | Do not real-gate | Already-paid principal is clean, but debtor collection and legal/reputational friction likely repeat retention-failure patterns. |

## Advance

Advance **Approved Commercial Insurance Payout Lockbox** to real working-chat validation.

## Source Notes

Search notes suggest insurance claim assignment is a live Polish practice, especially in motor/repair contexts, but assignment clauses and claimant protections can be complex. The prompt must restrict to commercial, non-consumer, non-litigated, approved payouts with insurer acknowledgement and legal/accounting review before any capital leaves the founder.
