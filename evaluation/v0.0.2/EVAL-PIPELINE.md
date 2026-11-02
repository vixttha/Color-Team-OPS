# P4 — Source evaluation ingestion API (NOT host execution)

`policy_v002/eval_trial_pipeline.py` defines the read-only scoring/integrity interface for externally observed specialist trials; `evaluation/v0.0.2/trial-observation.schema.json` is the portable evidence shape.

- Inputs: exact SHA, installed v0.0.2 version, one case/arm, model/permissions/toolset/input, host session/run/response digests, independent oracle and scoring reviewer references, claimed tool actions with provider receipts.
- Decisions: missing source/host/oracle/receipt → UNVERIFIED; duplicate case/arm or receipt → blocked; critical security violation → CRITICAL_BLOCKED; supplied proof adapter successes **remain PROVISIONAL, NEVER release acceptance**.
- Baselines/ablations: four declared arms, comparable paired evaluation only with identical source and model/toolset/permission/input context; repeated attempts are not independent cases. Wilson intervals avoid claiming 99% on tiny samples.
- Actual independent verification must be performed outside this module with an authenticated provider adapter and distinct reviewer. The Python reference is not in browser plugin ZIP.

**What ran:** Native Python unit regression of structural input validators, replay/permissions checks, paired-ablation comparability and synthetic mock adapter. **What did NOT run:** no model trial, no installed v0.0.2 candidate, no independent authenticated oracle or scored specialist quality. This pipeline's provisional score must not update `P4.real_trials` or `m4.accuracy`.

When external access is authorized, record actual host data using this schema; verify source/host/owner grant and independent labels, then issue a new artifact with immutable primary evidence before attaching a quality score. Run all nine teams sequentially only when the host and reviewer requirements can be met.
