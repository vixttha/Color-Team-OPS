# CTO-V002 P0–P7 — Owner-facing release-readiness dossier

**Mission:** CTO-V002-SINGLE-THREAD. **Version:** v0.0.2. **Status: RELEASE_BLOCKED.** **Integration:** `integration/v0.0.2-master-single-thread`. Owner explicitly permits development/test/audit, **NOT** merge, production deployment or plugin release.

## Priority disposition and review evidence

| Priority | Team/Head disposition | Actual scope and missing proof |
| --- | --- | --- |
| P0 Orange | REQUIRES_OWNER_DECISION | Technical trust classification written in `V002-P0-ORANGE-TRUST-SCOPE.md`; owner must resolve whether initial v0.0.2 requires protected-host mode. |
| P1 Yellow → Orange | TECHNICALLY_COMPLETE for D2 reference source/tests; production UNVERIFIED | New `repair-event.schema.json` and D2 repair protocol; M1 bridge v6, journal/worker/receipt binding and adversarial negative regressions. No genuine protected issuer. |
| P2 Yellow | REQUIRES_OWNER_DECISION | Canonical installed private plugin 0.0.1; no verified unpublished preview. Staging identity or canonical update requires separate approval. All host trials NOT_RUN. |
| P3 Purple | BLOCKED | 270 candidates/54 reserved visible holdouts; independent oracle labels **0**, independent reviewer refs **0**, truly sealed holdouts **0**. Candidate preregistration is not final frozen corpus. |
| P4 Yellow | BLOCKED | No candidate-host trial, baseline or ablation execution; actual evaluated case count **0/270**; no quality statistic. |
| P5 Orange/Purple/Gray | BLOCKED | Source-only adversarial checks and host-trial matrix prepared. Genuine host acceptance and UX traces NOT_RUN. |
| P6 Green | IN_PROGRESS until FINAL documentation source SHA native CI succeeds | Exact source/ZIP parity and compatibility previously passed, but every code/docs change requires a new run. |
| P7 Head/Verification Gate | BLOCKED | Mandatory host/evaluation evidence missing; no release grant; do not present for publication as READY. |

## Confirmed source engineering scope
- Nine specialists, three coordinators, and only the three existing coordinator skills updated from v0.0.1; nine specialist SKILL.md files retain the v0.0.1 exact blob hashes.
- M1 reference repairs are bounded and consent-linked, new D2 repair event/transition/prior receipt checker is fail-closed, and read-only advice remains usable without an authenticated host.
- M2 directory has 18 capability identifiers, a compact skills-only fallback; M3 advisor is not an authority issuer.
- The optional ideas/features library is not a runtime dependency; IDEA-000037 stays captured/not planned/not tested.
- Source candidate manifests indicate 0.0.2; **this is NOT an installed v0.0.2 plugin**.

## Exact revision evidence — retain historical SHA boundaries
- Prior verified baseline `9b6c0eedf6b577dcce1f516c58c7a1c2ad953315`, run 41151644480: **520/520 Linux and Windows**, four matching 32-file ZIP builds.
- Latest **completed code + test evidence before this dossier revision**: `6abc04a8465667ca7ebf0bc02a1d6a1f8123471d`, [GitHub Actions run 41528132175](https://github.com/vixttha/Color-Team-OPS/actions/runs/41528132175), **550/550 Linux and Windows**, two complete ZIP builds each OS; cross-platform SHA-256 `6c673256a5cb7ee3371e64134e31eb640729577c74fdb5a93dc1a0d37c11db98`.
- **The documentation commit containing this dossier changes HEAD. Revalidate that new exact HEAD with the same trusted Windows/Linux CI before claiming it tested; capture new run ID and artifact hash in Issue #8.** Archives in CI temp space are not published release artifacts.

## Unresolved risks by severity
- CRITICAL RELEASE GATE: no real installed-v0.0.2 host acceptance, no independent 270-case oracle/trial evidence; no basis for quantitative quality claims.
- HIGH if privileged mode is selected: no authenticated managed issuer, durable multi-tenant revocation, signed protected repair receipts or real cross-chat exclusive-write fence. Owner scope decision P0-DEC-01 required.
- HIGH: authority confusion if GitHub comments, test doubles or source manifests are promoted into host grants; the verifier and skills must fail closed.
- MEDIUM: candidate eval boilerplate and unblinded reserved holdouts; Gray Cell live UX untested.
- MEDIUM: integration branch protection/ruleset enforcement has not been verified as active; use exact-SHA leases, branch-scoped CI, restricted write permissions and explicit owner review before promotion. Historical preflight found no branch protection and a ruleset-read plan limitation; no invented new protection claim.

## Rollback and restricted next steps
The *installed* plugin is currently private v0.0.1 with canonical identity `plugins_6ae3edf1ea4c819182f275592273e2cc`, observed current release ID `pluginrel_6ae3edf2a4ec8191b5cf9c92c317db22`. Its accepted source is `release/v0.0.1-cloud-only` at `fc77a647554cd40fb94839b3eb99e5f0ce4210a9`. Since no v0.0.2 publication occurred, no rollback action is currently necessary. For a later owner-authorized upgrade, archive exact old release, validate old/new package digests, obtain owner approval, update **only** canonical identity, verify installed version and smoke tests, and restore the saved old release using an explicitly authorized rollback procedure if needed; do not infer automatic rollback APIs.

Owner decisions needed before gated activities: choose initial skills-only versus protected-host mandatory acceptance; authorize an actual private staging mechanism (or candidate install procedure) and independent eval reviewer/resource if desired; later separately approve specific merge/canonical publication. **No permission to deploy, spend or publish is contained here.**

**Logical Internal Auditor verdict:** Source tests may validate source claims at their specific SHAs only. Real host tool actions, separate authenticated reviewers and user authorizations remain unproven. **Final Head decision: RELEASE_BLOCKED.**
