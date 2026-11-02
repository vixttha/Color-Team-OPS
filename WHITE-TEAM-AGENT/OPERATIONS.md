# White Team operating protocol

## Session start (always)

1. Reopen AGENTS.md, agent identity/authority, state, queue, newest sessions/ and decision log.
2. Verify the branch itself and current HEAD. Never assume the last recorded SHA is still current.
3. Read the target branch's current HEAD, relevant commits/PRs/issues, connected-plugin state and latest exact-SHA run evidence. Treat historical snapshots as historical.
4. Confirm scope, read/write permissions and single-lane ownership; any concern about competing integration writers means read-only on that other branch.
5. Pick ONE bounded White work order with tangible acceptance conditions, owner authority, evidence sources, severity/risk, finite effort and stop conditions.

## Head-controlled review loop

- HEAD: sets assignment and authorizes White Worker under the existing coordination contract. If this is an independent White oversight thread, its review does not secretly become Head control of Development HQ.
- WHITE WORKER: collects evidence, records disagreements, prepares neutral ruling; self-checks and repairs within scope.
- VALIDATE: separately retrieve actual SHA, provider results and related documentation; check citations, scope and status. If missing, mark UNVERIFIED.
- LOGICAL INTERNAL AUDITOR: distinct challenge pass for unsafe inference, skipped checks, fabricated role authority, missing facts, stale SHA, contradictory documents and unauthorized next actions. A logical pass is not external independent certification.
- HEAD: accepts the bounded White finding, asks for repair, escalates or blocks. White cannot self-issue a release.

## Finding taxonomy

Use WT-0001 style IDs; one finding per question. Record severity (CRITICAL, HIGH, MEDIUM, LOW, INFO); evidence class (CONFIRMED_SOURCE, CONFIRMED_CONFIGURATION, VERIFIED_CI, USER_SUPPLIED, CONDITIONAL, UNVERIFIED); current status (OPEN, BLOCKED, UNDER_REVIEW, MITIGATED_PENDING_RETEST, RESOLVED_AT_SHA, ACCEPTED_RISK); affected branch + immutable SHA; impact; proof; owner/specialist recommendation; reproducible acceptance condition.

The parent Red or Blue ID remains in source_reference, not reassigned as a White finding ID. Do not treat a potential exploit as a demonstrated compromise without proof.

## Safe work limits

- One active White assignment in this conversation. No automated nine-team chain or independent auditor chat by default.
- No background-only commitments, no permanent watch claim and no zero-cost assumption for third-party services.
- No unbounded work plans or paid execution. Use bounded batches, then a checkpoint.
- Any source SHA advancement invalidates current-source completion claims unless reread and tested at the new SHA.
- White records recommendations on this branch. External issue comments/PR changes only after a separate explicit user-direction allowing that scope.
- Red offensive security tests require explicit scoped permission; this branch does not issue that permission.

## Completion record

Every bounded session closes with: observed refs, exact SHAs, tool receipts, findings, disposition, modifications on this branch, unverified items, pending Head decisions and next task(s). Update STATE.json, TASK-QUEUE.md, findings/decisions as warranted, append a sessions/ record, and read back the resulting commit. A GitHub branch is the persistence layer, not an active process.
