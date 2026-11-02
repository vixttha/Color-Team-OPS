# BLUE TEAM AGENT — primary evidence catalog

Every linked item should be rechecked if used for a **current** decision. This catalog is a historical starting index, not a continuous live monitoring log.

| Evidence ID | Observation | Original primary source | Classification |
| --- | --- | --- | --- |
| E-001 | 12 branch heads were enumerated on 2026-11-02 before this Blue branch was created; it is now the 13th if none were added/removed meanwhile | [GitHub repository branches](https://github.com/vixttha/Color-Team-OPS/branches) | OBSERVED AT POINT IN TIME |
| E-002 | 583 tests passed on Linux and 583 on Windows, two 32-file ZIP builds per OS, identical archive SHA-256 `79466fbef60218c9d4aa92b90080eb7ec95d7153c6d08b1a0e4e4b8a723e33e8`, pinned integration SHA `908235bdd5fdd929db791518a414467816fb6b79` | [Actions run #41534746888](https://github.com/vixttha/Color-Team-OPS/actions/runs/41534746888) | TESTED AT EXACT HISTORICAL SHA; not current |
| E-003 | Canonical private plugin `plugins_6ae3edf1ea4c819182f275592273e2cc` remains v0.0.1 with a single attached release on initialization read | [Canonical plugin](https://chatgpt.com/plugins/plugins_6ae3edf1ea4c819182f275592273e2cc) | PROVIDER OBSERVED; refresh before claiming current |
| E-004 | Owner explicitly locked v0.0.2 release until approval and established Issue #8 communication | [Issue #8 — owner release lock](https://github.com/vixttha/Color-Team-OPS/issues/8#issuecomment-6589322069) | OWNER BOUNDARY RECORD, not a grant for new actions |
| E-005 | Portable, provider-neutral cloud skills-only scope; no user runner runtime | [Issue #8 — cloud-only law](https://github.com/vixttha/Color-Team-OPS/issues/8#issuecomment-6589225030) | OWNER-BOUNDARY RECORD |
| E-006 | Dedicated Blue team SKILL.md / competency file and nine-team directory | [Blue skill](https://github.com/vixttha/Color-Team-OPS/blob/db4eb42e2de7abf4ff3d464e747bfc1b22c575c6/skills/blue-team/SKILL.md) | SOURCE OBSERVED |
| E-007 | Web individual ZIP exporter accepts a syntactically valid SHA without matching repo tree/HEAD | [Exporter](https://github.com/vixttha/Color-Team-OPS/blob/db4eb42e2de7abf4ff3d464e747bfc1b22c575c6/devtools/export_v002_web_skills.py) | SOURCE-OBSERVED GAP |
| E-008 | Evaluation receipt type/replay paths and provider-proof adapter boundaries | [Trial pipeline](https://github.com/vixttha/Color-Team-OPS/blob/db4eb42e2de7abf4ff3d464e747bfc1b22c575c6/policy_v002/eval_trial_pipeline.py) | SOURCE-OBSERVED GAP |
| E-009 | Eleven supported-host candidate scenarios all NOT_RUN | [Host trial register](https://github.com/vixttha/Color-Team-OPS/blob/db4eb42e2de7abf4ff3d464e747bfc1b22c575c6/docs/V002-P2-P5-HOST-TRIALS.json) | RELEASE GATE |
| E-010 | 270 concrete synthetic evaluation fixtures, no independent labels or host trial observations | [Evaluation fixtures](https://github.com/vixttha/Color-Team-OPS/blob/db4eb42e2de7abf4ff3d464e747bfc1b22c575c6/evaluation/v0.0.2/concrete-domain-fixtures.json) | DRAFT/SYNTHETIC |
| E-011 | Development-only CI triggers on integration push, uses owner-managed runners | [Workflow](https://github.com/vixttha/Color-Team-OPS/blob/db4eb42e2de7abf4ff3d464e747bfc1b22c575c6/.github/workflows/v0.0.2-integration-native.yml) | SOURCE; live branch protections need recheck |
| E-012 | The original master issue remains central, without plugin release grant | [Mission Issue #8](https://github.com/vixttha/Color-Team-OPS/issues/8) | GOVERNANCE |

## Interpretation rules

- The Blue home is based on integration snapshot `db4eb42e2de7abf4ff3d464e747bfc1b22c575c6`. Do not assume this SHA or a dated CI SHA is the latest upstream branch.
- A `PASS` of 583 native Python tests is **not** equivalent to 583 independent specialist trials or to a detected/contained security event.
- The newest source may add 270 reference-router tests; such tests use seeded expected capabilities and are explicitly **not** measured LLM routing accuracy.
- Source-level code inspection is not a live exploit, production telemetry, permission audit, proof of branch protection, or evidence of incident closure.
- Redact all secrets, access tokens and identifying incident details; prefer immutable links and hashes rather than copying sensitive raw content into GitHub.
