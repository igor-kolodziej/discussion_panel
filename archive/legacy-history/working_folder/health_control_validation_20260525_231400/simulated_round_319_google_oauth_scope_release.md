# Simulated Round 319: Google OAuth Restricted-Scope Go-Live Release Desk

Date: 2026-05-31 Europe/Warsaw

Current real validation gates: working Zero To One >=85; fresh Zero To One >=85. Internal simulation gate: only validate if simulated score is strictly >87.

## Search Pivot

Round 318 passed working validation but failed fresh validation because the fresh evaluator saw the LC overflow idea as lumpy expert labor with unproven partner volume. Round 319 avoids another partner-overflow finance desk and tests a different hard-control surface: official platform access cases where a named customer deployment or renewal is blocked by a platform verification/admin-consent gate.

The target must not be a generic security questionnaire, appsec report, or developer-help desk. It must start only after a live Google OAuth, Workspace admin-consent, or restricted-scope verification problem is blocking a named customer go-live, renewal, procurement step, or user rollout.

## Source Notes

Official source timing/control notes used for the simulation:

- Google OAuth verification docs state that apps requesting sensitive or restricted Google API scopes must complete app verification before being granted access.
- Google's API Services User Data Policy says applications accessing sensitive/restricted scopes must demonstrate secure data handling and, depending on API and user count, may need an annual security assessment and Letter of Assessment from a Google-designated third party.
- Google restricted-scope verification docs state that restricted scopes can require a more extensive review and security assessment unless an exception applies.
- Google Workspace Admin docs show that Workspace administrators can control third-party app access and mark apps as trusted, limited, specific, or blocked.

Sources:

- `https://support.google.com/cloud/answer/13463073`
- `https://developers.google.com/terms/api-services-user-data-policy`
- `https://developers.google.com/identity/protocols/oauth2/production-readiness/restricted-scope-verification`
- `https://support.google.com/a/answer/7281227`

## Raw Candidate Control Table

