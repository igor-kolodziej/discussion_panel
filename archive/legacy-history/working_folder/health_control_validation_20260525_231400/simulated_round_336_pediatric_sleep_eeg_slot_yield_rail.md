# Simulated Round 336: Pediatric Sleep-EEG Slot Yield Rail

Date: 2026-05-31 Europe/Warsaw

## Gate In Force

- Simulated score must be strictly above 87 before real validation.
- Real working-chat Zero To One gate: >=85.
- Real fresh-chat Zero To One gate: >=85.
- Zero To One prompts must not include internal scoring caps, evaluator instructions, working-chat language, fresh-chat language, or gate language.

## Why This Branch Despite The Health Boundary

The recent non-health branches have repeatedly failed because they were service-heavy evidence desks, recovery mandates where incumbents own the workflow, assumed micro-acquisitions, or physical lots where expert incumbents own supply. This round tests a different hard-control shape: a provider-routed capacity/yield rail where the startup controls a real operational queue and first proof is paid routed cases plus recovered slot value.

This is EEG/medical-workflow-adjacent, so the safety boundary is explicit:

- the lab remains medical provider and data controller;
- licensed EEG technicians perform recordings;
- licensed/qualified physicians or EEG specialists interpret reports;
- lab-approved instructions control all patient/parent communication;
- the startup does not diagnose, interpret EEG, recommend treatment, change sleep-deprivation instructions, handle raw EEG, or provide medical advice;
- the startup signs DPA/processor terms with the lab and processes only scheduling/readiness data needed for the workflow.

The candidate is allowed through simulation only because the hard control point is unusually concrete: a signed lab pilot that makes parent routing mandatory for named pediatric sleep/sleep-deprived EEG bookings, plus a founder-owned standby family list for recovered slots.

## Source Check

This round used current public checks only to validate that the operational substrate is real:

- EEG-GRAF publishes child sleep EEG pricing with extra fees for late hours and an unsuccessful-exam charge when the child does not sleep or the patient resigns on site.
- Klinika Neuron publishes private home sleep/deprivation EEG pricing for children and longer home EEG formats.
- A 261-child sleep-deprived EEG feasibility study reported 37 children sleeping under 15 minutes and 19 with no sleep during recording.
- ACNS pediatric EEG technical standards discuss the value of sleep recording where possible.

These sources are not part of the validation prompt. They support the internal simulation only.

## Raw Candidate Control Table

