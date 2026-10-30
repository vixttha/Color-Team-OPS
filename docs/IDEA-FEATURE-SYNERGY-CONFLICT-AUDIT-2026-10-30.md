# Purple Team — source-linked 36-idea / 5-feature synergy, status and conflict audit

**Observed:** 2026-10-30. **Audit source:** all 36 `ideas/records/*.json` and five `features/records/*.json` read at Purple SHA `2c150833867d506f3fb622a0d0e19f9c5330d5f8`; actual v0.0.2 master `integration/v0.0.2-master-single-thread` SHA `984ba437bae41f26b2ade703c704ffcd1c8347ba`; later Yellow repeated-worker repair SHA `72d09023f9edc29638f26d734262905346069bb3` (NOT merged into this reviewed master). No new model/provider skill execution was observed. The library's earlier source SHA remains original provenance, not today’s engineering status.

## 1. Count, identity and provenance (verified)
- **36 ideas**, sequential `IDEA-000001` … `IDEA-000036`, originally mapped to `F01`…`F36`. **Five are marked adopted as *idea directions***: F01, F02, F06, F09, F20; the other 31 are captured. All 36 still have `implementation_status=not_planned` and `testing.status=untested` from the frozen import.
- **5 umbrella feature proposals** `FEAT-000001` … `FEAT-000005`; all carry `lifecycle_status=proposed`, `implementation_status=not_planned`, `release_membership=NOT_ASSERTED`, no feature-level verified evidence.
- **27 unique idea IDs referenced** by the five features; **9 NOT referenced**: F15, F27, F28, F29, F30, F31, F34, F35, F36. These are not automatically missing requirements; several are product laws, evaluation controls, developer workflow options or historical status.
- **47 original library files** were imported byte-for-byte into reviewed master, but import is not runtime use nor release approval. `main` and v0.0.1 source do not include this library.
- The five features summarize bundles; counting five does **not** discount existing v0.0.1 12 skills, M1–M5 code or earlier D1–D5 development.

## 2. How ALL 36 ideas work together if selected

| Layer | Original ideas | Composition | Status vs reviewed master |
| --- | --- | --- | --- |
| A — User, Head and safety constraints | **F10, F17, F18, F19, F31, F32** | Provider-neutral host boundary, checked consent, scope, permission, one-worker budget, release stop, *optional* protected issuer/gateway | M1/Yellow reference exists; actual hosted production issuer, durable tenant ledger and global writes NOT verified |
| B — Nine specialist knowledge and retrieval | **F02, F03, F04, F05, F25, F34** | Single nine-team directory with owned capability IDs, optional focused sub-specialty guides, lazy worker context, nine performance profiles and solo-developer examples | Directory has 9 teams/18 metadata capabilities; separate sub-specialty packs and per-team measured skills NOT proven |
| C — Head-controlled adaptive selection | **F01, F07, F08, F09, F11, F12, F30** | Task/risk classifier → eligible capabilities → permitted next Worker/STOP with reasons; 17 routing scenarios are examples, **not a forced sequence** | OPS Director advisory router exists; actual hosted automatic dispatch not verified |
| D — Team communication and source-proof | **F06, F13, F14, F15, F16, F33, F36** | Typed handoff and completion, exact task/SHA evidence, independent provider observation and logical Internal Auditor, source-stamped cross-thread handoff notes | Schemas/verifier/GitHub reader and logical gate exist; provider account attribution ≠ independently authenticated team roles; master M1 bridge supports only one audited task |
| E — Real evaluation, efficiency, promotion | **F20, F21, F22, F23, F24, F26, F27, F28, F29, F35** | Independent specialist + routing oracles, baseline/candidate/ablation, per-risk reliability, critical-error gate, budgets, safe promotion/rollback, feedback corpus and real DORA-like outcomes | 270 **unlabeled slots**, no real 270-case execution, no validated 99% claim, no real delivery metric/promotion proof |
| Product-independent research support | **F01–F36 as historical idea records** | This optional library can compare/remember them and record source references without being loaded into every mission | Isolated Purple branch exists; not a v0.0.2 runtime prerequisite |

