"""Append-only v2 solo-grader quota recovery. NOT part of the frozen grader.

Default mode is read-only. One optional explicitly approved model call can
create attempt 2 AFTER a fully verified QUOTA_BLOCKED attempt 1. No source,
rubric, model, grading prompt, raw historical evidence or stage boundary changes.
The existing frozen evaluator recognizes a successful attempt-2 grade via
solo_eval.rows() and will subsequently skip the pair. Results remain provisional.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import json
import subprocess

from devtools import cli_eval as e
from devtools import solo_eval as s
from devtools import solo_grader as g


FREEZE_REL = "evaluation/v0.0.2/CLI-EVAL-SOLO-FREEZE-v2.json"
TARGET_STATUS = "QUOTA_BLOCKED"


def check(freeze_path):
    frozen = e.validate_freeze(freeze_path)
    e.require(frozen.get("evaluation_mode") == "SOLO_DEVELOPER" and
              frozen.get("solo_revision") == "solo-eval-v1" and
              frozen.get("candidate_target") == 1080 and
              frozen.get("pilot_target") == 36 and
              frozen.get("grader") == g.configuration() and
              frozen["grader"]["max_attempts"] == 2,
              "FROZEN_V2_GRADER_CONFIGURATION_MISMATCH")
    base = s.location(frozen)
    e.require(base.is_dir(), "LOCAL_EVIDENCE_NAMESPACE_NOT_FOUND")
    e.require(not (base / "supervisor.lock").exists(), "SUPERVISOR_ALREADY_ACTIVE")
    records = s.rows(frozen)
    e.require(len({(r["case_id"], r["arm"]) for r in records}) == len(records),
              "DUPLICATE_COMPLETED_PAIR")
    cases = {x["case_id"]: x for x in e.corpus(e.ROOT)}
    rubrics = e.load(e.ROOT / e.EVAL / "reviewer-case-criteria.json")["cases"]
    potential = []
    all_receipts = list(base.glob("grades/*/*/receipt.json"))
    e.require(len(all_receipts) <= 2160, "UNBOUNDED_GRADE_RECEIPTS")
    for path in all_receipts:
        saved = e.load(path)
        if saved.get("status") != TARGET_STATUS:
            continue
        raw_id = path.parent.parent.name
        linked = [r for r in records if r["receipt"]["raw_sha256"] == raw_id]
        e.require(len(linked) == 1, "AMBIGUOUS_BLOCKED_GRADE_CANDIDATE")
        r = linked[0]
        case = cases[r["case_id"]]
        rubric = rubrics[r["case_id"]]
        e.require(not r.get("grade"), "CANNOT_RETRY_ALREADY_GRADED_PAIR")
        e.require(path.parent.name == "1", "QUOTA_FAILURE_NOT_FIRST_ATTEMPT")
        directory = path.parent.parent
        # Validate native frozen raw candidate trace and its response text:
        candidate = s.location(frozen) / "candidates" / e.digest(
            r["case_id"] + "|" + r["arm"])[:24]
        trial = candidate / str(r["receipt"]["attempt"])
        parsed = s.verify_candidate(frozen, trial, set(), set())
        response = parsed["response"]
        prompt = e.encode(g.grade_input(case, rubric, response))
        native_schema = g.response_schema(response)
        binding = {
            "source_sha": frozen["source_sha"],
            "freeze_sha256": e.digest(frozen),
            "candidate_raw_sha256": raw_id,
            "case_id": r["case_id"],
            "rubric_sha256": frozen["cases"][r["case_id"]]["rubric_sha256"],
        }
        e.require(
            saved.get("kind") == "AI_GRADER" and
            saved.get("attempt") == 1 and
            saved.get("independent") is False and
            saved.get("configuration_sha256") == e.digest(g.configuration()) and
            saved.get("input_sha256") == e.digest(prompt) and
            saved.get("response_sha256") == e.digest(response) and
            saved.get("native_schema_sha256") == e.digest(native_schema) and
            saved.get("rubric_sha256") == e.digest(rubric) and
            saved.get("binding") == binding and
            e.digest((path.parent / "stdout.jsonl").read_bytes()) == saved.get("raw_sha256") and
            e.digest((path.parent / "stderr.txt").read_bytes()) == saved.get("stderr_sha256") and
            e.digest((path.parent / "input.json").read_bytes()) == saved.get("input_sha256"),
            "BLOCKED_GRADE_RECEIPT_INTEGRITY_FAILURE")
        next_dir = directory / "2"
        e.require(not next_dir.exists(), "GRADE_ATTEMPT_2_ALREADY_EXISTS")
        potential.append({
            "case_id": r["case_id"],
            "arm": r["arm"],
            "directory": directory,
            "response": response,
            "rubric": rubric,
            "case": case,
            "prompt": prompt,
            "schema": native_schema,
            "binding": binding,
        })
    e.require(len(potential) == 1, "EXPECTED_EXACTLY_ONE_QUOTA_BLOCKED_GRADER_PAIR")
    return frozen, records, potential[0]


def plan(freeze_path):
    frozen, records, target = check(freeze_path)
    return {
        "disposition": "EXACT_APPEND_ONLY_ATTEMPT_2_AVAILABLE",
        "new_model_calls": 0,
        "case_id": target["case_id"],
        "arm": target["arm"],
        "candidate_completed": len(records),
        "graded": sum(bool(x.get("grade")) for x in records),
        "source_sha": frozen["source_sha"],
        "freeze_sha256": e.digest(frozen),
        "frozen_grader_configuration_sha256": e.digest(g.configuration()),
        "retained_attempt_1": TARGET_STATUS,
        "safe_to_call_after_quota_refresh": "UNKNOWN_NOT_QUERIED",
        "remaining_frozen_attempts_for_target": 1,
        "candidate_reexecution": False,
        "prior_checkpoint_mutation": False,
        "release": "RELEASE_BLOCKED",
    }


def execute_one(freeze_path, explicit):
    e.require(explicit == "ALLOW_ONE_EXISTING_CHATGPT_SUBSCRIPTION_GRADER_CALL",
              "EXPLICIT_ONE_CALL_AUTHORIZATION_REQUIRED")
    frozen, records, target = check(freeze_path)
    exe = e.executable()
    auth = subprocess.run([exe, "login", "status"], capture_output=True,
                          timeout=15, env=e.minimal_env(), check=False)
    e.require(auth.returncode == 0 and b"ChatGPT" in auth.stdout + auth.stderr,
              "CHATGPT_SUBSCRIPTION_LOGIN_REQUIRED")
    # Never overwrite a prior attempt; 2 is the *last* frozen attempt slot.
    dest = target["directory"] / "2"
    dest.mkdir(exist_ok=False)
    prompt = target["prompt"]
    # Reuse *the same frozen grader instruction material, native schema,
    # model, effort, sandbox and tool/credential boundaries*.
    with (dest / "input.json").open("xb") as f:
        f.write(prompt)
    out, err, code, started, ended, latency, isolated = e.invoke(
        exe, prompt.decode("utf-8"), g.INSTRUCTIONS,
        g.configuration()["timeout_seconds"], response_schema=target["schema"])
    with (dest / "stdout.jsonl").open("xb") as f:
        f.write(out)
    with (dest / "stderr.txt").open("xb") as f:
        f.write(err)
    record = {
        "kind": "AI_GRADER",
        "classification": g.configuration()["classification"],
        "independent": False,
        "configuration_sha256": e.digest(g.configuration()),
        "input_sha256": e.digest(prompt),
        "response_sha256": e.digest(target["response"]),
        "native_schema_sha256": e.digest(target["schema"]),
        "rubric_sha256": e.digest(target["rubric"]),
        "binding": target["binding"],
        "raw_sha256": e.digest(out),
        "stderr_sha256": e.digest(err),
        "attempt": 2,
        "started_at": started,
        "ended_at": ended,
        "latency_seconds": latency,
        "exit_code": code,
        "model_requested": e.MODEL,
        "effort_requested": e.EFFORT,
        "model_observed": "NOT_EXPOSED_BY_JSONL",
        "status": e.failure_kind(e.provider_diagnostics(out, err, code), code),
    }
    grade = None
    if not isolated:
        record["status"] = "INVALID_TRACE"
        record["reason"] = "GRADER_SCRATCH_MUTATION"
    elif code == 0 and record["status"] not in ("QUOTA_BLOCKED", "RATE_LIMIT_BLOCKED"):
        try:
            parsed = e.parse_trace(out, code)
            record.update({key: parsed[key] for key in ("session_sha256", "usage", "tool_events")})
            with (dest / "response.txt").open("x", encoding="utf-8") as f:
                f.write(parsed["response"])
            grade = json.loads(parsed["response"])
            from jsonschema import Draft202012Validator
            Draft202012Validator(target["schema"]).validate(grade)
            g.validate_grade(grade, target["response"], target["rubric"])
            record["grade_sha256"] = e.digest(grade)
            record["status"] = "GRADED"
            e.save_new(dest / "grade.json", grade)
        except (ValueError, KeyError, TypeError) as exc:
            record["status"] = "INVALID_GRADE"
            record["reason"] = str(exc)[:200]
        except Exception as exc:
            from jsonschema import ValidationError
            if not isinstance(exc, ValidationError):
                raise
            record["status"] = "INVALID_GRADE"
            record["reason"] = "GRADE_SCHEMA_VALIDATION"
    e.save_new(dest / "receipt.json", record)
    if grade is not None:
        # Real frozen v2 loader sees only the valid /2 grade, preserving
        # the original /1 quota receipt and its raw evidence.
        validated = s.rows(frozen)
        e.require(sum(bool(r.get("grade")) for r in validated)
                  == sum(bool(r.get("grade")) for r in records) + 1,
                  "RECOVERED_GRADE_NOT_ACCEPTED_BY_FROZEN_LOADER")
    return {
        "disposition": record["status"],
        "case_id": target["case_id"],
        "arm": target["arm"],
        "new_model_calls": 1,
        "historical_attempt_1_retained": True,
        "new_append_only_attempt": 2,
        "release": "RELEASE_BLOCKED",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=("check", "execute-one"))
    p.add_argument("--freeze", type=Path, default=Path(FREEZE_REL))
    p.add_argument("--one-call-authorization")
    a = p.parse_args()
    try:
        if a.action == "check":
            result = plan(a.freeze)
        else:
            result = execute_one(a.freeze, a.one_call_authorization)
        print(json.dumps(result, sort_keys=True))
    except (e.Invalid, OSError, ValueError, KeyError) as exc:
        # Do not print errors with receipt or token contents.
        print(json.dumps({"disposition": "REPAIR_BLOCKED", "reason_code": type(exc).__name__}))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