| # | Candidate | Buyer | Acute trigger | Transferable control point inside 60 days | First proof | Main copy risk | Internal score |
|---:|---|---|---|---|---|---|---:|
| 1 | Pediatric Sleep-EEG Slot Yield Rail | Private EEG labs doing pediatric sleep or sleep-deprived EEG | failed sleep, late cancels, long slots lost, parent prep errors | signed lab pilot, mandatory routed booking flow, lab-approved prep, standby list, paid routed cases | 30-50 bookings routed, 10+ paid cases, recovered slots/no-shows reduced | labs can send reminders; clinic software | 89.2 |
| 2 | Home EEG Capacity Router | parents/neurologists/small clinics | fast home EEG slot needed before neurology decision | reserved technician and interpretation slots | prepaid appointments | medical provider/trust risk | 86.5 |
| 3 | Pediatric MRI sedation-readiness yield rail | imaging centers | failed pediatric MRI slots | routed prep/standby list | fewer failed slots | hospital protocols/clinical risk | 80 |
| 4 | Pediatric sleep-study prep yield rail | sleep labs | failed sleep study nights | routed parent prep | successful studies | sleep labs/clinicians | 82 |
| 5 | Dental pediatric anesthesia no-show rail | dental clinics | missed sedation slots | parent prep/standby | filled slots | medical/anesthesia risk | 72 |
| 6 | IVF genetic add-on consent routing | IVF clinics | optional carrier screening creates counseling burden | clinic-routed workflow and reviewer slot | paid cycle flow | geneticists/labs | 83 |
| 7 | Care-home family complaint event rail | private care homes | complaint/bad review/inspection stress | mandatory high-risk event routing | paid home pilots | CRMs/nurse auditors | 84 |
| 8 | Dialysis transport no-show yield rail | dialysis centers | missed transport slots | transport confirmation workflow | reduced no-shows | providers already own | 73 |
| 9 | Physiotherapy post-op appointment yield rail | rehab clinics | missed post-op slots | reminder/standby list | filled visits | simple admin | 65 |
| 10 | Pediatric allergy challenge readiness rail | allergy clinics | failed challenge appointment | prep confirmation | completed visits | clinical protocol risk | 70 |
| 11 | Endoscopy prep completion rail | GI clinics | failed bowel prep cancellations | prep calls/checklist | completed scopes | clinical risk/providers own | 75 |
| 12 | Private ADHD assessment document-readiness rail | psych clinics | missing school/parent forms delay visit | routed forms | completed assessments | clinics can internalize | 71 |
| 13 | Speech therapy evaluation readiness rail | therapy centers | no-shows/missing documents | parent routing | completed evals | simple admin | 63 |
| 14 | Autism diagnostic packet readiness rail | psych clinics | missing school/development evidence | form routing | completed visits | clinical/private data | 68 |
| 15 | Home sleep apnea test yield rail | sleep clinics | device not returned / bad signal | readiness/return workflow | usable tests | clinics/device firms | 70 |
| 16 | Ambulatory ECG Holter return-yield rail | cardiology clinics | devices returned late or diary missing | return confirmation | usable returns | simple reminders | 62 |
| 17 | 24h BP monitor return-yield rail | clinics | devices lost/late | reminders/deposits | returns | commodity | 55 |
| 18 | Private lab fasting-test readiness rail | labs | wrong fasting/med timing | reminders | fewer redraws | labs own | 48 |
| 19 | Occupational medicine document-readiness rail | clinics/employers | missing referrals/forms | employer routing | completed visits | admin commodity | 60 |
| 20 | Veterinary MRI/anesthesia readiness rail | vet clinics | pet prep failures | owner prep/standby | completed cases | vet clinics | 67 |
| 21 | Sports performance test yield rail | sports labs | no-shows/prep errors | athlete prep | completed tests | small/low urgency | 50 |
| 22 | Driving-school medical exam readiness rail | clinics | missing documents | routing | completed exams | commodity | 44 |
| 23 | Private vaccination cohort no-show rail | clinics | appointment no-shows | reminders/standby | completed shots | low value | 42 |
| 24 | Clinical-trial visit evidence routing | sites/CROs | missing visit docs blocks payment | site packet | invoice release | prior trialpay failed/trust | 74 |
| 25 | EEG lab cancellation marketplace | EEG labs/patients | last-minute vacancies | standby waitlist | filled slot | marketplace risk | 64 |
| 26 | EEG technician slot bank for clinics | clinics | technician absence/backlog | technician availability reservation | completed tests | provider supply/trust | 84 |
| 27 | EEG report-turnaround queue for neurologists | labs | delayed interpretations | reserved reader slots | report time | physician credential risk | 82 |
| 28 | Pediatric neurodiagnostic intake standard | neuro clinics | scattered parent history | intake forms | accepted histories | forms/software | 66 |
| 29 | EEG artifact-quality prep rail for adult home EEG | home EEG providers | bad signal/hair prep | prep workflow | fewer repeats | provider-owned | 72 |
| 30 | School absence documentation rail for chronic illness | parents/schools | documents missing | admin workflow | accepted docs | legal/privacy | 50 |
| 31 | Dental aligner scan no-show yield rail | dental/ortho clinics | missed scans | reminder/standby | filled slots | clinics/software | 54 |
| 32 | Ophthalmology pediatric dilation readiness rail | eye clinics | child prep/no-show | parent workflow | completed exams | low value | 55 |
| 33 | Dermatology patch-test return rail | clinics | patients miss readings | reminders | completed readings | simple | 58 |
| 34 | Audiology ABR sleep-prep yield rail | audiology clinics | child must sleep for ABR | parent prep/standby | completed tests | strong but smaller | 84 |
| 35 | Pediatric blood-draw anxiety prep rail | labs/clinics | failed draw | prep scripts | completed draws | low ticket | 51 |
| 36 | Private neurology first-visit packet rail | neurologists | missing prior records | patient prep | completed visits | secretarial | 59 |
| 37 | Imaging contrast paperwork rail | imaging centers | missing creatinine/allergy forms | admin prep | fewer reschedules | centers own | 54 |
| 38 | EEG parent transport micro-shuttle | EEG labs | late arrivals | transport coordination | on-time slots | logistics | 45 |
| 39 | Neurofeedback qEEG prep rail | neurofeedback centers | prep/no-show | reminders | completed sessions | weaker medical/consumer | 48 |
| 40 | Pediatric rehab standby-fill list | rehab clinics | cancellations | waitlist | filled slots | generic | 52 |

