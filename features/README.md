# Color-Team-OPS Feature Candidate Registry — Governance-inspired prototype
**Status: isolated, proposals ONLY. Not live v0.0.2 features and not release membership.**

This `features/records/FEAT-xxxxxx.json` register is deliberately separate from `ideas/`:
- **Ideas** retain brainstorming, pros/cons, source, relationships and owner decisions.
- **Features** provide stable user-visible capability identity, scope/acceptance, links to ideas and milestone targets.
- **Engineering** owns code commits/test results on actual implementation branches; candidate records are not self-verifying.
- **Mission authority** remains with Head, D2 and protected host verification; **release/version truth** remains with owner-approved manifest/changelog/release records, never duplicated in feature data.
- The `release_membership: NOT_ASSERTED` field expressly prevents claiming a feature is shipped from this branch.
- A `verified` lifecycle claim requires actual scoped source-SHA/receipt evidence, plus independent review; syntactic JSON alone cannot confer trust.

The Governance-Branch-Bible source's Feature Registry is a **design candidate**, not a released registry to copy blindly. See `research/05-VERIFIED-SOURCES.md` and the source links in `docs/V002-CONSOLIDATED-PIPELINE.md`.

`features/INDEX.md` is a generated read-only index; the records are canonical. An optional standard-library Python generator and structural checker are under `tools/`. No dependency on Governance, Python, owner runner or specific cloud host for plugin operation.
