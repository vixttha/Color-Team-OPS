# CTO-V002 — Owner-ordered acceptance ledger: ChatGPT Smoke A/B LAST

**Order locked at owner request:** 2026-11-04. **Review branch:** `review/v0.0.2-pre-smoke-acceptance`. This is a read-only acceptance/reviewer sidecar to the already accepted plugin payload. No runtime feature requests, permission updates, host assumption, staging or canonical publication.

## Exact accepted source/runtime binding

- Functional source Git SHA: `0e9561fd06034674eca4fcf07ceef9381f8249a2`; direct installed-vs-source text equality independently reconfirmed for all **29/29** functional files.
- Current docs/test SHA: `42d79e31ecd510d8c4fb3a49eb98a6ff509a68c4`; source integration branch unchanged, native self-hosted Windows and Linux 979/979 PASS per OS from Actions run [41874707174](https://github.com/vixttha/Color-Team-OPS/actions/runs/41874707174).
- Current PRIVATE staging: `plugins_6ae9238966508191b3402640e65217bf`, private iteration `0.0.5`, release `pluginrel_6aea9f63eee88191ba42a906ae04049d`, **product target v0.0.2**. Canonical private v0.0.1 is unchanged.
- Smoke candidate text: strictly `candidate_input_exact.SMOKE_A` and `.SMOKE_B` in `evaluation/v0.0.2/SMOKE-PROMPT-FREEZE.json`. No evaluator instructions or expected roles in candidate input.

## Mandatory sequence

| Sequence | Gate | Current observed state | Exit requirement |
|---|---|---|---|
| 0 | Accepted core source and staging integrity | **PASS** — no source-change permission needed | Preserve source and identity; if a real repair later changes functional files, repeat affected exact-SHA tests/parity |
| 1 | H-01…H-11 pre-output criteria | **PURPLE_TEXT_CRITERIA_11/11 PREPARED** ([sidecar rubric](H-CASES-PURPLE-PREOUTPUT-REVIEW-2026-11-04.md)); hosted skill/identity proof unverified | Rubric frozen before candidate outputs; preserve text vs tool/skill provenance boundary |
| 2 | 270-case oracle certification | **0/270 authenticated independent approvals**; 270 source drafts inspected ([quality/holdout audit](270-CASE-PURPLE-SOURCE-AUDIT-AND-HOLDOUT-PROTOCOL-2026-11-04.md)) | Case-specific independent reviewer decisions+pre-output digests and genuine reviewer evidence for all required cases |
| 3 | 54 source-visible holdouts | **54 nonblind, 0 genuinely blinded** | Secure fresh hidden independent set OR explicit owner-authorized disclosure of a changed nonblind acceptance policy; do not silently weaken original requirement |
| 4 | Genuine model trials, paired baselines and ablations | **0/270 domain cases executed, 0 accepted paired results** | Authorized model/host/tool access, frozen per-case criteria, authentic receipts, controlled costs; determine real critical violations |
| 5 | Genuine H-01…H-11 host scenarios | **0/11 NOT_RUN** | Authentic private staging-enabled host responses and source-bound grading; do not promote role narration to host skill activation |
| **6** | **CHATGPT SMOKE A AND B — FINAL FUNCTIONAL TEST** | **0/2 NOT_RUN** | Genuine two fresh private staging-enabled ChatGPT sessions; unchanged exact frozen candidate prompts; complete transcripts, actual skill/tool evidence where visible; independent Purple grade. If earlier tests result in source repairs, reverify and then rerun Smoke LAST |
| 7 | Final release assessment / owner sign-off | **RELEASE_BLOCKED** | Final Purple evidence audit and separate explicit owner decision; no implicit merge or official plugin update |

**Important:** Final Smoke is last **test**, not the last governance step. Owner approval/release operations remain later and separate; no automatic publication.

## Blockers that cannot be converted to source-only PASS

- **Authentic independent oracle and holdout custody:** the current reviewer/producer distinction needs actual identifiable separate approval; current ChatGPT logical reviewer narrative is insufficient. 54 current holdouts cannot become blind retroactively.
- **Authorized model execution:** neither existing CI runners nor an installed skills package alone produce 270 independently observable model replies or four-arm evaluations. Any new model/usage bill or credential change needs explicit owner approval.
- **Actual private ChatGPT host execution:** the current connected GitHub and Plugin Creator APIs can inspect sources/install metadata but cannot send messages into new staging-enabled ChatGPT conversations. Do not use ordinary assistant replies as substitutes or demand a particular UI mode as product dependency.
- **Native test trigger scope:** existing exact-SHA owner-runner CI runs only for commits to `integration/v0.0.2-master-single-thread`. This separate review-only branch does not claim a new Windows/Linux run; accepted integration branch was intentionally not edited.

## Operational handoff policy

Issue #8 is the authoritative live handoff ledger. Its top anti-drift state and the already configured hourly Color OPS Acceptance Pipeline were updated to respect this order. This review branch contains only supplementary reviewer criteria and quality findings, never alternative canonical plugin source.

Use single lane Head → one Worker → Validate → logical Internal Auditor → Head; freeze accepted source, keep all unsupported gates `NOT_RUN` or `UNVERIFIED`, suppress repeat blocker comments, use owner self-hosted runners only for allowed *development* testing (not runtime). No outside products, new meta prompts, new teams/coordinators, paid hosted runners, local compute dependency, new staging identity, protected host infrastructure, publication or main merge.

**State:** `PRE_SMOKE_PREPARATION_ADVANCED; INDEPENDENT_ORACLES_AND_REAL_TRIALS_OUTSTANDING; CHATGPT_SMOKE_DEFERRED_TO_LAST; RELEASE_BLOCKED`.
