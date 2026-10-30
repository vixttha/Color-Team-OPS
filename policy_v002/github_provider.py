"""Read-only GitHub Actions evidence adapter for the v0.0.2 D2 policy engine.

NO AUTOMATIC AUTHORITY: only a trusted host may construct/protect HostAuthority,
provide GitHub credentials and register immutable RunBinding records. GitHub
API observations alone never authorize Head, dispatches, or internal audit.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Callable, Mapping, Optional, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .verifier import Authorization, GateAttestation, MissionSnapshot, Observation, TransitionAttestation

_REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_BRANCH_SEGMENT = re.compile(r"^[A-Za-z0-9_.-]+$")
_SHA = re.compile(r"^[0-9a-f]{40}$")
_RUN = re.compile(r"^run:([1-9][0-9]*)$")
_WORKFLOW = re.compile(r"^\.github/workflows/[A-Za-z0-9_.-]+\.ya?ml$")
_API_ORIGIN = "https://api.github.com"
_MAX_JOBS = 1000


class ProviderReadError(RuntimeError):
    """Unavailable, invalid or untrustworthy provider observation."""


class _NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ProviderReadError("GitHub API redirect refused")


def _valid_repository(full_name: str) -> bool:
    return isinstance(full_name, str) and _REPO.fullmatch(full_name) is not None


def _valid_branch(branch: str) -> bool:
    return (isinstance(branch, str) and len(branch) <= 128
            and all(_BRANCH_SEGMENT.fullmatch(p) and p not in (".", "..")
                    for p in branch.split("/"))
            and not branch.startswith("/") and not branch.endswith("/"))


def _path_for_repo(repository: str) -> str:
    if not _valid_repository(repository):
        raise ProviderReadError("Invalid repository locator")
    return "/repos/" + "/".join(quote(part, safe="") for part in repository.split("/"))


class GitHubReader(Protocol):
    """A GitHub REST GET-only reader, instantiated within a trusted host."""
    def repository(self, repository: str) -> Mapping: ...
    def branch_ref(self, repository: str, branch: str) -> Mapping: ...
    def workflow_run(self, repository: str, run_id: int) -> Mapping: ...
    def latest_jobs(self, repository: str, run_id: int) -> list[Mapping]: ...


class GitHubRESTReader:
    """Network-capable implementation; requires a protected token supplier.

    No repository secrets or access tokens belong in source code, fixtures,
    logs or user-controlled mission JSON. This class does not grant permissions.
    """
    def __init__(self, token_supplier: Callable[[], str], timeout: float = 10.0):
        if not callable(token_supplier) or timeout <= 0:
            raise ValueError("Protected credential supplier and timeout required")
        self._token_supplier = token_supplier
        self._timeout = timeout
        self._opener = build_opener(_NoRedirects())

    def _get(self, path: str) -> Mapping:
        if not path.startswith("/") or "//" in path or "\n" in path or "\r" in path:
            raise ProviderReadError("Unsafe API path")
        token = self._token_supplier()
        if not isinstance(token, str) or not token.strip() or "\n" in token or "\r" in token:
            raise ProviderReadError("Missing protected GitHub credential")
        request = Request(
            _API_ORIGIN + path,
            method="GET",
            headers={"Accept": "application/vnd.github+json",
                     "Authorization": "Bearer " + token,
                     "X-GitHub-Api-Version": "2026-03-10",
                     "User-Agent": "color-team-ops-v002-readonly"},
        )
        try:
            with self._opener.open(request, timeout=self._timeout) as result:
                if result.status != 200 or result.geturl().split("?")[0] != (_API_ORIGIN + path.split("?")[0]):
                    raise ProviderReadError("Unexpected GitHub endpoint response")
                raw = result.read(4_000_001)
                if len(raw) > 4_000_000:
                    raise ProviderReadError("Oversize GitHub response")
        except (HTTPError, URLError, OSError, TimeoutError) as exc:
            raise ProviderReadError("GitHub read failed") from exc
        try:
            data = json.loads(raw)
        except (ValueError, UnicodeError) as exc:
            raise ProviderReadError("Malformed GitHub response") from exc
        if not isinstance(data, dict):
            raise ProviderReadError("Expected GitHub object")
        return data

    def repository(self, repository: str) -> Mapping:
        return self._get(_path_for_repo(repository))

    def branch_ref(self, repository: str, branch: str) -> Mapping:
        if not _valid_branch(branch):
            raise ProviderReadError("Invalid branch ref")
        path = _path_for_repo(repository)
        return self._get(path + "/git/ref/heads/" + "/".join(quote(p, safe="") for p in branch.split("/")))

    def workflow_run(self, repository: str, run_id: int) -> Mapping:
        if type(run_id) is not int or run_id < 1:
            raise ProviderReadError("Invalid workflow run ID")
        return self._get(_path_for_repo(repository) + "/actions/runs/" + str(run_id))

    def latest_jobs(self, repository: str, run_id: int) -> list[Mapping]:
        if type(run_id) is not int or run_id < 1:
            raise ProviderReadError("Invalid workflow run ID")
        path = _path_for_repo(repository) + "/actions/runs/" + str(run_id) + "/jobs"
        jobs = []
        for page in range(1, 12):
            response = self._get(path + "?per_page=100&filter=latest&page=" + str(page))
            total = response.get("total_count")
            batch = response.get("jobs")
            if type(total) is not int or total < 0 or total > _MAX_JOBS or not isinstance(batch, list):
                raise ProviderReadError("Incomplete or invalid GitHub jobs pagination")
            if any(not isinstance(job, dict) for job in batch):
                raise ProviderReadError("Invalid GitHub job payload")
            jobs.extend(batch)
            if len(jobs) > total or len(jobs) > _MAX_JOBS:
                raise ProviderReadError("Inconsistent jobs count")
            if len(jobs) == total:
                if len({j.get("id") for j in jobs}) != len(jobs):
                    raise ProviderReadError("Duplicate GitHub job IDs")
                return jobs
            if not batch:
                raise ProviderReadError("Incomplete jobs pagination")
        raise ProviderReadError("Exceeded jobs pagination limit")


@dataclass(frozen=True)
class RunBinding:
    """Trusted host-issued mapping; NEVER deserialize from a worker's claim."""
    mission_id: str
    task_id: str
    criterion_id: str
    repository_id: int
    repository: str
    branch: str
    source_sha: str
    run_id: int
    workflow_path: str
    event: str
    required_jobs: tuple[str, ...]
    required_job_steps: tuple[tuple[str, str], ...]


