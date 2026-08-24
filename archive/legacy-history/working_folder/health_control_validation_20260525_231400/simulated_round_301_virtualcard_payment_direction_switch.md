# Simulated Round 301: VirtualCard Payment-Direction Switch Lockbox

Date: 2026-05-31 Europe/Warsaw

Real gates: working Zero To One >=85 and fresh Zero To One >=85.
Simulation gate: advance only if simulated score is strictly above 87.

Internal scoring caps are applied here only. They are not included in the Zero To One prompt.

## Search Frame

Round 300 failed because a large official refund workflow was still owned by licensed customs incumbents. Round 301 avoids public refund portals, platform discretion, and regulated claim filing. It tests a direct current-payment object: approved B2B invoices where the supplier is being pushed into a fee-bearing virtual-card, card-network, or AP-payment-network route that creates a 1.5-3% margin haircut or delays cash if the supplier refuses the payment method.

The hard control object is not a savings report. It is customer-approved payment-direction change for named buyer accounts and named approved invoices, ending in AP acknowledgement, remittance scheduling, or first bank-transfer/ACH/SEPA payment without the card fee.

## Raw Candidate Control Table

| # | Candidate | Buyer/payor | Acute trigger | Transferable control point | 60-day signed/titled/assigned/prepaid proof | First acquisition | Economics/payback | Copy risk | Why incumbents cannot copy before control | Why not service/report/app/broker | Internal score |
|---:|---|---|---|---|---|---|---|---|---|---|---:|
| 1 | VirtualCard payment-direction switch lockbox | B2B suppliers paid by enterprises through VCC/AP networks | approved invoices suffer card-fee haircut or delayed payment unless supplier accepts VCC | signed supplier mandate, approved invoice list, buyer AP route, payment-method ticket, AP acknowledgement, first fee-free remittance | 8 mandates, 20 buyer accounts, 1m PLN invoice volume switched/scheduled, first fee-free payment | CFO/AR/accountant outreach | setup plus share of avoided fees; immediate payback | AR teams, accountants, AP consultants | exact buyer accounts and AP cases locked | payment direction and remittance outcome | 88.2 |
| 2 | General AP portal invoice release | suppliers using Coupa/Ariba/Tungsten | invoice rejected in buyer portal | portal ticket and invoice file | paid invoice | AR teams | fee | AP consultants | exact ticket | too generic | 72 |
| 3 | Early-payment discount leakage recovery | suppliers | dynamic discount taken incorrectly | invoice/remittance files | credit | CFOs | success fee | AR/accounting | exact remittance | ordinary AR | 70 |
| 4 | Bank-change vendor master no-go desk | suppliers | buyer blocks bank update | registry/bank evidence | payment release | accountants | fee | fraud controls | exact buyer ticket | fraud/legal risk | 73 |
| 5 | Payee-name mismatch AR release | exporters | buyer refuses payment on name/IBAN mismatch | AP issue text | payment | AR teams | fee | prior VoP branch failed | exact invoice | prior failed | 68 |
| 6 | Unapplied cash application mandate | vendors | paid cash not applied | remittance/invoice files | invoice cleared | AR teams | fee | prior failed | exact remittance | ordinary AR | 65 |
| 7 | Credit memo cashout | vendors with credits | customer credit memo not refunded | credit statement | refund | accountants | success fee | prior failed | exact credit | prior failed | 66 |
| 8 | Supplier portal tax-form cure | vendors | W-8/W-9/VAT form blocks payment | tax form/status | payment | accountants | fee | tax boundary | exact ticket | tax admin | 60 |
| 9 | Customer e-invoice onboarding release | suppliers | buyer requires e-invoice setup | portal/KSeF/EDI file | invoice accepted | EDI firms | fee | prior KSeF/EDI failures | exact buyer | setup service | 72 |
| 10 | Vendor master duplicate-entity cure | suppliers | buyer has wrong entity/vendor ID | registry and AP ticket | payment | AR teams | fee | AP can do | exact buyer | admin | 68 |
| 11 | ACH/check returned-payment cure | suppliers | buyer payment returned | remittance and bank file | reissued payment | accountants | fee | simple | exact remittance | low-complexity | 64 |
| 12 | Payment-terms correction desk | suppliers | buyer applies wrong terms | contract/invoices | payment acceleration | AR teams | success fee | copyable | exact contract | ordinary AR | 67 |
| 13 | PO mismatch release | suppliers | approved goods but PO/invoice mismatch | PO/GRN/invoice | paid invoice | AP teams | fee | generic | exact invoice | admin | 66 |
| 14 | Retainage release mandate | construction suppliers | retention due | debtor acknowledgement | payment | lawyers/factors | success fee | prior failed | exact receivable | legal | 62 |
| 15 | Customer short-pay recovery | suppliers | customer short-pays deductions | remittance and contract | credit | deduction firms | success fee | PromoLeak-adjacent | exact claim | prior failed | 69 |
| 16 | Payment-card merchant settlement cure | merchants | filed claim payment defect | portal defect | status advance | lawyers/accountants | fee | prior failed | exact claim | legal/scam-adjacent | 55 |
| 17 | OTA virtual-card recovery | hotels | VCC/commission mismatch | OTA statement claim | credit | revenue managers | success | prior failed | exact claim | platform recovery | 65 |
| 18 | Marketplace seller payout KYC release | sellers | payout held | account case | payout | agencies | fee | prior failed | exact account | platform discretion | 60 |
| 19 | PSP reserve maturity release | merchants | reserve should release | processor case | payout | payment consultants | success | prior failed | exact account | platform discretion | 62 |
| 20 | Freight invoice payment-method switch | carriers | shipper forces card fee | shipper AP route | first ACH | carrier AR | fee | carrier AR | exact shipper | subset | 76 |
| 21 | Medical payer EFT enrollment cure | providers | paper checks/fees delay cash | EFT enrollment | EFT payment | billing firms | fee | healthcare data | exact payer | health/admin | 58 |
| 22 | Ad-platform refund payment election | advertisers | refund approved but payment failed | support case | refund | agencies | fee | platform opacity | exact case | platform | 57 |
| 23 | Public buyer e-invoice payment path | suppliers | public invoice accepted but payment route wrong | public AP ticket | payment | admin teams | fee | public admin | exact invoice | low margin | 60 |
| 24 | Supplier financing opt-out desk | suppliers | AP platform pushes paid early-payment financing | customer AP setting | fee-free payment | AR teams | fee share | AP can do | exact buyer | similar to lead | 82 |
| 25 | Procurement-card acceptance reversal | suppliers | customer forces purchasing card | contract/AP ticket | bank transfer | AR teams | fee | buyer policy | exact account | similar to lead | 83 |
| 26 | Card surcharge implementation desk | suppliers | recover card fees via surcharge | terms/legal setup | first surcharge | payment lawyers | fee | legal | exact policy | legal/tax | 50 |
| 27 | Cross-border wire fee recovery | exporters | OUR/SHA fee mismatch | remittance/invoice | corrected fee | accountants | fee | small | exact payment | low value | 58 |
| 28 | AP network invoice-fee opt-out | suppliers | network charges invoice/payment fee | portal opt-out/ticket | fee-free invoice | AR teams | fee | AP can do | exact account | subset | 79 |
| 29 | Enterprise customer direct-debit mandate switch | suppliers | card/portal cost high | signed debit mandate | first debit | finance teams | fee | customer policy | exact account | payment setup | 74 |
| 30 | Factor-approved payment-direction transfer | suppliers using factors | buyer pays wrong account | factor notice/AP acknowledgement | correct payment | factors | fee | factor teams | exact debtor | factoring-owned | 60 |

