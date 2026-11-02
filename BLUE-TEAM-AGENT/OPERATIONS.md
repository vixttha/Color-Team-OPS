# BLUE TEAM AGENT — durable operations runbook

## 0. Scope and no-unattended-execution boundary

This runbook establishes **repeatable behavior when a Blue Team session is active**. It does not schedule an agent, promise background work, or authorize one ChatGPT conversation to keep running unattended for weeks. GitHub persists files; each later session must reread them. If the owner separately requests recurring monitoring, use an explicitly authorized scheduled automation and record that setup/limitations.

The only default writable Git ref is `agents/blue-team-agent`. Use cloud GitHub API/connector operations. Product runtime may not depend on the owner's machine, local runner, local terminal, desktop software, or vendor-locked service. Development tests on owner runners require existing separate permission and may never be triggered as a hidden runtime fallback.

## 1. Open a work session

1. Resolve the live `agents/blue-team-agent` tip and copy the full SHA into the session report.
2. Read `HANDOFF.md`, `STATE.json`, `IDENTITY.md`, the top of `BACKLOG.md`, `FINDINGS.json`, and most recent `logs/` entry.
3. Refresh relevant upstream source refs from GitHub, especially `integration/v0.0.2-master-single-thread` and Issue #8; do **not** assume this branch automatically tracks upstream.
4. Check owner's current instruction for scope; default to evidence-only observation. Record allowed branch, directories, tools, budgets, forbidden actions and task ID.
5. Head selects a **single** bounded Blue work item. If a new skill/tool action is unsupported, preserve `CAPABILITY_BLOCKED` rather than pretending it happened.

## 2. Work and evidence

For each finding attach `finding_id`, time/date, repo/ref/exact SHA (when source-specific), path or CI run/job IDs, observed behavior, potential impact, severity and certainty, remediation, owner, validation method, lifecycle. Never use one stale CI run to pass a later SHA. Separate authored tests from executed tests. If source is actively moving, pin the observed SHA and report head drift.

Incident-oriented tasks: collect only permitted observations, build timeline from provider timestamps, preserve source identity and redaction, identify detection gap and recovery recommendations, ask for explicit containment authorization where needed. Synthetic alert checks must be marked `SYNTHETIC`; they never imply actual intrusion or normal production health.

## 3. Mandatory single-lane gate

For every bounded task document:
- **Head / scope:** mission/task/criterion and explicit allowed actions.
- **Blue Worker:** exact reading/analysis or changed paths on the Blue branch; no lateral team dispatch.
- **Validate:** independently re-read source or CI receipts and test claims at exact SHA.
- **Logical Internal Auditor:** adversarial check for forged evidence, untrusted authority, stale revision, missing log coverage, self-certification, scope drift, misleading severity and unverified runtime claims.
- **Head disposition:** ACCEPT, REPAIR, REASSIGN, BLOCK, UNVERIFIED or COMPLETE for the bounded task only.

The logical Auditor is not an independent authenticated individual or separate plugin. Do not elevate a task PASS to v0.0.2 release PASS.

## 4. Save session and leave a checkpoint

1. Create a **new timestamped record** under `logs/YYYY-MM-DD-<slug>.md` (never rewrite earlier logs); use a unique slug for multiple sessions on one date.
2. Update `FINDINGS.json` and `BACKLOG.md` for genuinely changed statuses, with links. Mark an item resolved only after source-bound revalidation.
3. Update `STATE.json` and `HANDOFF.md` last, with last known observed upstream SHA, blockers, next actionable tasks and truthful evidence. Avoid a self-referential claim of current branch SHA inside the same commit; GitHub must resolve it.
4. Commit only on the Blue branch. Use an expected-head lease or sequential fresh SHA recheck and refuse conflicting writes. Never force-push or delete branch history without explicit authorization.
5. Read back the changed file(s) and branch tip after commit. Validate that another branch was not modified. Link the verified branch and relevant source evidence to the user.
6. If one write fails, report the exact partial commit/state and recover from a new read; never silently claim an atomic multi-file update from sequential commits.

## 5. Source synchronization and escalation

This branch began as a *snapshot* of integration `db4eb42e2de7abf4ff3d464e747bfc1b22c575c6`. It is NOT a parallel v0.0.2 release integration or a general permission to edit production skill source.

- By default, **inspect newer upstream source remotely** while keeping Blue's own branch independent.
- If tasked with implementing a defensive fix, develop the patch on **this Blue branch**, record base and tests; do not merge or cherry-pick into integration automatically.
- Have Head/Development HQ review an evidence-bound proposal and explicitly authorize any cross-branch promotion. Respect single integration writer.
- Do not rebase/force-push this long-lived home merely to pick up upstream changes; protect the longitudinal log. Only perform controlled synchronization with authorized review.

## 6. Weekly cadence without fake background activity

When actively invoked after a gap, examine open P0/P1 risks first; refresh CI/source/ownership; retest stale findings; then execute a bounded backlog item. At each weekly checkpoint write a dated report identifying **actual work performed**, age of outstanding findings, new upstream divergence and intended next tasks. A week with no active session must be recorded as **NO OBSERVATION**, never as continuously monitored or clean.

## 7. Stop conditions

Stop on unauthorized action, untrusted consent, source mismatch, missing tools, budget exhaustion, conflicting writers, suspected exposure of sensitive data, or missing required external approval. Return a specific `CAPABILITY_BLOCKED`, `UNVERIFIED` or `RELEASE_BLOCKED` condition. Never fake completion or silently schedule work.
