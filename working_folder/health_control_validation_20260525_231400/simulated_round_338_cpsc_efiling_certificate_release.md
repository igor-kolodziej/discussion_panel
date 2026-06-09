# Simulated Round 338: CPSC eFiling Certificate Release Queue

Date: 2026-05-31 Europe/Warsaw

## Pivot From Round 337

Round 337, `TwoCodePay Buyer-Issued Exception Release Queue`, failed working Zero To One validation at `73 / 100`. The decisive weakness was that the founder still depended on debtor/buyer internal AP action. This round shifts away from AP and ordinary recovery queues toward a current official filing gate where the first buyer can be a customs broker or importer with a live entry workflow and the proof artifact is accepted filing data, not interest or a generic compliance memo.

The current timing is specific. CPSC materials state that eFiling requirements for most imported consumer products subject to certification take effect on July 8, 2026, with Foreign Trade Zone entries later on January 8, 2027. CPSC certificate data includes product identification, certifier, applicable rules, manufacture date/place, testing date/lab, and record-holder contact. The candidate below does not certify product safety, test products, issue legal opinions, or act as customs broker. It controls a broker/importer-authorized certificate data file for a named SKU/import batch and returns accepted Product Registry / broker filing data or a clean no-go.

Official source notes used for timing and field structure:

- CPSC eFiling FAQ: `https://www.cpsc.gov/FAQ/eFiling-Frequently-Asked-Questions-FAQ`
- CPSC certificate/eFiling guidance: `https://www.cpsc.gov/Business--Manufacturing/Business-Education/Business-Guidance/Certificates`
- CPSC final rule release: `https://www.cpsc.gov/Newsroom/News-Releases/2025/CPSC-Approves-Final-Rule-to-Implement-eFiling-for-Certificates-of-Compliance`

## Raw Candidates

