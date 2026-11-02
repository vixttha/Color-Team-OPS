# CTO-V002 P0 — Orange trust-scope determination (2026-11-02)

**Mission:** CTO-V002-SINGLE-THREAD. **Head disposition (2026-11-02):** Owner has resolved P0 initial product scope: portable cloud-only skills-only; no dedicated protected backend is mandatory. **Release authorization:** NOT GRANTED. **Baseline source reviewed:** `9b6c0eedf6b577dcce1f516c58c7a1c2ad953315`.

## Evidence and controlling authority

- `docs/CONSTITUTION.md` L1–L10 (L1 cloud-only, L2 optional development runners, L3 host compatibility conditional, L4 bounded actions, L5 actual grants, L6 evidence, L7 stage separation, L8 fail-closed, L9 portability, L10 release review).
- [Issue #8](https://github.com/vixttha/Color-Team-OPS/issues/8), single-thread mission and cross-cutting *conditional* protected-host gate. Existing `docs/V002-MASTER-HEAD-PREFLIGHT.md`, `docs/V002-MASTER-RELEASE-GATES.json`, `policy_v002/verifier.py` and `policy_v002/host_runtime.py`.
- `skills/mission-control/SKILL.md`, `skills/ops-director/SKILL.md`, `skills/verification-gate/SKILL.md`, `docs/V002-M1-REPAIR-EXTENSION.md`.
- Canonical Plugin Creator readback on 2026-11-02: `plugins_6ae3edf1ea4c819182f275592273e2cc`, **private v0.0.1**; no v0.0.2 release.

## Capability classification

| Capability | v0.0.2 classification | Acceptance boundary |
| --- | --- | --- |
| 1. Portable skills-only one-thread logical Head → Worker → Validate → logical Internal Auditor → Head | **Mandatory for v0.0.2**; supported by source guidance; actual installed v0.0.2 host trial **NOT RUN** | Host must use the three existing coordinators, nine specialist skills, one Worker at a time, bounded repair, honest stop; no fabricated identities or tools |
| 2. Actual provider-executed specialist tool actions | **Mandatory only when an authorized tool-backed action is claimed**; otherwise skills-only advice or CAPABILITY_BLOCKED | Actual connected tool permission, observed call and exact source/receipt; metadata never grants access |
| 3. Protected user consent and authenticated mission grants | **Mandatory only for a separately approved protected-host mode / privileged guarantees**. Not a portable Markdown skill capability | Authenticated issuer, audience/scope/expiry/revocation, provider-neutral adapter and protected grant receipts; otherwise UNVERIFIED |
| 4. D2 versioned repair-transition and prior/next receipt binding | **Mandatory engineering/source gate P1**; *production authenticity* mandatory if protected-host mode claimed | Code, schemas, fail-closed tests + exact SHA; only real protected issuer may certify grant/transition validity; synthetic reference may test shape but cannot establish host identity |
| 5. Durable revocation, replay-resistant multi-tenant store | **Mandatory only for separately authorized protected-host mode**; skills-only must not claim durable protection | Transactional protected store, trusted issuer and tested revoke/replay behavior; local SQLite is development adapter only |
| 6. Global cross-session exclusive writing | **Future optional unless owner explicitly selects it as required mode**; not present in skills-only | Protected fencing/atomic gateway, real cross-session test. A prompt or local runner cannot prove a global mutex |
| 7. Unattended persistent cloud execution | **Future optional, not a runtime guarantee of v0.0.2** | Separate explicit authorization, managed cloud agent/service, budgets and monitoring; do not imply from one-thread continuation |

**OWNER DECISION RESOLVED 2026-11-02 (P0-DEC-01):** The initial v0.0.2 must be **portable, cloud-only and skills-only**, with no mandatory protected host service, billable cloud backend, global cross-session lock or unattended server. The owner clarified this explicitly in [Issue #8, comment 6589225030](https://github.com/vixttha/Color-Team-OPS/issues/8#issuecomment-6589225030), reaffirmed in [comment 6589322069](https://github.com/vixttha/Color-Team-OPS/issues/8#issuecomment-6589322069) and in the latest owner master directive. This resolves the earlier open architecture choice; the older paragraph must not be interpreted as current. All connected provider actions still require real host-issued permissions. Unsupported protected claims stay `UNVERIFIED`/`CAPABILITY_BLOCKED`. D2's versioned reference-contract negative tests remain mandatory engineering. Browser-host functioning and independent M4 evaluations **remain hard acceptance**; this clarification does not waive them.

## Orange security challenge

1. A D2 adapter supplied from a model-generated JSON file or GitHub comment can assert `valid=True` without authenticated issuance; it **must not** authorize real tool actions.
2. A matching source SHA/CI PASS proves the source under test, *not* a valid user grant, consent, tenant isolation, durable revocation or internal-auditor identity.
3. `SQLiteDevelopmentJournal` and its hash chain do not resist a privileged DB attacker and cannot serve as a global cross-chat writer lock.
4. Even perfect static capability routing cannot authenticate provider dispatch or 270 real independent model trials.

**Separate logical Internal Auditor:** Examined these claims against the constitution/Issue #8 and deliberately rejects any implied hosted authority or waived trial requirements. Supports the conditional classification, *not* a release PASS. No tenth team, fourth coordinator, vendor dependency, local runtime requirement or product-side Purple Review HQ.

**Head disposition (superseded by explicit owner directive):** `P0 SOURCE_SCOPE_RESOLVED / TECHNICALLY_COMPLETE_PENDING_CURRENT_SHA_NATIVE_TESTS`. Logical Internal Auditor: accept original skills-only law with no unverified protected host guarantees; no release clearance. Continue P2–P5 engineering.