**Interaction diagram:** `Owner scope/Head & host gates (A) → compact directory (B) → advisory router (C) → ONE authorized Worker → typed handoff/provider evidence/logical Validate+Audit (D) → Head decision`. Layer E tests and improves this loop; the *optional library* stores product-design thinking alongside it. No FEAT or IDEA file may grant tools, change host scope or self-promote a release.

## 3. Five feature umbrellas and nine unlinked ideas

| Existing feature | Idea coverage | How it works with other features | Status |
| --- | --- | --- | --- |
| **FEAT-000001** Directory/Capabilities | F02–F05 | Supplies read-only, bounded matching data to FEAT-000003 and context to FEAT-000004 | Prototype on master; host behavior unverified |
| **FEAT-000002** Typed Handoffs | F06–F08, F13 | Source-bound Worker→Gate→Head data consumed by FEAT-000003 and validated against FEAT-000005 trust | Draft contract/reference |
| **FEAT-000003** Adaptive Head Routing | F01, F09–F12 | Candidate ranking is only used after Head authorization and uses FEAT-000001/002 | Advisory only |
| **FEAT-000004** Evaluation Lab | F20–F26 | Evaluates specialist quality, safe routing, synergy and evidence correctness across FEAT-000001–003/005 | Scoring fixture; no actual 270-case evaluation |
| **FEAT-000005** Host Authority Reference | F14, F16–F19, F32–F33 | Governs trust/consent and provider evidence for all other modules; current prototype is deliberately read-only | Synthetic reference, no deployed issuer |
| **No FEAT link (cross-cutting)** | F15, F27–F31, F34–F36 | Internal Auditor semantics, budgets, promotion/recovery, feedback, scenario examples, product law, playbooks, DORA outcomes, handoff continuity | Preserve as design requirements/options; link only if the owner chooses an actual feature work order |

## 4. Cross-idea / cross-feature conflict register

