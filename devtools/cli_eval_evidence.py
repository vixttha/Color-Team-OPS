"""Local-only evidence transfer. Integrity hashes are NOT provider attestation."""
import argparse
from pathlib import Path, PurePosixPath
import json
import re
import zipfile

from devtools.cli_eval import digest, encode, require

MAX_FILE = 32*1024*1024
MAX_TOTAL = 512*1024*1024


def export(source, destination):
    source=Path(source).resolve()
    destination=Path(destination).resolve()
    require(source.is_dir() and not destination.exists(), 'SOURCE_OR_DESTINATION_INVALID')
    require(not destination.is_relative_to(source), 'ARCHIVE_INSIDE_SOURCE')
    files={}
    total=0
    for p in sorted(source.rglob('*')):
        require(not p.is_symlink(), 'SYMLINK_REJECTED')
        if p.is_file():
            require(p.stat().st_size <= MAX_FILE, 'FILE_TOO_LARGE')
            data=p.read_bytes()
            total+=len(data)
            require(total <= MAX_TOTAL, 'ARCHIVE_TOO_LARGE')
            files[p.relative_to(source).as_posix()]=data
    index={name:{'sha256':digest(data),'bytes':len(data)} for name,data in files.items()}
    require('INDEX.json' not in files, 'RESERVED_INDEX_NAME')
    with zipfile.ZipFile(destination,'x',compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('INDEX.json',encode(index))
        for name,data in files.items(): z.writestr(name,data)
    return {'archive_sha256':digest(destination.read_bytes()),'index_sha256':digest(index),'files':len(files)}


def import_archive(source, destination, expected_archive_sha256):
    source=Path(source)
    destination=Path(destination).resolve()
    require(source.stat().st_size <= MAX_TOTAL, 'ARCHIVE_TOO_LARGE')
    require(digest(source.read_bytes()) == expected_archive_sha256, 'ARCHIVE_DIGEST_MISMATCH')
    require(not destination.exists(), 'DESTINATION_ALREADY_EXISTS')
    with zipfile.ZipFile(source) as z:
        names=z.namelist()
        require(len(names) == len(set(names)) and 'INDEX.json' in names, 'DUPLICATE_OR_MISSING_INDEX')
        require(sum(i.file_size for i in z.infolist()) <= MAX_TOTAL, 'ARCHIVE_TOO_LARGE')
        for i in z.infolist():
            p=PurePosixPath(i.filename)
            require(p.parts and all(re.fullmatch(r'[A-Za-z0-9_.-]+',part) and
                    not part.endswith('.') and not re.fullmatch(r'(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])',part.split('.')[0],re.I)
                    for part in p.parts) and
                    not p.is_absolute() and '..' not in p.parts and ':' not in i.filename and
                    '\\' not in i.filename and p.as_posix() == i.filename and
                    i.file_size <= MAX_FILE and not i.is_dir(), 'UNSAFE_ARCHIVE_MEMBER')
            require((i.external_attr >> 16) & 0o170000 != 0o120000, 'SYMLINK_REJECTED')
        index=json.loads(z.read('INDEX.json'))
        require(set(index) == set(names)-{'INDEX.json'}, 'INDEX_MEMBERS_MISMATCH')
        contents={n:z.read(n) for n in index}
        for n,data in contents.items():
            require(index[n] == {'sha256':digest(data),'bytes':len(data)}, 'EVIDENCE_HASH_MISMATCH')
    destination.mkdir()
    for n,data in contents.items():
        target=destination/n
        target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('xb') as out: out.write(data)
    return {'files':len(contents),'index_sha256':digest(index)}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['export','import'])
    p.add_argument('--source',required=True,type=Path)
    p.add_argument('--destination',required=True,type=Path)
    p.add_argument('--expected-archive-sha256')
    a=p.parse_args()
    result=export(a.source,a.destination) if a.action=='export' else import_archive(a.source,a.destination,a.expected_archive_sha256)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
