"""Read-only, pre-output reviewer intake packet generator (development only).

This deliberately DOES NOT enroll a reviewer, mint a signing key, sign an oracle,
approve a rubric, upload evidence or grade candidate outputs. Private keys belong
on the separately authenticated reviewer's machine.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from devtools import cli_eval

ROOT = cli_eval.ROOT
EVAL = cli_eval.EVAL
PRIVATE = ROOT / ".cli-eval-private"


def encoded(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False,
                       indent=2) + "\n").encode("utf-8")


def sha256(value: bytes):
    return hashlib.sha256(value).hexdigest()


def assemble(freeze, cases, criteria):
    """Return reviewer-visible inputs and safe UNAPPROVED receipt templates."""
    bindings = freeze.get("cases", {})
    by_id = {case["case_id"]: case for case in cases}
    if len(by_id) != 270 or len(cases) != 270 or set(bindings) != set(by_id):
        raise ValueError("EXPECTED_EXACT_270_FROZEN_CASES")
    if set(criteria) != set(bindings):
        raise ValueError("REVIEWER_CRITERIA_ID_MISMATCH")
    if freeze.get("oracle_independent_approvals") != 0:
        raise ValueError("USE_NEW_PREOUTPUT_REVIEW_SEQUENCE")
    packets = []
    templates = []
    for cid in sorted(bindings):
        case, rubric, bind = by_id[cid], criteria[cid], bindings[cid]
        if (cli_eval.digest(rubric) != bind["rubric_sha256"] or
                cli_eval.digest(cli_eval.candidate_input(case)) != bind["input_sha256"]):
            raise ValueError("SOURCE_OR_RUBRIC_CHANGED:" + cid)
        category = bind.get("holdout")
        if category not in ("SOURCE_VISIBLE_DEVELOPMENT", "NONBLIND_REGRESSION_ONLY"):
            raise ValueError("UNKNOWN_HOLDOUT_CLASSIFICATION:" + cid)
        nonblind = category == "NONBLIND_REGRESSION_ONLY"
        packets.append({
            "case_id": cid,
            "team_id": case["team_id"],
            "band": case["band"],
            "topic": case["topic"],
            "candidate_input": json.loads(cli_eval.candidate_input(case)),
            "proposed_developer_criteria": {
                "required_observable_findings": rubric["required_observable_findings"],
                "forbidden_outcomes": rubric["forbidden_outcomes"],
                "expected_domain_conclusion": rubric["expected_domain_conclusion"],
                "variant_condition": rubric["variant_condition"],
                "review_status": "NOT_INDEPENDENTLY_APPROVED"
            },
            "frozen_rubric_sha256": bind["rubric_sha256"],
            "frozen_candidate_input_sha256": bind["input_sha256"],
            "source_sha": freeze["source_sha"],
            "holdout_classification": ("NONBLIND_REGRESSION_ONLY" if nonblind
                                       else "VISIBLE_DEVELOPMENT_FIXTURE"),
            "candidate_output": None,
            "independent_score": None,
        })
        templates.append({
            "reviewer_principal": None,
            "decision": "PENDING_NOT_APPROVED",
            "case_id": cid,
            "rubric_sha256": bind["rubric_sha256"],
            "reviewed_at": None,
            "preoutput_commit": freeze["source_sha"],
            "technical_outcome": None,
            "valid_alternatives": None,
            "legitimate_refusal": None,
            "critical_flaws": None,
            "difficulty_fairness": None,
        })
    if sum(p["holdout_classification"] == "NONBLIND_REGRESSION_ONLY"
           for p in packets) != 54:
        raise ValueError("HOLDOUT_SOURCE_POLICY_CHANGED")
    return packets, templates


def ensure_private_destination(destination):
    """Fail closed: output only to a new directory inside ignored local storage."""
    base = PRIVATE.resolve()
    dest = Path(destination).resolve()
    if not dest.is_relative_to(base) or dest == base:
        raise ValueError("OUTPUT_MUST_BE_UNDER_CLI_EVAL_PRIVATE")
    if dest.exists():
        raise FileExistsError("REVIEWER_PACKET_DESTINATION_ALREADY_EXISTS")
    return dest


def prepare(freeze_path, destination):
    freeze = cli_eval.load(freeze_path)
    cases = cli_eval.corpus(ROOT)
    criteria = cli_eval.load(ROOT / EVAL / "reviewer-case-criteria.json")["cases"]
    packets, templates = assemble(freeze, cases, criteria)
    dest = ensure_private_destination(destination)
    dest.mkdir(parents=True)
    packet_bytes = encoded(packets)
    template_bytes = encoded(templates)
    manifest = {
        "classification": "REVIEWER_ONBOARDING_ONLY_NOT_APPROVAL",
        "source_sha": freeze["source_sha"],
        "freeze_sha256": sha256(Path(freeze_path).read_bytes()),
        "case_count": len(packets),
        "unsigned_template_count": len(templates),
        "nonblind_source_visible_cases": 54,
        "independent_oracle_approvals": 0,
        "real_independent_reviewer_enrolled": False,
        "candidate_responses_included": False,
        "reviewer_packets_sha256": sha256(packet_bytes),
        "unsigned_templates_sha256": sha256(template_bytes),
        "next_step": ("Require separately owner-verified reviewer principal and "
                      "signing public key, THEN signed per-case pre-output reviews "
                      "committed before a NEW freeze and NEW formal candidate runs."),
    }
    (dest / "reviewer-packets.json").write_bytes(packet_bytes)
    (dest / "UNSIGNED-REVIEW-TEMPLATES.json").write_bytes(template_bytes)
    (dest / "manifest.json").write_bytes(encoded(manifest))
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(prepare(args.freeze, args.output),
                     sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