| # | Candidate | Buyer/payor | Acute trigger | Transferable control point inside 60 days | First acquisition mechanism | Economics | Copy risk / cap |
|---:|---|---|---|---|---|---|---|
| 1 | Google OAuth Restricted-Scope Go-Live Release Desk | B2B SaaS, workflow, AI, sales/email, backup, document-automation, and integration vendors using Gmail/Drive/Calendar/Sheets APIs | Enterprise customer go-live, renewal, or rollout blocked by unverified-app warning, restricted-scope review, Google rejection, security assessment request, Workspace admin block, or 100-user/test-user ceiling | Vendor authorization over OAuth project, exact scopes, Google review/rejection thread, app evidence, data-use disclosures, scope-minimization map, demo video, CASA/security-assessment route, Workspace admin consent pack, submission log | SOC2 consultants, appsec boutiques, Google Workspace/MSP partners, SaaS dev agencies, RevOps/integration agencies | 12k-35k PLN for sensitive-scope/admin-consent case; 35k-80k PLN plus pass-through for restricted-scope/security-assessment prep | Appsec firms, assessors, and dev teams can copy; exact live Google case and customer go-live workroom are controlled |
| 2 | Microsoft Entra Admin-Consent Deal Release Desk | B2B SaaS vendors with Microsoft 365 integrations | Enterprise buyer blocks deployment over verified publisher, tenant consent, risky scopes, or app registration trust | App registration, permissions, publisher verification, customer admin thread, consent package | Microsoft partners and SOC2 consultants | 10k-30k PLN | Microsoft partners/devs can copy; less official platform review than Google |
| 3 | Slack Marketplace Security Review Go-Live Desk | SaaS vendors and agencies launching Slack apps | Customer cannot install or app marketplace review blocks release | App review ticket, scopes, manifest, test workspace, security questionnaire | Slack dev agencies | 8k-25k PLN | Slack agencies/internal devs |
| 4 | Atlassian Cloud App Security Review Release | Atlassian Marketplace vendors | Marketplace update/review blocks paid cloud app | Marketplace ticket, app descriptor, vuln fixes, reviewer trail | Atlassian partners | 15k-45k PLN | Already tested Atlassian app buyout; security trust heavy |
| 5 | Chrome Web Store MV3 Migration Release | Chrome extension vendors | MV2 deprecation blocks extension availability | Extension source, MV3 migration branch, store review ticket | Extension dev agencies | 10k-35k PLN | Developer shops can copy |
| 6 | Google Play Data Safety / Restricted Permission Release | App developers | Release blocked by Play privacy/data safety or restricted permission review | Play Console ticket, declarations, permission map | Mobile agencies | 5k-20k PLN | Mobile agencies; lower ARPU |
| 7 | Apple App Review Privacy Nutrition Release | App developers | App update blocked by privacy declaration / ATT / entitlement mismatch | App Store Connect ticket, privacy labels, screenshots | Mobile agencies | 5k-20k PLN | Common agency work |
| 8 | Shopify App Data Protection / Protected Customer Data Release | Shopify app vendors | App cannot access protected customer data or app review blocks rollout | Shopify Partner ticket, app scopes, privacy/security evidence | Shopify agencies | 8k-25k PLN | Shopify agencies and devs |
| 9 | HubSpot App Marketplace Scope Review Release | HubSpot integration vendors | Marketplace listing or customer install blocked by scope/security review | App listing ticket, scopes, test portal, review responses | HubSpot agencies | 5k-18k PLN | Lower urgency |
| 10 | Meta App Review Advanced Access Release | SaaS/social tools | Business app blocked by advanced access review | Meta app review ticket, permission use-case evidence | Social/dev agencies | 8k-25k PLN | Meta app review consultants |
| 11 | LinkedIn API Partner Approval Release | recruiting/sales tools | Customer deal blocked by missing LinkedIn API partner access | Partner request, customer use case, app review thread | RevOps agencies | 10k-30k PLN | Access is discretionary, opaque |
| 12 | Zoom App Marketplace Review Release | SaaS vendors | Zoom app review blocks customer rollout | App review ticket, OAuth scopes, privacy docs | Zoom agencies | 5k-18k PLN | Lower complexity |
| 13 | Salesforce Connected App Security Release | ISVs | Customer blocks OAuth/connected app over scope/security concerns | Security review notes, package, connected app config | Salesforce partners | 12k-40k PLN | Salesforce partners strong |
| 14 | Microsoft Graph Change Notification / Publisher Release | SaaS vendors | Enterprise customer blocks Graph integration | App registration, Graph scopes, publisher verification, admin consent | Microsoft partners | 10k-30k PLN | Subcase of #2 |
| 15 | AWS Marketplace SaaS Contract Listing Release | SaaS vendors | Procurement wants AWS Marketplace private offer but listing/remittance setup blocked | Marketplace listing ticket, tax/payout docs, entitlement testing | AWS partners | 15k-45k PLN | Cloud marketplace variants failed |
| 16 | Azure Marketplace Transactable Offer Release | SaaS vendors | Customer procurement can buy only through Azure Marketplace | Partner Center ticket, offer listing, payout setup | Cloud partners | 15k-45k PLN | Microsoft partners can handle |
| 17 | Google Cloud Marketplace Procurement Release | SaaS vendors | Customer needs GCP Marketplace purchase path | Partner portal listing, entitlement testing | Cloud partners | 15k-40k PLN | Cloud marketplace path failed before |
| 18 | Okta OIN App Submission Release | SaaS vendors | Enterprise customer demands Okta Integration Network app | OIN submission, SAML/OIDC config, test tenant | IAM consultants | 8k-25k PLN | IAM consultants |
| 19 | SCIM Provisioning Enterprise Deal Release | B2B SaaS vendors | Enterprise customer blocks deal until SCIM/SAML provisioning works | Customer request, test IdP, SCIM endpoints, acceptance evidence | SOC2/customer-trust partners | 15k-50k PLN | Dev shops and identity consultants |
| 20 | SAML Enterprise Security Exception Release | SaaS vendors | Customer blocks renewal/go-live over SSO/SAML evidence | Customer ticket, test tenant, config, signoff | SOC2/customer-trust partners | 8k-25k PLN | Very common |
| 21 | CASA Security Assessment Prep Lane | Google API app vendors | Google requires CASA/security assessment | Scope map, policy docs, assessment booking, assessor questions | CASA assessors and appsec boutiques | 25k-70k PLN | Assessors own trust; useful only as prep |
| 22 | OAuth Scope-Minimization Retrofit Sprint | SaaS vendors | Google or customer rejects overbroad scopes | Code/scopes, feature map, consent screen, resubmission | Appsec/dev agencies | 10k-30k PLN | Dev teams can do |
| 23 | Workspace Admin Allowlist Consent Pack | SaaS vendors selling to Google Workspace customers | Customer admin blocks third-party app under API controls | OAuth client IDs, scopes, data-use note, admin instructions | Workspace MSPs | 6k-18k PLN | Admin/docs simple unless combined with Google verification |
| 24 | Gmail Add-on Verification Release | Gmail add-on vendors | Add-on listing or OAuth review blocks publish | Add-on project, scopes, demo, review ticket | Workspace agencies | 8k-25k PLN | Narrow and platform-dependent |
| 25 | Drive Backup App Restricted-Scope Release | backup/compliance SaaS | Google restricted scopes block production | Restricted-scope case and security assessment path | backup SaaS vendors | 25k-80k PLN | High-trust data/security |
| 26 | Calendar Automation Scope Release | scheduling/workflow SaaS | Customer deployment blocked by sensitive Calendar scopes | Google review ticket, demo, privacy evidence | SaaS agencies | 10k-30k PLN | May be simple/internal |
| 27 | Gmail Send/Modify Scope Release | email productivity/sales tools | Revenue blocked by Gmail API restricted scopes | Google review, scope use-case, data deletion, assessor path | RevOps/email-tool agencies | 20k-70k PLN | Appsec and email vendors |
| 28 | Drive DLP/Document Automation Scope Release | document automation/AI vendors | Enterprise customer blocks Drive integration | Google review plus Workspace admin consent pack | customer-trust advisers | 20k-70k PLN | Trust and security heavy |
| 29 | Google Ads API Token Review Release | martech/adtech vendors | Developer token review blocks customer rollout | Ads API token application, MCC/customer evidence | PPC agencies | 8k-25k PLN | Ads agencies/devs |
| 30 | Looker Studio Community Connector Review Release | analytics vendors | Connector review blocks publishing or enterprise deployment | Connector source, scopes, OAuth, review ticket | analytics agencies | 5k-18k PLN | Lower ACV |
| 31 | OpenAI/LLM Enterprise Security Exception Pack | AI app vendors | Enterprise buyer blocks over AI/data-use controls | Buyer questionnaire, logs, model/data flow | AI trust consultants | 10k-35k PLN | RAG/AI branch fresh-failed |
| 32 | Zendesk Marketplace App Security Release | support-tech vendors | Marketplace review/customer install blocked | App review ticket, scopes, privacy/security docs | Zendesk agencies | 5k-18k PLN | Lower urgency |
| 33 | ServiceNow Store App Certification Release | SaaS/ITSM app vendors | Store app certification blocks enterprise sale | Certification ticket, test evidence | ServiceNow partners | 15k-50k PLN | ServiceNow partners strong |
| 34 | Adobe Marketplace OAuth Review Release | creative/workflow SaaS | Marketplace/app review blocks access | OAuth review ticket, privacy/scopes | Adobe dev agencies | 5k-18k PLN | Smaller volume |
| 35 | GitHub App Permission Review Release | Devtools vendors | Enterprise customer blocks GitHub App permissions | App permissions map, org install instructions | DevSecOps consultants | 8k-25k PLN | Devtools teams can do |
| 36 | GitLab App/Integration Security Release | Devtools vendors | Enterprise buyer blocks integration permissions | Scope map, security ticket | DevSecOps consultants | 8k-25k PLN | Similar to #35 |
| 37 | Notion Integration Review Release | productivity SaaS | Customer blocks integration over Notion scopes | Integration config, review evidence | Notion agencies | 3k-12k PLN | Low ACV |
| 38 | Dropbox App Review Scope Release | document/workflow SaaS | App review/customer security blocks file access | Review ticket, app scopes | appsec agencies | 8k-25k PLN | Smaller market |
| 39 | Box App Enterprise Authorization Pack | B2B SaaS vendors | Enterprise Box admin blocks app | OAuth app, scopes, admin trust doc | Box partners | 8k-25k PLN | Box partners/internal IT |
| 40 | Enterprise Browser Extension Approval Pack | SaaS/browser extension vendors | Customer IT blocks extension rollout | Extension ID, permissions, store listing, policy template | SOC2/customer-trust partners | 8k-25k PLN | Dev/customer-success can do |

