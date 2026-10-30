# Issue #8 / M5 — Green deterministic cloud-only ZIP build contract

**Worker:** Green (release engineering; separate from Yellow functional coding).
**Target:** `integration/v0.0.2-master-single-thread`.
**Classification:** BUILD TOOL + TEST FIXTURES AUTHORED, not an executed real source-bound ZIP.

`devtools/build_v002_candidate.py` defines a stdlib-only deterministic ZIP for the canonical **portable, skills-only** ChatGPT candidate, requiring a checked-out exact 40-character Git commit SHA. It sorts archive entries, sets fixed 1980 timestamps, stores file contents without platform-dependent compression, rejects symlinks, missing team skills/references, missing portable schemas/examples, invalid manifest identity, path escapes and overlarge files; produces a SHA256-per-file JSON manifest and archive SHA256. Its CLI performs **two complete builds and compares their bytes/digests** before writing the requested ZIP. Development CI may execute it in a standard authorized cloud environment.

**Bundle contents:** canonical two plugin manifests; 12 unchanged/updated skill descriptions (nine specialists and three coordinators), nine lazily loaded specialization references, three v0.0.1 portable schemas, three examples, Constitution and the v0.0.2 nine-team registry. It does **not** claim ChatGPT loads or executes the GitHub-only `policy_v002/*.py` modules; those remain versioned developer references, not part of the installed Markdown/JSON runtime. The Ideas/Feature Library and `portable/` companion are **excluded** and not required for normal operation. A real accepted runtime change to executable host dispatch must be separately integrated and proven.

`tests/test_v002_deterministic_build.py` adds 12 authored fixture tests: two byte-identical builds, exact skill/reference counts, absent optional library/Python runtime, SHA-bound source manifest, missing files, bad identities, wrong SHA, unavailable Git, tamper and symlink rejection. **Tests are authored but not natively run at this candidate SHA.** No ZIP has actually been built from the private GitHub candidate checkout, and no archive digest or source-to-installed-plugin parity is yet available.

### Reproduction in a separately authorized cloud checkout

1. Pin the integration checkout to its actual accepted commit and validate `git rev-parse HEAD` exactly equals that SHA.
2. Run `python -B -m unittest discover -s tests -p 'test_v002_*.py' -v` with the declared compatible dependencies.
3. Run `python -B -m unittest discover -s tests -p 'test_package.py' -v`.
4. Run `python -B -m devtools.build_v002_candidate --root . --source-sha <exact-40-hex-current-commit> --output cto-v002-candidate.zip`. The command builds twice, compares hashes and writes one ZIP on success.
5. Rebuild in a distinct clean checkout/authorized environment and compare SHA256, verify manifest, test installed canonical private ChatGPT version only after explicit owner release authorization.

These steps **have not actually run as a GitHub Actions/installed-plugin acceptance** in this work order. GitHub Actions owner/self-hosted runners are not a plugin runtime dependency and have not been dispatched; no chargeable external service or production host was provisioned.

**Validate result:** SOURCE-IMPLEMENTED, NATIVE-TEST-UNVERIFIED. **Auditor challenge:** Archive immutability and deterministic content must be proven with actual exact-SHA bytes, and the user must approve merge/publication. **Head:** M5 release stays BLOCKED.
