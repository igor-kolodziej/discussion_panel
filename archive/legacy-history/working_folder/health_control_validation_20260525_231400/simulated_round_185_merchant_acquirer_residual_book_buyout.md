# Simulated Round 185: Merchant Acquirer Residual Book Buyout

Date: 2026-05-29  
Real browser gates: working Zero To One `>=85`, fresh Zero To One `>=85`

## Search Frame

Round 184 failed because "reserved capacity" was not real enough without proven lab-side commitment. This round searches for a harder object: an already-paid recurring commission/payment stream that can be assigned, transferred, or redirected with the payor's written acknowledgement before the founder pays for it.

## Raw Candidate Control Table

| # | Candidate | Buyer/source | Acute trigger | 60-day signed/assigned/prepaid proof | First cash movement | Copy/fatal risk | Internal score |
|---:|---|---|---|---|---|---|---:|
| 1 | Merchant acquirer residual book buyout | retiring POS/acquiring agents | agent exits small merchant portfolio | acquirer/master-agent approved residual assignment, seller option, first residual payment | current-month residual paid to startup/escrow | acquirer may block assignment | 88.2 |
| 2 | Business telecom residual book buyout | retiring telecom agents | agent retires before fiber/VoIP renewals | carrier/master-agent commission assignment, first commission | monthly commission redirect | carrier terms/support churn | 84 |
| 3 | Energy broker commission book buyout | B2B energy brokers | broker exits renewal portfolio | supplier commission assignment, customer list, first residual | supplier-paid commission | regulation/commodity/churn | 80 |
| 4 | Waste-hauling broker residual book | waste-service brokers | broker retires | hauler-approved commission transfer | monthly commission | low margin/service disputes | 73 |
| 5 | Cyber-insurance referral residual book | small brokers | book too small for broker | licensed-broker partner assignment | commission split payment | insurance licensing | 70 |
| 6 | SaaS reseller commission stream buyout | software consultants | partner exits customers | vendor-approved partner-of-record transfer | recurring commission | vendor terms/support | 76 |
| 7 | Microsoft CSP residual transfer | CSP sellers | partner retires | distributor-approved tenant transfer | margin/residual payment | already near failed PartnerCenter branch | 68 |
| 8 | Shopify/agency app referral residuals | ecommerce agencies | agency exits partner referrals | platform approved payout transfer | referral payout | low/opaque/copyable | 62 |
| 9 | Domain/hosting renewal book | retiring webmasters | renewal admin handoff | customer approvals, first renewal cash | customer-paid renewal | already failed | 72 |
| 10 | SMS notification traffic residuals | CPaaS resellers | reseller exits | customer billing transfer, first margin | SMS margin | already failed OTP | 61 |
| 11 | Lift emergency SIM book | lift/intercom installers | admin book succession | customer approvals, SIM transfer, first cash | monthly SIM revenue | already failed | 62 |
| 12 | B2B printer consumables route | warehouse supply agents | retiring rep | customer billing approvals, supplier terms | first reorder cash | commodity | 69 |
| 13 | Cleaning consumables route | facility suppliers | route owner retires | customer approvals, first invoices | reorder cash | commodity/low margin | 62 |
| 14 | IP renewal docket book | IP paralegals | docket owner retires | customer approvals, docket transfer | renewal fees | legal trust | 70 |
| 15 | LEI renewal book | LEI agents | renewal book neglected | LOU/agent transfer, first renewals | renewal fees | commodity/low ARPU | 58 |
| 16 | Qualified certificate renewal book | e-signature resellers | certificate expiry book | QTSP transfer, customer consent | renewal commission | provider-of-record | 61 |
| 17 | Payment terminal service book | POS installers | service owner exits | merchant approvals, device admin | service fees | payment/support liability | 67 |
| 18 | B2B toll-box commission book | fleet service agents | agent exits | provider-approved transfer | monthly commission | provider terms/churn | 66 |
| 19 | Fuel-card agent residual book | fleet agents | seller retires | issuer-approved residual assignment | monthly residual | issuer/credit risk | 72 |
| 20 | Corporate travel booking residual book | travel agents | small book succession | supplier/customer transfer | commission payment | travel support/low margin | 61 |
| 21 | Hotel channel-manager reseller book | hospitality tech agents | agent exits | vendor partner transfer | recurring commission | support/vendor terms | 72 |
| 22 | Restaurant POS SaaS residual book | local POS resellers | reseller exits | vendor-approved partner transfer | recurring commission | support/field work | 74 |
| 23 | Bookkeeping software reseller residuals | accountants | accountant exits add-on resales | vendor transfer, first commission | commission payment | accountants can keep | 64 |
| 24 | Security alarm monitoring reseller book | installers | installer retires | station/vendor transfer, customer approvals | monitoring fees | safety/field response | 62 |
| 25 | Fleet GPS/telematics reseller book | fleet tech agents | agent retires | vendor/customer transfer | monthly commission | support/field hardware | 70 |
| 26 | B2B broadband/fiber install order book | telecom agents | pending orders | carrier-approved order transfer | install commission | one-off/not residual | 65 |
| 27 | Payment gateway integration residuals | ecommerce consultants | consultant exits | gateway-approved residual assignment | monthly gateway residual | support/security | 78 |
| 28 | Merchant cash-advance referral residuals | finance brokers | broker exits | lender-approved payout transfer | commission payment | lending/regulatory | 55 |
| 29 | Leasing broker residual/referral book | equipment brokers | broker exits | lessor-approved commission transfer | commission payment | one-off, credit/legal | 63 |
| 30 | Marketplace agency retainer book | Amazon agencies | agency exits support book | customer-approved billing transfer | monthly retainer | service/trust | 66 |
| 31 | EPR compliance renewal book | packaging agents | recurring filings | customer approvals | filing fees | compliance advice | 66 |
| 32 | BDO waste reporting book | environmental clerks | reporting season | customer approvals | filing/admin fees | legal/accounting | 63 |
| 33 | Fire extinguisher inspection book | local inspectors | inspector retires | customer transfer | inspection cash | field/safety/licensed | 60 |
| 34 | Training-cert renewal book | safety trainers | trainer retires | customer transfer, trainer subcontract | renewal cash | instructor dependence | 65 |
| 35 | Commercial cleaning contract book | janitorial owner | owner exits small contracts | customer approvals, first month cash | monthly service cash | staffing/field ops | 58 |
| 36 | Parking-payment residual book | parking operators | agent exits locations | provider/customer transfer | commission | hardware/site support | 64 |
| 37 | Vending micro-route buyout | retiring route owner | route owner exits | site agreements, title, cashbox/POS cash | vending cash | field/logistics | 61 |
| 38 | Managed print click residual book | printer dealers | dealer exits small accounts | OEM/finance transfer, meter residual | monthly click revenue | hardware service | 72 |
| 39 | Payment chargeback agency residual | chargeback firms | agency exits cases | merchant approvals, first fee | monthly success fees | already crowded | 65 |
| 40 | POS fiscal device review book | fiscal-service owners | periodic review book | service-authorized transfer | review cash | authorized-provider dependence | 70 |

