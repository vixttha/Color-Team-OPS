# Permanent product version and issue workflow

Owner direction: 2026-11-26. Governance record: issue #26. Release acceptance: issue #8.

- Maintain exactly one canonical Color Team OPS plugin identity. Product versions are distinct from development checkpoints and historical staging iterations. The next official target is v0.0.2; staging 0.0.9 is not an official product version.
- Use the permanent Version-Issues-Hub branch for issue-version assignments, exact revision, handoff and evidence. One active Worker; Head → Worker → Validate → Internal Auditor → Head. Assign permanent issue checkpoints using the verified VIB rules; never guess, reuse or manually bypass an assignment. Do not claim a checkpoint until installed product-ref binding and migration support are qualified.
- Develop on reviewed GitHub candidate branches; integrate selectively into the canonical product source, never merge permanent tool branches wholesale. Keep Version-Issues-Hub, Veraphify, readme-hq and Provenistem independent and persistent. Preserve prior branch and evidence history.
- Only free standard GitHub-hosted runners in the public repository are permitted for new development verification. No self-hosted/local or paid runners. Product runtime remains cloud-only, provider-neutral, skills-only in the initial release, with nine teams and three coordinators.
- Require exact source/package parity, applicable license and notice, privacy review, real fresh-session acceptance H-01–H-11 and Smoke A/B last, and separate owner release approval. Historical or exploratory traces do not become fresh acceptance. Optional Codex benchmark is not a release gate.
- Preserve the existing staging identity until the official replacement has passed acceptance, version/package readback and rollback evidence retention. Retire only the superseded staging identity afterward; no further staging identities. A capability blocker does not authorize bypassing acceptance.
- Preserve professional project attribution and the public information policy. Do not expose private identifiers, secrets or private test traces.
- License policy: unmodified PolyForm Strict 1.0.0 and project-specific supplemental installation permission, limited to rights actually held. Preserve third-party notices and prior grants; no blanket relicensing of historical refs.

Current blocker: installed VIB manifest binds main, which is a public landing branch, rather than the active integration source. Do not edit the manifest to bypass package rules requiring the default product branch. Qualify supported branch binding or owner-approved migration first. Current official plugin remains unchanged.
