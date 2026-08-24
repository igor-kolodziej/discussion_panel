# Simulated Round 134: PPWR PFAS Food-Contact Packaging Release

Date: 2026-05-29
Real gate for this search: working >=85 and fresh >=85
Internal simulation gate: strictly >87

## Current Fact Check

Regulation (EU) 2025/40 on packaging and packaging waste entered into force on 11 February 2025 and generally applies from 12 August 2026. The European Commission guidance and PPWR Article 5(5) state that from 12 August 2026 food-contact packaging cannot be placed on the market if PFAS exceed specified concentration limits, unless another Union act already prohibits it. Guidance commentary notes that no general stock-exhaustion period solves this after the application date.

Sources checked:

- `https://environment.ec.europa.eu/topics/waste-and-recycling/packaging-waste_en`
- `https://eur-lex.europa.eu/legal-content/AUTO/?uri=LEGISSUM%3A4806724`
- `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=PI_COM%3AC%282026%292151`
- `https://environment.ec.europa.eu/document/download/02cef414-20f1-4871-8d58-3e0d7bc39c5c_en?filename=Communication+to+the+Commission_Approval+of+the+draft+Commission+Notice+on+the+Guidance+document+for+Regulation+EU+202540+on+packaging+and+packaging+waste.pdf`

## Raw Candidate Screen

| # | Candidate | Buyer | Acute cash/control trigger | 60-day control proof | Internal score | Decision |
|---|---|---|---|---|---:|---|
| 1 | PPWR PFAS FoodPack Order Release Pack | food-contact packaging converters and food brands | retailer/brand order or packaging run paused pending PPWR PFAS evidence | live PO/request, packaging BOM, supplier declarations/test evidence, customer-accepted release pack | 88 | Advance |
| 2 | PPWR Void-Space Packaging Redesign Release | ecommerce brands | order paused due empty-space ratio rules | carton redesign and customer approval | 78 | product redesign/service |
| 3 | PPWR Recyclability Declaration Pack | packaging converters | brand asks recyclability class evidence | supplier declarations | 80 | too broad and future 2030-heavy |
| 4 | PPWR EPR Multi-Country Listing Release | cross-border sellers | retailer/marketplace asks EPR registration proof | registrations and listing release | 76 | EPR agencies dominate |
| 5 | PPWR Label/Sorting Evidence Pack | brands | customer asks packaging label proof | label pack | 72 | low ticket/design compliance |
| 6 | Food-contact PFAS Lab Slot Bank | brands/converters | need fast PFAS testing slot | prepaid lab slot and report | 79 | broker/lab can copy |
| 7 | Food-contact Packaging Substitute Lot Bank | food brands | PFAS-risk packaging inventory unusable | buyer deposit for replacement lot | 82 | distribution/working-capital |
| 8 | PPWR Retailer Private-Label Release Desk | private-label suppliers | retailer asks PPWR/PFAS declarations | retailer evidence pack | 85 | fold into #1 |
| 9 | Molded Fiber PFAS-Free Run Reservation | QSR/food-service suppliers | customer needs grease-resistant PFAS-free packaging | supplier reservation and deposit | 83 | supplier/distributor risk |
| 10 | Bakery Greaseproof Paper PFAS Release | bakeries/converters | greaseproof paper evidence request | declarations/test | 84 | fold into #1 |
| 11 | Pizza Box / Food-Service Board PFAS Pack | converters | QSR order paused | evidence pack | 84 | fold into #1 |
| 12 | Pet-Food Packaging Contact Pack | pet-food brands | packaging compliance request | evidence pack | 82 | lower urgency |
| 13 | Cosmetics Packaging PPWR Pack | cosmetics brands | packaging request | evidence pack | 74 | not food-contact PFAS core |
| 14 | Toy Packaging PPWR Pack | toy brands | packaging request | evidence pack | 72 | not PFAS food-contact core |
| 15 | EUDR DDS Shipment Release Desk | coffee/cocoa/wood/rubber importers | customer asks EUDR data | DDS/customer pack | 82 | deadline moved to Dec 2026 |
| 16 | Battery EPR Listing Release | battery sellers/importers | marketplace asks EPR/battery proof | registration/evidence | 78 | agencies/platforms |
| 17 | Right-to-Repair Parts Access Desk | repair shops | part access blocks paid repair | OEM request and part release | 77 | legal/enforcement |
| 18 | EU Withdrawal Button Emergency Pack | ecommerce/subscription sellers | June 2026 deadline | production deploy | 74 | app/dev agency |
| 19 | VoP Payee-Name Payment Release | B2B suppliers | bank transfer warning blocks payment | payee alias pack | 80 | bank/AP-owned |
| 20 | Construction Retention Release Desk | subcontractors | retention cash locked | release letter/payment | 81 | legal/contract managers |
| 21 | Warranty-Bond Substitution Desk | contractors | retention cash replaceable by bond | bond and release | 82 | brokers/lawyers |
| 22 | Customs Guarantee Release Pack | importers | guarantee/deposit tied up | customs release | 79 | customs brokers |
| 23 | Merchant Acquirer Reserve Release | merchants | payout reserve held | reserve release | 78 | PSP discretion |
| 24 | OTA Commission Recovery | hotels | OTA statement errors | credit | 74 | revenue managers |
| 25 | Freight Detention Credit Recovery | importers | accessorial invoice errors | carrier credit | 80 | freight audit incumbents |
| 26 | Public Tender Bond Refund Release | contractors | bid/performance deposit not returned | refund | 73 | admin/legal |
| 27 | Product Recall Insurance Evidence Pack | brands | insurer asks recall docs | claim pack | 75 | insurance adjusters |
| 28 | Amazon GPSR Generic Listing Release | marketplace sellers | listing blocked by GPSR docs | case pack | 78 | REDBlocked adjacency/agencies |
| 29 | Cosmetic CPNP Marketplace Release | cosmetic sellers | listing blocked by CPNP/PIF/RP | case pack | 80 | RP/labs own |
| 30 | AI Model-Risk Renewal Pack | AI vendors | bank renewal blocker | evidence room | 77 | Round 133 failed |