| # | Candidate | Buyer | Acute trigger | Transferable control point | Signed/titled/assigned/prepaid inside 60 days | First acquisition mechanism | Margin / payback logic | Copy risk and why incumbents cannot copy before control | Why not wrapper |
|---|---|---|---|---|---|---|---|---|---|
| 1 | CPSC eFiling Certificate Release Queue | CEE customs brokers, forwarders, importers, e-commerce sellers shipping CPSC-regulated products into the US | July 8, 2026 eFiling gate; broker cannot submit certificate data for current SKUs/entries | Importer/broker mandate, SKU/certificate file, Product Registry / broker filing status, certificate data map, source-doc no-go split | 3 broker pilots, 8 paid SKU/import batches, accepted certificate IDs or broker-ready data packets | Broker/forwarder outreach and Amazon/ecom compliance agencies with US import lanes | 6k-25k PLN per SKU family/import batch; high value versus held shipment/retailer stockout | Brokers/TIC labs can copy generic fields, but not the signed current SKU files and broker deadlines already controlled | Live entry/certificate release queue, not readiness training |
| 2 | Children's Product CPC eFiling Batch Desk | Importers of toys, children's apparel, juvenile products | CPC fields/test lab/manufacture data missing before entry | CPC/test report mapping, importer authorization, lab/source RFI | 6 paid CPC SKU cases | Toy importers and brokers | High if shipment value high | Toy compliance consultants strong | Narrow subcase |
| 3 | General Certificate GCC eFiling Batch Desk | Importers of furniture, rugs, household goods, adult products subject to rules | GCC data not in eFiling-ready form | GCC/product rule map and broker data packet | 6 paid cases | Brokers | Medium | Product-safety firms | Subcase |
| 4 | CPSC Product Registry Account Setup Lane | Importers | Business account/user setup and cert upload blocking broker | Product Registry account checklist and certificate upload | 10 paid setup cases | Broker referrals | Medium | CPSC resources/free setup | Too admin-like |
| 5 | Broker-Branded CPSC eFiling Overflow Cell | US customs brokers | Client flood before July 8 | White-label queue, broker templates, client files | 2 broker retainers and 20 SKUs | Brokers | Strong channel | Brokers internalize | Strong as channel for #1 |
| 6 | CPSC eFiling Reject Rescue Desk | Importers after ACE/CPSC rejection | Filing rejects for missing/invalid certificate data | Rejection code, product certificate file, corrected packet | 5 paid reject cases | Brokers after deadline | High urgency | Broker-owned | Useful later |
| 7 | CPSC Lab/Trade Party Data RFI Desk | Importers with foreign suppliers/labs | Certificate requires exact test lab and record-holder fields | Supplier/lab RFI, source evidence tracker | 10 paid RFIs | Importers | Medium | TIC labs closer | Submodule |
| 8 | CPSC Certificate Key Archive For Repeat Importers | Repeat importers | Same product repeats across shipments | Product Registry certificate-key library | 10 SKU subscriptions | Brokers | Recurring | Brokers/PLM can copy | Archive layer |
| 9 | CPSC FTZ January 2027 Prep Queue | FTZ importers | Later deadline for FTZ entries | FTZ-specific certificate file | 5 cases | FTZ operators | Medium | Less urgent now | Future |
| 10 | CPSC De Minimis Seller Import Rescue | Cross-border e-commerce sellers | Low-value shipments now face product certificate scrutiny | Seller/SKU/certificate file | Paid cases | Marketplaces | Medium | Platforms/brokers | Messy low-ticket |
| 11 | Amazon US CPSC Import Certificate Case Desk | Amazon sellers/importers | Amazon or FBA inbound asks CPC/GCC/eFiling readiness | Seller Central + import cert file | 5 paid ASIN/SKU cases | Amazon agencies | Medium-high | REDBlocked adjacency, Amazon agencies | Platform evidence desk |
| 12 | Walmart/Target Vendor CPSC eFiling Release Pack | Retail vendors | Retailer asks for eFiling/certificate proof before PO/shipment | Retailer request, cert file, broker data | 4 paid vendor cases | Retail compliance agencies | High | Retail compliance teams | Buyer evidence, not entry filing |
| 13 | CPSC Sleepwear Flammability Certificate Batch | Apparel importers | Children's sleepwear/apparel certificates missing fields | SKU/test report map | 5 cases | Apparel brokers | Good | Apparel labs | Narrow |
| 14 | CPSC Furniture/Rug GCC eFiling Batch | Home goods importers | GCC fields and rules unclear | Product/rule certificate map | 5 cases | Home goods brokers | Medium | Consultants | Subcase |
| 15 | CPSC Button Cell / Battery Door Certificate Lane | Importers of button-cell products | Reese's Law / battery compartment evidence appears in certificate needs | Product/test docs | 4 cases | Ecom/importers | Medium | Product safety firms | Testing risk |
| 16 | CPSC Recall-Risk No-Go Screen | Importers | Concern that cert data exposes noncompliance | No-go screen only | 3 cases | Counsel referrals | Medium | Lawyers | Legal risk |
| 17 | CPSC Small Importer Voluntary Stage Sprint | Importers before mandatory date | Need voluntary test filing before July | Registry setup + test certificate | 8 cases | Brokers | Medium | CPSC self-service | Admin |
| 18 | CPSC Broker Client Data Cleanup Batch | Brokers | Client spreadsheets incomplete | Data cleanup queue | Retainer | Brokers | Medium | Broker ops can do | Back office |
| 19 | CPSC Certificate Chain Reconstruction | Importers changing suppliers | Old CPC/GCC/test reports not tied to current product | Source-doc reconstruction and no-go | 5 cases | Ecom agencies | Medium-high | TIC/law firms | Can become certification |
| 20 | CPSC Accepted Lab Status Check Batch | Importers | Lab status or test-report owner ambiguity blocks cert | Lab status evidence and RFI | 6 cases | Toy importers | Medium | Labs/TIC | Submodule |
| 21 | CPSC SKU-to-Rule Applicability Triage | Importers with mixed catalog | Which SKUs need cert/eFiling | Rule triage | 10 cases | Brokers | Medium | Legal/safety classification risk | Too advisory |
| 22 | CPSC Certificate Holder Contact Update | Importers | Record-holder contact outdated | Updated certificate contacts | 10 cases | Brokers | Low | Admin | Too small |
| 23 | CPSC Product-ID Normalization Queue | Importers | Model/SKU/product IDs do not match invoice/entry/cert | Product identity match file | 10 cases | Brokers | Medium | Broker data ops | Submodule |
| 24 | CPSC Test Report Key Optional Evidence Pack | Importers | Want lower inspection risk with optional test report fields | Test report key mapping | 8 cases | Brokers | Medium | Labs | Optional weaker |
| 25 | CPSC Manufacturer Date/Place Evidence RFI | Importers | Foreign supplier cannot provide date/place data | Supplier RFI | 10 cases | Importers | Low-medium | Supplier/broker | Submodule |
| 26 | CPSC Trade Party Master Data Book | Brokers | Repeated labs/manufacturers/record holders across clients | Master data mapping | Retainer | Brokers | Medium | Broker systems | Data product but needs volume |
| 27 | CPSC Private Label Seller Certificate Rescue | Private label ecom sellers | Supplier provides generic certificate that does not match brand/model | Certificate mismatch file, supplier RFI | 5 cases | Ecom agencies | Medium-high | Amazon/product compliance agencies | Good subcase |
| 28 | CPSC CEE Exporter-to-US Certificate Pack | Polish/CEE manufacturers exporting consumer goods to US | US importer/broker asks for certificate/eFiling fields | Manufacturer certificate pack | 5 cases | Export advisers | Medium | Export consultants/TIC | Less acute unless shipment live |
| 29 | CPSC Shipment Hold Evidence Packet | Importer after CPSC/CBP hold | Hold asks for certificate data/docs | Hold notice, cert file, broker submission | 3 urgent cases | Brokers | High | Broker/legal counsel | Strong later, less POC before holds |
| 30 | CPSC Product Registry API/CSV Prep Service | Large importers | Need bulk upload format | Bulk data prep | 3 cases | Importers | Medium | Software/consultants | Implementation |
| 31 | CPSC Broker Training Kit | Brokers | Need train staff | Training docs | Paid workshops | Brokers | Low | Content/training | Reject |
| 32 | CPSC Consumer Product Certificate Generator | Importers | Need certificates generated | App form | Subscriptions | Online | Medium | SaaS/cert generators | App, legal risk |
| 33 | CPSC eFiling Audit Trail Vault | Importers | Need evidence record after filing | Record vault | Subscriptions | Brokers | Low-medium | PLM/compliance tools | Dashboard |
| 34 | CPSC Inbound Product Sampling Coordinator | Importers | Need test samples to labs | Sample custody | Paid cases | Labs | Medium | Labs/brokers | Logistics/testing risk |
| 35 | CPSC Lab Retest Slot Bank | Importers | Old tests insufficient; need lab retest before July | Lab slots and deposits | Prepaid lab slots | Labs | Medium-high | Labs control slots | Slot arbitrage |
| 36 | CPSC Children's Product Annual Recert Calendar Book | Importers | Recurring certificate refresh | Calendar and source docs | Retainers | Ecom agencies | Medium | Compliance tools | Not acute enough |
| 37 | CPSC Certificate Evidence For Finance/Insurance | Importers | Lender/insurer asks import compliance | Evidence pack | Cases | Finance channels | Low | Indirect | Weak |
| 38 | CPSC Retailer Onboarding Certificate Pack | Brands | Retailer wants CPC/GCC before launch | Retailer request + certificate file | Paid launch cases | Retail agencies | Medium-high | Retail compliance | Buyer-side, less official |
| 39 | CPSC Toys Marketplace Listing Rescue | Toy sellers | Marketplace listing suppressed over CPC | Marketplace request + certificate | 5 cases | Marketplace agencies | Medium | Already common | Too close to Amazon toy evidence |
| 40 | CPSC eFiling Transition No-Go Desk | Importers | Need know if shipment should not move | No-go memo with source defects | 5 cases | Brokers | Medium | Consultants | Submodule |

