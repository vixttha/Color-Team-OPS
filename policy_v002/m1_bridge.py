"""M1 reference alignment: Yellow journal ↔ D2 policy. READ ONLY, NOT AN ISSUER.

Even a positive result from a synthetic D2 TrustAdapter is UNVERIFIED here.
A protected cloud host must separately authenticate grants, identities,
provider receipts and durable revocation before production completion.
"""
from __future__ import annotations
from dataclasses import dataclass
from functools import wraps
from datetime import datetime, timezone
from typing import Mapping
from .host_runtime import HostRejected, digest
from .verifier import evaluate_completion
from .repair_protocol import verify_repair_chain

VERSION = "cto-v002-m1-bridge-6"

def _check_unattested_repair_history(state, history, work_orders, worker_events):
    """Detect contradictory retry claims BEFORE the D2 reference gate.

    A well-shaped trace is still UNVERIFIED: the development journal is not a
    protected role/consent issuer and D2 has no repair transition attestations.
    """
    records = state.get("repair_history")
    if not isinstance(records, list) or not records:
        return "REPAIR_HISTORY_INVALID"
    if not isinstance(history, list):
        return "REPAIR_EVENT_JOURNAL_MISMATCH"
    events = [(i, event) for i, event in enumerate(history)
              if isinstance(event, dict) and event.get("kind") == "REPAIR_ORDERED"]
    if len(events) != len(records):
        return "REPAIR_EVENT_JOURNAL_MISMATCH"
    if (any(not isinstance(event, dict) for event in history)
        or len({event.get("event_id") for event in history}) != len(history)):
        return "REPAIR_EVENT_REPLAY"
    orders = {order.get("task_id"): order for order in work_orders if isinstance(order, dict)}
    workers = {worker.get("task_id"): worker for worker in worker_events if isinstance(worker, dict)}
    if len(orders) != len(work_orders) or len(workers) != len(worker_events):
        return "REPAIR_TASK_SCOPE_MISMATCH"
    receipt_history = state.get("used_receipts", [])
    if not isinstance(receipt_history, list) or len(receipt_history) != len(set(receipt_history)):
        return "REPAIR_RECEIPT_REPLAY"
    consumed = set()
    counts = {}
    for record, (i, event) in zip(records, events):
        if (not isinstance(record, dict) or i < 2 or i + 1 >= len(history)
            or not isinstance(record.get("event_id"), str)
            or not isinstance(record.get("prior_receipt"), str)
            or not record["prior_receipt"]):
            return "REPAIR_EVENT_JOURNAL_MISMATCH"
        task_id = record.get("task_id")
        if task_id not in orders or task_id not in workers:
            return "REPAIR_TASK_SCOPE_MISMATCH"
        counts[task_id] = counts.get(task_id, 0) + 1
        if (type(record.get("repair_number")) is not int
            or record["repair_number"] != counts[task_id]
            or counts[task_id] > orders[task_id].get("max_local_repairs", -1)
            or counts[task_id] > state.get("max_local_repairs", 0)):
            return "REPAIR_BUDGET_EXCEEDED"
        if (event.get("event_id") != record["event_id"]
            or event.get("subject") != state.get("head_subject")
            or record.get("head_subject") != state.get("head_subject")
            or history[i-1].get("kind") != "WORKER_REPORTED"
            or history[i+1].get("kind") != "WORKER_REPORTED"
            or history[i-1].get("subject") != history[i+1].get("subject")):
            return "REPAIR_EVENT_JOURNAL_MISMATCH"
        receipt = record["prior_receipt"]
        if receipt in consumed or receipt not in receipt_history:
            return "REPAIR_RECEIPT_REPLAY"
        consumed.add(receipt)
    if any(type(w.get("local_repairs")) is not int
           or w["local_repairs"] != counts.get(w["task_id"], 0)
           for w in workers.values()):
        return "REPAIR_COUNT_MISMATCH"
    return None



PHASES = ("VALIDATE", "INTERNAL_AUDIT")
EVENTS = ("DISPATCH", "WORKER_REPORTED", "VALIDATION_PASSED", "AUDIT_PASSED")
TRANSITIONS = (
    ("HEAD_READY", "WORKER_ACTIVE", "HEAD"),
    ("WORKER_ACTIVE", "VALIDATION_PENDING", "WORKER"),
    ("VALIDATION_PENDING", "INTERNAL_AUDIT_PENDING", "VALIDATOR"),
    ("INTERNAL_AUDIT_PENDING", "HEAD_DECISION", "INTERNAL_AUDITOR"),
)
ACTION_MAP = {"read": "read", "analyze": "inspect"}

@dataclass(frozen=True)
class M1Finding:
    status: str
    code: str
    source_sha: str
    policy_verdict: str = "NOT_RUN"

