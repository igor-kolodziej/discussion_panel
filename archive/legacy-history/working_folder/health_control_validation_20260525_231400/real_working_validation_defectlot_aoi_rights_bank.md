# Real Working Validation: DefectLot AOI Rights Bank

Date: 2026-05-29

Prompt file: `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/zero_to_one_prompt_defectlot_aoi_rights_bank.txt`

Simulated score: 88.4

Working-chat Zero To One score: 64

Gate decision: FAILED. The current real gate is `>=85`; this scored below the gate.

Prompt hygiene:
- Clean Zero To One opening used.
- No internal caps, evaluator instructions, threshold language, or validation-agent instructions were included in the prompt.

## Zero To One Summary

Zero To One judged this as a data-asset licensing business, not an AI software company. It acknowledged a real buyer pain: machine-vision and AOI vendors often lack enough real defect examples before a factory POC. It also liked the capital discipline of buyer reservation before source payout.

The score stayed low because industrial defect image data is highly context-specific. A third-party defect lot captured under one product, line, lighting setup, camera, material, tolerance rule, and label convention may only weakly help another buyer's POC. The business therefore looks more like high-friction bespoke dataset sourcing than a scalable rights bank.

## Strongest Objections

1. Buyers ultimately need customer-specific data from the target factory line, product, camera setup, and defect definition. Third-party lots may help demos, pretraining, or sales proof, but they do not de-risk deployment enough to command strategic pricing.

2. Source rights may be weaker than they look. Factory images can include customer products, confidential defects, serial numbers, drawings, logos, process know-how, supplier/customer identifiers, regulated production context, or contractual restrictions.

3. Factories may refuse supply because defect images are reputationally and commercially sensitive, even when anonymized.

4. Historical labels may be inconsistent, incomplete, locally defined, or missing normal/non-defect controls. Without strong label QA, buyers will not trust the lot.

5. Public industrial anomaly datasets and synthetic-data tools weaken willingness to pay for generic examples. Private lots must be much more specific and closer to a live buyer need.

6. The two-sided timing is hard: buyers need a named defect class quickly, while source-side rights approval, scrubbing, metadata collection, and authority checks can take weeks.

7. The 60-day proof was too ambitious for a part-time unknown founder because both source and buyer trust are bottlenecks.

8. The business can collapse into a low-value defect-dataset marketplace unless every lot is buyer-reserved and tied to a live POC need.

## Useful Narrowing From Evaluator

The evaluator suggested that the broad industrial defect data-bank version should not be pursued. A narrower test could focus on rights-cleared surface-defect pilot lots for metal, plastic, or packaging inspection vendors because those are easier to anonymize than PCB/customer assemblies and less exposed to regulated or safety-critical contexts.

However, even this narrowed version remains below the real gate because the core objection is structural: third-party visual-defect data is useful but not controlled enough to become a high-scoring company for this founder profile.

## Lesson

Rights-cleared digital assets are not automatically strong control points. If the asset is heavily domain-specific and buyers still need customer-specific deployment data, the founder controls a useful demo input rather than a decisive payment event, claim, account, or production-critical asset.
