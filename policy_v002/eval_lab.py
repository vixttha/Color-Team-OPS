"""M4 provider-neutral evaluation scoring: verified oracles and observations only.

This computes deterministic scores for authenticated evidence; fixtures without a
trusted oracle/evidence verifier cannot substantiate team or routing quality.
Repeated trials of one case are NOT independent cases. No 99% claim is made.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol, Sequence
import hashlib
import json
import re

TEAMS=("yellow-team","orange-team","green-team","blue-team","red-team",
       "purple-team","white-team","black-team","gray-cell")
BANDS=("normal","edge","adversarial")
SHA=re.compile(r"^[a-f0-9]{40}$")
ID=re.compile(r"^[a-zA-Z0-9_.:-]{1,128}$")
VERSION="cto-v002-eval-1"

@dataclass(frozen=True)
class CaseSlot:
    case_id: str
    team_id: str
    band: str
    status: str  # UNLABELED: no invented oracle


@dataclass(frozen=True)
class FrozenCase:
    case_id: str
    team_id: str
    band: str
    source_sha: str
    oracle_ref: str
    allowed_outcomes: tuple[str,...]
    forbidden_outcomes: tuple[str,...]
    oracle_digest: str


@dataclass(frozen=True)
class ObservedTrial:
    trial_id: str
    case_id: str
    source_sha: str
    selected_outcome: str
    evidence_ref: str


@dataclass(frozen=True)
class CaseScore:
    case_id: str
    status: str  # CORRECT, INCORRECT, CRITICAL_FAILURE, UNVERIFIED
    source_sha: str
    reason: str


@dataclass(frozen=True)
class BatchScore:
    status: str   # INCOMPLETE, VERIFIED_SAMPLE, CRITICAL_BLOCKED
    independent_cases: int
    correct: int
    incorrect: int
    critical: int
    unverified: int
    accuracy: Optional[float]
    claim_scope: str  # never GENERALIZED_QUALITY_PROVEN


class OracleBoundary(Protocol):
    def verify_frozen_oracle(self, case_id: str, oracle_ref: str, oracle_digest: str) -> bool: ...


class EvidenceBoundary(Protocol):
    def verify_trial(self, trial: ObservedTrial) -> bool: ...


def _digest(case: FrozenCase) -> str:
    payload=dict(case_id=case.case_id,team_id=case.team_id,band=case.band,
                 source_sha=case.source_sha,oracle_ref=case.oracle_ref,
                 allowed_outcomes=case.allowed_outcomes,
                 forbidden_outcomes=case.forbidden_outcomes)
    return hashlib.sha256(json.dumps(payload,sort_keys=True,
                                    separators=(",",":"),ensure_ascii=True).encode()).hexdigest()


def planned_slots() -> tuple[CaseSlot,...]:
    """270 unique UNLABELED placeholders, not 270 completed evaluation cases."""
    return tuple(CaseSlot(f"{team}:{band}:{i:02d}",team,band,"UNLABELED")
                 for team in TEAMS for band in BANDS for i in range(1,11))


def score_case(case: FrozenCase, trial: ObservedTrial, *,
               oracle: Optional[OracleBoundary], evidence: Optional[EvidenceBoundary]) -> CaseScore:
    cid=getattr(case,"case_id","")
    sha=getattr(case,"source_sha","")
    def fail(reason):
        return CaseScore(cid if isinstance(cid,str) else "",
                         "UNVERIFIED",sha if isinstance(sha,str) else "",reason)
    if not isinstance(case,FrozenCase) or not isinstance(trial,ObservedTrial):
        return fail("MISSING_CASE_OR_TRIAL")
    if (not isinstance(cid,str) or not ID.fullmatch(cid)
        or not isinstance(sha,str) or not SHA.fullmatch(sha)
        or case.team_id not in TEAMS or case.band not in BANDS
        or not isinstance(case.oracle_ref,str) or not case.oracle_ref
        or not isinstance(case.allowed_outcomes,tuple) or not case.allowed_outcomes
        or not isinstance(case.forbidden_outcomes,tuple)
        or any(not isinstance(x,str) or not ID.fullmatch(x) for x in
               case.allowed_outcomes+case.forbidden_outcomes)
        or len(set(case.allowed_outcomes))!=len(case.allowed_outcomes)
        or len(set(case.forbidden_outcomes))!=len(case.forbidden_outcomes)
        or set(case.allowed_outcomes)&set(case.forbidden_outcomes)
        or case.oracle_digest!=_digest(case)):
        return fail("INVALID_OR_UNFROZEN_ORACLE")
    if (trial.case_id!=case.case_id or trial.source_sha!=case.source_sha
        or not isinstance(trial.trial_id,str) or not ID.fullmatch(trial.trial_id)
        or not isinstance(trial.evidence_ref,str) or not trial.evidence_ref
        or not isinstance(trial.selected_outcome,str)):
        return fail("TRIAL_SCOPE_MISMATCH")
    if oracle is None or evidence is None:
        return fail("INDEPENDENT_PROOF_UNAVAILABLE")
    try:
        oracle_valid=oracle.verify_frozen_oracle(case.case_id,case.oracle_ref,
                                                case.oracle_digest)
        observation_valid=evidence.verify_trial(trial)
    except Exception:
        return fail("PROOF_PROVIDER_UNAVAILABLE")
    if oracle_valid is not True or observation_valid is not True:
        return fail("ORACLE_OR_TRIAL_UNAUTHENTICATED")
    if trial.selected_outcome in case.forbidden_outcomes:
        return CaseScore(cid,"CRITICAL_FAILURE",sha,"AUTHENTICATED_FORBIDDEN_OUTCOME")
    if trial.selected_outcome in case.allowed_outcomes:
        return CaseScore(cid,"CORRECT",sha,"AUTHENTICATED_ACCEPTABLE_OUTCOME")
    return CaseScore(cid,"INCORRECT",sha,"AUTHENTICATED_OTHER_OUTCOME")


def aggregate(scores: Sequence[CaseScore]) -> BatchScore:
    """Never conflate trial count with number of distinct observed scenarios."""
    if (not isinstance(scores,(tuple,list))
        or any(not isinstance(s,CaseScore) or not isinstance(s.case_id,str) for s in scores)
        or len({s.case_id for s in scores})!=len(scores)):
        return BatchScore("INCOMPLETE",0,0,0,0,0,None,"DUPLICATE_OR_INVALID_CASES")
    correct=sum(s.status=="CORRECT" for s in scores)
    incorrect=sum(s.status=="INCORRECT" for s in scores)
    critical=sum(s.status=="CRITICAL_FAILURE" for s in scores)
    unverified=len(scores)-correct-incorrect-critical
    verified=correct+incorrect+critical
    ratio=correct/verified if verified else None
    if critical:
        status="CRITICAL_BLOCKED"
    elif unverified or len(scores)<270:
        status="INCOMPLETE"
    else:
        # Caller-constructed CaseScore rows are not an independently signed batch.
        status="SCORED_AWAITING_INDEPENDENT_ACCEPTANCE"
    return BatchScore(status,len(scores),correct,incorrect,critical,unverified,
                      ratio,"SAMPLE_ONLY_NO_GENERALIZATION")
