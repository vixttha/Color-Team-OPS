# Portable Idea + Feature Library v0.0.2 — six one-lane source audit

**DRAFT development report, 2026-11-10. Not release acceptance.**

- Scope: only the portable `ideas/`, `features/`, `templates/`, `tools/`, `tests/`, and local documentation of `vixttha/Color-Team-OPS`.
- Immutable source baseline: branch `idea-feature-library-v0.0.1`, commit `7b22c0417faa7ec11bab22f4dc4e12caea69ce87` (20 tracked files; no canonical records).
- Development destination: `idea-feature-library-v0.0.2`, forked from that exact baseline.
- NOT in scope: Color-Team-OPS v0.0.2 runtime/integration/master, team-agent home branches, Governance-Branch or its Bible, any production adopter, workflow dispatch, runner configuration, protected settings, release/publishing or merges.
- Each lane follows `HEAD → one specialist WORKER → VALIDATE → distinct logical INTERNAL AUDITOR → HEAD`. These are *reasoning/review stages in one chat*, **not six authenticated independent agents** and not an external security certification.
- "Validation" below means source-level review and added regression cases unless a specific executed test receipt is linked. Existing v0.0.1 tests were **read**, not executed. The baseline had **zero GitHub Actions runs** for its branch as observed on 2026-11-10. New tests remain **NOT RUN** at the time of this report.

## RED lane — adversarial inputs and filesystem escape

- **HEAD scope:** malformed JSON, untrusted record text, hostile symlinks; no active attack on external systems.
- **WORKER observations:** original `read_records()` preserved structurally invalid records in its maps; `validate()` later treated nested `testing` as a dict, `related_ideas` as iterable, and `lifecycle_status` as hashable. These combinations may raise exceptions instead of returning structured failures. `build` used `Path.write_text` on `INDEX.md` without a symlink preflight. `safe_repo_path` did not reject Windows drive-relative paths such as `C:secret` (as opposed to drive-absolute paths).
- **VALIDATE (static):** inspect original `tools/library.py` and compare with branch changes. Added invalid-type, evidence-path, index-symlink and record/schema-symlink regression cases in `tests/test_hardening.py`.
- **INTERNAL AUDITOR challenge:** link preflights remain vulnerable to race/TOCTOU changes by a hostile concurrent process. This template is not a hardened untrusted-workspace sandbox and may not claim globally atomic writes.
- **HEAD disposition:** P1 patches in development; run exact-SHA negative tests before acceptance. Maintain fail-closed semantics for invalid structures.

## BLUE lane — defensive behavior and recovery

- **HEAD scope:** failure detection, baseline drift and operator-safe recovery, not production monitoring.
- **WORKER observations:** `check` compares derived indexes with canonical records, but record-invalid-type exception paths could bypass its useful diagnostics. The built-in `shape` helper implements a subset of JSON Schema 2020-12 yet originally did not reject new unsupported schema keywords, risking silent validation drift after schema edits. Markdown tables also reflected titles containing link/formatting syntax.
- **VALIDATE (static):** new schema-keyword preflight and Markdown cell escaping; planned test cases demonstrate unknown `$ref`/`oneOf` constraints are explicitly refused rather than ignored.
- **INTERNAL AUDITOR challenge:** this is a limited checked-in-schema interpreter, not a standard-complete JSON Schema evaluator. Untrusted titles remain untrusted in all renderers, including GitHub's UI.
- **HEAD disposition:** P1 patches pending exact-SHA suite; no external detections or incident claims.

## PURPLE lane — Red/Blue correlation and boundaries

- **HEAD scope:** correlate attacks with detectable/blocked behavior; preserve authoritative boundaries.
- **WORKER observations:** no record files are bundled; the original one-way Governance isolation contract prohibits upstream registration, imports, auto-sync and shared release authority. Static guard tests detect obvious source violations, not cross-repository write permissions or future changes. A syntactically plausible `verified` feature can still cite fabricated evidence; no offline template can authenticate third-party receipts or human approval.
- **VALIDATE (static):** Red invalid-record/symlink cases mapped to Blue structured refusals, generated index safety and schema compatibility checks. Release membership stays `NOT_ASSERTED`.
- **INTERNAL AUDITOR challenge:** do not call a logically distinct reviewer a separately authenticated independent reviewer. Governance-wide non-interference and real adopter behavior remain external acceptance gates.
- **HEAD disposition:** preserve the no-Governance-dependency contract and require a separate blind adopter plus independent audit before release.

## WHITE lane — exercise rules and neutral adjudication

