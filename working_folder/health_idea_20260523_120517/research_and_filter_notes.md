# Research And Filter Notes

## Sources Checked

- EEG-GRAF price list: sleep-deprived adult EEG 400 PLN; child sleep EEG 800 PLN until 23:00; failed child sleep prep can still incur a 400 PLN charge. https://eeg.med.pl/prices-of-eeg/
- Neurosfera Warsaw home child sleep EEG: 750 PLN within 30 km, with stated consequences if the child does not sleep and additional repeat cost. https://www.centrum-neurosfera.pl/badanie-eeg-we-snie-w-domu-w-ciagu-dnia-dzieci/
- Royal Children's Hospital sleep-deprived EEG instructions: child sleep timing, no naps between waking and test, transport warning, seizure caveat. https://www.rch.org.au/neurology/professionals/instructions_for_eeg_sleep_deprivation/
- Boston Children's Hospital EEG prep: EEG preparation is important; children are sleep deprived to obtain awake/drowsy/asleep readings. https://www.childrenshospital.org/conditions-treatments/electroencephalograms
- ACNS pediatric EEG guideline: sleep recordings should be obtained whenever possible; natural sleep preferred; sleep deprivation or melatonin may help; careful notation/observation matters. https://www.acns.org/UserFiles/file/EEGGuideline5Ped.pdf
- PubMed abstract, feasibility of sleep-deprived EEG in children: in one 261-child retrospective review, 14% slept less than 15 min and 7% had no sleep during recording. https://pubmed.ncbi.nlm.nih.gov/26774459/
- Polish Ministry of Health IVF program source. https://www.gov.pl/web/zdrowie/in-vitro
- Polish Ministry of Health BRCA-dependent cancer molecular testing change from July 2025. https://www.gov.pl/web/zdrowie/wazna-zmiana-dla-pacjentow-onkologicznych
- GUS older people in Poland 2024. https://stat.gov.pl/obszary-tematyczne/osoby-starsze/osoby-starsze/sytuacja-osob-starszych-w-polsce-w-2024-r-%2C2%2C7.html
- OECD Poland 2025 healthcare/long-term care context. https://www.oecd.org/en/publications/oecd-economic-surveys-poland-2025_483d3bb9-en/full-report/towards-better-healthcare_debd3cc4.html
- Polish patient.gov long-term home nursing care. https://pacjent.gov.pl/artykul/pielegniarska-domowa-opieka-dlugoterminowa

## Subagent Integration

Elderly-care strongest:

- CareProof Rail for private elderly-care homes: pre-score 88. Good live workflow control point, but buyer urgency before a complaint is uncertain.
- 14-Day Senior Discharge Bridge: pre-score 86. Strong crisis demand and cash conversion, but service-heavy and operationally messy.

Genetics strongest:

- IVF Carrier-Screening Consent & Routing Layer: pre-score 91. Strong demand momentum through Polish IVF program and clinic flow, but requires clinical trust and could be internalized by clinics/labs.
- BRCA-Dependent Cancer Molecular Test Routing Desk: pre-score 88. Strong July 2025 policy momentum, but medical trust and clinic access are heavier.

EEG strongest:

- Pediatric Sleep-EEG Success Layer / Fill-Rate Rail: pre-score 86 locally and externally. Best founder fit and strongest 2-month bootstrap; needs stronger value capture than simple reminders.
- Trial-Ready Epilepsy Patient Packets: pre-score 89. Highest upside, but CRO/site sales and GDPR/trust are likely slower than 2 months.

## Finalists For Simulated Gate

1. Pediatric Sleep-EEG Fill-Rate Rail.
2. IVF Carrier-Screening Consent & Routing Layer.
3. CareProof Rail For Private Elderly-Care Homes.
4. Trial-Ready Epilepsy Patient Packets.
5. BRCA-Dependent Cancer Molecular Test Routing Desk.
6. 14-Day Senior Discharge Bridge.

## Current Lean

The strongest practical candidate may be Pediatric Sleep-EEG Fill-Rate Rail if sharpened from "prep reminders" into a paid, routed slot-yield workflow with:

- lab-mandated routing of every child sleep/sleep-deprived booking;
- parent readiness scoring 48h and 12h before the exam;
- active rescue calls for high-risk prep failures;
- owned standby list of prepared families for cancellations;
- payment tied to completed interpretable sleep/sleep-deprived slots or recovered slot value;
- 2-month proof from one signed lab, 30-50 routed bookings, and lower failed/no-show/late-cancel rates.

The strongest genetics candidate is IVF Carrier-Screening Consent & Routing Layer, but the control point is a clinic intake workflow and requires a geneticist reviewer plus clinic trust. It may score well on momentum but could fail the "unknown founder can secure this" gate.
