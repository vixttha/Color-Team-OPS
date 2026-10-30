# ADR-0003 — Canonical plugin identity and retirement discipline

**Status:** ACCEPTED — v0.0.1 repository hygiene rule  
**Date:** 2026-10-29  
**Owner's request:** Prevent a repeat of duplicate private plugins or accidental version advancement.

## Binding single-canonical-identity policy

**The sole canonical Color Team OPS private ChatGPT plugin is `plugins_6ae3edf1ea4c819182f275592273e2cc`.** Its v0.0.1 release is `pluginrel_6ae3edf2a4ec8191b5cf9c92c317db22`.

The original `plugins_6ae3ccf13f548191bdcba269f33085d3` is **SUPERSEDED BUT STILL INSTALLED**. It is not retired or uninstalled. Never describe it as removed without successful backend removal evidence. No source file or GitHub branch change can uninstall it.

The machine-readable [plugin identity registry](../PLUGIN-RELEASE-REGISTRY.json) is the release ledger, and the README must link to the canonical plugin.

## Future upgrade sequence

1. Read the identity registry and **both the live Plugin Creator release and installed skill state** before making changes. Check the existing plugin ID, current release ID, version and supported update semantics.
2. Prefer updating the **same canonical plugin ID**, not creating a duplicate with the same title and version. Prepare the exact-source ZIP and verify it twice.
3. Never allow implicit SemVer increments. If Plugin Creator will auto-bump `0.0.1` to `0.0.2` or does not support an in-place v0.0.1 correction, **stop and report the constraint**. Do not create another `0.0.1` plugin as a workaround without explicit owner approval of replacement plus retirement handling.
4. Compare all installed portable files with approved exact GitHub SHA; allow only documented platform-generated compatibility files and explicitly approved package README differences. Check twelve skills and their cloud-only law.
5. Record the plugin ID, release ID, exact source SHA, package digest, GitHub runner test URLs, version, author audit and outstanding host acceptance limitations in README, CHANGELOG and evidence records.
6. If replacement is explicitly approved, mark the old ID `superseded_still_installed` until an **explicit owner-approved uninstall action** succeeds and the old ID is no longer reported as available. Only then set `retired_uninstalled`.
7. Keep only one `canonical` entry. Fail closed when two candidates share the same name/version, the registry disagrees with the installed product, an old plugin has unknown state, or the correct tool operation is unavailable.

## Hard boundary

This document concerns **release-management bookkeeping only**. GitHub development runners may test and audit but must never be required for the plugin, autonomous cloud operations, or a backend.

> Your runners can help develop and verify Color Team OPS, but Color Team OPS must never need them to exist or operate.

## Limits of enforcement

Repository tests validate the registry and its references; they **cannot** by themselves stop Plugin Creator from creating a second private plugin. Every creation/update/uninstall must therefore be preceded by checking the live Plugin Creator identity and version and receiving whatever owner authorization is required.
