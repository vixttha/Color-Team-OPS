# Current v0.0.2 master candidate — October 30, 2026

**Current source branch:** `integration/v0.0.2-master-single-thread`. **Status:** UNPUBLISHED / RELEASE BLOCKED. The first heading further below preserves the older design-branch README as historical context, not the current branch identity.

This is **one v0.0.2 release mission**, with internal checkpoints M1–M5. In the same conversation the Head uses **Head → one Worker → Validate → logically distinct Internal Auditor → Head**. Within the user's already-authorized bounded work, continue through ordinary internal handoffs without requesting a new confirmation every time; still stop for externally restricted grants, paid services, merges or publication.

**Candidate source now includes:** the existing nine specialist skills (byte-identical to v0.0.1), three **intentionally updated** coordinator skills (Mission Control, OPS Director, Verification Gate), portable schemas/examples and constitution; M1 reference bridge, M2 nine-team directory/18 capabilities, M3 advisory routing/typed handoff, M4 evaluation scaffold, and M5 blocked release gate records. There are **still exactly twelve skills**, not a 13th routing agent.

**Evidence:** 137 focused M1–M4 Python tests passed in an isolated cloud test workspace with GitHub blob matches, but used synthetic adapters for D2/host integration. The current twelve-skill files and manifests passed 13/13 GitHub-backed static continuity checks. **A full current-SHA repository-wide test, actual installed ChatGPT v0.0.2 missions, 270 real independently labeled specialist cases, true hosted consent/revocation, cross-session lock and owner release approval remain unavailable or unverified.** Do not call the current candidate a released plugin or production-authenticated service.

See [one-thread Head preflight](docs/V002-MASTER-HEAD-PREFLIGHT.md), [M5 coordinator-skill delta](docs/V002-M5-SKILL-CONTINUITY.md), [blocked release gate matrix](docs/V002-MASTER-RELEASE-GATES.json), and [M5 audit](docs/V002-M5-VALIDATION-AUDIT-HEAD.md). This repo remains **cloud-only, provider-neutral and independent of any hosting vendor**, and no user-owned runner is a plugin runtime dependency.

---

# Color Team OPS — Future v0.0.2 Architecture Ideas

**Status: ISOLATED FUTURE-v0.0.2 DESIGN, PROTOTYPE CODE AND TESTS — not merged, published, installed or production-accepted.**
**Branch:** `design/v0.0.2-team-contracts-single-lane`
**Date:** 2026-10-29
**Scope:** One conversation, one Head-controlled execution lane, nine distinct specialist teams, three reused coordination skills, evidence-first validation, internal challenge review, team quality evaluations.

This branch began as documentation-only but now contains D1–D4 prototype code, synthetic tests and limited live GitHub read evidence. It DOES NOT replace `main`, `release/v0.0.1-cloud-only`, the installed plugin, existing skill files, or Issue #4. There are no installed v0.0.2 team skills, production state machine, protected hosted authority, production runtime backend, or automatic dispatch here; owner-runner development CI does exist on this isolated branch. The current implementation baseline remains v0.0.1; the separate Issue #4 design is a reference, not automatically integrated into this proposal.

## Mission cycle

**HEAD → WORKER → VALIDATE → INTERNAL AUDITOR → HEAD**

- **Head:** logical combination of existing Mission Control + OPS Director; accountable for scope, authorized routing, repair decisions, limits, and completion.
- **Worker:** exactly one active selected specialist from the existing nine; specialist owns bounded task execution and its own local self-check/repair.
- **Validate:** evidence-based Verification Gate phase checking real tool results against the exact revision and acceptance criteria.
- **Internal Auditor:** distinct evidence-focused adversarial review phase within the same conversation; not a separate mandatory conversation, not an independent human review.
- **Return to Head:** sole authority to accept, repair, dispatch another permitted team, block, or conclude truthfully.

> **Accountability:** The Head is accountable for completion, the teams are accountable for their work, and the validation evidence is accountable for the claims.

> **Permanent runner-independence law:** Your runners can help develop and verify Color Team OPS, but Color Team OPS must never need them to exist or operate.

## Document map

