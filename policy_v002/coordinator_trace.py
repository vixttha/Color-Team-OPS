"""Development-only, provider-neutral coordinator trace guards.

NEVER bundled as plugin runtime. Schema-valid model text is NOT an owner grant,
authenticated receipt, independent reviewer, or global cross-chat lock.
"""
from dataclasses import dataclass
from typing import FrozenSet, Optional
import re

SHA = re.compile(r"^[0-9a-fA-F]{40}$")
PHASES = ("HEAD_ASSIGN", "WORKER_RESULT", "VALIDATE",
          "INTERNAL_AUDIT", "HEAD_REVIEW")
ROLES = ("HEAD", "WORKER", "VALIDATOR", "INTERNAL_AUDITOR", "HEAD")
DISPOSITIONS = ("ASSIGN", "DONE", "PASS", "PASS", None)

@dataclass(frozen=True)
class GateResult:
    status: str
    code: str

@dataclass(frozen=True)
class HostObservation:
    """Synthetic input interface; only an actual host may supply trusted facts."""
    mission_id: str
    task_id: str
    repository: str
    branch: str
    source_sha: str
    permitted_actions: FrozenSet[str]
    tool_connected: bool
    owner_approved: bool
    revoked: bool = False
    host_verified: bool = False

def assess_external_action(mission, task_id, action, current_sha,
                           observation: Optional[HostObservation] = None):
    """An advisory eligibility assessment. Never grants or performs a tool call."""
    if not isinstance(mission, dict) or not isinstance(task_id, str) or not task_id:
        return GateResult("BLOCKED", "INVALID_MISSION_OR_TASK")
    if action not in mission.get("allowed_actions", ()):
        return GateResult("BLOCKED", "ACTION_OUTSIDE_MISSION_SCOPE")
    if action in ("analyze", "propose_patch"):
        return GateResult("ADVISORY_ONLY", "USER_SUPPLIED_TEXT_ONLY")
    if observation is None:
        return GateResult("UNVERIFIED", "HOST_AUTHORITY_NOT_OBSERVED")
    if not isinstance(observation, HostObservation):
        return GateResult("BLOCKED", "UNTRUSTED_PERMISSION_OBJECT")
    if (mission.get("state") != "AUTHORIZED"
        or observation.mission_id != mission.get("mission_id")
        or observation.task_id != task_id
        or observation.repository != mission.get("repository")
        or observation.branch != mission.get("authorized_branch")
        or observation.source_sha != mission.get("source_sha")
        or current_sha != observation.source_sha):
        return GateResult("BLOCKED", "STALE_OR_WRONG_AUTHORITY_SCOPE")
    if observation.revoked or not observation.owner_approved or not observation.host_verified:
        return GateResult("UNVERIFIED", "OWNER_OR_HOST_AUTHORITY_NOT_VERIFIED")
    if not observation.tool_connected:
        return GateResult("CAPABILITY_BLOCKED", "CONNECTED_TOOL_UNAVAILABLE")
    if action not in observation.permitted_actions:
        return GateResult("BLOCKED", "HOST_PERMISSION_DENIED")
    # This result is NOT an authorization token or permission to execute.
    return GateResult("ELIGIBLE_HOST_CHECK_ONLY", "LIVE_PERMISSION_RECHECK_REQUIRED")

