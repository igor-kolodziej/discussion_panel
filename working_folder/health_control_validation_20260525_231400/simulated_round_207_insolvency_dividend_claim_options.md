# Simulated Round 207: Insolvency Dividend Claim Option Desk

Date: 2026-05-30 Europe/Warsaw
Real gates: working Zero To One >=85 and fresh Zero To One >=85.
Simulation gate: advance only if simulated score is strictly above 87.

## Search Frame

Round 206 failed because a mandate over a messy operational ledger did not create enough control. This round tests literal title or option control over admitted, non-disputed distribution claims where the first proof is a signed cession/option, proceeding-side acknowledgement, and cash conversion path.

Primary public-law context checked before simulation:

- Polish bankruptcy proceedings use lists of claims and distribution plans for satisfying creditors from the bankruptcy estate.
- The Ministry of Justice publishes standard bankruptcy-procedure forms, including distribution-plan forms.
- Distribution and admitted-claim mechanics are formal enough to make "included in an official list/plan" a materially harder artifact than ordinary invoice-chasing.

Sources consulted for context:

- Polish Ministry of Justice bankruptcy procedure forms: `https://www.gov.pl/web/sprawiedliwosc/wzory-stosowane-w-postepowaniu-upadlosciowym.`
- OpenLEX / consolidated Polish Bankruptcy Law sections on lists of claims and distribution plans.

## Raw Candidate Control Table

