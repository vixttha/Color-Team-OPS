"""Gate 2 single-target candidate retry -> grader -> read-only receipt audit.

No unattended scheduling or bypass of owner RUNNER TRUST STOP is provided.
This script MUST only be launched by an authenticated, externally protected
owner-authorized executor with access to the authentic original checkpoint.
The acknowledgement argument is NOT itself a runner/host authorization gate.

Default `check` is read-only and makes zero model calls. `execute-once` runs
exactly one candidate retry (attempt 2), then the original frozen semantic
grader (up to its frozen two permitted grader attempts), then re-audits all
candidate and grader receipts and the immutable attempt-1 evidence.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from devtools import cli_eval as e
from devtools import solo_eval as s
from devtools import solo_grader as g
from devtools import solo_eval_candidate_recovery as recovery
from devtools import solo_eval_quality_audit as audit

FREEZE_REL = recovery.FREEZE_REL
EXPECT_COMPLETED = 209
EXPECT_GRADED = 209
TARGET = (recovery.TARGET_CASE, recovery.TARGET_ARM)


def original_hashes(first: Path):
    """Bind the already-verified attempt 1 bytes before any new trial."""
    names = ("input.json", "stdout.jsonl", "stderr.txt", "receipt.json")
    e.require(all((first / name).is_file() and not (first / name).is_symlink()
                  for name in names), "ORIGINAL_ATTEMPT_1_MISSING")
    return {name: e.digest((first / name).read_bytes()) for name in names}


def preflight(freeze_path: Path):
    """Audit original private receipts; no model call, no evidence writes."""
    frozen, base, records, target = recovery.check(freeze_path)
    completed = len(records)
    graded = sum(bool(x.get("grade")) for x in records)
    e.require(completed == EXPECT_COMPLETED and graded == EXPECT_GRADED,
              "HISTORICAL_209_CHECKPOINT_CHANGED")
    status = audit.audit(freeze_path)
    e.require(status["audit_only"] is True and
              status["source_sha"] == recovery.EXPECTED_SOURCE_SHA and
              status["freeze_sha256"] == recovery.EXPECTED_FREEZE_SHA and
              status["verified_completed_candidate_pairs"] == EXPECT_COMPLETED and
              status["verified_graded_pairs"] == EXPECT_GRADED and
              status["pilot_acceptance_present_and_bound"] is True and
              status["supervisor_lock_present"] is False and
              status["candidate_terminal_obstructions"] == [
                  {"case_id": TARGET[0], "arm": TARGET[1], "status": "QUOTA_BLOCKED"}]
              and not status["grader_terminal_obstructions"],
              "LIVE_ORIGINAL_CHECKPOINT_AUDIT_MISMATCH")
    return frozen, base, target, original_hashes(target["first"])


def check_original(first: Path, reference: dict[str, str]):
    e.require(original_hashes(first) == reference,
              "ORIGINAL_ATTEMPT_1_MUTATED")


def execute_once(freeze_path: Path, external_approval: str):
    # Required regardless of other checks; NOT sufficient to authorize the host.
    e.require(external_approval == recovery.ONE_CALL_ACK,
              "SEPARATE_OWNER_ONE_CALL_ACK_REQUIRED")
    frozen, base, target, original = preflight(freeze_path)
    result = recovery.execute_one(freeze_path, external_approval)
    check_original(target["first"], original)
    e.require(result["disposition"] == "COMPLETED" and
              result["candidate_model_calls"] == 1 and
              result["new_append_only_attempt"] == 2,
              "CANDIDATE_RETRY_FAILED_NO_GRADER_CALL")
    case = target["case"]
    retrieved = recovery.recovered_for_resume(frozen, case, recovery.TARGET_ARM)
    e.require(retrieved is not None, "CANDIDATE_ATTEMPT_2_NOT_VERIFIED")
    receipt, response = retrieved
    e.require(receipt["status"] == "COMPLETED" and receipt["attempt"] == 2,
              "CANDIDATE_ATTEMPT_2_NOT_COMPLETED")

    # Check raw receipt count BEFORE adding a grader. Original 209 remain intact.
    before_grade = s.rows(frozen)
    e.require(len(before_grade) == EXPECT_COMPLETED + 1 and
              sum(bool(x.get("grade")) for x in before_grade) == EXPECT_GRADED and
              sum((x["case_id"], x["arm"]) == TARGET for x in before_grade) == 1,
              "NEW_CANDIDATE_NOT_UNIQUELY_BOUND")
    rubric = e.load(e.ROOT / e.EVAL / "reviewer-case-criteria.json")["cases"][TARGET[0]]
    binding = {"source_sha": frozen["source_sha"],
               "freeze_sha256": e.digest(frozen),
               "candidate_raw_sha256": receipt["raw_sha256"],
               "case_id": TARGET[0],
               "rubric_sha256": frozen["cases"][TARGET[0]]["rubric_sha256"]}

    lock = base / "supervisor.lock"
    # Cooperate with original supervisor; do not run a grader if another task
    # has taken the lock. The external executor must also serialize jobs.
    with lock.open("x", encoding="utf-8") as handle:
        handle.write(e.now())
    try:
        grade_receipt, grade = g.grade(
            case, rubric, response, base / "grades" / receipt["raw_sha256"],
            binding, e.executable())
    finally:
        lock.unlink()
    check_original(target["first"], original)
    e.require(grade is not None and grade_receipt["status"] == "GRADED",
              "GRADER_BLOCKED_CHECKPOINT_RETAINED")

    status = audit.audit(freeze_path)
    e.require(status["audit_only"] is True and
              status["verified_completed_candidate_pairs"] == EXPECT_COMPLETED + 1 and
              status["verified_graded_pairs"] == EXPECT_GRADED + 1 and
              status["supervisor_lock_present"] is False and
              status["pilot_acceptance_present_and_bound"] is True and
              not status["grader_terminal_obstructions"] and
              not status["candidate_terminal_obstructions"],
              "POST_RECOVERY_RECEIPT_AUDIT_MISMATCH")
    check_original(target["first"], original)
    quality_stop = bool(grade["critical_violations"] or grade["contradictions"] or
                        grade["uncertainty"] == "HIGH")
    return {"gate": "CTO_V002_GATE_2",
            "disposition": "REQUIRES_SEMANTIC_REVIEW" if quality_stop else
                           "RECOVERED_AND_RECEIPTS_VERIFIED",
            "case_id": TARGET[0], "arm": TARGET[1],
            "original_attempt_1_retained": True,
            "new_candidate_attempt": 2, "candidate_model_calls": 1,
            "grader_attempts_permitted_by_original_freeze": 2,
            "candidate_completed": status["verified_completed_candidate_pairs"],
            "provisional_grades": status["verified_graded_pairs"],
            "all_receipts_reaudited": True,
            "quality_independent": False,
            "release": "RELEASE_BLOCKED"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("check", "execute-once"))
    parser.add_argument("--freeze", type=Path, default=Path(FREEZE_REL))
    parser.add_argument("--one-call-authorization")
    args = parser.parse_args()
    try:
        if args.action == "check":
            f, base, target, original = preflight(args.freeze)
            output = {"disposition": "LIVE_ORIGINAL_CHECKPOINT_READ_ONLY_PASS",
                      "candidate_model_calls": 0,
                      "completed": EXPECT_COMPLETED, "graded": EXPECT_GRADED,
                      "target": TARGET[0], "arm": TARGET[1],
                      "host_trust_verified": False,
                      "release": "RELEASE_BLOCKED"}
        else:
            output = execute_once(args.freeze, args.one_call_authorization)
        print(json.dumps(output, sort_keys=True))
    except (e.Invalid, ValueError, OSError, KeyError) as exc:
        # Fail closed, no raw text or credentials in logs.
        print(json.dumps({"disposition": "GATE_2_EXECUTION_BLOCKED",
                          "error_class": type(exc).__name__,
                          "release": "RELEASE_BLOCKED"}))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
