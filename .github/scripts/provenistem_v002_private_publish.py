#!/usr/bin/env python3
"""Private package-only Provenistem v0.0.2 publication; explicit one-shot owner arm.

Creates only a Git tag and private GitHub Release at the exact audited
24-file package SHA. Does not merge, edit repositories, sync adopters,
operate Governance, or change the Color-Team-OPS main branch.

Requires GitHub Actions GITHUB_TOKEN with contents:write. Token is never logged.
"""
import json
import os
import urllib.error
import urllib.request

REPOSITORY = "vixttha/Color-Team-OPS"
TAG = "provenistem-v0.0.2"
PACKAGE_SHA = "77e33e7e82ab6d1accc5b331ce2c5b5408db75d2"

RELEASE_NOTES = """# Provenistem v0.0.2

**The living record of a project's possibilities.**

This is the **private, package-only** release of Provenistem, a portable
and optional Ideas + Features library. It is **not** a Color-Team-OPS
product release, Governance-Branch release, Governance runtime dependency,
or a merge into an adopter repository.

## Included
- Two separate project-owned canonical JSON record libraries: Ideas and Features
- Stable local IDs, independently tracked lifecycle, implementation, and testing states
- Explicit human decision metadata and checkable (not automatically authenticated) evidence references
- Read-only indexes, deterministic standard-library Python validation, and no-clobber adopter planning
- Hard-stop \`NAMESPACE_COLLISION\` for recognized Governance-owned catalog layouts
- Bounded JSON parsing, JSON Schema subset checks, defensive filesystem preflights
- Five portable offline regression suites and a human/LLM reader guide

**Exactly 24 portable files**; zero project-specific canonical records;
no GitHub Actions workflows, runner credentials, upstream Governance files,
or runtime/cloud dependencies. Adopters keep their own schemas, records,
instructions, approvals, and product-release authority.

## Acceptance evidence (exact SHA)
- Source: [run 43126348560](https://github.com/vixttha/Color-Team-OPS/actions/runs/43126348560),
  49/49 Linux and 49/49 Windows, at \`21d6cc4b07bdbb4895445940e3ccf29a09209e9f\`.
- MONDEX: [run 43126846929](https://github.com/vixttha/MONDEX/actions/runs/43126846929),
  50/50 Linux and Windows, original 20 ideas / 27 features preserved,
  at \`78abeb7a0fb848014e42ac94924c5c73913f06a4\`.
- D-D-World: [run 43128853103](https://github.com/vixttha/D-D-World/actions/runs/43128853103),
  42/42 Linux and Windows, all protected host object hashes preserved,
  at \`1aea4bb46cc758ffbb180a0a14c5533bc4bf6d8b\`.
- Clean standalone 24-file package (before documentation-only branding):
  [run 43137997324](https://github.com/vixttha/Color-Team-OPS/actions/runs/43137997324),
  48/48 clean and 48/48 populated fresh-host tests on both OSs,
  at package \`a3fdbcbc36632146ef6be6fbec68d60be50c3e85\`.
- Provenistem-branded release retains the **identical tools, tests, JSON schemas,
  examples and record placeholders**. Only human-readable Markdown changed;
  the one-shot publication gate rechecks that branded package before release.

## Boundaries
Use a no-clobber, project-owned adoption procedure. An idea is not authority;
a feature record does not prove a shipment; evidence references are not
authentication. The library never adds itself to, modifies, or makes
Governance-Branch depend on Provenistem. Its validation is not a security
sandbox or an independent audit.

External independent review was waived for this internal one-lane acceptance;
the reported scripted audits are not external certification.

**Private distribution:** access is limited to readers of the private
\`vixttha/Color-Team-OPS\` repository. No public redistribution license is
granted by this release. The version number belongs to Provenistem, not
the host's product version.

**Tag target (exact 24-file branded package):**
\`77e33e7e82ab6d1accc5b331ce2c5b5408db75d2\`.
"""


def call(method, endpoint, payload=None, missing_ok=False):
    token = os.environ.get("GH_RELEASE_TOKEN")
    if not token:
        raise RuntimeError("GitHub token unavailable (contents:write required)")
    url = "https://api.github.com/repos/" + REPOSITORY + endpoint
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        url, data=body, method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": "Bearer " + token,
            "User-Agent": "Provenistem-v002-private-publisher",
            **({"Content-Type": "application/json"} if body is not None else {}),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        if missing_ok and error.code == 404:
            return None
        # Do not echo authorization headers or full remote response.
        raise RuntimeError(
            "GitHub API call failed: method=" + method +
            ", endpoint=" + endpoint.split("?")[0] +
            ", HTTP=" + str(error.code)
        ) from None


def main():
    assert os.environ.get("GITHUB_REPOSITORY") == REPOSITORY
    assert os.environ.get("GITHUB_ACTOR") == "vixttha"
    assert os.environ.get("GITHUB_REF") == (
        "refs/heads/idea-feature-library-v0.0.2"
    )
    existing = call("GET", "/git/ref/tags/" + TAG, missing_ok=True)
    release = call("GET", "/releases/tags/" + TAG, missing_ok=True)
    if existing is not None:
        assert existing["object"]["type"] == "commit"
        assert existing["object"]["sha"] == PACKAGE_SHA, (
            "Tag collision: existing ref does not point to approved package!"
        )
    if release is not None:
        assert existing is not None and release["tag_name"] == TAG
        assert release["name"] == "Provenistem v0.0.2"
        assert not release["draft"] and not release["prerelease"]
        print("PROVENISTEM_ALREADY_PUBLISHED_VERIFIED", release["html_url"])
        return
    if existing is None:
        result = call("POST", "/git/refs", {
            "ref": "refs/tags/" + TAG,
            "sha": PACKAGE_SHA,
        })
        assert result["object"]["type"] == "commit"
        assert result["object"]["sha"] == PACKAGE_SHA
        print("PROVENISTEM_TAG_CREATED", TAG, PACKAGE_SHA, flush=True)
    result = call("POST", "/releases", {
        "tag_name": TAG,
        "target_commitish": PACKAGE_SHA,
        "name": "Provenistem v0.0.2",
        "body": RELEASE_NOTES,
        "draft": False,
        "prerelease": False,
        "generate_release_notes": False,
        "make_latest": "false",
    })
    assert result["tag_name"] == TAG
    assert result["name"] == "Provenistem v0.0.2"
    assert not result["draft"] and not result["prerelease"]
    # Verify both published release and immutable target ref via the GitHub API.
    ref = call("GET", "/git/ref/tags/" + TAG)
    published = call("GET", "/releases/tags/" + TAG)
    assert ref["object"]["type"] == "commit"
    assert ref["object"]["sha"] == PACKAGE_SHA
    assert published["id"] == result["id"]
    assert published["tag_name"] == TAG
    assert not published["draft"] and not published["prerelease"]
    print("PROVENISTEM_V002_PRIVATE_RELEASE_PASS", published["html_url"],
          "target=", PACKAGE_SHA, flush=True)


if __name__ == "__main__":
    main()
