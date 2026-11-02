# Optional P2 web skill-source export (NOT plugin installation)

`devtools/export_v002_web_skills.py` can create twelve **individual skill-folder ZIP candidates**, in memory, from the approved source tree. Each includes its SKILL.md, constitution, portable schemas, registry and the matching reference for nine specialists. No new team or coordinator is generated. All paths are copied from checked source and exports use deterministic ZIP metadata.

This is an **optional development exporter**; browser product runtime never calls it. The export format follows the basic skill-folder ZIP concept described by Claude's [custom skills documentation](https://support.claude.com/en/articles/12512180-use-skills-in-claude), but this has **NOT** been uploaded to or accepted by any Claude account. Host may reject extra resources, have account-specific limits or route twelve individually uploaded skills differently. It does not certify product compatibility.

Invoke only in an already-authorized development workspace with an exact source SHA and optional `--out`; the user does **not** need local Python, a machine or any owner self-hosted runner for the plugin itself. The original ChatGPT 32-file source ZIP remains the canonical unpublished candidate for v0.0.2.

No code path updates Plugin Creator, creates a staging identity, touches GitHub main or deploys a service. Do not treat exported ZIPs as installed or tested H-01–H-11 missions.