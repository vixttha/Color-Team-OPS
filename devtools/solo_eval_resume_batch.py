"""Resume the immutable SOLO_DEVELOPER v2 model matrix, preserving checkpoints.

Additive supervisor, not included in the frozen 44 source files. Prioritize
already-completed ungraded candidate pairs; then follow the existing full_order.
No new freeze, rerun of successful candidates, host/staging actions, paid API
fallback, changed prompts, models or grader policy.

One active supervisor.lock; stop on quota, invalid evidence, material security
finding or time budget; always retain raw original receipts and re-audit.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import subprocess
import time
from pathlib import Path

from devtools import cli_eval as e
from devtools import solo_eval as s
from devtools import solo_grader as g
from devtools import solo_eval_candidate_recovery as candidate_recovery

EXPECTED_FREEZE_SHA = "116c8468e98bfed123c7014586c6791114f2d57b596cb8af918192c437d3186b"
EXPECTED_SOURCE_SHA = "f789912bee3b8e50d323244299f3bf4e61969055"
BOUNDARY_SECONDS = 420
MAX_RUNTIME_SECONDS = 17000


def queue_for_full(frozen, existing):
    """Resume order: candidate responses in hand first, then new candidate calls."""
    requested = [tuple(pair) for pair in frozen["full_order"]]
    e.require(len(requested) == 1080 and len(set(requested)) == 1080, "FULL_ORDER_INTEGRITY")
    all_pairs = {(r["case_id"], r["arm"]) for r in existing}
    completed = {(r["case_id"], r["arm"]) for r in existing if r.get("grade")}
    e.require(all_pairs <= set(requested), "UNKNOWN_COMPLETED_PAIR")
    return [pair for pair in requested if pair in all_pairs and pair not in completed], [
        pair for pair in requested if pair not in all_pairs
    ]


def validate_frozen(freeze_path):
    frozen = e.validate_freeze(freeze_path)
    e.require(
        frozen.get("evaluation_mode") == "SOLO_DEVELOPER"
        and frozen.get("solo_revision") == "solo-eval-v1"
        and frozen.get("candidate_target") == 1080
        and frozen.get("pilot_target") == 36
        and frozen.get("grader") == g.configuration()
        and e.digest(frozen) == EXPECTED_FREEZE_SHA
        and frozen.get("source_sha") == EXPECTED_SOURCE_SHA,
        "FROZEN_V2_SOURCE_OR_MODEL_POLICY_MISMATCH",
    )
    base = s.location(frozen)
    e.require(base.is_dir(), "ORIGINAL_LOCAL_EVIDENCE_NOT_FOUND")
    accepted = e.load(base / "pilot-acceptance.json")
    e.require(accepted.get("freeze_sha256") == EXPECTED_FREEZE_SHA, "PILOT_FREEZE_MISMATCH")
    s.quality_gate(accepted["summary"])
    rows = s.rows(frozen)
    pilot = {tuple(pair) for pair in frozen["pilot_order"]}
    graded = {(r["case_id"], r["arm"]) for r in rows if r.get("grade")}
    e.require(len(pilot) == 36 and pilot <= graded, "PILOT_RAW_GRADE_BINDING_INCOMPLETE")
    e.require(not (base / "supervisor.lock").exists(), "SUPERVISOR_LOCK_ALREADY_PRESENT")
    return frozen, base, rows


def status_snapshot(frozen):
    status = s.summary(frozen)
    return {
        "candidate_completed": status["candidate_completed"],
        "graded": status["graded"],
        "ungraded": status["ungraded"],
        "critical_pairs": status["critical_pairs"],
        "contradiction_pairs": status["contradiction_pairs"],
        "high_uncertainty": status["high_uncertainty"],
        "candidate_attempts": status["candidate_attempts"],
        "grader_invocations": status["grader_invocations"],
        "candidate_outcomes": status["candidate_outcomes"],
        "grader_outcomes": status["grader_outcomes"],
    }


def run(freeze_path: Path, max_new_pairs: int, runtime_seconds: int):
    e.require(1 <= max_new_pairs <= 1008, "BAD_NEW_PAIR_LIMIT")
    e.require(900 <= runtime_seconds <= MAX_RUNTIME_SECONDS, "BAD_RUNTIME_BUDGET")
    frozen, base, existing = validate_frozen(freeze_path)
    before = status_snapshot(frozen)
    e.require(before["critical_pairs"] == 0 and before["contradiction_pairs"] == 0
              and before["high_uncertainty"] == 0, "EXISTING_UNREVIEWED_CRITICAL_GRADE")
    pending, fresh = queue_for_full(frozen, existing)
    exe = e.executable()
    auth = subprocess.run([exe, "login", "status"], capture_output=True, timeout=15,
                          env=e.minimal_env(), check=False)
    e.require(auth.returncode == 0 and b"ChatGPT" in auth.stdout + auth.stderr,
              "CHATGPT_SUBSCRIPTION_NOT_AUTHENTICATED")
    cases = {x["case_id"]: x for x in e.corpus(e.ROOT)}
    rubrics = e.load(e.ROOT / e.EVAL / "reviewer-case-criteria.json")["cases"]
    lock = base / "supervisor.lock"
    started = time.monotonic()
    finished_saved = 0
    new_pairs = 0
    disposition = "BATCH_LIMIT_REACHED"
    blocked_detail = None
    e.require(not (base / "supervisor.lock").exists(), "SUPERVISOR_LOCK_ALREADY_PRESENT")
    with lock.open("x", encoding="utf-8") as handle:
        handle.write(e.now())
    try:
        for cid, arm in [*pending, *fresh]:
            existing_candidate = (cid, arm) in {(r["case_id"], r["arm"]) for r in existing}
            if not existing_candidate and new_pairs >= max_new_pairs:
                break
            # Always leave sufficient time for BOTH possible isolated frozen
            # model subprocesses and checkpoint flush before GitHub job timeout.
            if time.monotonic() - started + BOUNDARY_SECONDS >= runtime_seconds:
                disposition = "TIME_BUDGET_STOP"
                break
            case = cases[cid]
            # The frozen solo_eval.candidate() stops at an existing QUOTA_BLOCKED
            # attempt 1. Read only the exact verified append-only candidate /2
            # if one exists; never modify the 44 frozen evaluator/source files.
            recovered = candidate_recovery.recovered_for_resume(frozen, case, arm)
            receipt, response = (recovered if recovered is not None else
                                 s.candidate(frozen, case, arm, exe))
            if receipt["status"] != "COMPLETED":
                disposition = "CANDIDATE_" + receipt["status"]
                blocked_detail = "CANDIDATE_STOP"
                break
            if not existing_candidate:
                new_pairs += 1
            binding = {
                "source_sha": frozen["source_sha"],
                "freeze_sha256": e.digest(frozen),
                "candidate_raw_sha256": receipt["raw_sha256"],
                "case_id": cid,
                "rubric_sha256": frozen["cases"][cid]["rubric_sha256"],
            }
            grader_receipt, result = g.grade(
                case, rubrics[cid], response,
                base / "grades" / receipt["raw_sha256"],
                binding, exe,
            )
            if result is None:
                disposition = "GRADER_" + grader_receipt["status"]
                blocked_detail = "GRADING_STOP"
                break
            if existing_candidate:
                finished_saved += 1
            if result["critical_violations"] or result["contradictions"] or result["uncertainty"] == "HIGH":
                disposition = "CRITICAL_OR_UNCERTAIN_GRADE_REQUIRES_REVIEW"
                blocked_detail = "QUALITY_STOP"
                break
            if (new_pairs + finished_saved) % 6 == 0:
                print(json.dumps({"event": "BOUNDED_PROGRESS",
                                  "saved_responses_graded": finished_saved,
                                  "fresh_candidates_graded": new_pairs}, sort_keys=True), flush=True)
        else:
            disposition = "ALL_FROZEN_PAIRS_EXAMINED"
    finally:
        lock.unlink()
    after = status_snapshot(frozen)
    e.require(after["candidate_completed"] >= before["candidate_completed"]
              and after["graded"] >= before["graded"], "COMPLETION_COUNTS_REGRESSED")
    e.require(after["candidate_completed"] <= 1080 and after["graded"] <= 1080,
              "COUNTS_EXCEED_FROZEN_MATRIX")
    if after["candidate_completed"] == after["graded"] == 1080:
        disposition = "MATRIX_COMPLETE_REQUIRES_QUALITY_REVIEW"
    report = {
        "status": disposition,
        "freeze_sha256": EXPECTED_FREEZE_SHA,
        "frozen_source_sha": EXPECTED_SOURCE_SHA,
        "before": before,
        "after": after,
        "saved_responses_graded_this_run": finished_saved,
        "fresh_candidates_completed_this_run": new_pairs,
        "no_paid_api": True,
        "no_host_or_staging_actions": True,
        "no_historical_evidence_rewrites": True,
        "holdouts": "54_NONBLIND_REGRESSION_ONLY",
        "model_identity": "REQUEST_ONLY_NOT_PROVIDER_ATTESTED",
        "release": "RELEASE_BLOCKED",
        "blocked_detail": blocked_detail,
    }
    e.save_new(base / ("bounded-full-resume-" +
                       datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") +
                       ".json"), report)
    print(json.dumps(report, sort_keys=True), flush=True)
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--freeze", type=Path, required=True)
    p.add_argument("--max-new-pairs", type=int, default=1008)
    p.add_argument("--runtime-seconds", type=int, default=MAX_RUNTIME_SECONDS)
    args = p.parse_args()
    try:
        run(args.freeze, args.max_new_pairs, args.runtime_seconds)
    except (e.Invalid, ValueError, OSError, KeyError, subprocess.SubprocessError) as exc:
        # Do not expose credentials, local paths, user data, raw JSONL,
        # Codex authentication diagnostics, or model response material.
        print(json.dumps({"status": "RESUME_BLOCKED",
                          "error_class": type(exc).__name__,
                          "release": "RELEASE_BLOCKED"}), flush=True)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