## Finalists

| Finalist | Control strength | Decision |
|---|---|---|
| Google OAuth Restricted-Scope Go-Live Release Desk | Official Google verification/rejection thread, exact scopes, live customer go-live blocker, app project authority, submission log, Workspace admin consent evidence, security-assessment route where required | Advance. Strongest because the platform gate is binary and costly, the case memory compounds across rejection reasons, and the initial case can be controlled before Google/appsec incumbents see it. |
| Microsoft Entra Admin-Consent Deal Release Desk | Strong enterprise go-live pain, but many Microsoft partners and dev teams can solve and there is less central verification pressure | Hold as backup. |
| SCIM Provisioning Enterprise Deal Release | High WTP for enterprise SaaS but quickly becomes implementation/dev work and is crowded | Reject. |
| Shopify App Protected-Data Release | Clear platform gate but lower ACV and app agencies are close | Reject. |
| Chrome MV3 Migration Release | Real deadline pressure but mostly developer migration; weak control once templates exist | Reject. |
| Google CASA Security Assessment Prep Lane | High ticket but assessor-owned; best as subcase of Google OAuth lead | Reject as standalone. |

## Internal Cap Check

- Concrete 6-month control proof exists: Google review/rejection threads, exact OAuth scopes, app project authority, consent screen/homepage/privacy evidence, demo videos, submission logs, scope-minimization decisions, security-assessment booking/LOA handoff where required, Workspace admin consent packet, and customer go-live/procurement progress.
- First proof is not interest: the case starts only when a named customer deployment, renewal, procurement step, or rollout is blocked by Google OAuth verification, restricted scopes, security assessment, or Workspace admin app controls.
- The first buyer is not a consumer app founder asking for generic help; it is a B2B SaaS or integration vendor with contract value at risk.
- Copy risk is material: appsec firms, Google-designated assessors, dev agencies, SOC2 consultants, and internal engineering teams can do parts of the workflow. The score is capped below 90 because this is a productized access-release desk, not ownership of a legal receivable or titled asset.
- It still clears simulation because the platform gate is official, the artifact is operational rather than advisory, the outcome is visible in Google/customer admin workflows, and the niche compounds into a rejection-pattern and reviewer-response memory that generic appsec firms do not start with.

## Simulation Verdict

**Advance: Google OAuth Restricted-Scope Go-Live Release Desk**

Simulated score: **88.2 / 100**

Rationale: This is stronger than the recent AI/RAG evidence pack failures because the blocker is an official platform verification/admin-consent case, not merely an enterprise questionnaire. It is stronger than generic developer help because it starts with a named customer go-live or renewal at risk, excludes broad appsec remediation, and produces a platform/customer action record: Google submission, reviewer response, scope approval/progress, security-assessment handoff, Workspace admin consent progress, or clean no-go.
