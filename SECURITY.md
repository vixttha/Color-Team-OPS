# Security

Early-stage private skills-only plugin; not an independently verified scanner, managed SOC, or autonomous agent runtime.

Report security issues privately to the repository owner through a private GitHub channel. Do not paste credentials, private customer data, or exploit material into public issues. Test only explicitly authorized targets.

The v0.0.1 development/test workflow uses the owner's explicitly authorized Windows and Linux GitHub runners on a controlled release branch only, with read-only permissions, no secrets and no untrusted PR trigger. These runners are never part of installed-plugin operations. The assistant performs the requested audit; do not call it an independent outside sign-off. Record actual exact-SHA test evidence.

See [Constitution](docs/CONSTITUTION.md) and [locked runner policy](docs/design/RUNNER-POLICY.md).
