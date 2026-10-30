# Issue #8 — M4 Yellow scenarios / Validate / Internal Auditor / Head

**Reviewed source commit:** `109e1b35774173bfa6523706e95295d97f6645d5` (master v0.0.2 integration branch).
**Worker:** Yellow evaluation-infrastructure authoring only.

## Validate

An exact-source GitHub tree and file-range inspection verified the new `evaluation/v0.0.2/candidate-scenarios.json` is a 357,771-byte source blob (`f7e4c8e4eb597b38f390a36cc9f94449c15b8430`). The metadata declares `count:270`, `DRAFT_UNLABELED_NOT_EVALUATED`, no oracle authority, and individual case records with `label_status:DRAFT_NEEDS_INDEPENDENT_ORACLE` and `outcome_status:NOT_RUN`. `tests/test_v002_case_candidates.py` has **11 authored tests**, not executed by a native Python interpreter at this SHA.

**Validate result:** `SOURCE_BLOB_OBSERVED`; `270_REAL_LABELED_CASES=NOT_RUN`; `NATIVE_TESTS=UNVERIFIED`.

## Internal Auditor

The case prompts, acceptance criteria and critical-error descriptions are model-written proposals. Their distinct IDs and domain-specific wording are useful **evaluation preparation**, but neither independence of expected outcomes nor actual nine-team model competence has been verified. No pre-registered independent oracle, hidden holdout, run context, host provider receipts, scored failures, paired baseline/ablation runs or uncertainty calculation exists yet. No quality percentage or release promotion can be inferred. A single scenario repeated three times with variants needs distinct contextual objectives to qualify as statistically independent; that remains reviewer-dependent.

**Internal Auditor result:** `M4_EVALUATION_PLANNING_ACCEPTABLE`; `M4_REQUIRED_INDEPENDENT_MEASUREMENT_BLOCKED`.

## Head

M4 remains **incomplete** under Issue #8 despite useful authoring. Continue with Green for independent M5 reproducible-build engineering and cloud-neutral release readiness. This is a capability-based selection: Green handles CI/build/recovery; no Red/Blue/White or forced nine-team chain. Head permits only code+tests+read-only release planning on this isolated integration branch, **not** actual paid CI, self-hosted owner runner, cloud deployment, merge or publication.

**Next assignment:** Green M5 standard-library deterministic source ZIP builder and negative tests for omissions/changed hashes, exact source inventory, optional library absence, no imported credentials. Runtime cloud provider independence remains locked.