## Finalists And Strict Simulated Scores

| Rank | Candidate | Simulated score | Decision | Rationale |
|---|---|---:|---|---|
| 1 | CPSC eFiling Certificate Release Queue | **88.4** | Advance | The control point is a live broker/importer certificate file tied to an official July 8, 2026 entry gate. It is more concrete than readiness consulting because proof is accepted Product Registry/broker filing data, a certificate ID/data packet, or a clean no-go. |
| 2 | Broker-Branded CPSC eFiling Overflow Cell | 87.4 | Hold | Strong channel, but on its own the buyer is a broker outsourcing back-office labor and can internalize the queue. Fold into the lead as acquisition mechanism. |
| 3 | CPSC eFiling Reject Rescue Desk | 86.8 | Hold | High urgency after mandatory date, but not enough live cases before deadline and too broker-owned as a standalone. |
| 4 | Private Label Seller Certificate Rescue | 85.8 | Hold | Good pain but platform/account-health and supplier-document dependencies resemble weaker Amazon evidence cases. |
| 5 | Children's Product CPC eFiling Batch Desk | 85.5 | Hold | Useful subcase but product-safety consultants and labs are too close. |
| 6 | CPSC Shipment Hold Evidence Packet | 84.8 | Hold | Strong current-cash pain when holds occur, but the six-month POC depends on unpredictable holds and broker/legal handling. |

