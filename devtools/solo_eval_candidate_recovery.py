"""Additive, single-pair SOLO v2 candidate QUOTA_BLOCKED recovery.

The 44 frozen source files and the original attempt-1 receipt are immutable.
`check` is read-only. `execute-one` may use ONE existing subscription model
call only after separate owner authorization AND safe external execution.
A command-line authorization phrase is not a host-side security boundary.
Neither running this script nor passing its tests authorizes runner execution.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import re
from pathlib import Path

from devtools import cli_eval as e
from devtools import solo_eval as s

FREEZE_REL = "evaluation/v0.0.2/CLI-EVAL-SOLO-FREEZE-v2.json"
TARGET_CASE = "blue-team:edge:05"
TARGET_ARM = "no_handoff"
TARGET_STATUS = "QUOTA_BLOCKED"
ONE_CALL_ACK = "ALLOW_ONE_EXISTING_CHATGPT_SUBSCRIPTION_CANDIDATE_RETRY"
EXPECTED_FREEZE_SHA = "116c8468e98bfed123c7014586c6791114f2d57b596cb8af918192c437d3186b"
EXPECTED_SOURCE_SHA = "f789912bee3b8e50d323244299f3bf4e61969055"


def _target(frozen, base):
    """Derive the exact target from the *original* frozen model and inputs."""
    e.require(e.digest(frozen) == EXPECTED_FREEZE_SHA and
              frozen["source_sha"] == EXPECTED_SOURCE_SHA and
              frozen["environment"]["max_attempts_per_pair"] == 2 and
              frozen["environment"]["model_requested"] == e.MODEL and
              frozen["environment"]["effort_requested"] == e.EFFORT and
              frozen["environment"]["tools"] == "NONE_AUTHORIZED" and
              frozen["environment"]["permissions"] == "read-only",
              "FROZEN_CANDIDATE_CONTRACT_CHANGED")
    e.require((TARGET_CASE, TARGET_ARM) in map(tuple, frozen["full_order"]),
              "TARGET_NOT_IN_FROZEN_ORDER")
    matches = [c for c in e.corpus(e.ROOT) if c["case_id"] == TARGET_CASE]
    e.require(len(matches) == 1 and matches[0]["team_id"] == "blue-team",
              "TARGET_CASE_AMBIGUOUS")
    case = matches[0]
    prompt = e.candidate_input(case)
    material = e.arm_material(e.ROOT, case["team_id"])[TARGET_ARM]
    e.require(e.digest(prompt) == frozen["cases"][TARGET_CASE]["input_sha256"] and
              e.digest(material) == frozen["arm_material_sha256"][case["team_id"]][TARGET_ARM],
              "FROZEN_INPUT_OR_ARM_CHANGED")
    parent = base / "candidates" / e.digest(TARGET_CASE + "|" + TARGET_ARM)[:24]
    first = parent / "1"
    # Reject symlinked evidence components and an existing retry, even broken links.
    e.require(not any(x.is_symlink() for x in (base, base / "candidates", parent, first)),
              "SYMLINK_EVIDENCE_PATH")
    e.require(first.is_dir(), "ORIGINAL_CANDIDATE_ATTEMPT_MISSING")
    return case, prompt, material, parent, first


def _verify_first(frozen, base):
    case, prompt, material, parent, first = _target(frozen, base)
    receipt_path = first / "receipt.json"
    e.require(receipt_path.is_file() and not receipt_path.is_symlink(),
              "FIRST_RECEIPT_MISSING_OR_SYMLINKED")
    receipt = e.load(receipt_path)
    expected = {"case_id": TARGET_CASE, "arm": TARGET_ARM, "attempt": 1,
                "status": TARGET_STATUS, "host": "CLI_TEST",
                "evaluation_mode": "SOLO_DEVELOPER",
                "source_sha": frozen["source_sha"],
                "functional_source_sha": frozen["functional_source_sha"],
                "freeze_sha256": EXPECTED_FREEZE_SHA,
                "environment_digest": frozen["environment_digest"],
                "input_sha256": e.digest(prompt), "arm_sha256": e.digest(material),
                "model_requested": e.MODEL, "effort_requested": e.EFFORT,
                "model_observed": "NOT_EXPOSED_BY_JSONL",
                "model_identity_provenance": "CLI_REQUEST_NOT_PROVIDER_ATTESTED"}
    e.require(all(receipt.get(k) == val for k, val in expected.items()),
              "BLOCKED_CANDIDATE_BINDING_MISMATCH")
    e.validate_observation(receipt)
    for name, field in (("input.json", "input_sha256"),
                        ("stdout.jsonl", "raw_sha256"),
                        ("stderr.txt", "stderr_sha256")):
        path = first / name
        e.require(path.is_file() and not path.is_symlink() and
                  e.digest(path.read_bytes()) == receipt[field],
                  "BLOCKED_CANDIDATE_EVIDENCE_TAMPERED:" + name)
    e.require(not (first / "response.txt").exists(),
              "BLOCKED_CANDIDATE_HAS_RESPONSE")
    return case, prompt, material, parent, first, receipt


def check(freeze_path):
    """Zero-write preflight; requires authentic original private checkpoint."""
    from devtools import solo_eval_resume_batch as resume
    frozen, base, records = resume.validate_frozen(freeze_path)
    case, prompt, material, parent, first, prior = _verify_first(frozen, base)
    completed = {(row["case_id"], row["arm"]) for row in records}
    e.require((TARGET_CASE, TARGET_ARM) not in completed, "TARGET_ALREADY_COMPLETED")
    e.require(not (parent / "2").exists() and not (parent / "2").is_symlink(),
              "CANDIDATE_ATTEMPT_2_ALREADY_EXISTS")
    attempts = sorted((base / "candidates").glob("*/*/receipt.json"))
    e.require(len(attempts) <= 2160, "UNBOUNDED_CANDIDATE_ATTEMPTS")
    quotas = [p for p in attempts if e.load(p).get("status") == TARGET_STATUS]
    e.require(quotas == [first / "receipt.json"], "UNEXPECTED_QUOTA_BLOCKED_PAIR")
    return frozen, base, records, {"case": case, "prompt": prompt,
                                  "material": material, "parent": parent,
                                  "first": first, "receipt": prior}


def plan(freeze_path):
    frozen, base, rows, target = check(freeze_path)
    return {"disposition": "CANDIDATE_ATTEMPT_2_READY_FOR_SEPARATE_AUTHORIZATION",
            "case_id": TARGET_CASE, "arm": TARGET_ARM,
            "existing_completed": len(rows),
            "frozen_source_sha": EXPECTED_SOURCE_SHA,
            "freeze_sha256": EXPECTED_FREEZE_SHA,
            "previous_status": TARGET_STATUS,
            "attempt_1_retained": True, "attempt_2_exists": False,
            "candidate_model_calls": 0, "pending_live_checkpoint_recheck": False,
            "host_authorization_verified": False,
            "runner_execution_authorized": False, "release": "RELEASE_BLOCKED"}


def recovered_for_resume(frozen, case, arm):
    """Only intercept the one /2 recovery; leave frozen solo_eval.py untouched."""
    if (case["case_id"], arm) != (TARGET_CASE, TARGET_ARM):
        return None
    base = s.location(frozen)
    _, _, _, parent, _, _ = _verify_first(frozen, base)
    second = parent / "2"
    if not second.exists() and not second.is_symlink():
        return None
    e.require(second.is_dir() and not second.is_symlink(),
              "RECOVERED_ATTEMPT_PATH_INVALID")
    receipt = e.load(second / "receipt.json")
    e.require(receipt.get("attempt") == 2 and receipt.get("status") == "COMPLETED",
              "RECOVERED_ATTEMPT_NOT_COMPLETED")
    parsed = s.verify_candidate(frozen, second, set(), set())
    e.require(receipt.get("input_sha256") == frozen["cases"][TARGET_CASE]["input_sha256"] and
              receipt.get("arm_sha256") == frozen["arm_material_sha256"]["blue-team"][TARGET_ARM],
              "RECOVERED_CANDIDATE_CHANGED_INPUT")
    return receipt, parsed["response"]



def observed_cli_version(exe):
    """Observe the actual selected Codex executable; never copy a frozen label."""
    try:
        raw = subprocess.check_output([exe, "--version"], env=e.minimal_env(),
                                      timeout=15)
        version = raw.decode("utf-8").strip()
    except (OSError, UnicodeError, subprocess.SubprocessError) as exc:
        raise e.Invalid("CODEX_EXECUTOR_VERSION_UNVERIFIED") from exc
    e.require(re.fullmatch(r"codex-cli [0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.\-]+)?",
                           version) is not None, "CODEX_EXECUTOR_VERSION_INVALID")
    return version


def execute_one(freeze_path, explicit):
    """One externally authorized call. Never call without true owner/host approval."""
    e.require(explicit == ONE_CALL_ACK, "EXPLICIT_CANDIDATE_CALL_APPROVAL_REQUIRED")
    frozen, base, old_rows, target = check(freeze_path)
    exe = e.executable()
    auth = subprocess.run([exe, "login", "status"], capture_output=True,
                          timeout=15, env=e.minimal_env(), check=False)
    e.require(auth.returncode == 0 and b"ChatGPT" in auth.stdout + auth.stderr,
              "CHATGPT_SUBSCRIPTION_LOGIN_REQUIRED")
    actual_cli_version = observed_cli_version(exe)
    lock = base / "supervisor.lock"
    with lock.open("x", encoding="utf-8") as file:
        file.write(e.now())
    try:
        # Recheck original attempt while holding the cooperative supervisor lock.
        _verify_first(frozen, base)
        dest = target["parent"] / "2"
        dest.mkdir(exist_ok=False)
        with (dest / "input.json").open("xb") as file:
            file.write(target["prompt"].encode("utf-8"))
        out, err, code, started, ended, latency, isolated = e.invoke(
            exe, target["prompt"], target["material"],
            frozen["environment"]["timeout_seconds"])
        with (dest / "stdout.jsonl").open("xb") as file:
            file.write(out)
        with (dest / "stderr.txt").open("xb") as file:
            file.write(err)
        record = {"host": "CLI_TEST", "evaluation_mode": "SOLO_DEVELOPER",
                  "case_id": TARGET_CASE, "arm": TARGET_ARM, "attempt": 2,
                  "source_sha": frozen["source_sha"],
                  "functional_source_sha": frozen["functional_source_sha"],
                  "environment_digest": frozen["environment_digest"],
                  "freeze_sha256": EXPECTED_FREEZE_SHA,
                  "input_sha256": e.digest(target["prompt"]),
                  "arm_sha256": e.digest(target["material"]),
                  "raw_sha256": e.digest(out), "stderr_sha256": e.digest(err),
                  "started_at": started, "ended_at": ended,
                  "latency_seconds": latency, "exit_code": code,
                  "cli_version": actual_cli_version,
                  "model_requested": e.MODEL, "effort_requested": e.EFFORT,
                  "model_observed": "NOT_EXPOSED_BY_JSONL",
                  "model_identity_provenance": "CLI_REQUEST_NOT_PROVIDER_ATTESTED",
                  "status": e.failure_kind(e.provider_diagnostics(out, err, code), code),
                  "metrics": e.ungraded(target["case"])}
        if not isolated:
            record["status"] = "INVALID_TRACE"
            record["reason"] = "CANDIDATE_SCRATCH_MUTATION"
        elif code == 0 and record["status"] not in ("QUOTA_BLOCKED", "RATE_LIMIT_BLOCKED"):
            try:
                parsed = e.parse_trace(out, code)
                with (dest / "response.txt").open("x", encoding="utf-8") as file:
                    file.write(parsed["response"])
                record.update({key: value for key, value in parsed.items() if key != "response"})
                record["grading"] = "SOLO_DEVELOPER_UNGRADED"
            except e.Invalid as exc:
                record["status"] = "INVALID_TRACE"
                record["reason"] = str(exc)[:120]
        e.validate_observation(record)
        e.save_new(dest / "receipt.json", record)
        if record["status"] == "COMPLETED":
            s.verify_candidate(frozen, dest, set(), set())
            latest = s.rows(frozen)
            e.require(len(latest) == len(old_rows) + 1 and
                      sum((r["case_id"], r["arm"]) == (TARGET_CASE, TARGET_ARM)
                          for r in latest) == 1,
                      "RECOVERY_NOT_ACCEPTED_BY_FROZEN_LOADER")
        return {"disposition": record["status"], "case_id": TARGET_CASE,
                "arm": TARGET_ARM, "candidate_model_calls": 1,
                "new_append_only_attempt": 2, "original_attempt_retained": True,
                "observed_cli_version": actual_cli_version,
                "frozen_cli_version": frozen["cli_version"],
                "cli_version_changed": actual_cli_version != frozen["cli_version"],
                "comparison_policy": ("CROSS_VERSION_REPORT_SEPARATELY"
                                      if actual_cli_version != frozen["cli_version"]
                                      else "MATCHES_FROZEN_CLI_VERSION"),
                "grade": "NOT_RUN", "release": "RELEASE_BLOCKED"}
    finally:
        lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("check", "execute-one"))
    parser.add_argument("--freeze", type=Path, default=Path(FREEZE_REL))
    parser.add_argument("--one-call-authorization")
    args = parser.parse_args()
    try:
        result = (plan(args.freeze) if args.action == "check" else
                  execute_one(args.freeze, args.one_call_authorization))
        print(json.dumps(result, sort_keys=True))
    except (e.Invalid, ValueError, OSError, KeyError, subprocess.SubprocessError):
        # Keep credentials, private paths, raw model text and prompts out of logs.
        print(json.dumps({"disposition": "CANDIDATE_RECOVERY_BLOCKED",
                          "release": "RELEASE_BLOCKED"}))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
