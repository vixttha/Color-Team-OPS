# Single v0.0.2 target — Purple coordination plan, not release authorization

**Owner intent:** complete the requested capability set under one version (v0.0.2), using **internal engineering milestones** rather than renumbering them as v0.0.3–v0.0.6. This plan supersedes Purple's *proposal* for a six-version staging plan, not already owner-locked constitutional rules.

## Current observed foundations (source-bound)
- Existing v0.0.2 design + D1-D5: `design/v0.0.2-team-contracts-single-lane` at `963533265c21b0c0ae05d3d85846d65630593c08`.
- Yellow's isolated host authority reference: `feature/v0.0.2-yellow-host-authority` at `9b3ca3349016749ed4b809932b5a9e930ec3368b`.
- GitHub CI run [41016921417](https://github.com/vixttha/Color-Team-OPS/actions/runs/41016921417) directly observed **260/260 Linux and 260/260 Windows PASS**, plus successful GitHub REST read (result `PROVIDER_EVIDENCE_OBSERVED_ROLE_AUTHORITY_UNVERIFIED`). This is reference/development evidence, **NOT production consent, real model-role independence or hosted issuer state**.
- Prior research/36 concepts: `research/nine-team-role-audit-2026-10-30` at `b59bd2b7fa289b77cec7f9c2f42eedfcccd2449a`.
- This branch is solely the new Ideas and Feature Registry candidate, built from research baseline, **not from Yellow branch**. No silent merge/integration.

## One version, five bounded internal milestones
| Milestone | Owner / work | Required deliverables | Exit tests and evidence | Downside / mitigation |
| --- | --- | --- | --- | --- |
| M1 — Mergeable trust foundation | Yellow implementing with Head dispatch; Purple review | Reconcile D1-D5 policy/evidence with Yellow host-engine interfaces, versioned state, audit envelopes, replay/revocation and exact consent | Exact final candidate SHA CI + negative cases, controlled sequential mission; honest missing-host status | Integration conflicts; pin base SHA and test |
| M2 — Team awareness and registry | Yellow implementing, Purple cross-role audit | Shared nine-team directory, versioned sub-capability IDs, triggers/exclusions/tools and searchable metadata; lazy load the active worker | No team identity remapping; unsupported capability blocks or abstains; no self-permission | Stale/duplicated metadata; single canonical registry |
| M3 — Adaptive Head router + handoff contracts | Yellow under Head; Purple adversarial routing review | OPS Director rules for required/optional/forbidden transitions, typed handoff evidence, risk classification, stop conditions; **D2 authorization remains separate** | Wrong-team, stale SHA, missing evidence, unauthorized/simultaneous worker, source-edit invalidation, handoff budget tests | Rule explosion and duplication; bounded deterministic gate + reason codes |
| M4 — Measured expertise and orchestration | Yellow creates test fixtures, Purple challenges measures | 270 distinct initial specialist scenarios (30/team), routing/handoff/end-to-end test set, holdouts, A/B component ablation, cost/time tracking | Actual independent oracles and traces; no observed critical forged evidence/authorization failures; separate accuracy measures | Test cost/overfitting; frozen oracles, precommitted gates |
| M5 — v0.0.2 integration and ship decision | Head owns acceptance and plugin identity; Yellow build; Purple review; independent release requirement if policy says so | Exact source/package parity for 12 skills, v0.0.1 backward compatibility, supported ChatGPT tool trials, complete decision/evidence ledger and owner sign-off | NO merge or publication until actual exact-SHA test + permission + release evidence; unsupported operations remain UNVERIFIED/CAPABILITY_BLOCKED | Scope/launch inflation; split safety mode from unverified optional production mode |

## One-release rule does not mean false feature certification
**Base skill-first v0.0.2** can be released only with features it actually supports in the intended host. Stronger **production-authenticated mission completion** requires a real host-issued consent identity, protected cloud issuer, transactional durable revocation/state store and live end-to-end mission through actual trust boundary. **Global cross-chat exclusive writes** additionally need enforced cloud gateway fencing and protected write paths. These are **unproven at this point**; cannot be marked done or silently simulated. If user requires them in v0.0.2, they remain release blockers until a separately authorized cloud implementation and actual tests; no hosting vendor, subscription or user runner may be assumed.

## Source-of-truth map and drift repair
- Historical D0-D7 roadmaps are **historical**; D2/D3/D4/D5 labels were repurposed in executed engineering records. Avoid reusing D labels for the new work. Use **M1-M5** here and maintain a separate current release manifest mapping old D labels to tested SHA.
- `ideas/records` owns brainstorm/research/owner idea status and tradeoffs.
- `features/records` owns distinct candidate feature identity and evidence references; no duplicate mutable release state.
- `policy_v002` and contracts own actual code, state and provenance semantics.
- Release documents/Head owner acceptance own release inclusion/version.
- `research/` and this docs file do not override v0.0.1 constitution or authorize the next worker.

## Hard compatibility / role invariants
Exactly 9 specialists (Yellow, Orange, Green, Red, Blue, Purple, White, Black threat intel, Gray Cell), 3 coordinators (Mission Control, OPS Director, Verification Gate); no Gold team and no fourth skill. Single Head → one active Worker → Validate → distinct Internal Auditor → Head. White governs exercise rules, Purple correlates attack/defense, neither becomes generic mandatory Auditor. No host, platform, Vercel/Supabase, GitHub runtime, user runner, local CLI or paid service mandated. Release and PR merge require owner authorization. Source SHA changes invalidate/re-establish affected checks.

## Purple review responsibilities
Review specialist routing and attack/defense correlation, challenge handoff omissions, contradictory authority claims and the nine-team directory. Purple's recommendation is not a Head command, an independent authenticated human review or v0.0.2 release acceptance. Yellow's existing implementation branch remains untouched.

## External Governance origin and distinctions
- Ideas Library lifecycle and schema (observed): https://github.com/vixttha/Governance-Branch-Bible/blob/ideas/universal-progress-and-reuse-intake-2026-10-12/docs/IDEA-LIFECYCLE.md
- Canonical idea records / generated views: https://github.com/vixttha/Governance-Branch-Bible/blob/ideas/universal-progress-and-reuse-intake-2026-10-12/ideas/README.md
- **Feature Registry is PROPOSED in Governance**, not released: https://github.com/vixttha/Governance-Branch-Bible/blob/planning/governance-feature-inventory-2026-10-26/docs/product-candidates/FEATURE-REGISTRY-DESIGN-CANDIDATE.md
- Governance project's own Ideas/Decisions/Roadmap/Releases are separate authority domains; Color-Team-OPS does NOT install or depend on Governance runtime.
