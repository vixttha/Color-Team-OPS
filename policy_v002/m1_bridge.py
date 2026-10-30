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

VERSION = "cto-v002-m1-bridge-2"
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
                        journal=None, event_links=(), trust=None,
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
        if (not state.get("head_subject") or not state.get("consent_id")
            or state.get("consent_digest") != digest(intent)):
            return result("BLOCKED", "CONSENT_MISMATCH")
    except (KeyError, ValueError, TypeError):
        return result("BLOCKED", "CONSENT_MISMATCH")
    records = (work_orders, worker_events, evidence_claims, gate_records,
               transition_events, event_links)
    if any(not isinstance(x, (tuple, list)) for x in records):
        return result("BLOCKED", "RECORDS_INVALID")
    count = len(work_orders)
    if (count != 1 or len(worker_events) != 1 or len(evidence_claims) != 1
        or len(gate_records) != 2 or len(transition_events) != 4
        or len(event_links) != 4 or len(history) != 5 or len(state.get("gates", [])) != 2):
        return result("UNVERIFIED", "M1_TRACE_OR_MIGRATION_UNAVAILABLE")
    if (state.get("revision") != 5 or [e.get("revision") for e in history] != [1,2,3,4,5]
        or history[0].get("kind") != "CONSENT_GRANTED"
        or history[0].get("consent_id") != state["consent_id"]
        or history[0].get("subject") != state["head_subject"]):
        return result("BLOCKED", "JOURNAL_TRACE_MISMATCH")
    order, worker, claim = work_orders[0], worker_events[0], evidence_claims[0]
    if any(not isinstance(x, dict) for x in (order,worker,claim)):
        return result("BLOCKED", "RECORDS_INVALID")
    task, receipt = order.get("task_id"), claim.get("provider_record_id")
    if (not isinstance(task,str) or not task or not isinstance(receipt,str) or not receipt
        or state.get("used_task_ids") != [task] or state.get("used_receipts") != [receipt]
        or worker.get("task_id") != task or worker.get("team") != order.get("team")
        or worker.get("outcome") != "DONE" or worker.get("local_repairs") != 0
        or worker.get("evidence_claim_ids") != [claim.get("claim_id")]
        or claim.get("mission_id") != mission["mission_id"]
        or claim.get("task_id") != task or claim.get("source_sha") != sha):
        return result("BLOCKED", "TASK_OR_RECEIPT_MISMATCH")
    for i, phase in enumerate(PHASES):
        gate = state["gates"][i]
        if (not isinstance(gate, dict) or gate.get("phase") != phase
            or gate.get("task_id") != task or gate.get("sha") != sha
            or gate.get("criterion") not in order.get("criteria_ids", [])
            or gate.get("evidence_ref") != receipt or gate.get("verdict") != "PASS"
            or not gate.get("subject")):
            return result("BLOCKED", "GATE_RECEIPT_MISMATCH")
        # This checks journal consistency, not authenticated role independence.
        if gate["subject"] != history[i + 3].get("subject"):
            return result("BLOCKED", "GATE_ACTOR_LINK_MISMATCH")
    for i, kind in enumerate(EVENTS):
        event, link, transition = history[i+1], event_links[i], transition_events[i]
        if (not isinstance(link, dict) or not isinstance(transition,dict)
            or event.get("kind") != kind
            or link.get("journal_event_id") != event.get("event_id")
            or link.get("journal_revision") != event.get("revision")
            or link.get("transition_id") != transition.get("transition_id")
            or link.get("task_id") != task or link.get("source_sha") != sha):
            return result("BLOCKED", "TRANSITION_LINK_MISMATCH")
        if ((transition.get("from_phase"), transition.get("to_phase"), transition.get("actor"))
                != TRANSITIONS[i]):
            return result("BLOCKED", "TRANSITION_ROLE_MISMATCH")
        if not isinstance(event.get("subject"), str) or not event["subject"]:
            return result("BLOCKED", "JOURNAL_ACTOR_MISSING")
        if i == 0 and event["subject"] != state["head_subject"]:
            return result("BLOCKED", "HEAD_DISPATCH_ACTOR_MISMATCH")
    if (not set(state.get("required_teams", [])).issubset(state.get("approved_teams", []))
        or not set(state.get("criteria", [])).issubset(state.get("validated_criteria", []))):
        return result("BLOCKED", "WORK_INCOMPLETE")
    if any(not isinstance(g, dict) for g in gate_records):
        return result("BLOCKED", "AGGREGATE_GATE_INVALID")
    gates = {g.get("phase"):g for g in gate_records}
    if set(gates) != set(PHASES):
        return result("BLOCKED", "AGGREGATE_GATE_INVALID")
    for g in gates.values():
        if (g.get("verdict") != "PASS" or g.get("source_sha") != sha
            or g.get("evidence_refs") != [claim.get("claim_id")]
            or set(g.get("criterion_ids", [])) != set(state["criteria"])):
            return result("BLOCKED", "AGGREGATE_GATE_INVALID")
    if (not isinstance(head_decision, dict) or head_decision.get("source_sha") != sha
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
