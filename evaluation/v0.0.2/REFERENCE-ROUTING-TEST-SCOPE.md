# P4 — 270 genuine source-code router checks (not model trials)

The development test module `tests/test_v002_p4_270_reference_routes.py` dynamically registers one actual Python unittest method for each of the 270 concrete candidate case IDs. Each executes `policy_v002.route_advice.recommend_one` against the canonical M2 directory and tests source SHA stale blocking, active-Worker exclusivity, handoff budget and tool-missing handling.

**Measurement scope:** these checks exercise actual Python reference routing and trust boundaries on synthetic data. They DO NOT infer the intended team independently: the test seeds the required capability and eligible team from the canonical registry. Thus, `270/270` passing would be a **source routing contract/guard PASS**, **not** measured team-selection accuracy or specialist competence. No web host model is invoked, no candidate version installed and no reviewer oracle independently authenticated.

**P4 measured real specialist trials remain 0.** The source checks are a valuable deterministic regression for all 270 IDs and five guard paths; they do not satisfy independent host performance gates. The scoring pipeline `policy_v002/eval_trial_pipeline.py` remains proof-adapter guarded.
