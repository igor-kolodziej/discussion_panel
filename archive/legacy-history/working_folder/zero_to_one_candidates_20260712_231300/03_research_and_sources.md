# Research and Sources

Research date: 2026-07-12. Evidence below is separated from business hypotheses. Direct sources are preferred; vendor pages are used only for competition or technical feasibility.

## Cross-Cutting Physical-AI Evidence

- **Evidence:** NVIDIA's GR00T training mix explicitly includes egocentric human video and real robot trajectories. [NVIDIA Research](https://research.nvidia.com/publication/2025-03_nvidia-isaac-gr00t-n1-open-foundation-model-humanoid-robots)
- **Evidence:** Electrical-cabinet automation remains an active research target; a February 2026 paper addresses DIN-rail terminal assembly in simulation, while separate connector work describes wiring as difficult because of deformable cables and geometry variance. [Electrical cabinet assembly paper](https://arxiv.org/abs/2602.14561), [connector assembly paper](https://arxiv.org/abs/2602.22100)
- **Evidence/competition:** Commercial firms already sell generic human, egocentric, teleoperation, and task-specific manipulation data. [Amplibotics](https://www.amplibotics.ai/), [Operant](https://www.operantdata.com/services/robot-demonstration-data), [Roborecs](https://roborecs.com/), [Renlei Labs](https://renleilabs.com/)
- **Evidence/competition:** Renlei explicitly lists electrical work, while Operant states that useful demonstrations must match the robot, environment, and evaluation goal. This weakens the thesis that human video plus a common board is sufficient before buyer-specific embodiment work.
- **Hypothesis:** A shippable standardized cabinet board, tool-state/torque telemetry, failure/recovery episodes, and electrician-grade task taxonomy are scarce enough to escape generic data-collection competition.
- **Hypothesis:** At least two European robotics teams will pay 15,000–60,000 PLN for a schema-confirmed task capsule or benchmark before the founder buys a robot.

## SealFault Evidence

- **Evidence:** Moving toward recyclable mono-material packaging can narrow process windows, while continuous seal inspection remains a technical problem. [Fraunhofer IVV OCTinline](https://www.ivv.fraunhofer.de/en/processing-machinery/octinline.html)
- **Evidence:** Commercial systems detect seal contamination, weak seals, pinholes, and other defects through vision or leak testing; this proves buyer pain and also establishes strong equipment competition. [Bizerba PackSecure](https://www.bizerba.com/ca/en/products/sealsecure), [Sepha PakScan](https://sepha.com/products/leak-testing/pakscan/), [Cognex seal inspection](https://www.cognex.com/industries/food-and-beverage/packaging-inspection/tamper-and-safety-seal-inspection), [Valco Melton PouchChek](https://www.valcomelton.com/en/product/pouchchek-heat-seal-inspection-system)
- **Evidence:** Regulation (EC) 852/2004 requires packaging operations to avoid contamination and protect product integrity. [EUR-Lex](https://eur-lex.europa.eu/legal-content/en/ALL/?uri=CELEX%3A32004R0852)
- **Evidence:** The Packaging and Packaging Waste Regulation increases pressure toward recyclable formats and applies generally from August 2026. [European Commission](https://environment.ec.europa.eu/topics/waste-and-recycling/packaging-waste_en), [Regulation (EU) 2025/40](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32025R0040)
- **Hypothesis:** Vendors and packaging labs will pay for a neutral blind physical benchmark rather than make defects internally.
- **Hypothesis:** A first 300–500-specimen matrix and basic seal-strength/leak ground truth can be built for less than 90,000 PLN without claiming accredited certification.

## SafeCassette Evidence

- **Evidence:** Poland's Civil Protection and Civil Defence Act establishes the new operating framework. [Official act](https://eli.gov.pl/api/acts/DU/2024/1907/text.html)
- **Evidence:** Official recognition criteria require filter ventilation and extended protective operation for shelters; operating rules include filter replacement. [Recognition criteria](https://eli.gov.pl/api/acts/DU/2025/235/text/O/D20250235.pdf), [Operating rules](https://eli.gov.pl/api/acts/DU/2025/933/text/O/D20250933.pdf)
- **Evidence:** The 2025–2026 national program allocated almost 34 billion PLN, and a February 2026 Mazowieckie call explicitly funds inventory, modernization, building work, and essential equipment. [National program](https://www.gov.pl/web/premier/uchwala-w-sprawie-zatwierdzenia-programu-ochrony-ludnosci-i-obrony-cywilnej-na-lata-2025-2026), [2026 call](https://www.gov.pl/web/olioc/320-mln-zl-na-obiekty-zbiorowej-ochrony---nabor-wnioskow-rusza-23-lutego)
- **Evidence:** Public tenders for shelter assessments are active in 2026. [Zamość notice](https://ezamowienia.gov.pl/mo-client-board/bzp/notice-details/id/08de54fb-7195-52fb-d6d3-f500016a9e7e)
- **Evidence/competition:** FASER sells multiple stationary shelter filter-ventilation units, Eurofaser advertises modernization of old RM systems, and Shelters.pl imports and renovates shelter equipment. [FASER](https://faser.com.pl/produkty/sprzet-wojskowy/urzadzenia-filtrowentylacyjne/), [Eurofaser](https://www.eurofaser.pl/), [Shelters.pl](https://shelters.pl/)
- **Hypothesis:** A small set of recurring legacy geometries covers enough facilities to justify a standard adapter family.
- **Hypothesis:** A prototype can be lawfully tested without the POC becoming a full safety-certification program above 100,000 PLN.

## AccessCore Evidence

- **Evidence:** The European Accessibility Act covers relevant self-service and payment-terminal use cases, and Poland has implemented it nationally. [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj/eng), [Polish Accessibility Act](https://eli.gov.pl/eli/DU/2024/731/ogl), [UKE summary](https://uke.gov.pl/wydarzenia/dostepnosc-produktow-i-uslug%2C5.html)
- **Evidence/competition:** ANKER's EAA-Pad, Storm tactile/audio interfaces, and JAWS for Kiosk already provide accessible hardware and software components. [EAA-Pad](https://en.anker.net/eaa-pad), [Storm Interface](https://www.storm-interface.com/products/), [JAWS for Kiosk](https://vispero.com/jaws-for-kiosk/)
- **Hypothesis:** Small CEE OEMs still lack a lower-cost combined reference design, firmware, localized interaction patterns, and conformity test pack that they prefer over established global components.
- **Hypothesis:** Three paid design-ins can be won before tooling, and model-family integration creates enough switching cost to resist vendor entry.

## Textile-Bale Yield Evidence

- **Evidence:** Separate collection increases textile supply while the EEA warns that collected quality may decline; Poland remains a material exporter and landfill user. [European Environment Agency](https://www.eea.europa.eu/en/analysis/publications/management-of-used-and-waste-textiles-in-europes-circular-economy)
- **Evidence:** The Waste Framework Directive revision introduces harmonized textile extended producer responsibility across Member States. [European Commission](https://environment.ec.europa.eu/topics/waste-and-recycling/waste-framework-directive_en)
- **Evidence/competition:** Handheld NIR already identifies fibres and blends, while industrial systems combine NIR/RGB sorting. [trinamiX](https://trinamixsensing.com/application/textile-identification/), [Fibersort](https://www.fibersort.com/en/technology)
- **Evidence/competition:** The EU-funded SORT4CIRC project has a nearly EUR 5 million budget and explicitly combines industrial collectors, sorters, recyclers, AI, multisensors, NIR, traceability, and business models. [CORDIS SORT4CIRC](https://cordis.europa.eu/project/id/101181988)
- **Evidence:** Research confirms that mechanical-process design materially changes realized yield, which supports process specificity but makes cross-customer transfer harder. [Open-access experimental study](https://www.sciencedirect.com/science/article/pii/S2666016424002433)
- **Hypothesis:** Composition plus contamination and process-specific outcomes predicts realized usable yield within eight percentage points and materially improves purchase pricing.
- **Hypothesis:** Recyclers will record/assign enough processing-outcome data and pay at least 1,500 PLN per lot decision or 50,000 PLN per site annually.

## Rejected-Direction Evidence Retained

- FuelEU permits banking, borrowing, and pooling of compliance balances. [Regulation (EU) 2023/1805](https://eur-lex.europa.eu/eli/reg/2023/1805/oj/eng), [Commission Q&A](https://transport.ec.europa.eu/transport-modes/maritime/decarbonising-maritime-transport-fueleu-maritime/questions-and-answers-regulation-eu-20231805-use-renewable-and-low-carbon-fuels-maritime-transport_en)
- From 19 July 2026, large companies face the ESPR ban on destroying unsold apparel and footwear; disclosure and remanufacturing alternatives are explicit. [European Commission](https://environment.ec.europa.eu/news/new-eu-rules-stop-destruction-unsold-clothes-and-shoes-2026-02-09_en), [Delegated Regulation](https://environment.ec.europa.eu/document/download/d211580f-c888-4f4e-848d-c10da6f03ce6_en?filename=C_2026_659_1_EN_ACT_part1_FINAL.pdf)
- Pharmaceutical and cosmetics producers must finance at least 80% of quaternary wastewater-treatment costs under the revised directive. [European Commission](https://environment.ec.europa.eu/news/new-rules-urban-wastewater-management-set-enter-force-2024-12-20_en)
- eFTI authorities are expected to accept certified-platform information from 9 July 2027, with remaining specifications still being completed. [European Commission](https://transport.ec.europa.eu/transport-themes/logistics-and-multimodal-transport/efti-regulation_en)

## Round-Two Rights and Consumables Evidence

Research date: 2026-07-13.

### LyoShield

- **Evidence:** The University of Gdańsk lists PL Pat.244159 and EP3670645, TRL4, and expressly offers a licence or sale of property rights. It reports equal or sometimes better survival than BSA-containing Reagent 18 and lower ingredient cost. [UG technology offer](https://ctt.ug.edu.pl/en/baza_ofert/reagent-for-the-preservation-of-microorganisms-in-the-lyophilisation-processodczynnik-do-ochrony-mikroorganizmow-w-procesie-liofilizacji/)
- **Evidence:** The published European application claims TSB, sucrose, and defined wheat-peptone ranges and reports tests on multiple bacterial and probiotic strains. [EPO publication](https://data.epo.org/publication-server/rest/v1.2/publication-dates/20200624/patents/EP3670645NWA1/document.pdf)
- **Evidence:** ATCC documents BSA-containing Reagent 18 as a preservation recipe. [ATCC bacteriology guide](https://www.atcc.org/resources/culture-guides/bacteriology-culture-guide)
- **Hypothesis:** An exclusive EU field licence can be optioned for no more than 20,000 PLN upfront with milestone/royalty economics.
- **Hypothesis:** Three small producers will pay for blinded CFU-retention comparisons and at least one will qualify the formulation for repeat purchase.
- **Risk:** Commercial culture producers may already use cheaper proprietary protectants; alternative plant peptones and sugars may design around the patent.

### InsulaTip

- **Evidence:** UWr's 2026 portfolio offers licence or sale of rights to P.448634 for a controlled rotating/translating probe-coating device at stated TRL6. [UWr offer portfolio](https://ctt.uwr.edu.pl/oferta/), [official offer PDF](https://ctt.uwr.edu.pl/wp-content/uploads/sites/8/2026/03/9_Urzadzenie-do-pokrywania-ostrza-mikroskopu.pdf)
- **Evidence:** EC-STM requires a coated probe with only the apex exposed. [Bruker EC-STM](https://www.bruker.com/es/products-and-solutions/microscopes/materials-afm/afm-modes/ec-stm.html)
- **Evidence:** The inventors' published automated coater tests found meaningful operator variability in manual methods; across 60 tips, 30% achieved leakage below ±10 pA and 10% exceeded ±100 pA, showing both need and incomplete yield. [Automated tip-coater paper](https://www.mdpi.com/2571-9637/7/4/65)
- **Evidence/competition:** Bruker and other vendors sell ordinary STM probes, while labs have long used wax, varnish, electropaint, and other insulation methods. [Bruker probes](https://www.brukerafmprobes.com/c-202-tungsten.aspx), [Chemical Reviews operando probe review](https://doi.org/10.1021/acs.chemrev.2c00766)
- **Hypothesis:** Ten EU EC-STM laboratories will pay €800–2,000 for qualified evaluation packs and reorder at least twice yearly.
- **Risk:** The addressable lab count and consumable frequency may be too small; laboratories can coat tips themselves or use non-infringing methods.

### Wantlist Reissue

- **Evidence:** Discogs exposes historical sales and wantlists, which can identify scarcity and transaction prices before rights are acquired. [Discogs sales history](https://support.discogs.com/hc/en-us/articles/360007425553-Where-Can-I-Access-Sales-History), [Discogs wantlists](https://support.discogs.com/hc/en-us/articles/360007331594-How-Does-The-Wantlist-Feature-Work)
- **Evidence:** ZPAV reports Polish vinyl revenue of 72.1 million PLN in 2025, up 13.5%. [ZPAV 2025 market release](https://zpav.pl/aktualnosc.php?idaktualnosci=2181)
- **Evidence:** A current Polish manufacturer quote is €1,779 before VAT and shipping for 500 classic-pack records. [Kuro Neko manufacturing offer](https://www.kuroneko-manufacture.com/offers)
- **Hypothesis:** A rights holder will sign a 12-month/500-copy exclusive option for 3,000–8,000 PLN plus royalty and permit refundable preorders before exercise.
- **Hypothesis:** 250 paid preorders at 149–169 PLN predict a sold-out 500-copy run with 50–65 PLN contribution per unit.
- **Risk:** Wantlists may reflect original-pressing collectibility rather than repress demand; rights/title clearance can fail and adjacent labels can option other titles.

### ShiftRoster Buyout

- **Evidence:** Apple supports transfer of eligible apps while retaining availability, ratings, and reviews; Google transfers users, statistics, ratings, reviews, and subscriptions subject to its process. [Apple app transfer](https://developer.apple.com/help/app-store-connect/transfer-an-app/overview-of-app-transfer/), [Google Play transfer](https://support.google.com/googleplay/android-developer/answer/6230247?hl=en-EN)
- **Evidence:** Acquire.com's 2025 report documents a functioning small-software acquisition market, but individual listing economics require seller evidence. [Acquire.com annual report](https://blog.acquire.com/wp-content/uploads/2025/02/acquire-annual-report-2025.pdf)
- **Hypothesis:** A transferable app with 20,000–30,000 PLN annual net owner earnings can be acquired for 45,000–65,000 PLN after payout, code, IP, cohort, and store-transfer diligence.
- **Hypothesis:** Polish hospital rota-PDF import and overtime/fatigue features materially lift retention or paid conversion.
- **Risk:** No specific qualifying asset has yet been identified; generic shift apps can add imports and platform discovery controls the acquired distribution.

### Decisive Competition and Blacklist Checks

- Cold-plasma seed treatment is already commercialized by firms with industrial systems, installations, services, or active field trials. [Zayndu](https://zayndu.com/about/), [PETKUS Selecta](https://www.petkus-selecta.com/portfolio/cf-04-series), [Hemeris](https://hemeris.bio/), [Apolarion](https://apolarion.ch/)
- Poland already has FarmaJet's cartridge-based, low-maintenance egg printer and local customer references; global and EU suppliers cover the same small-farm-to-industrial range. [FarmaJet](https://farmajet.pl/UK/index.html), [Domino egg coding](https://www.domino-printing.com/en-gb/industries/food/egg-shell/eggs-shells-printing-coding), [European low-cost example](https://eclaculture.com/products/imprimante-a-oeufs)
- Polish construction-waste rules require source separation of ceramics for reuse/recycling, but a roof-tile pool remains an explicitly blacklisted exact-match salvage shape. [Polish Waste Act amendment](https://eli.gov.pl/api/acts/DU/2024/1834/text.html)
- White certificates require at least 10 toe/year, may combine same-type projects, must be applied for before work, and create tradable rights; the shape remains explicitly blacklisted. [Ministry overview](https://www.gov.pl/web/klimat/efektywnosc-energetyczna), [current act](https://eli.gov.pl/api/acts/DU/2024/1047/text.html), [URE explanation](https://www.ure.gov.pl/pl/urzad/informacje-ogolne/aktualnosci/9359%2CEfektywnosc-energetyczna-biale-certyfikaty-PMEF-wkrotce-traca-waznosc.html)
