"""M3 OPS Director recommendation policy, never a dispatch or grant authority.

Uses M2 metadata to suggest ONE specialist. Host-side user consent, protected
mission locks, actual role attestations and provider permissions stay outside.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import re
from .team_directory import TeamDirectory, RegistryRejected, EXPECTED_TEAMS, VERSION as REGISTRY_VERSION

_SHA=re.compile(r"^[0-9a-f]{40}$")
_ID=re.compile(r"^[A-Za-z0-9_.:-]{1,128}$")

@dataclass(frozen=True)
class RouteIntent:
    mission_id: str
    source_sha: str
    observed_sha: str
    mission_revision: int
    observed_revision: int
    permitted_teams: tuple[str,...]
    required_capabilities: tuple[str,...]
    available_tools: tuple[str,...]
    task_text: str
    active_worker: Optional[str]
    prior_gate_status: str  # NOT_REQUIRED, VALIDATED_AND_AUDITED, UNVERIFIED
    dispatch_count: int
    max_handoffs: int
    forbidden_capabilities: tuple[str,...] = ()
    advisory_only: bool = False
    supplied_context_ref: Optional[str] = None
    synthetic_only: bool = False

@dataclass(frozen=True)
class RouteAdvice:
    status: str  # SUGGEST_ONLY, BLOCKED, UNVERIFIED, CAPABILITY_BLOCKED, ABSTAIN
    code: str
    mission_id: str
    source_sha: str
    registry_version: str
    suggested_team: Optional[str] = None
    capability_id: Optional[str] = None
    playbook_ref: Optional[str] = None
    reason: str = ""

@dataclass(frozen=True)
class HandoffDraft:
    classification: str  # DRAFT_ONLY, never authenticated
    mission_id: str
    source_sha: str
    mission_revision: int
    team_id: str
    capability_id: str
    playbook_ref: str
    criterion_ids: tuple[str,...]
    evidence_refs: tuple[str,...]
    authorization_status: str  # ALWAYS UNVERIFIED_HOST_GRANT
    objective: str = ""
    declared_tools: tuple[str,...] = ()
    prior_gate_status: str = "UNVERIFIED"
    remaining_handoffs: int = 0
    stop_conditions: tuple[str,...] = ()
    previous_validation_ref: Optional[str] = None
    previous_audit_ref: Optional[str] = None


def recommend_one(intent: RouteIntent, directory: Optional[TeamDirectory] = None) -> RouteAdvice:
    mid=getattr(intent,"mission_id","")
    sha=getattr(intent,"source_sha","")
    def out(status,code,reason="",team=None,cap=None,playbook=None):
        return RouteAdvice(status,code,mid if isinstance(mid,str) else "",
                           sha if isinstance(sha,str) else "",REGISTRY_VERSION,
                           team,cap,playbook,reason)
    if not isinstance(intent,RouteIntent):
        return out("BLOCKED","INVALID_ROUTE_INTENT")
    if (not isinstance(mid,str) or not _ID.fullmatch(mid)
        or not isinstance(sha,str) or not _SHA.fullmatch(sha)
        or type(intent.mission_revision) is not int or intent.mission_revision < 1
        or type(intent.observed_revision) is not int or intent.observed_revision < 1
        or type(intent.dispatch_count) is not int or intent.dispatch_count < 0
        or type(intent.max_handoffs) is not int or intent.max_handoffs < 0):
        return out("BLOCKED","INVALID_ROUTE_SCOPE")
    if intent.source_sha != intent.observed_sha:
        return out("BLOCKED","STALE_SOURCE")
    if intent.mission_revision != intent.observed_revision:
        return out("BLOCKED","REVISION_CONFLICT")
    if intent.active_worker is not None:
        return out("BLOCKED","ONE_ACTIVE_WORKER_ENFORCED")
    if intent.dispatch_count > intent.max_handoffs:
        return out("BLOCKED","HANDOFF_BUDGET_EXCEEDED")
    if intent.prior_gate_status not in ("NOT_REQUIRED","VALIDATED_AND_AUDITED"):
        return out("UNVERIFIED","PRIOR_GATES_NOT_VERIFIED")
    if intent.dispatch_count > 0 and intent.prior_gate_status != "VALIDATED_AND_AUDITED":
        return out("BLOCKED","MISSING_PREVIOUS_GATE")
    if (not isinstance(intent.permitted_teams,tuple) or
        any(t not in EXPECTED_TEAMS for t in intent.permitted_teams) or
        len(intent.permitted_teams)!=len(set(intent.permitted_teams)) or
        not isinstance(intent.required_capabilities,tuple) or
        not isinstance(intent.available_tools,tuple) or
        not isinstance(intent.forbidden_capabilities,tuple) or
        not isinstance(intent.task_text,str) or
        any(not isinstance(c,str) for c in intent.required_capabilities) or
        any(not isinstance(c,str) for c in intent.forbidden_capabilities) or
        any(not isinstance(t,str) for t in intent.available_tools)
        or type(intent.advisory_only) is not bool
        or type(intent.synthetic_only) is not bool
        or (intent.supplied_context_ref is not None
            and not isinstance(intent.supplied_context_ref,str))):
        return out("BLOCKED","INVALID_ROUTING_METADATA")
    if not intent.permitted_teams or not intent.required_capabilities:
        return out("ABSTAIN","NO_REQUIRED_CAPABILITY_OR_PERMITTED_TEAM")
    if set(intent.required_capabilities)&set(intent.forbidden_capabilities):
        return out("BLOCKED","FORBIDDEN_REQUIRED_CAPABILITY")
    if intent.advisory_only and not intent.supplied_context_ref:
        return out("UNVERIFIED","USER_SUPPLIED_CONTEXT_MISSING")
    if (intent.advisory_only and
        any(x.startswith("red.") for x in intent.required_capabilities)
        and not intent.synthetic_only):
        return out("CAPABILITY_BLOCKED","RED_ADVISORY_REQUIRES_SYNTHETIC_ONLY_SCOPE")
    if directory is None:
        try:
            directory=TeamDirectory()
        except (OSError,ValueError,TypeError,KeyError):
            return out("UNVERIFIED","REGISTRY_UNAVAILABLE")
    try:
        result=directory.search(query=intent.task_text,
            permitted_teams=intent.permitted_teams,
            required_capabilities=intent.required_capabilities,
            available_tools=intent.available_tools,limit=18,
            advisory_only=intent.advisory_only,
            supplied_context_ref=intent.supplied_context_ref)
    except (RegistryRejected,OSError,ValueError,TypeError,KeyError):
        return out("BLOCKED","REGISTRY_SCOPE_INVALID")
    if result.status=="ABSTAIN":
        return out("ABSTAIN","REQUIRED_CAPABILITIES_UNSATISFIED")
    if not result.matches:
        return out("ABSTAIN","NO_ELIGIBLE_CAPABILITY")
    eligible=[c for c in result.matches
              if (intent.advisory_only or not c.missing_tools)
              and c.capability_id not in intent.forbidden_capabilities]
    if not eligible:
        return out("CAPABILITY_BLOCKED","DECLARED_TOOLS_OR_CAPABILITY_NOT_AVAILABLE")
    # One Worker must be able to cover the whole required obligation in one route.
    by_team={}
    for c in eligible:
        by_team.setdefault(c.team_id,[]).append(c)
    teams=[team for team,caps in by_team.items()
           if set(intent.required_capabilities).issubset({x.capability_id for x in caps})]
    if not teams:
        return out("ABSTAIN","REQUIRES_SEQUENTIAL_HEAD_DECOMPOSITION")
    winner=sorted(teams)[0]
    candidates=sorted(by_team[winner],key=lambda c:c.capability_id)
    candidate=candidates[0]
    if intent.advisory_only:
        return out("SUGGEST_ONLY","ADVISORY_WITH_SUPPLIED_CONTEXT",
                   "User-supplied text only: no live test, provider operation, tool grant, "
                   "authenticated review or actual external observation.",
                   winner,candidate.capability_id,candidate.playbook_ref)
    return out("SUGGEST_ONLY","CANDIDATE_NOT_AUTHORIZED",
               "Metadata match only. Head and protected host must authorize the actual Worker.",
               winner,candidate.capability_id,candidate.playbook_ref)


def handoff_draft(intent: RouteIntent, advice: RouteAdvice, *,
                  criterion_ids: tuple[str,...], evidence_refs: tuple[str,...],
                  previous_validation_ref: Optional[str] = None,
                  previous_audit_ref: Optional[str] = None) -> HandoffDraft:
    if (not isinstance(intent,RouteIntent) or not isinstance(advice,RouteAdvice)
        or advice.status!="SUGGEST_ONLY" or advice.mission_id!=intent.mission_id
        or advice.source_sha!=intent.source_sha
        or advice.suggested_team not in intent.permitted_teams
        or not advice.capability_id or not advice.playbook_ref
        or not isinstance(criterion_ids,tuple) or not criterion_ids
        or not all(isinstance(x,str) and _ID.fullmatch(x) for x in criterion_ids)
        or len(set(criterion_ids))!=len(criterion_ids)
        or not isinstance(evidence_refs,tuple)
        or any(not isinstance(x,str) or not _ID.fullmatch(x) for x in evidence_refs)
        or len(set(evidence_refs))!=len(evidence_refs)
        or (previous_validation_ref is not None
            and (not isinstance(previous_validation_ref,str)
                 or not _ID.fullmatch(previous_validation_ref)))
        or (previous_audit_ref is not None
            and (not isinstance(previous_audit_ref,str)
                 or not _ID.fullmatch(previous_audit_ref)))):
        raise RegistryRejected("INVALID_UNAUTHENTICATED_HANDOFF")
    return HandoffDraft("DRAFT_ONLY",intent.mission_id,intent.source_sha,
                        intent.mission_revision,advice.suggested_team,
                        advice.capability_id,advice.playbook_ref,criterion_ids,
                        evidence_refs,"UNVERIFIED_HOST_GRANT",
                        objective=intent.task_text,
                        declared_tools=intent.available_tools,
                        prior_gate_status=intent.prior_gate_status,
                        remaining_handoffs=max(0,intent.max_handoffs-intent.dispatch_count),
                        stop_conditions=("SOURCE_CHANGED","MISSING_TRUSTED_GATE",
                                         "BUDGET_EXHAUSTED","TOOL_UNAVAILABLE"),
                        previous_validation_ref=previous_validation_ref,
                        previous_audit_ref=previous_audit_ref)
