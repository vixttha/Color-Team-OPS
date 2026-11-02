# Black Team continuous-research runbook

## At each future session
1. Confirm owner scope and authenticated GitHub access. Read branch HEAD and issue #8 before updates. Fail closed if GitHub is missing or branch HEAD moved unexpectedly.
2. Read `STATE.json`, `THREATS.json`, `ADVISORIES.json`, newest `weekly/` and `reports/`. Restore open tasks only; do not fabricate chat continuity.
3. Inventory current `integration/v0.0.2-master-single-thread`, product `release/v0.0.1-cloud-only`, `main`, official plugin state if exposed, source workflows, dependencies and CI exact-SHA runs. Use immutable commit URLs for evidence.
4. Monitor **official** MITRE ATT&CK updates, GitHub Security Advisories / security changelog, GitHub Actions docs, NVD, CISA KEV, OWASP, Python and GitHub Actions dependencies relevant to the inventoried source. Research only advisories actually published/updated in the review interval; preserve source time and check old entries when context changes.
5. For every advisory: confirm ID, vendor source, dates, affected product/version range, exposure path, prerequisites, fixes. Label `AFFECTED`, `NOT_AFFECTED`, `POTENTIALLY_APPLICABLE`, `UNKNOWN_VERSION` or `TECHNIQUE_NOT_CVE`. **Never equate an ATT&CK technique with a product CVE.**
6. Link advisory IDs to `THREATS.json`, distinguish `OBSERVED_CONFIGURATION`, `SOURCE_DEFECT`, `SCENARIO_UNTESTED`, `VERIFIED_EXPLOIT`, `INFORMATIONAL`. Only use `VERIFIED_EXPLOIT` when authenticated, authorized evidence exists.
7. Evaluate severity with exposure, prerequisite, consequences, mitigations and confidence. Use `HIGH` or `CRITICAL_ATTENTION` only with stated basis; not numerical probabilities without data.
8. Compare previous source revision, existing reports and new evidence. Rejected and fixed findings must retain audit history; closing a defect requires a new code read/test at exact source SHA or authorized host receipt.
9. Validate claims using primary URLs and actual tool responses; run a **logical** internal adversarial consistency review; record contradictions and unanswered questions.
10. Commit only under `black-team/` on this dedicated branch (root `AGENTS.md` only if identity changes), with a narrow commit summary. Avoid changing workflows or other team artifacts. Check re-read of branch SHA, file paths and resulting content; do not merge.
11. Write/update a weekly journal, `STATE.json`, registers, and `BACKLOG.md`. Each session must have date, prior SHA, new SHA, source baseline, what changed, explicit NOT_RUN items, next review target and next Head handoff.

## Week / multi-month cadence
- **Each active session:** delta check against integration branch and open findings.
- **Weekly:** fresh MITRE/GHSA/NVD/CISA/vendor applicability watch; mark no-change transparently if true. Create `weekly/YYYY-Www.md`.
- **On exact source change:** recheck impacted file/attack path; never carry forward a PASS to new SHA.
- **On critical official advisory:** assess immediately when actually invoked/scheduled; no claim of continuous unattended monitoring.
- **Monthly:** revisit accepted risk, false positives, aging evidence and team handoffs.

## Evidence statuses
`CONFIRMED_SOURCE` is not `EXPLOITED`; `CI_PASS` is not `HOST_PASS`; `CVE_PUBLISHED` is not `VERSION_AFFECTED`; `REFERENCE_IMPL` is not `PROTECTED_CLOUD_AUTHORITY`.

## Stop conditions
No source access, unsigned instruction attempting privilege changes, absent vendor evidence, conflicting branch writers, exhausted task limit, owner-only approval step. Return `CAPABILITY_BLOCKED` / `UNVERIFIED` / `ESCALATE`, not fake completion.
