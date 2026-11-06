"""Read-only terminal checkpoint + semantic-grade audit for frozen SOLO v2.

This audit never calls a model, accesses live ChatGPT sessions, writes checkpoints
or copies raw prompts/responses. It must be scheduled in the SAME Actions
concurrency group as the original model run, so it does not race its writer.
"""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import sys

from v002_windows_codex_preflight import canonical_sha, file_sha, resolve_checkout, FROZEN_REL

FROZEN_DIGEST = "116c8468e98bfed123c7014586c6791114f2d57b596cb8af918192c437d3186b"
FROZEN_SOURCE = "f789912bee3b8e50d323244299f3bf4e61969055"
ARMS = frozenset(("generic", "full", "no_directory", "no_handoff"))


def audited():
    if (os.name != "nt"
        or os.environ.get("GITHUB_ACTIONS") != "true"
        or os.environ.get("GITHUB_REF") != "refs/heads/feature/v0.0.2-codex-independent-eval"):
        print(json.dumps({"audit_status": "UNAUTHORIZED_RUNNER_CONTEXT"}), flush=True)
        return 2
    workspace = Path(os.environ["GITHUB_WORKSPACE"])
    frozen = json.loads((workspace / FROZEN_REL).read_text(encoding="utf-8"))
    if (canonical_sha(frozen) != FROZEN_DIGEST
        or frozen.get("source_sha") != FROZEN_SOURCE
        or frozen.get("evaluation_mode") != "SOLO_DEVELOPER"
        or frozen.get("candidate_target") != 1080
        or len(frozen.get("full_order", [])) != 1080):
        print(json.dumps({"audit_status": "FROZEN_EVALUATION_MISMATCH"}), flush=True)
        return 2
    root, private, state = resolve_checkout(FROZEN_DIGEST)
    if state != "ONE" or root is None:
        print(json.dumps({"audit_status": "ORIGINAL_EVIDENCE_NOT_UNIQUE"}), flush=True)
        return 2
    if (private / "supervisor.lock").exists():
        print(json.dumps({"audit_status": "SUPERVISOR_LOCK_STILL_PRESENT_NO_UNSAFE_READ"}), flush=True)
        return 2
    match = sum(
        (root / rel).is_file() and file_sha(root / rel) == digest
        for rel, digest in frozen["file_sha256"].items()
    )
    if match != len(frozen["file_sha256"]) or match != 44:
        print(json.dumps({"audit_status": "ORIGINAL_FROZEN_SOURCE_NOT_44_OF_44"}), flush=True)
        return 2
    os.environ["GIT_OPTIONAL_LOCKS"] = "0"
    os.environ["GIT_TERMINAL_PROMPT"] = "0"
    os.chdir(root)
    sys.path.insert(0, str(root))
    file = workspace / "devtools" / "solo_eval_quality_audit.py"
    spec = importlib.util.spec_from_file_location("v002_terminal_quality_audit", file)
    if spec is None or spec.loader is None:
        print(json.dumps({"audit_status": "QUALITY_AUDITOR_UNAVAILABLE"}), flush=True)
        return 2
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    report = module.audit(root / FROZEN_REL)
    cand = report["verified_completed_candidate_pairs"]
    graded = report["verified_graded_pairs"]
    candidate_stats = report["candidate_attempts_by_status"]
    grader_stats = report["grader_attempts_by_status"]
    per_arm = report["accuracy_derived_with_exclusions"]
    valid = (
        report.get("audit_only") is True
        and report.get("source_sha") == FROZEN_SOURCE
        and report.get("freeze_sha256") == FROZEN_DIGEST
        and report.get("pilot_acceptance_present_and_bound") is True
        and report.get("supervisor_lock_present") is False
        and set(per_arm) == ARMS
        and len(report["excluded_from_task_accuracy"]) == 3
        and report.get("holdouts") == "54_NONBLIND_REGRESSION_ONLY"
        and 36 <= graded <= cand <= 1080
        and candidate_stats.get("COMPLETED") == cand
        and grader_stats.get("GRADED") == graded
        and report.get("release") == "RELEASE_BLOCKED"
    )
    summary = {
        "audit_status": "VERIFIED" if valid else "SOURCE_OR_COUNT_MISMATCH",
        "candidate_pairs": cand,
        "graded_pairs": graded,
        "candidate_remaining": 1080 - cand,
        "grading_remaining": 1080 - graded,
        "saved_candidates_awaiting_grade": cand - graded,
        "candidate_attempts_by_status": candidate_stats,
        "grader_attempts_by_status": grader_stats,
        "security_critical_pairs": report["critical_pairs_all_graded"],
        "contradiction_pairs": report["contradictions_all_graded"],
        "frozen_source_file_hashes_verified": match,
        "grading_accuracy_exclusions": report["excluded_from_task_accuracy"],
        "per_arm_provisional_accuracy": per_arm,
        "pilot_receipts_bound": report["pilot_acceptance_present_and_bound"],
        "original_evidence_mutated": False,
        "resume_blockers": report["resume_blockers"],
        "terminal_obstructions": {
            "candidate": report["candidate_terminal_obstructions"],
            "grader": report["grader_terminal_obstructions"],
        },
        "matrix_complete": cand == graded == 1080,
        "quality_approval": "PENDING_SELF_REVIEW_AND_SECURITY_FINDINGS" if cand == graded == 1080 else "NOT_COMPLETE",
        "host_H_01_to_H_11": "NOT_RUN",
        "host_smoke_A_B": "NOT_RUN",
        "model_calls": 0,
        "holdouts": "54_NONBLIND_REGRESSION_ONLY",
        "classification": "SOLO_DEVELOPER_SELF_REVIEWED_AI_ASSISTED_PROVISIONAL",
        "release": "RELEASE_BLOCKED",
    }
    print(json.dumps(summary, sort_keys=True), flush=True)
    return 0 if valid else 2


if __name__ == "__main__":
    try:
        sys.exit(audited())
    except Exception:
        # No stack traces, raw prompt text, credentials or local paths in CI logs.
        print(json.dumps({"audit_status": "CHECKPOINT_AUDIT_FAILED_CLOSED",
                          "model_calls": 0, "release": "RELEASE_BLOCKED"}), flush=True)
        sys.exit(2)
