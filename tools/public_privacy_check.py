#!/usr/bin/env python3
"""Aggregate-only detection; never print matching values or paths."""
import argparse
import json
import os
import re
import subprocess

EMAIL = re.compile(r"(?i)[a-z0-9._%+-]+@(?:[a-z0-9-]+\.)+[a-z]{2,}")
HOME = re.compile(r"(?i)(?:[a-z]:[\\/]users[\\/]|/home/|/Users/)[\w.-]+")
PRIVATE_CONTEXT = re.compile(r"(?i)\b(?:solo[- ]developer|my personal (?:email|address|account))\b")
SAFE_DOMAINS = {"example.com", "example.org", "example.net", "example.test", "sample.invalid", "users.noreply.github.com", "noreply.github.com"}
def flags(text, terms=()):
    result = set()
    if any(x.rsplit("@", 1)[1].lower() not in SAFE_DOMAINS for x in EMAIL.findall(text)):
        result.add("email")
    if HOME.search(text):
        result.add("home_path")
    if PRIVATE_CONTEXT.search(text):
        result.add("personal_context")
    if any(term.casefold() in text.casefold() for term in terms):
        result.add("private_term")
    return result

def git(*args):
    return subprocess.check_output(["git", *args], stderr=subprocess.DEVNULL)

def scan():
    terms = [x.strip() for x in os.environ.get("PRIVACY_PRIVATE_TERMS", "").splitlines() if x.strip()]
    ids = git("rev-list", "--objects", "--all", "--no-object-names")
    rows = subprocess.check_output(["git", "cat-file", "--batch-check"], input=ids).splitlines()
    counts = {"objects_checked": 0, "binary_skipped": 0, "oversize_skipped": 0, "objects_flagged": 0, "email": 0, "home_path": 0, "personal_context": 0, "private_term": 0}
    for row in rows:
        oid, kind, size = row.split()
        if kind not in (b"blob", b"commit", b"tag", b"tree"):
            raise RuntimeError("Unexpected object type")
        if int(size) > 2_000_000:
            counts["oversize_skipped"] += 1
            continue
        data = git("cat-file", "-p", oid.decode("ascii"))
        if b"\0" in data:
            counts["binary_skipped"] += 1
            continue
        try:
            value = data.decode("utf-8")
        except UnicodeDecodeError:
            counts["binary_skipped"] += 1
            continue
        counts["objects_checked"] += 1
        found = flags(value, terms)
        counts["objects_flagged"] += bool(found)
        for category in found:
            counts[category] += 1
    print(json.dumps({"private_terms_configured": bool(terms), **counts}, sort_keys=True))
    return int(bool(counts["objects_flagged"] or counts["oversize_skipped"] or counts["binary_skipped"] or not terms))

def self_test():
    assert flags("contact@" + "synthetic-check.test") == {"email"}
    assert not flags("contact@example.com")
    assert not flags("123+example@users.noreply.github.com")
    assert flags("/" + "home/" + "synthetic-user") == {"home_path"}
    assert flags("solo" + " developer") == {"personal_context"}
    assert flags("SYNTHETIC MARKER", ["synthetic marker"]) == {"private_term"}
    print("6 synthetic privacy checks passed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        raise SystemExit(scan())
