#!/usr/bin/env python3
"""Optional local copy helper. No project code, runner, network, or plugin required.

Preflights every top-level destination and refuses to overwrite existing files.
As with any nontransactional filesystem copy, concurrent external writers can
cause partial installation. Never claim atomicity or automatic cleanup.
"""
import argparse
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1]
CORE = ("ideas", "features", "templates", "LIBRARY-AGENT-GUIDE.md")
OPTIONAL = ("tools", "tests", "docs")


def adopt(target, source=SOURCE, with_tools=False):
    target, source = Path(target), Path(source)
    if not target.is_dir() or target.is_symlink():
        raise ValueError("Target must be an existing, non-symlink project directory")
    names = CORE + (OPTIONAL if with_tools else ())
    for name in names:
        inp, out = source / name, target / name
        if not inp.exists() or inp.is_symlink():
            raise ValueError(f"Missing or unsafe template source: {name}")
        if out.exists() or out.is_symlink():
            raise FileExistsError(f"Refusing to overwrite host path: {out}")
        if inp.is_dir() and any(p.is_symlink() for p in inp.rglob("*")):
            raise ValueError(f"Unsafe symlink in template: {name}")
    # All destinations are checked before the first write. copytree and copy
    # refuse to overwrite; a concurrent write can still leave partial copies.
    for name in names:
        inp, out = source / name, target / name
        if inp.is_dir():
            shutil.copytree(inp, out)
        else:
            with inp.open("rb") as stream, out.open("xb") as dest:
                shutil.copyfileobj(stream, dest)
    return names


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="Existing host project directory")
    parser.add_argument("--with-tools", action="store_true", help="Also copy optional tools, tests and docs")
    args = parser.parse_args()
    copied = adopt(args.target, with_tools=args.with_tools)
    print("Copied without overwrites:", ", ".join(copied))
