# Conditional mission routing — replace inflexible team chains with testable decision rules

**Status: design idea, not active routing policy.** This is a comprehensive successor to the earlier heuristic sequence table. **Head first / Head last** for every mission; after each selected Worker the actual pipeline is **Worker -> Validate -> distinct Internal Auditor -> Head** before subsequent dispatch. Every candidate next team is proposed, not automatic. An already-existing outcome and no need for a new writer can legitimately finish without a new team.

## Decision order
1. Mission Control checks owner request, authority, exact target/revision, tool availability, expected outcome, cost/handoff budget, data sensitivity, approved write scope, stop conditions.
2. Classify primary outcome: build / secure design / fault diagnosis / adversarial validation / security detection / user misuse / threat research / exercise rules / delivery/recovery.
3. Determine technical evidence already available and the current stage. Evidence may change the optimal first specialist.
4. Construct **required** capability obligations and **optional** conditional checks; forbid unapproved write/deploy/release.
5. OPS Director recommends **one** qualified available worker and why. Never infer capability from a job title alone.
6. Worker performs bounded scoped work, returns actual evidence (including unavailable/not-run).
7. Validate, logically distinct internal audit and Head choose repair, another worker, complete, abstain or block. An unverified source cannot become a completed verified claim.
8. On relevant source change, invalidate/re-establish dependent tests for exact revision.

## Example mission decision table — all entries conditional
| Mission class | Typical first worker | Required or likely next specialties **only if justified** | Outcome/exit evidence | Risk of naive fixed chain |
| --- | --- | --- | --- | --- |
| Standard feature | Yellow | Orange when auth/data/trust boundary; Gray when UX acceptance; Green when actual release readiness | Hidden/actual functional tests and acceptance; production release separately granted | Unnecessary Orange/Red/Green for harmless edits |
| Authn/authz or security-sensitive feature | Orange to specify threat requirements, OR Yellow when detailed requirements already vetted | Yellow implementation; Orange regression; Red only for separately authorized adversarial test; Green for deployment | Authz invariants, negative tests, functional tests, current SHA, external grants if any | Missing threat model or overtesting |
| Ordinary bug | Yellow | Gray if user journey reproduces; Orange if security-rooted; Green if deployment bug | Reproducer fixed and regression passes | Calling security specialists on a text bug |
| Reported vulnerability | Orange for triage (or Red if authorized verified reproduction required and conditions set) | Black only if current threat intel relevant; Orange/Yellow for repair; Red scoped retest; Purple/Blue if detection target | Verified issue and fix at current SHA, residual risk documented | Treating every report as confirmed, invoking Red without ROE |
| Improve detection | Blue | Green for instrumentation; Red for approved emulation; Purple for attack↔alert mapping | Grounded log/alert before/after and known false positives | False claim that proposal == observed detector |
| Cloud deployment of built app | Green | Yellow for demonstrated code defect; Orange for security blocker; White only for exercise disputes (not generic release signoff) | Provider run/job/revision evidence, health/rollback, proper release permission | Equating CI green with production approval |
| Cloud incident / outage (unknown cause) | Green if operational failure indications | Blue if compromise suspected; Yellow if application regression proven; Orange for confirmed app vuln | Observed incident cause/recovery and residual uncertainty | Sending code fix blindly when service is down |
| Security incident / suspected compromise | Blue | Green for containment/recovery infra; Black threat context; Orange/Yellow remediation; Purple targeted validation | Verified containment and recovery status; missing telemetry disclosed | Mislabeling absence of logs as clean bill of health |
| Verified threat intelligence research | Black | Orange/Blue/Red only if follow-up requested and authorized | Sources dated, versions/configs relevant, uncertainty explained | TTP speculation presented as live exploit |
| User journey / onboarding | Gray Cell | Yellow when functional bug; Orange when access/data leak; Green if monitoring issues | Synthetic expected-vs-observed test receipt, privacy safe | AI persona treated as real-user evidence |
| Exercise permissions or rules dispute | White | Head authorized decision/stop; Red only after explicit ROE | Trusted scope/safety source, neutral ruling; authorization by actual Head/host | White self-granting permissions |
| Infrastructure secrets or CI misconfiguration | Green | Orange if application credential handling; Blue if leaked secrets used; Yellow for code tests | Provider config and token rotation authorization, no false claims | Misrouting to released Black threat intelligence |
| Performance degradation | Green for production signals, Yellow for established application bottleneck | Gray for UX experience when relevant; Blue if attack-driven load suspected | Grounded profile and before/after measurements | Assuming infra or code cause in advance |
| Accessibility failure | Gray for observed user journey or Yellow for known code defect | Yellow for implementation/repair | Observable accessibility regression pass / known limits | Too many stages for localized issue |
| Research-and-planning only | Black for threat topics; Yellow for design; Head if scheduling/priority; White for exercise policy | No other specialist if no implementation is authorized | Dated, scoped report explicitly not execution | Auto-creating implementation work from research |
| External merge/release permission pending | Head/host authority; **no specialist by default** | Green only if technical readiness incomplete | Blocked-external-approval until trusted actor approves | Asking White to impersonate independent approver |
| Unsupported tool / no trusted evidence | Head returns honest blocked or read-only advice | None unless another allowed source actually exists | UNVERIFIED / CAPABILITY_BLOCKED with precise missing capability | Invented tests, invisible runner dependency |
| Multiple sessions attempt same write | Head + protected service if available | No writer without provider-enforced protection where required | Fenced gateway/expected SHA or CAPABILITY_BLOCKED | Prompt-based fake global mutex |