class HostAuthority(Protocol):
    """The host (not GitHub) must authenticate these mission state records."""
    def authorization(self, mission_id: str, authorization_ref: str) -> Optional[Authorization]: ...
    def expected_repository_id(self, repository: str) -> Optional[int]: ...
    def run_binding(self, provider_record_id: str) -> Optional[RunBinding]: ...
    def authorized_dispatch(self, mission_id: str, task_id: str, team: str, source_sha: str) -> bool: ...
    def authenticate_gate(self, record_id: str) -> Optional[GateAttestation]: ...
    def authenticate_transition(self, transition_id: str) -> Optional[TransitionAttestation]: ...
    def mission_snapshot(self, mission_id: str) -> Optional[MissionSnapshot]: ...
    def exclusive_write_enforced(self, mission_id: str, repository: str, branch: str) -> bool: ...


class GitHubBackedTrustAdapter:
    """Bridge between protected mission authority and live GitHub reads.

    An arbitrary injected HostAuthority can lie; only use inside an authenticated
    host/service. No permanent mission ledger is bundled or auto-created.
    """
    def __init__(self, reader: GitHubReader, host: HostAuthority):
        self._reader = reader
        self._host = host

    def authorization(self, mission_id: str, authorization_ref: str) -> Optional[Authorization]:
        return self._host.authorization(mission_id, authorization_ref)

    def _repository_identity(self, repository: str, expected_id: Optional[int]) -> bool:
        if not _valid_repository(repository) or type(expected_id) is not int or expected_id < 1:
            return False
        data = self._reader.repository(repository)
        return (data.get("id") == expected_id and
                data.get("full_name", "").casefold() == repository.casefold() and
                data.get("private") in (True, False))

    def current_sha(self, repository: str, branch: str) -> Optional[str]:
        expected_id = self._host.expected_repository_id(repository)
        if not self._repository_identity(repository, expected_id) or not _valid_branch(branch):
            return None
        ref = self._reader.branch_ref(repository, branch)
        expect = "refs/heads/" + branch
        obj = ref.get("object")
        if ref.get("ref") != expect or not isinstance(obj, dict) or obj.get("type") != "commit":
            return None
        sha = obj.get("sha")
        return sha if isinstance(sha, str) and _SHA.fullmatch(sha) else None

    def authorized_dispatch(self, mission_id: str, task_id: str, team: str, source_sha: str) -> bool:
        return self._host.authorized_dispatch(mission_id, task_id, team, source_sha)

    def authenticate_gate(self, record_id: str) -> Optional[GateAttestation]:
        return self._host.authenticate_gate(record_id)

    def authenticate_transition(self, transition_id: str) -> Optional[TransitionAttestation]:
        return self._host.authenticate_transition(transition_id)

    def mission_snapshot(self, mission_id: str) -> Optional[MissionSnapshot]:
        return self._host.mission_snapshot(mission_id)

    def exclusive_write_enforced(self, mission_id: str, repository: str, branch: str) -> bool:
        return self._host.exclusive_write_enforced(mission_id, repository, branch)

    def resolve_observation(self, provider: str, provider_record_id: str) -> Optional[Observation]:
        if provider != "github" or not isinstance(provider_record_id, str):
            return None
        match = _RUN.fullmatch(provider_record_id)
        if match is None:
            return None
        binding = self._host.run_binding(provider_record_id)
        if binding is None or not isinstance(binding, RunBinding):
            return None
        if (binding.run_id != int(match.group(1)) or type(binding.repository_id) is not int
                or binding.repository_id < 1 or not _SHA.fullmatch(binding.source_sha)
                or not _valid_branch(binding.branch) or not _WORKFLOW.fullmatch(binding.workflow_path)
                or binding.event != "push" or not binding.criterion_id or not binding.mission_id
                or not binding.task_id or not binding.required_jobs or not binding.required_job_steps
                or len(set(binding.required_jobs)) != len(binding.required_jobs)
                or len(set(binding.required_job_steps)) != len(binding.required_job_steps)
                or any(not isinstance(item, tuple) or len(item) != 2
                       or not all(isinstance(part, str) and part.strip() for part in item)
                       for item in binding.required_job_steps)
                or {name for name, _ in binding.required_job_steps} != set(binding.required_jobs)):
            
            return None
        trusted_repo_id = self._host.expected_repository_id(binding.repository)
        if binding.repository_id != trusted_repo_id or not self._repository_identity(binding.repository, trusted_repo_id):
            return None

        run = self._reader.workflow_run(binding.repository, binding.run_id)
        source_repo = run.get("repository")
        head_repo = run.get("head_repository")
        if (run.get("id") != binding.run_id or not isinstance(source_repo, dict)
                or not isinstance(head_repo, dict)
                or source_repo.get("id") != binding.repository_id
                or head_repo.get("id") != binding.repository_id
                or run.get("head_sha") != binding.source_sha
                or run.get("head_branch") != binding.branch
                or run.get("path") != binding.workflow_path
                or run.get("event") != binding.event
                or run.get("status") != "completed"
                or type(run.get("run_attempt")) is not int or run["run_attempt"] < 1):
            return None

        if run.get("conclusion") not in ("success", "failure"):
            return None
        jobs = self._reader.latest_jobs(binding.repository, binding.run_id)
        matches = {}
        for job in jobs:
            if job.get("run_id") != binding.run_id:
                return None
            name = job.get("name")
            if name in binding.required_jobs:
                if name in matches:
                    return None
                matches[name] = job
        if set(matches) != set(binding.required_jobs):
            return None

        steps_passed = True
        for job in matches.values():
            if job.get("status") != "completed" or job.get("conclusion") not in ("success", "failure"):
                return None
            if job.get("conclusion") != "success":
                steps_passed = False
            steps = job.get("steps")
            if not isinstance(steps, list):
                return None
            for required_job, step_name in binding.required_job_steps:
                if required_job != job["name"]:
                    continue
                relevant = [step for step in steps if isinstance(step, dict)
                            and step.get("name") == step_name]
                if len(relevant) != 1:
                    return None
                if relevant[0].get("status") != "completed":
                    return None
                if relevant[0].get("conclusion") != "success":
                    steps_passed = False

        success = run["conclusion"] == "success" and steps_passed
        return Observation(binding.mission_id, binding.task_id, "github", provider_record_id,
                           binding.source_sha, binding.criterion_id, "PASS" if success else "FAIL")
