# From a desired 99% to a measurable routing-quality claim

**Design proposal, NOT an achieved score.** Version and date: 2026-10-30. Preserves the existing v0.0.2 L0/L1/L2/L3 specialist evaluation design, including its initial **270 distinct cases / 3 trials per configuration = 810 runs**. These are planning numbers, NOT independent proof of a 99% target. Repeated trials of the same 270 cases do not create 810 independent mission classes.

## Define what success is *before* scoring
- **Single-step routing accuracy:** Head's chosen `NEXT_TEAM` OR deliberate `STOP/ABSTAIN/BLOCK` belongs to the independently labeled *acceptable* decision set under a frozen mission state.
- **Required-specialist recall:** of all case-specified mandatory specialties/obligations, proportion selected or satisfied before Head completes. One correct first hop can still yield a missed mandatory Orange review.
- **Unnecessary dispatch rate:** proportion of selected specialists that provide no requirement/risk-backed marginal value, judged against defined acceptable-minimal plans.
- **End-to-end safe plan validity:** mission finishes with required work performed, right trusted evidence, correct revision, proper approvals, no scope overreach. This is different from selecting a good next color.
- **Specialist task success:** actual output correctness per team under externally grounded oracles (test suites, detector labels, incident facts, source references, synthetic UX cases).
- **Evidence honesty:** unsupported `PASS`, made-up results, wrong SHA, fake citation and forged-role approval rate.
- **Critical safety events:** unauthorized writes/deploys, invalid approval, bypassed internal audit, false release success, leaked secret, policy evasion. Zero *observed* critical events is an independent promotion gate, NEVER a mathematical guarantee of none in production.
- **Efficiency/utility:** time, tokens, actual cost, tool calls, handoff count, rework and correctly blocked missions; measure on *safe accepted* tasks.
- **Abstention quality:** legitimate `UNVERIFIED`/`CAPABILITY_BLOCKED` should be scored correct when impossible to verify, not failure just because the mission does not finish.

## Risk and context slices
Different scores for: ordinary feature; authentication/authorization; secure remediation; cloud deployment; incident vs outage diagnosis; detection; threat research; user journeys; White permissions; multi-team mission; unsupported tools; untrusted prompt injection; stale SHA; concurrent writer; denied release; missing externally authenticated host authority. Partition by real tasks, adversarial cases and difficulty. Report per slice and overall; an easy-case majority must not hide a critical security-class failure.

## 99% statistical honesty
- **Target should be pre-registered:** e.g. >= 99% *observed* acceptable single-step next-action accuracy on a representative unseen set, with Wilson or exact binomial confidence interval and separate safety strata; the exact *confidence requirement* is also set before running tests.
- **No observed errors does not mean proof of perfection.** Under an *illustrative IID Bernoulli* simplification, zero errors across about **299 independent samples** yields a one-sided 95% exact lower bound roughly 99% for success probability; for a two-sided 95% lower bound of 99%, about **367** independent all-correct samples are needed. Real mission data are correlated, nonstationary and unevenly risky, so these counts are NOT a sufficient final test plan. One failure changes the bound and requires more cases.
- **99% routing is not 99% mission success.** Separately publish end-to-end task results and severe-failure counts, plus reason for genuine abstention.
- **An average 99% across easy tasks is not acceptable for high-impact approval actions.** High-risk failure paths require hard deterministic proof, not inferred model probability.
- **Confidence is about sampling under declared conditions, not future behavior across all products/providers.** Do not state the system is universally 99% accurate.

