# D5 — Account-attributed GitHub pilot, not production mission authority

**Owner-locked prerequisite:** [CTO-LOCK-001](23-CTO-LOCK-001-CLOUD-PROVIDER-NEUTRALITY.md). Product is cloud-only, provider-neutral, and hosting-platform-independent.

## Live pilot already performed
[Issue #7](https://github.com/vixttha/Color-Team-OPS/issues/7) contains five ordered server-hosted records `D5-01` through `D5-05` describing one bounded read-only mission: HEAD → Yellow WORKER → VALIDATE → INTERNAL AUDITOR → HEAD. They were created via the connected GitHub app and attributed to the same owner account ID `237333433`. GitHub provider reported creation timestamps and matching unchanged update timestamps.

**Verified CI target:** private repository ID `1439026865`, branch `design/v0.0.2-team-contracts-single-lane`, **historical** source SHA `2d77eb25a185fad37bec55b97be60f26eb15b47c`, run `41007120206` / attempt 1, and completed successful required Linux/Windows regression jobs plus the live GitHub REST smoke. The source is historical; a later design-branch commit **does not invalidate the provenance of that old run**, and cannot be silently treated as tested by it.

## Executable D5 check
`policy_v002/pilot_provenance.py` offers an **optional GitHub-specific provider adapter check** for this pilot. It checks reviewed repository/actor/app IDs, event markers and ordering, creation/update timestamps, source run attempt, and exact CI jobs/steps. Its output **always leaves role authority `UNVERIFIED`**, including when GitHub provider observations pass.

The GitHub adapter uses read-only authenticated GET endpoints. No opaque role claims from GitHub comment bodies are converted into authority, no signing key is minted, and no human/auditor independence is asserted. The actual host permission to dispatch, current authenticated user grant, durable revision counter, key custody, signed transition attestation, and any global cloud lease **remain future implementations**.

### Threats deliberately not solved by GitHub issue comments
- An account or integration with edit/delete rights may alter or remove historical events, then leave surviving comments unchanged. No append-only or immutable log property is established.
- All five event comments have **the same GitHub principal**; provider metadata cannot independently attest model roles or separation of duties.
- An acting GitHub app being attributable to an account is not by itself a cryptographically bound ChatGPT user consent record for this specific mission.
- A green CI run proves named checks reported success, not the quality of every color specialist or absence of defects.

### Vendor neutrality
GitHub is **one replaceable evidence source**, not the Color Team OPS host. The product must remain usable where the supported cloud host offers other authenticated provider adapters, and basic skills-only mode does not require a separate backend. Vercel, Supabase, or any particular managed database is **not required or approved** by this mission. No paid project was provisioned.

### D5 acceptance
Accept `PROVIDER_EVIDENCE_OBSERVED_ROLE_AUTHORITY_UNVERIFIED` only as authenticated observation of GitHub records. Do not accept it as the D2 policy's `INTERNAL_COMPLETION_VERIFIED` under a genuinely protected HostAuthority. The actual hosted issuer, atomic revocation/mission ledger, same-session principal binding and real provider-neutral end-to-end mission are **NOT IMPLEMENTED / NOT RUN**.

The earlier five-stage read-only mission concluded **complete-with-limitations** only as observational analysis, without claiming production authorization.
