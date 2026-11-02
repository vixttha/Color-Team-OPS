"""Optional SOURCE-ONLY exporter for individual web skill ZIP candidates.

Development/release helper, not installed plugin runtime and not a universal
installer. In particular this does not install a skill in Claude or any host.
"""
from __future__ import annotations
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import argparse
import re
import stat
import zipfile

SKILLS=("yellow-team","orange-team","green-team","red-team","blue-team",
        "purple-team","white-team","black-team","gray-cell",
        "mission-control","ops-director","verification-gate")
SPECIALISTS=frozenset(SKILLS[:9])
_SOURCE_SHA=re.compile(r"^[a-f0-9]{40}$")
_FIXED=(1980,1,1,0,0,0)


def export_skill(root: Path, skill: str, source_sha: str) -> tuple[bytes,str]:
    """Return portable single-skill archive bytes and digest without writing files."""
    if skill not in SKILLS or not isinstance(source_sha,str) or not _SOURCE_SHA.fullmatch(source_sha):
        raise ValueError("INVALID_SKILL_OR_SOURCE_SHA")
    root=Path(root).resolve()
    sources={"SKILL.md":root/"skills"/skill/"SKILL.md",
             "docs/CONSTITUTION.md":root/"docs"/"CONSTITUTION.md",
             "registry/v0.0.2/teams.json":root/"registry"/"v0.0.2"/"teams.json"}
    if skill in SPECIALISTS:
        sources["references/v002-competencies.md"]=(
            root/"skills"/skill/"references"/"v002-competencies.md")
    for p in sorted((root/"schemas").glob("*.json")):
        sources["schemas/"+p.name]=p
    if len([x for x in sources if x.startswith("schemas/")])!=3:
        raise ValueError("REQUIRED_SCHEMAS_MISSING")
    outputs={}
    for name,src in sources.items():
        if not src.is_file() or not src.resolve().is_relative_to(root):
            raise ValueError("SKILL_SOURCE_UNAVAILABLE")
        for parent in (src,*src.parents):
            if parent==root.parent:
                break
            if parent.is_symlink():
                raise ValueError("SYMLINK_NOT_ALLOWED")
        body=src.read_bytes()
        if len(body)>4*1024*1024:
            raise ValueError("SOURCE_TOO_LARGE")
        outputs[skill+"/"+name]=body
    buff=BytesIO()
    with zipfile.ZipFile(buff,"w",compression=zipfile.ZIP_STORED,allowZip64=False) as z:
        for name in sorted(outputs):
            info=zipfile.ZipInfo(name,date_time=_FIXED)
            info.compress_type=zipfile.ZIP_STORED
            info.create_system=3
            info.external_attr=(stat.S_IFREG|0o644)<<16
            z.writestr(info,outputs[name])
    data=buff.getvalue()
    return data,sha256(data).hexdigest()


def main():
    p=argparse.ArgumentParser(description="OPTIONAL individual skills ZIPs, not installed host proof")
    p.add_argument("--root",type=Path,required=True)
    p.add_argument("--source-sha",required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    for skill in SKILLS:
        data,digest=export_skill(args.root,skill,args.source_sha)
        path=args.out/(skill+".zip")
        path.write_bytes(data)
        print(skill,digest,len(data),"SOURCE_EXPORT_NOT_INSTALLED")
if __name__=="__main__":main()
