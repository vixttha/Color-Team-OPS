# Portable Idea + Feature Library v0.0.1 — independent template

This subdirectory is a self-contained, blank, optional **two-library** template suitable for copying to an unrelated project. The original Color-Team-OPS 36 ideas and 5 feature candidates are intentionally **not present**.

**Human-only:** copy the `ideas/`, `features/`, `templates/` and `LIBRARY-AGENT-GUIDE.md` paths into a project only when those target paths are unused. Never overwrite `AGENTS.md`, a host's policies or an existing library. Use the [adoption guide](docs/ADOPTION.md).

**Optional safe-copy helper if Python happens to be available:**

```sh
python tools/adopt.py /path/to/existing/unrelated-project
python tools/adopt.py /path/to/existing/unrelated-project --with-tools
```

Use only *one* command per destination; re-running fails safely rather than replacing files. The first command copies the two libraries, templates and agent guide. The second adds optional developer tools, tests, docs but also refuses occupied paths. The file-copy process is not a transaction in the presence of concurrent external writers; a failed operation may require manual inspection of partial outputs.

For a developer who opted in to the helpers:

```sh
python tools/library.py check
python tools/library.py build
python -m unittest discover -s tests -v
```

No network access, plugin, hosted account, local runner or package installation is required for manual use. The optional checker does not authenticate evidence, release decisions or human authorization.

[Schema profile mapping](../../docs/SCHEMA-PROFILES-AND-COMPATIBILITY.md) is provided in the *source Purple branch*; the copied standalone template does not depend on that source repository.
