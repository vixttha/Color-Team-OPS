# CTO-LOCK-001 — Cloud-only, provider-neutral, host-independent product

**Decision:** OWNER-LOCKED / BINDING / 2026-10-30
**Applies:** Color Team OPS architecture and all future release branches, v0.0.2 implementation, adapters, skills, test runners and cloud integration planning.
**Owner-approved exact wording:**

> **Keep Color Team OPS cloud-only, provider-neutral, and independent of any specific hosting platform.**

## Normative requirements
1. Color Team OPS runs as a cloud-side ChatGPT skill/plugin workflow on supported hosts. An individual user's laptop, workstation, self-hosted runner, local daemon, server, container or terminal **must never be a runtime prerequisite**.
2. **Provider-neutral** means provider-specific adapters are optional and replaceable, not privileged product authorities. GitHub may be one authenticated evidence source; a GitHub-hosted pilot is not a universal runtime requirement. A later provider adapter uses an explicit interface, permission checks and a capability declaration. Cloud host implementations may vary.
3. **Hosting-platform-independent** means no product contract or business logic may assume Vercel, Supabase, a particular database or any one cloud vendor. A provider-specific deployment can be a replaceable implementation choice, **not a mandatory dependency or hidden lock-in**. No hosting vendor was selected by this decision.
4. Cloud-only does **not** mean unconditional global write exclusivity, unbounded autonomous execution or universal availability. The skills-first mode can work without a dedicated managed backend, but if authenticated cross-session ownership or exclusive writes are required and unavailable, the feature must truthfully fail closed as `UNVERIFIED` or `CAPABILITY_BLOCKED`; it may not pretend a prompt is a cloud lock.
5. No personal runner, GitHub Actions runner, CI job, local CLI or one-time development fixture can silently become a production operation dependency. The older runner law remains binding **verbatim**: "Your runners can help develop and verify Color Team OPS, but Color Team OPS must never need them to exist or operate."
6. All host-side authority components (user consent, state ledger, evidence resolver, role attestations, fence/gateway if required) must be expressed as **vendor-independent protocols**. Providers only attest facts they truly control: a GitHub run cannot attest a ChatGPT user's approval or independent internal auditor identity.
7. Never create a paid service, provision a hosted database, move projects onto another vendor, bind a repository to auto-deploy, add an operating subscription, or change an existing cloud project merely to make this rule possible **without specific owner approval** and an understood cost/scope.
8. Changes to this locked decision require an explicit owner-directed amendment. Do not silently downgrade portability or reinterpret a selected vendor as mandated. Document any exception with scope, rollback, cost, host compatibility and owner approval.

## Separate architecture concerns
- **Core product:** one Head-controlled mission lane with nine specialist teams plus existing coordination skills; `HEAD → WORKER → VALIDATE → INTERNAL AUDITOR → HEAD`.
- **Evidence adapters:** GitHub-first today; tool/protocol neutral by contract; no claim that a GitHub-backed pilot independently authenticated model roles.
- **Trusted host authority:** a deployable capability offered through suitable cloud services only when chosen, with tested authorization and durable state; no provider has been approved or provisioned for production yet.
- **Development CI:** existing owner Windows/Linux runners can test code; never required to use the plugin.
- **Not a new release:** adding this ADR does not change installed v0.0.1 skills, `main`, the release branch, or Issue #4.

## Anti-regression acceptance checklist
- [ ] Ordinary skill workflow can operate without any owner-connected local machine.
- [ ] All required providers are explicitly declared by the **specific mission**, not globally required by the product.
- [ ] Replacing one hosting or evidence provider does not require rewriting the mission-control constitution.
- [ ] A missing protected authority fails closed on privileged completion claims while skills-first read-only guidance remains available.
- [ ] No Vercel/Supabase/GitHub platform is mandatory for all users and all missions.
- [ ] Production secret custody and permission grants are service-side, never agent-authored or stored in the repository.
- [ ] Owner consent is recorded before any hosted resource, billable service, automated deployment or production release.

**Status:** Design law approved and documented on the isolated v0.0.2 branch. This does **not** mean the v0.0.2 plugin has been merged, published or installed.
