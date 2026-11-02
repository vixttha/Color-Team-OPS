"""D2 v0.0.2 repair-event reference contract; no production credential issuer.

A positive result asserts only that the SUPPLIED TrustAdapter is internally
consistent. The adapter must be authenticated by a protected external host before
this result can be used for privileged execution or production completion.
"""
from dataclasses import dataclass
from typing import Sequence
import json
from pathlib import Path
from jsonschema import Draft202012Validator


@dataclass(frozen=True)
class RepairAttestation:
    mission_id: str
    repair_id: str
    task_id: str
    team: str
    source_sha: str
    repair_number: int
    head_subject: str
    worker_subject: str
    prior_receipt: str
    next_receipt: str
    valid: bool


def verify_repair_chain(*, mission: dict, work_orders: Sequence[dict],
                        worker_events: Sequence[dict], evidence_claims: Sequence[dict],
                        repair_events: Sequence[dict], trust) -> tuple[str, str]:
    """Returns (PASS|BLOCKED|UNVERIFIED, reason). Does not issue grants."""
    if not isinstance(repair_events, (list, tuple)):
        return "BLOCKED", "REPAIR_EVENTS_INVALID"
    if not isinstance(mission, dict) or not isinstance(work_orders, (list, tuple)):
        return "BLOCKED", "REPAIR_SCOPE_INVALID"
    if any(not isinstance(x, dict) for x in list(work_orders)+list(worker_events)+list(evidence_claims)):
        return "BLOCKED", "REPAIR_SCOPE_INVALID"
    task_map = {x.get("task_id"): x for x in work_orders}
    event_map = {x.get("task_id"): x for x in worker_events}
    final_claims = {x.get("task_id"): x for x in evidence_claims}
    if (len(task_map) != len(work_orders) or len(event_map) != len(worker_events)
        or len(final_claims) != len(evidence_claims) or set(task_map) != set(event_map)
        or set(task_map) != set(final_claims)):
        return "BLOCKED", "REPAIR_TASK_SET_MISMATCH"
    counts = {}
    for task, result in event_map.items():
        count = result.get("local_repairs")
        order = task_map[task]
        if (type(count) is not int or count < 0 or count > mission.get("max_local_repairs", -1)
            or count > order.get("max_local_repairs", -1)):
            return "BLOCKED", "REPAIR_BUDGET_EXCEEDED"
        counts[task] = count
    if sum(counts.values()) != len(repair_events):
        return "UNVERIFIED", "REPAIR_ATTESTATIONS_MISSING"
    if not repair_events:
        return "PASS", "ZERO_REPAIR_BACKWARD_COMPATIBLE"
    schema = json.loads((Path(__file__).resolve().parents[1] /
                         "contracts/v0.0.2/repair-event.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    if any(not validator.is_valid(x) for x in repair_events):
        return "BLOCKED", "REPAIR_EVENT_SCHEMA_INVALID"
    if len({x["repair_id"] for x in repair_events}) != len(repair_events):
        return "BLOCKED", "REPAIR_EVENT_REPLAY"
    transitions = [t for x in repair_events for t in (
        x["head_transition_id"], x["worker_transition_id"])]
    if len(set(transitions)) != len(transitions):
        return "BLOCKED", "REPAIR_TRANSITION_REPLAY"
    all_receipts = set()
    grouped = {task: [] for task in task_map}
    for x in repair_events:
        task = x["task_id"]
        if (task not in grouped or x["mission_id"] != mission.get("mission_id")
            or x["source_sha"] != mission.get("source_sha")
            or x["team"] != task_map[task].get("team")
            or x["head_subject"] == x["worker_subject"]):
            return "BLOCKED", "REPAIR_SCOPE_MISMATCH"
        grouped[task].append(x)
        for rec in (x["prior_receipt"], x["next_receipt"]):
            if not rec or x["prior_receipt"] == x["next_receipt"]:
                return "BLOCKED", "REPAIR_RECEIPT_MISMATCH"
        # A prior receipt may be the next receipt of an immediately previous
        # retry, but may never recur across different tasks or epochs.
        if x["next_receipt"] in all_receipts:
            return "BLOCKED", "REPAIR_RECEIPT_REPLAY"
        all_receipts.add(x["next_receipt"])
    try:
        for task, records in grouped.items():
            if len(records) != counts[task]:
                return "BLOCKED", "REPAIR_COUNT_MISMATCH"
            for i, x in enumerate(records, 1):
                if x["repair_number"] != i:
                    return "BLOCKED", "REPAIR_NUMBER_MISMATCH"
                if i > 1 and x["prior_receipt"] != records[i-2]["next_receipt"]:
                    return "BLOCKED", "REPAIR_RECEIPT_CHAIN_MISMATCH"
                expected = final_claims[task]
                if i == len(records) and x["next_receipt"] != expected.get("provider_record_id"):
                    return "BLOCKED", "REPAIR_FINAL_RECEIPT_MISMATCH"
                proof = trust.authenticate_repair(x["repair_id"])
                if proof is None:
                    return "UNVERIFIED", "REPAIR_ATTESTATION_UNAVAILABLE"
                fields = ("mission_id", "repair_id", "task_id", "team", "source_sha",
                          "repair_number", "head_subject", "worker_subject",
                          "prior_receipt", "next_receipt")
                if not proof.valid or any(getattr(proof, key, None) != x[key] for key in fields):
                    return "BLOCKED", "REPAIR_ATTESTATION_MISMATCH"
                for key, before, after, actor in (
                    ("head_transition_id", "VALIDATION_PENDING", "WORKER_ACTIVE", "HEAD"),
                    ("worker_transition_id", "WORKER_ACTIVE", "VALIDATION_PENDING", "WORKER"),
                ):
                    att = trust.authenticate_transition(x[key])
                    if att is None:
                        return "UNVERIFIED", "REPAIR_TRANSITION_UNAUTHENTICATED"
                    if (not att.valid or att.mission_id != x["mission_id"]
                        or att.transition_id != x[key] or att.task_id != task
                        or att.team != x["team"] or att.source_sha != x["source_sha"]
                        or (att.from_phase, att.to_phase, att.actor) != (before, after, actor)):
                        return "BLOCKED", "REPAIR_TRANSITION_SCOPE_MISMATCH"
                # Provider observation of the previous attempt may legitimately
                # be FAIL; it must still bind to the same mission/task/source.
                prior = trust.resolve_observation(expected["provider"], x["prior_receipt"])
                if prior is None:
                    return "UNVERIFIED", "REPAIR_PRIOR_RECEIPT_UNAVAILABLE"
                if (prior.mission_id != x["mission_id"] or prior.task_id != task
                    or prior.source_sha != x["source_sha"]
                    or prior.provider != expected["provider"]
                    or prior.provider_record_id != x["prior_receipt"]
                    or prior.criterion_id not in task_map[task].get("criteria_ids", [])):
                    return "BLOCKED", "REPAIR_PRIOR_RECEIPT_SCOPE_MISMATCH"
    except Exception:
        return "UNVERIFIED", "REPAIR_TRUST_ADAPTER_UNAVAILABLE"
    return "PASS", "REPAIR_CHAIN_ATTESTED_BY_SUPPLIED_ADAPTER"
