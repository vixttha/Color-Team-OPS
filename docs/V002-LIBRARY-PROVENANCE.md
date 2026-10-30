# CTO-V002-SINGLE-THREAD — M2/M5 Ideas + Feature Library provenance

**Source branch:** `feature/v0.0.2-idea-feature-library-purple` at `2c150833867d506f3fb622a0d0e19f9c5330d5f8`.
**Target:** `integration/v0.0.2-master-single-thread`.
**Decision:** copy stable library records unchanged, not the entire diverged Purple branch.

## Exact source-preserving integration

- 36 `IDEA-` records and idea schema/README/generated index.
- 5 `FEAT-` candidate records and feature schema/README/generated index.
- **47 source files in total**, brought in by exact Git object IDs rather than rewritten or renumbered.
- No ID collisions, and no prior `ideas/` or `features/` content existed on the integration branch at import.
- Five idea directions have `lifecycle_status=adopted`; the other 31 are `captured`. **All 36** preserve their original `implementation_status=not_planned` and `testing.status=untested`. `adopted` means an idea direction was accepted, not that it was implemented.
- All five feature records remain `proposed`, `not_planned`, `release_membership=NOT_ASSERTED` with empty `verified_evidence`. Their source frozen links remain intact. Code prototypes under M1–M4 do **not** silently upgrade these separate proposal records.

The original Purple README and index wording describes their **source branch and generated historical view**. This integration note is the current master-context authority and makes clear that those exact copied source records now also exist in the candidate; the original provenance text is retained to avoid rewriting history. Relative links to separate Purple research files are historical source references, not evidence those files were copied.

The library is **metadata only** and does not grant Head permission, mint a protected host token, override D2 policy, authenticate provider observations, add a team, deploy a service, or certify a feature as shipped. A separate user-approved feature promotion and release record are required.

**Validation:** GitHub source-blob parity, record status inspection, and metadata consistency are not real specialist task successes. `tests/test_v002_library.py` provides structural regressions for IDs, links, unshipped status, schema versions and generated indexes. Actual Python execution of that test must be reported separately at the exact revision.

**Owner lock:** cloud-only, provider-neutral, no required user hardware/runner, no auto merge, no publication or paid host provisioning.
