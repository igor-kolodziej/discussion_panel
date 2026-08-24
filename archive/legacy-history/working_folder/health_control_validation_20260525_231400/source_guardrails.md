# Source Guardrails: Health / Biosignal / Rx Search

Created: 2026-05-25 Europe/Warsaw.

## Non-Negotiable Boundaries

- Do not validate any business that directly sells, resells, brokers, forwards, or advertises prescription medicines to the public unless a licensed pharmacy/medical entity is the seller/provider of record and the workflow is lawful.
- Treat GLP-1s, opioids, benzodiazepines, stimulants, medical cannabis, and other high-risk prescription categories as compliance/clinic/pharmacy/payment-risk domains, not consumer marketplace domains.
- Do not build dosing, prescribing, diagnosis, adverse-event triage, or treatment software unless the medical-device / clinical governance boundary is explicit and handled by licensed professionals.
- Treat health data as GDPR special-category data. Data reuse, patient outreach, and re-consent ideas must prove lawful basis, controller/processor structure, and buyer trust before scoring above the gate.

## Sources Used

- GIF online medicines sale: https://www.gov.pl/web/chief-pharmaceutical-inspectorate/online-medicines-sale
- GIF safe purchase guidance: https://www.gov.pl/web/chief-pharmaceutical-inspectorate/safe-medicine-safe-purchase
- Ministry of Health pharmaceutical trade: https://www.gov.pl/web/zdrowie/obrot-produktami-leczniczymi1
- GIF medicinal product advertising: https://www.gov.pl/web/chief-pharmaceutical-inspectorate/medicinal-product-advertising
- EMA/HMA illegal medicines warning, including GLP-1: https://www.ema.europa.eu/en/news/warning-about-sharp-rise-illegal-medicines-sold-eu
- EMA falsified medicines reporting obligations: https://www.ema.europa.eu/en/human-regulatory-overview/post-authorisation/compliance-post-authorisation/falsified-medicines-reporting-obligations
- EDPB GDPR Article 9 special categories: https://www.edpb.europa.eu/gdpr-articles/article-9-processing-special-categories-personal-data_en
- MDCG 2019-11 software qualification/classification guidance: https://health.ec.europa.eu/system/files/2020-09/md_mdcg_2019_11_guidance_qualification_classification_software_en_0.pdf
- EU Data Act Regulation 2023/2854: https://eur-lex.europa.eu/eli/reg/2023/2854/oj
- EU AI Act Regulation 2024/1689: https://eur-lex.europa.eu/eli/reg/2024/1689/
- European Health Data Space reuse page: https://health.ec.europa.eu/ehealth-digital-health-and-care/reuse-health-data_en
- Polish Patient Rights Ombudsman on medical-record retention after closure/death: https://www.gov.pl/web/rpp/dostep-do-dokumentacji-medycznej-likwidacja-placowki-medycznej-smierc-lekarza-czas-przechowywania
- EU medical-device sector/economic-operator context: https://health.ec.europa.eu/medical-devices-sector_en
- EU medical-device economic operators: https://health.ec.europa.eu/medical-devices-topics-interest/economic-operators_en

## Prior Local Failures That Constrain This Run

- SleepVault HDAB archive mandates passed simulated scoring at 91 but failed real working-chat at 74 because lab mandates did not equal a legally usable commercial data asset, buyer prepayment before legal clearance was unproven, and medtech trust/CAC was weak.
- ImplantKey / orphan dental implant bank passed simulated at 89 but failed real working-chat at 76 because MDR traceability, clinical trust, compatibility liability, single-use device status, and lumpy demand capped the business.
- NeuroDevice Acceptance Escrow previously scored 76 in the health-biosignal run because used-device escrow was episodic and bypassable by sellers/buyers or existing resellers/biomed firms.
- SeedLot DNA Claim Rail previously scored 78 because claim/sample control was case-level and seed labs/lawyers/agronomists/insurers could copy unless pre-dispute routing became standard.
- KSeF/e-Delivery Accounting Book Succession Lockbox passed simulated at 88 but failed real working-chat at 74 because it collapsed into labor-heavy accounting services with liability and weak part-time founder fit.
- SpecialWork Archive Rights Rail previously scored 76/62 because official routes and regulated copy fees weakened pricing/control, GDPR constrained proactive indexing, and ZUS outcome proof was slow.

