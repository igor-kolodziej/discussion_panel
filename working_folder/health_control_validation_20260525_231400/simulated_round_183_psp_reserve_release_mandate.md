# Simulated Round 183: PSP Reserve Maturity Release Mandate

Date: 2026-05-29
Gate setting: simulated score strictly `>87`; working and fresh Zero To One gates `>=85`.

## Search Premise

Round 182 failed because underwriting evidence was still broker-trust coordination. This round tests hard current cash: payment-processor reserves, closed-account balances, and matured rolling holds where the PSP already shows a reserve schedule, reserve threshold, release date, balance, or account-review path.

Useful market facts checked:

- PayPal describes rolling reserves as a percentage of each transaction held and later released on a schedule, and says minimum reserves are reviewed at 180-day intervals.
- Shopify Payments reserves can hold a percentage for a defined number of days, then pay out the original positive reserve transactions with equal negative reserve transactions.
- Adyen documents merchant reserve balances, thresholds, top-ups, payable transfers, and payout behavior when thresholds are lowered.
- Stripe Connect has reserve-hold release schedules for connected accounts.

Reference URLs used for simulation context:

- `https://www.paypal.com/us/brc/article/account-reserves`
- `https://help.shopify.com/en/manual/payments/shopify-payments/payouts/reserves`
- `https://docs.adyen.com/account/balances/reserve/`
- `https://docs.stripe.com/connect/connected-account-reserves`

Internal scoring caps applied here only:

- cap below 82 without concrete 6-month control proof;
- cap below 85 if one vendor contract, equipment purchase, consultant, or hire can copy it;
- cap below 87 if CAC, payback, margins, cash conversion, or owner earnings are weak;
- cap below 87 if dependent on vague partnerships/goodwill/interviews;
- cap below 82 if clinical/legal/patient/regulated-data authority is unresolved.

## Raw Candidate Control Table

