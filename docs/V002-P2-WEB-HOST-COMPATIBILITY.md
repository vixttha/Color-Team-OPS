# P2 — Five browser-host capability audit (2026-11-02)

Owner approved **cloud-only skills-only** initial v0.0.2. No local hardware or provider service is a plugin runtime requirement. All provider results below are **official documentation observations**, NOT installed v0.0.2 mission tests. Source-bound data: [machine matrix](V002-P2-WEB-HOST-COMPATIBILITY.json).

| Host | Web user-supplied skill/plugin pathway | Proven installation of our v0.0.2? | Required caveat |
| --- | --- | --- | --- |
| ChatGPT | Plugin Creator and individually created/uploaded skills, account-dependent | **NO** | Current private canonical plugin remains 0.0.1; no authorized candidate update |
| Claude | Web skill ZIP upload; custom plugins in web paid plans | **NO** | Code execution/skills setting and plan dependent; chat does not run plugin hooks/subagents |
| Grok | Web native Skills and Skill Creator | **NO** | Universal custom 12-skill plugin import/ZIP mapping not confirmed |
| Kimi | Web plugin use with MCP+Skills in supported modes | **NO** | Browser personal plugin creation path not verified; documented Plugin Builder creation depends on Kimi Work desktop |
| Z.ai | ZCode has plugin support | **NO** | ZCode workspace/desktop docs are not evidence that browser chat at z.ai imports user plugins |

## Official sources (documentation support only)

- ChatGPT: https://help.openai.com/en/articles/20001256-plugins-in-chatgpt and https://help.openai.com/en/articles/20001066-skills-in-chatgpt
- Claude: https://support.claude.com/en/articles/12512180-use-skills-in-claude and https://support.claude.com/en/articles/13837440-use-plugins-in-claude
- Grok: https://x.ai/news/grok-skills and https://docs.x.ai/grok/faq
- Kimi: https://www.kimi.com/en/help/plugins-and-skills/overview and https://www.kimi.com/en/help/plugins-and-skills/create
- Z.ai/ZCode: https://zcode.z.ai/en/docs/plugin (**different product surface**)

## Portable source guidance

The installed candidate uses `skills/*/SKILL.md` (nine specialists, three coordinators), with relative references that must fail gracefully if a given host does not load files. Portable source may be adapted into individually imported skills only where the vendor actually supports that capability; a twelve-skill multi-import installer, provider-neutral tool permissions, automatic hooks, cloud global mutex and native cross-host plugin API have **not** been established. The product must remain usable as advice-only bounded logical coordination where tools are absent.

**Developer limitation:** the GitHub reference Python engine and evaluation modules are *not part* of the 32-file installed portable ZIP. No claim that they run in Claude, Grok, Kimi, Z.ai or ChatGPT skill chat. No user-owned compute, paid service or host SDK is necessary.

**Test plan:** H-01–H-11 stay NOT_RUN against actual v0.0.2. A real live candidate must first be lawfully installed/previewed with exact version binding, consent, observed tool traces and separate reviewer evidence. No new plugin identity or canonical 0.0.1 mutation was authorized.

**Yellow Validate:** checked official documents for the five targets. **Orange internal challenge:** document capability is not account entitlement or provider tool grant; ZCode ≠ z.ai chat and Kimi Work desktop ≠ mandatory browser mode. **Head:** source portability researched, host integration still BLOCKED_EXTERNAL_CAPABILITY/REQUIRES_OWNER_AUTHORIZATION.