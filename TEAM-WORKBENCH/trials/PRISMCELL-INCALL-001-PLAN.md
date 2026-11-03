# PRISMCELL-INCALL-001 — Purple-led live GitHub exchange plan
Date: 2026-11-02. Owner explicitly authorized a single-conversation, sequential five-role INCALL trial, repair and audit.
## Mission boundaries
PrismCell is a workspace template, **not** the installed Color-Team-OPS plugin or Development HQ or Purple Review HQ. No merge/release, no running owner self-hosted runners, no GitHub ruleset/permission edits, no external target testing. Owner permits narrowly scoped team-home and template source repairs plus actual GitHub issue comments.
The SAME authenticated GitHub account executes all comments through one connected tool. Blue/Orange/Purple are **logical roles**, NOT independently authenticated GitHub principals; this trial cannot prove separate-service identity isolation. A GitHub author is an account identity, not a color role.
## Loop, checkpoints, pass criteria
Every specialist step: Head selects → one role Worker → Validate tool/GitHub readback → logical Internal Auditor challenges → Head accepts/repairs/blocks.
1. PURPLE: define baseline, exact source SHA, 9/9 issue inventory; target Orange INCALL #10, sender Blue. Document provenance and safety.
2. BLUE: send ONE real, harmless source finding about existing message schema allowing self-asserted `ACCEPTED` and claimed identity; record posted comment immutable id, URL and source ref in Blue outbox, never change Orange branch.
3. ORANGE: read #10 independently; verify actual GitHub comment metadata, canonical issue, source SHA and finding by rereading source; do NOT authenticate a BLUE service principal by body text. Acknowledge with a new issue comment; write inbox record on Orange branch; do not touch Blue branch.
4. YELLOW: implement narrowed v0.0.1 template hardening on template branch only, with offline tests, schema/validator alignment, non-breaking documented migration and no product pipeline changes; if constrained, report gaps as BLOCKED. Do not mark v0.0.1 security-release accepted without real hosting proof.
5. WHITE only if scope/authority conflicts arise, otherwise optional lightweight adjudication of authorization claims. Preserve exact limitations.
6. PURPLE: verify issue roundtrip, both branch-ledger records, exact template changes + executed tests, unchanged unrelated branch source and genuine observed author. Publish evidence and final conditional verdict.
## Attack model / acceptance
- Reject untrusted claimed sender role and approval status as authorization. Preserve original comment body and author/time in issue metadata.
- Message may be accepted into **review queue** based on actual issue comment metadata and evidence; no autonomous work/branch authority from message.
- Duplicate/comment edit handling must be testable and fail closed; issue comments can be edited/deleted, so observed snapshots aren't immutable external proof.
- Real GitHub delivery/read/ack + two workcell evidence records is observable. Separate authenticated Blue/Orange agent execution and real cross-branch ACL enforcement remain UNVERIFIED.
- Any source SHA copied from prior audits is historical; reread actual target before coding or claiming.
## Inputs reviewed
User-provided Black/Blue/White findings PC-01..PC-09, plus Red nine-finding audit and direct inspection of the v0.0.1 JSON schemas at initial SHA `62d43ef51d362cf064c367158a8d7fce207abd68`. Current product source baseline at kickoff `311290784fe7d5647666f88b328222de62d3cee6` (not a PrismCell implementation target).
## Purple initial Validate / logical Auditor / Head
Validate: GitHub branches and #10/#13 comments fetched; #10 was empty. Connected authenticated GitHub login reports `vixttha`; role impersonation risks cannot be solved by claiming team names.
Logical Auditor: github account identity cannot distinguish colors; branch `protected:false` is not proof of unauthorized access; schema checks are not live host acceptance.
Head decision: ACCEPT scoped harmless real comment, independent issue readback, branch-local records and template-only security hardening. No merge, release or CI runner dispatch.
