# Color Team OPS v0.0.2 — ONE master mission / Head preflight

**Mission ID:** CTO-V002-SINGLE-THREAD
**Date:** 2026-10-30
**Status:** HEAD_PREFLIGHT_RECORDED / M1 YELLOW WORK ORDER RECOMMENDED, **not yet executed**
**Control loop:** HEAD → one selected specialist → VALIDATE → INTERNAL AUDITOR → HEAD. Each specialist assignment must complete its own gates before Head selects another. No independent auditor chat or automatic nine-team queue.
**Mission target:** one v0.0.2 release with five internal checkpoints M1–M5; not separate v0.0.3–v0.0.6 releases.

## Authoritative source inventory observed at preflight

| Purpose | Branch | Observed SHA | Confidence |
| --- | --- | --- | --- |
| Released v0.0.1 source (do not touch) | `release/v0.0.1-cloud-only` | `fc77a647554cd40fb94839b3eb99e5f0ce4210a9` | Separate skills-only release / PR #1 draft |
| Main | `main` | `a28c2908da47d16dbdf7e55eb29a0c1ce9b6c7d3` | Existing default branch, not selected for writes |
| D1–D5 design/contracts/provider reference | `design/v0.0.2-team-contracts-single-lane` | `963533265c21b0c0ae05d3d85846d65630593c08` | Development source, not product release |
| Yellow host engine | `feature/v0.0.2-yellow-host-authority` | `9b3ca3349016749ed4b809932b5a9e930ec3368b` | Exact-SHA 260/260 Windows + Linux, real GitHub read (run 41016921417); host role authority UNVERIFIED |
| Purple contract and candidate library | `feature/v0.0.2-idea-feature-library-purple` | `2c150833867d506f3fb622a0d0e19f9c5330d5f8` | One-thread routing proposal; 36 ideas and 5 proposed features, not accepted code |
| Research baseline | `research/nine-team-role-audit-2026-10-30` | `b59bd2b7fa289b77cec7f9c2f42eedfcccd2449a` | Research only |
| Master integration branch | `integration/v0.0.2-master-single-thread` | Started at Yellow SHA `9b3ca3349016749ed4b809932b5a9e930ec3368b` | Isolated branch, no integration yet |

The mission contract is `docs/V002-ONE-THREAD-MISSION-CONTRACT.md` on the Purple branch and **is a proposal adopted for planning here**, not itself a protected host grant. Every new commit changes the current integration SHA and requires updated evidence.

## Permissions and protections observed

- The connected account `vixttha` has GitHub repository permissions `admin=true`, `pull=true`, `push=true`; it does not establish an independent protected user-grant issuer.
- Every listed source branch reported `protected=false`; a rulesets API read returned HTTP 403 with GitHub plan restriction. This cannot establish a missing rule of all kinds or a global writer lock. Do not infer real cross-session single-lane exclusivity.
- There is one existing open draft PR #1 from v0.0.1 to main; **do not merge, modify or reuse it**.
- Permission for this mission is bounded to research, preflight, creating/working on this isolated integration branch, source integration, and optional explicitly approved development tests. **No** default authority to merge, publish plugin, deploy, provision paid hosting, issue secret credentials, alter roles, or perform production writes.
- No purchased resource, required user-owned runner, real cloud issuer or production durable ledger is established by the preflight. Actual user approval in ChatGPT is not a cryptographically authenticated host consent token.

## Locked invariants

Exactly nine specialist colors, exactly three coordination skills (Mission Control + OPS Director + Verification Gate); Head controls routing and completion. Internal Auditor is a logical Verification Gate phase, not White, Purple, another specialist or a 13th skill. Source/evidence must match exact revision. No worker can self-grant permissions, bypass validation or declare release.

**CTO-LOCK-001:** Keep Color Team OPS cloud-only, provider-neutral, and independent of any specific hosting platform. GitHub is an optional evidence provider; owner-registered development CI runners **can test** but **can never be required to operate** the product. Without protected host state or exclusive gateway, privileged production completion and cross-chat locking are UNVERIFIED/CAPABILITY_BLOCKED.

## ONE release, M1–M5 internal checkpoints