1. [Scope and decision register](docs/01-SCOPE-AND-DECISIONS.md)
2. [Single-lane architecture and state machine](docs/02-SINGLE-LANE-ARCHITECTURE.md)
3. [Universal Team Creation Contract](docs/03-UNIVERSAL-TEAM-CONTRACT.md)
4. [Nine specialist team contracts](docs/04-NINE-TEAM-SPECIALIZATIONS.md)
5. [Evidence, validation, internal audit and authority](docs/05-EVIDENCE-AND-AUDIT.md)
6. [Specialist evaluation laboratory](docs/06-EVALUATION-LAB.md)
7. [Integration plan, tests and migration](docs/07-INTEGRATION-AND-ACCEPTANCE.md)
8. [Traceability, non-goals and references](docs/08-TRACEABILITY-AND-SOURCES.md)
9. [Three-pass design audit](docs/09-THREE-PASS-AUDIT.md)

## Binding interpretation of "single lane"

One active worker *per mission* and one user-facing conversation are core user goals. A skills-only plugin can instruct this behavior during an available host conversation, but **cannot guarantee a global cross-chat singleton**, persistence or unattended continuation. Those require separately authorized cloud-side enforcement; unavailable proof must be labeled UNVERIFIED. No user-owned runner, device, localhost or local service is required to use Color Team OPS.

## Proposed, not yet accepted

The user has expressed approval of the overall direction, but every new detailed contract, benchmark, state extension and integration step in these documents remains a **candidate design for a future v0.0.2** pending acceptance. Do not silently modify the v0.0.1 release or treat documentation as shipped capability.

## Future v0.0.2 decisions: detailed candidate specifications
These topics were open during the original nine-document design review. They now have **proposed technical decisions, not implemented guarantees**: [single-lane locking](docs/10-SINGLE-LANE-LOCKING-DECISION.md), [authenticated evidence](docs/11-AUTHENTICATED-EVIDENCE-DECISION.md), [specialist performance](docs/12-SPECIALIST-PERFORMANCE-DECISION.md), and the [combined roadmap/decision register](docs/13-V0.0.2-DECISION-RECORD-AND-ROADMAP.md). Basic skills-only use never requires an extra auditor chat, a local runner or a managed backend. Guaranteed cross-chat exclusive writes remain **UNVERIFIED unless cloud gateway and all relevant enforcement are actually established**. Evaluations and cloud services here are future design only.

## Design-resolution audit
A follow-on [three-pass design resolution audit](docs/14-V0.0.2-DESIGN-RESOLUTION-AUDIT.md) covers the three new technical decisions and final commit isolation. This review validates documentation consistency only—not a deployed lock, actual hosted evidence service, executed specialist benchmarks or a production v0.0.2 release.

## D1: versioned contract reference (new design-stage prototype)
The next stage adds [seven proposed JSON Schema contracts](contracts/v0.0.2/README.md), [the D1 contract map](docs/15-V0.0.2-CONTRACT-PROTOTYPE.md), a [Python reference test suite](tests/test_v002_contracts.py) and [test-scope preflight](docs/16-D1-SCHEMA-TEST-PREFLIGHT.md). These are **design/reference development assets, not a v0.0.2 plugin implementation or evidence that native tests passed**. Earlier three-pass audit reports describe the historical documentation-only snapshots, not these newly added files. Cross-record trusted policy and live provider verification remain to be built. None of the 12 installed skills was changed.

## D1 safety audit follow-up
The transition reference now explicitly permits **Head-authorized emergency BLOCKED/CAPABILITY_BLOCKED/UNVERIFIED** from active stages, without allowing a worker to claim COMPLETE or bypass required gates during successful execution. Regression tests demonstrate that a schema-valid COMPLETE containing arbitrary gate IDs is **still only a claim**, not authenticated mission completion. See [D1 design audit](docs/16-D1-SCHEMA-TEST-PREFLIGHT.md). The 19/19 dual-runner pass on `f091c686...` is historical evidence, not an automatic pass for the newest SHA.

## D2 — Cross-record policy verifier prototype
A [read-only deterministic verifier](policy_v002/verifier.py) now connects the D1 contracts, mission authority, sequential Worker assignments, trusted-source observations, gate records and final Head decisions. The [D2 tests](tests/test_v002_policy.py) use **synthetic provider fixtures only**, not live authenticated GitHub/ChatGPT identities. [D2 audit and observed CI evidence](docs/18-D2-POLICY-AUDIT.md) distinguish structural test results from actual trust-service deployment. D2 does **not** require personal runners, a separate auditor conversation, or a new specialist skill at plugin runtime. No real cloud adapter, global lock or release is claimed.