def validate_logical_chain(mission, events, observed_sha):
    """Check a five-phase per-assignment event ledger without attesting identity."""
    if (not isinstance(mission, dict) or not isinstance(events, (list, tuple))
        or not isinstance(observed_sha, str) or not SHA.fullmatch(observed_sha)
        or not isinstance(mission.get("mission_id"), str)
        or not isinstance(mission.get("allowed_teams"), list)
        or not isinstance(mission.get("max_handoffs"), int)
        or not isinstance(mission.get("max_retries"), int)):
        return GateResult("BLOCKED", "INVALID_TRACE_SCOPE")
    if mission.get("source_sha") != observed_sha:
        return GateResult("BLOCKED", "STALE_SOURCE")
    if mission.get("state") != "AUTHORIZED" or not mission.get("authorization_ref"):
        return GateResult("UNVERIFIED", "INITIAL_MISSION_SCOPE_UNVERIFIED")
    if not events:
        return GateResult("UNVERIFIED", "NO_LOGICAL_EVENTS")
    if len(events) % len(PHASES):
        return GateResult("BLOCKED", "MISSING_WORKER_VALIDATE_AUDIT_OR_HEAD_PHASE")
    seen_ids = set()
    evidence_task = {}
    previous = None
    prev_review = None
    prev_task = None
    prev_team = None
    prev_retry = None
    distinct_handoffs = 0
    for i, event in enumerate(events):
        if not isinstance(event, dict):
            return GateResult("BLOCKED", "INVALID_EVENT_SHAPE")
        w = event.get("workflow")
        if not isinstance(w, dict) or w.get("schema_version") != "cto-v002-logical-chain-1":
            return GateResult("BLOCKED", "INVALID_OR_LEGACY_EVENT")
        phase_index = i % len(PHASES)
        phase = PHASES[phase_index]
        event_id = event.get("event_id")
        task_id = w.get("task_id")
        team = event.get("team")
        refs = event.get("evidence_refs")
        attempt = w.get("repair_attempt")
        if (not isinstance(event_id, str) or not event_id
            or event_id in seen_ids or not isinstance(task_id, str) or not task_id
            or not isinstance(team, str) or team not in mission["allowed_teams"]
            or not isinstance(refs, list) or not refs
            or any(not isinstance(ref, str) or not ref for ref in refs)
            or len(refs) != len(set(refs))
            or type(attempt) is not int or attempt < 0
            or w.get("actor_provenance_ref") in (None, "")
            or w.get("authority_effect") != "NO_EXTERNAL_PERMISSION"
            or w.get("provenance_kind") not in ("MODEL_LOGICAL","CONNECTED_TOOL_CLAIM","USER_SUPPLIED")):
            return GateResult("BLOCKED", "MALFORMED_OR_REPLAYED_EVENT")
        if (event.get("mission_id") != mission["mission_id"]
            or event.get("source_sha") != observed_sha):
            return GateResult("BLOCKED", "CROSS_MISSION_OR_STALE_EVENT")
        # A FAILED/BLOCKED Worker or a missing-evidence gate cannot be
        # promoted to logical completion by writing a PASS label later.
        if event.get("status") != "DONE":
            return GateResult("BLOCKED", "FAILED_OR_BLOCKED_PHASE")
        if event.get("evidence_state") == "MISSING":
            return GateResult("BLOCKED", "MISSING_EVIDENCE_CANNOT_PASS")
        if (w.get("phase") != phase or w.get("actor_role") != ROLES[phase_index]):
            return GateResult("BLOCKED", "OUT_OF_ORDER_OR_FORGED_ROLE_PHASE")
        if (w.get("predecessor_event_id") != previous):
            return GateResult("BLOCKED", "MISSING_OR_REPLAYED_PREDECESSOR")
        if event.get("evidence_state") == "OBSERVED":
            # The text claim has not supplied an authenticated provider receipt.
            return GateResult("UNVERIFIED", "OBSERVED_CLAIM_NEEDS_TRUSTED_HOST")
        for ref in refs:
            if ref in evidence_task and evidence_task[ref] != task_id:
                return GateResult("BLOCKED", "CROSS_TASK_EVIDENCE_REPLAY")
            evidence_task[ref] = task_id
        if phase_index == 0:
            if w.get("review_disposition") != "ASSIGN":
                return GateResult("BLOCKED", "ASSIGNMENT_DISPOSITION_INVALID")
            if i == 0:
                if attempt != 0:
                    return GateResult("BLOCKED", "INITIAL_REPAIR_INDEX_INVALID")
            elif prev_review == "REPAIR":
                if task_id != prev_task or team != prev_team or attempt != prev_retry + 1:
                    return GateResult("BLOCKED", "INVALID_SAME_WORKER_REPAIR")
                if attempt > mission["max_retries"]:
                    return GateResult("BLOCKED", "RETRY_BUDGET_EXCEEDED")
            elif prev_review == "ACCEPT":
                if task_id == prev_task or attempt != 0:
                    return GateResult("BLOCKED", "INVALID_NEXT_TASK_OR_REPLAY")
                distinct_handoffs += 1
                if distinct_handoffs > mission["max_handoffs"]:
                    return GateResult("BLOCKED", "HANDOFF_BUDGET_EXCEEDED")
            else:
                return GateResult("BLOCKED", "PREVIOUS_HEAD_REVIEW_NOT_ACCEPTED")
        else:
            if task_id != current_task or team != current_team or attempt != current_retry:
                return GateResult("BLOCKED", "CROSS_TASK_OR_OVERLAPPING_WORKER")
            needed = DISPOSITIONS[phase_index]
            if needed and w.get("review_disposition") != needed:
                return GateResult("BLOCKED", "MISSING_OR_FAILED_GATE")
            if phase_index == 4:
                if w.get("review_disposition") not in ("ACCEPT", "REPAIR"):
                    return GateResult("BLOCKED", "HEAD_REVIEW_NOT_ACCEPTED")
                prev_review = w["review_disposition"]
                prev_task, prev_team, prev_retry = task_id, team, attempt
        if phase_index == 0:
            current_task, current_team, current_retry = task_id, team, attempt
        previous = event_id
        seen_ids.add(event_id)
    if prev_review == "REPAIR":
        return GateResult("UNVERIFIED", "REPAIR_PENDING_NEXT_CYCLE")
    # PASS here means ONLY structurally coherent logical phase sequencing.
    return GateResult("LOGICAL_VALID_UNVERIFIED", "NO_INDEPENDENT_HOST_AUTHENTICATION")