| Checkpoint | Completion criteria | Current |
| --- | --- | --- |
| M1 trust-state integration | D1–D5 verifier/provider and Yellow host state interoperable; exact-SHA, replay, consent and source checks pass; synthetic/production trust states separate | **Pending integration; Yellow foundation tested** |
| M2 shared awareness | One canonical nine-team registry, searchable versioned capabilities, lazy playbooks; preserve 36 ideas/5 candidate features without marking them shipped | Proposed only |
| M3 adaptive Head routing + typed handoffs | Extend OPS Director (no fourth skill); reasons, required/optional/forbidden capabilities, source-bound evidence and budget/stop gates | Proposed only |
| M4 measured team and route quality | Initial 270 distinct pilot cases with independent oracles; honest holdouts, baseline/combined comparisons and uncertainty; no invented 99% | Plan only; not executed |
| M5 package/release decision | 12-skill identity, v0.0.1 compatibility, exact-SHA candidate source/package parity, real host skill trials, actual user release authorization; no premature production auth claims | **Release BLOCKED** |

All five must remain in **one v0.0.2 release mission**. Head chooses specialists based on findings; nine-team serial execution is **not** mandatory.

## HEAD — First M1 Yellow engineering work order (recommended, NOT executed)

**Capability:** YELLOW / functional engineering / controlled integration and compatibility.
**Goal:** On the master integration branch only, connect the **existing** `policy_v002/host_runtime.py` lifecycle (`IdentityBoundary`, `EvidenceBoundary`, `JournalPort`) to the **existing** seven D1 schemas, D2 `evaluate_completion`, D3 GitHub evidence adapter, D4 signed host reference and D5 provenance observer. **Do not rebuild or replace accepted source.**

**Required work:**
1. Create a source/version mapping that names D1–D5, Yellow, trust levels and actual supported host modes; forbid schema-valid role text from becoming real authority.
2. Build a small versioned adapter/bridge to supply verified cross-record scope and gate facts to the D2 verifier **only** when a protected HostAuthority is genuinely available. If not available, fail closed to `UNVERIFIED`/`CAPABILITY_BLOCKED` without affecting skills-only read-only guidance. Do not treat SQLite test rows or the D4 synthetic MAC as genuine host identity.
3. Reconcile phase enums, event identities, exact SHA, task/criterion/receipt binding, consent digest, mission-level bounded handoff budget, unique receipts, gate order, and revocation/current revision. Keep Head's single active Worker invariant and avoid making a second state authority.
4. Add focused negative and integration tests: forged grant, wrong role, stale/edited SHA, wrong provider record or run attempt, duplicate receipt, missing/failed validation, untrusted auditor, replay, revoke, expired grant, unsupported backend and version migration/backward compatibility.
5. Run actual exact-candidate-SHA tests on permitted development infrastructure; report logs, failures and repair evidence. CI cannot imply a real production-authenticated user grant. Keep plugin runtime independent of owner runners.
6. Deliver source changes, compatibility/migration notes, changed-file scope, actual test links/SHAs, remaining host blockers and a recommendation; then STOP for Validate and separate logical Internal Auditor before Head can dispatch any further team.

**Authority boundaries:** No merge, publish, paid provisioning, production secrets, external cloud deployments, release status changes or changes outside `integration/v0.0.2-master-single-thread` without explicit later owner authorization. Work order can be refined at dispatch when exact current integration SHA and available tools are reread.

**Conservative budgets:** One active Worker; at most two bounded same-Worker repairs per Yellow assignment before Head re-evaluation; no automatic other-team handoff; zero new billable services; no token/cost quota claim. No background/unattended execution.

**Stop conditions:** Source SHA or repository ref changes, external conflicting writer, tool/permission unavailable, unverified user approval for privileged action, missing true host attestation, gate bypass attempt, handoff/repair cap reached, or evidence inconsistent. Record BLOCKED or UNVERIFIED rather than proceeding.

## Head verdict

**PREFLIGHT_PASS_FOR_PLANNING**, `M1_YELLOW_SELECTED_PENDING_DISPATCH`.
This document does **not** certify a production host or grant broad write authority. The first engineering assignment is recommended by Head and awaits the explicit dispatch/gate cycle in this conversation. No Yellow implementation commits, validation or internal audit have occurred **in this master mission** yet.