## Internal Cap Audit

- Not capped below 82: the 60-day proof is concrete and current: broker/importer mandates, live SKU/import batches, Product Registry/broker filing status, accepted certificate data packets, and no-go outcomes.
- Not capped below 85: although brokers and TIC labs can copy pieces, the first wedge is broker-routed overflow plus current certificate files. The score is still limited because broker internalization is credible.
- Not capped below 87: CAC and cash conversion are plausible only if brokers route cases and importers prepay. The score stays near the threshold rather than above 90 because durability after the transition is not proven.
- No unresolved clinical, patient, legal-practice, tax, insurance-adjusting, or regulated-drug authority.

## Lead Candidate

**CPSC eFiling Certificate Release Queue**

### Buyer

Customs brokers, freight forwarders, trade-compliance agencies, Amazon/e-commerce compliance agencies, and importers with CEE/EU customers shipping CPSC-regulated finished consumer products into the United States.

The first cases should come through brokers or forwarders with actual entry deadlines, not cold importers asking for abstract readiness.

### Acute Trigger

The importer has a named SKU family or shipment that must be eFiled under the CPSC certificate rules from July 8, 2026. The broker cannot file, test-file, or confidently prepare the entry because CPC/GCC fields, product identity, applicable rule citations, manufacturer date/place, testing date/place, lab identity, certifier, record-holder contact, Product Registry certificate status, or source-document match is incomplete or inconsistent.

### Control Point

The startup controls the current certificate-release file after a signed importer or broker mandate:

- named importer, broker, SKU family, entry/shipment deadline, and product scope;
- existing CPC/GCC, test reports, invoices, packing lists, SKU/model identifiers, PO and product photos where needed;
- Product Registry / certificate ID / data-entry status or broker filing packet;
- supplier/lab/manufacturer RFI tracker;
- mismatch and no-go register;
- broker-ready data packet with source references;
- accepted filing, Product Registry status, broker acknowledgement, or clean no-go outcome.

### 60-Day Proof

Within 60 days:

1. Sign at least three broker, forwarder, or compliance-agency referral pilots.
2. Close at least eight prepaid live SKU/import batches at 6,000-25,000 PLN each.
3. Cover at least 60 SKU/certificate lines across those batches.
4. Produce at least four objective outcomes: Product Registry certificate uploaded/accepted, broker-ready eFiling packet accepted by broker, voluntary-stage/test filing accepted, actual post-July entry filing accepted, or clean no-go before goods move.
5. Collect 80,000-180,000 PLN in prepaid fees.
6. Reject at least 30% of screened inbound SKU lines where certification/testing/source documents are missing or unsafe to package.

