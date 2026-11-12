#!/usr/bin/env python3
"""Release-review-only standalone v0.0.2 smoke.

Run against a pinned clean 24-file Git checkout; never modifies source,
any user's repository, credentials, branch, tag, or published release.
Uses only Python standard library and a disposable OS-temp host.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

FILES = {
    "LIBRARY-AGENT-GUIDE.md",
    "README.md",
    "docs/ADOPTION.md",
    "docs/ISOLATION.md",
    "docs/LIFECYCLE.md",
    "docs/ONE-WAY-BOUNDARY.md",
    "docs/PROVENANCE.md",
    "features/INDEX.md",
    "features/README.md",
    "features/records/.gitkeep",
    "features/schema/v1/feature.schema.json",
    "ideas/INDEX.md",
    "ideas/README.md",
    "ideas/records/.gitkeep",
    "ideas/schema/v1/idea.schema.json",
    "templates/feature.example.json",
    "templates/idea.example.json",
    "tests/test_adopter_profiles.py",
    "tests/test_hardening.py",
    "tests/test_library.py",
    "tests/test_one_way_boundary.py",
    "tests/test_v002_six_team_repairs.py",
    "tools/adopter.py",
    "tools/library.py",
}


def invoke(args, cwd, good=(0,), capture=False):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    completed = subprocess.run(args, cwd=str(cwd), env=env,
                               text=True, stdout=subprocess.PIPE if capture else None,
                               stderr=subprocess.PIPE if capture else None,
                               check=False)
    if completed.returncode not in good:
        if capture:
            print("STDOUT:", completed.stdout, "STDERR:", completed.stderr, flush=True)
        raise AssertionError(f"Command failed status={completed.returncode}: {args}")
    return completed


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean_git(path):
    dirty = invoke(["git", "status", "--porcelain", "--untracked-files=all"],
                   path, capture=True).stdout.strip()
    if dirty:
        raise AssertionError("Source checkout unexpectedly modified: " + dirty)


def verify_manifest(package, sha):
    actual_sha = invoke(["git", "rev-parse", "HEAD"], package, capture=True).stdout.strip()
    assert actual_sha == sha, (actual_sha, sha)
    tracked = invoke(["git", "ls-files", "-z"], package, capture=True).stdout
    actual = set(tracked.strip("\x00").split("\x00"))
    assert actual == FILES, {"missing": sorted(FILES - actual),
                             "unexpected": sorted(actual - FILES)}
    assert len(FILES) == 24
    for relative in sorted(FILES):
        path = package / relative
        assert path.is_file() and not path.is_symlink(), relative
    for forbidden in ("AGENTS.md", "GOVERNANCE-START.md", "governance",
                      "src", ".github", "ops", "plugin.json", ".codex-plugin"):
        assert not (package / forbidden).exists(), forbidden
    for kind in ("ideas", "features"):
        assert not list((package / kind / "records").glob("*.json"))
    doc_links = 0
    for relative in sorted(FILES):
        if not relative.endswith(".md"):
            continue
        content = (package / relative).read_text(encoding="utf-8")
        for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", content):
            target = match.group(1).split("#", 1)[0].split("?", 1)[0]
            if not target or re.match(r"^(https?://|mailto:|app://)", target):
                continue
            resolved = (package / relative).parent / target
            assert resolved.is_file(), (relative, target)
            assert resolved.resolve().is_relative_to(package.resolve()), target
            doc_links += 1
    assert doc_links >= 15, doc_links
    print("PASS_PACKAGE_MANIFEST", actual_sha, "files=24, local_links=", doc_links,
          flush=True)


def smoke_fresh_host(package):
    with tempfile.TemporaryDirectory(prefix="v002-fresh-adopter-") as td:
        host = Path(td) / "unrelated-host"
        host.mkdir()
        for relative in sorted(FILES):
            target = host / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(package / relative, target)
        assert not (host / ".git").exists()
        # First the copied package must validate as a genuinely empty starter.
        invoke([sys.executable, "-B", "tools/library.py", "check", "--expect-empty"],
               host)
        idea = json.loads((host / "templates/idea.example.json").read_text("utf-8"))
        feature = json.loads((host / "templates/feature.example.json").read_text("utf-8"))
        idea["title"] = "Synthetic unrelated-host idea"
        feature["title"] = "Synthetic unrelated-host feature"
        feature["idea_ids"] = [idea["id"]]
        idea_path = host / "ideas/records" / (idea["id"] + ".json")
        feat_path = host / "features/records" / (feature["id"] + ".json")
        idea_path.write_text(json.dumps(idea, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8", newline="\n")
        feat_path.write_text(json.dumps(feature, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8", newline="\n")
        local_doc = host / "docs/ADOPTION.md"
        local_doc.write_text(local_doc.read_text(encoding="utf-8") +
                             "\nHost-owned customization: do not overwrite.\n",
                             encoding="utf-8", newline="\n")
        before = {x: digest(x) for x in (idea_path, feat_path, local_doc)}
        invoke([sys.executable, "-B", "tools/library.py", "build"], host)
        invoke([sys.executable, "-B", "tools/library.py", "check"], host)
        # Explicitly prevent the publisher-only empty flag passing in adopters.
        invoke([sys.executable, "-B", "tools/library.py", "check",
                "--expect-empty"], host, good=(1,))
        # Full regression suite must also work with populated host records.
        invoke([sys.executable, "-B", "-m", "unittest", "discover",
                "-s", "tests", "-p", "test_*.py", "-v"], host)
        plan = invoke([sys.executable, "-B", "tools/adopter.py", str(host),
                       "--source", str(package)], package, good=(1,), capture=True)
        result = json.loads(plan.stdout)
        assert result["status"] == "EXISTING_DESTINATION"
        assert result["writes"] is False
        actions = {r["path"]: r["action"] for r in result["entries"]}
        assert actions["docs/ADOPTION.md"] == "REVIEW_LOCAL_DIFFERENCE"
        assert actions["tests/test_v002_six_team_repairs.py"] == "SAME"
        assert actions["ideas/records/.gitkeep"] == "KEEP_HOST"
        assert before == {x: digest(x) for x in before}
        # A Governance collision must STOP, not produce an upgrade plan.
        (host / "ideas/library.yaml").write_text("type: synthetic-governance\n",
                                                  encoding="utf-8")
        blocked = invoke([sys.executable, "-B", "tools/adopter.py", str(host),
                          "--source", str(package)], package, good=(2,), capture=True)
        collision = json.loads(blocked.stdout)
        assert collision["status"] == "NAMESPACE_COLLISION"
        assert collision["writes"] is False and collision["entries"] == []
        assert before == {x: digest(x) for x in before}
        print("PASS_FRESH_HOST: 1 idea, 1 feature, linked, indexes deterministic, "
              "suite passed, no-clobber and Governance collision blocked",
              flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--sha", required=True)
    opts = parser.parse_args()
    package = opts.package.resolve(strict=True)
    assert re.fullmatch("[0-9a-f]{40}", opts.sha), opts.sha
    if sys.version_info < (3, 10):
        raise RuntimeError("Python 3.10+ required for smoke harness")
    before = {p: digest(package / p) for p in FILES}
    clean_git(package)
    verify_manifest(package, opts.sha)
    invoke([sys.executable, "-B", "tools/library.py", "check", "--expect-empty"],
           package)
    invoke([sys.executable, "-B", "-m", "unittest", "discover",
            "-s", "tests", "-p", "test_*.py", "-v"], package)
    invoke([sys.executable, "-B", "tools/library.py", "build", "--expect-empty"],
           package)
    clean_git(package)
    smoke_fresh_host(package)
    assert before == {p: digest(package / p) for p in FILES}
    clean_git(package)
    print("PASS_STANDALONE_PACKAGE: manifest + original-byte integrity + "
          "standalone suite + disposable fresh-adopter, without host writes",
          flush=True)


if __name__ == "__main__":
    main()