| # | Candidate | Buyer/payor/source | Acute trigger | Transferable control point | 60-day proof | First acquisition | Economics/payback | Copy risk | Why incumbent cannot copy exact controlled item | Why not service/report/app/broker |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | Insolvency dividend claim option desk | SME creditors with admitted claims | creditor wants cash before distribution/admin burden | signed claim option or cession, claim list/plan proof, trustee/court notice | 6 options/cessions, 2 acknowledgements, first cash sale/distribution | insolvency notices, accountants, lawyers | discount spread on expected dividend | lawyers, distressed-debt buyers | exact assigned claim/option locked | claim title/control |
| 2 | Court deposit refund assignment | SMEs/law firms | final order returns deposit | refund order/payment direction | assignments | lawyers | low spread | lawyers | exact order assigned | named refund |
| 3 | Public procurement bid-bond refund buyout | contractors | bid bond/security due back | release letter/cession | cessions | contractors | small | banks/contractors | exact security return | named refund |
| 4 | Approved restructuring-plan instalment assignment | creditors | debtor has approved plan instalments | assigned instalment claim | cessions | creditors | spread | lawyers/funds | exact plan claim | claim title |
| 5 | Liquidator surplus distribution claim buyout | shareholders/creditors | liquidation surplus approved | distribution right | assignment | accountants | spread | lawyers | exact right | title |
| 6 | Court-awarded cost reimbursement assignment | SMEs | final award costs unpaid | final order/cession | assignments | law firms | spread | enforcement lawyers | exact awarded claim | legal/enforcement risk |
| 7 | Notary escrow release assignment | SMEs | escrow release conditions met | escrow instruction/right | assignment | notaries | low | parties/notaries | exact escrow | named payment |
| 8 | Approved insurance payout claim purchase | SMEs | payout approved but delayed | assignment/payment direction | ack | brokers | failed family | factors | exact payout | already failed |
| 9 | Approved grant reimbursement assignment | grant recipients | reimbursement approved | approval/right | assignment | grant consultants | spread | banks/grant firms | exact claim | public-payment limits |
| 10 | Customs refund decision assignment | importers | refund decision issued | refund right | assignment | brokers | spread | customs/tax advisors | exact refund | legal/tax risk |
| 11 | Energy supplier accepted credit-note purchase | SMEs | credit memo issued | credit note/cession | cessions | energy brokers | spread | accountants | exact credit | generic credit |
| 12 | Leasing overpayment refund purchase | SMEs | lease end settlement overpaid | settlement statement | cessions | accountants | low | leasing firms | exact overpayment | small |
| 13 | Factoring reserve release claim buyout | ex-clients | factor reserve due | reserve statement | assignment | SMEs | spread | factors/lawyers | exact reserve | legal friction |
| 14 | Insolvency wage/employee claim buyout | workers | admitted wage claim | claim assignment | reject | labor issue | risky | legal/consumer | exact claim | avoid consumer/labor |
| 15 | Mass tort/class settlement business claim | companies | settlement fund claim approved | claim sale | assignment | claims administrators | spread | claims firms | exact claim | foreign/legal |
| 16 | Antitrust settlement distribution claim | SMEs | approved settlement participation | claim sale | assignment | industry groups | spread | law firms | exact claim | litigation-adjacent |
| 17 | Unclaimed property company claim purchase | companies | state holds unclaimed property | claim assignment | assignment | databases | spread | recovery firms | exact claim | US/legal |
| 18 | Court enforcement overpayment refund | businesses | bailiff acknowledges overpayment | refund statement | assignment | accountants | spread | lawyers | exact refund | sensitive/legal |
| 19 | Tax penalty refund right purchase | SMEs | authority decision reverses penalty | refund decision | assignment | tax advisors | spread | tax firms | exact refund | tax law |
| 20 | Approved cargo insurance payout purchase | importers | payout approved | assignment | ack | adjusters | spread | insurers/factors | exact payout | claims handling |
| 21 | Insolvency secured collateral distribution tail | secured creditors | collateral sale plan final | distribution right | assignment | banks/suppliers | spread | funds | exact secured tail | legal/priority risk |
| 22 | Vendor rebate statement purchase | distributors | supplier statement final | assignment | cession | accountants | failed-ish | rebate firms | exact rebate | supplier discretion |
| 23 | Court registry expert-fee refund | experts/SMEs | deposit balance due | refund order | assignment | experts | low | lawyers | exact refund | small |
| 24 | Public late-payment interest claim option | contractors | principal paid late | assigned interest | assignment | contractors | spread | lawyers | exact interest | enforcement friction |
| 25 | Approved EU project cost reimbursement | SMEs/universities | payment claim accepted | approved claim | assignment | grant advisors | spread | banks | exact claim | public limits |
| 26 | Insolvency claim data-room purchase for micro funds | claim buyers | need screened small admitted claims | optioned claim package | buyer deposit | distressed investors | origination fee/spread | funds/lawyers | exact optioned claims | asset package |
| 27 | Consumer bankruptcy creditor claim purchase | creditors | admitted consumer claim | claim assignment | reject | creditors | low | legal | exact claim | consumer/legal |
| 28 | Reorganization supplier instalment book | suppliers | plan instalments accepted | instalment cession | assignments | suppliers | spread | factors | exact instalments | title |
| 29 | Litigation finance award receivable sale | businesses | final award payable | assignment | assignment | lawyers | spread | litigation funders | exact award | legal/enforcement |
| 30 | Insolvency VAT bad-debt relief support | creditors | unpaid debtor bankrupt | docs | reject | accountants | service | tax advisors | no title | tax service |
| 31 | Approved municipal compensation claim purchase | suppliers | gmina compensation approved | acknowledgement/assignment | assignment | suppliers | spread | lawyers | exact payment | public-debtor risk |
| 32 | Supplier insolvency prepayment refund claim buyout | buyers | claim admitted for prepaid goods | claim assignment | cession | ecommerce/SMEs | spread | lawyers | exact claim | title |
| 33 | Estate creditor distribution claim option | business creditors | deceased debtor estate distribution | claim option | assignment | lawyers | low | lawyers | exact claim | probate/legal |
| 34 | Bank guarantee claim surplus refund | contractors | beneficiary release approved | release/assignment | assignment | contractors | spread | banks | exact release | retention family |
| 35 | Insolvency escrowed asset-sale proceeds right | creditors | asset sale proceeds allocated | plan/order | option | lawyers | high | funds | exact right | legal priority |
| 36 | Receivership rent distribution claim | landlords/suppliers | receiver distribution scheduled | claim assignment | cession | landlords | spread | lawyers | exact claim | legal |
| 37 | Approved warranty-retention final tranche | contractors | final tranche acknowledged | cession | assignment | contractors | failed family | lawyers | exact tranche | retention failed |
| 38 | Bankruptcy estate supplier administrative expense claim | post-bankruptcy suppliers | estate owes current expense | assignment | reject | suppliers | spread | lawyers | exact claim | priority/legal |
| 39 | Restructuring arrangement creditor claim option | SMEs | arrangement approved | claim option | cession | creditors | spread | funds | exact claim | slow/default risk |
| 40 | Official distribution-plan remittance cleanup | creditors | plan lists creditor but bank data stale | mandate | trustee ack | creditors | fee | trustees/accountants | exact remittance | service unless assignment |

## Finalists

