# PrismCell v0.0.1 schema source authority

**Current canonical schemas:** `PRISMCELL/core/schemas/`. All new project adopters, starter validation and code use these paths.

**Backward-compatible paths:** `PRISMCELL/schemas/` contain byte-identical copies of the four canonical schemas. The automated parity test must fail if any copy differs. The source manifest is `PRISMCELL/SCHEMA-SOURCES.json`.

**Original Color-Team-OPS-specific schemas:** immutable migration copies in `PRISMCELL/adapters/color-team-ops/legacy-schemas/`. These are historical compatibility evidence, not alternate validators for new v0.0.1 projects. They retain the original nine-team model and older message constraints. Do **not** use them when generating new workcells.

`PRISMCELL/tools/guard.mjs` remains a separate legacy, nine-team-specific reference guard. It is not the reusable generic engine and is not privileged or a GitHub authorization mechanism. This repair does not modify its implementation or historical test records.

**No version bump, no cloud runtime, no Vercel dependencies.**
