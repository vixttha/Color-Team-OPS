"""Invoke new additive quota-recovery CHECK only, against existing local freeze.

Runs on owner's Windows self-hosted GitHub Actions runner. No model inference,
no credential printing, no local file modifications, no checkpoint rewriting.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import runpy
import sys

from v002_windows_codex_preflight import canonical_sha, resolve_checkout, FROZEN_REL


def main():
    if os.name != "nt" or os.environ.get("GITHUB_ACTIONS") != "true":
        print(json.dumps({"status": "NOT_AUTHORIZED_RUNNER"}))
        return 2
    workspace = Path(os.environ["GITHUB_WORKSPACE"])
    freeze = json.loads((workspace / FROZEN_REL).read_text(encoding="utf-8"))
    root, private, state = resolve_checkout(canonical_sha(freeze))
    if state != "ONE" or root is None:
        print(json.dumps({"status": "EXACT_EVIDENCE_NOT_UNIQUELY_FOUND"}))
        return 2
    # Force imports of the ORIGINAL 44 frozen source files. Only the new
    # companion is read from the workflow checkout.
    os.environ["GIT_OPTIONAL_LOCKS"] = "0"
    os.environ["GIT_TERMINAL_PROMPT"] = "0"
    os.chdir(root)
    sys.path.insert(0, str(root))
    sys.argv = [str(workspace / "devtools" / "solo_eval_quota_recovery.py"),
                "check", "--freeze", str(root / FROZEN_REL)]
    runpy.run_path(sys.argv[0], run_name="__main__")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, TypeError):
        print(json.dumps({"status": "SAFE_LOCAL_PREFLIGHT_BLOCKED"}))
        sys.exit(2)