| # | Candidate | Buyer | Acute trigger | Transferable control point | 60-day proof | First acquisition | Economics/payback | Copy risk | Why incumbents cannot copy before control | Why not service/report/app/broker |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | PSP reserve maturity release mandate | ecommerce/SaaS merchants | reserve/hold matured but funds not released | signed mandate, reserve statement, case, payout trace | 5 mandates, 500k PLN reserves, 150k released | merchant groups, CFOs, ecommerce accountants | 10-20% success/fixed | payment consultants/lawyers | exact account/reserve case controlled | cash release mandate |
| 2 | PayPal 180-day hold release file | marketplace sellers | permanent limitation hold mature | account owner docs, hold email | releases | seller groups | high but messy | lawyers/forums | exact hold | platform opaque |
| 3 | Shopify Payments reserve release desk | Shopify merchants | reserve expiry/payout mismatch | reserve schedule/admin exports | releases | Shopify agencies | medium | agencies/Shopify support | exact store | release case |
| 4 | Adyen reserve threshold reduction pack | ticketing/hospitality/retail merchants | reserve above needed threshold | reserve balance/admin roles | payouts | payment consultants | medium | Adyen consultants | exact account | release file |
| 5 | Stripe connected-account reserve release | platforms/marketplaces | reserve holds release schedule | platform-controlled reserve plans | releases | platforms | high | Stripe/platform teams | exact connected accounts | release file |
| 6 | Closed merchant account balance release | merchants | account closed after risk window | PSP balance statement | releases | accountants | high | lawyers | exact balance | legal risk |
| 7 | Acquirer rolling-reserve early review | high-risk merchants | reserve review window opens | reserve addendum, chargeback data | partial releases | payment brokers | high | payment consultants | exact account | release case |
| 8 | PSP KYC hold evidence release | merchants | KYC/doc hold blocks payout | KYC request/evidence | payout | accountants | medium | PSP support | exact case | evidence, weaker |
| 9 | Marketplace payout reserve release | sellers | marketplace reserve/hold mature | reserve statement | payout | seller groups | medium | seller agencies | exact account | platform risk |
| 10 | Ticketing reserve release | venues/events | event passed, reserve remains | event settlement/reserve | payout | venues | high | ticketing platforms | exact event | release file |
| 11 | Hotel OTA virtual-card payout hold release | hotels | VCC/chargeback reserve mature | OTA statement | release | hotel accountants | medium | OTA recovery failed | exact account | prior weak |
| 12 | Subscription merchant dispute reserve release | SaaS | dispute window passed | dispute report/reserve schedule | release | SaaS CFOs | high | payment consultants | exact reserve | release |
| 13 | BNPL merchant reserve release | ecommerce | BNPL reserve/settlement held | BNPL statement | payout | ecommerce CFOs | medium | BNPL support | exact merchant | release |
| 14 | Chargeback-ratio improvement review pack | merchants | reserve can be lowered after clean period | chargeback reports | reserve cut | payment brokers | medium | consultants | exact account | advisory risk |
| 15 | Processor migration reserve release | merchants | migrated away, old reserve remains | closure statement | release | payment brokers | high | brokers | exact old account | release |
| 16 | Cross-border PSP blocked balance release | merchants | PSP requests final docs after closure | balance + docs | release | ecommerce groups | high | lawyers | exact account | risk/legal |
| 17 | Marketplace seller court-order hold release | sellers | creditor/legal hold lifted | release order | payout | lawyers | high | legal work | exact order | reject legal |
| 18 | VAT/tax lien payment-processor hold release | merchants | tax hold lifted | tax release | payout | tax advisers | high | tax/legal | exact lien | reject |
| 19 | Payment facilitator reserve release | SaaS platforms | platform reserve excess | reserve account threshold | payout | SaaS platforms | high | Stripe/Adyen teams | exact reserve | release |
| 20 | Merchant rolling-reserve discount purchase | merchants | reserve matured soon, wants cash now | assignment/payout direction | cashout | finance partners | high | factoring | exact reserve | financing/capital risk |
| 21 | Matured loan holdback release | merchants | fintech lender holdback mature | lender statement | release | merchants | medium | lenders | exact account | finance/legal |
| 22 | Affiliate network hold release | publishers | payout hold mature | network statement | payout | affiliates | low-medium | agencies | exact account | low ARPU |
| 23 | App marketplace payout hold release | developers | Apple/Google payout hold | developer account | payout | app studios | medium | app agencies | exact account | platform opaque |
| 24 | Creator platform hold release | creators/agencies | payout hold mature | account evidence | payout | agencies | low-medium | agencies | exact account | low ticket |
| 25 | Acquirer terminal deposit refund | merchants | terminal/security deposit mature | contract/deposit | refund | retailers | low | acquirers | exact deposit | commodity |
| 26 | Payment gateway unused balance refund | merchants | top-up balance/refund reserve unused | account statement | payout | merchants | low | PSPs | exact account | low ticket |
| 27 | Payment processor negative balance reversal | merchants | erroneous reserve setoff | PSP ticket | credit | accountants | medium | PSP support | exact account | dispute risk |
| 28 | Fraud false-positive payout release | merchants | payout held pending review | evidence case | payout | merchants | high | lawyers | exact case | high-risk dispute |
| 29 | Platform ad-credit refund release | advertisers | ad account credit/refund stuck | account balance | refund | agencies | medium | ad agencies | exact account | low moat |
| 30 | Telecom prepaid deposit refund | businesses | prepaid/deposit unused after closure | account statement | refund | multi-site | medium | utility auditors | exact account | generic |
| 31 | Utility supplier credit-balance refund | multi-site | account closure overpayment | supplier statement | refund | retailers | medium | utility auditors | exact accounts | generic |
| 32 | Software vendor credit memo cashout | IT buyers | approved credit unapplied | vendor ticket | credit/refund | MSPs | medium | SAM tools | exact ticket | generic |
| 33 | Shipping COD remittance reserve release | ecommerce | COD payout/reserve mature | courier statement | payout | sellers | medium | COD failed | exact statement | prior weak |
| 34 | Escrow.com transaction reserve release | sellers | online escrow payout held | escrow status | release | sellers | medium | escrow support | exact transaction | legal/platform |
| 35 | Marketplace shop closure final settlement | sellers | account closed, final balance due | closing statement | payout | sellers | medium | seller agencies | exact shop | platform opaque |
| 36 | Processor interchange/fee rebate recovery | merchants | contract rebate owed | merchant statement | credit | payment consultants | medium | consultants | exact contract | fee audit |
| 37 | PayFac submerchant reserve unwind | ISVs | submerchant reserve not released | reserve ledger | release | ISVs | high | internal teams | exact ledger | niche |
| 38 | Ticket refund reserve unwind | event operators | refunds done, reserve remains | ticketing ledger | payout | events | high | ticket platforms | exact event | release |
| 39 | High-risk merchant MOTO reserve release | merchants | card processor reserve mature | processor statement | payout | payment brokers | high | brokers/lawyers | exact account | risk-heavy |
| 40 | PSP account balance death/closure estate release | companies/estates | owner/company change blocks balance | authority docs | payout | accountants | medium | lawyers | exact account | legal |