## Finalist Review

### Merchant Acquirer Residual Book Buyout

Why it advances:

- It controls an actual current payment stream, not a claim queue, dashboard, report, or evidence packet.
- The gate is written acquirer/master-agent approval and first residual cash movement before the founder pays meaningful consideration.
- The startup does not process merchant payments or hold merchant funds. Licensed acquirers/PSPs remain provider and merchant-of-record.
- Copy risk is transaction-specific: competitors can buy other residual books, but cannot copy an already assigned residual stream, seller handoff, noncompete, merchant list, and acquirer-approved payout direction.
- It is operationally lighter than direct service-book transfers because the payor is the acquirer/master agent and the end merchants remain on existing contracts.

Strict objections:

- Acquirer or master-agent agreements may block assignment or require the buyer to become an approved agent.
- Residual statements can be opaque and subject to chargebacks, clawbacks, merchant churn, terminal returns, fraud, high-risk merchant exclusions, and repricing.
- Good residual books may already be bought by ISOs, acquirers, POS dealers, or payment consultants.
- Some books may hide support obligations, field terminal issues, PCI/KYC questions, merchant complaints, or sales-misconduct liabilities.
- The first deal may prove a small financial asset purchase rather than a scalable company unless repeat seller sourcing works.

## Internal Simulated Score

**88.2 / 100**

This clears the simulation gate because the proof is current residual cash redirected by the payor, not founder influence over a discretionary counterparty. The strict condition is that the founder pays only after acquirer/master-agent written acceptance and first residual cash movement. If the real validator treats the residual assignment as rare, non-transferable, too regulated, or too small, kill this branch.

## Gate Decision

Advance Round 185 to working Zero To One validation.
