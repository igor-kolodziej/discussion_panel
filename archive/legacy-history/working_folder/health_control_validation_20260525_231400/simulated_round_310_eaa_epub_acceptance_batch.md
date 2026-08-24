# Simulated Round 310 - EAA EPUB Acceptance Batch

Date: 2026-05-31 Europe/Warsaw

Current real validation gates: working Zero To One >=85; fresh Zero To One >=85. Internal simulation gate: only validate if simulated score is strictly >87.

## Search Pivot

Round 309 failed fresh because the main asset was an assumed seller book whose supply may be rare. Round 310 avoids rare seller supply and tests a visible, current, file-level control object: named EPUB/title batches that a publisher, distributor, library supplier, or retailer needs accepted under European Accessibility Act pressure.

The prior EAA buyer accessibility sprint scored only 77 because it looked like a crowded accessibility-agency service. This narrower variant removes open-ended web/app remediation and focuses on specific ebook files, metadata, EPUBCheck/accessibility findings, distributor/library rejection notes, and resubmitted files. The first proof is file acceptance or narrowed defect lists, not an audit report.

Context sources used for timing and technical shape:

- European Commission digital policy page says the European Accessibility Act entered application on 28 June 2025 and covers selected products and services.
- The Commission news page lists e-books among the product/service areas covered by the Act.
- ETSI EN 301 549 is the ICT accessibility standard commonly used for EAA technical mapping.
- W3C EPUB 3.3 and EPUB Accessibility 1.1 define EPUB accessibility conformance and discoverability requirements.

Sources:

- `https://digital-strategy.ec.europa.eu/en/news/eu-becomes-more-accessible-all`
- `https://commission.europa.eu/news-and-media/news/eu-becomes-more-accessible-all-2025-07-31_en`
- `https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_20/en_301549v030201a.pdf`
- `https://www.w3.org/publishing/epub3/`
- `https://www.w3.org/TR/epub-a11y-11/`

## Raw Candidate Control Table

| # | Candidate | Buyer/payor | Acute trigger | Transferable control point inside 60 days | First acquisition mechanism | Economics | Copy risk / cap |
|---:|---|---|---|---|---|---|---|
| 1 | EAA EPUB Acceptance Batch | small and mid-size publishers, ebook distributors, library suppliers | title batch rejected or at risk because EPUB/accessibility metadata/files are deficient | prepaid title batch, files, rejection notes, metadata, remediation queue, resubmission trail | publisher/distributor outreach around live title batches | 350-1,200 PLN/title, 8k-45k batches | publishing vendors can copy, but exact files and resubmission queue controlled |
| 2 | Generic EAA web remediation sprint | B2B SaaS/ecommerce vendors | buyer asks accessibility | sprint access | prior 77 | 12k-35k | rejected, crowded agencies |
| 3 | App-store accessibility rejection release | app publishers | app review rejects accessibility | app issue list | mobile agency channel | 8k-30k | mobile dev shops |
| 4 | Public-sector PDF accessibility batch | municipalities/vendors | tender or public body rejects PDFs | file batch | PDF vendors | per page | crowded and low ticket |
| 5 | EAA ecommerce checkout component fix | checkout SaaS | merchant buyer blocks checkout | component repo and defect list | PSP partners | sprint fee | dev shops |
| 6 | EAA audiobook/ebook metadata correction | publishers | distributor metadata warnings | ONIX/accessibility metadata | metadata vendors | batch fee | too small |
| 7 | EPUB fixed-layout remediation for illustrated books | publishers | FXL titles inaccessible | titled files | publisher outreach | high per title | complex, low repeat |
| 8 | Academic publisher EPUB procurement pack | academic publishers | library framework asks accessibility | title batch and VPAT notes | library suppliers | batch fee | academic vendors |
| 9 | Library vendor accessibility acceptance desk | library content aggregators | library buyer asks accessible titles | supplier files and library request | aggregators | batch fee | aggregators internalize |
| 10 | KDP/Apple/Google EPUB acceptance cleanup | self-publishers | store rejects files | files and account rejection | author communities | low | consumer support, avoid |
| 11 | Accessible ebook conversion book buyout | retiring conversion shop | recurring publisher clients | customer payment transfer | seller | MRR | seller rarity, service book |
| 12 | ONIX accessibility metadata batch | publishers | retailers demand accessibility metadata | ONIX records | metadata tools | low | metadata vendors |
| 13 | Backlist triage no-go batch | publishers | need classify legacy backlist | title list | publishers | low | report-only |
| 14 | EPUB alt-text sprint | publishers | missing image descriptions | image files | freelancers | per title | commodity |
| 15 | EPUB reading order remediation | publishers | validators fail reading order | files | publishers | batch | conversion vendors |
| 16 | Publisher distributor holdback release | publishers | distributor withholds title listing | rejection ticket and files | distributors | success fee | platform acceptance |
| 17 | EAA e-reader software acceptance | e-reader vendors | app/device questions | code/product evidence | vendors | high | too technical/incumbents |
| 18 | University press accessibility rescue | university presses | library framework | files and procurement note | public targets | medium | public procurement |
| 19 | Accessible PDF-to-EPUB replacement batch | publishers | PDFs no longer accepted | source PDFs and EPUB outputs | publisher lists | batch | conversion vendors |
| 20 | Bookshare/ONIX discoverability fix lane | publishers | discoverability missing | metadata | accessibility nonprofits | low | low ticket |
| 21 | EAA digital textbook acceptance batch | edtech publishers | school/platform rejects textbooks | HTML/EPUB files | edtech channels | high | LMS/content vendors |
| 22 | Transport timetable PDF accessibility release | transport operators | authority/customer request | PDF batch | agencies | medium | accessibility agencies |
| 23 | Bank statement PDF accessibility packet | fintechs/banks | customer complaint | doc templates | fintech vendors | high | banks/vendors |
| 24 | Insurance policy document accessibility batch | insurers/insurtechs | renewal/customer request | template files | doc-gen vendors | high | insurers/doc vendors |
| 25 | Ticketing PDF/mobile wallet accessibility fix | ticketing vendors | venue/operator issue | tickets/templates | ticketing vendors | medium | product teams |
| 26 | Accessible invoice PDF batch | SaaS vendors | customer asks accessible invoices | templates | SaaS support | medium | product teams |
| 27 | Publisher accessibility statement pack | publishers | need public statement | title process | publisher advisors | low | report-only |
| 28 | EAA national-market exemption/no-go memo | publishers | unsure scope | legal facts | lawyers | fee | legal, reject |
| 29 | Retailer title delisting recovery | publishers | title delisted | files + ticket | distributors | batch | platform opacity |
| 30 | EPUB QA contractor bench | conversion vendors | overflow | contractor capacity | agencies | staffing | not a business |
| 31 | Translation memory accessibility check | publishers | translated titles | files | LSPs | per title | low |
| 32 | Accessible manga/comic ebook remediation | publishers | image-heavy title blocked | title files | manga publishers | high | complex alt-text/licensing |
| 33 | Library tender sample-title acceptance | publishers | tender demands sample accessible files | sample batch | tender notices | fee | tender advisors |
| 34 | Ebook subscription platform supplier batch | subscription platforms | suppliers send inaccessible files | supplier batch | platforms | batch | platform internalizes |
| 35 | Publisher-side accessibility evidence room | publishers | buyer asks evidence, no file change | records | publishers | fee | report-only |
| 36 | EPUBCheck validator wrapper | publishers | validation errors | app | product-led | subscription | app/dashboard |
| 37 | Accessibility metadata database | publishers | discoverability | database | subscription | low | database |
| 38 | Marketplace for ebook remediators | publishers | need experts | broker intros | platform | margin | marketplace |
| 39 | AI alt-text generator for books | publishers | image descriptions | SaaS | product | subscription | AI wrapper |
| 40 | EAA compliance training for publishers | publishers | deadline awareness | training | webinars | low | training |

