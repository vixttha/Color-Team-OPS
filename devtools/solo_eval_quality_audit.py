"""Read-only, source-bound quality and checkpoint audit for SOLO freeze v2.

This is NOT the frozen evaluator, a model invocation, or a scoring oracle.
It preserves original grades and records exclusions only in derived accuracy.
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import json

from devtools import cli_eval as e
from devtools import solo_eval as s

PILOT_AUDIT = e.ROOT / e.EVAL / "CLI-EVAL-SOLO-PILOT-AUDIT-v2.json"
REQUIRED_EXCLUSIONS = {
    ("black-team:normal:01", "task_correctness"),
    ("red-team:normal:01", "task_correctness"),
    ("yellow-team:normal:01", "task_correctness"),
}
TERMINAL_ATTEMPTS = {"QUOTA_BLOCKED", "RATE_LIMIT_BLOCKED", "TIMEOUT", "INVALID_TRACE"}
GRADE_TERMINAL = TERMINAL_ATTEMPTS | {"INVALID_GRADE"}


def verified_exclusions(pilot_audit, freeze):
    """Accept ONLY the already documented three v2 accuracy exclusions."""
    e.require(pilot_audit.get("freeze_sha256") == e.digest(freeze),
              "PILOT_AUDIT_FREEZE_MISMATCH")
    values = pilot_audit.get("accuracy_exclusions", [])
    actual = [(x.get("case_id"), x.get("metric")) for x in values]
    e.require(len(actual) == len(REQUIRED_EXCLUSIONS) and set(actual) == REQUIRED_EXCLUSIONS,
              "UNEXPECTED_ACCURACY_EXCLUSIONS")
    return {cid for cid, metric in actual if metric == "task_correctness"}


def accuracy_after_exclusions(rows, excluded_ids):
    """Provisional, paired, case-bound quality statistics; never host accuracy."""
    e.require(len({(r["case_id"], r["arm"]) for r in rows}) == len(rows),
              "DUPLICATE_GRADED_PAIR")
    known = set(e.ARMS)
    e.require(all(r["arm"] in known for r in rows), "UNKNOWN_EVAL_ARM")
    scores = {(r["case_id"], r["arm"]): r["grade"]["metrics"]["task_correctness"]["status"]
              for r in rows if r.get("grade") is not None
              and r["case_id"] not in excluded_ids
              and r["grade"]["metrics"]["task_correctness"]["status"] != "NOT_OBSERVABLE"}
    baseline = {cid: state for (cid, arm), state in scores.items() if arm == "generic"}
    result = {}
    for arm in e.ARMS:
        items = {cid: state for (cid, a), state in scores.items() if a == arm}
        counts = Counter(items.values())
        pairs = sorted(set(items) & set(baseline))
        n = len(items)
        result[arm] = {
            "graded_denominator": n,
            "states": dict(counts),
            "strict_correctness": counts["PASS"] / n if n else None,
            "wilson95": e.wilson(counts["PASS"], n),
            "paired_n": len(pairs),
            "paired_delta": (sum(int(items[cid] == "PASS") -
                                 int(baseline[cid] == "PASS") for cid in pairs) /
                             len(pairs)) if pairs else None,
        }
    return result


def receipt_integrity(path, kind):
    """Verify all available attempts, including non-completed receipts."""
    r = e.load(path)
    if kind == "candidate":
        e.validate_observation(r)
    for filename, key in (("stdout.jsonl", "raw_sha256"), ("stderr.txt", "stderr_sha256")):
        e.require(path.parent.joinpath(filename).is_file(), "MISSING_" + filename.upper())
        e.require(e.digest(path.parent.joinpath(filename).read_bytes()) == r.get(key),
                  "CHECKPOINT_HASH_MISMATCH:" + key)
    if kind == "candidate":
        e.require(path.parent.joinpath("input.json").is_file(), "MISSING_INPUT")
        e.require(e.digest(path.parent.joinpath("input.json").read_text(encoding="utf-8"))
                  == r["input_sha256"], "CANDIDATE_INPUT_HASH_MISMATCH")
    return r


def local_checkpoint_status(freeze, records, candidate_attempts, grader_attempts, base):
    completed = {(r["case_id"], r["arm"]) for r in records if r.get("grade")}
    candidate_obstructions = sorted({
        (r["case_id"], r["arm"], r["status"]) for r in candidate_attempts
        if r["status"] in TERMINAL_ATTEMPTS
        and (r["case_id"], r["arm"]) not in completed
    })
    grader_obstructions = sorted({
        (r["binding"]["case_id"], r["status"]) for r in grader_attempts
        if r["status"] in GRADE_TERMINAL
        and not any(z.get("grade") and z["receipt"]["raw_sha256"] == r.get("binding", {}).get("candidate_raw_sha256")
                    for z in records)
    })
    lock = (base / "supervisor.lock").exists()
    pilot_path = base / "pilot-acceptance.json"
    pilot_valid = False
    if pilot_path.is_file():
        audit = e.load(pilot_path)
        e.require(audit.get("freeze_sha256") == e.digest(freeze),
                  "PILOT_ACCEPTANCE_FREEZE_MISMATCH")
        s.quality_gate(audit["summary"])
        pilot_valid = True
    blockers = []
    if lock:
        blockers.append("ACTIVE_OR_STALE_SUPERVISOR_LOCK_REQUIRE_OWNER_INSPECTION")
    if candidate_obstructions:
        blockers.append("FROZEN_RUNNER_CANNOT_RESUME_TERMINAL_CANDIDATE_CHECKPOINTS")
    if grader_obstructions:
        blockers.append("FROZEN_GRADER_CANNOT_RESUME_TERMINAL_GRADER_CHECKPOINTS")
    if not pilot_valid:
        blockers.append("NO_VERIFIED_PILOT_ACCEPTANCE_FILE")
    return {
        "candidate_attempts_by_status": dict(Counter(r["status"] for r in candidate_attempts)),
        "grader_attempts_by_status": dict(Counter(r["status"] for r in grader_attempts)),
        "candidate_terminal_obstructions": [dict(case_id=c, arm=a, status=status)
                                             for c, a, status in candidate_obstructions],
        "grader_terminal_obstructions": [dict(case_id=c, status=status)
                                          for c, status in grader_obstructions],
        "supervisor_lock_present": lock,
        "pilot_acceptance_present_and_bound": pilot_valid,
        "resume_blockers": blockers,
        "resume_disposition": "BLOCKED_INSPECT_LOCALLY" if blockers
                              else "PRECHECK_PASS_LOCAL_AUTH_QUOTA_UNVERIFIED",
    }


def audit(freeze_path):
    f = e.validate_historical_freeze(freeze_path)
    e.require(f.get("evaluation_mode") == "SOLO_DEVELOPER"
              and f.get("candidate_target") == 1080
              and f.get("pilot_target") == 36, "UNSUPPORTED_FROZEN_EVALUATION")
    pilot_audit = e.load(PILOT_AUDIT)
    excluded = verified_exclusions(pilot_audit, f)
    records = s.rows(f)  # verifies candidate and grader raw traces and their bindings
    base = s.location(f)
    candidates = [receipt_integrity(p, "candidate")
                  for p in sorted(base.glob("candidates/*/*/receipt.json"))]
    graders = [receipt_integrity(p, "grader")
               for p in sorted(base.glob("grades/*/*/receipt.json"))]
    status = local_checkpoint_status(f, records, candidates, graders, base)
    return {
        "classification": "SOLO_DEVELOPER_SELF_REVIEWED_AI_ASSISTED_PROVISIONAL",
        "audit_only": True,
        "source_sha": f["source_sha"],
        "freeze_sha256": e.digest(f),
        "pilot_audit_sha256": e.digest(PILOT_AUDIT.read_bytes()),
        "matrix_total": 1080,
        "verified_completed_candidate_pairs": len(records),
        "verified_graded_pairs": sum(bool(r.get("grade")) for r in records),
        "excluded_from_task_accuracy": sorted(excluded),
        "accuracy_derived_with_exclusions": accuracy_after_exclusions(records, excluded),
        "critical_pairs_all_graded": sum(bool(r["grade"]["critical_violations"])
                                          for r in records if r.get("grade")),
        "contradictions_all_graded": sum(bool(r["grade"]["contradictions"])
                                        for r in records if r.get("grade")),
        "holdouts": "54_NONBLIND_REGRESSION_ONLY",
        "unhinted_routing": "NOT_OBSERVABLE",
        "chatgpt_host_activation": "NOT_OBSERVABLE",
        "release": "RELEASE_BLOCKED",
        **status,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", type=Path, required=True)
    parser.add_argument("--output", type=Path, help="Optional NEW local-only audit JSON")
    args = parser.parse_args()
    try:
        report = audit(args.freeze)
        if args.output:
            e.save_new(args.output, report)
        print(json.dumps(report, indent=2, sort_keys=True))
    except (e.Invalid, ValueError, OSError, KeyError) as exc:
        parser.exit(2, "AUDIT_BLOCKED: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
