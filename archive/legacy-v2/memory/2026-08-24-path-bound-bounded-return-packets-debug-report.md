# DEBUG REPORT — path-bound bounded-return packets

Status: `DONE`

Date: 2026-08-24

## Scope

This repair hardens only bounded-return packet rendering, pre-dispatch verification, and the matching protocol text. The failed run `zero_to_one_candidates_20260824_111939`, its five discovery traces and returns, registration receipt, seed reservation, run registration, protection anchors, and development contract were used read-only. The run was not resumed or integrated. No candidate cohort was generated or registered.

## Root cause

Packets declared an absolute required return path but reused a static generic wrapper example containing only `<JSON-encoded complete patch>`. The RSA agent therefore invented a workspace-relative `*** Add File:` header. The trace parser correctly rejected that target, but packet preparation did not bind the exact absolute patch header into each packet or structurally verify that binding at dispatch authorization.

## Repair

The static instruction was replaced by `bounded_return_instruction(output_path, run_dir)`. It emits one packet-specific instruction containing the literal canonical absolute output path in both the required-return declaration and the exact patch header:

```text
*** Begin Patch
*** Add File: /the/packet-specific/absolute/agent_returns/path
```

New packets instruct only the canonical long form:

```javascript
const patch = "<JSON-encoded complete patch beginning with the exact absolute header above>";
const result = await tools.apply_patch(patch);
text(result);
```

The trace parser retains exactly the two approved, fully anchored JSON-string wrapper grammars, with insignificant whitespace only:

```javascript
const patch = "<JSON-string literal>";
const result = await tools.apply_patch(patch);
text(result);
```

```javascript
const patch = "<JSON-string literal>";
text(await tools.apply_patch(patch));
```

JSON decoding remains `json.loads`; the strict legacy raw-patch branch remains separate. JavaScript is never executed or generically evaluated.

Before rendering or dispatch authorization, the verifier now requires:

- an absolute, lexically canonical, NFC-normalized output path directly inside the run-owned `agent_returns` directory;
- exact filesystem spelling for every existing run/output component, no traversal, sibling, workspace-relative, case, Unicode, symlink, or hard-link alias, and an unused target as required by `Add File`;
- one exact-spelling, single-link, run-owned packet read through `O_NOFOLLOW`, with stable inode, size, and modification time;
- exactly one matching required-return declaration, literal `*** Add File:` header, canonical long wrapper, and precommit packet digest;
- no placeholder, relative/absolute alternative, second declaration/header, encoded or literal extra patch operation, alternate wrapper, or different output path;
- deterministic manager/runtime stage, agent, task, packet, output, allocation-precommit, and batch identities rather than identities selected by mutable launch values.

The resulting-file verifier also requires exact component spelling, a single-link regular file, matching `lstat`/opened inode, exact FileChange correlation, reconstructed bytes, and resulting-file equality.

The manager applies the gate to Audited Funnel discovery, history compression, cartography, cluster audit, and Level-1. The candidate runtime applies it to baseline and shadow Level-2 and fact closure both during preparation and immediately before each batch. The protocol makes the same path-bound rendering and executable gate mandatory for every listed Archipelago scout, builder, transformer, mapper, selector, challenger, dossier, and closure role without embedding a run-specific path in the protocol.

## Immutable replay results

| Agent | Observed wrapper/target | Trace SHA-256 | Return SHA-256 | Bytes | Completion (Europe/Warsaw) | Replay result |
|---|---|---|---|---:|---|---|
| baseline-gen-tse | long / absolute | `1a23d4d2ee1c2bcade3de28c50dd728797b2bd1340104b2a59f8d59aee277303` | `32e0b6b2e9c1c98d3e5e26a66bfab65e5acc3b60cde3a46db78af2f2d95ac11e` | 23,541 | `2026-08-24T11:28:50.499000+02:00` | attested |
| baseline-gen-ih | long / absolute | `76900f39d39bc1bfb3d863678eecc2d14da8afa868a30f4f01854a1ed148e036` | `a07c5b0f288b8ac06c585bdc9cefa36c962a987437848f22de803ac534e27ae3` | 23,505 | `2026-08-24T11:28:59.045000+02:00` | attested |
| baseline-gen-ia | long / absolute | `2bff26b31d288c62892e3c3a73d81ff7df23b70addb4ad3d5fe295f4dba7717b` | `c252c78adf2ebb50b9682db0bb39db01e3b70b02ae8df493d486fdfe8cb695a3` | 27,717 | `2026-08-24T11:25:41.011000+02:00` | attested |
| baseline-gen-rsa | long / workspace-relative | `9ebe6833c7f56f56c68cbf00d63f3b9bff640e533df06a5a05f76a631d06db7b` | `fcb7686adfb291032c5bea3c57a0a508020e2daed8c6a6ef0f3f291f6e64729f` | 26,332 | `2026-08-24T11:25:17.781000+02:00` | correctly rejected |
| baseline-gen-fpe | inline-await / absolute | `0800fe49bc8ae01d75def18b8a8027ae94511bd90f307ac4d83ee89ce8f26b54` | `90dbb93da3b164bf5f7fe8b5b99483119a71bcf74ca964ba4fe36a2dc999cdc6` | 25,402 | `2026-08-24T11:25:10.912000+02:00` | attested |

