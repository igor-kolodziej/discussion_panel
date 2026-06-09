# Simulated Round 210: PackPlate Reorder Book Buyout

Date: 2026-05-30 Europe/Warsaw
Real gates: working Zero To One >=85 and fresh Zero To One >=85.
Simulation gate: advance only if simulated score is strictly above 87.

## Search Frame

Round 209 showed that sensitive-security books are capped by liability and specialist trust. Round 210 tests a lower-trust, current-cash book where the founder controls a repeat purchasing artifact: packaging dielines, print-ready files, plates/cylinders, approved proofs, SKU specs, supplier terms, order history, and customer-approved payment direction.

## Raw Candidate Control Table

| # | Candidate | Buyer/payor | Acute trigger | Transferable control point | 60-day proof | First acquisition | Economics/payback | Copy risk | Why incumbent cannot copy exact book first | Why not service/report/app/broker |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | Packaging source-file reorder book | food/cosmetics/ecommerce SMEs | retiring print broker, current reorders due | dielines, art, proofs, plates, supplier terms, customer approvals | 20 approvals, 150k PLN orders, 35k gross margin | retiring brokers/prepress shops | reorder margin + file custody | printers/brokers | exact files/orders controlled | acquired reorder book |
| 2 | Label/ribbon thermal print book | warehouses/retail | reorder specs | label specs/customer list | orders | suppliers | margin | commodity | exact customer book | commodity |
| 3 | Corporate uniform embroidery file book | SMEs | repeat uniform orders | digitized files/sizes | orders | embroidery shops | margin | many shops | exact files | low ticket |
| 4 | Promotional product logo file book | SMEs | merch reorders | art files/vendor specs | orders | promo firms | margin | many firms | exact files | commodity |
| 5 | Die-cut POS display reorder book | CPG brands | display reorders | dielines/proofs/supplier | orders | display printers | margin | display firms | exact files | project-based |
| 6 | Food label compliance source file book | food SMEs | label reorders | files/proofs | orders | label brokers | margin | label firms | exact files | compliance creep |
| 7 | Industrial product instruction leaflet book | manufacturers | manual/IFU reorders | print files/versions | orders | print brokers | margin | printers | exact version files | lower margin |
| 8 | Small carton cutting die inventory book | packaging customers | carton reorders | dies/dielines/customer history | orders | die shops | margin | packaging firms | exact die/customer link | physical dies |
| 9 | Flexible packaging cylinder/artwork book | food/cosmetics | pouch/sleeve reorders | cylinders/artwork/proofs | orders | brokers | margin | converters | exact cylinder/art | strong subset |
| 10 | Custom corrugated shipper reorder book | ecommerce brands | box reorders | dielines/vendor terms | orders | corrugated brokers | margin | box suppliers | exact specs | commodity-ish |
| 11 | Retail price-tag template book | retailers | seasonal tags | templates/order history | orders | printers | low | commodity | exact templates | low ticket |
| 12 | Wine/spirits label plate book | producers | vintage/season reorders | label plates/proofs | orders | printers | margin | label printers | exact files | alcohol boundary |
| 13 | Cosmetics carton/label reorder book | beauty SMEs | packaging reorders | files/proofs/supplier | orders | brokers | margin | printers | exact files | claims/compliance risk |
| 14 | Supplement label reorder book | supplement sellers | label reorders | files/proofs | reject | supplement risk | margin | printers | exact files | health/claims |
| 15 | Medical device label/IFU book | med suppliers | IFU/label reorders | reject | no | printers | high | regulated | exact files | med risk |
| 16 | Textile care-label reorder book | apparel SMEs | label reorders | specs/files | orders | label brokers | margin | many suppliers | exact files | low ticket |
| 17 | QR/warranty card print book | electronics sellers | reorders | files/supplier | orders | print shops | low | printers | exact files | commodity |
| 18 | Packaging barcode/GTIN proof book | CPG SMEs | GTIN/label reorders | art/proofs | orders | brokers | margin | GS1/printers | exact files | data errors |
| 19 | Printed bag/tape reorder book | ecommerce SMEs | recurring packaging | specs/files | orders | brokers | low-mid | suppliers | exact customer book | commodity |
| 20 | High-end boutique paper packaging book | luxury brands | reorders | dies/foil plates/proofs | orders | boutique printers | margin | boutique firms | exact dies/files | attractive subset |
| 21 | Restaurant menu print source book | restaurants | menus reprinted | files/customer list | orders | printers | low | can recreate | exact files | low margin |
| 22 | Event badge/lanyard template book | agencies | recurring events | templates/order history | orders | printers | seasonal | many | exact templates | project |
| 23 | Product carton photography/retouch file book | brands | reorders/update | source files | orders | studios | margin | studios | exact source | service |
| 24 | Technical drawing print archive book | engineers | plans reprint | CAD/PDF archive | orders | print shops | low | archives | exact files | archive-like |
| 25 | Safety sign template reorder book | factories | signs reorders | templates/customer list | orders | sign shops | low-mid | sign shops | exact templates | commodity |
| 26 | Fleet vehicle wrap artwork book | companies | vehicle additions | wrap files/supplier | orders | wrap shops | margin | sign shops | exact files | service/install |
| 27 | Retail shelf-edge label template book | stores | reorders | templates | low | printers | low | stores | exact templates | low |
| 28 | Printed electronics overlay/membrane book | industrial OEMs | overlay reorders | films/dies/specs | orders | specialty printers | high | specialty firms | exact tooling | good but technical |
| 29 | Control-panel frontplate artwork book | machine builders | reorders | art/dies | orders | printers | margin | machineplate-adjacent | exact art | prior plate failure |
| 30 | Packaging color proof library book | brands | match old print | proof library/files | orders | brokers | margin | printers | exact proofs | support |
| 31 | Board-game component print book | publishers | reprints | dielines/art/proofs | orders | game printers | margin | game printers | exact files | niche |
| 32 | Educational workbook print file book | schools/publishers | annual reprints | files/order history | orders | print brokers | margin | printers | exact files | IP rights |
| 33 | Custom stickers/decal reorder book | SMEs | stickers reorders | art/specs | orders | sticker printers | low | commodity | exact files | low |
| 34 | Industrial pouch/bag film spec book | manufacturers | material reorders | specs/supplier | orders | packaging brokers | margin | converters | exact specs | quality risk |
| 35 | Product sample card/packaging book | material suppliers | sample packs | files/dies | orders | printers | margin | printers | exact files | niche |
| 36 | Ceramic/tile decal print book | manufacturers | decal reorders | art/screens | orders | specialty printers | margin | specialty shops | exact screens | niche |
| 37 | Pharma OTC package print book | OTC sellers | package reorders | reject | no | printers | high | regulated | exact files | health/legal |
| 38 | Pet-food packaging reorder book | pet food SMEs | packaging reorders | art/dielines/proofs | orders | brokers | margin | printers | exact files | good subset |
| 39 | Frozen-food label/sleeve reorder book | food SMEs | seasonal reorders | art/dies/proofs | orders | brokers | margin | printers | exact files | food compliance |
| 40 | Industrial lubricant label/drum art book | chemical SMEs | label reorders | art/SDS links/proofs | orders | label brokers | margin | label firms | exact files | chemical compliance |

