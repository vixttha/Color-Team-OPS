# P3 — 270 concrete specialist fixture inputs (development-only)

This set supplements, rather than replaces, `candidate-scenarios.json` and `preregistration-draft.json`. It preserves all 270 canonical IDs, nine specialist roles × ten topics × three difficulty bands. For each topic, it supplies a concrete synthetic record/mini-artifact, a different edge probe, a different adversarial probe, a case-specific proposed core finding, required output fields, a proposed prohibited-outcome rubric, a declared permission boundary and reproducible retest steps.

**These are development-authored candidate fixtures.** Their proposed reference findings are NOT independent oracles; keyword matching is not credible competence evaluation. `independent_oracle_count=0`, `actual_host_trial_count=0`. The 54 designated holdouts are only reserved, visible in GitHub and **not blinded**. Future evaluator must generate privately sealed, independently reviewed oracle commitments before accepting holdout scores. For current reusable baseline test work, use only non-holdout indices 01–08 for development; reserve 09–10 from iterative tuning. No generated model response is judged independently by the same model.

## Fields

`fixture.artifact_text` is concrete synthetic domain evidence; `fixture.variant_probe` changes the normal/edge/adversarial task requirements. `task_specific_proposed_oracle` is explicitly unapproved. `measurement.required_output_fields` makes observations parseable but **does not certify semantic correctness**. A real independent reviewer must assess nuanced application security, live threat-intel recency, user-research claims, and engineering correctness. `retest` provides version-bound reproduction steps for the later supported host.

## Source and authority

Baseline source commit: `f1e630205eeba7d9cc1d1957b97e715ad4b2d925`. Historical `candidate-scenarios.json` is preserved. Source ZIP contains only the twelve skills and portable references; these evaluation fixtures and Python evaluation code are developer tooling, never required to run the browser plugin.

**Head → Purple → Validate → logical Auditor → Head:** Source reviewer checks structural completeness and role relevance; logical auditor explicitly rejects labeling model-generated findings as independently verified. P3 remains incomplete until objective oracles are authenticated and expert-held cases genuinely reviewed.