## Finalists

| Candidate | Reason to advance or reject |
|---|---|
| Pediatric Sleep-EEG Slot Yield Rail | Advances. It targets a narrow, measurable provider pain: valuable pediatric sleep/sleep-deprived EEG slots fail when parents mishandle preparation or cancel late. The lab controls medical care; the startup controls routed readiness workflow and standby demand. |
| Home EEG Capacity Router | Rejected for this round. Harder capacity control, but direct patient trust transfer and medical-provider structuring are more sensitive. |
| EEG technician slot bank for clinics | Close but depends on technician labor supply and provider substitution; less differentiated than sleep-yield. |
| EEG report-turnaround queue | Useful but physician credentialing/interpretation capacity is too close to medical-service provision. |
| Pediatric sleep-study prep yield rail | Similar pattern but sleep-study workflows are more clinical and often hospital-owned. |
| ABR sleep-prep yield rail | Similar and promising, but smaller first market than pediatric sleep EEG. |

## Selected Candidate

**Pediatric Sleep-EEG Slot Yield Rail**

## Internal Simulation

| Dimension | Score | Notes |
|---|---:|---|
| Acute pain | 9 | Pediatric sleep/sleep-deprived EEG uses scarce long slots; failed sleep, no-shows, late cancels, and bad prep waste paid capacity and parent goodwill. |
| Buyer specificity | 9 | Private EEG labs and neurodiagnostic clinics with pediatric sleep/deprivation EEG are identifiable through public search and price lists. |
| Control point | 9 | Signed lab pilot makes routing mandatory for named booked cases; startup controls readiness queue, escalation calls, slot-risk score, and standby list. |
| 60-day proof | 9 | One lab pilot with 30-50 routed bookings, 10+ paid routed cases, readiness completion metrics, and one filled/recovered slot is feasible if the pain exists. |
| Economics | 8 | 80-160 PLN per routed booking or 20-30% of recovered slot value can be justified by one saved 800-1,100 PLN slot; gross margin is high after playbook setup. |
| Copy risk | 6 | Labs can copy reminders; defense is parent-prep pattern memory, standby demand, cross-lab benchmarks, and founder-owned operational execution. |
| Founder fit | 9 | Warsaw data-science/neuroscience/EEG fit is unusually strong; validation can start with written outreach and simple workflow tooling. |
| Incumbent weakness | 7 | Labs provide clinical EEG, but parent yield and cancellation recovery are low-status operational work that is rarely optimized like a revenue product. |
| Boundary safety | 8 | Strict lab-provider boundary avoids diagnosis, interpretation, raw EEG handling, or medical instruction changes. |
| Durability | 8 | If the workflow becomes default for pediatric sleep EEG bookings and keeps a standby list, it can expand to home EEG, ABR, sleep studies, and pediatric neurodiagnostic yield. |

**Simulated score: 89.2 / 100.**

This clears the simulated gate strictly above 87.

## Why This Is Not A Duplicate Of Existing Confirmed Ideas

It is not BioSignal Claim-Risk Diligence Pack because it is not investor diligence, startup claim review, or a memo. It is not Supplement Stack Safety because it does not involve supplements, consumer safety, or ingredient risk. It is not DORA, REDBlocked, HeritageDoor, TraceFaktura, CBAM, Data Act, GreenTender, BatteryFit, HeatQuiet, PromoLeak, or any platform/payment recovery idea. The controlled object is lab-routed pediatric sleep/sleep-deprived EEG booking flow and standby-slot demand, not a regulatory evidence packet, scarce heritage asset, import file, machine data request, or claim recovery.

## Internal Objections To Watch In Real Validation

- The evaluator may treat it as a reminder service or clinic admin workflow.
- The buyer pool may be small if only a few private labs do meaningful pediatric sleep EEG volume.
- Labs may believe they can send SMS instructions themselves.
- Staff may resist third-party routing of parents.
- Patient data, consent, and medical-provider boundaries must be clean.
- The startup must not give medical advice, change instructions, or promise diagnostic quality.
- Measured lift may be noisy unless labs have a baseline failure/no-show rate.
- The standby list must be real; otherwise the product is only reminders.
- Retention depends on measurable reduced failed-prep/no-show/late-cancel rates or recovered slot revenue.

## Real Validation Prompt

Use:

`/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/zero_to_one_prompt_pediatric_sleep_eeg_slot_yield_rail.txt`