## Finalists

| Candidate | Internal simulated score | Advance? | Rationale |
|---|---:|---|---|
| PackPlate Reorder Book Buyout | **88.2** | **Yes** | Strongest lower-trust book: current packaging reorders, controlled source files/proofs/dies/supplier specs, customer-approved payment direction, and switching cost from recreating packaging artwork and proofing under deadline. |
| Flexible Packaging Cylinder/Artwork Book | 86 | No | Stronger artifacts but narrower, converter-owned, and higher quality/food compliance risk. |
| High-End Boutique Paper Packaging Book | 84 | No | Better margins but niche and design-service creep. |
| Printed Electronics Overlay Book | 83 | No | High-value repeat work but technically specialist and QA-sensitive. |
| Pet-Food Packaging Reorder Book | 81 | No | Real reorders but food-label compliance risk. |
| Corporate Uniform Embroidery Book | 76 | No | Source files are real but ticket size and defensibility are too low. |

## Selected Candidate

**PackPlate Reorder Book Buyout**

### Why This Advanced

The candidate is not another generic route book. The acquired asset is a reorder execution bundle:

- customer-approved packaging source files;
- dielines;
- plates/cutting dies/cylinder references where relevant;
- approved proofs and color targets;
- SKU version history;
- supplier specifications and pricing;
- repeat order history;
- current customer payment transfer.

Recreating packaging from scratch can cost time, proofing cycles, color mismatch, production delay, and supplier onboarding friction. That gives the book a stronger switching-cost asset than ordinary commodity consumables.

### Control Point

- Seller option over source files, dielines, proofs, color targets, supplier specs, plate/cylinder/die references, customer approvals, current orders, invoices, phone/domain/mailbox, and supplier terms.
- Customer-approved payment transfer before seller payout.
- Existing printers/converters remain production providers; the startup does not certify label compliance or manufacture packaging.

### 60-Day Proof

- Option one retiring print broker/prepress/packaging reorder book.
- Verify 40 active SKUs with source files, proofs, specs, order history, and supplier route.
- Obtain 20 customer reauthorizations and payment-direction approvals.
- Convert at least 150,000 PLN of current reorder value.
- Collect at least 35,000 PLN gross margin before seller payout.
- Complete 10 reorder jobs with fewer than 5% rework or color/spec dispute.

### Economics

- 8-20% gross margin on repeat packaging orders after printer/converter costs.
- 1,500-5,000 PLN source-file cleanup or SKU version-control fee for messy accounts.
- 2,000-12,000 PLN annual packaging source-file custody/reorder continuity retainer for larger accounts.
- Seller payout mostly earnout on retained gross margin, keeping upfront cash below 100,000 PLN.

### Internal Caps Applied

- Capped below 92 because printers, converters, brokers, and agencies can copy or buy books.
- Capped below 90 because customer files, IP rights, label compliance boundaries, and print-quality disputes can be messy.
- Not capped below 87 because the book has current cash, source-file custody, proof/spec switching cost, and customer payment transfer rather than mere goodwill.

## Simulated Zero To One Score

**88.2 / 100**

Passes the simulated gate because it is strictly above 87.

## Zero To One Prompt File

`/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/zero_to_one_prompt_packplate_reorder_book_buyout.txt`

## Kill Criteria

Kill this branch if:

- customer source-file rights are unclear or files belong to printers/customers rather than seller;
- customer reauthorization is below 40%;
- gross margin after printer/converter cost, shipping, rework, seller earnout, and admin is below 15%;
- reorders require new design, compliance review, or custom project management rather than repeat production;
- printers/converters or customers bypass the startup once the handoff is announced;
- Zero To One treats the book as ordinary print brokerage with weak defensibility.
