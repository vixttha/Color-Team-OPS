"""Owner-controlled GitHub self-hosted runner *pre-job* admission guard.

Candidate v0.3: to be installed only by the host administrator outside any checkout.
No CLI argument can bypass approval validation. Does NOT itself grant owner consent.

Runs before job workflow steps via ACTIONS_RUNNER_HOOK_JOB_STARTED.
A host must prove all GitHub variables are present and authentic in this phase.
"""
from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Mapping

# Root/admin-controlled location; deliberately NOT configurable via workflow env.
LINUX_APPROVALS = Path('/etc/color-team-ops/runner-gate/approvals')
WINDOWS_APPROVALS = Path(r'C:\CTOPSRunnerGate\approvals')
_SHA = re.compile(r'^[0-9a-f]{40}$')
_REPO = re.compile(r'^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$')
_SAFE_ID = re.compile(r'^[A-Za-z0-9_-]{1,100}$')
_UINT = re.compile(r'^[1-9][0-9]{0,18}$')
_FIELDS = {
    'repository': 'GITHUB_REPOSITORY',
    'sha': 'GITHUB_SHA',
    'workflow_ref': 'GITHUB_WORKFLOW_REF',
    'workflow_sha': 'GITHUB_WORKFLOW_SHA',
    'job_key': 'GITHUB_JOB',
    'runner': 'RUNNER_NAME',
    'runner_os': 'RUNNER_OS',
    'run_id': 'GITHUB_RUN_ID',
    'attempt': 'GITHUB_RUN_ATTEMPT',
}

class Denied(Exception):
    """Expected fail-closed denial, with non-sensitive reason."""


def _unique_pairs(pairs):
    output = {}
    for key, value in pairs:
        if key in output:
            raise Denied('duplicate JSON key')
        output[key] = value
    return output


def context_from_env(env: Mapping[str, str]) -> dict[str, str]:
    data = {}
    for name, key in _FIELDS.items():
        value = env.get(key)
        if not isinstance(value, str) or not value or len(value) > 1024 or value != value.strip():
            raise Denied(f'missing or invalid {key}')
        data[name] = value
    if data['repository'] != 'vixttha/Color-Team-OPS' or not _REPO.fullmatch(data['repository']):
        raise Denied('repository mismatch')
    if not _SHA.fullmatch(data['sha']) or not _SHA.fullmatch(data['workflow_sha']):
        raise Denied('invalid executable or workflow SHA')
    if (not data['workflow_ref'].startswith(data['repository'] + '/.github/workflows/')
            or '@refs/heads/' not in data['workflow_ref'] or ' ' in data['workflow_ref']):
        raise Denied('invalid workflow ref')
    if not _SAFE_ID.fullmatch(data['job_key']) or not _SAFE_ID.fullmatch(data['runner']):
        raise Denied('invalid job key or runner')
    if (data['runner_os'], data['runner']) not in (
        ('Linux', 'color-team-ops-linux-01'), ('Windows', 'color-team-ops-windows-01')
    ):
        raise Denied('unknown owner runner OS/name pairing')
    if not _UINT.fullmatch(data['run_id']) or not _UINT.fullmatch(data['attempt']):
        raise Denied('invalid run ID or attempt')
    if env.get('RUNNER_ENVIRONMENT') != 'self-hosted':
        raise Denied('not self-hosted')
    return data


def _utc_iso(value: str) -> dt.datetime:
    if not isinstance(value, str) or not value.endswith('Z'):
        raise Denied('invalid UTC timestamp')
    try:
        parsed = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as exc:
        raise Denied('invalid UTC timestamp') from exc
    if parsed.utcoffset() != dt.timedelta(0):
        raise Denied('timestamp not UTC')
    return parsed


