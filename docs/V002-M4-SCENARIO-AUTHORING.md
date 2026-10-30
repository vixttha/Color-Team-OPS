# Issue #8 / M4 — 270 distinct draft specialist scenario specifications

**Scope:** one v0.0.2 release mission, Yellow infrastructure assignment.
**Artifact:** `evaluation/v0.0.2/candidate-scenarios.json` (source-committed candidate dataset, NOT independently reviewed/approved oracle).

## Progress beyond empty slots

The existing evaluation scaffold `policy_v002/eval_lab.py` generated **270 UNLABELED placeholders**. This assignment prepares **270 distinct authored scenario specifications**: 9 specialists × 10 different domain-specific objectives × 3 meaningful bands (normal, edge, adversarial). Each specifies a concrete specialist task prompt, proposed success criteria, proposed critical failure, authorization setting and intended source/evidence discipline. They cover distinct engineering, AppSec, cloud, authorized adversarial, defensive operations, cross-team correlation, exercise governance, dated threat-intelligence and human-factors domains.

The content is **model-authored case specifications**, not measured specialist performance. Every record intentionally has `label_status=DRAFT_NEEDS_INDEPENDENT_ORACLE`, `outcome_status=NOT_RUN`, `independent_reviewer_ref=null`, `oracle_digest=null`, `held_out=false`, empty observed provider receipts and synthetic/no-external-target scope. The proposed criteria are not frozen independent labels. No hidden holdout, tool/model trial, baseline comparison, ablation, statistical confidence interval, or quality score was produced.

`tests/test_v002_case_candidates.py` contains **11 authored structural tests** for counts, diversity, safety, not-run status, no forged labels and no fabricated 99% claim. Actual native test execution and independent human/oracle adjudication must be recorded with separate evidence and source SHA.

## Next required independent M4 acceptance

1. Freeze each case's independent oracle and versioned expected outcomes **by a reviewer distinct from the model generating these proposals**; preserve holdouts outside the candidate-producing source where supported.
2. Execute approved real model/host/tool tasks with authenticated provider receipts, exact revision, capability context, refusals and budgets.
3. Compare v0.0.1 baseline to v0.0.2 candidate, run source-bound ablations and classify each of nine specialties separately.
4. Report measured correctness, necessary/unnecessary specialist routing, mission handoffs, gate integrity, critical violations, costs/tokens/latency actually observed, confidence and failure recovery.
5. Do not assert 99% or release readiness from fixture outcomes.

**Head and verification:** these artifacts are **draft scenario authorship**, not acceptance of M4's mandatory independent real evaluations. No cloud provider was provisioned and no owner-owned runner or real third-party target was used.
