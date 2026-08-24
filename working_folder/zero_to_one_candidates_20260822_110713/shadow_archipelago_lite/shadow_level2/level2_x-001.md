# Level-2 X-001 — Installation-Day Readiness Preflight

## Problem And Payer Evidence

Renewable installations require coordination of connection prerequisites, designs, permits, equipment, qualified personnel, customer access, safety conditions, and post-installation documents. Poland’s national contact point exposes separate grid-connection procedures and application routes, while URE has expressly reminded applicants that renewable connection applications require documents supporting the proposed location, such as planning documentation or a development-conditions decision. [Polish grid-connection procedures](https://www.gov.pl/web/national-contact-point-for-renewable-energy-sources/grid-connection-procedures) [URE formal-requirement notice](https://www.ure.gov.pl/pl/urzad/informacje-ogolne/aktualnosci/11030%2CPrezes-URE-przypomina-o-wymaganiach-formalnych-dotyczacych-wnioskow-o-wydanie-wa.html)

Operational prerequisites extend beyond permits. Government installation guidance identifies prior site visits, equipment matching, accredited personnel, switchboard and roof access, weather, customer presence, Wi-Fi access, commissioning, and retained documentation as factors affecting installation and activation. This is not Polish failure-incidence evidence, but it verifies that a readiness check has multiple independently failing inputs. [Australian government installation guidance](https://www.energy.gov.au/solar/solar-retailers-and-installation/installation-day-and-after)

A U.S. installer survey reported an average of roughly 16 weeks from contract to operation and identified permitting, inspection, and interconnection as important delay drivers. Geography limits transfer to Poland, and those authority-controlled delays may not be correctable 48–72 hours before dispatch. [Installer-delay study](https://www.sciencedirect.com/science/article/pii/S0301421521002913)

The direct payer is a renewable installer’s operations manager, dispatcher, installation director, or owner. A plausible initial payer handles 20–500 installations per year and bears the cost of idle crews, second visits, customer rescheduling, and incomplete closeout. Poland had 1,636,673 connected renewable microinstallations at the end of 2025, 99.9% photovoltaic, but that installed base is not an annual job count and does not reveal the number of installer companies or paying operations teams. The reachable payer denominator is therefore unknown. [URE microinstallation report](https://www.ure.gov.pl/pl/urzad/informacje-ogolne/aktualnosci/13173%2CRaport-URE-w-Polsce-mamy-juz-ponad-16-mln-mikroinstalacji-OZE.html)

The closest substitutes are dispatcher calls, project-management checklists, spreadsheets, CRM stages, calendar buffers, warehouse picking lists, electrician sign-off, and a pre-installation site visit. The incumbent route-around is to add administrative staff, hold more buffer inventory, schedule conservatively, or use an existing field-service platform. Those approaches persist because readiness rules are installer-specific and experienced staff can resolve ambiguous cases through calls.

A willingness proxy exists in adjacent solar workflow software: Solo publishes per-proposal pricing of $17–$32 depending on volume. This verifies that solar firms can buy a project-priced managed workflow, but not that a Polish installer will pay the same amount for readiness preflight. [Solo pricing](https://gosolo.io/pricing-old-3/)

## Proposed Transaction

The paid event is a scheduled installation that receives a completed, configurable readiness review 48–72 hours before dispatch. The result should be “ready,” “conditional,” or “not ready,” with evidence, owner, corrective action, and deadline for every exception. A “ready” result is not a warranty that weather, authorities, customers, equipment, or site conditions will cooperate.

A plausible range is:

- Small residential or microinstallation job: 40–120 PLN per completed preflight.
- Larger residential-plus-storage or small commercial job: 150–500 PLN.
- Complex commercial project: 500–1,500 PLN where the customer supplies an agreed checklist and evidence map.
- Volume bundle: approximately 1,000–4,000 PLN monthly for a limited number of scheduled reviews, with overages priced per project.

These are interpreted ranges. A nearby managed solar deliverable costs $17–$32 per proposal, but a readiness service’s value depends on avoided dispatch or revisit cost, which remains unknown.

The first version should ingest exports or a shared project folder rather than changing schedules. Required fields can include project identifier, address, installation type, approved design, required permits or notifications, grid status, crew qualifications, equipment reservation and serials, access confirmation, roof/electrical prerequisites, special lifting or safety needs, customer contact confirmation, forecast conditions, and unresolved changes.

Exact access requires written installer authorization; a data-processing agreement covering customer names, addresses, contact details, and project records; least-privileged access to the specified project folder or export; documented retention and deletion; and a prohibition on contacting customers, changing schedules, or representing regulatory approval unless separately authorized. Whether the installer is controller and the service provider processor in each workflow, and whether subcontractors may access project data, is counsel-required.

A private historical proof can fit within roughly 10,000–30,000 PLN. A shadow pilot including secure document ingestion, rule configuration, contractor labeling, and eight weeks of observation could require 25,000–60,000 PLN. Live integrations or business-hours intervention could exhaust the full 100,000 PLN budget before causality is demonstrated.

The decisive sensitivity is the avoidable share. At least 15% of delayed or revisited jobs must contain a non-weather exception that was evidenced 48–72 hours before dispatch and could still have been corrected or rescheduled. If historical data show 100 delayed or revisited jobs, at least 15 must satisfy all parts of that definition—not merely have incomplete documents discovered afterward.

## Acquisition Route

The first customer should be a local renewable installer or electrical-design contractor able to provide historical failed, delayed, or revisited jobs and the files that existed before dispatch. The sequence is:

1. Define “delay,” “failed visit,” “revisit,” “non-weather,” “evidenced,” and “actionable.”
2. Label historical outcomes without exposing the model to post-event documents during the initial test.
3. Reconstruct the information available exactly 72 and 48 hours before dispatch.
4. Have an experienced dispatcher judge whether each detected exception was actionable.
5. Shadow future jobs for eight weeks without automatically changing schedules.
6. Compare flagged jobs with actual outcomes, corrective actions, false alarms, and missed exceptions.

The cheapest falsification uses perhaps 30–100 historical problem jobs plus a matched sample of successful jobs. It requires only customer-authorized files and staff adjudication. If fewer than 15% of problem jobs have early, actionable non-weather evidence—or if false alarms overwhelm dispatchers—the core premise fails before integration.

The first route can be mediated by an electrical-design contractor that already receives designs, grid documents, and equipment requirements from multiple installers. However, that contractor may lack crew, warehouse, customer-access, and dispatch data, making file sufficiency an explicit test.

A compounding asset could be a permissioned library connecting installation type, jurisdiction, readiness rule, exception, action, lead time, and first-visit outcome. Customer-specific schedules and identifiable household data should not become shared training material.

## Decision-Critical Unknowns

- **Verified:** Installation readiness spans documents, connection prerequisites, equipment, personnel, access, safety, commissioning, and customer coordination.
- **Verified:** Formal connection documentation is required in Poland.
- **Verified:** Readiness checklists are an established procurement mechanism; a U.S. Department of Energy contract, for example, requires a construction/installation readiness checklist before work, including schedule risks and equipment lists. [DOE checklist](https://www.energy.gov/nnsa/articles/attachment-2reporting-requirements-checklist-rev-05152023)
- **Interpreted:** Installers completing 20–500 jobs annually are a plausible initial payer segment.
- **Unknown:** The number of reachable Polish installers in that segment.
- **Unknown:** Local delayed-installation, failed-visit, and revisit prevalence.
- **Unknown:** Whether at least 15% of problem jobs contain actionable, non-weather evidence 48–72 hours before dispatch.
- **Unknown:** Whether historical folders preserve the documents and timestamps needed to avoid hindsight leakage.
- **Unknown:** Installer willingness to pay the proposed per-project amount.
- **Unknown:** The cost of an avoidable failed dispatch or revisit and thus the maximum rational price.
- **Unknown:** False-positive tolerance among dispatchers and crew managers.
- **Unknown:** Reduction achievable during live use rather than retrospective labeling.
- **Unknown:** Whether useful operation requires CRM, warehouse, scheduling, weather, or grid-system integrations.
- **Unknown:** Whether exceptions require business-hours intervention incompatible with part-time operation.
- **Contradicted:** A readiness pass cannot control continuous rain, unsafe roofs, late authority decisions, grid constraints, customer emergencies, or new site conditions.
- **Contradicted:** Poland’s installed microinstallation count is not a payer denominator or annual installation volume.
- **Counsel-required:** Personal-data roles, subcontractor access, customer-contact authority, regulatory representations, and liability language around a readiness “pass.”

## Evidence And Sources

Dated direct-URL ledger:

- 2026-08-22 accessed — Polish national grid-connection procedure index: [https://www.gov.pl/web/national-contact-point-for-renewable-energy-sources/grid-connection-procedures](https://www.gov.pl/web/national-contact-point-for-renewable-energy-sources/grid-connection-procedures)
- 2023-04-12 published, 2024-02-21 modified, 2026-08-22 accessed — URE formal-document requirements: [https://www.ure.gov.pl/pl/urzad/informacje-ogolne/aktualnosci/11030%2CPrezes-URE-przypomina-o-wymaganiach-formalnych-dotyczacych-wnioskow-o-wydanie-wa.html](https://www.ure.gov.pl/pl/urzad/informacje-ogolne/aktualnosci/11030%2CPrezes-URE-przypomina-o-wymaganiach-formalnych-dotyczacych-wnioskow-o-wydanie-wa.html)
- 2026-08-22 accessed — Australian government installation-day dependencies and counterevidence: [https://www.energy.gov.au/solar/solar-retailers-and-installation/installation-day-and-after](https://www.energy.gov.au/solar/solar-retailers-and-installation/installation-day-and-after)
- 2021 published, 2026-08-22 accessed — installer survey on project delays: [https://www.sciencedirect.com/science/article/pii/S0301421521002913](https://www.sciencedirect.com/science/article/pii/S0301421521002913)
- 2026-08-22 accessed — URE’s 2025 microinstallation totals: [https://www.ure.gov.pl/pl/urzad/informacje-ogolne/aktualnosci/13173%2CRaport-URE-w-Polsce-mamy-juz-ponad-16-mln-mikroinstalacji-OZE.html](https://www.ure.gov.pl/pl/urzad/informacje-ogolne/aktualnosci/13173%2CRaport-URE-w-Polsce-mamy-juz-ponad-16-mln-mikroinstalacji-OZE.html)
- 2023 checklist revision, 2026-08-22 accessed — DOE construction/installation readiness procurement requirement: [https://www.energy.gov/nnsa/articles/attachment-2reporting-requirements-checklist-rev-05152023](https://www.energy.gov/nnsa/articles/attachment-2reporting-requirements-checklist-rev-05152023)
- 2026-08-22 accessed — adjacent per-project solar workflow pricing: [https://gosolo.io/pricing-old-3/](https://gosolo.io/pricing-old-3/)

### Query trace

1. `Poland photovoltaic installation grid connection required documents official installer`
2. `Poland renewable installation permit documentation delays official report`
3. `solar installation project delays missing materials crew access survey`
4. `solar installer pre installation checklist official`
5. `site:gov.uk solar installation checklist installer site readiness`
6. `site:energy.gov solar permitting inspection delays soft costs`
7. `site:seia.org solar installation delays permitting interconnection workforce`
8. `site:nrel.gov residential solar installation delays permitting interconnection`
9. `solar installation scheduling software pricing per project`
10. `renewable installer rework first time fix rate solar`
11. `electrical contractor pre construction readiness checklist materials permits crew`
12. `Poland solar installer market number companies official 2025`

