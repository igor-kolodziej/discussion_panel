# Shadow Selector Audit

The provisional order was sealed before the independent rankers and challenger launched. No list was averaged or voted. The pre-registered round-robin permutation was `ranker-2 → tail-challenger → ranker-1`.

## Sealed provisional order

- Main six: `D-012`, `D-009`, `D-008`, `D-020`, `X-001`, `D-001`
- Highest reserve sequence used for cutoff sampling: `D-006`, `D-007`, `D-003`, `D-002`, `D-016`, `D-011`, `D-036`, `D-015`, `X-003`, `D-018`, `D-032`, `D-033`
- Frozen at: `2026-08-22T13:16:45+02:00`

## Independent ballots

- Ranker 1: `D-009`, `D-008`, `D-036`, `D-020`, `D-012`, `D-007`
- Ranker 2: `D-012`, `X-001`, `D-009`, `D-001`, `D-006`, `D-020`
- Tail challenger: `D-036`, `D-035`, `I-004`, `D-017`, `D-028`, `D-027`

## Twelve Level-2 slots

| Concept | Selection category | Deterministic rule |
|---|---|---|
| `D-012` | `main_provisional` | Sealed main six |
| `D-009` | `main_provisional` | Sealed main six |
| `D-008` | `main_provisional` | Sealed main six |
| `D-020` | `main_provisional` | Sealed main six |
| `X-001` | `main_provisional` | Sealed main six |
| `D-001` | `main_provisional` | Sealed main six |
| `D-006` | `selector_or_challenger` | Next unique nomination in the pre-registered round-robin |
| `D-036` | `selector_or_challenger` | Next unique nomination in the pre-registered round-robin |
| `D-007` | `selector_or_challenger` | Next unique nomination in the pre-registered round-robin |
| `X-002` | `rejected` | FNV-1a seeded draw from concepts omitted by main and all three ballots |
| `D-003` | `near_cutoff` | Highest unused ID from the sealed provisional reserve |
| `D-034` | `singleton` | FNV-1a seeded draw from one-member semantic clusters |

No shadow selection changes the frozen live cohort or enters downstream routing.

