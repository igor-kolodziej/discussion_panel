# Research and Sources

Research date: 2026-07-14. Evidence, hypotheses, founder assumptions, and reviewer verdicts are kept separate. No prospect, clinic, manufacturer, researcher, or partner was contacted.

## Evidence

### Regulation, buyer discovery, and local momentum

- [EU Medical Device Regulation 2017/745](https://eur-lex.europa.eu/legal-content/ENG/ALL/?uri=CELEX%3A32017R0745) requires programmable medical devices to address repeatability, reliability, performance, verification, and validation. This supports engineering-test demand; it does not prove demand for any particular vendor.
- [AI Act Article 15](https://eur-lex.europa.eu/legal-content/en/TXT/?uri=CELEX%3A32024R1689) requires appropriate accuracy, robustness, and cybersecurity through the lifecycle and recognizes benchmarks and measurement methods. Enforcement timing is not treated as the paid event.
- [European Commission EUDAMED overview](https://health.ec.europa.eu/medical-devices-eudamed/overview_en) states that actor, device, and certificate modules became mandatory on 28 May 2026. Public records can support target-account research without privileged introductions.
- [POLMED](https://polmed.org.pl/izba-polmed-wybrala-nowe-wladze-na-kadencje-2026-2029/) reports 133 member medical-device companies; [PARP's Polish medical-device catalogue](https://www.parp.gov.pl/component/publications/publication/the-medical-devices-and-pharma-sector-in-poland) is another local discovery source.
- [UDT's certified OZE installer register](https://www.udt.gov.pl/wykazy/rejestr-certyfikowanych-instalatorow-oze.html) creates a direct acquisition list. [URE](https://www.ure.gov.pl/en/communication/news/518%2CURE-report-The-number-of-RES-micro-installations-in-Poland-has-already-exceeded-.html) reports more than 1.6 million Polish RES micro-installations at end-2025, 99.9% PV.
- [UDT](https://www.udt.gov.pl/aktualnosci/zadbaj-o-bezpieczenstwo-oraz-jakosc-przy-instalowaniu-paneli-fotowoltaicznych-i-pomp-ciepla) warns that installation quality affects performance, safety, and warranty and maintains a public installer base.
- [PARP](https://www.parp.gov.pl/component/content/article/90648%3Apolska-stawia-na-robotyzacje-firmy-ze-wschodu-korzystaja-z-dotacji) reports more than 1.345 billion PLN of Polish robotization investment in 2022–2024; [FAIRP](https://fairp.pl/lista-czlonkow/) publishes a member directory of robot integrators and suppliers.
- The [Polish tax portal](https://www.podatki.gov.pl/ulgi-i-odliczenia/ulga-na-robotyzacje-cit) documents a robotization tax relief allowing an additional 50% qualifying-cost deduction through the tax year beginning in 2026.

### Signal-chain and wearable reliability

- A [BMJ Health & Care Informatics study](https://informatics.bmj.com/content/26/1/e100083) found that 32% of wearable update items examined could affect earlier validation, and updates sometimes occurred days apart.
- A [wearable data-quality review](https://pmc.ncbi.nlm.nih.gov/articles/PMC8294465/) identifies undocumented algorithm changes, inconsistent variable definitions, packet loss, and non-random missingness as material risks.
- [BLE packet-loss research](https://pmc.ncbi.nlm.nih.gov/articles/PMC8533907/) documents real packet-loss behavior relevant to end-to-end validation.
- Current prototype inputs are affordable: [Movesense](https://www.movesense.com/shop/) offers a raw ECG/IMU developer kit around EUR 399; [Shimmer](https://www.shimmersensing.com/shop/) lists biosignal kits around EUR 723–799; [OpenBCI](https://shop.openbci.com/products/cyton-biosensing-board-8-channel) lists Cyton at USD 1,249.
- [WhaleTeq AECG100](https://www.whaleteq.com/en/product/4/16-health-wearables-testing/view21-aecg100) already provides ECG/PPG simulation and fixtures. Therefore SignalChain Sentinel cannot be merely a signal generator; its wedge must be full physical-device-to-cloud release regression, cross-vendor adapters, and change history.

### Dry EEG and fit mechanics

- A [2025 3D-printed EEG phantom paper](https://pubmed.ncbi.nlm.nih.gov/40871838/) reports a low-cost conductive phantom, supporting prototype feasibility.
- Research on [dry-electrode geometry](https://pmc.ncbi.nlm.nih.gov/articles/PMC13265750/), [flower electrodes](https://pmc.ncbi.nlm.nih.gov/articles/PMC10547758/), and [wearable EEG artifacts](https://pmc.ncbi.nlm.nih.gov/articles/PMC12473706/) links geometry, pressure, curvature, hair, and motion to contact quality and comfort.
- [Fraunhofer PhantomHead](https://www.idmt.fraunhofer.de/en/institute/projects-products/projects/phantomhead.html) explicitly addresses the lack of known EEG ground truth and objective performance comparison. It validates the problem and is a serious competition/IP warning.
- [Brain Products LabSim](https://www.brainproducts.com/solutions/labsim/) simulates EEG signals through a full signal chain. DryEEG FitGrid therefore must remain focused on contact mechanics, anthropometry, hair, pressure, and repeated donning rather than generic amplifier testing.
- A [mobile phantom-head paper](https://pubmed.ncbi.nlm.nih.gov/27137818/) and a [motion-artifact phantom paper](https://pubmed.ncbi.nlm.nih.gov/32746290/) demonstrate physical motion/phantom approaches relevant to artifact testing.

### Human augmentation and skilled work

- Existing spray-training products include [SimSpray](https://simspray.net/simspray/), [VR Paint](https://vr-paint.com/), and [E-CO Painter](https://en.brtech.kr/e-co-painter). They validate training demand but force SprayPilot to own a real-production, actual-defect feedback loop rather than an offline simulator.
- A [2025 Nature paper](https://www.nature.com/articles/s41586-025-09255-w) demonstrates general non-invasive wrist sEMG; [Meta](https://about.fb.com/news/2025/09/meta-ray-ban-display-ai-glasses-emg-wristband/) reports a commercial EMG wristband trained on a very large participant base. This is technical validation and a strong reason not to pursue a generic neural-command interface.
- The [EU Machinery Regulation 2023/1230](https://eur-lex.europa.eu/eli/reg/2023/1230/en) applies from 20 January 2027 and addresses operator workload, HMI adaptation, autonomous behavior, intervention records, and safety software. It is context, not proof that a compliance product will be bought.
- [EU-OSHA](https://healthy-workplaces.osha.europa.eu/en/publications/smart-digital-systems-better-safety-and-health-work) reports workplace wearable use but emphasizes participation, transparent data use, and privacy. Finalists avoid emotion inference and individual productivity ranking.
- [UODO workplace guidance](https://uodo.gov.pl/pl/file/4933) emphasizes power imbalance, purpose limitation, proportionality, and DPIAs. Any human-sensing pilot must minimize raw data and obtain an appropriate legal basis.

### Robot skill data

- [LeRobot dataset guidance](https://huggingface.co/blog/lerobot-datasets) and its [real-world workflow](https://huggingface.co/docs/lerobot/main/en/getting_started_real_world_robot) document the capture effort and recurring data-quality/metadata failures in robot-learning datasets.
- [Kaiwu](https://arxiv.org/abs/2503.05231) demonstrates synchronized multimodal assembly capture including gaze, EMG, pressure, motion, audio, and video. This supports technical value but not transferability or buyer willingness to pay.

## Commercial hypotheses to test

- A wearable product-line owner will pay 15,000–35,000 PLN for initial SignalChain Sentinel integration and 40,000–100,000 PLN annually for monitored regression. No source proves these prices.
- A dry-EEG developer will pay 12,000–25,000 PLN for a fit/electrode comparison before a human study and later 35,000–60,000 PLN for a calibrated kit. No buyer evidence exists yet.
- A small coating shop will pay 8,000–15,000 PLN for a shadow-mode trial and later 4,500–7,000 PLN per month when technique guidance reduces rework/material use by at least 1.5 times the fee. The relationship between motion telemetry and defects is unproven.
- An installer will pay 8,000–15,000 PLN for a 10-job commissioning pilot and then about 200–260 PLN per completed asset passport if callbacks, evidentiary work, and warranty friction fall enough. No paid evidence exists.
- Cross-customer benchmark or derivative-data clauses will be commercially acceptable. Every finalist must make that acceptance a kill test, not an assumption.

## Founder assumptions

- The founder can allocate roughly five hours per day while employed and can use the family renewable-energy business only as a non-paying testbed, never as independent paid proof.
- Public lists and technical demonstrations can reach owner-led SMEs and product engineers without status or warm introductions.
- Contractors can cover mechanical/electronics work while the founder owns customer discovery, product scope, data design, and economics.

## Reviewer verdicts

None. Candidate generation does not score or validate ideas. Advisory evaluations, simulated judges, and real chatbot verdicts will be recorded separately and must never be treated as market evidence.
