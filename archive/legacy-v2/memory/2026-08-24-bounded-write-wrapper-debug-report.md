# DEBUG REPORT — second bounded-write wrapper incompatibility

Status: `DONE_WITH_CONCERNS`

Date: 2026-08-24

## Scope

This repair addresses only strict bounded-return parsing and canonical bounded-return packet instructions. The failed run `zero_to_one_candidates_20260824_111939`, its five discovery traces and returns, its receipt, seed reservation, run registration, protection anchors, and development contract were used read-only and were not resumed, integrated, rewritten, or re-pinned. No candidate cohort was generated or registered.

## Root cause

The bounded-write decoder admitted the anchored long JSON-string wrapper but had no grammar for the observed anchored inline-await wrapper. The FPE trace therefore failed before its otherwise exact add-file patch could be attested.

## Repair

The decoder now admits exactly two fully anchored wrapper grammars, with insignificant whitespace only:

```javascript
const patch = "<JSON-string literal>";
const result = await tools.apply_patch(patch);
text(result);
```

```javascript
const patch = "<JSON-string literal>";
text(await tools.apply_patch(patch));
```

The literal is decoded only with `json.loads`. The strict legacy raw-patch branch remains separate. The existing single-call, single canonical add-file operation, expected absolute path, regular-file, no-symlink, FileChange/call/result correlation, byte reconstruction, and resulting-file equality checks remain in force. No JavaScript is executed or generically evaluated.

New manager discovery, history, cartography/mapping, cluster-audit, and Level-1 packets, plus candidate-runtime Level-2 and fact-closure packets, contain the exact canonical long-form instruction. The Archipelago protocol requires the same instruction for all bounded-return scout/discovery, builder, transformation, history, mapping, audit, Level-1, selector/ranker/challenger, Level-2, finalist-selector, and fact-closure packets.

## Immutable replay results

| Agent | Wrapper | Trace SHA-256 | Return SHA-256 | Bytes | Completion (Europe/Warsaw) | Result |
|---|---|---|---|---:|---|---|
| baseline-gen-tse | long | `1a23d4d2ee1c2bcade3de28c50dd728797b2bd1340104b2a59f8d59aee277303` | `32e0b6b2e9c1c98d3e5e26a66bfab65e5acc3b60cde3a46db78af2f2d95ac11e` | 23,541 | `2026-08-24T11:28:50.499000+02:00` | attested |
| baseline-gen-ih | long | `76900f39d39bc1bfb3d863678eecc2d14da8afa868a30f4f01854a1ed148e036` | `a07c5b0f288b8ac06c585bdc9cefa36c962a987437848f22de803ac534e27ae3` | 23,505 | `2026-08-24T11:28:59.045000+02:00` | attested |
| baseline-gen-ia | long | `2bff26b31d288c62892e3c3a73d81ff7df23b70addb4ad3d5fe295f4dba7717b` | `c252c78adf2ebb50b9682db0bb39db01e3b70b02ae8df493d486fdfe8cb695a3` | 27,717 | `2026-08-24T11:25:41.011000+02:00` | attested |
| baseline-gen-rsa | long | `9ebe6833c7f56f56c68cbf00d63f3b9bff640e533df06a5a05f76a631d06db7b` | `fcb7686adfb291032c5bea3c57a0a508020e2daed8c6a6ef0f3f291f6e64729f` | 26,332 | `2026-08-24T11:25:17.781000+02:00` | wrapper parsed; canonical attestation rejected |
| baseline-gen-fpe | inline-await | `0800fe49bc8ae01d75def18b8a8027ae94511bd90f307ac4d83ee89ce8f26b54` | `90dbb93da3b164bf5f7fe8b5b99483119a71bcf74ca964ba4fe36a2dc999cdc6` | 25,402 | `2026-08-24T11:25:10.912000+02:00` | attested |

All five wrapper programs match their intended long or inline grammar, and all FileChange bytes and timestamps reconcile with their own return files. The RSA trace is independently malformed for the preserved path rule: its patch header targets the relative path `working_folder/zero_to_one_candidates_20260824_111939/agent_returns/baseline-gen-rsa.json`, not the expected absolute canonical path. Accepting it would weaken an explicitly preserved security invariant. Consequently, the immutable evidence can support three attested long wrappers plus the attested inline wrapper, not four fully attested long wrappers.

The failed run remains at its sole `registered` checkpoint, contains no agent manifest records or raw-pool integration, and retains only its pre-existing IA trace attestation.

## Verification

- Focused parser/manager/runtime suite: 65 tests passed in 2.100 seconds.
- Focused adversarial parser suite: 36 tests passed.
- Auditor self-test, including integration coverage: 162 tests passed in 776.955 seconds.
- Standalone complete integration suite: 65 tests passed in 750.793 seconds.
- Python syntax parsing: manager, runtime, three local test modules, and auditor all passed.
- Generator skill validation: `Skill is valid!`.
- Protected fixed files, Validation Gates block, immutable root/child anchors, seed reservation, run registration, and development-contract hashes all match their failed-run pins.
- Independent adversarial review found no wrapper or expression bypass. It confirmed the RSA evidence/path conflict and recommended preserving the absolute canonical-path rejection.

## Current workflow hashes

- `audit-funnel`: `9e8ed1ab9138ff1573eb540e1cf2f0af5fea1f10647f8c3de8dfed73f23b7a35`
- `blind-search-protocol`: `7b64926e604fc7a5f219a54769d81816a5183145cd72adfe9274925694173824`
- `v2-candidate-development`: `15d5ccccb027beeeb7f4656864954a309a06032a7f10b53a530fc7584eddfcb5`
- `v2-matched-experiment-manager`: `e76a3710dc317224b9364400e7ffdb211ce3f7d3c1e648f4e8f00e09e9867486`

The old root and child anchors remain immutable and therefore retain the prior protocol/runtime/manager hashes. A completely fresh Step 1 run must bind all four current workflow hashes in new root and child protection anchors and must create a new unique explicit seed, seed reservation, run registration, receipt, and development contract under a new run identity.
