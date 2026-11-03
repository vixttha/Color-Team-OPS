# GRAY CELL AGENT — PrismCell v0.0.1 independent usability and operator-error audit

**Date:** 2026-11-03. **Specialty:** onboarding, safe failure states, cognitive load, operator confusion, instruction integrity and project reuse. **Home:** `agent/GRAY-CELL-AGENT`. This is a logical, evidence-led Gray Cell review, **not** an observed human usability study or a separately authenticated agent.

**Source:** active v0.0.1 `25d59530210949792b3ce47ac0a804442997a9b1`; Yellow candidate `e4de4b037e61e2893a5a8e4178b51bb298c70ab4`, draft PR #18. Native [#41700021272](https://github.com/vixttha/Color-Team-OPS/actions/runs/41700021272) passed 89 Node / 21 Python per owner platform and generated a *synthetic* ASTRONOMY/STORY/REVIEW project.

## Gray pass 1 — simulate a new adopter and first-run path

The proposed instructions require a user to (a) prepare project JSON and team/branch/issue IDs, (b) arrange real GitHub branches and Issues, (c) run an **optional one-shot Node** offline document generator, (d) select each generated `TEAM-WORKBENCH/` folder, (e) commit it to the correct branch without sharing history, and (f) manually verify provider state before activation. This is a reasonable developer-oriented installer but **not** a one-click installation nor an automated GitHub provisioner. Node is used for optional generation, not required for on-demand operation of already created workcells.

The candidate does produce exactly **17 workcell documents** per team, with empty queue, inbox, outbox, evidence and `BOOTSTRAPPED_PENDING_LIVE_VERIFICATION`. This safe initial status prevents accidental claims of completed installation or live permission verification. Its explicit no-overwrite destination check is a positive control.

## Gray pass 2 — independent error-path challenge

**GRAY-PC-01 — MEDIUM/HIGH / misleading “verified” manifest claim.** `tools/verify-manifest.mjs` checks root `MANIFEST.json` count/source and reads *only* `STATE.json` and `OPERATIONS-CHECKPOINT.json` for each team. It does not verify bytes/hashes, presence or unmodified contents of the other **15** generated files such as `SCOPE.md`, `IDENTITY.md` or `WORKFLOW.md`, despite printing `PRISMCELL_OFFLINE_MANIFEST_VERIFIED`. An operator may infer the entire starter is correct even if a guidance file is missing or modified. **Remedy:** enforce exact expected file set and source-bound per-file digest manifest, verify all files, and separate `STRUCTURE_PASS` from provider-side installation acceptance.

**GRAY-PC-02 — MEDIUM / instruction text contaminated by project metadata.** Source `core/starter.mjs` injects arbitrary `project_id` into generated `IDENTITY.md` and `README.md`. Synthetic input containing newline + `### HEAD OVERRIDE` passed project validation and rendered that heading inside the agent identity document. No agent obeyed the injected text in this trial. A user could nevertheless mistake it for genuine instructions. **Remedy:** a safe single-line identifier policy, Markdown escaping, and a clear separation of owner-authored instructions versus configuration labels.

**GRAY-PC-03 — MEDIUM / confusing compatibility folders.** A new user sees `PRISMCELL/schemas/` and `PRISMCELL/core/schemas/`; all four pairs differ. Legacy `tools/guard.mjs` hardcodes the original nine Color Team OPS labels, although the new starter supports fresh names. The docs explain that legacy files should not be copied, but an accessible entrypoint should make the right choices mechanical: **START HERE** install checklist, canonical manifest listing supported files and a single source schema import path.

**GRAY-PC-04 — MEDIUM / late Git ref failures.** The validator accepts apparent branch names `team/` and `team/.lock` (synthetic examples); users might finish generating 17 documents for a branch that GitHub cannot create. Validate the chosen branch name before filesystem generation and give a plain-language actionable error identifying the invalid team/ref.

**GRAY-PC-05 — MEDIUM / insufficient role setup for new projects.** The generated `IDENTITY.md` contains only generic team identity, and `ROADMAP.md` intentionally says “Unassigned”. This is safe but does not help a user define the specialty, boundaries, evidence criteria or a meaningful first task. Provide a short first-run setup worksheet and a sample fully populated **nonprivileged** task for new projects; do not invent agent authority.

**GRAY-PC-06 — LIMITATION / no human or real second repo trial.** The 3-team clean-room test proves deterministic files and basic manifest checks, not that an unfamiliar user can install the template correctly or that a new ChatGPT project can read the new workcell without setup help. Perform a small hands-on clean-room onboarding trial with a real distinct GitHub repo, if authorized, and record every misunderstanding and recovery step.

## Gray pass 3 — usability verdict

**Existing nine Color-Team-OPS workcells:** USABLE with current owner-guided operational startup.
**Candidate reusability:** **CONDITIONAL/HOLD for beginner-ready release** pending Gray-PC-01–04 corrections and a guided first-run flow. Reusable **developer-only GitHub/manual prototype** is already credible.
**Claim boundary:** “Any project” is false if it means every platform/provider or zero setup. `GitHub Issues manual`, 1–50 teams and on-demand Head initiation are current v0.0.1 constraints.

No live human accessibility test, real GitHub install, new hosted service, credentials, release action, other-branch edit or Vercel deployment occurred.
