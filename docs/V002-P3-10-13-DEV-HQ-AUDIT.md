# CTO-V002 Development HQ — Purple P3-10 through P3-13 bounded remediation audit

**Mission:** CTO-V002-SINGLE-THREAD. **Branch:** `integration/v0.0.2-master-single-thread`. **Separate Purple Review HQ verdict:** [Issue #8, comment 6593250610](https://github.com/vixttha/Color-Team-OPS/issues/8#issuecomment-6593250610). Source producer is Development HQ; this document is NOT a Purple HQ approval. The owner authorized **two exploratory private staging smoke tests**, not a full release.

## P3-10 — Explicit direct rubric records (source improvement, semantic gate open)

`evaluation/v0.0.2/reviewer-case-criteria.json` enumerates all 270 case IDs with a producer-authored base domain decision, exact expected variant disposition, two explicit positive and two explicit fail conditions, fixture identity and context/evidence boundary. Three previously hand-authored Blue P-03 rubric entries are preserved; **267 are newly derived draft criteria from the existing synthetic topic/variant details**. `policy_v002/p3_variant_compiler.py` requires the matching case-ID/fixture-ID/variant/core outcome and fails closed for missing, stale, unapproved or generic fallback criteria. No fallback criteria remain in executable compiler.

**Limit:** These 267 case records are DEVELOPMENT proposals, not 267 individually approved substantive oracles. Rephrasing the existing fixture/expected outcome does not establish expert validity; separate Purple HQ must still judge feasibility, discrimination, factual context and domain-specific grading for certification. Review labels `NOT_INDEPENDENTLY_APPROVED`; no real host results or holdout blinding.

## P3-11 — Detached-score truth boundary

`score_provisional(case, verdict)` now validates case ID, draft grading/variant source, candidate input and exact dimensions. Detached booleans yield `example_math_points` **only**, while `provisional_points` and `actual_trial_score` are always `None`. The returned status is `DETACHED_FLAGS_ONLY_NOT_TRIAL` or `CRITICAL_BLOCKED` if the boolean critical flag was set. No verdict can return `accepted`, `independent_review`, `reviewer_authenticated`, `host_execution_verified`, or `eligible_for_aggregation` as true.

Genuine future output measurement must go through separately observed host traces and `policy_v002/eval_trial_pipeline.py` with case ID, pinned source SHA, installed candidate version, input/output digest, oracle/reviewer refs, tool receipts and external proof adapter. Adapter-only source tests remain provisional; they do NOT independently authenticate actual reviewers.

## P3-12 — Trusted synthetic context updates, not new runtime permission

The previously corrected `gray-cell:edge:01` now states that a *later trusted user message* pins the repository but leaves permission/time unspecified. In addition, `evaluation/v0.0.2/context-overrides.json` supplies ten explicit draft context clarifications across Yellow, Orange, Green, Blue, Purple and Gray Cell. Examples: a new valid form submission is distinct from the earlier invalid one; an unavailable provider may not be cited as a live receipt; a changed token expiration is a separate synthetic edge token; E3 has no UTC evidence even if E1/E2 do; 100/100 one-OS CI does not prove a skipped second OS. Compiler includes these as **trusted SYNTHETIC edge-case updates**, without granting actions or substituting for provider records.

All 90 underlying triplets still require separate semantic acceptance. Adversarial/untrusted statements are **not** treated as trusted scenario overrides.

## P3-13 — Specialist quality cannot be inferred from generic safety

Candidate-facing instruction was shortened to ask for a concrete domain decision and honest uncertainty, without coaching five template output fields. Detached arithmetic reports **domain** example points (base/variant, 0–2) separately from **safety** example points (evidence/authority, 0–2). Safety-only success has domain example points 0 and cannot be promoted to specialist quality. Genuine performance requires independent baseline/ablation and domain correctness, not templated safe wording.

## Regression and release boundaries

`tests/test_v002_p3_review_gates.py` and `tests/test_v002_p3_variant_compiler.py` check 270 source-bound draft entries, distinct variants, context notes, missing Blue event IDs, same-case binding, cross-case replay, variant ignored, safety-only outcomes, and detached false-pass prevention. **Do not claim test PASS until a fresh exact-commit GitHub CI run completes.** Source-only corrections do not touch the installed 32-file runtime payload.

The sole existing PRIVATE v0.0.2 staging identity is `plugins_6ae9238966508191b3402640e65217bf`, release `pluginrel_6ae9238a80008191945e990f8fa87308`, installed runtime source `311290784fe7d5647666f88b328222de62d3cee6`. Canonical v0.0.1 remains untouched. Purple [source signoff](https://github.com/vixttha/Color-Team-OPS/issues/8#issuecomment-6593250610) permits initial two controlled explorations ONLY; this development code does not change the installed plugin.

**Real host gates:** Smoke A/B **0/2 NOT_RUN**; H-01–H-11 **0/11 NOT_RUN**; real specialist outputs **0/270**, independent oracle approvals **0/270**, visible unblinded reserve **54/54**. Current available Developer HQ host tools do not provide a staging-plugin conversation invocation; prior browser observation of ChatGPT was explicitly blocked by host policy and will not be bypassed. An actual staged-plugin conversation must produce literal observed output and a genuine session/tool record before claiming a hosted smoke result.

**Head disposition:** Source remediation candidate for CI and separate Purple HQ reassessment, NOT final P3 certification; release remains `RELEASE_BLOCKED`. No staging clone/update, no official v0.0.2 release, no main merge, no paid infrastructure or local product runtime requirement.
