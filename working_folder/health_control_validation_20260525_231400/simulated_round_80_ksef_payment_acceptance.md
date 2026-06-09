# Simulated Round 80: KSeF / AP Payment-Acceptance Control Points

Date: 2026-05-27

## Round Rule

This round avoids generic KSeF support. The control point must be a named payment, invoice batch, AP rejection, buyer acknowledgement, office queue, or delegated acceptance workflow. Optional readiness, dashboards, broad accounting cleanup, and open-ended XML support are capped.

## Raw Candidate Table

| # | Candidate | Buyer | Acute trigger | Transferable/control point | Signed/titled/assigned/prepaid inside 60 days | First acquisition mechanism | Margin / payback logic | Copy risk and why incumbents cannot copy first | Why not wrapper |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | KSeF AP Payment-Acceptance Release Desk | B2B suppliers/wholesalers/manufacturers selling to large buyers | Buyer AP will not pay named invoices because KSeF/AP/PO acceptance failed | Signed mandate over named unpaid invoice batch, buyer rejection/status email, accountant-approved correction/reissue path | Paid mandate, buyer AP status, accountant approval, first payment movement | Direct outbound to suppliers with large-buyer payment blocks and accountants | 4k-15k fixed fee or 1-3% on released invoices; ROI tied to cash release | Accountants/ERP vendors can copy generic fixes, but not the named mandate and buyer AP case once signed | Controls a payment-release case, not KSeF education |
| 2 | KSeF ERP Integrator Exception Queue Retainer | Small ERP integrators | Clients flood integrator with repeated KSeF rejections after rollout | Retainer over exception queue plus recurring source-system error corpus | 3 prepaid integrator retainers and source-system samples | Integrator partnerships | 6k-15k/month per integrator | ERP vendors can patch common errors | Queue/control retainer, not app |
| 3 | KSeF Large-Buyer Supplier Onboarding Pack | SMEs onboarding to large buyers | Buyer procurement requires KSeF endpoint, AP fields, GLN/PO mapping, notices | Buyer-specific onboarding packet and supplier mandate | Paid onboarding case and buyer AP acknowledgement | Supplier outreach from buyer portals | 3k-8k/case | Buyers publish guides; low moat | Live onboarding case |
| 4 | KSeF Correction Invoice Release Pack | Suppliers with rejected corrections/credit notes | Large buyer refuses credit/debit/correction flow | Named correction batch and accountant approval | Paid mandate and buyer status | Accounting office referrals | 3k-10k/case | Accountants can solve | Named blocked corrections |
| 5 | KSeF UPO Recovery For Marketplace Sellers | Marketplace merchants | Marketplace/warehouse refuses settlement without accepted invoice/UPO | Batch UPO/status and marketplace case | Paid case and status evidence | Marketplace accountants | 2k-6k/case | Platforms can document flows | Named settlement block |
| 6 | KSeF Split-Payment Acceptance Desk | Suppliers in MPP-sensitive categories | Buyer/AP rejects split-payment/VAT-field mismatch | Named invoice pack and accountant fix | Paid mandate, accountant signoff | Tax/accountant referrals | 3k-8k/case | Tax/accounting-sensitive | Payment release case |
| 7 | AP Portal Invoice Match Desk | Vendors using SAP/Ariba/Coupa portals | Portal invoice accepted in KSeF but rejected by buyer AP/PO match | Buyer portal case plus KSeF invoice ID | Paid mandate and buyer status | Supplier finance teams | 5k-15k/case | AP consultants can copy; buyer-specific memory helps | Named cash blocker |
| 8 | EDI ASN/Invoice Chargeback Release | FMCG suppliers | Retailer chargebacks / payment holds due EDI mismatch | Retailer dispute case and payment hold | Paid dispute mandate | Similar to PromoLeak, duplicate risk | 5-15% recovery | PromoLeak duplicate | Recovery case |
| 9 | KSeF Receivables Factoring Readiness Pack | Factors/borrowers | Factor refuses financing due KSeF status mismatch | Named receivable evidence pack | Factor status and borrower mandate | Factor referrals | 3k-10k/case | Factors may internalize | Finance case |
| 10 | KSeF Public Buyer Payment Pack | SME contractors selling to public entities | Public buyer payment held for KSeF/formal invoice defects | Named invoice/payment status | Paid mandate and buyer confirmation | Public contractors | 3k-10k/case | Procurement/legal delays | Payment release |
| 11 | Foreign Vendor Polish KSeF Receipt Desk | Foreign suppliers selling to Polish buyers | Polish buyer refuses non-KSeF/foreign invoice workflow | Buyer guidance and invoice pack | Paid mandate and buyer AP acknowledgement | Foreign chambers/accountants | 3k-8k/case | Narrow edge cases | Named buyer blocker |
| 12 | KSeF Cash-Application Exception Book | Accounting offices | KSeF received invoices do not match bank/ERP AP | Office exception queue | Retainer | Accounting offices | Low/medium | Month-end rail repeat; prior 81 risk | Queue retainer |
| 13 | KSeF Buyer Notification Rail | Suppliers | Buyers no longer get PDF/email invoices and payments slow | Buyer notification/update workflow | Paid supplier batch | Direct | Low | App-like | Notification flow |
| 14 | KSeF Local-Government Supplier Pack | Vendors to gminas/schools | Public buyer asks for specific KSeF handling | Named public buyer requirement | Paid mandate | BIP supplier lists | 2k-6k/case | Low ticket | Case pack |
| 15 | KSeF SAP Business One Error Cell | SMEs on SAP B1 | Integration rejects FA(3) invoices | Source-system batch | Prepaid retainer | SAP consultants | 5k-15k/month | Consultants copy | Error cell |
| 16 | KSeF enova/Optima/Subiekt Batch Repair Desk | SMEs/accountants | Popular ERP export creates repeat errors | Error family queue | Paid office/integrator retainer | ERP forums/partners | 3k-10k/month | Vendors patch | Queue support |
| 17 | KSeF Buyer Master-Data Cleanup Mandate | Suppliers | Wrong NIP/name/address/PO data blocks AP | Buyer master-data case | Paid mandate and buyer contact | Supplier finance | 3k-8k/case | Admin-heavy | Named AP case |
| 18 | KSeF UPO Archive Evidence Pack | Audits/disputes | Customer claims invoice not received/accepted | UPO/KSeF archive evidence | Paid case | Accountants | Low | Low urgency | Evidence pack |
| 19 | KSeF Micro-Entity Receiving Onboarding | small NGOs/clubs | Need receive invoices via KSeF | account setup | Paid setup | Too low ticket | Low | App/setup |
| 20 | KSeF Developer Error Corpus Subscription | ERP vendors | Need rejection examples | Dataset rights | paid data licenses | Developer outreach | Data-rights weak | Dataset |
| 21 | KSeF Large-Employer Expense Invoice Desk | Employees/JDG vendors | Expense invoices stuck | HR/AP case | Mandate | Low | Low | Admin |
| 22 | KSeF Construction Progress Invoice Release | Construction subcontractors | Monthly progress invoice held by buyer AP/KSeF mismatch | Named high-value invoice and buyer status | Paid mandate, protocol, accountant fix | Contractor finance referrals | 5k-20k/case | Similar retention but stronger invoice trigger | Payment release |
| 23 | KSeF B2B Marketplace Seller Settlement Desk | sellers on Polish B2B marketplaces | settlement held due invoice acceptance | platform case | Paid mandate | Marketplaces | Medium | Platform can copy | Settlement case |
| 24 | KSeF EDI-to-FA(3) Retail Supplier Pack | retail suppliers | EDI invoice converted wrongly into FA(3) | buyer EDI/KSeF case | Paid mandate | EDI integrators | Medium | EDI firms copy | Named blocker |
| 25 | KSeF Reverse-Charge/Export Exception Desk | exporters/foreign services | invoice fields rejected by buyer/accountant | accountant-approved case | Paid mandate | accountants | medium | tax-sensitive | Case |
| 26 | KSeF AP Helpdesk Buyout | retiring KSeF consultant | live client ticket queue | customer-approved payment transfer | option + prepaid clients | buy microconsultant book | medium | service labor | ticket book |
| 27 | KSeF Invoice Reissue Legal Boundary Desk | companies afraid of duplicate/reissue | need correction/reissue decision | lawyer/accountant review | paid case | lawyers/accountants | low/medium | professional veto | review case |
| 28 | KSeF Bank Loan Receivable Evidence Pack | banks/borrowers | bank wants KSeF proof for receivable financing | bank evidence case | paid mandate | factoring brokers | medium | banks internalize | finance case |
| 29 | KSeF API Incident Evidence Pack | software vendors | customer claims vendor outage caused rejected invoices | incident/evidence case | paid vendor case | SaaS vendors | low | support-like | evidence case |
| 30 | KSeF Cross-Border Branch Invoice Pack | Polish branches / foreign HQ | HQ ERP cannot handle local KSeF fields | HQ rollout blocker | paid mandate | expat accountants | medium | consultants copy | implementation pack |

## Finalists And Strict Simulated Scores

| Rank | Candidate | Simulated score | Decision | Main reasoning |
|---:|---|---:|---|---|
| 1 | KSeF AP Payment-Acceptance Release Desk | 89 | Advance | Stronger than the prior month-end rail because the control point is a named unpaid invoice batch with buyer AP rejection/status and accountant-approved correction/reissue. The buyer pays against cash release, not generic compliance. |
| 2 | AP Portal Invoice Match Desk | 87 | Hold | Strong pain, but it becomes enterprise AP consulting unless the KSeF-specific blocker is explicit. Does not clear strict `>87`. |
| 3 | KSeF ERP Integrator Exception Queue Retainer | 86 | Hold | Better channel than accounting offices but still faces source-system vendor patches and SLA load. |
| 4 | KSeF Construction Progress Invoice Release | 86 | Hold | High-value cash trigger, but construction disputes can contaminate the clean KSeF/AP blocker. |
| 5 | KSeF Large-Buyer Supplier Onboarding Pack | 84 | Hold | Useful but more readiness/onboarding than hard payment control. |

## Round Decision

Submit `KSeF AP Payment-Acceptance Release Desk` to working Zero To One using a clean prompt without meta-scoring cap instructions.