| ID and severity | Conflict or tension | Actual reconciliation/acceptance |
| --- | --- | --- |
| **C01 P1**: F01/F09 vs F30 | Dynamic Head selection **conflicts** with treating scenario routes as mandatory fixed team order | Treat 17 scenario families as test fixtures and onboarding examples; route using current evidence and risk; benchmark when stopping is correct |
| **C02 P1**: F07/F10/F18 vs F27 | Cost/latency optimization **must not override** mandatory security, evidence or permission checks | Safety/authorization constraints before ranking; if budget cannot cover a mandatory check, BLOCK rather than silently skip it |
| **C03 P1**: F09/F11 vs F10/F14/F32 | Advisory model ranking cannot own authorization or mint trusted Head dispatch | D2/host gate exclusively verifies grants; only Head directs the selected Worker; route output always advisory until a trusted host executes it |
| **C04 P1**: F15 vs F14/F32 | A “distinct internal auditor” in one LLM conversation is **logical separation**, not a separately authenticated external person | Two separately recorded checks and re-observed source evidence; never claim independent human/host role identity without external attestation |
| **C05 P1**: F31 vs F32/F33 | Platform-neutral product would conflict with requiring one cloud provider or owner runner for every mission | Protected issuer/storage and GitHub evidence are optional replaceable adapters/modes, not mandatory hosting dependencies; stronger claims block absent actual host proof |
| **C06 P1**: F17/F08 vs F27 and FEAT-000002/003 | Dependency cycles and repeated handoffs risk infinite or duplicate team execution | Finite Head budget; visited task IDs; no parallel Worker; bounded repairs and no-progress detection; new task on same team permitted only within consented limit |
| **C07 P1**: F20/F21/F24/F26 | A 270-slot lab or a high average score can be falsely sold as 99% confidence or zero future safety failures | 270 are unlabeled placeholders; freeze genuinely independent test cases, risk strata, holdouts and confidence; zero *observed* critical failures only |
| **C08 P2**: F04/F05/F06/F36 | Lazy specialist context can hide critical handoff details and decision provenance | Fetch lightweight metadata first; load current Worker plus mandatory bounded evidence/decision context; never drop required safety or trace fields for token savings |
| **C09 P2**: F03/F04 vs exactly nine workers | Sub-specialist packs and capability IDs could be misread as extra color agents, a fourth coordinator or permissions | Subspecialties are *metadata and scoped checklists under existing nine IDs*, not new agents or OAuth grants |
| **C10 P2**: F16/F28/F29 | Evolving implementations/feedback can cause stale SHA-backed tests and scorecards to be reused | Snapshot each trial and evidence by exact revision, host/model version and case source; revalidate affected results after change |
| **C11 P2**: F23/F28/F29 | Feedback-driven tests and published scorecards can contaminate hidden holdout oracles or leak private experience | Separate public training corpus from protected blinded holdouts, minimize sensitive data, record consent and restrict exposure |
| **C12 P2**: F28/F19 and library feature statuses | “Promoted” feature score or `verified` library state could be mistaken for an approved plugin release | Feature/idea records only reference external owner-controlled release manifest; no automatic deployment or status promotion |
| **C13 P2**: F33/F14 vs F32 | Authentic GitHub account read is not equivalent to signed Head/Worker/Validator grants | Distinguish observed provider data, consent issuer, role attestation, revocation ledger and actual host-mediated operation |
| **C14 P2**: F34/F30 vs F01/F07 | Beginner playbooks may be mistaken for mandatory team sequences or omit escalation | Mark as illustrative/conditional; Head dynamically checks mission context and mandatory specialist gates |
| **C15 P2**: F35/F22/F27 | DORA/latency/cost improvements may drive metric gaming or shortcuts | Treat delivery metrics as secondary observational measures with baseline/case-mix context; never overrule safety gates |
| **C16 P2**: F36 vs one-thread mission | Cross-thread handoff could imply background continuation or ownership transfer across threads | It is source-stamped restart context only; each new Head checks tools, grants, current SHA and budgets afresh |
| **C17 P1**: optional library vs master import | A library copied into the integration candidate could accidentally be treated as a mandatory v0.0.2 product/runtime dependency | Confirm runtime functions without `ideas/`, `features/`, `portable/` or Purple docs; final package can exclude them; library acceptance separate |
| **C18 P2**: historical state vs current development | Original 36 say `not_planned/untested`, F31 says `captured` despite **CTO-LOCK-001**, and F14/F15/F17/F33 now have partial reference code | Preserve original proposal records as historical evidence; add current dated observation snapshots; do not change human approval and claim status from repo code alone |
| **C19 P2**: portable library vs initial schema | Original idea schema requires Fxx origin IDs, feature schema requires M1–M5 and literal `NOT_ASSERTED`, validator hardcodes 36/5 | Keep original historical schema for source records; use independent `portable/` generic schemas/templates and empty catalog; full schema validator and cross-project tests remain separate acceptance work |

**Classification:** C01–C07 and C17 are genuine *incompatibilities if both sides are interpreted as mandatory authority/flow*. They are **resolvable design constraints**, not proof that the owner approved contradictory rules. C08–C16/C18–C19 are integration/data-model tradeoffs. No evidence was found that all 36 ideas are approved features or 36 separately executable agents.

## 5. Fresh status by area, derived from separate source

