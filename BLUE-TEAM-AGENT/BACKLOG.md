# BLUE TEAM AGENT — durable task queue

**Mode:** active only when invoked by the owner/authorized Head or an explicitly scheduled automation. Every item is an *intended work item*, not a claim that it has executed.  
**Home branch:** `agents/blue-team-agent`; **integration source remains separate**.  
**Current owner release lock:** v0.0.2 must NOT be released without explicit approval.

| ID | Priority | Responsible recommendation | Current status | Acceptance evidence required |
| --- | --- | --- | --- | --- |
| BT-001 | P0 / HIGH | Blue → recommend Yellow fix, Orange review | OPEN | Optional web-skill exporter binds claimed source SHA to clean HEAD and every packaged Git blob; negative tests reject spoofed SHA, dirty tree, symlink and archive mismatch |
| BT-002 | P1 / MEDIUM | Blue / Yellow | OPEN | Evaluation ingestion safely rejects malformed/unhashable receipt values without exceptions; source unit tests executed at exact SHA |
| BT-003 | P1 / MEDIUM | Blue / Orange | OPEN | Receipt uniqueness checked across cases and arms, bound to case, provider, source and operation; replay-negative tests executed |
| BT-004 | P1 / HIGH | Blue / Green / Head | OPEN / NEEDS LIVE RULE EVIDENCE | Read branch protections/rulesets, collaborator access and runner trigger restrictions; no unreviewed push can execute untrusted code on owner machines; no unauthorized runner run |
| BT-005 | P1 / HIGH RELEASE GATE | Head / Orange / Gray / Purple | BLOCKED_EXTERNAL_HOST | Actual installed v0.0.2 cloud-host H-01–H-11 traces, role/handoff evidence and denial behaviors; owner identity actions require separate approval |
| BT-006 | P1 / HIGH RELEASE GATE | Purple / independent reviewers / nine specialists | BLOCKED_INDEPENDENT_ORACLES | 270 independent oracle labels, protected holdouts, real host trials, scored reliability with source and reviewer provenance; 0 approved at foundation |
| BT-007 | P2 / MEDIUM | Blue / Purple | OPEN | Blue synthetic alert fixtures contain event IDs or explicit insufficient-evidence outcomes and measurable false-positive/false-negative expectations |
| BT-008 | P2 / MEDIUM | Blue / Green | OPEN | Release evidence ledgers updated from frozen final SHA; historical results clearly segregated from latest commit and vendor skill archives |
| BT-009 | P2 / MEDIUM | Blue / Purple | OPEN | Purple optional library and integration source drift compared without treating library as runtime dependency; no blind cross-branch promotion |
| BT-010 | P2 / DEFENSIVE DESIGN | Blue / Green | OPEN | Cloud-only detection coverage matrix for auth failures, forged evidence, revocation, handoff violations, CI/source integrity and missing tool denials |
| BT-011 | P2 / DEFENSIVE DESIGN | Blue / Orange | OPEN | Redacted incident response playbook: identify evidence source, triage, authorization, preservation, escalate, containment approval, close with receipts |
| BT-012 | P3 / WEEKLY HYGIENE | Blue / Head | RECURRING_WHEN_INVOKED | New dated log, refreshed exact refs, closed/reopened finding changes, stale-evidence check and a truthful handoff; no invented no-session monitoring |

## Task disposition rules

- **OPEN**: technically actionable but not yet executed/verified.
- **IN_PROGRESS**: bounded active work, with live session evidence.
- **IMPLEMENTED_UNVERIFIED**: patch written, execution/acceptance evidence absent.
- **TESTED_AT_SHA**: an actual run explicitly linked to a particular immutable commit; not a later SHA.
- **BLOCKED_EXTERNAL_HOST**: cannot run without unsupported/unapproved host action.
- **RESOLVED_VERIFIED**: exact-SHA evidence meets acceptance and distinct logical review accepts.
- **DEFERRED_BY_HEAD**: explicit Head scope or budget decision with reason, not silently dropped.

## How to select work

Head picks the next single Blue assignment based on severity, safety, tool access, expected impact, current source and dependency status; no enforced rigid order. A specialist patch stays isolated on the Blue branch until Head/Development HQ separately accepts a promotion. These tasks coexist with master [Issue #8](https://github.com/vixttha/Color-Team-OPS/issues/8) but cannot substitute its acceptance gates or authorize a main/integration merge.

## Blockers never treated as completed

BT-005 and BT-006 cannot be closed by adding a document, fixture or Python test. Verified real host/independent review is necessary. A source-only mock can be useful but must be labeled `SYNTHETIC` or `TESTED_REFERENCE_ONLY`.