## Finalists

| Finalist | Internal simulated score | Advance? | Rationale |
|---|---:|---|---|
| VirtualCard Payment-Direction Switch Lockbox | **88.2** | **Yes** | Best current-cash control: named approved invoices, written buyer AP payment-method route, supplier mandate, and first fee-free payment or schedule. It avoids public portals, legal claims, tax advice, and platform discretion. |
| Procurement-card acceptance reversal | 83 | No | Similar mechanics, but narrower and more likely buried in customer procurement policy. |
| Supplier financing opt-out desk | 82 | No | Good but often looks like ordinary AP-network settings cleanup. |
| AP network invoice-fee opt-out | 79 | No | Fee savings are smaller and more admin-like. |
| Freight invoice payment-method switch | 76 | No | Plausible but carrier AR teams and freight payment platforms own many cases. |

## Lead Candidate

**VirtualCard Payment-Direction Switch Lockbox**

### Internal Simulated Score

88.2 / 100

### Why It Advances

- It starts from current approved invoices or recurring customer accounts, not speculative future savings.
- The proof artifact is customer-side AP acknowledgement, payment-method update, scheduled bank transfer, ACH/SEPA remittance, or first no-card-fee payment.
- AP automation and card-network intermediaries are often economically misaligned because virtual cards and early-pay networks generate rebates or fees; the supplier needs its own payment-direction operator.
- The founder does not touch funds, advise on law, negotiate procurement terms broadly, or collect claims. The work is tightly bounded to named buyer-account payment route changes.
- Gross margin can work if minimum invoice volume is enforced: one 500,000 PLN monthly buyer account with a 2% card haircut can justify a 10,000-25,000 PLN fee from avoided annual leakage.

