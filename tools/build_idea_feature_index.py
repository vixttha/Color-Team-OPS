#!/usr/bin/env python3
"""Deterministic derived views for the Color-Team-OPS historical catalog.

Records are the source of truth; generated indexes are NEVER approval or release evidence.
No dependencies, network, runtime integration, or automatic writes except explicit build.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _records(root, kind):
    result = []
    for path in sorted((root / kind / "records").glob("*.json")):
        with path.open(encoding="utf-8") as handle:
            row = json.load(handle)
        result.append(row)
    return result


def _cell(value):
    # Escape display-only Markdown content without treating it as instructions.
    return (str(value).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace("|", "/")
            .replace("\r", " ").replace("\n", " "))


def render_indexes(root=ROOT):
    ideas = [
        "# Color-Team-OPS — Idea Index (generated)", "",
        "> Generated from `ideas/records/*.json` in this exact branch; do not edit manually. Source status and adoption are not implementation evidence.",
        "", "| ID | Idea | Lifecycle | Implementation | Source |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in _records(root, "ideas"):
        origin = row.get("origin") or {}
        ideas.append("| {} | {} | {} | {} | {} |".format(
            _cell(row["id"]), _cell(row["title"]), _cell(row["lifecycle_status"]),
            _cell(row["implementation_status"]), _cell(origin.get("source_catalog_id", "—"))))
    features = [
        "# Color-Team-OPS — Candidate Features (generated)", "",
        "> Generated view only; no verified implementation or release membership is asserted.",
        "", "| ID | Feature | Proposed milestone | State |",
        "| --- | --- | --- | --- |",
    ]
    for row in _records(root, "features"):
        features.append("| {} | {} | {} | {} / {} |".format(
            _cell(row["id"]), _cell(row["title"]), _cell(row.get("planned_milestone", "—")),
            _cell(row["lifecycle_status"]), _cell(row["release_membership"])))
    return {
        "ideas/INDEX.md": "\n".join(ideas) + "\n",
        "features/INDEX.md": "\n".join(features) + "\n",
    }


def build(root=ROOT):
    from check_idea_feature_library import validate
    failures = validate(root)
    if failures:
        raise ValueError("Invalid records, refusing to regenerate indexes: " + "; ".join(failures))
    for filename, output in render_indexes(root).items():
        target = root / filename
        if target.is_symlink():
            raise ValueError(f"Refusing symlink index: {target}")
        target.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    build(args.root)
    print("PASS: regenerated historical catalog indexes (views only)")