| Theme | Idea-level source state | Current evidence on other branch | Remaining |
| --- | --- | --- | --- |
| F01/F02/F03/F05/F09 | 4 adopted/mostly captured; all `not_planned` historical | M2 `team_directory.py`; M3 `route_advice.py`; exactly nine worker metadata IDs | Real host-use/behavioral tests, routing measurement |
| F06–F08/F13–F18 | Captured/adopted; all `untested` historical | D1 schemas, M1 bridge and Yellow runtime exist; logical two gate phases | Full multi-task bridge, role attestation, exact full-source tests |
| F17 repeated-team budget | `not_planned` historical | Later Yellow SHA `72d090…` passed 263/263 Windows & Linux; **not in reviewed master** | Integrate and test on master exact SHA |
| F20–F26 | F20 adopted idea direction; all `untested` historical | M4 `eval_lab.py` has 270 **unlabeled slots** | Real labeled case/oracle/model/tool trials, scorecards and ablations |
| F27–F30/F34–F36 | Captured; unlinked to initial five feature bundles | Historical budget, routing scenario, handoff docs/reference exist | Determine owner-selected feature vs docs/research status, avoid runtime mandates |
| **F31 provider-neutrality** | **Captured/not_planned historic metadata is stale** | Owner-locked CTO-LOCK-001 exists in master `docs/23-CTO-LOCK-001-CLOUD-PROVIDER-NEUTRALITY.md`; neutrality tests documented | Treat law as binding regardless of library lifecycle metadata |
| F32/F33 | Captured/not_planned historical | D3/D5 GitHub observations and Yellow synthetic authority reference | Real protected hosted issuer not established; provider neutrality preserved |
| All five FEAT records | `proposed/not_planned/NOT_ASSERTED` with no verified receipts | M1–M4 reference modules **exist** in master, not linked to feature-level live status | Explicit current evidence link and acceptance; do not silently label shipped |
| Actual private plugin | Not a library record | Canonical Creator product verified v0.0.1 in prior release audit; master source says `0.0.2` but unpublished | Official Creator release/version verification at actual release time |

## 6. What to update without falsifying history

1. Use THIS dated audit as the current evidence overlay; previous `ideas/records` import is a frozen **idea source**. Any future owner decision gets a new provenance entry and explicit editor identity.
2. Make separate **current engineering observations** for implementation, host tests, security audit and release status. Never infer approved release from JSON or CI alone.
3. Make library stand-alone and blank-initializable using independent `portable/` generic schemas/templates. Do not let old project-specific `tools/check_idea_feature_library.py` decide portable-project validity.
4. Require an **absence/portability test** at product release: core still works if this optional library is missing; no hidden dependency.
5. Correct the previous `planning/v0.0.2-complete-release-pipeline-2026-10-30` release plan’s blanket “36 mandatory feature links” interpretation: all original ideas remain *auditable*, but only owner-selected actual features are release gates. Library adoption is never a requirement by itself.
6. Before promoting a selected FEAT idea into implementation status, obtain exact current engineering source SHA + actual tests/host observations. Independent challenge is separate from model self-report.
7. The operational product can **consult the optional library only when connected/readable and when task relevance warrants**. Unavailable library must not block Head/Worker/Validate/Audit mission completion.
8. Avoid new external providers or permanent background monitors without an independent grant. Keep the master execution branch and released v0.0.1 untouched.

## 7. Purple verdict

**Source integrity: CONFIRMED** (36 ideas, 5 umbrellas, five adoption-direction flags, unlinked list).  
**Current implementation statuses: HISTORICAL SNAPSHOT, NOT LIVE TRUTH.**  
**Conflicts: 19 identifiable conditional interaction and data-boundary issues; no permission to resolve by ignoring constitutional gates.**  
**Library isolation: REQUIRED / OPTIONAL-BY-DESIGN**; 47 historical files were already copied to master, but not established as required runtime components.  
**Live 270-case quality, real production auth, general host support: UNVERIFIED.**  
**Native suite / independent external security acceptance in this audit: NOT EXECUTED.**

Next scoped acceptance: review generic portable schemas and blank templates with a fresh-project trial; no release or product merge required.
