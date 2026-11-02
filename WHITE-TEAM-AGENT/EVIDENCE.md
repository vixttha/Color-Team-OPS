# Evidence register — observed 2026-11-02 bootstrap snapshot

Historical observations below are source-bound and may be outdated when reopened. Refresh live facts in the next session before assigning a current PASS.

| ID | What was observed | Immutable evidence / reference | Limit |
| --- | --- | --- | --- |
| WTE-0001 | GitHub main initial commit; minimal README | main a28c2908da47d16dbdf7e55eb29a0c1ce9b6c7d3 | Branch boot base, not current product source |
| WTE-0002 | v0.0.2 integration candidate source | db4eb42e2de7abf4ff3d464e747bfc1b22c575c6 | Snapshot; Development HQ may advance |
| WTE-0003 | GitHub run 41536557201 succeeded at WTE-0002; 869 tests per OS, four matching 32-file ZIPs | https://github.com/vixttha/Color-Team-OPS/actions/runs/41536557201 ; SHA256 97910219e8a038e19696900afa27b8a83ca198ee108e7990b0afef5cb2f3568c | Native source tests, NOT installed host behavior |
| WTE-0004 | All enumerated branches were unprotected in an earlier 13-branch list (12 source + new Black home) | GitHub branches API 2026-11-02; https://github.com/vixttha/Color-Team-OPS/branches | Does NOT imply anonymous GitHub write access |
| WTE-0005 | Canonical Creator private installed plugin was 0.0.1 | plugins_6ae3edf1ea4c819182f275592273e2cc ; current release pluginrel_6ae3edf2a4ec8191b5cf9c92c317db22 | Does not validate unpublished v0.0.2 |
| WTE-0006 | 11 H-01–H-11 host trials marked NOT_RUN | integration branch docs/V002-P2-P5-HOST-TRIALS.json at WTE-0002 | No host security or one-prompt result proven |
| WTE-0007 | Evaluation has 270 prepared cases, zero independent approved oracles/trials, 54 visible holdouts | integration branch docs/V002-P0-P7-ACCEPTANCE.json at WTE-0002 | Python reference tests are not model quality |
| WTE-0008 | White team skill role and L1–L10 constitution | release/v0.0.1-cloud-only SHA fc77a647554cd40fb94839b3eb99e5f0ce4210a9 | Canonical project policy source |
| WTE-0009 | Owner P0 resolution and standing no-release condition | https://github.com/vixttha/Color-Team-OPS/issues/8 | Issue notes may lag newer owner direction |
| WTE-0010 | Blue/Red findings were source-challenged in White Team conversation | audits/2026-11-02-red-blue-adjudication.md | White static review is not dynamic penetration testing |

## Evidence acceptance rules

- Treat user-provided team reports as reported evidence until connector recheck, not as automatic live facts.
- For CI, record exact workflow run ID, attempt, head_sha, job logs and zip digest.
- For host, demand actual version/host/session, observations, provider action receipts and separately evidenced reviewer where required.
- For source, cite immutable SHA and path; never cite mutable branch alone to substantiate a current PASS.
- Do not store credentials, private chat content, local paths containing personal information, or secrets.
