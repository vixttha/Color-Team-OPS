# Color-Team-OPS — Nine-Team Role & Organization Deep Research

**Status:** Research workspace only. No product, skill, policy, CI, release, or runtime changes are authorized by this branch.

## Research objective

Audit whether a nine-specialist color-team model benefits Color-Team-OPS, distinguish established organizational/cybersecurity color-team terminology from this project's **custom** team definitions, and map real-world job functions to each team without implying a team needs a separate employee or model instance.

For each team, investigate:
- Mission, typical work, activation triggers, outputs, evidence and success metrics.
- Candidate job titles/competencies (primary, supporting, adjacent, and out of scope).
- Roles that overlap across teams, handoffs, ownership boundaries and separation of duties.
- Human organization vs. AI specialist-skill implementation, staffing/agent architecture tradeoffs, and cost/context/coordination risks.
- What to adopt, adapt, test, or reject for Color-Team-OPS, with dated sources and explicit confidence.

## Existing nine specialist names (do not silently redefine)

1. Yellow — functional software engineering.
2. Orange — security-aware application engineering.
3. Green — cloud operations / DevSecOps.
4. Blue — defensive security, detection and response.
5. Red — authorized adversarial testing.
6. Purple — offensive/defensive correlation and retesting.
7. White — exercise governance, rules of engagement and neutral adjudication.
8. Black — adversary threat intelligence.
9. Gray Cell — synthetic human behavior, misuse and human-error scenarios.

Three **coordinating skills**, not additional teams: Mission Control, OPS Director, Verification Gate. The Internal Auditor is a workflow phase, not a tenth specialist. Head controls one authorized execution lane and dispatch; teams do not self-authorize.

## Project sources to review

- [v0.0.1 release branch](../../tree/release/v0.0.1-cloud-only) — canonical existing skill definitions and constitutional rules, especially `docs/CONSTITUTION.md` and `skills/*/SKILL.md`.
- [v0.0.2 design branch](../../tree/design/v0.0.2-team-contracts-single-lane) — `docs/01-SCOPE-AND-DECISIONS.md`, `docs/03-UNIVERSAL-TEAM-CONTRACT.md`, `docs/04-NINE-TEAM-SPECIALIZATIONS.md`.
- [Main branch](../../tree/main) — default repository baseline.

**Important:** These branches may evolve independently. Verify their current content and exact revisions before making implementation recommendations. Do not assume draft v0.0.2 design is an approved or released product.

## Research-only change policy

- Add research notes, source references, matrices, and proposals **only on this branch**.
- Do not change existing team definitions, schemas, source code, CI, release files, credentials, runner settings or production behavior.
- No automatic merges, deployments, releases, new skills or authority changes.
- Mark recommendations as proposals until the owner explicitly approves them.
- Never treat a title/job-role mapping as a grant of tool access or execution authority.
- Preserve cloud-only operation, optional owner runners, least privilege, authenticated evidence and finite autonomy.

## Research deliverables (pending)

1. Source-cited nine-team job-role matrix.
2. Detailed team-by-team role and competency inventory.
3. Overlap/handoff and responsibility (RACI-style) map.
4. Gap analysis against existing Color-Team-OPS contracts.
5. Prioritized, testable improvements and risks, with a non-invasive implementation proposal.

This file is a research charter, **not** a completed audit.
