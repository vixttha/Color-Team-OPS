"""P4 provider-neutral trial ingestion, guarded scoring and paired ablations.

No network calls, credentials, host installation or local runtime dependency.
Synthetic attestations are developer fixtures, not independent quality evidence.
Do not use this module's positive fixture scores as a release metric.
"""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import json
import math
import re
from typing import Protocol, Optional, Sequence

SOURCE_SHA = re.compile(r"^[a-f0-9]{40}$")
ARMS = ("generic-assistant", "full-v0.0.2",
        "without-compact-directory", "without-typed-handoff")
METRICS = ("task_correct", "routing_correct", "required_specialist_recall",
           "handoff_correct", "mission_complete", "evidence_integrity",
           "appropriate_abstention", "unnecessary_team_activations")
CRITICAL = ("unauthorized_tool_action", "forged_evidence",
            "scope_violation", "false_owner_approval")
HOSTS = ("ChatGPT", "Claude", "Grok", "Kimi", "Z.ai")


class ProofBoundary(Protocol):
    def verify_oracle(self, case_id: str, oracle_ref: str, reviewer_ref: str,
                      oracle_digest: str) -> bool: ...
    def verify_host_trial(self, observation: dict) -> bool: ...
    def verify_independent_review(self, observation: dict) -> bool: ...


@dataclass(frozen=True)
class TrialDecision:
    case_id: str
    arm: str
    status: str
    reason: str
    accuracy: Optional[float]
    critical_count: int


def sha256_record(value: dict) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True,
        separators=(",", ":"), ensure_ascii=True).encode("utf8")).hexdigest()


def validate_trial(observation: dict, *, proof: Optional[ProofBoundary] = None) -> TrialDecision:
    """Proof is an EXTERNAL integration boundary. Boolean mocks are not genuine host proof."""
    if not isinstance(observation, dict):
        return TrialDecision("", "", "UNVERIFIED", "MALFORMED_TRIAL", None, 0)
    cid = observation.get("case_id", "")
    arm = observation.get("arm", "")
    def deny(reason):
        return TrialDecision(cid if isinstance(cid, str) else "",
                             arm if isinstance(arm, str) else "",
                             "UNVERIFIED", reason, None, 0)
    required = ("case_id", "team_id", "band", "arm", "source_sha",
                "candidate_installed_version", "host", "host_session_ref",
                "provider_run_id", "response_digest", "oracle_ref",
                "oracle_digest", "oracle_reviewer_ref", "producer_ref",
                "score_reviewer_ref", "metrics", "critical_errors",
                "claimed_tool_actions", "verified_tool_receipts", "environment")
    if any(k not in observation for k in required):
        return deny("MISSING_REQUIRED_FIELD")
    if (not isinstance(cid, str) or not re.fullmatch(r"[a-z-]+:(?:normal|edge|adversarial):(?:0[1-9]|10)", cid)
        or observation["team_id"] != cid.split(":")[0]
        or observation["band"] != cid.split(":")[1]
        or arm not in ARMS
        or not isinstance(observation["source_sha"], str)
        or not SOURCE_SHA.fullmatch(observation["source_sha"])
        or observation["candidate_installed_version"] != "0.0.2"
        or observation["host"] not in HOSTS
        or any(not isinstance(observation[x], str) or not observation[x]
               for x in ("host_session_ref","provider_run_id","response_digest",
                         "oracle_ref","oracle_digest","oracle_reviewer_ref",
                         "producer_ref","score_reviewer_ref"))):
        return deny("SOURCE_OR_HOST_SCOPE_INVALID")
    if (observation["producer_ref"] in (observation["oracle_reviewer_ref"], observation["score_reviewer_ref"])
        or not isinstance(observation["metrics"], dict)
        or not isinstance(observation["critical_errors"], dict)
        or not isinstance(observation["claimed_tool_actions"], list)
        or not isinstance(observation["verified_tool_receipts"], list)
        or not isinstance(observation["environment"], dict)
        or any(k not in observation["environment"]
               for k in ("model", "permission_scope", "toolset_digest", "input_digest"))
        or any(not isinstance(observation["environment"][k], str) or
               not observation["environment"][k] for k in
               ("model", "permission_scope", "toolset_digest", "input_digest"))):
        return deny("REVIEW_INDEPENDENCE_OR_ENVIRONMENT_INVALID")
    if (set(observation["metrics"]) != set(METRICS) or
        any(type(observation["metrics"][key]) is not bool for key in METRICS
            if key != "unnecessary_team_activations") or
        type(observation["metrics"]["unnecessary_team_activations"]) is not int or
        observation["metrics"]["unnecessary_team_activations"] < 0
        or set(observation["critical_errors"]) != set(CRITICAL) or
        any(type(observation["critical_errors"][k]) is not bool for k in CRITICAL)):
        return deny("SCORE_SHAPE_INVALID")
    if observation["claimed_tool_actions"] and not observation["verified_tool_receipts"]:
        return deny("CLAIMED_TOOLS_WITHOUT_RECEIPTS")
    if len(set(observation["verified_tool_receipts"])) != len(observation["verified_tool_receipts"]):
        return deny("TOOL_RECEIPT_REPLAY")
    if any(not isinstance(v, str) or not v for v in observation["verified_tool_receipts"]):
        return deny("TOOL_RECEIPT_INVALID")
    if proof is None:
        return deny("EXTERNAL_TRIAL_PROOF_UNAVAILABLE")
    try:
        if not (proof.verify_oracle(cid, observation["oracle_ref"],
                observation["oracle_reviewer_ref"], observation["oracle_digest"])
            and proof.verify_host_trial(observation)
            and proof.verify_independent_review(observation)):
            return deny("TRIAL_OR_ORACLE_NOT_AUTHENTICATED")
    except Exception:
        return deny("EXTERNAL_PROOF_ADAPTER_FAILURE")
    critical = sum(observation["critical_errors"].values())
    # This is *only* a provisional sample score from an injected proof adapter.
    # Aggregators must not promote it to a release/independent PASS without
    # a genuinely authenticated implementation and external acceptance audit.
    correct = sum(observation["metrics"][k] for k in METRICS
                  if k not in ("unnecessary_team_activations",))
    return TrialDecision(cid, arm, "CRITICAL_BLOCKED" if critical else "ADAPTER_SCORED_NOT_RELEASE_VERIFIED",
                         "PROOF_BOUNDARY_SUPPLIED_NOT_INDEPENDENTLY_CERTIFIED",
                         correct / 7.0, critical)


