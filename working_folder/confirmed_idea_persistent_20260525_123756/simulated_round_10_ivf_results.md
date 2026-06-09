# Simulated Round 10 Results: IVF Carrier-Screening Consent Rail

Date: 2026-05-25 Europe/Warsaw.

## Candidate

IVF Carrier-Screening Consent & Routing Layer / CycleGuard Genetics.

## Scores

| Review | Score | Result |
|---|---:|---|
| Prior simulated archive review | 91-92 | Pass on paper |
| Current simulated reviewer 1 | 84 | Fail under current `>87` gate |
| Current adversarial simulated reviewer 2 | 76 | Fail |

## Dominant Objections

- The 2-month proof path is concrete, but clinic acquisition is only marginally securable for an unknown part-time founder because it touches patient trust, genetics-adjacent health data, and consent flow.
- Copy risk is high: IVF clinics, lab vendors, nurses, genetic counselors, or clinic software vendors can internalize the workflow once shown.
- The strongest version is clinic operations/compliance, not genetics advice; it needs a named reviewer, clinic medical control, clean DPA/DPIA, and no diagnosis/treatment advice.
- Economics are plausible but contract-value-to-CAC is uncertain.

## Decision

Do not advance to real Zero To One in this run because the current independent simulated score does not exceed 87.

## Useful Future Pivot

If revisited, start with a lower-trust clinic operations product: sample/status chasing and audit-log support under clinic control, not consent workflow ownership. Require a named reviewer and one warm clinic path before serious work.
