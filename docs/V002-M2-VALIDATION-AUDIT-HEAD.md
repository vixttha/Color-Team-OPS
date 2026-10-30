# CTO-V002-SINGLE-THREAD — M2 Validate / Internal Auditor / Head

**M2 source SHA:** `3422daa9c916de0220d2468ac17ca04f21a664bb`
**Registry JSON blob:** `3716b025bfd0edbbb6b8c0da1d6d96dd6017ae5b`
**Directory source blob:** `9ecb324636bd90ad6d66c9cfd5c620d5a063f619`
**Test blob:** `a0da5bad95f42626a796601d0c286028d00d9fe7`

## Yellow → Validate
M2 introduces exactly nine teams, 18 stable capability IDs, playbook pointers to existing published skills, required-tool metadata (not tool grants), search/abstain, and blocked missing-tool states. No 13th skill, cloud-provider dependency or local runner was introduced.

Initial M2 candidate contained a literal `\\n` in Python source and was invalid. It was repaired in commit `54a41c317cec9771a9f85fc121ba1aa148caaec7`. The 31-test candidate then passed **31/31** in an isolated cloud test sandbox with source, test and registry blob hashes exactly matching GitHub. An additional audit found caller-owned catalog mutation influenced search results and that a partial required-capability match could be treated as sufficient. Yellow issued one bounded repair.

The repaired implementation creates deeply immutable snapshots of loaded team/capability data and refuses incomplete required-capability sets, even when results are truncated by a limit. **35/35 committed M2 Python tests PASS** in the isolated test sandbox; exact file blobs verified above. No full D1–D5 + M1 + M2 repository-wide CI was run on this revision; a separate protected cloud user-authority execution remains unavailable.

**Validate:** `PASS_FOCUSED_M2_SANDBOX`; `EXACT_SHA_FULL_CI_UNVERIFIED`; `PRODUCTION_HOST_UNVERIFIED`.

## Internal Auditor
- Reproduced input-catalog mutation poisoning before repair; after repair, mutation cannot modify a loaded directory.
- Registry identity set is exact nine: Yellow, Orange, Green, Red, Blue, Purple, White, Black, Gray Cell. Coordinator phases are not counted as teams.
- Duplicate capability IDs, path traversal, cross-team playbook pointers, unexpected privilege properties, malformed IDs and invalid schema versions are rejected.
- A search result is **metadata only**, even when a caller supplies tools. It does not provide a validated owner grant, dispatch, scoped evidence, or proof of quality.
- All new M2 tests use designed fixtures, not an authenticated multi-team production execution.

**Internal Auditor:** `M2_REFERENCE_DIRECTORY_ACCEPTABLE`; `ROUTER_AND_AUTHORITY_NOT_YET_PROVEN`.

## Head decision

**M2 development checkpoint accepted** as a canonical reference directory and searchable capability layer, not a published feature or an authenticated production routing decision. Purple's IDEA/FEAT library remains proposed and unmerged; this is distinct implementation source.

**Next active specialist:** YELLOW — M3. Capability: functional policy routing + typed handoff implementation. Justification: now that the registry is available, the next deliverable is conditional OPS Director recommendation, evidence prerequisites, exact source, budgets, at-most-one Worker and no self-dispatch. The existing three coordinators remain, with no fourth routing skill.

**M3 work order:** implement a deterministic **recommendation-only** routing/typed-handoff layer over the M2 directory with required/optional/forbidden capability constraints, exact mission revision/SHA match, previous gate status, stop/budget limits and one active specialist. Invalid or missing authority must block actual dispatch; router cannot issue authenticated tool grants. Add adversarial regression cases and feed outcomes to Validate → Internal Auditor → Head. No paid infrastructure, release, merge or production secrets.