| Candidate | Internal simulated score | Advance? | Rationale |
|---|---:|---|---|
| Insolvency Dividend Claim Option Desk | **88.4** | **Yes** | Strongest claim-title structure: admitted non-disputed claim, official list/plan evidence, option/cession, trustee/court acknowledgement, and cash conversion through discount purchase or downstream buyer deposit. |
| Approved restructuring-plan instalment assignment | 85 | No | Similar but debtor performance risk and plan default risk are higher. |
| Insolvency claim package for micro funds | 84 | No | Useful channel, but becomes origination/brokerage unless the founder controls claim options first. |
| Court deposit refund assignment | 82 | No | Clean but low-volume, lawyer-owned, and too small. |
| Customs refund decision assignment | 80 | No | Public-law assignment/tax boundaries cap it. |
| Public late-payment interest claim option | 78 | No | Enforcement/legal friction resembles failed retention and public-payment ideas. |

## Selected Candidate

**Insolvency Dividend Claim Option Desk**

### Why This Advanced

The candidate directly addresses the repeated failure mode of "mandate over messy recovery." The startup either controls a signed option/cession over an admitted claim or does not accept the case. The proof artifact is not a memo, dashboard, or better document packet; it is a legal transfer path around a specific admitted claim already included in an official creditor list, arrangement, or distribution plan.

### Buyer / Seller

The supply side is SME creditors, landlords, distributors, service providers, and B2B vendors holding admitted, non-disputed insolvency or restructuring claims that are administratively annoying, delayed, or below the attention threshold of funds and lawyers.

The economic buyer can be the startup itself for small claims, a downstream distressed-claim buyer for larger packages, or a creditor that pays only when the startup converts stale distribution administration into cash. The first version should avoid consumers, employees, disputed claims, secured-priority disputes, and litigation.

### Control Point

- Signed option or cession over a named admitted claim.
- Claim-list, arrangement, or distribution-plan proof.
- Creditor identity, invoice/proof of debt, proceeding reference, trustee/supervisor/debtor contact, expected category, expected dividend or instalment schedule, and payment-account update.
- Lawyer-reviewed transfer documents and no-go rules.
- Trustee/supervisor/court/debtor acknowledgement where required.
- Downstream buyer escrow/deposit or founder discount-purchase only after acknowledgement path is clear.

### 60-Day Proof

- Screen at least 60 public/professional leads and 25 creditor files.
- Sign 6 options or cessions over admitted, non-disputed claims with at least 500,000 PLN face value and at least 120,000 PLN expected distribution or plan instalment value.
- Obtain 2 proceeding-side acknowledgements or written no-objection/payment-direction confirmations.
- Close at least 1 cash conversion: founder purchase, downstream buyer assignment, or actual first distribution/instalment.
- Collect at least 25,000 PLN gross spread, origination fee, option fee, or realized distribution margin.
- Reject every file with unresolved objections, setoff, security-priority dispute, employee/consumer status, missing admission proof, ongoing litigation, unclear authority, sanctions/AML concerns, or no credible payment horizon.

### Economics

Use small fixed diligence fees only for downstream buyers, not for creditors. The core economics are claim-control spread:

- buy or option small admitted claims at 45-75% of expected distribution value when payment horizon is visible;
- resell packaged claims to a distressed-claim buyer at a lower discount;
- or hold selected small claims to first distribution where the payout horizon and acknowledgment are credible.

The 100,000 PLN budget is enough for legal templates, targeted sourcing, small pilot purchases, and selective downstream-buyer deposits. The startup does not need to buy every claim; it needs to control enough clean options to prove conversion.

### Internal Caps Applied

- Capped below 92 because legal transferability, priority, timing, and acknowledgement are real friction.
- Capped below 90 because distressed-debt funds, lawyers, and factors can copy the structure if they see enough supply.
- Not capped below 87 because signed claim options/cessions are a harder control object than recovery mandates, evidence packets, or portal submissions, and because the first proof can be actual cash conversion.

## Simulated Zero To One Score

**88.4 / 100**

Passes the simulated gate because it is strictly above 87.

## Zero To One Prompt File

`/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/zero_to_one_prompt_insolvency_dividend_claim_options.txt`

## Kill Criteria

Kill this branch if Zero To One says any of the following are decisive:

- clean admitted claims do not need a founder and can simply wait for distribution;
- assignment/option acknowledgement is too lawyer-owned or slow for a 60-day proof;
- good claims are already known to distressed-debt buyers and bad claims are adverse-selection traps;
- cash conversion is not credible inside six months under the 100,000 PLN budget;
- the business is merely legal/debt-collection brokerage rather than controlled claim ownership.
