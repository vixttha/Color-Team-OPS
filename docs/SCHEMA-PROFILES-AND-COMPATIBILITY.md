# Purple — Schema reconciliation (historical + neutral v0.0.1)

**Scope:** `feature/v0.0.2-idea-feature-library-purple`, development/reference only. Original 36 IDEA and 5 FEAT record blobs are preserved. The historical schemas remain in `ideas/schema/v1` and `features/schema/v1`; the neutral template lives under `portable/v0.0.1/`.

## The compatibility decision

Do **not** overwrite old records with a new schema, or declare one profile silently interchangeable with the other. These are intentionally versioned **profiles**:

| Meaning | Historical Color-Team-OPS | Reusable v0.0.1 | Policy |
| --- | --- | --- | --- |
| Idea identity | `id: IDEA-xxxxxx` | same ID shape | Stable **within** each host repository; preserve history |
| Idea origin | `created_by/type/source/source_catalog_id` | `created_by/source` | Historical Fxx catalog ID retained, optional for new local records |
| Idea positive effects | `positive_effects` | `benefits` | Semantically related, but not auto-translated |
| Idea negative effects | `negative_effects` | `risks` | Keep the original words and severity, do not flatten |
| Idea synergy | `synergy_note` | relation + narrative | Preserve old synergy in the original; do not discard on export |
| Idea decision | `decision_scope/decided_by/reason` | `decided_by/decided_at/reason` | Needs source review; do not fabricate a date or approval |
| Feature references | `idea_ids` | `idea_ids` | Targets must resolve within same host |
| Feature source | `source_refs`, `verified_evidence` | typed `evidence` | No automatic promotion of source refs into verified evidence |
| Feature milestone | `planned_milestone` (legacy M1–M5) | optional `project_milestone` | Never assume M1–M5 exists in an unrelated host |
| Feature limitations | optional `limitations` | optional `limitations` | Preserve and carry forward, never drop |
| Feature testing | optional `testing` | `testing` | Testing state remains separate from lifecycle |
| Feature release | `release_membership: NOT_ASSERTED` | same mandatory value | **Neither** owns releases; never infer shipped version |
| Prior portable starter | `portable/catalog.json`, `portable/schema` | `portable/v0.0.1/` | Prior files retained for compatibility; **prefer v0.0.1** |

The historical schema now permits additional records without requiring `origin.source_catalog_id` or a fixed M1–M5 milestone, while still validating all previously captured values. The checker does not enforce 36/5 counts. A feature can have zero linked ideas at intake, but a nonempty link must resolve.

## Safe migration of a particular record (only if separately requested)

1. Verify exact branch, record, owner authority and evidence; choose one host as canonical.
2. Allocate the target host ID without overwriting or recycling existing IDs. Build an explicit ID mapping if necessary.
3. Map related fields carefully; retain untranslatable fields and original source reference in a supplementary migration note. A source Fxx is not automatically a target idea ID.
4. Carry original decision only with actual supporting record; keep unknown/untested states unverified.
5. Validate source and target, verify the generated indexes, and compare field-by-field before authorized commit.
6. Never copy private source data, tokens, host grants or product release claims into a reusable starter.

**There is deliberately no automatic lossy converter.** Original records, original decision claims, roadmap, official releases, and integration code are unchanged. The templates are reference data, not permissions.
