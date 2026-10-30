# D4 — Protected mission-authority boundary and live provider integration

**Status:** Candidate implementation, NOT a deployed ChatGPT service; no user grants were minted.

## Design: separate independent trust sources
GitHub REST is authoritative only about the repository, branch SHA, run attempt, test jobs and steps it reports. A protected **host** must authenticate the user and issue immutable mission authorization, Head dispatches, stage transitions and two internal gate attestations. These are not authenticated by GitHub merely because a repository can be read.

\`SignedSnapshotAuthority\` in \`policy_v002/host_authority.py\` is a read-only implementation of D3's \`HostAuthority\` protocol. It verifies a canonical HMAC-SHA256 envelope against a **secret looked up in a protected service**, the issuer/audience, exact current mission revision from an **independently protected revision counter**, a UTC validity interval (maximum 1 hour), explicit non-revocation, mission/source binding, nonduplicate record IDs, approved dispatches, quiescent HEAD_DECISION state and aligned run bindings. Every read re-checks integrity, expiry, revocation and revision. Any malformed, stale, missing or unverifiable input raises \`AuthorityUnavailable\` (a D2 caller should return \`UNVERIFIED\`, never PASS).

**Do not treat this as a user-authentication solution.** Only a cloud service that actually checked user consent, tool permissions and target scope may issue the signed records. HMAC proves possession of the signing key, not independent human signoff, and is only as strong as the service protecting the key. The reference provides **no signing API**, issuer registration, real KMS, revocation database, hosted token exchange or storage.

## Live GitHub reader test
A development-only integration smoke test uses an ephemeral repository-scoped GitHub Actions \`GITHUB_TOKEN\` with \`contents:read\` and \`actions:read\` and calls the **actual Python \`GitHubRESTReader\`** against GitHub, using previously observed completed run 41005643330, attempt 1, commit \`64e23731bc889909614494bb88cbb6da2abbf37f\` on branch \`design/v0.0.2-team-contracts-single-lane\`. Its expected jobs are \`linux\` and \`windows\`, and their respective test steps. The GitHub-only smoke verifies what GitHub reported, not an authorized Color Team OPS mission or signed issuer record. No real user tokens, synthetic approval keys or credentials are written to the repository or printed.

GitHub Actions jobs run on **owner self-hosted development runners only**, and do not become a plugin runtime requirement. There is no mandatory CI, PC or local server when the plugin is used through ChatGPT.

## Acceptance boundaries
- **D4 host-authority tests:** verify signed-record integrity, expiry, replay, revision, scope, issuer/audience, Head authorization, team/transition/gate provenance and binding to D2/D3. Test signing key is clearly a synthetic fixture, never a production credential.
- **D4 live GitHub smoke:** calls GitHub over HTTPS using the actual GitHubRESTReader and ephemeral CI token. If blocked by permissions/network, report FAILED/UNVERIFIED and retain the exact run log.
- **NOT PROVIDED:** installed cloud trust service, real authenticated user approval, production mission ledger, issuer KMS, independent auditor, cloud fenced lock, real ChatGPT plugin trials or authorized end-to-end completion.
- **Base skills-first mode remains operable** without backend, but strong authenticated completion remains UNVERIFIED without a protected host.

Next: provision the issuer and revocation/mission store only after selecting and approving a cloud host and its costs, and run a real user-authorized host mission; do not conflate the development CI run with owner authorization to execute repository changes.
