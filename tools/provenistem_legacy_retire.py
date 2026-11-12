"""Retire the historical Color-Team-OPS Provenistem GitHub Release metadata.

Preserves original tag, commit, evidence URL and published release. No files,
branches, adopters, Governance state or release status are moved/deleted.
"""
import json
import os
import urllib.error
import urllib.request

REPO = "vixttha/Color-Team-OPS"
TAG = "provenistem-v0.0.2"
ORIGINAL_SHA = "77e33e7e82ab6d1accc5b331ce2c5b5408db75d2"
RELEASE_ID = 442469998
NEW_HOME = "https://github.com/vixttha/Governance-Branch-Bible/releases/tag/provenistem-v0.0.2"
MOVED_NAME = "HISTORICAL — Provenistem v0.0.2 (moved to Governance-Branch-Bible)"
NOTICE = (
    "> **HISTORICAL / RELOCATED — not the authoritative Provenistem release.**\n"
    "> Provenistem now belongs to Governance-Branch-Bible. The verified,\n"
    "> package-only v0.0.2 release is " + NEW_HOME + ".\n"
    "> This original release, tag, Git commit and tests are retained as\n"
    "> immutable development provenance; no future changes occur here.\n\n"
)

def api(method, endpoint, body=None):
    token = os.environ["GH_RELEASE_TOKEN"]
    url = "https://api.github.com/repos/" + REPO + endpoint
    req = urllib.request.Request(
        url, method=method,
        data=None if body is None else json.dumps(body).encode("utf-8"),
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "Provenistem-historical-relocation",
            "Authorization": "Bearer " + token,
            **({"Content-Type": "application/json"} if body is not None else {}),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            return json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(
            "GitHub release retirement HTTP " + str(exc.code) +
            " at " + endpoint
        ) from None

def main():
    assert os.getenv("GITHUB_REPOSITORY") == REPO
    assert os.getenv("GITHUB_ACTOR") == "vixttha"
    assert os.getenv("GITHUB_REF") == "refs/heads/idea-feature-library-v0.0.2"
    ref = api("GET", "/git/ref/tags/" + TAG)
    assert ref["object"]["type"] == "commit"
    assert ref["object"]["sha"] == ORIGINAL_SHA
    release = api("GET", "/releases/tags/" + TAG)
    assert release["id"] == RELEASE_ID and release["tag_name"] == TAG
    assert not release["draft"]
    if release["name"] != MOVED_NAME or not release["body"].startswith(NOTICE):
        original_body = release["body"] or ""
        if original_body.startswith(NOTICE):
            original_body = original_body[len(NOTICE):]
        updated = api("PATCH", "/releases/" + str(RELEASE_ID), {
            "name": MOVED_NAME,
            "body": NOTICE + original_body,
            "make_latest": "false",
        })
        assert updated["id"] == RELEASE_ID
    again = api("GET", "/releases/tags/" + TAG)
    pinned = api("GET", "/git/ref/tags/" + TAG)
    assert again["name"] == MOVED_NAME
    assert again["body"].startswith(NOTICE)
    assert again["tag_name"] == TAG and not again["draft"]
    assert pinned["object"]["sha"] == ORIGINAL_SHA
    print("COLOR_OPS_PROVENISTEM_LEGACY_RELEASE_RETIRED_PASS",
          again["html_url"], "historical_tag=", ORIGINAL_SHA)

if __name__ == "__main__":
    main()