- **HEAD scope:** read-only baseline inspection and writes only on the new dedicated portable-development branch.
- **WORKER observations:** no consent to install on unrelated repositories, merge into `main`, call runners, change CI, write to Governance, or publish a product release. No destructive red-team activity is necessary to audit this code.
- **VALIDATE (static):** reviewed branch ownership, scope and test plan; explicit `NOT RUN` and `UNVERIFIED` for external tests.
- **INTERNAL AUDITOR challenge:** a simulated six-team review in one conversation has correlated failure modes; six labels do not mean six independent auditors.
- **HEAD disposition:** development authorized by user request, release authority not inferred. Stop at external write/runner/security gates.

## BLACK lane — source-grounded threat applicability

- **HEAD scope:** assessment of *applicable* trust-boundary hazards, not assertion of an actual intrusion or novel zero-day.
- **WORKER references:** GitHub's security guidance warns about executing untrusted PR content in privileged workflows (https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target) and injecting untrusted context into scripts (https://docs.github.com/en/actions/concepts/security/script-injections). The JSON Schema 2020-12 specification defines broader keyword handling than this small interpreter (https://json-schema.org/draft/2020-12/json-schema-core).
- **VALIDATE (static):** the optional tool uses no network or external-schema fetching; refusing unsupported `$ref` avoids silently pretending to enforce it. No new Actions workflow or elevated CI permissions were added.
- **INTERNAL AUDITOR challenge:** these are general documented threat classes, not evidence of exploitation of Color-Team-OPS; future risks may differ.
- **HEAD disposition:** avoid privileged evaluation of contributor-controlled code; use dependency-free offline tests and controlled independent review.

## GRAY CELL lane — realistic adopter and LLM behavior

- **HEAD scope:** synthetic beginner and fresh-agent user journeys, not real-user experiments.
- **WORKER observations:** `README.md` originally calls `templates/` optional while the step-by-step creation flow relies on copying example JSON from it. Manual INDEX upkeep and JSON editing are feasible but error-prone. Existing host `ideas/`/`features/` is deliberately a stop condition, not a request to overwrite.
- **VALIDATE (static):** proposed three synthetic tasks: blank repository intake, collision with existing host paths, and stale-index correction. Each must preserve host `AGENTS.md` and release authority.
- **INTERNAL AUDITOR challenge:** no independent unrelated GitHub adopter or blind fresh-agent behavior has actually been exercised at the v0.0.2 SHA.
- **HEAD disposition:** P2 documentation/UX repair and dedicated disposable-adopter acceptance before a release claim.

## Consolidated findings / checkpoints

| Key | Severity | Evidence | Resolution/gate |
| --- | --- | --- | --- |
| L-01 malformed-record exceptions | P1 | Original `read_records` and `validate` source | Patch made; negative tests added; execution pending |
| L-02 local symlink read/write boundaries | P1 | Original `build` and `Path.write_text` | Preflight patch; symlink tests added; concurrency not solved |
| L-03 unsupported schema silently ignored | P1 | Original `shape` helper | Fail-closed schema-keyword check added; execution pending |
| L-04 premature testing PASS claims | P1 | Original schemas/semantic checks | Refuse outcome unless status is tested; does not authenticate evidence |
| L-05 Windows-relative/invalid evidence paths | P2 | Original `safe_repo_path` | Drive/control/invalid-character guard added |
| L-06 Markdown link formatting in index cells | P2 | Original `cell` | Escape Markdown metacharacters |
| L-07 examples/adoption flow ambiguity | P2 | `README.md`, `docs/ADOPTION.md` | Fix adoption docs; fresh-agent test pending |
| L-08 true independent/adopter evidence absent | release gate | No v0.0.1 branch Actions runs; no disposable adopter readback | Still open; never manufacture PASS |
| L-09 Governance cross-project non-interference | release gate | `docs/ONE-WAY-BOUNDARY.md`, static tests | No upstream edits; actual isolated adopter audit pending |
| L-10 no globally atomic filesystem transaction | known limitation | Preflight has race between checking and use | Explicit limitation; do not promise hostile-host protection |

## v0.0.2 target acceptance

1. Commit source and negative tests on the dedicated branch; preserve `idea-feature-library-v0.0.1` unchanged.
2. Execute `python tools/library.py check` and `python -m unittest discover -s tests -v` **against the exact candidate SHA** in a disposable authorized cloud environment. Record exit status, case count and environment. Do not dispatch costly owner runners without permission.
3. Test an actual unrelated blank GitHub repository, a deliberate no-clobber collision, a fresh-agent read-only discovery, invalid records and symlink preflight. Capture repository/revision proof. No real repo overwrite.
4. Audit Python source, schemas, manifest/paths, docs, and exact output independently; separate logical internal review from real external reviewer identity.
5. Resolve or explicitly accept remaining P2 limitations, obtain owner release authorization, and only then name a v0.0.2 release.

**Current verdict: DEVELOPMENT IN PROGRESS. No release, no external independent certification, no authenticated evidence verification.**
