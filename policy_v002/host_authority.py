"""D4 protected-authority *reader* for D2/D3. No signer, hosted service or keys.

The host MUST authenticate users/actions, issue signed immutable snapshots and
protect keys/revision counters OUTSIDE this package. Test fixtures do not do that.
HMAC is a symmetric integrity MAC, not independent human approval or public PKI.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import hmac
import json
import re
from typing import Callable, Mapping, Optional

from .github_provider import RunBinding
from .verifier import Authorization, GateAttestation, MissionSnapshot, TransitionAttestation

_HEX = re.compile(r"^[0-9a-f]{64}$")
_SHA = re.compile(r"^[0-9a-f]{40}$")
_TOKEN = re.compile(r"^[A-Za-z0-9_.:-]{1,128}$")
_MIN_KEY_BYTES = 32

class AuthorityUnavailable(RuntimeError):
    """Protected host issuance, signature, freshness or revision unavailable."""


def canonical_json(data: Mapping) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), allow_nan=False,
                      ensure_ascii=True).encode("utf-8")


@dataclass(frozen=True)
class SealedSnapshot:
    """Authenticated host-issued envelope. Payload cannot be edited after signing."""
    payload: Mapping
    mac_hex: str


class SignedSnapshotAuthority:
    """Read-only HostAuthority backed by a protected signed mission snapshot.

    The key lookup and latest revision MUST be from protected host state; caller-
    supplied key/revision or signed JSON without trusted issuer authentication is
    NOT evidence of user consent. Never expose a signing endpoint to Workers.
    """
    def __init__(
        self, sealed: SealedSnapshot, *,
        expected_issuer: str, expected_audience: str,
        key_lookup: Callable[[str], Optional[bytes]],
        trusted_latest_revision: Callable[[str], Optional[int]],
        clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ):
        if not isinstance(sealed, SealedSnapshot) or not callable(key_lookup) or not callable(trusted_latest_revision):
            raise AuthorityUnavailable("Missing protected authority dependencies")
        self._sealed = sealed
        self._issuer = expected_issuer
        self._audience = expected_audience
        self._key_lookup = key_lookup
        self._latest = trusted_latest_revision
        self._clock = clock
        self._read()  # Fail closed at construction.

    def _read(self) -> Mapping:
        try:
            p = self._sealed.payload
            if not isinstance(p, dict) or not isinstance(self._sealed.mac_hex, str):
                raise AuthorityUnavailable("Invalid signed envelope")
            if len(canonical_json(p)) > 250_000 or not _HEX.fullmatch(self._sealed.mac_hex):
                raise AuthorityUnavailable("Invalid signed envelope size or MAC")
            for f in ("issuer", "audience", "key_id", "mission_id", "authorization_ref"):
                if not isinstance(p.get(f), str) or not _TOKEN.fullmatch(p[f]):
                    raise AuthorityUnavailable("Invalid issuer/mission identifier")
            if p.get("version") != "cto-d4-snapshot-1" or p["issuer"] != self._issuer or p["audience"] != self._audience:
                raise AuthorityUnavailable("Wrong issuer, audience or snapshot version")
            key = self._key_lookup(p["key_id"])
            if not isinstance(key, bytes) or len(key) < _MIN_KEY_BYTES:
                raise AuthorityUnavailable("Signing key unavailable")
            expected = hmac.new(key, canonical_json(p), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(expected, self._sealed.mac_hex):
                raise AuthorityUnavailable("Signed snapshot integrity failure")
            if type(p.get("revision")) is not int or p["revision"] < 1:
                raise AuthorityUnavailable("Invalid revision")
            current = self._latest(p["mission_id"])
            if type(current) is not int or current != p["revision"]:
                raise AuthorityUnavailable("Stale or uncommitted mission revision")
            now = self._clock()
            if not isinstance(now, datetime) or now.tzinfo is None:
                raise AuthorityUnavailable("Missing UTC clock")
            now_sec = int(now.astimezone(timezone.utc).timestamp())
            issued, expires = p.get("issued_at"), p.get("expires_at")
            if (type(issued) is not int or type(expires) is not int or
                    expires <= issued or issued > now_sec or now_sec >= expires or
                    expires - issued > 3600):
                raise AuthorityUnavailable("Expired, future or overlong grant")
            if p.get("revoked") is not False:
                raise AuthorityUnavailable("Revoked/missing grant status")
            scope = p.get("scope")
            if (not isinstance(scope, dict) or scope.get("mission_id") != p["mission_id"]
                    or scope.get("authorization_ref") != p["authorization_ref"]
                    or type(scope.get("repository_id")) is not int or scope["repository_id"] < 1
                    or not isinstance(scope.get("repository"), str)
                    or not isinstance(scope.get("branch"), str)
                    or not isinstance(scope.get("source_sha"), str)
                    or not _SHA.fullmatch(scope["source_sha"])
                    or not isinstance(scope.get("principal_id"), str)
                    or not scope["principal_id"]):
                raise AuthorityUnavailable("Invalid authorized scope")
            for field in ("teams", "actions", "head_decisions", "task_ids"):
                if not isinstance(scope.get(field), list) or not scope[field] or not all(
                    isinstance(v, str) and _TOKEN.fullmatch(v) for v in scope[field]
                ) or len(set(scope[field])) != len(scope[field]):
                    raise AuthorityUnavailable("Invalid scoped permissions")
            for field in ("dispatches", "transitions", "gates", "run_bindings"):
                if not isinstance(p.get(field), list) or not all(isinstance(x, dict) for x in p[field]):
                    raise AuthorityUnavailable("Invalid signed event collection")
            snapshot = p.get("snapshot")
            if not isinstance(snapshot, dict) or snapshot.get("mission_id") != p["mission_id"]:
                raise AuthorityUnavailable("Missing signed mission state")
            if (snapshot.get("source_sha") != scope["source_sha"] or
                    snapshot.get("phase") != "HEAD_DECISION" or
                    snapshot.get("active_team") is not None or snapshot.get("active_task_id") is not None):
                raise AuthorityUnavailable("Mission not at quiescent Head decision")
            for field, key_field in (("dispatches", "task_id"), ("transitions", "transition_id"),
                                     ("gates", "record_id"), ("run_bindings", "provider_record_id")):
                values = [row.get(key_field) for row in p[field]]
                if any(not isinstance(v, str) or not v for v in values) or len(values) != len(set(values)):
                    raise AuthorityUnavailable("Missing or duplicate signed event IDs")
                if any(row.get("mission_id") != p["mission_id"] or
                       row.get("source_sha") != scope["source_sha"] for row in p[field]):
                    raise AuthorityUnavailable("Cross-mission or stale signed event")
            if any(row.get("task_id") not in scope["task_ids"] or
                   row.get("team") not in scope["teams"] for row in p["dispatches"]):
                raise AuthorityUnavailable("Unapproved signed dispatch")
            for row in p["run_bindings"]:
                if (row.get("repository") != scope["repository"] or
                        row.get("repository_id") != scope["repository_id"] or
                        row.get("branch") != scope["branch"] or
                        row.get("task_id") not in scope["task_ids"]):
                    raise AuthorityUnavailable("Unapproved run binding")
            return p
        except AuthorityUnavailable:
            raise
        except (KeyError, TypeError, ValueError, OverflowError, UnicodeError, RecursionError) as exc:
            raise AuthorityUnavailable("Malformed or unavailable protected authority") from exc

    def authorization(self, mission_id: str, authorization_ref: str) -> Optional[Authorization]:
        p = self._read()
        scope = p["scope"]
        if (mission_id, authorization_ref) != (p["mission_id"], p["authorization_ref"]):
            return None
        return Authorization(
            mission_id, authorization_ref, scope["repository"], scope["branch"],
            scope["source_sha"], scope["principal_id"], frozenset(scope["teams"]),
            frozenset(scope["actions"]), frozenset(scope["head_decisions"]),
            frozenset(scope["task_ids"]), True
        )

    def expected_repository_id(self, repository: str) -> Optional[int]:
        p = self._read()
        return p["scope"]["repository_id"] if repository == p["scope"]["repository"] else None

    def authorized_dispatch(self, mission_id: str, task_id: str, team: str, source_sha: str) -> bool:
        p = self._read()
        return any(row.get("mission_id") == mission_id and row.get("task_id") == task_id
                   and row.get("team") == team and row.get("source_sha") == source_sha
                   and row.get("actor") == "HEAD" and row.get("approved") is True
                   for row in p["dispatches"])

    def authenticate_transition(self, transition_id: str) -> Optional[TransitionAttestation]:
        p = self._read()
        row = next((x for x in p["transitions"] if x["transition_id"] == transition_id), None)
        if row is None:
            return None
        try:
            return TransitionAttestation(
                p["mission_id"], transition_id, row["from_phase"], row["to_phase"],
                row["actor"], row["source_sha"], row["task_id"], row["team"],
                row.get("approved") is True
            )
        except (KeyError, TypeError, ValueError):
            return None

    def authenticate_gate(self, record_id: str) -> Optional[GateAttestation]:
        p = self._read()
        row = next((x for x in p["gates"] if x["record_id"] == record_id), None)
        if row is None:
            return None
        try:
            return GateAttestation(
                p["mission_id"], record_id, row["phase"], row["verdict"],
                row["source_sha"], frozenset(row["criterion_ids"]),
                frozenset(row["evidence_refs"]), row["role"], row["verifier_ref"],
                row.get("approved") is True
            )
        except (KeyError, TypeError, ValueError):
            return None

    def mission_snapshot(self, mission_id: str) -> Optional[MissionSnapshot]:
        p = self._read()
        s = p["snapshot"]
        if p["mission_id"] != mission_id:
            return None
        return MissionSnapshot(mission_id, s["phase"], s["active_team"],
                               s["active_task_id"], s["source_sha"], True)

    def run_binding(self, provider_record_id: str) -> Optional[RunBinding]:
        p = self._read()
        row = next((x for x in p["run_bindings"] if x["provider_record_id"] == provider_record_id), None)
        if row is None:
            return None
        try:
            return RunBinding(
                p["mission_id"], row["task_id"], row["criterion_id"],
                row["repository_id"], row["repository"], row["branch"],
                row["source_sha"], row["run_id"], row["run_attempt"],
                row["workflow_path"], row["event"],
                tuple(row["required_jobs"]),
                tuple((v[0], v[1]) for v in row["required_job_steps"])
            )
        except (KeyError, TypeError, ValueError, IndexError):
            return None

    def exclusive_write_enforced(self, mission_id: str, repository: str, branch: str) -> bool:
        self._read()
        return False  # Deliberately never infer a cloud write lock from signed read-only records.
