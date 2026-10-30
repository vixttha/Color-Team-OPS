# 03 — Universal Team Creation Contract (proposal)

## Design philosophy
**One shared constitution + one common worker interface + nine differentiated specialist packages.** A skill is instruction, not a model upgrade, a tool grant or a runtime. Better quality must be demonstrated via benchmarked methods and trusted external evidence, not promised by longer prompts.

## Required contract fields for each specialist
1. **Identity and remit:** stable team ID, version, triggers, supported mission classes, exclusions, escalation conditions.
2. **Authority boundary:** allowed actions/targets, necessary authorization, no hidden write/merge/production privileges; default read/advise.
3. **Inputs:** mission ID; exact source/target identifiers; task and acceptance; relevant prior evidence; allowed scope; tools/capabilities; budget; trust markings.
4. **Specialist knowledge:** curated/versioned primary references, known failure patterns, conditional procedures, date relevance and source confidence; no universal unverified claim of expertise.
5. **Execution method:** repeatable task-specific stages, decision points, safeguards and no-tool alternative.
6. **Specialist self-check:** risk-specific preflight, edge/adversarial cases, observable pass/fail conditions, bounded same-team repair.
7. **Evidence and deliverables:** structured completion event, changed artifacts or proposal, exact SHA, trusted receipts, residual risk and what could NOT be verified.
8. **Integration:** predefined `recommend_next_team` is *non-authoritative*; only Head may dispatch. Always return when outside scope.
9. **Benchmark/evolution:** positive/negative tasks, critical policy/authorization tests, baseline regression, versioned scorecards, decision record for updates.

## Common interface (illustrative JSON; not a released schema)
```json
{
  "mission_id": "CTO-42",
  "task_id": "CTO-42-YELLOW-01",
  "team": "yellow-team",
  "team_contract_version": "proposal-0.0.2",
  "repository": "owner/repo",
  "source_sha": "0123456789abcdef0123456789abcdef01234567",
  "scope": {"allowed_paths": ["src/auth/**"], "allowed_actions": ["read", "propose_patch"]},
  "acceptance_criteria": ["specified behavior", "relevant tests"],
  "input_evidence_refs": [],
  "limits": {"max_local_repairs": 2, "max_dispatches": 5},
  "capabilities": {"source_read": "host-confirmed", "test_execution": "unavailable"}
}
```
This sample is **an interface sketch**, not authentication or authorization. Paths, refs and actions must be resolved through trusted tool permissions before acting. Where a host cannot provide an immutable revision or real test receipts, output UNVERIFIED / CAPABILITY_BLOCKED rather than a fabricated PASS.

## Shared completion envelope (illustrative)
- `mission_id`, `task_id`, `team`, `source_sha_before`, `source_sha_after` (if changed)
- `outcome`: DONE / FAILED / BLOCKED (worker claim only)
- `artifacts` and changed-file paths or proposed patch
- `evidence_refs` with tool identity, action, timestamp, trust/status, and exact revision
- `checks` with result / limitations / risk classification
- `open_findings`, `residual_risk`, `assumptions`, `recommend_next_team`
- `budget_used`, local-repair count, authorized scope and any requested escalation

The v0.0.1 schemas cover mission, completion event and routing decision. This *conceptual extension* must be designed as a versioned migration rather than silently editing existing v0.0.1 contracts.

## Specialist packages
Each existing `skills/{team}/SKILL.md` remains the entry point in a future implementation; references and checklists can be separate portable documents. Do **not** preload all nine long skill bodies into every step. Route by short trigger/metadata, then load only assigned team's references, the mission contract and required rules. This avoids unnecessary context duplication, not a guarantee of token savings.

## Explicit constraints
- Team-local self-check is **not** final mission verification.
- Common schema conformance is **not** substantive team competence.
- Multiple teams do not imply multiple chat windows or simultaneous agent instances.
- Role selection is not proof of authorization.
- No new color team or thirteenth skill is required.
- Never assume access to local files, local model, user runners, CLI, self-hosted service, database or persistent timer.