## How candidate eligibility is decided
A candidate must pass ALL mandatory checks:
1. Team matches registered capability and is allowed under mission scope.
2. Task is an authorized action; provider/host tool is actually available and permissions proven where necessary.
3. Required prerequisites and grounded evidence exist, or the task is an explicitly labeled diagnostic attempt.
4. No unreviewed worker or unsatisfied validation/audit stage is bypassed.
5. Source revision / mission revision valid, no stale grant or changed target.
6. Budget/retry and single-lane requirements preserved.
7. Unavoidable external approval is not bypassed by a color team.
Then Head may favor (among valid candidates) the one with clearest task fit, fewer unnecessary handoffs, lower risk and cost, and higher benchmarked confidence. Tool absence warrants honest blocking, not rerouting to an unqualified color.

## Positive vs negative example
- "Fix button alignment in internal staging dashboard": Yellow only if acceptance is visual+functional; use Gray only if UX evaluation is required. A mandatory nine-team chain is expensive and less reliable.
- "Add user login & cloud release": Orange threat requirements → Yellow build → Orange security check → Green release readiness; Gray if UX criteria; Red only if approved/required; Blue/Purple only if detection objectives. All transitions go via Head + validation/audit.
- "Account takeover signal": Blue first, Green for missing login logs, Orange if auth code defect, Purple if attack↔alert proof required. Starting with Yellow risks losing incident evidence.
- "Red found IDOR": Orange fix, Red controlled retest, Blue/Purple only for monitoring objectives. Black TTP research is optional, not a required stage.
- "Need an urgent production deployment but permission unknown": Mission Control/Head must block release; neither Green, White nor Gold can manufacture consent.

## Red/Green/Black/Gold/Gray taxonomy safeguard
Maintain Black as threat intelligence, Green as cloud/platform operations, Gray as synthetic user behavior, White as neutral exercise governance, and Head as sole strategic/dispatch/acceptance authority. The alternative uploaded 'Black Infrastructure/Gold Executive' *company* model lives only in research/06 and is not an adopted routing rule.

## What is still unverified
No numerical routing accuracy has been measured, no complete v0.0.2 hosted plugin mission has been accepted, and no production host user-grant system is demonstrated. This matrix is a proposal to test via research/09, not a proof of correctness.
