# 06 — Specialist Evaluation Laboratory (design proposal, NOT executed)

## Purpose
Measure how well nine differentiated teams work, not just whether their SKILL.md files parse. Existing v0.0.1 structural tests and past 25/25 platform runs do **not** prove specialist reasoning quality. A skill does not automatically make the base model more knowledgeable.

## Proposed entry-level corpus
**30 scenarios per specialist**: 10 normal tasks, 10 difficult/edge scenarios, 10 adversarial/negative cases. Nine specialists × 30 = **270 proposed cases**. These numbers are *planning defaults*, not approved acceptance thresholds or tests already run. Later extend coverage with real anonymized cases, unseen holdouts, updated vulnerability patterns and multiple supported hosts/models.

## Score dimensions
- Task success against an external/oracle-defined answer or observed tool outcome.
- Safety/authority: unauthorized action attempts, unapproved writes, scope changes, stop-rule violations; critical events block promotion regardless of average score.
- Evidence truthfulness: claimed versus observed execution, correct SHA, nonfabricated citations and tool results.
- Specialist quality: role-appropriate rigor (e.g., Orange bypass closure, Green rollback, Purple attack↔detection linkage).
- Precision/recall: missed issues, false positives and unsupported claims, where ground truth exists.
- Repair behavior: number of attempts, convergence, regression introduced, handling missing tools.
- Routing quality: right team selected, superfluous dispatches avoided, no uncontrolled handoffs.
- Efficiency: handoff count, available tool use, token/cost/time where measurable; never optimize cost by weakening safety.
- Compatibility: result fidelity across actual supported browser hosts; untested hosts remain unverified.

## Team-specific oracle / ground-truth examples
| Team | Benchmark oracle or observed outcome |
| --- | --- |
| Yellow | Hidden functional/edge tests and diff review |
| Orange | Seeded vulnerability + bypass tests and residual-risk verification |
| Green | Actual CI/deployment simulation receipts, config and rollback checks |
| Blue | Labeled alerts/telemetry cases, containment and recovery correctness |
| Red | Controlled vulnerable fixtures and scope-compliant reproducible findings |
| Purple | Attack-event ↔ detector correlation and measured before/after coverage |
| White | Rules-of-engagement conflict fixtures and correct authority decision |
| Black | Fresh dated source corpus and factual relevance/citation checks |
| Gray Cell | Synthetic user journeys and expected/observed task failures |

## Evaluation protocol
1. Freeze input fixture, acceptance, source SHA, test oracle, permissions and role version.
2. Establish baseline by running authorized tasks; save actual traces and outputs.
3. Introduce controlled edge/adversarial cases, including prompt injection in untrusted sources.
4. Score via deterministic checks where possible, documented human review for ambiguous quality, and independent tool observations for execution claims.
5. Compare updated team package against previous version on unchanged holdouts and new threats.
6. Block any critical authority/evidence regression even if average success improves.
7. Record exact versions, model/host limitations, seeds and uncertainty; never imply results were executed without receipts.
8. Promote a team contract only with documented user-approved gate, after future integration and package parity.

No global "zero mistakes" guarantee: aim to reduce error probability, detect severe errors early and fail closed. Distinguish false negatives from true absence of vulnerabilities. No evaluator may treat model confidence as objective proof.

## Operational separation
This lab is **development/testing infrastructure**, not a thirteenth runtime skill, not a local dependency and not a mandatory always-on service. User runners may optionally help develop/test it with permission; the installed Color Team OPS must run without them.
