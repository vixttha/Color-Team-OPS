# CTO-V002-SINGLE-THREAD — M2 Yellow Team Directory and capability lookup

**Mission:** one master v0.0.2 release, checkpoint M2.
**Source:** released team names and cloud skills; Purple proposed FEAT-000001 on its independent research branch.
**Status:** development candidate. Not a plugin release, grant, live Head router or signed authority.

## Added implementation

- `registry/v0.0.2/teams.json` is the single canonical machine-readable directory of **exactly nine** released specialist identities: Yellow, Orange, Green, Red, Blue, Purple, White, Black and Gray Cell.
- Each team has two stable versioned capability identifiers, conditional keyword triggers, *declared* tool requirements, expected evidence, and a pointer to the existing released specialist playbook `skills/<team>/SKILL.md`. The registry does **not** duplicate specialist prompts or create coordinator skills.
- `policy_v002/team_directory.py` validates the exact nine-team set, unique capability IDs, schema version, playbook path, tags and required tools. It offers deterministic scoped search and returns one playbook reference lazily when Head has selected that specific team. It has no tool invocation, OAuth connection, cloud host dependency or self-dispatch capability.
- `tests/test_v002_directory.py` contains 31 deterministic/negative tests covering nine identities, no Gold/Silver role, candidate lookup, no grant inference, tool access blocked without declaration, unknown/duplicated IDs, path traversal, extra privilege fields, schema version, explicit allowed-team scope and no provider lock-in.

## Operational boundary

Directory `SearchResult` statuses **CANDIDATES**, **ABSTAIN** and **CAPABILITY_BLOCKED** are metadata advice, not an OPS Director authorization decision. `Candidate.status=CANDIDATE_ONLY` remains advisory even when caller claims a tool exists: no grant or host-side token is supplied here. A real mission must independently verify user and host permissions, version/revision, no active Worker, capability budget and Head dispatch rights.

The nine-team catalog is a capability seed for M2, not a claim of measured team quality or official NICE job-color assignment. The research library's 36 idea records and five candidate features retain separate owner-controlled approval states; do not import or promote them silently.

**Host law:** Color Team OPS is cloud-only, provider-neutral and independent of any specific hosting platform. Skill pointers refer to package-bundled cloud-side playbooks, never a user's PC or a self-hosted runner. No Vercel, Supabase, paid host or GitHub runtime mandate was added.

## Head pipeline status

M1's reference code was internally audited and Orange's cross-scope findings repaired, but real protected-host authentication remains UNVERIFIED and full source-wide exact-revision CI remains missing. M2 candidate acceptance requires validation of the **actual committed** 31 tests and challenge of unauthorized capability/skill rights before Head may proceed to M3. There is no published v0.0.2 plugin or approved merge.
