# Purple Review HQ — Four optional capabilities, explicitly outside v0.0.2 release scope

**Record date:** 2026-11-04  
**Classification:** owner-requested documentation of discussed future capabilities; NOT development authorization, owner approval to implement, change of source policy, vendor choice, deployment, security grant, or release decision.  
**Product:** Color-Team-OPS (the existing nine specialists and three coordinators).  
**Source of current technical truth:** [v0.0.2 master Issue #8](https://github.com/vixttha/Color-Team-OPS/issues/8), not the historical idea status fields.

## Decision table (owner-requested preservation)

| Capability | Required for skills-only v0.0.2? | Disposition |
| --- | --- | --- |
| One-action Mission Planner & Launcher | **No** | **Valuable future feature**; captured as `IDEA-000037`, not authorized for implementation |
| Idea & Feature Library | **No** | **Keep as an optional research resource**; separate from runtime and release |
| Protected-host infrastructure | **No** | **Valuable when stronger enforcement is needed**; only an optional separately approved cloud architecture |
| Additional autonomous specialist execution | **No** | **Larger architectural investment**; research/design only, not a claim about existing v0.0.2 |

**Owner's request here is to DOCUMENT the distinction.** This is NOT permission to add a 13th skill, turn the 37 ideas into mandatory deliverables, build a host service, change permission scopes, enable agent autonomy, or change v0.0.2's accepted source/plugin payload. The current skills-only release requirements remain governed by the existing Issue #8 gates and final explicit owner decision.

## 1 — One-action Mission Planner & Launcher

**Canonical concept:** [`IDEA-000037`](../ideas/records/IDEA-000037.json); [detailed original design](IDEA-000037-ONE-ACTION-MISSION-PIPELINE.md).

**Future envisioned user flow:** one plain-language project request → editable milestone/task/dependency plan with acceptance criteria and candidate color-specialist assignments → explicit owner scope selection and a “Work on this” action → a bounded, sequential **Head → Worker → Validate → logical Internal Auditor → Head** mission → visible progress, task evidence, blocks, and justified team returns. Owner must still approve privileged deployment/publishing/fees/offensive test scope.

**Existing v0.0.2 is narrower:** its installed skills include Mission Control, OPS Director, Verification Gate, specialist routing instructions, a metadata directory, and logical task guidance. They do not establish a finished interactive plan editor, one-click launcher, persistent cloud execution engine, cross-chat authenticated identity, or unattended ongoing work.

**Decision:** Keep IDEA-000037 `captured / not_planned / untested`, not a mandatory v0.0.2 feature. Any future implementation needs a separate owner authorization, concrete host/UI capability model, finite budgets, no fabricated approvals, and dedicated acceptance cases. Avoid duplicating already implemented one-prompt Head routing.

## 2 — Optional Feature & Idea Library

**Canonical materials:** [37 IDEA records](../ideas/INDEX.md), [five candidate FEAT umbrellas](../features/INDEX.md), [current engineering reconciliation](V002-FEATURE-IDEA-CURRENT-STATUS-2026-11-04.md), and [standalone blank reusable starter](../portable/v0.0.1/README.md).

**Purpose:** a provenance-aware product research memory for benefits/tradeoffs, alternatives, overlap, proposal lifecycle, real source evidence, evaluation and release status; NOT the actual plugin execution engine, Head grant, host verifier, release signer, or mandatory dependency. Historical records may legitimately read `not_planned/untested` even if separate current software source now implements related guidance. Read the dated overlay to avoid confusion.

**Boundary:** the installed 32-file staging package contains no `ideas/`, `features/`, or `portable/` runtime files. The separate Purple library branch must remain optional. Its own portability/schema/index/UX work can be validated separately, but **must not block v0.0.2 initial Smoke A/B**. Do not copy this catalog into unrelated projects; use the empty portable starter.

**Decision:** Retain library and historical IDs; do not merge the entire Purple branch into the core plugin, set library data as permission, or add library quality milestones to the v0.0.2 mandatory release gates without owner direction.

## 3 — Protected-host infrastructure (stronger external enforcement)

**Canonical existing research:** [`IDEA-000032`](../ideas/records/IDEA-000032.json) optional authenticated authority/leases/fencing and [`FEAT-000005`](../features/records/FEAT-000005.json), whose *reference code* must not be mistaken for a deployed security service.

**Possible future enforcement:** independently authenticated owner consent and capability scopes; protected issuance and revocation; durable mission state; cross-session ownership arbitration; protected write gateways with fencing tokens; evidence provenance checked by a real host rather than only model narrative.

**Critical difference:** Markdown/JSON skills can *instruct* the model to respect permissions, but cannot themselves issue trusted user grants, authenticate distinct reviewers, prevent direct writes across unrelated sessions, enforce revocation or guarantee global exclusivity.

**Decision:** Optional, not required for approved portable skills-only v0.0.2. A future service would require explicit owner architecture/budget/provider choices, authentic security testing, and replaceable cloud adapters. No user-owned runner, personal server, one hardcoded cloud provider, or paid platform is a default runtime requirement.

## 4 — Additional autonomous specialist execution

**Related existing concepts:** [`IDEA-000037`](../ideas/records/IDEA-000037.json) planning/launch UX; [`IDEA-000017`](../ideas/records/IDEA-000017.json) single-lane bounded repair; [`IDEA-000036`](../ideas/records/IDEA-000036.json) cross-thread handoff context.

**Potential future architecture:** separately instantiated and authenticated specialist execution identities, durable cloud task queue/state, permitted continuing work after a conversation ends, controlled observation and recovery, real independent review where claimed, and explicit owner-controlled budgets/revocation. If designed, it must retain **nine specialist roles, three existing coordinators, one active Worker per mission, Head ownership, and human authority for privileged actions**.

**Current reality:** The installed staging plugin is skills-only. Role names, JSON envelopes, ChatGPT model narration, or different ChatGPT threads do **not** prove multiple independent connected agents, durable background execution, externally enforced mutexes or authorization. A portable skill can provide useful in-conversation logical handoffs without these features.

**Decision:** A larger future research/architecture track; not required or approved for v0.0.2 and not an implicit dependency of the One-action planner. A new IDEA ID or FEAT ID should be created only after explicit scoped proposal intake, not by silently changing historical catalog counts here.

## Scope versus real release gates

| Already in accepted source / current stage | Still required for v0.0.2 release evidence | **Not** required by this decision |
| --- | --- | --- |
| Cloud-only portable skills; 9 specialist teams; 3 coordinators; role guidance; stage 0.0.5 for product target v0.0.2 | Genuine ChatGPT staging Smoke A/B with host receipts; H scenario criteria/host trials; independent semantic evaluation/oracles and holdout treatment; final source/host audit and owner promotion decision | One-click UI/launcher, optional library runtime, protected host service, unattended background/multi-agent execution |

**Do not weaken original release requirements.** The current Issue #8 state remains `RELEASE_BLOCKED`; source/CI readiness is not host functional acceptance. This document changes NO staging release, canonical plugin, runtime source, owner permissions, GitHub Actions, release status, historical JSON record state, or FEAT membership.

## Evidence and revisit criteria

When reconsidering any future capability, require a new bounded owner scope decision and record: intended behavior, external service/tool needs, cloud-only/provider-neutral fit, threat and cost model, measurable host acceptance, migration/rollback, and relationship to existing 12 skills. No future concept may be declared shipped from a research Markdown or a synthetic test.
