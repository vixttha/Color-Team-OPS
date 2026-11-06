"""Owner-authorized Windows self-hosted runner preflight, strictly read-only.

Does not invoke a model, write evaluation evidence, alter Codex login, export
credentials, inspect secrets, or modify an installed plugin. No raw paths, login
messages, candidate text, model responses, or token strings are printed.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

FROZEN_REL = Path("evaluation/v0.0.2/CLI-EVAL-SOLO-FREEZE-v2.json")
ARMS = frozenset(("generic", "full", "no_directory", "no_handoff"))
MAX_ATTEMPT_FILES = 3000
SAFE_ENV = frozenset((
    "PATH", "SYSTEMROOT", "WINDIR", "TEMP", "TMP", "USERPROFILE",
    "HOMEDRIVE", "HOMEPATH", "APPDATA", "LOCALAPPDATA", "PROGRAMDATA",
    "PROGRAMFILES", "PROGRAMFILES(X86)", "COMSPEC", "PATHEXT", "CODEX_HOME",
))


def canonical_sha(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def file_sha(path):
    h = hashlib.sha256()
    with path.open("rb") as reader:
        while True:
            data = reader.read(262144)
            if not data:
                break
            h.update(data)
    return h.hexdigest()


def git_check(root, *args):
    try:
        env = dict(os.environ, GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0")
        run = subprocess.run(["git", "-C", str(root), *args],
                             capture_output=True, timeout=8, check=False, env=env)
        return run.stdout if run.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def checkout_candidates():
    """Only inspect the owner's already documented project folder and children."""
    bases = []
    workspace = os.environ.get("GITHUB_WORKSPACE", "")
    if workspace:
        for ancestor in (Path(workspace), *Path(workspace).parents):
            if ancestor.name.casefold() == "color-team-ops-project":
                bases.append(ancestor)
                break
    home = os.environ.get("USERPROFILE", "")
    if home:
        bases.append(Path(home) / "Desktop" / "Color-Team-OPS-Project")
    roots = []
    for base in bases:
        roots.extend((
            base / "Color-Team-OPS-Agent",
            base / "Color-Team-OPS-Agent" / "Color-Team-OPS",
            base / "Color-Team-OPS",
            base,
        ))
    # Deduplicate, with no filesystem-wide search or traversal.
    return list(dict.fromkeys(roots))


def resolve_checkout(namespace):
    options = []
    for root in checkout_candidates():
        private = root / ".cli-eval-private" / "solo-v1" / namespace
        if private.is_dir():
            options.append((root, private))
    if len(options) != 1:
        return None, None, "NONE" if not options else "MULTIPLE"
    return options[0][0], options[0][1], "ONE"


def resolve_codex():
    executable = shutil.which("codex")
    if not executable:
        return None, False
    path = Path(executable)
    if path.suffix.casefold() != ".exe":
        vendor = path.parent / "node_modules" / "@openai" / "codex" / "node_modules" / "@openai" / "codex-win32-x64" / "vendor"
        native = list(vendor.glob("**/codex.exe")) if vendor.is_dir() else []
        if len(native) == 1:
            return str(native[0]), True
    return executable, path.suffix.casefold() == ".exe"


def command_check(executable, args, timeout):
    env = {key: value for key, value in os.environ.items()
           if key.upper() in SAFE_ENV}
    try:
        completed = subprocess.run([executable, *args],
                                   env=env, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, timeout=timeout,
                                   check=False)
        # Sensitive stdout/stderr are never returned to logs.
        return completed.returncode, completed.stdout + completed.stderr
    except subprocess.TimeoutExpired:
        return None, b""
    except OSError:
        return -1, b""


def inspect_codex():
    executable, native = resolve_codex()
    report = {
        "present_on_runner_path": bool(executable),
        "native_executable": native,
        "version": None,
        "login": "NOT_CHECKED",
    }
    if not executable:
        report["login"] = "CLI_NOT_FOUND"
        return report
    code, raw = command_check(executable, ["--version"], 12)
    found = re.search(rb"(?<!\d)\d+\.\d+\.\d+(?!\d)", raw)
    report["version"] = found.group().decode("ascii") if code == 0 and found else None
    code, raw = command_check(executable, ["login", "status"], 18)
    if code is None:
        report["login"] = "STATUS_TIMED_OUT"
    elif code != 0:
        report["login"] = "NOT_AUTHENTICATED_OR_INACCESSIBLE"
    elif b"ChatGPT" in raw:
        report["login"] = "CHATGPT_ACCOUNT_REPORTED"
    else:
        report["login"] = "SUCCESS_UNCLASSIFIED_AUTH_TYPE"
    return report


def bounded_receipts(private, pattern):
    found = sorted(private.glob(pattern))
    if len(found) > MAX_ATTEMPT_FILES:
        raise ValueError("ATTEMPT_COUNT_EXCEEDS_SAFE_BOUND")
    return found


