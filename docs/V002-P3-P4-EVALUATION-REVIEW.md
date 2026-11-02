# CTO-V002 P3/P4 — Evaluation corpus and execution audit

**Candidate-only structural preparation, NOT independently frozen or executed.** On 2026-11-02 Purple examined `evaluation/v0.0.2/candidate-scenarios.json`: 270 unique IDs, 90 distinct topic × team combinations, nine specialists, 30 cases per team, 10 normal/10 edge/10 adversarial per team. The original 90 normal-case prompts share a generic boilerplate suffix, and proposed criteria are not a substitute for a source-grounded measurable oracle.

`evaluation/v0.0.2/preregistration-draft.json` now records all 270 candidate IDs, topic-linked structured inputs, intended acceptance criteria, difficulty bands, scenario constraints, preliminary critical-failure definitions, 54 reserved holdout IDs, paired baseline/ablation plan, and source-linked case-inventory provenance. **No independent reviewer/ref/label has been produced. No genuinely blind holdout has been sealed. No model trial has run.** Data remains `DRAFT_NOT_INDEPENDENT / NOT_RUN`. The tentative inputs still require domain-specific artifacts, independently specified expected outcomes and review before freezing; generic refusal checks alone do not measure specialist competence.

### Independent oracle acceptance prerequisites
1. Independent domain reviewers must provide expected outcomes *before* the candidate runs, with immutable digest/reviewer provenance; evaluator and candidate cannot simply be the same model pretending to be independent.
2. Verify unique case IDs and realistic domain-specific fixtures; rework topic-sparse variants and distinguish correctness from generic safe language.
3. Seal holdouts from candidate prompt development; current GitHub-visible allocation is only a reservation.
4. Use the same host, exact version, model effort, permissions and input in candidate/baseline comparisons; record actual model/tool observations and receipts. Preserve objective refusal test cases.
5. Score routing correctness, specialist recall, unnecessary handoffs, evidence honesty, critical authority errors, mission completion and measurable latency/tokens only where exposed. Report denominators and uncertainty by team/band; no unsupported 99% claim.

**P3 disposition:** IN_PROGRESS candidate preregistration, **BLOCKED on independent oracles and genuine blind holdouts**. **P4 disposition:** BLOCKED; independent labels 0/270, actual specialist trials 0/270, true score unavailable, baseline/ablation trials NOT_RUN. Existing `policy_v002/eval_lab.py` is a reference scorer whose fixture tests do not prove specialist quality.

**Validate:** source case inventory and preregistration tests, not an external evaluator. **Logical Internal Auditor:** rejects fabricated independent oracles and treating 270 synthetic slots as observations. **Head:** no release performance claim.
