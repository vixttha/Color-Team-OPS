"""D2 read-only cross-record policy verifier.

IMPORTANT: A TrustAdapter is a *trusted backend boundary*. A fake/test adapter
can drive deterministic tests but cannot authenticate real GitHub or ChatGPT
actors. No authorization is granted and no mutations are performed here.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import FrozenSet, Optional, Protocol, Sequence
import json

from jsonschema import Draft202012Validator

SCHEMAS = Path(__file__).resolve().parents[1] / "contracts" / "v0.0.2"


@dataclass(frozen=True)
class Authorization:
    mission_id: str
    authorization_ref: str
    repository: str
    branch: str
    source_sha: str
    principal_id: str
    teams: FrozenSet[str]
    actions: FrozenSet[str]
    approved_head_decisions: FrozenSet[str]
    approved_task_ids: FrozenSet[str]
    valid: bool


@dataclass(frozen=True)
class Observation:
    mission_id: str
    task_id: str
    provider: str
    provider_record_id: str
    source_sha: str
    criterion_id: str
    outcome: str  # PASS, FAIL, or UNVERIFIED: verified by the adapter


@dataclass(frozen=True)
class GateAttestation:
    mission_id: str
    record_id: str
    phase: str
    verdict: str
    source_sha: str
    criterion_ids: FrozenSet[str]
    evidence_refs: FrozenSet[str]
    role: str
    verifier_ref: str
    valid: bool


@dataclass(frozen=True)
class TransitionAttestation:
    mission_id: str
    transition_id: str
    from_phase: str
    to_phase: str
    actor: str
    source_sha: str
    task_id: str
    team: str
    valid: bool


@dataclass(frozen=True)
class MissionSnapshot:
    mission_id: str
    phase: str
    active_team: Optional[str]
    active_task_id: Optional[str]
    source_sha: str
    valid: bool


class TrustAdapter(Protocol):
    """Implement ONLY inside a trusted host/cloud integration.

    This verifier cannot prove that an adapter genuinely checked permissions,
    provider receipts, or gate provenance. An arbitrary caller-supplied adapter
    does not turn an LLM-supplied claim into trusted evidence.
    """
    def authorization(self, mission_id: str, authorization_ref: str) -> Optional[Authorization]: ...
    def current_sha(self, repository: str, branch: str) -> Optional[str]: ...
    def authorized_dispatch(self, mission_id: str, task_id: str, team: str, source_sha: str) -> bool: ...
    def resolve_observation(self, provider: str, provider_record_id: str) -> Optional[Observation]: ...
    def authenticate_gate(self, record_id: str) -> Optional[GateAttestation]: ...
    def exclusive_write_enforced(self, mission_id: str, repository: str, branch: str) -> bool: ...
    def authenticate_transition(self, transition_id: str) -> Optional[TransitionAttestation]: ...
    def mission_snapshot(self, mission_id: str) -> Optional[MissionSnapshot]: ...


@dataclass(frozen=True)
class Verdict:
    status: str
    code: str
    message: str
    source_sha: str = ""


def _answer(status: str, code: str, message: str, sha: str = "") -> Verdict:
    return Verdict(status, code, message, sha)


def _shape(name: str, value: dict) -> bool:
    if not isinstance(value, dict):
        return False
    schema = json.loads((SCHEMAS / (name + ".schema.json")).read_text(encoding="utf-8"))
    return Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER).is_valid(value)


def _unique(items: Sequence[dict], key: str) -> bool:
    ids = [d[key] for d in items]
    return len(ids) == len(set(ids))


def evaluate_completion(
    *,
    mission: dict,
    work_orders: Sequence[dict],
    worker_events: Sequence[dict],
    evidence_claims: Sequence[dict],
    gate_records: Sequence[dict],
    transition_events: Sequence[dict],
    head_decision: dict,
    trust: TrustAdapter,
) -> Verdict:
    """Evaluate an internal mission closure; READ ONLY.

    No external identity or action permission is certified by Python shape.
    A future trusted host must construct and protect the TrustAdapter.
    Decisions are advisory, not executable capability tokens or release approval.
    """
    sha = mission.get("source_sha", "") if isinstance(mission, dict) else ""
    if any(not isinstance(seq, (list, tuple)) for seq in (
        work_orders, worker_events, evidence_claims, gate_records, transition_events
    )):
        return _answer("BLOCKED", "INVALID_SHAPE", "Record collections must be arrays.", sha)
    if not _shape("mission", mission) or not all(
        _shape(name, data)
        for name, seq in (
            ("work-order", work_orders), ("worker-event", worker_events),
            ("evidence-claim", evidence_claims), ("gate-record", gate_records),
            ("transition-event", transition_events)
        ) for data in seq
    ) or not _shape("head-decision", head_decision):
        return _answer("BLOCKED", "INVALID_SHAPE", "Contract schema validation failed.", sha)

    if head_decision["action"] not in ("COMPLETE", "BLOCKED_EXTERNAL_APPROVAL"):
        return _answer("BLOCKED", "NOT_COMPLETION_ACTION", "No request to close an internal mission.", sha)
    if mission["state"] != "AUTHORIZED":
        return _answer("BLOCKED", "MISSION_NOT_AUTHORIZED", "Only authorized missions may close.", sha)
    if not mission.get("repository") or not mission.get("authorized_branch") or not sha or not mission.get("authorization_ref"):
        return _answer("BLOCKED", "MISSING_TARGET", "Exact scoped repository, revision and grant reference required.", sha)
    if head_decision["mission_id"] != mission["mission_id"] or head_decision["source_sha"] != sha:
        return _answer("BLOCKED", "DECISION_MISMATCH", "Head decision not bound to this mission and source.", sha)

    required = set(mission["required_teams"])
    allowed = set(mission["allowed_teams"])
    criteria = set(mission["acceptance_criteria"])
    if not required or not required.issubset(allowed):
        return _answer("BLOCKED", "TEAM_SET_INVALID", "Required teams must be a nonempty subset of allowed teams.", sha)
    if len(criteria) != len(mission["acceptance_criteria"]):
        return _answer("BLOCKED", "DUPLICATE_CRITERION", "Acceptance criteria identifiers must be distinct.", sha)
    if not all((_unique(s, k) for s, k in (
        (work_orders, "task_id"), (worker_events, "event_id"), (evidence_claims, "claim_id"),
        (gate_records, "record_id"), (transition_events, "transition_id")
    ))):
        return _answer("BLOCKED", "DUPLICATE_RECORD", "Duplicate record identifiers not permitted.", sha)

    try:
        auth = trust.authorization(mission["mission_id"], mission["authorization_ref"])
        if auth is None:
            return _answer("UNVERIFIED", "AUTH_UNAVAILABLE", "No authenticated authorization observation.", sha)
        if not auth.valid:
            return _answer("BLOCKED", "AUTH_REVOKED", "Authorization invalid or revoked.", sha)
        if (auth.mission_id != mission["mission_id"] or auth.authorization_ref != mission["authorization_ref"]
                or auth.repository != mission["repository"] or auth.branch != mission["authorized_branch"]
                or auth.source_sha != sha or not auth.principal_id):
            return _answer("BLOCKED", "AUTH_SCOPE_MISMATCH", "Trusted authorization mismatches declared mission scope.", sha)
        if (head_decision["decision_id"] not in auth.approved_head_decisions
                or not allowed.issubset(auth.teams)
                or not set(mission["allowed_actions"]).issubset(auth.actions)):
            return _answer("BLOCKED", "NOT_AUTHORIZED", "Head decision, team or action not authenticated.", sha)

        observed_sha = trust.current_sha(auth.repository, auth.branch)
        if observed_sha is None:
            return _answer("UNVERIFIED", "SOURCE_UNAVAILABLE", "Cannot resolve current source revision.", sha)
        if observed_sha != sha:
            return _answer("BLOCKED", "STALE_REVISION", "Current source differs from mission SHA.", sha)
        if mission.get("requires_global_exclusive_write", False):
            if mission["mode"] != "ENFORCED_CLOUD" or not trust.exclusive_write_enforced(
                mission["mission_id"], auth.repository, auth.branch
            ):
                return _answer("CAPABILITY_BLOCKED", "EXCLUSIVE_WRITE_NOT_ENFORCED",
                               "No verified exclusive-write enforcement boundary.", sha)

        # A trusted mission snapshot must place the Head at the decision point.
        # No active Worker can remain at a successful terminal decision.
        snapshot = trust.mission_snapshot(mission["mission_id"])
        if snapshot is None:
            return _answer("UNVERIFIED", "MISSION_STATE_UNAVAILABLE", "Cannot authenticate live Head/Worker phase.", sha)
        if (not snapshot.valid or snapshot.mission_id != mission["mission_id"]
                or snapshot.source_sha != sha or snapshot.phase != "HEAD_DECISION"
                or snapshot.active_team is not None or snapshot.active_task_id is not None):
            return _answer("BLOCKED", "MISSION_STATE_MISMATCH", "Head decision is not at an idle verified phase.", sha)

        # Four attested transitions per bounded work assignment. This makes the
        # worker's identity and sequential stage flow testable; it does not
        # establish global cross-chat exclusivity.
        if len(transition_events) != 4 * len(work_orders) or not work_orders:
            return _answer("BLOCKED", "MISSION_TRACE_INVALID", "Missing or extra stage transitions.", sha)
        for index, order in enumerate(work_orders):
            expected = (
                ("HEAD_READY" if index == 0 else "HEAD_DECISION", "WORKER_ACTIVE", "HEAD"),
                ("WORKER_ACTIVE", "VALIDATION_PENDING", "WORKER"),
                ("VALIDATION_PENDING", "INTERNAL_AUDIT_PENDING", "VALIDATOR"),
                ("INTERNAL_AUDIT_PENDING", "HEAD_DECISION", "INTERNAL_AUDITOR"),
            )
            for offset, (prior, after, role) in enumerate(expected):
                step = transition_events[4 * index + offset]
                if (step["mission_id"] != mission["mission_id"] or step["source_sha"] != sha
                        or (step["from_phase"], step["to_phase"], step["actor"]) != (prior, after, role)):
                    return _answer("BLOCKED", "MISSION_TRACE_INVALID", "Stage chain skips or reorders mission phases.", sha)
                attested_step = trust.authenticate_transition(step["transition_id"])
                if attested_step is None:
                    return _answer("UNVERIFIED", "TRANSITION_UNAUTHENTICATED",
                                   "Cannot authenticate the sequential worker phase event.", sha)
                if (not attested_step.valid or attested_step.mission_id != mission["mission_id"]
                        or attested_step.transition_id != step["transition_id"]
                        or attested_step.source_sha != sha
                        or (attested_step.from_phase, attested_step.to_phase, attested_step.actor) != (prior, after, role)
                        or attested_step.task_id != order["task_id"] or attested_step.team != order["team"]):
                    return _answer("BLOCKED", "TRANSITION_ATTESTATION_MISMATCH",
                                   "Trusted transition does not match the assigned active Worker.", sha)

        work_map = {}
        for order in work_orders:
            if (order["mission_id"] != mission["mission_id"] or order["source_sha"] != sha
                    or order["team"] not in allowed or order["authorization_ref"] != auth.authorization_ref
                    or order["task_id"] not in auth.approved_task_ids
                    or not set(order["scope_actions"]).issubset(set(mission["allowed_actions"]))
                    or not set(order["criteria_ids"]).issubset(criteria)
                    or order["max_local_repairs"] > mission["max_local_repairs"]):
                return _answer("BLOCKED", "WORK_SCOPE_MISMATCH", "Worker assignment outside authorized task scope.", sha)
            if not trust.authorized_dispatch(mission["mission_id"], order["task_id"], order["team"], sha):
                return _answer("BLOCKED", "DISPATCH_NOT_AUTHORIZED", "Head dispatch not authenticated.", sha)
            work_map[order["task_id"]] = order

        if not work_orders or not worker_events:
            return _answer("BLOCKED", "MISSING_WORK", "At least one scoped task and worker event required.", sha)
        events_by_task = {}
        claim_ids = set()
        for event in worker_events:
            order = work_map.get(event["task_id"])
            if (order is None or event["mission_id"] != mission["mission_id"]
                    or event["team"] != order["team"] or event["source_sha"] != sha
                    or event["local_repairs"] > order["max_local_repairs"]
                    or event["outcome"] != "DONE"):
                return _answer("BLOCKED", "WORKER_RESULT_INVALID", "Worker evidence/outcome not accepted for assigned task.", sha)
            if event["task_id"] in events_by_task:
                return _answer("BLOCKED", "MULTIPLE_TASK_RESULTS", "More than one worker result for the same final task.", sha)
            events_by_task[event["task_id"]] = event
            claim_ids.update(event["evidence_claim_ids"])

        if set(events_by_task) != set(work_map) or not required.issubset({w["team"] for w in work_orders}):
            return _answer("BLOCKED", "REQUIRED_WORK_INCOMPLETE", "Required current-SHA team tasks have not completed.", sha)
        # Diagnose duplicate results BEFORE checking missing required-team proof.
        for order in work_orders:
            if order["team"] in required and not events_by_task[order["task_id"]]["evidence_claim_ids"]:
                return _answer("BLOCKED", "REQUIRED_WORK_UNVERIFIED",
                               "Required team task has no source-bound evidence claim.", sha)

        claims = {c["claim_id"]: c for c in evidence_claims}
        if set(claims) != claim_ids:
            return _answer("BLOCKED", "CLAIM_LINKAGE_INVALID", "Worker claims and evidence records do not match.", sha)

        verified_criteria = set()
        positive_evidence = set()
        for claim in evidence_claims:
            order = work_map.get(claim["task_id"])
            event = events_by_task.get(claim["task_id"])
            if (order is None or event is None or claim["mission_id"] != mission["mission_id"]
                    or claim["source_sha"] != sha or claim["claim_id"] not in event["evidence_claim_ids"]):
                return _answer("BLOCKED", "CLAIM_SCOPE_MISMATCH", "Evidence pointer not assigned to current task.", sha)
            obs = trust.resolve_observation(claim["provider"], claim["provider_record_id"])
            if obs is None:
                return _answer("UNVERIFIED", "EVIDENCE_UNAVAILABLE", "Claim lacks a retrievable provider observation.", sha)
            if (obs.mission_id != mission["mission_id"] or obs.task_id != claim["task_id"]
                    or obs.provider != claim["provider"] or obs.provider_record_id != claim["provider_record_id"]
                    or obs.source_sha != sha or obs.criterion_id not in order["criteria_ids"]):
                return _answer("BLOCKED", "EVIDENCE_SCOPE_MISMATCH", "Provider observation mismatches task, criterion, or revision.", sha)
            if obs.outcome == "FAIL":
                return _answer("BLOCKED", "CRITERION_FAILED", "Observed task criterion failed.", sha)
            if obs.outcome != "PASS":
                return _answer("UNVERIFIED", "CRITERION_UNVERIFIED", "Provider did not verify criterion PASS.", sha)
            positive_evidence.add(claim["claim_id"])
            verified_criteria.add(obs.criterion_id)

        if verified_criteria != criteria:
            return _answer("UNVERIFIED", "CRITERIA_NOT_COVERED", "Not all required criteria have verified observations.", sha)

        gates = {g["phase"]: g for g in gate_records}
        if len(gate_records) != 2 or set(gates) != {"VALIDATE", "INTERNAL_AUDIT"}:
            return _answer("BLOCKED", "MISSING_GATE", "Exactly one Validate and one Internal Audit gate required.", sha)
        if (head_decision["validation_record_ref"] != gates["VALIDATE"]["record_id"]
                or head_decision["audit_record_ref"] != gates["INTERNAL_AUDIT"]["record_id"]):
            return _answer("BLOCKED", "GATE_REF_MISMATCH", "Head refers to other gate records.", sha)
        for phase, gate in gates.items():
            if (gate["mission_id"] != mission["mission_id"] or gate["source_sha"] != sha
                    or gate["verdict"] != "PASS" or set(gate["criterion_ids"]) != criteria
                    or not set(gate["evidence_refs"]).issubset(positive_evidence)
                    or not gate["evidence_refs"]):
                return _answer("BLOCKED", "GATE_INVALID", "Gate lacks current-revision PASS, criteria, or verified evidence.", sha)
            attested = trust.authenticate_gate(gate["record_id"])
            if attested is None:
                return _answer("UNVERIFIED", "GATE_UNAUTHENTICATED", "Cannot authenticate the gate record.", sha)
            if (not attested.valid or attested.mission_id != mission["mission_id"]
                    or attested.record_id != gate["record_id"] or attested.phase != phase
                    or attested.role != ("VALIDATOR" if phase == "VALIDATE" else "INTERNAL_AUDITOR")
                    or attested.verdict != "PASS" or attested.source_sha != sha
                    or attested.criterion_ids != criteria
                    or attested.verifier_ref != gate["verifier_ref"]
                    or attested.evidence_refs != set(gate["evidence_refs"])):
                return _answer("BLOCKED", "GATE_ATTESTATION_MISMATCH", "Trusted gate attestation differs from claim.", sha)

        # Detect a revision change during read-only evaluation; this is NOT a
        # transaction and cannot grant a race-free subsequent write.
        final_sha = trust.current_sha(auth.repository, auth.branch)
        if final_sha is None:
            return _answer("UNVERIFIED", "SOURCE_UNAVAILABLE", "Cannot re-check current source revision.", sha)
        if final_sha != sha:
            return _answer("BLOCKED", "REVISION_CHANGED_DURING_CHECK", "Source advanced during verification.", sha)

        if head_decision["action"] == "BLOCKED_EXTERNAL_APPROVAL":
            if head_decision.get("external_approval_required") is not True:
                return _answer("BLOCKED", "RELEASE_GATE_NOT_DECLARED", "External release gate must be explicit.", sha)
            return _answer("BLOCKED_EXTERNAL_APPROVAL", "RELEASE_APPROVAL_OUTSTANDING",
                           "Internal work verified, external release approval remains separately blocked.", sha)
        return _answer("PASS", "INTERNAL_COMPLETION_VERIFIED",
                       "Criteria and both gate records verified through the supplied trusted adapter.", sha)
    except Exception as err:
        return _answer("UNVERIFIED", "TRUST_ADAPTER_ERROR",
                       "Trusted observation failed: " + type(err).__name__, sha)
