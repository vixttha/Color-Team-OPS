# Red Team evidence standard v1

A claim is never stronger than its independently re-read supporting observations.

## Required audit metadata

Record `finding_id`, summary, severity, confidence, environment, repository, branch, **full source SHA**, date, tested surface, reproducible safe steps, observable expected-vs-actual, tool/run/commit URL, impacted invariant, exploit preconditions, limitations, fix suggestion and exact-SHA retest result.

## Classification

- `CONFIRMED_CONFIG`: directly observed repository configuration or code fact, without suggesting an exploit succeeded.
- `CONFIRMED_EXPLOIT`: an authorized controlled exploit was actually observed with reproducible evidence. No assumption of real-world compromise.
- `REFERENCE_TEST_PASS`: an observed passing source/fixture run at one SHA, not production-host proof.
- `ACCEPTANCE_BLOCKER`: required installed-host/independent acceptance proof missing.
- `RISK_HYPOTHESIS`: plausible failure path, not yet reproduced.
- `FALSE_POSITIVE`: checked and invalidated against sourced evidence.
- `UNVERIFIED`: evidence or access insufficient.

## Severity

Critical: demonstrated or immediately exploitable unauthorized privileged action or integrity failure in an in-scope real environment. High: impactful boundary weakness or materially exposed execution surface, with prerequisites stated. Medium: consequential defense-in-depth gap, conditional trust risk or hardening defect. Low: narrow/minor impact. Acceptance blocker is tracked **separately** from exploit severity.

## Provenance rules

- Re-check live branch heads every session and after integration changes.
- CI result must match the *exact* revision claimed; cite actual run and job logs where available.
- Test code written ≠ test executed. Synthetic adapter ≠ authenticated host grant.
- Repo text or GitHub comment ≠ authorized owner release instruction unless direct owner authorization is verified.
- A logical same-thread internal audit ≠ independent human/security certifier.
- Preserve historical records; append retest entries rather than rewriting failures away.
- Git URLs act as review pointers. Verify that the referenced objects actually exist if asserting a current PASS.