## Finalists

| Candidate | Internal simulated score | Advance? | Rationale |
|---|---:|---|---|
| PSP reserve maturity release mandate | **88** | **Yes** | Highest current-cash fit: reserve schedules and balances are documented by PSPs, the founder does not hold funds, and proof is recovered payout or written no-go. |
| Ticketing reserve release | 85 | No | Good event-specific cash but ticketing platforms internalize and volumes are lumpy. |
| Adyen reserve threshold reduction pack | 84 | No | Clear mechanics but likely consultant/internal-finance owned. |
| Shopify Payments reserve release desk | 83 | No | Real pain but Shopify/Stripe support and agencies are obvious. |
| Stripe connected-account reserve release | 82 | No | Potentially high value but platforms own the data and process. |
| PayPal 180-day hold release file | 80 | No | Pain is severe but consumer/legal/fraud/dispute noise is too high. |

## Lead Candidate: PSP Reserve Maturity Release Mandate

### Buyer

Polish and CEE ecommerce brands, subscription merchants, digital-product sellers, ticketing/event sellers, SaaS merchants, marketplaces, and payment-facilitator platforms with documented reserves, rolling holds, closed-account balances, payout holds, or reserve-threshold balances at PayPal, Shopify Payments, Stripe/Stripe Connect, Adyen, PayU, Mollie, Checkout.com, or local acquirers.

### Acute Trigger

The merchant has a reserve schedule, reserve threshold, account hold, closed-account balance, or risk-review communication showing funds should be releasable, partially releasable, or reviewable now, but the PSP has not paid out, lowered the threshold, or given a clean no-go. The trapped cash delays inventory, payroll, supplier payments, ad spend, refunds, or platform migration.

### Control Point

The startup controls only account-evidenced reserve-release files:

- signed merchant mandate over named PSP account/reserve cases;
- reserve balance, reserve schedule, threshold, hold email, payout report, chargeback/dispute report, closure notice, risk-review date, and PSP support case;
- merchant KYC, fulfillment, tracking, refund, chargeback, and customer-service evidence approved by the merchant;
- submitted reserve-release or threshold-review packet;
- PSP ticket acknowledgements, payout trace, reserve threshold change, partial release, final release, or documented no-go.

It does not file chargeback representments, give legal advice, fight fraud allegations, hold funds, or promise release.

### 60-Day Proof

1. Five merchants sign paid reserve-release mandates covering at least 500,000 PLN equivalent of account-evidenced reserves or closed-account balances.
2. Each accepted case has a reserve schedule, balance statement, hold/closure email, risk-review date, or PSP dashboard export showing a concrete release/review path.
3. At least three PSP cases receive written acknowledgement, escalation, narrowed evidence request, partial release, final release, threshold reduction, payout trace, or documented no-go.
4. At least 150,000 PLN equivalent is released, paid out, offset to payable balance, or threshold-reduced.
5. At least 50,000 PLN in fixed and success fees is collected before total spend exceeds 100,000 PLN.

