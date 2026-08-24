# Simulated Round 231: ItalyFBA VAT/VIES Inventory Release Desk

Date: 2026-05-30 Europe/Warsaw

## Gate Settings

- Real working-chat Zero To One gate: `>=85`
- Real fresh-chat Zero To One gate: `>=85`
- Internal simulation gate: strictly `>87`
- Prompt hygiene: no evaluator cap instructions in the Zero To One prompt

## Current Platform / Timing Check

Amazon's Pan-European FBA policy says sellers authorize Amazon to store inventory in placement-enabled countries and that the VAT number provided in Seller Central must be listed in the European Commission's VIES to be considered valid for the policy.

Amazon's Seller Forums show a 2026 Italian VAT/VIES issue where sellers reported Italian VAT numbers becoming invalid, account deactivation threats, and inventory restrictions. An Amazon forum response stated that where Amazon records indicate shipping from Italy, a seller is required to provide a valid VIES VAT number or applicable VAT number for EU transactions, and that since Italy no longer allows fiscal representation from January 2026 the seller must complete direct registration with Italian tax authorities.

Sources checked:

- https://m.media-amazon.com/images/G/02/rainier/help/legal/Amazon_PanEU_FBA_Terms_and_Conditions_English_080920.pdf
- https://sellercentral-europe.amazon.com/seller-forums/discussions/t/7a608ecb-f77a-4edd-a3cf-7e5211143715
- https://sell.amazon.it/en/imparare/centro-di-conoscenza-dell-iva?mons_sel_locale=en_GB

## Search Frame

This round tests a platform inventory lock where current cash is in unsellable FBA units, not a generic VAT registration service and not a product-safety evidence packet.

The candidate only advances if the control point is:

- a live Seller Central VAT/VIES warning or inventory restriction;
- seller authorization;
- tax-adviser proof or valid VIES/VAT status supplied by the responsible adviser;
- Amazon case IDs and inventory-country evidence;
- first sellable-status or removal/placement progress.

## Raw Candidate Table

