#!/usr/bin/env python3
"""Read-only, count-neutral validation of the historical Color-Team-OPS library.

Checks the assertions used by the checked-in JSON Schemas and semantic invariants.
Syntactic evidence checks DO NOT authenticate a receipt, reviewer, release or host.
"""
import json
import re
from pathlib import Path, PurePosixPath, PureWindowsPath

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = {"adopted", "parked", "rejected", "superseded", "duplicate", "retired"}
ALLOWED_SCHEMA_KEYS = {
    "$schema", "$id", "title", "description", "type", "required", "properties",
    "additionalProperties", "const", "enum", "pattern", "minLength", "maxLength",
    "minItems", "maxItems", "uniqueItems", "items", "allOf", "if", "then", "else",
}


def read_json(path):
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_pairs)


def validate_schema(value, schema, location):
    """Fail closed on unknown assertion keywords; only the bundled subset is supported."""
    errors = []
    unsupported = set(schema) - ALLOWED_SCHEMA_KEYS
    if unsupported:
        return [f"{location}: unsupported schema keywords {sorted(unsupported)}"]
    typ = schema.get("type")
    types = {
        "object": lambda x: isinstance(x, dict),
        "array": lambda x: isinstance(x, list),
        "string": lambda x: isinstance(x, str),
        "integer": lambda x: type(x) is int,
        "boolean": lambda x: isinstance(x, bool),
    }
    if typ is not None and (typ not in types or not types[typ](value)):
        return [f"{location}: wrong type ({typ})"]
    if "const" in schema and (type(value) is not type(schema["const"]) or value != schema["const"]):
        errors.append(f"{location}: const mismatch")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{location}: invalid enum value")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{location}: too short")
        if len(value) > schema.get("maxLength", float("inf")):
            errors.append(f"{location}: too long")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{location}: pattern mismatch")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{location}: too few items")
        if len(value) > schema.get("maxItems", float("inf")):
            errors.append(f"{location}: too many items")
        if schema.get("uniqueItems") and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            errors.append(f"{location}: duplicate items")
        for i, item in enumerate(value):
            errors.extend(validate_schema(item, schema.get("items", {}), f"{location}[{i}]"))
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for required in schema.get("required", []):
            if required not in value:
                errors.append(f"{location}: missing {required}")
        if schema.get("additionalProperties") is False:
            for key in value.keys() - properties.keys():
                errors.append(f"{location}: unknown field {key}")
        for key in value.keys() & properties.keys():
            errors.extend(validate_schema(value[key], properties[key], f"{location}.{key}"))
    for sub in schema.get("allOf", []):
        if "if" in sub:
            conditional = not validate_schema(value, sub["if"], location)
            branch = sub.get("then" if conditional else "else")
            if branch is not None:
                errors.extend(validate_schema(value, branch, location))
        else:
            errors.extend(validate_schema(value, sub, location))
    return errors


def safe_path(value):
    return (
        isinstance(value, str) and bool(value) and "\\" not in value
        and not PurePosixPath(value).is_absolute()
        and not PureWindowsPath(value).is_absolute()
        and not re.match(r"^[A-Za-z]:", value)
        and all(part not in ("", ".", "..") for part in value.split("/"))
    )


def load(root, kind, schema, failures):
    directory = root / kind / "records"
    rows = {}
    if directory.is_symlink() or not directory.is_dir():
        failures.append(f"{kind}: missing or symlink records directory")
        return rows
    for path in sorted(directory.iterdir()):
        if path.name == ".gitkeep":
            continue
        if path.is_symlink() or not path.is_file() or path.suffix != ".json":
            failures.append(f"{path}: unexpected entry or symlink")
            continue
        try:
            row = read_json(path)
        except (OSError, ValueError, UnicodeError) as exc:
            failures.append(f"{path}: invalid JSON ({exc})")
            continue
        if not isinstance(row, dict):
            failures.append(f"{path}: record is not object")
            continue
        ident = row.get("id")
        if not isinstance(ident, str) or path.stem != ident:
            failures.append(f"{path}: invalid or mismatched ID")
            continue
        failures.extend(validate_schema(row, schema, str(path)))
        if ident in rows:
            failures.append(f"{kind}: duplicate ID {ident}")
        rows[ident] = row
    return rows


def validate(root=ROOT):
    root = Path(root)
    failures = []
    schemas = {}
    for kind, singular in (("ideas", "idea"), ("features", "feature")):
        schema_file = root / kind / "schema" / "v1" / f"{singular}.schema.json"
        if schema_file.is_symlink():
            failures.append(f"{schema_file}: symlink schema")
            return failures
        try:
            schemas[kind] = read_json(schema_file)
        except (OSError, ValueError, UnicodeError) as exc:
            failures.append(f"{schema_file}: invalid schema {exc}")
            return failures
        if schemas[kind].get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            failures.append(f"{schema_file}: unsupported schema dialect")
    ideas = load(root, "ideas", schemas["ideas"], failures)
    features = load(root, "features", schemas["features"], failures)
    for ident, row in ideas.items():
        if row.get("lifecycle_status") in DECISIONS and not row.get("decision"):
            failures.append(f"{ident}: decision-bearing lifecycle without decision")
        if row.get("lifecycle_status") == "adopted" and (
            row.get("decision") or {}).get("decision_scope") != "idea_direction_only":
            failures.append(f"{ident}: adopted idea without scoped decision")
        for relation in row.get("related_ideas", []):
            if relation == ident or relation not in ideas:
                failures.append(f"{ident}: missing/self idea relation {relation}")
        for evidence in row.get("evidence", []):
            if not safe_path(evidence.get("path")):
                failures.append(f"{ident}: unsafe evidence path")
    for ident, row in features.items():
        for idea_id in row.get("idea_ids", []):
            if idea_id not in ideas:
                failures.append(f"{ident}: unresolved idea {idea_id}")
        if row.get("release_membership") != "NOT_ASSERTED":
            failures.append(f"{ident}: library cannot certify releases")
        if row.get("lifecycle_status") == "verified":
            receipts = row.get("verified_evidence", [])
            testing = row.get("testing")
            bad_testing = testing is not None and (
                testing.get("status") != "tested" or testing.get("outcome") != "pass"
                or not testing.get("refs"))
            if (row.get("implementation_status") != "implemented" or not receipts
                or any(not e.get("receipt", "").strip() for e in receipts)
                or bad_testing):
                failures.append(f"{ident}: unsupported verified claim")
        for reference in row.get("source_refs", []):
            if not safe_path(reference.get("path")):
                failures.append(f"{ident}: unsafe source path")
    return failures


def check_indexes(root=ROOT):
    from build_idea_feature_index import render_indexes
    failures = validate(root)
    if failures:
        return failures
    for filename, content in render_indexes(Path(root)).items():
        path = Path(root) / filename
        if path.is_symlink():
            failures.append(f"{filename}: symlink index")
        elif not path.is_file() or path.read_text(encoding="utf-8") != content:
            failures.append(f"{filename}: stale index")
    return failures


if __name__ == "__main__":
    problems = check_indexes()
    if problems:
        for failure in problems:
            print("FAIL", failure)
        raise SystemExit(1)
    print("PASS: count-neutral legacy schema, records, links, evidence and indexes; "
          "no release, approval or host proof asserted")
