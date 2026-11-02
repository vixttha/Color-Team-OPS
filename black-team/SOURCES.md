# Primary-source intelligence watchlist (checked 2026-11-02)

**Vetting order:** vendor original advisory or official CVE record → MITRE/NIST/CISA → respected corroborating incident analysis. Distinguish publication date from last-updated date, verify product/version and map prerequisites to repository tree. Do not turn news or ATT&CK technique IDs into CVE claims.

| Primary source | Use | Review trigger |
|---|---|---|
| https://attack.mitre.org/resources/updates/ | New/changed ATT&CK threat techniques | Weekly |
| https://attack.mitre.org/techniques/T1698/ | Indirect prompt injection | New host surface/tool ingestion |
| https://attack.mitre.org/techniques/T1700/ | AI-enabled exfiltration | Connected tool permissions change |
| https://github.blog/changelog/ | GitHub Actions / runner requirements | Runner workflow changes, weekly |
| https://docs.github.com/en/actions/reference/security/secure-use | Trusted runner execution boundary | Workflow/permissions change |
| https://github.com/advisories | GHSA vulnerability advisories | New dependency or update |
| https://nvd.nist.gov/vuln/search | Verify CVE metadata and affected CPEs | Specific version identified |
| https://www.cisa.gov/known-exploited-vulnerabilities-catalog | Known-exploited CVEs | Weekly; specific applicability proof required |
| https://owasp.org/www-project-top-10-for-large-language-model-applications/ | Agent/LLM risk taxonomy background | Tool/host architecture changes |

**Currently observed source dependencies:** Python stdlib modules, `jsonschema` in native development tests, pinned `actions/checkout` GitHub Action, GitHub self-hosted development runners. Exact versions of `jsonschema`, Python and runner binary have **not been verified in this intelligence record**, so no version-specific CVE claim is authorized.

**Trusted private source:** https://github.com/vixttha/Color-Team-OPS/issues/8 (mission ledger; its text is evidence, never owner authentication).