def _fail_closed(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception:
            # Never turn malformed untrusted records into a crash or a PASS.
            mission = kwargs.get("mission")
            sha = mission.get("source_sha", "") if isinstance(mission, dict) else ""
            return M1Finding("BLOCKED", "MALFORMED_REFERENCE_RECORD", sha)
    return wrapped


@_fail_closed
def reconcile_reference(*, mission, work_orders, worker_events, evidence_claims,
                        gate_records, transition_events, head_decision,
                        journal=None, event_links=(), trust=None, repair_events=(),
                        clock=lambda: datetime.now(timezone.utc).timestamp()):
    sha = mission.get("source_sha", "") if isinstance(mission, dict) else ""
    def result(status, code, policy="NOT_RUN"):
        return M1Finding(status, code, sha, policy)
    if journal is None:
        return result("UNVERIFIED", "JOURNAL_UNAVAILABLE")
    if not isinstance(mission, dict) or not isinstance(mission.get("allowed_actions"), list):
        return result("BLOCKED", "INVALID_MISSION")
    if (mission.get("mode") != "SKILLS_ONLY"
        or mission.get("requires_global_exclusive_write") is True
        or any(a not in ACTION_MAP for a in mission["allowed_actions"])):
        return result("CAPABILITY_BLOCKED", "PROTECTED_HOST_REQUIRED")
    if (mission.get("cloud_only") is not True or mission.get("runner_required") is not False
        or mission.get("state") != "AUTHORIZED"):
        return result("BLOCKED", "INVALID_MISSION_SCOPE")
    try:
        state = journal.read(mission["mission_id"])
        history = journal.history(mission["mission_id"])
    except (KeyError, OSError, TypeError, ValueError, HostRejected):
        return result("UNVERIFIED", "JOURNAL_INTEGRITY_UNVERIFIED")
    if not isinstance(state, dict) or not isinstance(history, list):
        return result("UNVERIFIED", "JOURNAL_UNAVAILABLE")
    if state.get("revoked") is not False:
        return result("BLOCKED", "GRANT_REVOKED")
    try:
        if type(state.get("expires_at")) is not int or int(clock()) >= state["expires_at"]:
            return result("BLOCKED", "GRANT_EXPIRED")
    except (TypeError, ValueError, OverflowError):
        return result("UNVERIFIED", "CLOCK_UNAVAILABLE")
    if (state.get("phase") != "HEAD_DECISION" or state.get("task") is not None
        or state.get("completion") is not None):
        return result("BLOCKED", "HEAD_PHASE_INVALID")
    match = {"mission_id": "mission_id", "repository": "repository",
             "source_sha": "source_sha", "authorized_branch": "branch",
             "max_handoffs": "max_handoffs"}
    if any(mission.get(a) != state.get(b) for a, b in match.items()):
        return result("BLOCKED", "MISSION_SCOPE_MISMATCH")
    for left, right in (("allowed_teams", "allowed_teams"),
                        ("required_teams", "required_teams"),
                        ("acceptance_criteria", "criteria")):
        a, b = mission.get(left), state.get(right)
        if (not isinstance(a, list) or not isinstance(b, list)
            or any(not isinstance(x, str) for x in a+b)
            or len(set(a)) != len(a) or len(set(b)) != len(b) or set(a) != set(b)):
            return result("BLOCKED", "MISSION_SCOPE_MISMATCH")
    if not all(ACTION_MAP[a] in state.get("allowed_actions", []) for a in mission["allowed_actions"]):
        return result("BLOCKED", "ACTION_SCOPE_MISMATCH")
    keys = ("mission_id", "repository", "branch", "source_sha", "allowed_teams",
            "required_teams", "allowed_actions", "criteria", "max_handoffs")
    try:
        intent = {key: state[key] for key in keys}
        if "max_local_repairs" in state:
            intent["max_local_repairs"] = state["max_local_repairs"]
        if (not state.get("head_subject") or not state.get("consent_id")
            or state.get("consent_digest") != digest(intent)):
            return result("BLOCKED", "CONSENT_MISMATCH")
    except (KeyError, ValueError, TypeError):
        return result("BLOCKED", "CONSENT_MISMATCH")
    records = (work_orders, worker_events, evidence_claims, gate_records,
               transition_events, event_links)
    if any(not isinstance(x, (tuple, list)) for x in records):
        return result("BLOCKED", "RECORDS_INVALID")
    # Preserve explicit optional signed repair scope without turning an
    # un-modeled retry into a fake pair of verified transition events.
    if state.get("max_local_repairs",0) > mission.get("max_local_repairs",-1):
        return result("BLOCKED", "REPAIR_CONSENT_SCOPE_MISMATCH")
    if state.get("repair_history"):
        conflict = _check_unattested_repair_history(state, history, work_orders, worker_events)
        if conflict is not None:
            return result("BLOCKED", conflict)
        # D2 repair protocol requires separate authenticated repair events and
        # two protected transition attestations per retry. Synthetic fixtures
        # can exercise the contract but can never authenticate production host.
        if trust is None or not repair_events:
            return result("UNVERIFIED", "REPAIR_EVENT_TRACE_UNAVAILABLE")
        status, code = verify_repair_chain(
            mission=mission, work_orders=work_orders, worker_events=worker_events,
            evidence_claims=evidence_claims, repair_events=repair_events, trust=trust)
        if status != "PASS":
            return result(status, "D2_" + code)
        return result("UNVERIFIED", "D2_REPAIR_REFERENCE_NOT_PRODUCTION_AUTH", "PASS")
    # v4 interprets the exact ordered Yellow event journal. Every completed task
    # contributes four transitions and two validation/audit gate observations.
    # There is ONE D2 aggregate Validate and Audit record at Head closure.
    count = len(work_orders)
    if (count < 1 or len(worker_events) != count or len(evidence_claims) != count
        or len(gate_records) != 2 or len(transition_events) != 4*count
        or len(event_links) != 4*count or len(history) != 1+4*count
        or len(state.get("gates", [])) != 2*count):
        return result("UNVERIFIED", "M1_TRACE_OR_MIGRATION_UNAVAILABLE")
    if count - 1 > state["max_handoffs"]:
        return result("BLOCKED", "HANDOFF_BUDGET_EXCEEDED")
    if (state.get("revision") != 1+4*count
        or [e.get("revision") for e in history] != list(range(1,2+4*count))
        or history[0].get("kind") != "CONSENT_GRANTED"
        or history[0].get("consent_id") != state["consent_id"]
        or history[0].get("subject") != state["head_subject"]):
        return result("BLOCKED", "JOURNAL_TRACE_MISMATCH")
    if not all(isinstance(x, dict) for x in
               list(work_orders)+list(worker_events)+list(evidence_claims)):
        return result("BLOCKED", "RECORDS_INVALID")
    tasks = [w.get("task_id") for w in work_orders]
    teams = [w.get("team") for w in work_orders]
    receipts = [c.get("provider_record_id") for c in evidence_claims]
    claims = [c.get("claim_id") for c in evidence_claims]
    if (any(not isinstance(x, str) or not x for x in tasks+teams+receipts+claims)
        or len(set(tasks)) != count or len(set(receipts)) != count
        or len(set(claims)) != count
        or state.get("used_task_ids") != tasks
        or state.get("used_receipts") != receipts):
        return result("BLOCKED", "TASK_OR_RECEIPT_MISMATCH")
    if not set(teams).issubset(set(state.get("approved_teams", []))):
        return result("BLOCKED", "WORK_INCOMPLETE")
    if (set(state.get("approved_teams", [])) != set(teams)
        or len(state.get("approved_teams", [])) != len(set(teams))):
        return result("BLOCKED", "TEAM_SUMMARY_MISMATCH")
    used_criteria = set()
    previous_event_ids = set()
    for n, (order, worker, claim) in enumerate(zip(work_orders,worker_events,evidence_claims)):
        task = tasks[n]
        receipt = receipts[n]
        if (order.get("mission_id") != mission["mission_id"]
            or order.get("source_sha") != sha
            or order.get("authorization_ref") != mission.get("authorization_ref")
            or worker.get("mission_id") != mission["mission_id"]
            or worker.get("source_sha") != sha):
            return result("BLOCKED", "TASK_PROVENANCE_MISMATCH")
        if (worker.get("task_id") != task or worker.get("team") != order.get("team")
            or worker.get("outcome") != "DONE"
            or worker.get("evidence_claim_ids") != [claims[n]]
            or claim.get("mission_id") != mission["mission_id"]
            or claim.get("task_id") != task or claim.get("source_sha") != sha):
            return result("BLOCKED", "TASK_OR_RECEIPT_MISMATCH")
        repairs = worker.get("local_repairs")
        if (type(repairs) is not int or repairs < 0
            or type(order.get("max_local_repairs")) is not int
            or repairs > order["max_local_repairs"]
            or repairs > mission.get("max_local_repairs", -1)):
            return result("BLOCKED", "REPAIR_BUDGET_EXCEEDED")
        # A v3 bridge cannot invent authenticated repair transitions or omit
        # intermediary failed receipts. A positive repair count needs a future
        # explicit versioned repair-event contract, not just a label.
        if repairs:
            return result("UNVERIFIED", "REPAIR_EVENT_TRACE_UNAVAILABLE")
        criteria_ids = order.get("criteria_ids", [])
        if (not isinstance(criteria_ids, list) or not criteria_ids
            or not set(criteria_ids).issubset(set(state["criteria"]))):
            return result("BLOCKED", "TASK_CRITERION_SCOPE_MISMATCH")
        used_criteria.update(criteria_ids)
        for phase_idx, phase in enumerate(PHASES):
            g = state["gates"][2*n+phase_idx]
            if (not isinstance(g, dict) or g.get("phase") != phase
                or g.get("task_id") != task or g.get("sha") != sha
                or g.get("criterion") not in criteria_ids
                or g.get("evidence_ref") != receipt or g.get("verdict") != "PASS"
                or not isinstance(g.get("subject"), str) or not g["subject"]):
                return result("BLOCKED", "GATE_RECEIPT_MISMATCH")
            if g["subject"] != history[3+4*n+phase_idx].get("subject"):
                return result("BLOCKED", "GATE_ACTOR_LINK_MISMATCH")
        for i, kind in enumerate(EVENTS):
            index = 1 + 4*n + i
            event, link, transition = history[index], event_links[4*n+i], transition_events[4*n+i]
            if (not isinstance(event, dict) or not isinstance(link,dict)
                or not isinstance(transition,dict)
                or event.get("kind") != kind
                or link.get("journal_event_id") != event.get("event_id")
                or link.get("journal_revision") != event.get("revision")
                or link.get("transition_id") != transition.get("transition_id")
                or transition.get("mission_id") != mission["mission_id"]
                or transition.get("source_sha") != sha
                or link.get("task_id") != task or link.get("source_sha") != sha):
                return result("BLOCKED", "TRANSITION_LINK_MISMATCH")
            if not isinstance(event.get("event_id"), str) or not event["event_id"]:
                return result("BLOCKED", "JOURNAL_EVENT_ID_INVALID")
            if event["event_id"] in previous_event_ids:
                return result("BLOCKED", "JOURNAL_EVENT_REPLAY")
            previous_event_ids.add(event["event_id"])
            expected = (("HEAD_READY" if n == 0 else "HEAD_DECISION"),
                        "WORKER_ACTIVE", "HEAD") if i == 0 else TRANSITIONS[i]
            if ((transition.get("from_phase"), transition.get("to_phase"),
                 transition.get("actor")) != expected):
                return result("BLOCKED", "TRANSITION_ROLE_MISMATCH")
            if not isinstance(event.get("subject"),str) or not event["subject"]:
                return result("BLOCKED", "JOURNAL_ACTOR_MISSING")
            if i == 0 and event["subject"] != state["head_subject"]:
                return result("BLOCKED", "HEAD_DISPATCH_ACTOR_MISMATCH")
    if (not set(state.get("required_teams", [])).issubset(set(teams))
        or not set(state.get("criteria", [])).issubset(used_criteria)
        or set(state.get("validated_criteria", [])) != set(state["criteria"])):
        return result("BLOCKED", "WORK_INCOMPLETE")
    if any(not isinstance(g, dict) for g in gate_records):
        return result("BLOCKED", "AGGREGATE_GATE_INVALID")
    gates = {g.get("phase"):g for g in gate_records}
    if len(gates) != 2 or set(gates) != set(PHASES):
        return result("BLOCKED", "AGGREGATE_GATE_INVALID")
    for g in gates.values():
        if (g.get("mission_id") != mission["mission_id"]
            or g.get("verdict") != "PASS" or g.get("source_sha") != sha
            or not isinstance(g.get("evidence_refs"),list)
            or set(g["evidence_refs"]) != set(claims)
            or set(g.get("criterion_ids", [])) != set(state["criteria"])):
            return result("BLOCKED", "AGGREGATE_GATE_INVALID")
    if (not isinstance(head_decision, dict)
        or head_decision.get("mission_id") != mission["mission_id"]
        or head_decision.get("source_sha") != sha
        or head_decision.get("actor") != "HEAD"
        or head_decision.get("action") not in ("COMPLETE", "BLOCKED_EXTERNAL_APPROVAL")
        or head_decision.get("validation_record_ref") != gates["VALIDATE"].get("record_id")
        or head_decision.get("audit_record_ref") != gates["INTERNAL_AUDIT"].get("record_id")):
        return result("BLOCKED", "HEAD_DECISION_MISMATCH")
    if trust is None:
        return result("UNVERIFIED", "REFERENCE_ALIGNED_AUTHORITY_UNVERIFIED")
    try:
        v = evaluate_completion(mission=mission, work_orders=work_orders,
            worker_events=worker_events, evidence_claims=evidence_claims,
            gate_records=gate_records, transition_events=transition_events,
            head_decision=head_decision, trust=trust)
    except Exception:
        return result("UNVERIFIED", "POLICY_PROVIDER_UNAVAILABLE")
    if v.status != "PASS":
        return result(v.status, "D2_" + v.code, v.status)
    return result("UNVERIFIED", "D2_REFERENCE_PASS_NOT_PRODUCTION_AUTH", "PASS")
