# Black Team priority backlog — opened 2026-11-02

This is an intelligence queue, NOT a command to other specialists and NOT proof that fixes are accepted.

## Immediate / next Black session
- [ ] Re-read integration SHA after Development HQ moves and compare `BTI-04` exporter source binding.
- [ ] Re-read `eval_trial_pipeline.py` and tests to determine whether malformed and replayed receipt paths have been repaired.
- [ ] Check if the 12-source-branch `protected:false` observation changed; separately assess real permissions and runner trust.
- [ ] Gather exact Python/`jsonschema`/runner version inventory from authorized cloud evidence; until then record `UNKNOWN_VERSION`, not an affected CVE.
- [ ] Confirm v0.0.2 installed host H-01..H-11 and specialist-review evidence only from real host receipts.
- [ ] Check new MITRE/GHSA/NVD/CISA notices at each active review, dismiss inapplicable notices explicitly.

## Ongoing week-after-week
- [ ] Maintain stable BTI and ADV IDs; append distinct weekly snapshots and closed/reopened findings.
- [ ] Evaluate Red/Blue/Orange/Green changes for threat impact; do not run their tools without Head approval.
- [ ] Challenge unsupported security and compatibility claims; preserve owner release veto.
- [ ] Produce Head-ready risk handoffs with one proposed next specialist and exact source SHA.

## Team handoffs proposed (not executed)
1. Green + Orange — branch/runner trust protections (`BTI-01`).
2. Yellow + Orange — optional exporter source-to-artifact binding (`BTI-04`).
3. Yellow + Purple — receipt validation and cross-case anti-replay (`BTI-06`).
4. Red, then Blue — real-host adversarial evidence and telemetry for `BTI-02`, `BTI-03`, `BTI-05`.

## Done this session
- [x] Reconciled Red and Blue reports to latest integration test logs: 869/869 each OS, four byte-identical ZIPs at `db4eb42e2de7abf4ff3d464e747bfc1b22c575c6`.
- [x] Verified 12 branches / 12 reporting `protected:false` before creating the Black home branch.
- [x] Triaged authoritative MITRE techniques T1698 / T1700 and GitHub self-hosted runner enforcement notice.
- [x] Identified optional export SHA-binding and evaluation receipt-processing concerns.