An in-memory clone of the RSA trace that changes only the relative patch header and corresponding FileChange stdout to the exact absolute target attests the same 26,332 bytes and completion timestamp. The immutable trace and return were not modified.

The failed run remains at only its `registered` checkpoint. It contains no agent manifest records, raw pool, or Level-2 cohort, and retains only its pre-existing IA trace attestation. No failed output was integrated.

## Verification

- Complete focused trace-parser/manager/runtime suite: 80 tests passed in 4.313 seconds.
- Standalone complete integration suite: 65 tests passed in 854.329 seconds.
- Complete auditor self-test: 162 tests passed in 854.671 seconds.
- Python syntax validation passed for manager, runtime, all three local test modules, and auditor.
- Generator skill validation returned `Skill is valid!`.
- Protected-boundary hashes, Validation Gates block, failed-run trust files, receipt, development contract, and immutable RSA trace/return hashes match their pre-repair pins.
- Independent adversarial review: `PASS`; no remaining concrete wrapper, expression, path-alias, packet-substitution, or result-attestation bypass found.

## Files changed

- `utilities/v2_matched_experiment_manager.py`
- `utilities/v2_candidate_development.py`
- `utilities/test_v2_trace_parser.py`
- `utilities/test_v2_manager_seed.py`
- `utilities/test_v2_candidate_development.py`
- `/Users/igor/.codex/skills/generate-zero-to-one-candidates/references/blind-search-protocol.md`
- `memory/2026-08-24-path-bound-bounded-return-packets-debug-report.md`

The auditor and all protected validator/founder/contract/seed/routing artifacts were not changed.

## Workflow pins for a fresh Step 1

- `v2-matched-experiment-manager`: `6f33b047440f9c7e2c8fd5c4c0759806977811e852dd1b8dad4658a53300b532`
- `v2-candidate-development`: `87eebd321a81f0ddfc2f9017ae491f26c1d38a173fdd368e6b6848f5007110b2`
- `blind-search-protocol`: `e30d4dd9ae2336ae74acd10ead28ea60e3cf84acc3c93723eaea228aa45eff5f`
- `audit-funnel`: `9e8ed1ab9138ff1573eb540e1cf2f0af5fea1f10647f8c3de8dfed73f23b7a35`

A completely fresh Step 1 must bind all four hashes into newly created root and child protection anchors and use a new run identity, explicit unique seed, seed reservation, run registration, registration receipt, and development contract. Existing failed-run anchors and pins remain immutable and are not reusable as current-workflow attestations.

## Protected hashes

- Founder profile: `2110e393cf8d266906924a394ac5764ce8470a79a76aba7c43555e742ef24f97`
- Success/safety contract: `807dd4758bd5006a98fff51f6aa40246ba160a618d2094258a5d1180d99fb08c`
- Goal: `c236846bd7507f647754bfe38d24a09d3dad48f34440f871d2c48e424a8fa626`
- Validator: `a9089ded6c63e239cdee4445af21381f11e6ad86ae7f6c79c0159bbc5f1e817b`
- Orchestration prompt: `153c09ea955bdac08eb079c617cb66e3456f96cb00956c72ca7cbe82f16a2e0b`
- Validation Gates block: `51a34d0dace801fc277d11ccfa515c16005aad88b856784dd339d3ce1ae5e944`
- Generator skill: `16791c2dead827360698537e5f1df80c1167461c5d6428004311e9c660e234a9`
- Evaluator skill: `e3602e433672cb2355acec26ae7d10e87e5c5384f2a08aa67ef5cc7d8eb0394d`
- Pivot skill: `56088a5792a0658b47c8551093f044f5a8fc57d46d7dcd00840d4713492f9b5b`
- Failed-run root anchor: `9268c1f5b2788d9d3e3033a4559d605f7eb2eb351f45d5c2aeabed18f7458c0f`
- Failed-run child anchor: `6aa6ba85ee8bce4749aa8900a8da212a546dff4a7f69b181ed1766e47971af59`
- Seed reservation: `785daa8636e0372c58fb509e85fe462b0ba1940cae964d3c983cf26a4c0f5808`
- Run registration: `b22d1361659a0fed71ec33872f557733f6d3500db2c8e45335387c7064da29f1`
- Registration receipt: `61a427de33e5439076330c419f62a8086dacac840eb342e8f377910503eb229f`
- Development contract: `521379f9314e7ebc5954265064f594de6716d31cd66ee230d444dc70ffb46aa1`
