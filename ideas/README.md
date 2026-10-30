# Color-Team-OPS Ideas Library — Governance-inspired, project-owned v1
**Status: isolated proposal branch; not installed/plugin runtime.**

## Canonical record rule
The 36 source-derived idea records in `ideas/records/IDEA-xxxxxx.json` are canonical for this branch. `ideas/INDEX.md` is a GENERATED VIEW of those records; do not edit it directly. `research/07-IDEA-APPROVAL-FEATURE-CATALOG.md` remains the historical primary discussion capture at frozen source commit `b59bd2b7fa289b77cec7f9c2f42eedfcccd2449a`.

This is an **adaptation, not a literal copy** of Governance-Branch-Bible: JSON is used instead of YAML front matter for easy direct GitHub review and schema validation; no Governance code or runtime dependency. Stable human `IDEA-` IDs are retained, but Governance UUIDv7 identities, its vendor-specific provider library and full CLI are not bundled.

## Lifecycle (separate from implementation/test outcomes)
`captured → triaged → exploring → decision_ready → adopted`; alternative dispositions are `parked,rejected,superseded,duplicate,retired`. This is a conceptual flow, not an auto-promotion state machine. `adopted` means the owner endorsed the **idea direction**, not implementation, test evidence, release or authorization. Implementation statuses are `not_planned,planned,in_progress,implemented,removed,not_applicable`. Testing separately tracks `untested,planned,in_progress,tested` and observed outcome.

## Creating an idea
Create the next unused `IDEA-xxxxxx.json` following `ideas/schema/v1/idea.schema.json`; include benefit, harm, synergy, origin/evidence, stable relation IDs, independent lifecycle/implementation/testing and decision rationale when adopted. Do not rename/recycle IDs. Do not use model text as proof of a test.

## Interoperability / role boundary
Ideas express possibilities and owner intent. Feature candidates under `features/records` reference these IDs but do not own release truth. Existing Color-Team-OPS Constitution, Head permissions, exact SHA, work-order schemas and outside release approvals stay in control. GitHub files are readable without Python/runner; developer validation script is optional, NEVER a plugin runtime dependency.

## Compatibility and check

Existing 36 records are a **historical snapshot**, not a maximum capacity. Additional local records may omit the old `origin.source_catalog_id`; do not recycle IDs or invent original Fxx provenance. Run `python tools/check_idea_feature_library.py` to detect malformed records and stale indexes. For an unrelated project use the empty [portable v0.0.1](../portable/v0.0.1/README.md) profile, not this historical source catalog. See [dated engineering readback](../docs/HISTORICAL-STATUS-VS-ENGINEERING.md).
