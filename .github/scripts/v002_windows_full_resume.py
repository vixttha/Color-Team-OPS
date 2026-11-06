"""Owner-authorized bounded frozen 270x4 resume through Windows self-hosted CI.

This is a bridge, NOT a model evaluator: import frozen source/credentials only
from the already validated local original checkout, keep untrusted CI source out
of the original runtime import path, and execute the additive supervisor.
No paid API, host tests, staging writes, credential export or raw trace uploads.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import runpy
import sys

from v002_windows_codex_preflight import canonical_sha, resolve_checkout, FROZEN_REL

REQUIRED_REF = "refs/heads/feature/v0.0.2-codex-independent-eval"
REQUIRED_AUTH = "OWNER_APPROVED_RESUME_FROZEN_270x4_2026_11_05"
EXPECTED_FROZEN_SHA = "116c8468e98bfed123c7014586c6791114f2d57b596cb8af918192c437d3186b"


def main():
    if (
        os.name != "nt" or os.environ.get("GITHUB_ACTIONS") != "true"
        or os.environ.get("GITHUB_EVENT_NAME") != "push"
        or os.environ.get("GITHUB_REF") != REQUIRED_REF
        or os.environ.get("CTO_FULL_RESUME_AUTH") != REQUIRED_AUTH
    ):
        print(json.dumps({"status": "RESUME_UNAUTHORIZED_CONTEXT"}))
        return 2
    workspace = Path(os.environ["GITHUB_WORKSPACE"])
    frozen = json.loads((workspace / FROZEN_REL).read_text(encoding="utf-8"))
    if canonical_sha(frozen) != EXPECTED_FROZEN_SHA:
        print(json.dumps({"status": "FROZEN_V2_DIGEST_CHANGED"}))
        return 2
    root, private, state = resolve_checkout(EXPECTED_FROZEN_SHA)
    if state != "ONE" or root is None:
        print(json.dumps({"status": "ORIGINAL_LOCAL_CHECKPOINT_NOT_UNIQUELY_FOUND"}))
        return 2
    os.environ["GIT_OPTIONAL_LOCKS"] = "0"
    os.environ["GIT_TERMINAL_PROMPT"] = "0"
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    os.chdir(root)
    sys.path.insert(0, str(root))
    sys.argv = [
        str(workspace / "devtools" / "solo_eval_resume_batch.py"),
        "--freeze", str(root / FROZEN_REL),
        "--max-new-pairs", "1008",
        "--runtime-seconds", "17000",
    ]
    runpy.run_path(sys.argv[0], run_name="__main__")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # No untrusted stack trace, local paths, model text or auth output.
        print(json.dumps({"status": "RESUME_BRIDGE_FAILED",
                          "raw_evidence_preserved": True}))
        sys.exit(2)