## D3 — GitHub provider evidence integration (prototype)
The [D3 read-only GitHub adapter](policy_v002/github_provider.py) provides bounded provider lookups and is designed for protected host-issued mission-run bindings, alongside the [D3 trust-boundary guide](docs/19-D3-GITHUB-EVIDENCE-ADAPTER.md). **GitHub evidence does not authenticate Head, user consent or audit independence**; a real host ledger and credential boundary are not yet installed. Tests are designed to mock GitHub responses, while an actual connected GitHub workflow run has been separately inspected. Not a v0.0.2 plugin release.

## D3 audited reference status
[D3 three-pass security and evidence audit](docs/20-D3-PROVIDER-EVIDENCE-AUDIT.md) records the source-bound tests, the separate real GitHub connector observations, and the unimplemented protected-host authorization requirements. The D3 implementation is a read-only reference adapter; a synthetic HostAuthority fixture cannot authenticate real mission grants.

## D4 protected authority reference and real GitHub REST evidence
The [signed host authority reader](policy_v002/host_authority.py), [live GitHub reader smoke](devtools/live_github_smoke.py), [authority regressions](tests/test_v002_authority.py), [trust-boundary design](docs/21-D4-HOST-AUTHORITY.md), and [three-pass D4 audit](docs/22-D4-HOST-AUTHORITY-AUDIT.md) are included on this isolated v0.0.2 branch. The live Python GitHub REST read succeeded in owner-runner development CI. A protected issuer and real user-approved mission ledger have NOT been deployed; the v0.0.2 plugin is not released.

## Owner-locked cloud/provider neutrality — CTO-LOCK-001 (2026-10-30)
**Binding decision:** "Keep Color Team OPS cloud-only, provider-neutral, and independent of any specific hosting platform." See [CTO-LOCK-001](docs/23-CTO-LOCK-001-CLOUD-PROVIDER-NEUTRALITY.md). This rule supersedes any suggestion that Vercel, Supabase, GitHub, an owner-owned runner, or a particular cloud database must be used to operate the product. Provider adapters and managed host choices remain **optional and replaceable** subject to mission needs and explicit authorization. Existing Head/Worker/Validate/Internal Auditor/Head design and original no-runner law remain unchanged.

## D5 — Read-only provider provenance pilot (NOT role authority)
The [D5 observed-records contract](docs/24-D5-PROVIDER-PROVENANCE-PILOT.md) and [optional GitHub provenance inspector](policy_v002/pilot_provenance.py) check ordered issue records and source-bound GitHub CI evidence from [Issue #7](https://github.com/vixttha/Color-Team-OPS/issues/7). The verifier's result **never authenticates Head, Worker, Validator or Internal Auditor merely from GitHub comment labels**, and never claims an issued production host grant. This optional GitHub adapter is compatible with [CTO-LOCK-001 provider-neutrality law](docs/23-CTO-LOCK-001-CLOUD-PROVIDER-NEUTRALITY.md).

## D5 audit and architecture regression
The [D5 pilot audit](docs/25-D5-PILOT-PROVENANCE-AUDIT.md) records both the initial test failure and the repaired live provider check. [Owner-law regression checks](tests/test_v002_neutrality.py) assert cloud-only and runner independence at the core-contract boundary without making GitHub or any hosting vendor mandatory. The pilot confirms real provider observations, **not** authenticated internal team-role identities or production user consent.

## Yellow Team host-authority development lane (isolated feature branch)
The [provider-neutral host authority implementation](policy_v002/host_runtime.py) is tested with an isolated, persistent development journal. The [implementation contract](docs/26-YELLOW-HOST-AUTHORITY-IMPLEMENTATION.md), [Yellow regression suite](tests/test_v002_yellow_host.py) and [Yellow execute/validate/internal audit](docs/27-YELLOW-HOST-AUTHORITY-AUDIT.md) document exact-intent consent boundaries, bounded handoffs, provider evidence rechecks, persistence, revocation and replay rejection. **No real cloud host, user OAuth consent or production-authenticated end-to-end mission was deployed or proven.** The locked cloud-only/provider-neutral/no-runner requirements remain unchanged. This feature branch is not a v0.0.2 plugin release.