## Planned test suite
1. **L0 contract/policy:** eligibility, schema, one writer, Head-only dispatch, exact revision, external approval separation, missing evidence and no 13th skill.
2. **L1 specialist competence pilot:** 30 distinct normal/edge/adversarial cases per team (=270), independent expected observations. Repeat three times under each chosen host/model *only within owner-approved cost cap*. Cases come from existing `docs/06-EVALUATION-LAB.md` and `docs/12-SPECIALIST-PERFORMANCE-DECISION.md`.
3. **New R1 routing dataset:** natural-language real/representative mission intents, correct eligible specialist sets, deliberately ambiguous tasks and valid abstentions. Multiple acceptable next actions may be labeled; labels must be versioned and independently reviewed.
4. **New R2 handoff/adversarial dataset:** missing prerequisite, misplaced vulnerability handler, duplicate worker, White self-grant, Gold override, stale SHA, spoofed GitHub comment, forged provider receipt, false audit PASS, exhausting retry/budget, unavailable tool, unsupported vendor.
5. **New R3 full mission plans:** mission state transition traces from HEAD_READY to completion or blocked; measure exact-SHA evidence and mandatory obligations across the whole chain.
6. **New R4 composition/ablation study:** on identical held-out cases, compare A) current skill-only basic routing; B) A+registry; C) A+handoff contracts; D) A+router policy; E) combinations; F) all combined. Control host/model/time/available tools and compare complexity, success, errors and cost. Avoid post-hoc re-labeling.
7. **Qualification:** only once pilots expose common defects, freeze larger independent hidden holdouts and thresholds; publish uncertainty, per-risk findings, false positives and non-executed scenarios.

## Evaluation scoring logic
- Freeze inputs, source code/fixture SHA, mission grant, registry revision, router policy revision, available tools, reviewer labels, permitted teams, and acceptance criteria before each run.
- Each result logs: model/host, version/skill IDs, source SHA, actual tool observations, decision, expected acceptable actions, required obligations, cost/time, severity, reviewer disagreement, PASS/FAIL/UNVERIFIED/NOT RUN.
- Prefer deterministic oracles, labeled telemetry, trusted GitHub CI attempts and test outputs; use separately calibrated evaluators for qualitative issues. Do not score model self-explanation as a verified receipt.
- Record paired baseline and candidate traces on the same independent scenarios. No selective hiding of failed runs.
- Don't modify holdouts to make a candidate score better; add a new version of the corpus and report both sets.
- Record dataset representativeness and holdout leakage risks; protect sensitive content, do not ingest real private data into uncontrolled files.
- Explicitly record all untested host/model configurations as UNVERIFIED.
- **No service assumption:** tests can use available cloud developer infrastructure; the product cannot require a user laptop/runner or a particular commercial evaluation provider.

## What would make another feature stronger?
- Registry improvements -> measured decrease in wrong-team routes, but only if held-out tasks support claim.
- Handoff contracts -> fewer missing-evidence / wrong-revision transfers, but latency may rise.
- Router policy -> fewer irrelevant dispatches / better mandatory-review recall, but may block more.
- Evaluation feedback -> selective changes to weak registry entries, handoff validation, and router rules, with no automatic promotion.
- Combined effect -> **synergy metric**: compare improvement of all components together to the sum of individually measured deltas; record if the combination is worse. Interaction value is a hypothesis, not assumed.

## No-go conclusions
Do not use '270 tests passed' as 99% routing assurance. Do not count 810 runs as 810 independent tasks. Do not imply live CI or GitHub comment provenance certifies user consent. Do not add an LLM-powered judge as an untrusted replacement for provider evidence. Do not release based only on a high average score.

## References (public)
- NIST NICE tasks/knowledge/skills: https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center/about
- NIST role/job distinction: https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center/resources/occupations-jobs-and-work
- NIST AI RMF: https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- OpenAI evaluation best practices (principles; no dependency on a particular hosted eval product): https://developers.openai.com/api/docs/guides/evaluation-best-practices
- OpenAI agent traces/evaluations: https://developers.openai.com/api/docs/guides/agent-evals
- Existing local v0.0.2 design: https://github.com/vixttha/Color-Team-OPS/blob/design/v0.0.2-team-contracts-single-lane/docs/12-SPECIALIST-PERFORMANCE-DECISION.md

**Source/currentness note:** If a vendor evaluation product changes or is deprecated, preserve the vendor-neutral methodology rather than requiring that product.