## Finalists

| Finalist | Control strength | Decision |
|---|---|---|
| EAA EPUB Acceptance Batch | Specific title files, validator findings, distributor/library rejection notes, metadata, remediated outputs, resubmission trail, prepaid batch | Advance. Strongest because the object is a named batch of files with acceptance output, not an advisory audit. |
| EAA digital textbook acceptance batch | Higher ticket but entangled with LMS/product teams, copyright, and education procurement | Reject for first pass. |
| Academic publisher EPUB procurement pack | Good buyer pressure but likely lower speed and public/procurement bureaucracy | Reject. |
| Retailer title delisting recovery | Strong acute trigger but platform opacity and consumer author noise | Reject. |
| App-store accessibility rejection release | Operationally concrete but mobile dev shops own fixes | Reject. |
| Insurance policy document accessibility batch | Potentially high ticket but doc-generation vendors and insurers own templates | Reject. |

## Internal Cap Check

- Concrete 6-month control proof exists: prepaid title batches, original files, accessibility/EPUBCheck findings, distributor or library rejection notes, metadata records, remediation queue, resubmission trail, and accepted/narrowed defects.
- First proof is not interest: the publisher pays for a named batch, and the output is file acceptance, distributor/library progress, or explicit no-go for unsalvageable files.
- This avoids broad EAA service risk by rejecting web/app/product redesign and accepting only bounded EPUB/title files.
- Copy risk remains material because ebook conversion houses, accessibility agencies, publishers' production teams, freelancers, and distributors can do similar work. The defense is fast case intake, exact file control, narrow batch packaging, Polish/CEE publisher/distributor outreach, and repeated acceptance pattern memory.
- Internal score is capped below 90 because file remediation is still a productized service, not a legal asset or assigned payment stream. It clears the simulation gate only because the deliverable is concrete, batchable, urgent after EAA application, and tied to distribution/listing/procurement acceptance rather than generic compliance posture.

## Simulation Verdict

**Advance: EAA EPUB Acceptance Batch**

Simulated score: **88.1 / 100**

Rationale: The idea is materially stronger than the prior EAA buyer accessibility sprint because it removes open-ended UI/product remediation and narrows to title-level file acceptance. It has a visible buyer trigger, compact digital goods, clear before/after artifacts, low capital requirements, and batch economics. The ceiling is limited by crowded publishing-accessibility vendors and the possibility that publishers can use existing conversion shops.
