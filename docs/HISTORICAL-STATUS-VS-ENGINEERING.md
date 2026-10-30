# Purple — Historical idea status versus engineering source readback

**Read-only, dated observation: 2026-10-30.** This note is a **separate snapshot**, not an update to 41 original JSON records or an official current-state claim.

**Historical library source:** `feature/v0.0.2-idea-feature-library-purple` at `05f768cafabfb2189f9f0992f53223fde3ad87fe`. Source catalog provenance originates at `b59bd2b7fa289b77cec7f9c2f42eedfcccd2449a`.

**Engineering candidate inspected:** `integration/v0.0.2-master-single-thread` at `984ba437bae41f26b2ade703c704ffcd1c8347ba`. Other development branches may differ and require independent SHA readback.

The 36 imported IDEA records retain original captured/adopted **idea direction**, and all still say `not_planned/untested` as the **original discussion snapshot**. The five umbrella FEAT records retain `proposed/not_planned/NOT_ASSERTED`. **Do not interpret those frozen historical labels as proof that engineering has not started**, and do not rewrite them on inference.

| Source feature | Engineering source **present at inspected SHA** | Still NOT asserted |
| --- | --- | --- |
| FEAT-000001 Team Directory | `policy_v002/team_directory.py`, `registry/v0.0.2/teams.json`, `tests/test_v002_directory.py` | Real-host operational acceptance and shipped status |
| FEAT-000002 Typed Handoffs | `contracts/v0.0.2/worker-event.schema.json`, `policy_v002/verifier.py`, `tests/test_v002_contracts.py` | Fully authenticated live cross-team handoff |
| FEAT-000003 Adaptive Routing | `policy_v002/route_advice.py`, `tests/test_v002_route_advice.py` | Live authorized automatic dispatch or 99% routing accuracy |
| FEAT-000004 Evaluation Lab | `policy_v002/eval_lab.py`, `tests/test_v002_eval_lab.py` | Executed independent 270-case specialist evaluation or a verified score |
| FEAT-000005 Host Authority | `policy_v002/host_authority.py`, `policy_v002/host_runtime.py`, `tests/test_v002_authority.py` | Deployed issuer, durable protected host, production credentials or accepted release |

**Important:** Existence of source code, tests, or a research report is *not* evidence that tests executed successfully or acceptance passed. This note reflects file presence at that exact SHA only. It does not claim full end-to-end performance.

### How to read status without a contradiction
- Historical `ideas/records` and `features/records` are immutable evidence of what was originally discussed and proposed.
- Actual implementation must be re-observed from a separately identified current branch + SHA and accepted test reports.
- The official v0.0.2 release state, consent, operational status, and permission decisions belong outside these optional libraries.
- If these sources disagree, report **HISTORICAL_SNAPSHOT + CURRENT_ENGINEERING_UNVERIFIED**, not a fabricated merged completion status.

For detailed interactions, adverse combinations and unresolved gates, see `docs/IDEA-FEATURE-SYNERGY-CONFLICT-AUDIT-2026-10-30.md`.
