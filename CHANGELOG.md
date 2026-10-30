# Changelog

Newest version first. Every version updates README.md, this changelog, acceptance evidence and relevant architecture documents.

## [0.0.1] — Private ChatGPT skills package created; GitHub PR remains draft

### Added
- Nine color-team roles plus OPS Director, Verification Gate and Mission Control (12 skills).
- Cloud-only constitution, cross-host portability notes, contracts and examples.
- v0.0.1 owner-authorized Windows/Linux GitHub self-hosted release tests, confined to the trusted v0.0.1 branch.
- The plugin and any future cloud backend remain independent of those developer runners.
- Design-stage runner policy and accepted ADR-0001.
- README-per-version rule, evidence-backed assistant audits and repository hygiene files.

### Security hardening (included in new canonical private package)
- Mission and evidence JSON Schema Draft 2020-12 cross-field requirements, disallowing incomplete OBSERVED/PASS and branch-write claims.
- Adversarial negative-schema regressions, semantically parsed workflow policy, and CI mutation tests.
- Cloud-only development test dependencies, explicitly absent from installed skill runtime.
- Corrected preflight evidence so source/installed package divergence remains clearly visible.

### Corrected CI and review policy
- ADR-0002 supersedes the mandatory GitHub-hosted baseline portion of ADR-0001. Hosted CI startup failures are historical and no longer the chosen test path for this release.
- The owner selected the assistant to audit this release; outside independent review is not a prerequisite.

### Release identity incident prevention

- ADR-0003 and `docs/PLUGIN-RELEASE-REGISTRY.json` establish exactly one canonical plugin ID.
- Owner expressly authorized deletion of the old ID. It is relabeled **OLD Color Team OPS - DELETE** and currently appears as its own draft release v0.0.2 (label-only change; **not** the canonical product's v0.0.2). The exact-ID uninstall command returned `not_installed`, but Plugin Creator still lists the old record; **full deletion remains pending a Creator-library delete action**.
- Added regression tests for plugin ID uniqueness, canonical version/source references, and mandatory release upgrade checks.
- This is repository release governance only; the installed v0.0.1 package and its cloud-only runtime have not been changed.

### Outstanding
- Both Windows and Linux GitHub Actions jobs passed 25/25 tests at `52b4160c8246e3ada245fe15c8d2657972118386` ([run #40983579901](https://github.com/vixttha/Color-Team-OPS/actions/runs/40983579901)); Linux ZIP reproduced byte-for-byte.
- New private ChatGPT v0.0.1 plugin created; all twelve skills registered/readable and 25/25 shared source files identical. Full interactive user mission trials and third-party host integrations remain unverified.
- Persistent autonomous cloud execution is not part of the skills-only v0.0.1 release.

Canonical private plugin `plugins_6ae3edf1ea4c819182f275592273e2cc` is new v0.0.1 (not a v0.0.2 update). The old private draft was relabeled, remains separately listed in Plugin Creator, and was **not deleted**; the owner has authorized removal. GitHub issue #5 tracks deletion confirmation. GitHub PR #1 is still draft until explicitly authorized to merge.
