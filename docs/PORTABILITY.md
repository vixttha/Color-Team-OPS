# Browser host portability (v0.0.1)

The portable source is **not** a promise that all LLM websites implement identical plugin APIs. Product law L3 requires capability detection and honest degradation.

| Host | v0.0.1 expectations |
| --- | --- |
| chatgpt.com | Portable Agent Plugins skills-only package can be saved through Plugin Creator. User installation/host availability may still be necessary. |
| kimi.ai | Official Kimi help documents plugin Skills/MCP support in selected web modes, and plugin conversion from other platforms. Independent import or conversion is needed; this ChatGPT private plugin is not automatically installed there. |
| z.ai | Web plugin installation and this manifest's compatibility **not verified**. Skill text may be ported only through a documented compatible workflow. |
| grok.com | Web plugin installation and this manifest's compatibility **not verified**. Skill text may be ported only through a documented compatible workflow. |
| Other browser LLMs | Host-specific capability validation required. Unsupported host => CAPABILITY_BLOCKED; never prescribe local setup as mandatory. |

Required capabilities for basic mode: browser access and skill/instruction consumption. Required for cloud repo writes: explicit authorized GitHub/cloud source connector. Required for 24/7 dispatch: separate cloud event runner/database, not in v0.0.1. No client-side agent process, local CI, local SQLite or self-hosted runner required.

References: https://developers.openai.com/plugins/build/plugins and https://www.kimi.ai/help/plugins-and-skills/overview .
