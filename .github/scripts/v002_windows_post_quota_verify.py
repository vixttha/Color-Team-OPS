"""Post-recovery read-only validation from original local Codex evidence.

Reads frozen package with Git/integrity checks; never calls a model.
No raw prompts, credentials, local paths or responses are printed.
"""
from __future__ import annotations
import importlib.util
import json
import os
from pathlib import Path
import sys

from v002_windows_codex_preflight import canonical_sha, resolve_checkout, FROZEN_REL


def main():
    if os.name != "nt" or os.environ.get("GITHUB_ACTIONS") != "true":
        print(json.dumps({"status": "NOT_SELF_HOSTED_WINDOWS_CONTEXT"}))
        return 2
    workspace = Path(os.environ["GITHUB_WORKSPACE"])
    f = json.loads((workspace / FROZEN_REL).read_text(encoding="utf-8"))
    root, private, state = resolve_checkout(canonical_sha(f))
    if state != "ONE" or root is None:
        print(json.dumps({"status": "FROZEN_LOCAL_EVIDENCE_MISSING_OR_MULTIPLE"}))
        return 2
    os.environ["GIT_OPTIONAL_LOCKS"] = "0"
    os.environ["GIT_TERMINAL_PROMPT"] = "0"
    os.chdir(root)
    sys.path.insert(0, str(root))
    audit_file = workspace / "devtools" / "solo_eval_quality_audit.py"
    spec = importlib.util.spec_from_file_location("v002_read_only_post_quota_audit", audit_file)
    if spec is None or spec.loader is None:
        print(json.dumps({"status": "AUDITOR_UNAVAILABLE"}))
        return 2
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    report = module.audit(root / FROZEN_REL)
    candidate = report["candidate_attempts_by_status"].get("COMPLETED", 0)
    graders = report["grader_attempts_by_status"]
    passed = (
        report["verified_completed_candidate_pairs"] == 72
        and report["verified_graded_pairs"] == 70
        and candidate == 72
        and graders.get("GRADED") == 70
        and graders.get("QUOTA_BLOCKED") == 1
        and report["resume_blockers"] == []
        and report["source_sha"] == f["source_sha"]
        and report["freeze_sha256"] == canonical_sha(f)
        and report["release"] == "RELEASE_BLOCKED"
    )
    print(json.dumps({
        "status": "PASS" if passed else "VALIDATION_BLOCKED",
        "candidate_pairs_verified": report["verified_completed_candidate_pairs"],
        "graded_pairs_verified": report["verified_graded_pairs"],
        "original_quota_attempt_retained": graders.get("QUOTA_BLOCKED", 0) == 1,
        "grader_attempts_total": report["grader_invocations"] if "grader_invocations" in report
                                 else sum(graders.values()),
        "recovery_accepted_by_original_frozen_loader": passed,
        "remaining_ungraded_candidates": candidate - report["verified_graded_pairs"],
        "read_only": True,
        "additional_model_calls": 0,
        "resume_blockers": report["resume_blockers"],
        "release": "RELEASE_BLOCKED",
    }, sort_keys=True))
    return 0 if passed else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, KeyError, TypeError, ValueError):
        print(json.dumps({"status": "POST_RECOVERY_VALIDATION_FAILED"}))
        sys.exit(2)