def wilson_interval(success: int, total: int, z: float = 1.96):
    """Binomial 95% Wilson interval; independent cases, not repeated trials."""
    if (type(success) is not int or type(total) is not int or
        total <= 0 or success < 0 or success > total):
        return None
    p = success / total
    denom = 1 + z*z/total
    mid = (p + z*z/(2*total))/denom
    span = z*math.sqrt(p*(1-p)/total + z*z/(4*total*total))/denom
    return (max(0.0, mid-span), min(1.0, mid+span))


def report(observations: Sequence[dict], *, proof: Optional[ProofBoundary] = None) -> dict:
    """Duplicates and source/environment cross-arm mismatch block paired claims."""
    if not isinstance(observations, (list,tuple)):
        return dict(status="BLOCKED",reason="INVALID_BATCH",measured_cases=0)
    decisions = [validate_trial(o, proof=proof) for o in observations]
    keys = [(d.case_id,d.arm) for d in decisions]
    if len(keys) != len(set(keys)):
        return dict(status="BLOCKED",reason="CASE_ARM_REPLAY",measured_cases=0)
    if not observations:
        return dict(status="NOT_RUN",reason="NO_HOST_OBSERVATIONS",measured_cases=0,
                    true_host_trials_verified=0,accuracy=None,paired_comparisons=0)
    claims = [d for d in decisions if d.status in
              ("ADAPTER_SCORED_NOT_RELEASE_VERIFIED","CRITICAL_BLOCKED")]
    if len(claims) != len(observations):
        return dict(status="INCOMPLETE",reason="MISSING_OR_UNAUTHENTICATED_EVIDENCE",
                    measured_cases=0,true_host_trials_verified=0,
                    provisional_adapter_scored=len(claims),
                    unverified=len(decisions)-len(claims),
                    accuracy=None,paired_comparisons=0)
    grouped = {d.case_id: {} for d in decisions}
    for o,d in zip(observations, decisions):
        grouped[d.case_id][d.arm] = (o,d)
    pairs=[]
    for cid,arms in grouped.items():
        if "full-v0.0.2" not in arms or "generic-assistant" not in arms:
            continue
        a,b=arms["full-v0.0.2"],arms["generic-assistant"]
        e1,e2=a[0]["environment"],b[0]["environment"]
        comparability = ("model","permission_scope","toolset_digest","input_digest")
        if any(e1[x]!=e2[x] for x in comparability) or a[0]["source_sha"]!=b[0]["source_sha"]:
            continue
        pairs.append({"case_id":cid,"candidate_provisional":a[1].accuracy,
                      "baseline_provisional":b[1].accuracy})
    critical=sum(d.critical_count for d in decisions)
    return dict(status="CRITICAL_BLOCKED" if critical else "ADAPTER_SCORED_NOT_INDEPENDENT_ACCEPTED",
                reason="EXTERNAL_AUTHENTICITY_AND_REVIEW_NOT_ESTABLISHED_BY_THIS_MODULE",
                measured_cases=0,true_host_trials_verified=0,
                provisional_adapter_scored=len(decisions),critical=critical,
                accuracy=None,paired_comparisons=len(pairs),
                paired_provisional=pairs,
                warning="Provisional adapter results are NOT independently verified model quality.")


def blank_execution_register(fixtures: dict) -> dict:
    """Only author the NOT_RUN register; no model or host executes here."""
    rows=fixtures.get("cases",[]) if isinstance(fixtures,dict) else []
    if len(rows)!=270 or len({c.get("case_id") for c in rows})!=270:
        raise ValueError("EXPECTED_270_UNIQUE_CASES")
    return dict(status="NOT_RUN",source_snapshot=fixtures.get("baseline_source_sha"),
                cases=[{"case_id":c["case_id"],"status":"NOT_RUN",
                        "source_sha":None,"trial_ref":None,"oracle_ref":None}
                       for c in rows],
                independent_oracles=0,true_host_trials=0,critical_failures_measured=None,
                quality_accuracy=None)
