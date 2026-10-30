# Solo developer guide — who to call, when and why

**Core principle:** Nine available specialist toolkits, **one active worker**, not nine people/agents concurrently. Use Head to choose the smallest authorized sequence; Validate and Internal Auditor are separate phases for *each* worker. No claim that a recommendation was actually deployed or tested.

## Plain-English team use
| Team | One-sentence job | When to activate | Sample mission request |
| --- | --- | --- | --- |
| Yellow | Build and fix the product | Feature, bug, database, functional test | "Implement an image-upload flow with size/type restrictions and tests." |
| Orange | Secure the code and design | Auth, user data, trust boundary, security flaw | "Review the upload API for authorization and injection and repair confirmed bugs." |
| Green | Run the cloud/pipeline reliably and securely | GitHub CI, Vercel, cloud config, logs, recovery | "Audit deploy workflow, secret leaks, source SHA and safe rollback." |
| Red | Try to exploit it within explicit authorization | Pre-release abuse test, bypass assessment | "Run a scoped non-disruptive IDOR and upload-bypass assessment in staging." |
| Blue | Monitor and defend | Suspicious logs, alert rules, response | "Examine failed-login telemetry and propose/test meaningful alerts." |
| Purple | Prove attack visibility and remediation | Red finding + Blue detection or repaired control | "Link Red's reproducer with Blue's detector and prove before/after behavior." |
| White | Govern exercise scope and safety | Unclear permission, rules or stop trigger | "Determine approved targets, test boundaries and stop conditions." |
| Black | Source real threat intelligence | Vulnerability reports, attacker technique, technology-specific threats | "Find authoritative threats relevant to the exact auth framework versions in our stack." |
| Gray | Simulate ordinary mistakes and misuse | Onboarding/UX, unusual inputs, confused users | "Test incomplete signup, double clicks, failed uploads and recovery with synthetic users." |

## Mission A — start from blank app
1. Head defines scope, acceptance, allowed cloud tools/branch and constraints.
2. Yellow implements a minimal vertical slice and tests.
3. Orange reviews auth/data boundaries if relevant.
4. Gray tests confusing journeys if there is a real UI.
5. Green reviews cloud CI/deploy if release intended.
6. Head completes after each required Worker → Validate → Internal Auditor → Head gate, and only if criteria are met. Do not run all teams just because they exist.

## Mission B — insecure login feature
Head → Orange (threat model and minimal repair) → gate → Red (authorized bypass test) → gate → Blue (relevant attack signal) → gate → Purple (confirm Red-to-Blue coverage) → gate → Head. Yellow may own larger feature refactor; Green may own log/pipeline deployment. Black is optional if threat research relevant.

## Mission C — site outage
Head → Green (provider health/rollback analysis) → gate → Blue (security incident determination if signals exist) → gate → Yellow (actual code regression if proven) → gate → Head. Purple only if a security control or attack correlation requires testing. No invented provider run receipts.

## Mission D — source-grounded research only
Head → Black (dated relevant threat research) → gate → Head. White only for authorization conflict, never as generic text auditor; Internal Auditor remains separate.

## What starts / ends missions
Start with **Head always**, not a color by default. For initial build Yellow is frequent; for threat research Black; for operational malfunction Green; for security incidents Blue; for governance disputes White. End with Head after trusted validation and a logically distinct internal audit; final specialist is driven by acceptance criteria (often Green for cloud release prep or Purple for verified detection), not a universal color order.

## Role of Gold and Black-infrastructure from alternate uploaded model
An executive/program-management 'Gold' competency is an optional lens for **Head** planning/budgets; it is not a ninth replacement specialist and has no independent dispatch rights. Infrastructure Black from competition models can inform **Green** platform skills in this project without replacing Black threat intelligence. The uploaded Gray omission is a concrete loss for solo devs, since user-misuse simulations catch defects that code-centric checks may miss.

## Return format for every specialist
Mission ID; approved scope and tools; team name / focused role competency; exact source SHA (when applicable); work performed vs proposed vs NOT RUN; evidence source and timestamps; failures/unknowns; safe repair suggestion; next team suggestion to Head. Provider outputs remain untrusted until independently verified by allowed mechanisms.

## Guardrails
Cloud-only runtime; optional owner runner only for explicitly allowed development verification; least privilege; no invisible additional teams, parallel writers, automatic merges/production pushes or fabricated tool evidence. Green cloud platform capability is not permission to use user-owned hardware.
