# Issue #8 / M5 Green — Validate, Internal Auditor, Head

**Reviewed exact branch commit:** `e9e7afb6f537c8de123deef013ecb1a34bbb2e00`.
**Selected specialist:** Green — provider-neutral cloud release/CI and reproducibility engineering.

## Worker and Validate

Committed `devtools/build_v002_candidate.py` with deterministic file ordering, fixed archive metadata, Git HEAD check and *clean worktree* requirement, 12-skill/9-reference inventory, canonical identity in both manifests, generated per-file SHA256 manifest and complete ZIP-content digest verifier. `tests/test_v002_deterministic_build.py` contains 14 **authored but unexecuted** unit tests. The library is excluded, as are non-executable Python policy prototypes and test fixtures, so the installed-runtime package stays portable Markdown/JSON rather than pretending it has a protected cloud daemon.

GitHub read-back at this exact commit passed **11/11 static source/inventory checks**: 9 specialist SKILL.md files, 3 coordinators, 9 references, 3 schemas, 3 examples, aligned 0.0.2 plugin manifests, SHA binding, clean-worktree prohibition, no symlink sources, fixed time, manifest digest verification, and 14 test methods. This is **not** a native Python execution or an actual ZIP build.

**Validate:** `STATIC_SOURCE_PARITY_PASS`, `NATIVE_TESTS_NOT_RUN`, `TWO_REAL_ZIP_HASHES_NOT_OBTAINED`, `INSTALLED_PLUGIN_TRIAL_NOT_RUN`.

## Internal Auditor

A ZIP producer that only checks Git HEAD but ignores uncommitted files can bundle tampered content; Green repaired that by requiring `git status --porcelain --untracked-files=all` to be empty. This prevents mutable-source contamination but has not yet been independently exercised on the current actual private checkout. A generated source manifest and file hash are not signed release artifacts; no KMS, independent signer, trusted build attestation, protected host, canonical plugin update or real installed-version proof exists.

The ZIP is a **skills-only candidate**; `policy_v002/*.py` modules are not in the runtime ZIP. Therefore the new M1/M3 Python code cannot be claimed as deployed in ChatGPT from the ZIP alone. No external billable or user-owned runner operation was invoked.

**Internal Auditor:** `BUILD_CONTRACT_IMPLEMENTED`, `REPRODUCIBILITY_NOT_PROVEN`, `RELEASE_BLOCKED`.

## Head

Accept this narrow *development reference* for further validation, not M5 release acceptance. Security-sensitive Head/worker identity and repair-chain semantics remain unresolved in M1; select **Orange** for a focused read-only trust/authorization review. Orange may make a narrowly scoped repair to the master integration branch if it identifies a concrete source bug, then return to source-bound Validate → logical Internal Auditor → Head. No external penetration test, production service, paid infrastructure, merge or publication.
