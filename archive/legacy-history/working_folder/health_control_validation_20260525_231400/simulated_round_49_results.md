# Simulated Round 49 Results: LabOps Connector Succession Escrow

Date: 2026-05-25

## Candidate

LabOps Connector Succession Escrow.

## Score

- Strict simulated score: 88
- Decision: Advance to real Zero To One working-chat validation.

## Why It Passed Simulation

This candidate uses the one pattern that real Zero To One has consistently rewarded: acquisition of an already-paid continuity asset with prepaid contracts before closing.

It avoids recent fatal patterns:

- no health-data resale / patient reconsent cohort;
- no clinical-service authority;
- no patient/NFZ book transfer;
- no lumpy physical inventory;
- no distressed receivable underwriting;
- no generic dashboard/report/marketplace.

## Control Point

The acquired asset is the continuity layer already running in production:

- source code;
- deployment/update credentials;
- support inbox;
- issue history;
- customer list;
- data-processing agreements;
- seller handoff;
- assignable maintenance contracts;
- production connectors for instrument exports, HL7/FHIR/PDF/email/SFTP result flows, FASTQ/CSV/QC transfers, billing/private-portal exports, and EDF/PSG upload scripts.

The control point is custody of existing production connectors that labs already depend on before the retiring/tired vendor disappears.

## Two-Month Proof

- one signed conditional acquisition option with a tired one-person/small-team vendor;
- clean IP and contract-assignment review;
- 10-20 lab customer re-consents;
- rotated credentials and access logs;
- 25,000+ PLN prepaid maintenance/transition cash;
- one narrow compatibility/security patch completed for an existing customer;
- no net-new bespoke integrations during proof.

## Fatal Caveats

1. IP may not be clean.
   - Old scripts may be owned by labs, contractors, prior employers, or bundled with unlicensed libraries.

2. Contract assignment may fail.
   - Customers must re-consent, and some lab/vendor agreements may block transfer.

3. Health data risk is serious.
   - Genetic/health data are special-category data; processor agreements, access logging, credential rotation, and breach procedures are mandatory.

4. Regulatory boundary must stay clean.
   - If the connector interprets or clinically transforms diagnostic logic, it can drift toward medical/IVD software. Keep it to transport, mapping, uptime, audit, and format compatibility.

5. LIMS vendors are competitors.
   - The wedge is not "better LIMS"; it is continuity for abandoned production glue.

6. Bespoke work must be tightly limited.
   - Only existing-customer compatibility/security patches count during the POC.

## Sources

- EDPB GDPR Article 9: https://www.edpb.europa.eu/gdpr-articles/article-9-processing-special-categories-personal-data_en
- EU medical-device economic operators: https://health.ec.europa.eu/medical-devices-topics-interest/economic-operators_en
- Example LIMS competitors: https://www.inform-tech.pl/ , https://kotrak.com/pl/oferta/system-lims/ , https://www.softsystem.pl/en/products/