def hashes_match(receipt, directory, grade=False):
    for filename, field in (
        ("stdout.jsonl", "raw_sha256"),
        ("stderr.txt", "stderr_sha256"),
    ):
        target = directory / filename
        if not target.is_file() or file_sha(target) != receipt.get(field):
            return False
    inp = directory / "input.json"
    if not inp.is_file():
        return False
    if grade:
        if file_sha(inp) != receipt.get("input_sha256"):
            return False
        if receipt.get("status") == "GRADED":
            grade_file = directory / "grade.json"
            if not grade_file.is_file():
                return False
            try:
                saved = json.loads(grade_file.read_text(encoding="utf-8"))
                if canonical_sha(saved) != receipt.get("grade_sha256"):
                    return False
            except (ValueError, OSError):
                return False
    else:
        if hashlib.sha256(inp.read_text(encoding="utf-8").encode("utf-8")).hexdigest() != receipt.get("input_sha256"):
            return False
    return True


def inspect_checkpoints(root, private, frozen, freeze_sha):
    summary = {
        "checkout_source_files_matching_frozen": 0,
        "checkout_source_files_required": len(frozen["file_sha256"]),
        "checkout_HEAD_has_exact_freeze": False,
        "checkout_clean_for_frozen_execution": False,
        "candidate_attempts": 0,
        "candidate_completed": 0,
        "distinct_completed_pairs": 0,
        "grader_attempts": 0,
        "grader_completed": 0,
        "distinct_graded_pairs": 0,
        "candidate_terminal_attempts": 0,
        "grader_terminal_attempts": 0,
        "grader_terminal_status_counts": {},
        "invalid_checkpoint_receipts": 0,
        "pilot_acceptance_bound_to_36_grades": False,
        "supervisor_lock_present": (private / "supervisor.lock").exists(),
    }
    for relative, digest in frozen["file_sha256"].items():
        local = root / relative
        if local.is_file() and file_sha(local) == digest:
            summary["checkout_source_files_matching_frozen"] += 1

    head_freeze = git_check(root, "show", "HEAD:" + FROZEN_REL.as_posix())
    if head_freeze is not None:
        try:
            summary["checkout_HEAD_has_exact_freeze"] = (
                canonical_sha(json.loads(head_freeze)) == freeze_sha
            )
        except ValueError:
            pass
    dirty = git_check(root, "status", "--porcelain=v1", "--untracked-files=all")
    summary["checkout_clean_for_frozen_execution"] = dirty == b""

    candidate_paths = bounded_receipts(private, "candidates/*/*/receipt.json")
    grade_paths = bounded_receipts(private, "grades/*/*/receipt.json")
    summary["candidate_attempts"] = len(candidate_paths)
    summary["grader_attempts"] = len(grade_paths)
    completed = {}
    candidate_pair_seen = set()
    grader_pair_seen = set()
    for path in candidate_paths:
        try:
            receipt = json.loads(path.read_text(encoding="utf-8"))
            cid, arm = receipt.get("case_id"), receipt.get("arm")
            known_case = frozen["cases"].get(cid, {}) if isinstance(cid, str) else {}
            team = cid.split(":")[0] if isinstance(cid, str) else ""
            matched = (
                arm in ARMS and bool(known_case)
                and receipt.get("source_sha") == frozen["source_sha"]
                and receipt.get("freeze_sha256") == freeze_sha
                and receipt.get("environment_digest") == frozen["environment_digest"]
                and receipt.get("input_sha256") == known_case.get("input_sha256")
                and receipt.get("arm_sha256") == frozen["arm_material_sha256"].get(team, {}).get(arm)
                and hashes_match(receipt, path.parent)
            )
            if not matched:
                summary["invalid_checkpoint_receipts"] += 1
                continue
            pair = (cid, arm)
            if receipt.get("status") == "COMPLETED":
                summary["candidate_completed"] += 1
                if pair in candidate_pair_seen:
                    summary["invalid_checkpoint_receipts"] += 1
                candidate_pair_seen.add(pair)
                completed[receipt["raw_sha256"]] = pair
            elif receipt.get("status") in ("QUOTA_BLOCKED", "RATE_LIMIT_BLOCKED", "TIMEOUT", "INVALID_TRACE"):
                summary["candidate_terminal_attempts"] += 1
        except (ValueError, KeyError, TypeError, OSError, UnicodeError):
            summary["invalid_checkpoint_receipts"] += 1

    graded = set()
    for path in grade_paths:
        try:
            receipt = json.loads(path.read_text(encoding="utf-8"))
            binding = receipt.get("binding") or {}
            raw_id = binding.get("candidate_raw_sha256")
            linked = completed.get(raw_id)
            matching = (
                linked is not None
                and binding.get("source_sha") == frozen["source_sha"]
                and binding.get("freeze_sha256") == freeze_sha
                and binding.get("case_id") == linked[0]
                and binding.get("rubric_sha256") == frozen["cases"][linked[0]]["rubric_sha256"]
                and hashes_match(receipt, path.parent, grade=True)
            )
            if not matching:
                summary["invalid_checkpoint_receipts"] += 1
                continue
            if receipt.get("status") == "GRADED":
                summary["grader_completed"] += 1
                if linked in grader_pair_seen:
                    summary["invalid_checkpoint_receipts"] += 1
                grader_pair_seen.add(linked)
                graded.add(linked)
            elif receipt.get("status") in ("QUOTA_BLOCKED", "RATE_LIMIT_BLOCKED", "TIMEOUT", "INVALID_TRACE", "INVALID_GRADE"):
                summary["grader_terminal_attempts"] += 1
                status = receipt["status"]
                counts = summary["grader_terminal_status_counts"]
                counts[status] = counts.get(status, 0) + 1
        except (ValueError, KeyError, TypeError, OSError, UnicodeError):
            summary["invalid_checkpoint_receipts"] += 1
    summary["distinct_completed_pairs"] = len(candidate_pair_seen)
    summary["distinct_graded_pairs"] = len(graded)

    pilot_file = private / "pilot-acceptance.json"
    if pilot_file.is_file():
        try:
            acceptance = json.loads(pilot_file.read_text(encoding="utf-8"))
            expected = {tuple(pair) for pair in frozen["pilot_order"]}
            claimed = acceptance["summary"]
            summary["pilot_acceptance_bound_to_36_grades"] = (
                acceptance.get("freeze_sha256") == freeze_sha
                and len(expected) == 36
                and expected.issubset(graded)
                and claimed.get("candidate_completed") == 36
                and claimed.get("graded") == 36
            )
        except (ValueError, KeyError, TypeError, OSError):
            pass
    return summary


