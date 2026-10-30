# Role-model gap audit & non-invasive decision proposals

## Comparing existing Color-Team-OPS to uploaded corporate nine-team model
| Finding | Severity | Evidence | Result | Proposed treatment |
| --- | --- | --- | --- | --- |
| Proposed Gold conflicts with Head authority | HIGH | Existing Mission Control + OPS Director and design/02-SINGLE-LANE-ARCHITECTURE; uploaded Gold directs priorities | Real conceptual contradiction if adopted as a worker | Keep managerial strategy under Head; optional competency pack, no separate writer |
| Black reassigned from threat intelligence to platform ops | HIGH | v0.0.1 skills/black-team vs uploaded Black platform | Direct contract/skill breaking change | Preserve Black; place infrastructure roles under Green |
| Gray Cell removed in proposed nine | HIGH | v0.0.1 skills/gray-cell present; uploaded list lacks Gray | Direct functional loss | Preserve Gray as synthetic user experience tester |
| White proposed as generic independent audit + GRC | HIGH | v0.0.1 Constitution L7 and design/02 distinguish White vs Internal Auditor | Role/authority conflation risk | White neutral exercise governance; separate internal-audit phase |
| Green proposed narrowed to defense engineering | MEDIUM | Existing Green also owns cloud deployment / observability / reliability | Scope shrink / unowned deployment risk | Keep cloud ops plus security-aware platform tasks; test overlap with Yellow, Blue |
| Exhaustiveness of job titles | MEDIUM | NIST NICE says roles vs jobs are distinct | False standards claim if copied | Treat job titles as representative, multi-team contextual mapping |
| Color terminology presented as universal | MEDIUM | NIST exercise terms and NCCDC differ, especially Orange/Green/Gold | Evidence contradiction | Scope every color definition to a particular taxonomy |
| Team sequencing for every mission | MEDIUM | Head-controlled one-lane design; differing mission needs | Cost and loop risk | Routing determined by mission type and evidence; not nine mandatory stages |
| New teams based on labels alone | MEDIUM | No specialist benchmark showing effect | Unverified utility | Create measured mission trials, before/after baseline |
| Source provenance in uploaded research | MEDIUM | Inline citation references absent from pasted text, strong narrative claims | Individual assertions cannot be traced from paste alone | Cite original primary URLs and mark unsupported organizational suggestions clearly |

## Role routing and handoff map (proposed, not activation policy)
- Yellow ↔ Orange: implementation vs security-sensitive code; requirement traceability and tests.
- Orange ↔ Red: exploit-informed repair vs independent scoped attack retest.
- Red ↔ Purple ↔ Blue: attack case, actual alert, detector improvement.
- Blue ↔ Green: detection specification vs telemetry, secure cloud infrastructure, recovery.
- Gray ↔ Yellow/Orange: observed user misuse vs functional/security fixes.
- Black ↔ Red/Blue/Orange: dated observed threat relevance vs tests/defensive action.
- White ↔ Head: exercise rule or safety adjudication; White does not authorize itself.
- Head ↔ all: sole scope/routing/final-acceptance authority.
- VALIDATE and INTERNAL AUDITOR: mandatory noncolor phases, distinct from specialties.

## Evaluation experiments before any implementation change
**E1 Existing-team specialization utility:** Compare Yellow-only vs Head-routed Yellow→Orange on 10 authorized sample security tasks; measure real fix correctness, unchanged functional tests, false alarms, time and token cost; hold environment constant.
**E2 Black / Green split:** 5 current-vulnerability analyses and 5 deployment incidents; test whether Black research and Green cloud-ops results are relevant, source-cited and non-hallucinated.
**E3 Gray value:** 10 deterministic onboarding/error-recovery scenarios with synthetic accounts. Compare bugs found by Gray versus Yellow tests, false positives and reproducibility.
**E4 White vs Auditor separation:** 5 simulated authorization disputes and 5 forged proof cases. Verify White cannot self-authorize and internal audit rejects invalid evidence.
**E5 Gold/Head collision tests:** Try untrusted text requesting a Gold override/parallel dispatch; expect refusal, Head-only policy and one writer.
**E6 Workflow economics:** Compare baseline one-specialist+gate vs risk-adjusted multi-specialist workflows; track quality, tool calls, latency, tokens, repair churn.

Acceptance: source-bound evidence, precommitted test fixtures, reproducible PASS/FAIL, no fabricated assurance. Proposed experiments are NOT RUN and not proof of superiority.

## Proposed registry (not added to product)
Team metadata: team_id, mission, responsibility, role_candidates, capability_tags, activation_triggers, input_artifacts, output_evidence, boundaries, handoff_targets, performance_metrics, primary_sources, project_defined semantics.
Role metadata: title, primary_capability, optional_secondary_capabilities, task_families, knowledge/skills, experience level, authorized_tools **as mission-specific grants only**, measurement and limitations.

## Decision status
APPROVE AS RESEARCH: six-color conceptual mapping; role-to-capability registry idea; solo-developer task guide; concrete capability test plan.
DEFER: expand White into enterprise-wide GRC; deep division of platform competencies within Green.
REJECT WITHOUT NEW EXPLICIT OWNER AUTHORITY: renaming Black to infrastructure, removing Gray for Gold, creating autonomous Gold chain of command, delegating Head authority, any changes to runtime or release branches.

Research is intentionally isolated on research/nine-team-role-audit-2026-10-30. Nothing here changes v0.0.1 or draft v0.0.2 behavior.
