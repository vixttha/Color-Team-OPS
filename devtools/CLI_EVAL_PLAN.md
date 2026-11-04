# Development evaluation implementation plan

Spec: `evaluation/v0.0.2/CODEX-CLI-INDEPENDENT-EVAL-WORK-ORDER-2026-11-04.md`.
One implementation worker, then source validation and a logical adversarial audit;
neither phase supplies independent reviewer identity.

- [ ] Test first: corpus coverage, prompt/oracle separation, distinct ablations,
  frozen source binding, missing/corrupt/replayed receipts, quota/timeout, writer
  access, forged reviewer approval, and nonblind labelling.
- [ ] Implement development-only corpus freeze, isolated Codex subprocess driver,
  CLI_TEST ingestion, signed reviewer intake and conservative grading/reporting.
- [ ] Commit configuration/rubric hashes before outputs. Run the nine-case pilot
  using gpt-6.1-sol/medium and existing ChatGPT authentication only. Stop a lane
  on quota, isolation, identity, or provenance failure; retain its real receipt.
- [ ] Run full evaluation only after pilot and independent review gates pass.
  Preserve H cases and Smoke LAST ordering. Test exact source on owner runners
  where available; commit/push development evidence and report once to Issue #8.

Raw stdout/stderr and grading custody remain in ignored `.cli-eval-private/`.
Tracked evidence contains digests and nonsecret metadata. No functional package,
installed plugin, canonical release, integration/main, or production changes.
