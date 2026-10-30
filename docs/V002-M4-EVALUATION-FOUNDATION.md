# CTO-V002-SINGLE-THREAD — M4 evaluation foundation

**Status:** executable evaluation **infrastructure**, NOT 270 completed specialist evaluations or a quality score. **Worker:** Yellow. **Milestone:** M4 of ONE v0.0.2 release.

## What was implemented

`policy_v002/eval_lab.py` defines provider-neutral case/oracle/trial contracts, source-SHA and oracle digest binding, two injectable independent proof interfaces, deterministic correctness/incorrectness/critical safety scoring, no duplicate case IDs counted as independent, and batch scoring with mandatory `SAMPLE_ONLY_NO_GENERALIZATION`.

`planned_slots()` returns **270 distinct UNLABELED placeholders**: 9 teams × (10 normal + 10 edge + 10 adversarial). It deliberately supplies no expected answer, user identity, actual task performance, provider trace, experiment host or model, and therefore **does not represent 270 actual evaluated cases**.

`score_case()` returns `UNVERIFIED` when the trusted oracle or provider observation is unavailable or mismatched; test doubles in the Python suite are synthetic and cannot authenticate real oracles. The `aggregate()` function refuses duplicate samples, blocks observed critical violations, and always labels even 270 caller-provided all-correct rows `SCORED_AWAITING_INDEPENDENT_ACCEPTANCE`, not `99% achieved` or release-ready.

The source remains cloud-only/provider-neutral with no new runtime skill, user-owned runner, Vercel/Supabase dependency, paid experiment or live AI-model invocation.

## Test design

`tests/test_v002_eval_lab.py` includes 25 deterministic fixture cases covering exact slot counts, per-team/stratum distribution, empty/unverified oracles, wrong SHA/ID, manipulated oracle digest, forged/failed observations, incorrect/forbidden outcomes, duplicate trials, critical safety override and non-generalization of 270 synthetic all-correct scores. The test harness does not provide an independently reviewed performance corpus or real specialist quality evidence.

## M4 unfulfilled exit gates

The [Purple routing evaluation plan](https://github.com/vixttha/Color-Team-OPS/blob/feature/v0.0.2-idea-feature-library-purple/research/09-ROUTING-ACCURACY-EVALUATION-PLAN.md) still requires 270 **actual different, independently labeled specialist cases**, authorized real host/model trials, protected/source-bound recorded traces, holdout independence, paired ablations and preregistered promotion thresholds. No genuine 99% performance assertion, one-sided confidence guarantee or full mission success claim is supported by the current code. M4 development scaffold can be reviewed, but M4 full acceptance must remain INCOMPLETE.

## Interaction with M5

Do not merge, publish or create cloud services merely because this lab works. M5 must independently verify release/package/skill parity, backward compatibility, actual same-host trials, owner permission and trusted production authorization. If real production authenticated mission mode is a mandatory v0.0.2 requirement, the release is BLOCKED until a replaceable protected cloud host provides that evidence.
