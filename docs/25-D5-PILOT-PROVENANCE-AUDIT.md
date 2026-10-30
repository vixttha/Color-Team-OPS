# D5 — GitHub pilot provenance + locked host-neutrality: bounded audit

**Reviewed source:** `2139aec646754855b3660ae0a30cb4ebff522a73`
**Date:** 2026-10-30
**Audit status:** author-associated technical review; NOT an independent human/security certification.

## Pass 1 — Owner intent and architecture consistency
- The owner explicitly locked **"Keep Color Team OPS cloud-only, provider-neutral, and independent of any specific hosting platform."** The decision is in [CTO-LOCK-001](23-CTO-LOCK-001-CLOUD-PROVIDER-NEUTRALITY.md), referenced by the README, original scope and roadmap.
- D5 uses GitHub as an **optional source-specific evidence adapter**, not the product's required host. No Vercel/Supabase backend is provisioned. No specific database, runner, runtime cloud service or individual cloud vendor is required for skills-only mode.
- D5 adds no specialist team or 13th skill; the existing Head/Worker/Validate/Internal Auditor/Head cycle remains unchanged.
- No merge, main commit, v0.0.1 runtime change, Issue #4 code change or release occurred.

## Pass 2 — Real CI regression and corrected defect
- Added GitHub REST GET-only issue and comment reads with bounded pagination; added a D5 provenance observer that validates expected repository ID, issue/record actor and app metadata, five ordered logical-phase claims, no observed comment edits, historical exact workflow SHA/attempt/jobs and required test steps.
- **First candidate test failure:** [run 41008734262](https://github.com/vixttha/Color-Team-OPS/actions/runs/41008734262) failed seven endpoint tests: the new issue methods were accidentally placed in a Python `Protocol` rather than `GitHubRESTReader`. The failure was exposed by actual runner logs and repaired, not treated as passing.
- **Repaired code:** commit `2139aec646754855b3660ae0a30cb4ebff522a73`, [run 41008838794](https://github.com/vixttha/Color-Team-OPS/actions/runs/41008838794): **198/198 Linux tests PASS**, **198/198 Windows tests PASS**; each actual runner log was inspected with source-SHA PASS marker. This includes 40 newly added D5 negative/transport tests.
- **New anti-regression additions in this documentation commit:** explicit seven-case owner-law check for cloud-only, provider-neutral core and runner independence. These tests require an **independent exact-new-SHA rerun** before a final 205-test acceptance claim.

## Pass 3 — Live authenticated provider read and trust-limit challenge
- The real Python GitHub reader, running in a development-only CI job with a short-lived GitHub Actions token and `issues:read`, re-read [Issue #7](https://github.com/vixttha/Color-Team-OPS/issues/7) and GitHub CI run `41007120206` attempt 1 at **historical** SHA `2d77eb25a185fad37bec55b97be60f26eb15b47c`.
- Actual job output: `D5_GITHUB_PROVIDER_RESULT OBSERVED PROVIDER_EVIDENCE_OBSERVED_ROLE_AUTHORITY_UNVERIFIED`; `D5_ROLE_AUTHORITY_RESULT UNVERIFIED`.
- The five role labels were authored through the **same GitHub account and delegated integration**. That establishes provider-attributed event records, **not** independently authenticated Head/Worker/Validator/Auditor identity, not genuine host-issued user consent, and not cryptographically immutable history. Edited/deleted records may not be detectable after restoration without a separate protected audit ledger.
- The reference adapter deliberately **never outputs production role-authority PASS**. Real production completion must await a provider-neutral protected issuer with authenticated user grants, service-side secrets, transactional revision/revocation, role/state provenance, and a live mission test at the exact revision.
- The pilot remains read-only; previous owner runners are evidence/development infrastructure, never a condition for using Color Team OPS.

## Honest acceptance classification
- **CTO-LOCK-001 architecture law:** OWNER-LOCKED and documented.
- **D5 account-attributed GitHub issue and exact CI evidence:** OBSERVED from real authenticated provider responses.
- **D5 optional inspector and negative cases:** TESTED, with an initial defect repaired.
- **Production host user grants and independent model role attestation:** NOT IMPLEMENTED / UNVERIFIED.
- **Global cloud single-writer enforcement, nine team behavioral proficiency, v0.0.2 plugin release:** NOT VERIFIED / NOT READY.
- No statement here should be promoted into a claim of a complete production-host-authorized mission.

As in previous stages, this final audit documentation adds a new commit; only its own exact-SHA CI result can justify saying that new commit is fully tested.
