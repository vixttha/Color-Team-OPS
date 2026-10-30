"""D5 optional GitHub provenance inspector, strictly read-only.

GitHub authenticates account/app attribution and workflow observations.
It does NOT authenticate the model's Head/Worker/Auditor role or user consent,
and issue comments are not tamper-proof, immutable production grants.
No caller can turn this result into D2's trusted HostAuthority.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping, Protocol
import re

from .github_provider import ProviderReadError

_STAGES = ("D5-01", "D5-02", "D5-03", "D5-04", "D5-05")
_SHA = re.compile(r"^[a-f0-9]{40}$")


class PilotReader(Protocol):
    def repository(self, repository: str) -> Mapping: ...
    def issue(self, repository: str, issue_number: int) -> Mapping: ...
    def issue_comments(self, repository: str, issue_number: int) -> list[Mapping]: ...
    def workflow_run(self, repository: str, run_id: int) -> Mapping: ...
    def attempt_jobs(self, repository: str, run_id: int, attempt: int) -> list[Mapping]: ...


@dataclass(frozen=True)
class PilotScope:
    repository: str
    repository_id: int
    issue_number: int
    account_id: int
    acting_app: str
    branch: str
    historical_source_sha: str
    run_id: int
    run_attempt: int
    workflow_path: str
    required_job_steps: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class PilotVerdict:
    provider_status: str  # OBSERVED, BLOCKED or UNVERIFIED
    role_authority_status: str  # Always UNVERIFIED for this provider-only inspector
    code: str
    message: str


def _verdict(status: str, code: str, reason: str) -> PilotVerdict:
    return PilotVerdict(status, "UNVERIFIED", code, reason)


def _timestamp(value: object) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError("Provider timestamp missing")
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("Naive provider timestamp")
    return dt


def inspect_read_only_pilot(reader: PilotReader, scope: PilotScope) -> PilotVerdict:
    """Historical exact-run evidence, NEVER a production authorization grant.

    Expected principal/app/IDs must come from reviewed trusted host scope, NOT
    from the issue body. Even then, all role labels remain agent-authored.
    """
    if (not isinstance(scope, PilotScope) or
            not isinstance(scope.repository, str) or not scope.repository or
            type(scope.repository_id) is not int or scope.repository_id < 1 or
            type(scope.account_id) is not int or scope.account_id < 1 or
            type(scope.issue_number) is not int or scope.issue_number < 1 or
            type(scope.run_id) is not int or scope.run_id < 1 or
            type(scope.run_attempt) is not int or scope.run_attempt < 1 or
            not isinstance(scope.historical_source_sha, str) or
            not _SHA.fullmatch(scope.historical_source_sha) or
            not scope.acting_app or not scope.branch or not scope.workflow_path or
            len(scope.required_job_steps) < 1 or
            len({row[0] for row in scope.required_job_steps}) != len(scope.required_job_steps)):
        return _verdict("BLOCKED", "INVALID_PILOT_SCOPE", "Missing or malformed reviewed pilot scope.")

    try:
        repo = reader.repository(scope.repository)
        if (repo.get("id") != scope.repository_id or
                repo.get("full_name") != scope.repository or
                repo.get("private") is not True):
            return _verdict("BLOCKED", "REPOSITORY_MISMATCH", "Provider repository identity differs.")
        issue = reader.issue(scope.repository, scope.issue_number)
        if issue.get("number") != scope.issue_number or issue.get("state") != "open":
            return _verdict("BLOCKED", "ISSUE_MISMATCH", "Unexpected pilot issue record.")
        if (not isinstance(issue.get("user"), dict) or
                issue["user"].get("id") != scope.account_id or
                not isinstance(issue.get("performed_via_github_app"), dict) or
                issue["performed_via_github_app"].get("slug") != scope.acting_app):
            return _verdict("BLOCKED", "ISSUER_ATTRIBUTION_MISMATCH",
                            "Issue creator or acting connector does not match reviewed scope.")

        comments = reader.issue_comments(scope.repository, scope.issue_number)
        if not isinstance(comments, list) or len(comments) != len(_STAGES):
            return _verdict("UNVERIFIED", "INCOMPLETE_OR_CHANGED_TRACE",
                            "Expected five Head/Worker/Validate/Auditor/Head records not present.")
        prior_id, prior_time = 0, _timestamp(issue.get("created_at"))
        for expected, item in zip(_STAGES, comments):
            if not isinstance(item, dict) or type(item.get("id")) is not int:
                return _verdict("BLOCKED", "INVALID_EVENT_RECORD", "Missing provider event ID.")
            if (not isinstance(item.get("user"), dict) or
                    item["user"].get("id") != scope.account_id or
                    not isinstance(item.get("performed_via_github_app"), dict) or
                    item["performed_via_github_app"].get("slug") != scope.acting_app):
                return _verdict("BLOCKED", "EVENT_ATTRIBUTION_MISMATCH",
                                "One pilot phase was issued by a different authenticated account or app.")
            created, updated = _timestamp(item.get("created_at")), _timestamp(item.get("updated_at"))
            if updated != created:
                return _verdict("UNVERIFIED", "EVENT_EDITED",
                                "A surviving phase comment has been edited since its creation.")
            if item["id"] <= prior_id or created < prior_time:
                return _verdict("BLOCKED", "EVENT_ORDER_INVALID", "Provider event identifiers or times out of order.")
            body = item.get("body")
            # Strings only establish claimed logical phase, never permission/role.
            if not isinstance(body, str) or expected not in body:
                return _verdict("BLOCKED", "PHASE_CLAIM_MISMATCH",
                                "Required phase marker not present in expected provider record.")
            prior_id, prior_time = item["id"], created

        run = reader.workflow_run(scope.repository, scope.run_id)
        if (run.get("id") != scope.run_id or
                run.get("run_attempt") != scope.run_attempt or
                not isinstance(run.get("repository"), dict) or
                not isinstance(run.get("head_repository"), dict) or
                run["repository"].get("id") != scope.repository_id or
                run["head_repository"].get("id") != scope.repository_id or
                run.get("head_sha") != scope.historical_source_sha or
                run.get("head_branch") != scope.branch or
                run.get("path") != scope.workflow_path or
                run.get("event") != "push"):
            return _verdict("BLOCKED", "WORKFLOW_SCOPE_MISMATCH",
                            "GitHub workflow does not match the predeclared historical source and scope.")
        if run.get("status") != "completed" or run.get("conclusion") != "success":
            return _verdict("UNVERIFIED", "WORKFLOW_NOT_SUCCESSFUL",
                            "Required GitHub CI outcome was not observed as successful.")

        jobs = reader.attempt_jobs(scope.repository, scope.run_id, scope.run_attempt)
        expected = dict(scope.required_job_steps)
        if (not isinstance(jobs, list) or len(jobs) != len(expected) or
                {j.get("name") for j in jobs if isinstance(j, dict)} != set(expected)):
            return _verdict("UNVERIFIED", "REQUIRED_JOBS_MISSING",
                            "Exact required job inventory not confirmed.")
        for job in jobs:
            if (job.get("run_id") != scope.run_id or
                    job.get("head_sha") != scope.historical_source_sha or
                    job.get("status") != "completed" or job.get("conclusion") != "success"):
                return _verdict("BLOCKED", "JOB_EVIDENCE_MISMATCH",
                                "Job conclusion, run ID or source SHA invalid.")
            steps = job.get("steps")
            if not isinstance(steps, list):
                return _verdict("UNVERIFIED", "JOB_STEPS_UNAVAILABLE", "Provider job steps unavailable.")
            rows = [s for s in steps if isinstance(s, dict) and s.get("name") == expected[job["name"]]]
            if len(rows) != 1 or rows[0].get("status") != "completed" or rows[0].get("conclusion") != "success":
                return _verdict("UNVERIFIED", "REQUIRED_TEST_STEP_NOT_VERIFIED",
                                "Required job validation step not confirmed as successful.")
        return _verdict("OBSERVED", "PROVIDER_EVIDENCE_OBSERVED_ROLE_AUTHORITY_UNVERIFIED",
                        "Historical provider records and CI run match the bounded pilot; "
                        "same-account agent role labels are not authenticated host grants.")
    except (ProviderReadError, OSError, TimeoutError, ConnectionError, TypeError, KeyError,
            ValueError, OverflowError, AttributeError) as exc:
        return _verdict("UNVERIFIED", "PROVIDER_READ_UNAVAILABLE",
                        "Cannot complete provider provenance check: " + type(exc).__name__)
