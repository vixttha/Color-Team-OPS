"""Owner-authorized one-grader-call recovery bridge.

Use only through the one-off self-hosted Windows workflow. Executes the
separately committed append-only adapter against the ORIGINAL frozen checkout.
No source mutation, no prompt modification, no raw evidence or secrets in logs.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import runpy
import sys

from v002_windows_codex_preflight import canonical_sha, resolve_checkout, FROZEN_REL


def main():
    if (os.name != "nt" or
        os.environ.get("GITHUB_ACTIONS") != "true" or
        os.environ.get("GITHUB_EVENT_NAME") != "push" or
        os.environ.get("GITHUB_REF") != "refs/heads/feature/v0.0.2-codex-independent-eval" or
        os.environ.get("CTO_ONE_GRADER_CALL") != "OWNER_AUTHORIZED_QUOTA_RECOVERY_2026_11_05"):
        print(json.dumps({"disposition": "UNAUTHORIZED_JOB_CONTEXT"}))
        return 2
    workspace = Path(os.environ["GITHUB_WORKSPACE"])
    frozen = json.loads((workspace / FROZEN_REL).read_text(encoding="utf-8"))
    root, private, state = resolve_checkout(canonical_sha(frozen))
    if state != "ONE" or root is None:
        print(json.dumps({"disposition": "LOCAL_EVIDENCE_NOT_UNIQUELY_BOUND"}))
        return 2
    os.environ["GIT_OPTIONAL_LOCKS"] = "0"
    os.environ["GIT_TERMINAL_PROMPT"] = "0"
    os.chdir(root)
    sys.path.insert(0, str(root))
    sys.argv = [str(workspace / "devtools" / "solo_eval_quota_recovery.py"),
                "execute-one", "--freeze", str(root / FROZEN_REL),
                "--one-call-authorization",
                "ALLOW_ONE_EXISTING_CHATGPT_SUBSCRIPTION_GRADER_CALL"]
    runpy.run_path(sys.argv[0], run_name="__main__")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError):
        print(json.dumps({"disposition": "ONE_CALL_RECOVERY_BLOCKED"}))
        sys.exit(2)