def main():
    if os.name != "nt" or os.environ.get("GITHUB_ACTIONS") != "true":
        print(json.dumps({"status": "NOT_AUTHORIZED_HOST_OR_CONTEXT"}))
        return 3
    workspace = Path(os.environ["GITHUB_WORKSPACE"])
    frozen = json.loads((workspace / FROZEN_REL).read_text(encoding="utf-8"))
    if (frozen.get("evaluation_mode") != "SOLO_DEVELOPER"
            or frozen.get("candidate_target") != 1080
            or len(frozen.get("cases", {})) != 270
            or len(frozen.get("file_sha256", {})) != 44):
        print(json.dumps({"status": "FREEZE_CONTRACT_MISMATCH"}))
        return 3
    freeze_sha = canonical_sha(frozen)
    codex = inspect_codex()
    root, private, discovery = resolve_checkout(freeze_sha)
    checkpoints = inspect_checkpoints(root, private, frozen, freeze_sha) if root else None
    blockers = []
    if codex["login"] != "CHATGPT_ACCOUNT_REPORTED":
        blockers.append("CODEX_LOGIN_NOT_VERIFIED_ON_RUNNER")
    if discovery != "ONE":
        blockers.append("EXACT_LOCAL_CHECKPOINT_NAMESPACE_NOT_UNIQUELY_VISIBLE")
    if checkpoints:
        if checkpoints["invalid_checkpoint_receipts"]:
            blockers.append("LOCAL_CHECKPOINT_INTEGRITY_ERRORS")
        if checkpoints["checkout_source_files_matching_frozen"] != 44:
            blockers.append("FROZEN_SOURCE_NOT_AVAILABLE_IN_LOCAL_CHECKOUT")
        if not checkpoints["checkout_HEAD_has_exact_freeze"]:
            blockers.append("LOCAL_CHECKOUT_HEAD_DOES_NOT_CONTAIN_FREEZE")
        if not checkpoints["checkout_clean_for_frozen_execution"]:
            blockers.append("LOCAL_CHECKOUT_NOT_CLEAN")
        if not checkpoints["pilot_acceptance_bound_to_36_grades"]:
            blockers.append("PILOT_NOT_BOUND_TO_36_VERIFIED_GRADES")
        if checkpoints["candidate_terminal_attempts"] or checkpoints["grader_terminal_attempts"]:
            blockers.append("FROZEN_TERMINAL_ATTEMPTS_NEED_BOUNDARY_REPAIR")
        if checkpoints["supervisor_lock_present"]:
            blockers.append("SUPERVISOR_LOCK_NEEDS_MANUAL_STATE_CHECK")
    result = {
        "scope": "OWNER_AUTHORIZED_READ_ONLY_WINDOWS_PREFLIGHT",
        "no_model_calls": True,
        "no_checkpoint_modifications": True,
        "no_credentials_printed": True,
        "no_paid_api_or_github_hosted_runner": True,
        "codex": codex,
        "checkpoint_discovery": discovery,
        "checkpoints": checkpoints,
        "quota_state": "NOT_QUERIED_NO_MODEL_CALLS",
        "model_identity": "NOT_PROVIDER_ATTESTED",
        "resume_readiness": "PRECHECK_PASS_NO_MODEL_INVOKED" if not blockers else "BLOCKED",
        "blockers": blockers,
        "release": "RELEASE_BLOCKED",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        # Do not print traceback, local paths, auth stderr, model output, or secrets.
        print(json.dumps({"status": "PRECHECK_ERROR", "error_class": type(exc).__name__}))
        sys.exit(2)
