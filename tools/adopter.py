#!/usr/bin/env python3
"""Read-only, no-clobber adoption/upgrade preflight.

Never copies, modifies, deletes or overwrites host or source files.
Only the selected candidate is inspected; no unrelated repository is accessed.
This is NOT an atomic safeguard against concurrent filesystem changes.
"""
import argparse
import json
from pathlib import Path

import library

PACKAGE_ROOTS = ("ideas", "features", "templates")
PACKAGE_TOPLEVEL = ("LIBRARY-AGENT-GUIDE.md",)
PACKAGE_DOCS = {
    "ADOPTION.md", "ISOLATION.md", "LIFECYCLE.md",
    "ONE-WAY-BOUNDARY.md", "PROVENANCE.md",
}
PACKAGE_TOOL_FILES = {"library.py", "adopter.py"}
PACKAGE_TEST_FILES = {
    "test_library.py", "test_one_way_boundary.py", "test_hardening.py",
    "test_adopter_profiles.py",
}


def candidates(source):
    files = []
    for section in PACKAGE_ROOTS:
        folder = source / section
        if not folder.is_dir() or library.has_link_component(source, folder):
            raise ValueError(f"source section absent or linked: {section}")
        for path in folder.rglob("*"):
            if library.has_link_component(source, path):
                raise ValueError(f"source symlink is forbidden: {path}")
            if path.is_file():
                files.append(path.relative_to(source))
    for name in PACKAGE_TOPLEVEL:
        path = source / name
        if path.is_file():
            files.append(path.relative_to(source))
    for name in sorted(PACKAGE_DOCS):
        path = source / "docs" / name
        if path.is_file():
            files.append(path.relative_to(source))
    for prefix, allowed in (("tools", PACKAGE_TOOL_FILES), ("tests", PACKAGE_TEST_FILES)):
        for name in sorted(allowed):
            path = source / prefix / name
            if path.is_file():
                files.append(path.relative_to(source))
    return sorted(set(files), key=lambda p: p.as_posix())


def plan(source, destination):
    source = Path(source).absolute()
    destination = Path(destination).absolute()
    if source == destination:
        raise ValueError("source and host destination may not be the same")
    if library.has_link_component(source, source):
        raise ValueError("source root symlink")
    if destination.is_symlink() or (destination.exists() and not destination.is_dir()):
        raise ValueError("host destination is not a safe directory")
    if not destination.exists():
        # Parent path cannot be treated as an authorized installation.
        return {"status": "NEW_DESTINATION", "writes": False,
                "entries": [{"path": p.as_posix(), "action": "ADD"}
                            for p in candidates(source)]}
    if library.has_link_component(destination, destination):
        raise ValueError("host root symlink")
    entries = []
    for relative in candidates(source):
        target = destination / relative
        if library.has_link_component(destination, target):
            raise ValueError(f"host path symlink: {relative}")
        if target.is_dir():
            entries.append({"path": relative.as_posix(), "action": "CONFLICT_DIRECTORY"})
        elif target.is_file():
            # Do not interpret canonical host data or user documentation as upstream-managed.
            if "records" in relative.parts or relative.name == "INDEX.md":
                action = "KEEP_HOST"
            elif target.read_bytes() == (source / relative).read_bytes():
                action = "SAME"
            else:
                action = "REVIEW_LOCAL_DIFFERENCE"
            entries.append({"path": relative.as_posix(), "action": action})
        else:
            entries.append({"path": relative.as_posix(), "action": "ADD"})
    return {"status": "EXISTING_DESTINATION", "writes": False, "entries": entries}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="chosen host library directory")
    parser.add_argument("--source", type=Path, default=library.ROOT)
    args = parser.parse_args(argv)
    try:
        result = plan(args.source, args.destination)
    except (ValueError, OSError) as exc:
        print(json.dumps({"status": "BLOCKED", "writes": False, "error": str(exc)}))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if any(e["action"] in ("REVIEW_LOCAL_DIFFERENCE", "CONFLICT_DIRECTORY")
                    for e in result["entries"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
