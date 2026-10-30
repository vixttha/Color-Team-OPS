"""Yellow Team host-authority control plane: provider-neutral, fail-closed reference.

The trusted cloud gateway MUST supply an IdentityBoundary and EvidenceBoundary.
This module does not authenticate end users from caller-supplied labels/tokens.
SQLiteJournal is an isolated development test adapter, NOT a hosted deployment,
tamper-proof audit log, KMS, or production cross-replica backend.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Optional, Mapping
import hashlib
import json
import re
import sqlite3
import time

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_ID = re.compile(r"^[a-zA-Z0-9_.:-]{1,128}$")


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


class HostRejected(RuntimeError):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


@dataclass(frozen=True)
class ConsentProof:
    subject: str
    consent_id: str
    intent_digest: str
    expires_at: int


@dataclass(frozen=True)
class ActorProof:
    subject: str
    operation: str
    mission_id: str


@dataclass(frozen=True)
class EvidenceProof:
    mission_id: str
    task_id: str
    source_sha: str
    criterion_id: str
    provider_record_id: str
    outcome: str


class IdentityBoundary(Protocol):
    """Protected host gateway verifies user consent & purpose-scoped actor tokens."""
    def verify_consent(self, token: str, intent_digest: str) -> Optional[ConsentProof]: ...
    def verify_actor(self, token: str, mission_id: str, operation: str) -> Optional[ActorProof]: ...


class EvidenceBoundary(Protocol):
    """Authenticated external provider observations, never user-entered PASS fields."""
    def current_sha(self, repository: str, branch: str) -> Optional[str]: ...
    def resolve(self, mission_id: str, task_id: str, source_sha: str,
                criterion_id: str, provider_record_id: str) -> Optional[EvidenceProof]: ...


class JournalPort(Protocol):
    """Cloud store adapter must provide durable, atomic, revision-CAS writes."""
    def create(self, mission_id: str, state: dict, event: dict) -> int: ...
    def append(self, mission_id: str, expected_revision: int, state: dict, event: dict) -> int: ...
    def read(self, mission_id: str) -> Optional[dict]: ...
    def history(self, mission_id: str) -> list[dict]: ...


class SQLiteDevelopmentJournal:
    """Persistent fixture journal; NOT a production identity/storage implementation.

    The DB file should live in a sandbox with owner-only permissions for tests.
    Hashes catch accidental or unsophisticated edits, not a privileged DB attacker
    who can recompute the chain. For actual cloud usage replace JournalPort with
    protected transactional storage, immutable external logging and auth.
    """
    def __init__(self, path: str):
        if not isinstance(path, str) or not path or path == ":memory:":
            raise ValueError("A persistent isolated test file path is required")
        self.path = path
        con = self._connect()
        try:
            con.execute("CREATE TABLE IF NOT EXISTS mission_events("
                        "mission_id TEXT NOT NULL, revision INTEGER NOT NULL,"
                        "event_id TEXT NOT NULL UNIQUE, entry TEXT NOT NULL,"
                        "previous_hash TEXT NOT NULL, entry_hash TEXT NOT NULL,"
                        "PRIMARY KEY(mission_id, revision))")
            con.execute("CREATE TABLE IF NOT EXISTS consent_claims("
                        "consent_id TEXT NOT NULL PRIMARY KEY, mission_id TEXT NOT NULL UNIQUE)")
        finally:
            con.close()

    def _connect(self):
        con = sqlite3.connect(self.path, timeout=5, isolation_level=None)
        con.execute("PRAGMA busy_timeout=5000")
        con.execute("PRAGMA synchronous=FULL")
        return con

    @staticmethod
    def _read_in_tx(con, mission_id: str) -> tuple[Optional[dict], int, str]:
        rows = con.execute(
            "SELECT revision, event_id, entry, previous_hash, entry_hash "
            "FROM mission_events WHERE mission_id=? ORDER BY revision", (mission_id,)
        ).fetchall()
        prior = "GENESIS"
        latest = None
        for index, (rev, event_id, data, previous, signature) in enumerate(rows, 1):
            if type(rev) is not int or rev != index or previous != prior:
                raise HostRejected("JOURNAL_INTEGRITY_FAILURE")
            try:
                entry = json.loads(data)
            except (ValueError, TypeError):
                raise HostRejected("JOURNAL_INTEGRITY_FAILURE") from None
            if not isinstance(entry, dict) or entry.get("event", {}).get("event_id") != event_id:
                raise HostRejected("JOURNAL_INTEGRITY_FAILURE")
            expected = digest(dict(mission_id=mission_id, revision=rev,
                                   previous_hash=prior, entry=entry))
            if expected != signature:
                raise HostRejected("JOURNAL_INTEGRITY_FAILURE")
            latest = entry["state"]
            prior = signature
        return latest, len(rows), prior

    @staticmethod
    def _write(con, mission_id: str, revision: int, previous: str, state: dict, event: dict):
        record = dict(state=state, event=event)
        signature = digest(dict(mission_id=mission_id, revision=revision,
                                previous_hash=previous, entry=record))
        con.execute(
            "INSERT INTO mission_events(mission_id,revision,event_id,entry,previous_hash,entry_hash)"
            "VALUES (?,?,?,?,?,?)",
            (mission_id, revision, event["event_id"], canonical(record), previous, signature)
        )

    def create(self, mission_id: str, state: dict, event: dict) -> int:
        con = self._connect()
        try:
            con.execute("BEGIN IMMEDIATE")
            old, rev, prev = self._read_in_tx(con, mission_id)
            if rev:
                raise HostRejected("MISSION_EXISTS")
            if event.get("kind")!="CONSENT_GRANTED" or not event.get("consent_id"):
                raise HostRejected("CONSENT_GRANT_REQUIRED")
            if con.execute("SELECT 1 FROM consent_claims WHERE consent_id=?",
                           (event["consent_id"],)).fetchone():
                raise HostRejected("CONSENT_REPLAY")
            self._write(con, mission_id, 1, prev, state, event)
            con.execute("INSERT INTO consent_claims(consent_id,mission_id) VALUES (?,?)",
                        (event["consent_id"],mission_id))
            con.commit()
            return 1
        except (sqlite3.IntegrityError, sqlite3.OperationalError) as exc:
            con.rollback()
            raise HostRejected("JOURNAL_WRITE_FAILED") from exc
        except Exception:
            con.rollback()
            raise
        finally:
            con.close()

    def append(self, mission_id: str, expected_revision: int, state: dict, event: dict) -> int:
        con = self._connect()
        try:
            con.execute("BEGIN IMMEDIATE")
            old, rev, prev = self._read_in_tx(con, mission_id)
            if old is None:
                raise HostRejected("MISSION_UNKNOWN")
            if rev != expected_revision:
                raise HostRejected("REVISION_CONFLICT")
            self._write(con, mission_id, rev + 1, prev, state, event)
            con.commit()
            return rev + 1
        except (sqlite3.IntegrityError, sqlite3.OperationalError) as exc:
            con.rollback()
            raise HostRejected("JOURNAL_WRITE_FAILED") from exc
        except Exception:
            con.rollback()
            raise
        finally:
            con.close()

    def read(self, mission_id: str) -> Optional[dict]:
        con = self._connect()
        try:
            con.execute("BEGIN")
            state, revision, _ = self._read_in_tx(con, mission_id)
            return dict(state, revision=revision) if state is not None else None
        finally:
            con.close()

    def history(self, mission_id: str) -> list[dict]:
        con = self._connect()
        try:
            con.execute("BEGIN")
            _, _, _ = self._read_in_tx(con, mission_id)
            rows = con.execute(
                "SELECT revision,entry_hash,entry FROM mission_events "
                "WHERE mission_id=? ORDER BY revision", (mission_id,)
            ).fetchall()
            return [dict(revision=rev, hash=h, **json.loads(data)["event"]) for rev,h,data in rows]
        finally:
            con.close()


class CloudAuthorityEngine:
    """Trusted gateway-facing lifecycle; caller never supplies authenticated roles.

    Tokens are opaque to this class and MUST be verified by a genuine cloud
    identity adapter. Development fixtures can exercise behavior but cannot
    authenticate ChatGPT users. No API, KMS, signing endpoint or cloud deployment.
    """
    def __init__(self, journal: JournalPort, identity: IdentityBoundary,
                 evidence: EvidenceBoundary, clock=time.time):
        self.store, self.identity, self.evidence, self.clock = journal, identity, evidence, clock

    def _now(self):
        return int(self.clock())

    def _actor(self, token, mission_id, operation):
        try:
            actor = self.identity.verify_actor(token, mission_id, operation)
        except Exception:
            raise HostRejected("IDENTITY_UNVERIFIED") from None
        if (not isinstance(actor, ActorProof) or not actor.subject or
                actor.mission_id != mission_id or actor.operation != operation):
            raise HostRejected("IDENTITY_UNVERIFIED")
        return actor.subject

    def _fresh_sha(self, state):
        try:
            current = self.evidence.current_sha(state["repository"], state["branch"])
        except Exception:
            raise HostRejected("SOURCE_UNVERIFIED") from None
        if current is None:
            raise HostRejected("SOURCE_UNVERIFIED")
        if current != state["source_sha"]:
            raise HostRejected("STALE_SOURCE")

    @staticmethod
    def _require_id(value):
        if not isinstance(value, str) or not _ID.fullmatch(value):
            raise HostRejected("INVALID_IDENTIFIER")

    def authorize(self, intent: Mapping, *, consent_token: str, event_id: str):
        """Explicit consent must be for the canonical EXACT request, incl. scope."""
        self._require_id(event_id)
        if not isinstance(intent, dict):
            raise HostRejected("INVALID_INTENT")
        mandatory = ("mission_id","repository","branch","source_sha",
                     "allowed_teams","required_teams","allowed_actions","criteria",
                     "max_handoffs")
        if any(k not in intent for k in mandatory) or set(intent) != set(mandatory):
            raise HostRejected("INVALID_INTENT")
        mission_id = intent["mission_id"]
        self._require_id(mission_id)
        if (not isinstance(intent["source_sha"], str) or not _HEX40.fullmatch(intent["source_sha"])
                or not isinstance(intent["repository"], str) or not intent["repository"]
                or not isinstance(intent["branch"], str) or not intent["branch"]):
            raise HostRejected("INVALID_SCOPE")
        for key in ("allowed_teams", "required_teams", "allowed_actions", "criteria"):
            xs = intent[key]
            if (not isinstance(xs, list) or not xs or len(xs) != len(set(
                    str(x) for x in xs)) or any(not isinstance(x,str) or not _ID.fullmatch(x) for x in xs)):
                raise HostRejected("INVALID_SCOPE")
        if not set(intent["required_teams"]).issubset(set(intent["allowed_teams"])):
            raise HostRejected("INVALID_SCOPE")
        if (type(intent["max_handoffs"]) is not int or intent["max_handoffs"] < 0
                or intent["max_handoffs"] >= len(intent["allowed_teams"])):
            raise HostRejected("INVALID_HANDOFF_BUDGET")
        if any(x not in ("read", "inspect", "report") for x in intent["allowed_actions"]):
            raise HostRejected("READ_ONLY_PILOT_SCOPE")
        request_digest = digest(intent)
        try:
            consent = self.identity.verify_consent(consent_token, request_digest)
        except Exception:
            raise HostRejected("CONSENT_UNVERIFIED") from None
        if (not isinstance(consent, ConsentProof) or not consent.subject
                or not isinstance(consent.consent_id, str) or not _ID.fullmatch(consent.consent_id)
                or consent.intent_digest != request_digest or
                type(consent.expires_at) is not int or consent.expires_at <= self._now()
                or consent.expires_at - self._now() > 3600):
            raise HostRejected("CONSENT_UNVERIFIED")
        state = dict(intent, head_subject=consent.subject, consent_id=consent.consent_id,
                     consent_digest=request_digest, expires_at=consent.expires_at,
                     phase="HEAD_READY", task=None, used_task_ids=[], used_receipts=[],
                     approved_teams=[], validated_criteria=[],
                     gates=[], revoked=False, completion=None)
        self._fresh_sha(state)
        self.store.create(mission_id, state,
                          dict(event_id=event_id, kind="CONSENT_GRANTED", subject=consent.subject,
                               action="authorize", consent_id=consent.consent_id, at=self._now()))
        return self.read(mission_id)

    def read(self, mission_id):
        data = self.store.read(mission_id)
        if data is None:
            raise HostRejected("MISSION_UNKNOWN")
        if data["revoked"] or data["phase"] == "REVOKED":
            raise HostRejected("GRANT_REVOKED")
        if self._now() >= data["expires_at"]:
            raise HostRejected("GRANT_EXPIRED")
        return data

    def _load(self, mission_id, expected_revision, operation, token, *, require_head=False):
        state = self.read(mission_id)
        if state["revision"] != expected_revision:
            raise HostRejected("REVISION_CONFLICT")
        subject = self._actor(token, mission_id, operation)
        if require_head and subject != state["head_subject"]:
            raise HostRejected("HEAD_NOT_AUTHORIZED")
        self._fresh_sha(state)
        return state, subject

    def _append(self, state, event_id, kind, subject, changes):
        self._require_id(event_id)
        updated = {k:v for k,v in state.items() if k != "revision"}
        updated.update(changes)
        self.store.append(state["mission_id"], state["revision"], updated,
                          dict(event_id=event_id, kind=kind, subject=subject,
                               action=kind.lower(), at=self._now()))
        return self.read(state["mission_id"])

    def dispatch(self, mission_id, expected_revision, token, event_id, *, team, task_id, criterion):
        state, subject = self._load(mission_id,expected_revision,"head_dispatch",token,require_head=True)
        self._require_id(task_id)
        if state["phase"] not in ("HEAD_READY","HEAD_DECISION") or state["task"] is not None:
            raise HostRejected("BAD_PHASE")
        if team not in state["allowed_teams"] or criterion not in state["criteria"]:
            raise HostRejected("TASK_NOT_AUTHORIZED")
        if team in state["approved_teams"]:
            raise HostRejected("TEAM_ALREADY_COMPLETE")
        if len(state["used_task_ids"]) > state["max_handoffs"]:
            raise HostRejected("HANDOFF_BUDGET_EXCEEDED")
        if task_id in state["used_task_ids"]:
            raise HostRejected("TASK_REPLAY")
        return self._append(state,event_id,"DISPATCH",subject,
                            dict(phase="WORKER_ACTIVE",used_task_ids=state["used_task_ids"]+[task_id],
                                 task=dict(team=team,id=task_id,criterion=criterion,
                                           receipt=None,worker=None)))

    def worker_done(self,mission_id,expected_revision,token,event_id,*,task_id,provider_record_id):
        state, subject = self._load(mission_id,expected_revision,"worker_report",token)
        if state["phase"]!="WORKER_ACTIVE" or state["task"]["id"]!=task_id:
            raise HostRejected("BAD_PHASE")
        self._require_id(provider_record_id)
        if provider_record_id in state["used_receipts"]:
            raise HostRejected("EVIDENCE_REPLAY")
        task=dict(state["task"],receipt=provider_record_id,worker=subject)
        return self._append(state,event_id,"WORKER_REPORTED",subject,
                            dict(phase="VALIDATION_PENDING",task=task,
                                 used_receipts=state["used_receipts"]+[provider_record_id]))

    def _observe(self,state):
        task=state["task"]
        try:
            obs=self.evidence.resolve(state["mission_id"],task["id"],state["source_sha"],
                                      task["criterion"],task["receipt"])
        except Exception:
            raise HostRejected("EVIDENCE_UNVERIFIED") from None
        if obs is None:
            raise HostRejected("EVIDENCE_UNVERIFIED")
        if not isinstance(obs,EvidenceProof) or (
                obs.mission_id,obs.task_id,obs.source_sha,obs.criterion_id,
                obs.provider_record_id)!=(state["mission_id"],task["id"],state["source_sha"],
                                           task["criterion"],task["receipt"]):
            raise HostRejected("EVIDENCE_SCOPE_MISMATCH")
        if obs.outcome!="PASS":
            raise HostRejected("EVIDENCE_NOT_PASS")
        return obs

    def validate(self,mission_id,expected_revision,token,event_id):
        state,subject=self._load(mission_id,expected_revision,"validate",token)
        if state["phase"]!="VALIDATION_PENDING":
            raise HostRejected("BAD_PHASE")
        self._observe(state)
        gate=dict(phase="VALIDATE",subject=subject,task_id=state["task"]["id"],
                  criterion=state["task"]["criterion"],sha=state["source_sha"],
                  evidence_ref=state["task"]["receipt"],verdict="PASS")
        return self._append(state,event_id,"VALIDATION_PASSED",subject,
                            dict(phase="INTERNAL_AUDIT_PENDING",gates=state["gates"]+[gate]))

    def audit(self,mission_id,expected_revision,token,event_id):
        state,subject=self._load(mission_id,expected_revision,"internal_audit",token)
        if state["phase"]!="INTERNAL_AUDIT_PENDING":
            raise HostRejected("BAD_PHASE")
        self._observe(state)  # Fresh independently resolved receipt; no worker PASS reuse.
        task=state["task"]
        if not state["gates"] or state["gates"][-1]["phase"]!="VALIDATE" or (
                state["gates"][-1]["sha"],state["gates"][-1]["task_id"])!=(state["source_sha"],task["id"]):
            raise HostRejected("VALIDATION_MISSING")
        gate=dict(phase="INTERNAL_AUDIT",subject=subject,task_id=task["id"],
                  criterion=task["criterion"],sha=state["source_sha"],
                  evidence_ref=task["receipt"],verdict="PASS")
        return self._append(state,event_id,"AUDIT_PASSED",subject,
                            dict(phase="HEAD_DECISION",gates=state["gates"]+[gate],
                                 approved_teams=state["approved_teams"]+[task["team"]],
                                 validated_criteria=list(dict.fromkeys(state["validated_criteria"]+[task["criterion"]])),
                                 task=None))

    def complete(self,mission_id,expected_revision,token,event_id):
        state,subject=self._load(mission_id,expected_revision,"head_complete",token,require_head=True)
        if state["phase"]!="HEAD_DECISION" or state["task"] is not None:
            raise HostRejected("BAD_PHASE")
        if not set(state["required_teams"]).issubset(state["approved_teams"]) or not set(
                state["criteria"]).issubset(state["validated_criteria"]):
            raise HostRejected("INCOMPLETE_CRITERIA")
        if len([x for x in state["gates"] if x["phase"]=="VALIDATE"])<1 or len(
                [x for x in state["gates"] if x["phase"]=="INTERNAL_AUDIT"])<1:
            raise HostRejected("MISSING_GATE")
        return self._append(state,event_id,"HEAD_COMPLETED",subject,
                            dict(phase="COMPLETE",completion="INTERNAL_READ_ONLY_VERIFIED"))

    def revoke(self,mission_id,expected_revision,token,event_id):
        # Revocation is allowed after expiry: identity still must authorize HEAD.
        state=self.store.read(mission_id)
        if state is None:
            raise HostRejected("MISSION_UNKNOWN")
        if state["revision"]!=expected_revision:
            raise HostRejected("REVISION_CONFLICT")
        if state["revoked"]:
            raise HostRejected("GRANT_REVOKED")
        actor=self._actor(token,mission_id,"head_revoke")
        if actor!=state["head_subject"]:
            raise HostRejected("HEAD_NOT_AUTHORIZED")
        self._require_id(event_id)
        revised={k:v for k,v in state.items() if k!="revision"}
        revised.update(phase="REVOKED",revoked=True,completion=None,task=None)
        return self.store.append(mission_id,expected_revision,revised,
             dict(event_id=event_id,kind="REVOKED",subject=actor,action="head_revoke",at=self._now()))