### 6-Month POC

Handle 50-120 paid SKU/import batches through 4-8 broker/channel partners and 20-50 importers. Build a private accepted/deficient certificate-data taxonomy by product family, broker, supplier-document pattern, trade party, lab/source-doc defect, Product Registry state, and filing/no-go outcome. Collect 450,000-1,200,000 PLN in fees with gross margin above 65% after product-safety reviewer, secure intake, and data-cleaning costs. Maintain a no-go/rework rate above 25% so the desk is not rubber-stamping certificates.

### Economics

- 6,000-10,000 PLN for one simple SKU family / certificate file.
- 12,000-25,000 PLN for a multi-SKU import batch or broker urgent queue.
- 20-30% channel margin for brokers/agencies where they own the client relationship.
- Gross margin target above 65% after reviewer time, secure document handling, data cleanup, and supplier RFI support.

The buyer pays because shipment entry, retailer/FBA stock timing, seasonal inventory, and broker readiness are at risk weeks before the mandatory eFiling date.

### Copy Risk

Customs brokers, product-safety consultants, CPSC lawyers, TIC labs, freight forwarders, and importer compliance teams can copy much of the checklist. The defensible wedge is narrower:

- broker-routed overflow during a timed mandatory transition;
- current SKU/certificate files already under mandate;
- repeated Product Registry and broker filing patterns;
- mismatch/no-go memory by product family and supplier-document type;
- Chinese-friendly supplier RFI language;
- channel trust from brokers who want to keep customs filing while outsourcing certificate-data rescue.

### Why Incumbents Cannot Copy Before Control

Once the broker or importer signs the paid mandate and sends the named SKU/certificate file, entry deadline, Product Registry status, supplier/lab contacts, and existing certificates/test reports, another provider cannot control that exact filing queue before the current deadline unless the buyer terminates the mandate. Incumbents can compete for future CPSC compliance programs, but not the specific broker-routed certificate file already under paid control.

### Why It Is Not A Service, Report, App, Dashboard, Database, Marketplace, Or Generic Broker

The unit is a live release queue with a defined filing outcome: accepted Product Registry certificate/data status, broker-ready packet accepted for filing, voluntary/test filing acceptance, post-deadline entry acceptance, supplier/lab rework, or clean no-go. The startup does not sell training, a checklist, a software form, broker introductions, or broad product-safety consulting.

### Boundaries And Legal / Provider Limits

- The importer/manufacturer remains responsible for certificate truth and product compliance.
- The customs broker remains customs broker and filer of record where applicable.
- CPSC-accepted labs perform testing when needed.
- Product-safety counsel handles legal interpretations and enforcement-sensitive cases.
- The startup does not issue CPC/GCC certificates unless the legally responsible party provides and approves them, does not certify product safety, does not classify product rules as a legal opinion, does not represent clients before CPSC/CBP, and does not handle recalls, suspected falsity, unsafe products, or disputed compliance.

### Duplicate-Risk Distinction

This is not REDBlocked because the marketplace/platform is not Amazon EU, the category is not connected baby monitors or indoor cameras, and the trigger is US CPSC eFiling certificate data for import entry. It is not CBAM, CATCH, OrganicCOI, EUDR, F-gas, CBP tariff refunds, Amazon Vendor Central, PromoLeak, KSeF, DORA, Data Act, GreenTender, Supplement Stack, BatteryFit, HeatQuiet, HeritageDoor, TraceFaktura, BioSignal, or a generic product-compliance desk. The controlled artifact is the CPSC certificate-data filing file tied to a live broker/importer entry path.

## Decision

Advance Round 338 to working Zero To One validation because the simulated score is strictly greater than 87 and the candidate is materially distinct from the exhausted AP, KSeF, Amazon, customs-broker-owned EU import-release, physical-lot, and generic evidence-desk branches.
