# Session continuity protocol (weeks and longer)

## Start of a new session

1. Open the home branch and check exact HEAD.
2. Read: `README.md`, `identity/RED-TEAM-AGENT.md`, `policy/WORKING-CONTRACT.md`, `state/CURRENT.json`, `state/HANDOFF.md`, `state/WORK-QUEUE.json`, `state/FINDINGS.json`.
3. Check relevant prior report and worklog. Read Issue #8 and latest owner directives.
4. Re-query the live target branch, PR and CI status. Never assume the stored baseline is still current.
5. Re-evaluate approvals; choose one unfinished task within current grants. Record source SHA and budget.

## End of each session

1. Create `worklog/YYYY-MM-DD-<unique-topic>.md` and, when applicable, `audits/YYYY-MM-DD-<topic>-<shortSHA>.md`.
2. Update individual finding statuses only after evidence-backed Validate and logical Internal Auditor.
3. Update `state/CURRENT.json`, `state/WORK-QUEUE.json`, and `state/HANDOFF.md`, ensuring all refer to the same decision.
4. Commit with descriptive source-revision context and verify repository readback.
5. If tools fail, do **not** claim state was saved; explain which result is only in chat and which is on GitHub.

## Concurrency

This branch is persistent, but not an enforced distributed mutex. Multiple threads or agents must not overwrite each other; use expected-head commits and rebase only after inspecting conflicts. Never force-push this home branch. Check history before appending a session ID.

## Scheduling limitation

Plans for future cycles do **not** run by themselves. No weekly unattended security scan or automatic audit happens unless the owner separately configures a supported cloud automation with its own explicit authority and budget.
