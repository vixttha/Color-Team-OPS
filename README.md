# Color Team OPS — Future v0.0.2 Architecture Ideas

**Status: DESIGN IDEAS ONLY — not a v0.0.2 release, implementation, approval, or migration.**
**Branch:** `design/v0.0.2-team-contracts-single-lane`
**Date:** 2026-10-29
**Scope:** One conversation, one Head-controlled execution lane, nine distinct specialist teams, three reused coordination skills, evidence-first validation, internal challenge review, team quality evaluations.

This branch intentionally contains a clean documentation-only design tree. It DOES NOT replace `main`, `release/v0.0.1-cloud-only`, the installed plugin, existing skill files, or Issue #4. There are no executable team skills, production state machine, runtime backend, CI workflows, or automatic dispatch here. The current implementation baseline remains v0.0.1; the separate Issue #4 design is a reference, not automatically integrated into this proposal.

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
