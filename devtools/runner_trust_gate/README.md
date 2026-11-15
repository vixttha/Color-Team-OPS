# Runner trust gate — isolated build candidate

Development-only candidate. **Does not run on the Color Team OPS skills-only plugin.**

`admission.py` receives the GitHub pre-job environment and validates an *administrator-provisioned* exact-job permit stored outside the repository. Missing, stale or malformed permits fail closed. Linux template has a bounded timeout. Windows template also implements an external timeout and preliminary protected ACL checks, but has **not** passed native Windows acceptance. There is **no runtime auto-installer, workflow trigger, owner approval minting endpoint or runner dispatch** in this package.

The original historical v0.2 runner-gate ZIP is NOT embedded or replaced; see `docs/CTO-RUNNER-GATE-ISOLATED-BUILD.md` for provenance, gaps, installation prerequisites and acceptance criteria.

Offline unit tests only:

```sh
python -B -m unittest discover -s tests -p 'test_runner_trust_gate.py' -v
```

Installing this into a runner requires a separate *owner-admin controlled* review, OS ACL/permission hardening and real negative/positive pre-job tests. **Do not set `ACTIONS_RUNNER_HOOK_JOB_STARTED` to a repository checkout file.**