### 6-Month POC

Handle 30-60 screened reserve files; accept 15-25 clean cases; recover, release, or threshold-reduce 1,000,000-4,000,000 PLN equivalent; collect 200,000-600,000 PLN in fees; build a private PSP-specific reserve playbook by platform, country, merchant type, hold reason, evidence request, chargeback ratio, review timing, and payout behavior; keep gross margin above 65%; reject fraud, sanctions, legal holds, creditor claims, tax liens, unresolved chargeback spikes, consumer-heavy disputes, and cases without a concrete release/review path.

### Economics

Charge 5,000-15,000 PLN fixed triage/response fees for clean reserve files plus 10-20% of released cash or 5-10% of reserve-threshold reduction where release economics are measurable. The buyer pays because trapped PSP cash can be large, operationally urgent, and highly visible to the CFO/founder. Costs are merchant-data review, PSP-specific evidence assembly, and admin follow-up; no capital, custody, or receivable purchase is needed.

### Copy Risk

Payment consultants, chargeback firms, ecommerce agencies, lawyers, accountants, PSP relationship managers, and internal finance teams can copy parts. The defense is narrow account-case ownership, PSP-specific reserve-release memory, clean refusal of fraud/dispute work, and a live mandate over exact reserve balances and support cases before outsiders see the file.

### Why Incumbents Cannot Copy Before Control

Once the merchant signs the mandate and provides reserve dashboard exports, PSP emails, payout reports, support case access, chargeback/dispute data, and merchant-approved evidence, the startup controls the active reserve-release file. Competitors can offer similar reserve help later, but cannot collect or reassign that exact support case and payout trail without the merchant moving the mandate and account evidence.

### Why It Is Not A Service, Report, App, Dashboard, Database, Marketplace, Or Generic Broker

The startup accepts only named PSP reserve/hold/closed-balance cases with current account evidence and a concrete release or review path. It does not sell generic payments advice, chargeback defense, fraud consulting, legal demand letters, payment brokerage, financing, dashboards, or introductions. The output is recovered cash, reserve threshold reduction, payout trace, or documented no-go for that exact PSP account.

### Boundaries

The startup does not hold client funds, process payments, provide legal advice, represent merchants in litigation, handle tax/creditor/legal holds, file chargeback representments, alter transaction records, advise on sanctions, or argue disputed fraud findings. PSPs remain responsible for risk decisions, payout timing, account closure, reserve terms, and compliance. Reject cases involving legal notices, creditor attachments, tax liens, sanctions flags, active fraud accusations, identity mismatch, unresolved chargeback spikes, prohibited goods/services, consumer claims requiring legal handling, or requests to misstate fulfillment evidence.

### Duplicate Risk

This is not Approved Carrier Credit Lockbox, COD courier remittance recovery, 3PL recovery, OTA recovery, Amazon Vendor Central, PSP KYC evidence, insurance payout lockbox, PromoLeak, DORA, REDBlocked, Data Act, CBAM, GreenTender, Supplement Stack, HeatQuiet, BatteryFit, BioSignal, HeritageDoor, TraceFaktura, LeaseClear, RMA credit recovery, PropertyBind, or MiCARail. The buyer, control point, and payment event are specific to PSP reserve balances and payout holds, not carrier credits, retail deductions, regulatory evidence, insurance claims, or physical assets.

## Simulated Score

**88 / 100**

Reason for advancing: the candidate has current cash, documented reserve schedules, direct merchant mandate, fast proof by payout/threshold change/no-go, no custody, and strong operational urgency. The score is fragile because PSP discretion, fraud/chargeback/legal holds, and obvious payments consultants can cap the business if intake is not strict.

## Next Step

Write the clean Zero To One prompt and submit to working validation.