### Control Point

- Signed supplier mandate.
- Buyer/customer account list and approved invoice register.
- Evidence of virtual-card, card-network, AP-network, or fee-bearing payment route.
- Contract/payment-terms excerpt only to confirm the supplier may request fee-free bank transfer; legal interpretation is escalated or rejected.
- Buyer AP/procurement ticket, portal case, email acknowledgement, vendor-master payment-method update, remittance schedule, or first fee-free payment.
- Fee right tied to confirmed switch, payment schedule, or first remittance, not to a report.

### 60-Day Proof

1. Eight supplier mandates covering at least twenty named enterprise buyer accounts.
2. At least 1,000,000 PLN of monthly or scheduled approved invoice volume under switch review.
3. Ten customer AP acknowledgements or portal payment-method cases opened with supplier authorization.
4. Five customer accounts switched, scheduled, or confirmed for bank-transfer/ACH/SEPA payment.
5. At least one first fee-free remittance received.
6. 25,000-60,000 PLN collected through setup fees and release/savings-linked fees.
7. Reject cases involving disputed invoices, buyer insolvency, fraud flags, contract renegotiation, new bank-account risk, legal threats, or no written buyer AP path.

### 6-Month POC

- Control 40 suppliers and 120 buyer-account payment routes.
- Move 20,000,000-50,000,000 PLN annualized approved invoice volume away from avoidable card/AP-network fees.
- Document 400,000-1,000,000 PLN annualized supplier margin preserved.
- Collect 150,000-400,000 PLN in fees.
- Build a private buyer/AP-network/payment-method switch taxonomy: buyer policy, portal path, accepted evidence, remittance timing, rejection reason, and fee-free route.
- Keep customer-relationship complaints below 5% and hard no-go/rejection above 30% to avoid low-quality chasing.

### Economics

Charge 1,500-5,000 PLN per buyer-account switch setup after a written path is confirmed, plus 15-25% of first-year avoided card/AP-network fees capped by buyer account. For large recurring accounts, charge a fixed 10,000-25,000 PLN switch fee if the supplier dislikes success fees. Founder work is structured AR/AP case control; specialist contractor time is limited to portal operations, customer-account research, and secure document handling.

### Copy Risk

Supplier AR teams, accountants, AP consultants, and CFO-services firms can copy the workflow. AP networks and enterprise buyers may also harden policies. The defense is narrow: signed supplier mandates, exact buyer AP case memory, payment-method switch wording, approved invoice lists, remittance evidence, and repeat buyer-account routes before rivals know which accounts are movable.

### Why It Is Not A Service, Report, App, Dashboard, Database, Marketplace, Or Generic Broker

The startup is not selling spend analytics, AR consulting, a dashboard, a supplier directory, or generic payment advice. It controls a named payment-direction switch file for approved invoices and gets paid only when customer AP acknowledges the route, schedules fee-free payment, or the first no-card-fee remittance arrives.

### Duplicate Risk

- Not PromoLeak: no retailer deductions, promotions, retail media charges, shortage claims, or remittance leakage.
- Not VoP payee-name mismatch: the invoice is not blocked by beneficiary-name verification; the cash issue is a fee-bearing payment method.
- Not KSeF, AP portal, unapplied cash, credit memo, or approved true-up recovery: the controlled object is customer-approved payment direction away from virtual-card/AP-network haircut.
- Not Amazon Vendor Central, 3PL, OTA, freight, PSP reserve, card-settlement claim, or marketplace payout recovery.
- Not DORA, REDBlocked, BioSignal, HeritageDoor, TraceFaktura, CBAM, Data Act, GreenTender, BatteryFit, HeatQuiet, or health/Rx/clinical routes.

## Internal Cap Notes

- Not capped below 82: the 60-day proof is concrete current-cash control, not a memo.
- Not capped below 85: many incumbents can copy generic AP follow-up, but the exact buyer accounts, supplier mandates, and AP case routes are locked once controlled.
- Not capped below 87: economics are credible only with strict minimum invoice volume and recurring buyer-account payment routes.
- Capped at 88.2, not higher, because customer AP teams may refuse switches, suppliers can learn the playbook, and the moat is operational rather than structural.

## Gate Decision

Advance Round 301 to working Zero To One validation because the simulated score is strictly greater than 87.