def permit_valid(permit: object, observed: Mapping[str, str], now: dt.datetime) -> None:
    if not isinstance(permit, dict):
        raise Denied('approval is not a JSON object')
    if set(permit) != set(_FIELDS) | {'issued_at', 'expires_at', 'schema'}:
        raise Denied('approval schema mismatch')
    if type(permit['schema']) is not int or permit['schema'] != 1:
        raise Denied('unsupported approval schema')
    for name in _FIELDS:
        if not isinstance(permit[name], str) or permit[name] != observed[name]:
            raise Denied(f'approval {name} mismatch')
    start, stop = _utc_iso(permit['issued_at']), _utc_iso(permit['expires_at'])
    if stop <= start or (stop - start) > dt.timedelta(minutes=15):
        raise Denied('invalid approval validity interval')
    if not (start <= now <= stop):
        raise Denied('approval stale or future')


def _protected_unix_path(path: Path, *, directory: bool) -> None:
    """Defend against link replacement and ancestor write access.

    Admin-owned root (uid 0), ancestors are not group/world writable.
    OS ACLs, mount policy, interpreter and runner config require separate host audit.
    """
    if not path.is_absolute():
        raise Denied('relative trusted path')
    for candidate in (path, *path.parents):
        try:
            info = candidate.lstat()
        except OSError as exc:
            raise Denied('trusted path unavailable') from exc
        if stat.S_ISLNK(info.st_mode):
            raise Denied('symlink in protected path')
        should_dir = directory or candidate != path
        if should_dir and not stat.S_ISDIR(info.st_mode):
            raise Denied('expected directory')
        if not should_dir and not stat.S_ISREG(info.st_mode):
            raise Denied('expected regular file')
        if info.st_uid != 0 or info.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
            raise Denied('trusted path is not admin-controlled')


def _approval_filename(observed: Mapping[str, str]) -> str:
    return f"{observed['run_id']}-{observed['attempt']}-{observed['job_key']}-{observed['runner']}.json"


def verify_from_disk(env: Mapping[str, str], now: dt.datetime | None = None) -> None:
    observed = context_from_env(env)
    if os.name == 'posix' and sys.platform == 'linux':
        if os.geteuid() == 0:
            raise Denied('runner service must not be root')
        if observed['runner_os'] != 'Linux':
            raise Denied('host OS mismatch')
        approvals = LINUX_APPROVALS
        _protected_unix_path(approvals, directory=True)
        approval_path = approvals / _approval_filename(observed)
        _protected_unix_path(approval_path, directory=False)
    elif os.name == 'nt':
        if observed['runner_os'] != 'Windows':
            raise Denied('host OS mismatch')
        # The admin-installed PowerShell hook MUST validate Windows ACLs, owner,
        # all ancestors, and the exact candidate approval before invoking Python.
        # This is not a standalone authorization to run the Python module.
        approvals = WINDOWS_APPROVALS
        approval_path = approvals / _approval_filename(observed)
    else:
        raise Denied('unsupported OS')
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_CLOEXEC', 0)
    try:
        fd = os.open(approval_path, flags)
        with os.fdopen(fd, 'rb') as handle:
            info = os.fstat(handle.fileno())
            if (info.st_uid != 0 or not stat.S_ISREG(info.st_mode)
                    or info.st_mode & (stat.S_IWGRP | stat.S_IWOTH)
                    or info.st_size <= 0 or info.st_size > 4096):
                raise Denied('approval file not protected')
            raw = handle.read(4097)
            if len(raw) > 4096:
                raise Denied('approval exceeds size limit')
    except OSError as exc:
        raise Denied('approval file unavailable') from exc
    try:
        permit = json.loads(raw.decode('utf-8'), object_pairs_hook=_unique_pairs)
    except (ValueError, UnicodeError, TypeError) as exc:
        raise Denied('invalid approval JSON') from exc
    permit_valid(permit, observed, now or dt.datetime.now(dt.timezone.utc))


def main() -> int:
    try:
        verify_from_disk(os.environ)
    except Denied as exc:
        print(f'CTO_RUNNER_GATE_DENY: {exc}', flush=True)
        return 64
    except Exception:
        print('CTO_RUNNER_GATE_DENY: unexpected validation error', flush=True)
        return 65
    print('CTO_RUNNER_GATE_ALLOW: exact job bound to admin-controlled approval', flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())