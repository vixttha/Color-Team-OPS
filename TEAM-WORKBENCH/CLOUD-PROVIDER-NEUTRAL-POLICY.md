# YELLOW engineering policy — PrismCell cloud-only, provider-neutral runtime

**Owner decision implemented for Yellow's workcell:** PrismCell remains separate from Color-Team-OPS plugin, Development HQ and Purple Review HQ. No required local compute or specific cloud vendor is permitted in the product runtime.

## Non-negotiable boundaries

1. PrismCell retains nine independent **workspaces**, with at most **one active worker** under Head-controlled `Head → Worker → Validate → logical Internal Auditor → Head`. The workspaces alone are not nine independent authenticated AI principals.
2. GitHub repository/issue adapters may provide durable cloud evidence and source control. Their use does not require GitHub Actions as an execution runtime. The execution engine, scheduler and state-lease abstractions must be configurable across supported cloud providers. No Vercel-specific imports, `api/` layout, `vercel.json`, Vercel project ID, or required Vercel service in the canonical template.
3. The owner’s two self-hosted runners `color-team-ops-linux-01`, `color-team-ops-windows-01` are **optional development-test devices only**, never an installed agent/plugin production dependency. Do not use paid GitHub-hosted runner jobs. A successful test is SHA-bound evidence, not a host security attestation.
4. A real automatic processor must have trusted provider-authenticated receipts, explicit team-to-credential mapping, deny-by-default per-branch capability scopes, replay-resistant durable ledger, provider-side optimistic concurrency, lease fencing, safe recovery, provable Head authorization, and an external acceptance audit.
5. Untrusted INCALL text/issue comments cannot approve itself or grant authority, modify another team's branch, create cloud resources, pay for compute, or authorize product release.
6. Do not merge the frozen `feature/prismcell-cloud-control-gated` branch into the template or product. Audit-only security source/test concepts may be studied as input but must be rewritten/validated against the provider-neutral interfaces before any promotion.
7. Avoid deleting historical GitHub staging evidence or external cloud projects without distinct owner approval. *Stop development* and *delete the externally hosted service* are different actions.

## Status

- Current nine team workcells are **READY_ON_INVOCATION** and do not run unattended.
- Owner-runner PrismCell test workflow is `.github/workflows/prismcell-owner-selfhosted-validation.yml` on Yellow's home branch, exact PrismCell template pin `25d59530210949792b3ce47ac0a804442997a9b1`.
- No certified independent role authentication, branch ACL or autonomous cloud-execution service is part of this policy. Those remain separate implementation and acceptance requirements.
