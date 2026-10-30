"""Deterministic Color Team OPS skills-only candidate archive (stdlib only).

This build tool is for authorized cloud development/release CI, NOT plugin runtime.
It never authenticates a user, dispatches an agent or executes policy_v002 Python.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha1, sha256
from io import BytesIO
from pathlib import Path, PurePosixPath
import argparse
import json
import re
import stat
import subprocess
import zipfile

_SHA = re.compile(r"^[0-9a-f]{40}$")
_TEAMS = frozenset(("yellow-team","orange-team","green-team","red-team",
                    "blue-team","purple-team","white-team","black-team","gray-cell"))
_COORD = frozenset(("mission-control","ops-director","verification-gate"))
_FIXED_TIME = (1980,1,1,0,0,0)
_MAX_FILE = 4 * 1024 * 1024
_MAX_TOTAL = 40 * 1024 * 1024

class PackageError(ValueError):
    pass

@dataclass(frozen=True)
class BuildResult:
    archive: bytes
    sha256_digest: str
    file_count: int
    source_sha: str


def _paths(root: Path) -> list[Path]:
    paths = [root/"plugin.json",root/".codex-plugin"/"plugin.json",
             root/"docs"/"CONSTITUTION.md",root/"registry"/"v0.0.2"/"teams.json"]
    paths += sorted((root/"schemas").glob("*.json"))
    paths += sorted((root/"examples").glob("*.json"))
    paths += sorted((root/"skills").glob("*/SKILL.md"))
    paths += sorted((root/"skills").glob("*/references/v002-competencies.md"))
    skill_ids = {x.parent.name for x in paths if x.name=="SKILL.md"}
    ref_ids = {x.parent.parent.name for x in paths if x.name=="v002-competencies.md"}
    if skill_ids != _TEAMS|_COORD or ref_ids != _TEAMS:
        raise PackageError("REQUIRED_SKILLS_OR_REFERENCES_MISSING")
    if (len([p for p in paths if p.parent==root/"schemas"])!=3 or
        len([p for p in paths if p.parent==root/"examples"])!=3):
        raise PackageError("PORTABLE_SCHEMAS_OR_EXAMPLES_MISSING")
    return paths


def build(root: Path, source_sha: str, *, check_checkout: bool=True) -> BuildResult:
    root=Path(root).resolve()
    if not _SHA.fullmatch(source_sha):
        raise PackageError("INVALID_SOURCE_SHA")
    if check_checkout:
        try:
            git_sha=subprocess.check_output(
                ["git","-C",str(root),"rev-parse","HEAD"],stderr=subprocess.DEVNULL,
                text=True,timeout=10).strip()
        except (subprocess.SubprocessError,FileNotFoundError,OSError):
            raise PackageError("GIT_REVISION_UNVERIFIED") from None
        if git_sha!=source_sha:
            raise PackageError("SOURCE_SHA_MISMATCH")
        try:
            dirty=subprocess.check_output(
                ["git","-C",str(root),"status","--porcelain","--untracked-files=all"],
                stderr=subprocess.DEVNULL,text=True,timeout=10)
        except (subprocess.SubprocessError,FileNotFoundError,OSError):
            raise PackageError("GIT_WORKTREE_UNVERIFIED") from None
        if dirty.strip():
            raise PackageError("DIRTY_SOURCE_CHECKOUT")
    tracked = None
    if check_checkout:
        try:
            git_root=subprocess.check_output(
                ["git","-C",str(root),"rev-parse","--show-toplevel"],
                stderr=subprocess.DEVNULL,text=True,timeout=10).strip()
            tree=subprocess.check_output(
                ["git","-C",str(root),"ls-tree","-rz","--full-tree",source_sha],
                stderr=subprocess.DEVNULL,timeout=10)
        except (subprocess.SubprocessError,FileNotFoundError,OSError):
            raise PackageError("GIT_TREE_UNVERIFIED") from None
        if Path(git_root).resolve()!=root or not isinstance(tree,bytes):
            raise PackageError("GIT_TREE_UNVERIFIED")
        tracked={}
        try:
            for entry in tree.split(b"\0"):
                if not entry:
                    continue
                meta,name=entry.split(b"\t",1)
                mode,kind,object_id=meta.split(b" ",2)
                relative_name=name.decode("utf-8")
                if relative_name in tracked:
                    raise ValueError("duplicate git path")
                tracked[relative_name]=(mode,kind,object_id)
        except (ValueError,UnicodeDecodeError):
            raise PackageError("GIT_TREE_UNVERIFIED") from None
    left=json.loads((root/"plugin.json").read_text(encoding="utf-8"))
    right=json.loads((root/".codex-plugin"/"plugin.json").read_text(encoding="utf-8"))
    if (left.get("name")!="color-team-ops" or left.get("version")!="0.0.2" or
        right.get("name")!=left["name"] or right.get("version")!=left["version"]):
        raise PackageError("CANDIDATE_MANIFEST_IDENTITY_MISMATCH")
    items={}
    total=0
    for path in _paths(root):
        relative=path.relative_to(root).as_posix()
        pure=PurePosixPath(relative)
        probe=root
        for part in pure.parts:
            probe=probe/part
            if probe.is_symlink():
                raise PackageError("MISSING_OR_SYMLINK_SOURCE")
        if not path.is_file() or not path.resolve().is_relative_to(root):
            raise PackageError("MISSING_OR_SYMLINK_SOURCE")
        if (pure.is_absolute() or ".." in pure.parts or "\\" in relative or
            relative in items or relative.startswith(".")):
            # .codex-plugin is explicitly allowed.
            if relative!=".codex-plugin/plugin.json":
                raise PackageError("UNSAFE_PACKAGE_PATH")
        if path.stat().st_size>_MAX_FILE:
            raise PackageError("FILE_TOO_LARGE")
        body=path.read_bytes()
        if tracked is not None:
            git_id=sha1(b"blob "+str(len(body)).encode("ascii")+b"\0"+body).hexdigest().encode("ascii")
            record=tracked.get(relative)
            if (record is None or record[0] not in (b"100644",b"100755")
                or record[1]!=b"blob" or record[2]!=git_id):
                raise PackageError("SOURCE_NOT_IN_PINNED_GIT_TREE")
        total+=len(body)
        if total>_MAX_TOTAL:
            raise PackageError("PACKAGE_TOO_LARGE")
        items[relative]=body
    manifest={
        "schema_version":"cto-v002-package-manifest-1",
        "product":"color-team-ops","version":"0.0.2","source_sha":source_sha,
        "runtime":"portable-markdown-json-only",
        "python_policy_runtime_included":False,
        "files":[{"path":p,"sha256":sha256(data).hexdigest(),"bytes":len(data)}
                 for p,data in sorted(items.items())]
    }
    items["RELEASE-SOURCE-MANIFEST.json"] = (
        json.dumps(manifest,sort_keys=True,indent=2,ensure_ascii=True)+"\n"
    ).encode("utf-8")
    stream=BytesIO()
    with zipfile.ZipFile(stream,"w",compression=zipfile.ZIP_STORED,
                         strict_timestamps=True,allowZip64=False) as archive:
        for p,body in sorted(items.items()):
            info=zipfile.ZipInfo(p,date_time=_FIXED_TIME)
            info.compress_type=zipfile.ZIP_STORED
            info.create_system=3
            info.external_attr=(stat.S_IFREG|0o644)<<16
            archive.writestr(info,body)
    result=stream.getvalue()
    validate_archive(result,source_sha)
    return BuildResult(result,sha256(result).hexdigest(),len(items),source_sha)


def validate_archive(raw: bytes, expected_sha: str) -> None:
    with zipfile.ZipFile(BytesIO(raw)) as z:
        names=z.namelist()
        if len(names)!=len(set(names)) or "RELEASE-SOURCE-MANIFEST.json" not in names:
            raise PackageError("INVALID_ZIP_CONTENTS")
        m=json.loads(z.read("RELEASE-SOURCE-MANIFEST.json"))
        if (m["source_sha"]!=expected_sha or m["version"]!="0.0.2" or
            m["product"]!="color-team-ops" or m["python_policy_runtime_included"] is not False):
            raise PackageError("ZIP_MANIFEST_MISMATCH")
        if set(names)!={row["path"] for row in m["files"]}|{"RELEASE-SOURCE-MANIFEST.json"}:
            raise PackageError("ZIP_FILE_LIST_MISMATCH")
        for row in m["files"]:
            path=row["path"]
            if (PurePosixPath(path).is_absolute() or ".." in PurePosixPath(path).parts
                or sha256(z.read(path)).hexdigest()!=row["sha256"]
                or len(z.read(path))!=row["bytes"]):
                raise PackageError("ZIP_FILE_DIGEST_MISMATCH")


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",type=Path,default=Path.cwd())
    ap.add_argument("--source-sha",required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    a=build(args.root,args.source_sha)
    b=build(args.root,args.source_sha)
    if a.archive!=b.archive or a.sha256_digest!=b.sha256_digest:
        raise PackageError("NONDETERMINISTIC_BUILD")
    args.output.write_bytes(a.archive)
    print("CTO_V002_DETERMINISTIC_ARCHIVE",a.sha256_digest,a.file_count,a.source_sha)


if __name__=="__main__":
    main()