| # | Candidate | Buyer | Acute trigger | Transferable control point | 60-day proof | Copy risk / cap note | Internal score |
|---:|---|---|---|---|---|---|---:|
| 1 | ItalyFBA VAT/VIES inventory release desk | Amazon EU sellers via agencies/tax advisers | Italy/Pan-EU inventory restricted over VAT/VIES mismatch | Seller Central warning, VAT adviser proof, case IDs, inventory-country file | 12 cases, 5 release/progress outcomes | tax advisers/Amazon agencies can copy; strict boundaries needed | 88.0 |
| 2 | Amazon Vendor Central recovery mandate | Amazon 1P vendors | deductions/chargebacks | Vendor Central disputes | already failed | incumbents | 67 |
| 3 | FBA stranded inventory evidence desk | FBA sellers | stranded/unsellable inventory | ASIN/FBA case file | failed branch | platform opacity | 66 |
| 4 | Merchant Center suspension release | ecommerce sellers | Google listing suspension | MC case file | previous failed | agencies copy | 77 |
| 5 | ButtonCell Amazon release | Amazon sellers | battery safety evidence | agency case | previous failed | labs/docs | 77 |
| 6 | MoCRA Amazon release | cosmetics sellers | FDA/MoCRA evidence | agency case | previous failed | regulatory advisers | 67 |
| 7 | EPR marketplace release | Amazon/Kaufland/Allegro sellers | EPR evidence blocks | provider evidence | previous failed | commoditized | 76 |
| 8 | CPSC eFiling entry release | importers | broker eFiling issue | entry data | previous failed | broker/product safety | 70 |
| 9 | VAT ghost inventory mapping desk | Amazon sellers | Amazon thinks stock stored in wrong country | inventory node report, case ID | 8 cases | too narrow/platform support | 80 |
| 10 | Pan-EU country deactivation safe-removal lane | FBA sellers | needs to disable country without stranded stock | settings/removal file | 8 cases | Amazon support/agency | 72 |
| 11 | Amazon VAT tax-adviser handoff desk | tax advisers | client cases stuck after valid VAT | case prep | 12 cases | adviser internalization | 81 |
| 12 | EU VAT deregistration unsellable rescue | sellers | deregistered VAT still flagged | tax proof + Amazon case | 8 cases | tax/legal | 76 |
| 13 | FBA removal fee avoidance desk | sellers | unsellable units/storage fees | removal/reprice file | 10 cases | normal FBA ops | 61 |
| 14 | VAT number entity mismatch release | Amazon sellers | name/address mismatch | tax proof + Seller Central file | 8 cases | tax adviser owns | 78 |
| 15 | FBA fiscal representative transition desk | non-EU sellers | fiscal rep change | tax adviser route | 8 cases | legal/tax, providers | 75 |
| 16 | Amazon Spanish VAT VIES release | EU sellers | Spain VAT invalid | case file | 8 cases | tax incumbents | 76 |
| 17 | EU OSS/FBA country-mapping release | sellers | OSS vs storage conflict | inventory-country proof | 8 cases | complex tax | 70 |
| 18 | Amazon Pan-EU enrollment release | sellers | ASIN not PAN eligible | listing/offers/VAT proof | 10 cases | Amazon agency | 68 |
| 19 | VAT service provider refund recovery | sellers vs tax providers | paid registration not done | refund/chargeback file | 5 recoveries | legal/scam/trust | 58 |
| 20 | TikTok Shop EU VAT lock release | sellers | payout/listing blocked | tax file | 8 cases | platform/tax | 65 |
| 21 | Etsy DAC7/VAT payout release | sellers | payout blocked | tax evidence | 10 cases | low ticket | 58 |
| 22 | App store trader verification release | app devs | EU DSA trader data blocks update | developer evidence | 10 apps | low ticket | 63 |
| 23 | Shopify Payments reserve release | merchants | payout reserve | PSP case | previous PSP lesson | provider discretion | 62 |
| 24 | PayPal reserve release | merchants | funds hold | PSP case | 5 cases | support/legal | 57 |
| 25 | Stripe Tax ID mismatch payout release | SaaS/ecom | payout hold | KYC/tax file | 8 cases | PSP control | 60 |
| 26 | KSeF AP release | Polish suppliers | invoice payment hold | AP evidence | previous failed | accountants/ERP | 79 |
| 27 | SENTApparel dispatch release | wholesalers | shipment release | dispatch gate | previous failed | normalization/incumbents | 68 |
| 28 | Retailer DRS SKU release | beverage suppliers | SKU/order blocked | DRS file | previous failed | operator/label | 74 |
| 29 | PPWR PFAS order release | packaging suppliers | order blocked | supplier/lab evidence | previous failed | labs/legal | 78 |
| 30 | Italian marketplace VAT tax-adviser ticket book | tax advisers | repeated Seller Central VAT cases | partner tickets | 3 partners | adviser internalization | 82 |
| 31 | Amazon EU VAT case-book buyout | small Amazon agency | current VAT issue tickets | assigned ticket/billing | one agency, 10 cases | seller rare/platform | 79 |
| 32 | FBA inventory-country report recon service | sellers | ghost nodes | report/case | 20 cases | app/agency copy | 66 |
| 33 | Pan-EU VAT account-health triage | agencies | VAT warnings | triage sheet | 20 cases | report | 58 |
| 34 | FBA VAT removal-order release desk | sellers | cannot remove unsellable inventory | removal file | 10 cases | Amazon support | 68 |
| 35 | Amazon Italian VAT proof-of-application bridge | sellers | VAT pending, deactivation clock | application proof + Amazon case | 8 cases | tax adviser/Amazon discretion | 72 |
| 36 | FBA seller tax-provider failure audit | sellers | VAT provider failed | evidence for refund | 5 cases | legal/dispute | 55 |
| 37 | Amazon EU tax dashboard status monitor | sellers | VAT status changes | monitor | subscriptions | dashboard/app | 49 |
| 38 | Amazon agency white-label VAT desk | agencies | clients ask VAT lock help | white-label cases | 3 agencies | agencies can internalize | 78 |
| 39 | VAT/VIES inventory release retainer | sellers | repeated country locks | retainer | 5 accounts | recurring uncertain | 76 |
| 40 | Amazon VAT sellable-status release lane | sellers | sellable status blocked | case status | 10 cases | selected candidate narrower | 86 |

## Selected Candidate

**ItalyFBA VAT/VIES Inventory Release Desk**

## Simulated Score

**88.0 / 100**

## Internal Scoring Rationale

This is a stronger platform-lock test than broad Amazon evidence desks because the economic event is current inventory becoming unsellable or restricted, not a speculative compliance readiness file. The proof is also harder than a memo:

- live Seller Central VAT/VIES warning or restriction;
- inventory-country report or VAT dashboard status;
- tax-adviser supplied proof or VIES-active number;
- Amazon case IDs and escalation trail;
- sellable-status progress, removal progress, or clean tax-adviser no-go.

The candidate passes simulation only if the startup refuses tax registration/advice and acts as the agency-routed operational release layer after the responsible tax adviser has source truth.

## Internal Caps Applied

- Cap below 82 if the offer includes VAT registration, tax advice, fiscal representation, or legal/tax opinions.
- Cap below 85 if the case lacks live Amazon restriction or current inventory value.
- Cap below 87 if the only output is an evidence packet without Seller Central case progress or inventory-status movement.
- Cap below 87 if partner/tax adviser channels do not route repeat cases.

## Main Risks To Test

1. Tax advisers and Amazon agencies are natural owners.
2. Amazon outcomes are opaque and slow.
3. Many cases require actual VAT registration or tax authority processing, outside startup control.
4. Non-EU seller trust and sensitive tax data are hard.
5. The issue may be a 2026 transition wave around Italy/fiscal representation rather than durable.
6. Simple cases may be solved by Seller Central support or tax providers.

## Gate Decision

Advance to working-chat Zero To One validation using:

`zero_to_one_prompt_italyfba_vat_inventory_release.txt`
