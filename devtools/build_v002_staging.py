"""Create an isolated v0.0.2 STAGING variant from a VERIFIED source ZIP.

Developer-side only. This does not install/update/publish any ChatGPT plugin.
"""
from hashlib import sha256
from io import BytesIO
from pathlib import PurePosixPath
import json
import stat
import zipfile

from .build_v002_candidate import validate_archive, PackageError

STAGING_SLUG = "color-team-ops-v002-staging"
STAGING_LABEL = "Color Team OPS v0.0.2 STAGING — NOT RELEASED"
_MUTATED = ("plugin.json", ".codex-plugin/plugin.json")
_TIME = (1980, 1, 1, 0, 0, 0)


def _serialize(x):
    return (json.dumps(x, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode("utf8")


def build_staging(source_zip: bytes, source_sha: str):
    """Return staging zip and descriptor; exact 12 skills/9 refs, all original bytes except manifests."""
    validate_archive(source_zip, source_sha)
    with zipfile.ZipFile(BytesIO(source_zip)) as z:
        files = {name: z.read(name) for name in z.namelist()}
    original_hash = sha256(source_zip).hexdigest()
    for path in _MUTATED:
        m = json.loads(files[path])
        if m["name"] != "color-team-ops" or m["version"] != "0.0.2":
            raise PackageError("INVALID_CANONICAL_SOURCE_MANIFEST")
        m["name"] = STAGING_SLUG
        m["description"] = "PRIVATE TEST ONLY — Color Team OPS v0.0.2 STAGING. Not an official release; canonical v0.0.1 untouched. Cloud-only skill references."
        if path == "plugin.json":
            ui = m["extensions"]["com.openai"]["interface"]
        else:
            ui = m["interface"]
        ui["displayName"] = STAGING_LABEL
        ui["shortDescription"] = "PRIVATE STAGING — Not released"
        ui["longDescription"] = ("PRIVATE TEST ONLY for exact-source Color Team OPS v0.0.2; "
            "nine specialists, three coordinators, nine competency references. "
            "No canonical plugin updates, public sharing, production grants, "
            "local runner dependency or official release authorization.")
        ui["defaultPrompt"] = ("Use Color Team OPS v0.0.2 STAGING for one bounded "
            "test-only skills mission; do not claim production release or tool grants.")
        files[path] = _serialize(m)
    m = json.loads(files["RELEASE-SOURCE-MANIFEST.json"])
    if m["source_sha"] != source_sha:
        raise PackageError("STAGING_SOURCE_BOUNDARY_LOST")
    m["variant"] = "PRIVATE_STAGING_NOT_RELEASED"
    m["staging_name"] = STAGING_SLUG
    m["source_candidate_zip_sha256"] = original_hash
    m["modified_files_from_original_source"] = list(_MUTATED)
    m["files"] = [{"path": name, "sha256": sha256(data).hexdigest(), "bytes": len(data)}
                  for name, data in sorted(files.items()) if name != "RELEASE-SOURCE-MANIFEST.json"]
    files["RELEASE-SOURCE-MANIFEST.json"] = _serialize(m)
    specialists = [n for n in files if n.startswith("skills/") and n.endswith("/SKILL.md")]
    refs = [n for n in files if n.startswith("skills/") and n.endswith("/references/v002-competencies.md")]
    if len(files) != 32 or len(specialists) != 12 or len(refs) != 9:
        raise PackageError("STAGING_ROLE_OR_REFERENCE_COUNT_INVALID")
    out = BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_STORED, allowZip64=False) as z:
        for name, data in sorted(files.items()):
            if PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts:
                raise PackageError("UNSAFE_STAGING_ZIP_PATH")
            info = zipfile.ZipInfo(name, date_time=_TIME)
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            z.writestr(info, data)
    result = out.getvalue()
    with zipfile.ZipFile(BytesIO(result)) as z:
        actual = json.loads(z.read("RELEASE-SOURCE-MANIFEST.json"))
        if set(z.namelist()) != {x["path"] for x in actual["files"]} | {"RELEASE-SOURCE-MANIFEST.json"}:
            raise PackageError("STAGING_FILE_LIST_MISMATCH")
        if any(sha256(z.read(x["path"])).hexdigest() != x["sha256"] for x in actual["files"]):
            raise PackageError("STAGING_FILE_DIGEST_MISMATCH")
    return result, {"source_sha": source_sha, "source_zip_sha256": original_hash,
                    "staging_zip_sha256": sha256(result).hexdigest(),
                    "staging_slug": STAGING_SLUG,
                    "staging_display_name": STAGING_LABEL,
                    "files": 32, "skills": 12, "competencies": 9,
                    "private_test_only": True}


def main():
    import argparse
    from pathlib import Path
    p = argparse.ArgumentParser()
    p.add_argument("--source-zip", type=Path, required=True)
    p.add_argument("--source-sha", required=True)
    p.add_argument("--output", type=Path, required=True)
    x = p.parse_args()
    contents, report = build_staging(x.source_zip.read_bytes(), x.source_sha)
    x.output.write_bytes(contents)
    print("CTO_V002_PRIVATE_STAGING_ARCHIVE", report["staging_zip_sha256"],
          report["files"], report["source_sha"], "source", report["source_zip_sha256"])
if __name__ == "__main__":
    main()