## Finalists

| Candidate | Control point | Copy risk | Economics | Simulated score |
|---|---|---|---|---:|
| PPWR PFAS FoodPack Order Release Pack | live customer/retailer request, PO/run at risk, packaging BOM, supplier declarations/test evidence, customer response pack | labs, packaging consultants, FCM lawyers, packaging suppliers | 7k-30k PLN per release case; high value if PO/run is at risk | 88 |
| PPWR Retailer Private-Label Release Desk | live private-label customer request | retailer compliance teams and labs | 10k-35k PLN | 85 |
| Bakery Greaseproof Paper PFAS Release | narrow high-risk material category | paper suppliers/labs | 5k-20k PLN | 84 |
| Food-contact Packaging Substitute Lot Bank | reserved replacement lot | packaging distributors | margin/working-capital risk | 82 |
| EUDR DDS Shipment Release Desk | shipment/customer request | consultants/software | deadline future | 82 |

## Selected Candidate

PPWR PFAS FoodPack Order Release Pack.

## Why It Clears Internal Simulation

- The deadline is near-term and legally specific: food-contact packaging with PFAS above limits cannot be placed on the market from 12 August 2026.
- The payment event is a live retailer/brand-owner/customer order, packaging run, private-label approval, or Q3 reorder that can be paused before the legal date.
- The startup controls a specific case file rather than selling readiness: customer request, PO/run, packaging BOM, material supplier declarations, existing test evidence, lab sample path, no-go/substitute branch, and buyer response matrix.
- The first proof is commercial: one customer accepts evidence or releases a packaging run/order.
- The work is narrow enough for a solo founder with a packaging/FCM reviewer and lab contact, while avoiding legal certification and chemical testing authority.

## Internal Caps Applied

- Not capped below 82: concrete control proof exists through a live PO/run/customer request and customer acceptance.
- Not capped below 85: generic consultants can copy the category, but cannot instantly displace an active customer order-release workflow after the founder controls the packaging BOM, declarations, lab path, and response pack.
- Not capped below 87: CAC/payback/margins/cash conversion are credible only if accepted cases have order/run value above 150,000 PLN and prepaid fees.
- Main residual risk: packaging suppliers, labs, and FCM lawyers are natural incumbents; the source evidence may not exist or may reveal a no-go.

## Simulated Score

88 / 100

Proceed to working Zero To One validation.
