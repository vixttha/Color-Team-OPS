"""M2: immutable metadata directory for exactly the nine Color Team OPS workers.

An eligible candidate is NOT an authorized assignment. Mission Control, OPS
Director, protected host grants and Verification Gate remain separate.
No repository, provider or local runner connection is made by this module.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Optional
import json
import re

VERSION = "cto-v002-registry-1"
EXPECTED_TEAMS = frozenset((
    "yellow-team", "orange-team", "green-team", "red-team", "blue-team",
    "purple-team", "white-team", "black-team", "gray-cell"
))
_ID = re.compile(r"^[a-z][a-z0-9-]{1,31}$")
_CAP = re.compile(r"^[a-z]+[.][a-z0-9-]+$")
_TAG = re.compile(r"^[a-z0-9-]+$")
_PATH = re.compile(r"^skills/(yellow-team|orange-team|green-team|red-team|blue-team|purple-team|white-team|black-team|gray-cell)/SKILL[.]md$")
_DEFAULT = Path(__file__).resolve().parents[1] / "registry" / "v0.0.2" / "teams.json"

class RegistryRejected(ValueError):
    pass

@dataclass(frozen=True)
class Candidate:
    team_id: str
    capability_id: str
    evidence_expected: str
    required_tools: tuple[str, ...]
    missing_tools: tuple[str, ...]
    playbook_ref: str
    status: str  # CANDIDATE_ONLY or TOOL_ACCESS_UNVERIFIED

@dataclass(frozen=True)
class SearchResult:
    status: str  # CANDIDATES, ABSTAIN, CAPABILITY_BLOCKED
    registry_version: str
    matches: tuple[Candidate, ...]
    reason: str


class TeamDirectory:
    """Read-only. Returned references never cause dispatch or tool authorization."""
    def __init__(self, document: Optional[Mapping] = None):
        if document is None:
            document = json.loads(_DEFAULT.read_text(encoding="utf-8"))
        self._teams = self._validate(document)

    @staticmethod
    def _validate(doc: Mapping) -> tuple[dict, ...]:
        if (not isinstance(doc, dict) or set(doc) != {
                "registry_version", "schema_version", "source_classification", "teams"}
            or doc["registry_version"] != VERSION or type(doc["schema_version"]) is not int or doc["schema_version"] != 1
            or doc["source_classification"] != "development_metadata_not_grants"
            or not isinstance(doc["teams"], list) or len(doc["teams"]) != 9):
            raise RegistryRejected("REGISTRY_VERSION_OR_SHAPE_INVALID")
        ids = [item.get("id") if isinstance(item, dict) else None for item in doc["teams"]]
        if (any(not isinstance(x,str) for x in ids) or set(ids) != EXPECTED_TEAMS\n            or len(ids) != len(set(ids))):
            raise RegistryRejected("TEAM_IDENTITY_SET_MISMATCH")
        all_caps = set()
        result = []
        for item in doc["teams"]:
            if (set(item) != {"id", "name", "focus", "playbook_ref", "capabilities"}
                or any(not isinstance(item[k], str) or not item[k].strip()
                       for k in ("name", "focus", "playbook_ref"))
                or not _PATH.fullmatch(item["playbook_ref"])
                or item["playbook_ref"].split("/")[1] != item["id"]):
                raise RegistryRejected("INVALID_TEAM_METADATA")
            caps = item["capabilities"]
            if not isinstance(caps, list) or not caps or len(caps) > 32:
                raise RegistryRejected("INVALID_CAPABILITIES")
            for cap in caps:
                if not isinstance(cap, dict) or set(cap) != {
                        "id", "tags", "requires_tools", "evidence_expected"}:
                    raise RegistryRejected("INVALID_CAPABILITY_RECORD")
                cid = cap["id"]
                prefix = item["id"].replace("-team", "").replace("gray-cell","gray")
                if (not isinstance(cid, str) or not _CAP.fullmatch(cid)
                    or not cid.startswith(prefix + ".") or cid in all_caps):
                    raise RegistryRejected("CAPABILITY_ID_DUPLICATE_OR_FOREIGN")
                all_caps.add(cid)
                for key in ("tags", "requires_tools"):
                    vals = cap[key]
                    if (not isinstance(vals,list) or (key=="tags" and not vals)
                        or len(vals) > 24 or len(vals) != len(set(str(x) for x in vals))
                        or any(not isinstance(x,str) or not _TAG.fullmatch(x) for x in vals)):
                        raise RegistryRejected("INVALID_TAG_OR_TOOL_REQUIREMENT")
                if (not isinstance(cap["evidence_expected"],str)
                    or not cap["evidence_expected"].strip()):
                    raise RegistryRejected("MISSING_EVIDENCE_EXPECTATION")
            result.append(item)
        return tuple(result)

    def teams(self) -> tuple[str, ...]:
        return tuple(sorted(x["id"] for x in self._teams))

    def playbook_ref(self, team_id: str) -> Optional[str]:
        """Only return one selected file pointer, never preload all specialists."""
        return next((t["playbook_ref"] for t in self._teams if t["id"] == team_id), None)

    def search(self, *, query: str, permitted_teams: tuple[str,...],
               available_tools: Optional[tuple[str,...]] = None,
               required_capabilities: tuple[str,...] = (),
               limit: int = 5) -> SearchResult:
        if (not isinstance(query,str) or not isinstance(permitted_teams,tuple)
            or any(t not in EXPECTED_TEAMS for t in permitted_teams)
            or len(permitted_teams) != len(set(permitted_teams))
            or not isinstance(required_capabilities,tuple)
            or any(not isinstance(x,str) or not _CAP.fullmatch(x) for x in required_capabilities)
            or type(limit) is not int or limit < 1 or limit > 18
            or (available_tools is not None and
                (not isinstance(available_tools,tuple)
                 or any(not isinstance(t,str) or not _TAG.fullmatch(t) for t in available_tools)))):
            raise RegistryRejected("INVALID_SEARCH_SCOPE")
        words = set(re.findall(r"[a-z0-9-]+", query.lower()))
        provided = frozenset(available_tools or ())
        matches = []
        for team in self._teams:
            if team["id"] not in permitted_teams:
                continue
            for cap in team["capabilities"]:
                if required_capabilities and cap["id"] not in required_capabilities:
                    continue
                score = len(words & set(cap["tags"]))
                if not score and not (required_capabilities and cap["id"] in required_capabilities):
                    continue
                missing = tuple(sorted(set(cap["requires_tools"]) - provided))
                item = Candidate(team_id=team["id"],capability_id=cap["id"],
                                 evidence_expected=cap["evidence_expected"],
                                 required_tools=tuple(cap["requires_tools"]),
                                 missing_tools=missing,playbook_ref=team["playbook_ref"],
                                 status="TOOL_ACCESS_UNVERIFIED" if missing else "CANDIDATE_ONLY")
                matches.append((-score, team["id"], cap["id"], item))
        matches.sort(key=lambda x: x[:3])
        selected = tuple(x[3] for x in matches[:limit])
        if not selected:
            return SearchResult("ABSTAIN",VERSION,(),"NO_PERMITTED_MATCH")
        if all(x.missing_tools for x in selected):
            return SearchResult("CAPABILITY_BLOCKED",VERSION,selected,"MISSING_DECLARED_TOOLS")
        return SearchResult("CANDIDATES",VERSION,selected,
                            "METADATA_ONLY_NOT_AUTHORIZATION_OR_DISPATCH")
