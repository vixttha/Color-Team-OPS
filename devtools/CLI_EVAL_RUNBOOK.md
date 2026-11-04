# CLI_TEST development evaluation

## Owner policy override — solo developer (2026-11-04)

The owner explicitly retired the mandatory external independent reviewer, signed 270-case approvals, and blinded-holdout custody as release prerequisites. The signed external review pathway below remains OPTIONAL, not required. All results in this pathway must be honestly labeled SELF_REVIEWED or AI_ASSISTED_PROVISIONAL, never independently certified.

To create the next real SOLO_DEVELOPER evaluation, use the following in the existing development checkout on feature/v0.0.2-codex-independent-eval:

```powershell
python -B -m unittest discover -s tests -p "test*.py"
python -B -m devtools.cli_eval freeze --solo --output evaluation/v0.0.2/CLI-EVAL-SOLO-FREEZE.json
git add evaluation/v0.0.2/CLI-EVAL-SOLO-FREEZE.json
git commit -m "Freeze owner-approved solo evaluation before model output"
python -B -m devtools.cli_eval run --freeze evaluation/v0.0.2/CLI-EVAL-SOLO-FREEZE.json --stage pilot
python -B -m devtools.cli_eval run --freeze evaluation/v0.0.2/CLI-EVAL-SOLO-FREEZE.json --stage full
```

Only execute these commands if the working tree is clean, the model account is authenticated, and no new paid usage is required. The solo full gate requires the exact 36/36 completed pilot receipts with intact source, inputs, raw hashes and unique sessions; it does NOT falsely certify semantic correctness. Check pilot quality before expanding to the full 270×4 run. Semantic correctness scores remain unverified until actually reviewed, and the current CLI harness does not yet implement automatic AI-as-judge scoring.

Preserve the old freeze and historical 36 exploratory records unchanged; new evaluation requires a NEW pre-output freeze and new pilot. The 54 source-visible holdouts remain NONBLIND_REGRESSION_ONLY. The reviewer onboarding packet/SSH signing path is optional legacy tooling, not a blocking requirement. After the model evaluation, genuine H-01..H-11 host tests occur, then final ChatGPT Smoke A/B LAST. Release remains blocked until genuine evidence and owner approval.

---

This harness uses existing ChatGPT-account Codex authentication. It neither
reads/copies credentials nor falls back to a paid API key. The native child
process requests **gpt-6.1-sol / medium / default service tier**, read-only
sandboxing, no approvals, no shell, apps, plugins, hooks, memory or browser.
It ignores the user's config/rules and strips inherited API/runner credentials.
An isolated temporary Git workspace contains only the instruction material.
Any observed tool-action event invalidates the trial and stops that lane.
Configuration is a requested boundary; absence of observed tool actions does
not independently attest OS sandbox enforcement or provider model identity.

## Pre-output freeze and execution

Commit development source first, then:

```powershell
python -B -m devtools.cli_eval freeze --output evaluation/v0.0.2/CLI-EVAL-FREEZE-2026-11-04.json
git add evaluation/v0.0.2/CLI-EVAL-FREEZE-2026-11-04.json
git commit -m "Freeze evaluation before outputs"
python -B -m devtools.cli_eval certify --freeze evaluation/v0.0.2/CLI-EVAL-FREEZE-2026-11-04.json
python -B -m devtools.cli_eval run --freeze evaluation/v0.0.2/CLI-EVAL-FREEZE-2026-11-04.json --stage pilot
```

Use the already committed freeze for resume, never overwrite it. A completed
pair is skipped only after raw-hash, session, source and environment checks.
One transient launch retry is allowed. Quota, timeout, rate, unexpected event or
isolation failure stops the affected execution lane and retains its receipt.
The 36 pilot pairs are nine `normal:01` cases, randomized within each case.
Model subprocesses are sequential test subjects, not independent reviewers.

In OPTIONAL EXTERNAL_INDEPENDENT mode, `--stage full` requires all 270 signed pre-output independent approvals, all 36
pilot completions, signed pilot grades and no unresolved critical violations.
Pilot pairs contribute to the 1,080-pair total and are not rerun as new cases.
The current freeze has **no enrolled reviewers**, so full execution is blocked.
New enrollment requires a new pre-output freeze and must never retroactively
certify already visible pilot outputs.

## Instruction arms and limits

Generic uses only generic assistance plus the common synthetic-task boundary.
Full loads the constitution, three coordinators, the explicitly named team's
playbook/reference, schemas and registry. This preserves lazy specialist loading.
The directory ablation omits the built-in table and registry. The handoff ablation
omits completion-event schema and paragraphs containing typed handoff/workflow
guidance. Every resulting instruction bundle is hashed before outputs.
These are portable-instruction CLI comparisons, not installed-plugin sessions.
Inputs name the specialist, so unhinted routing and actual host skill activation
remain NOT_OBSERVABLE. The 54 old holdouts remain NONBLIND_REGRESSION_ONLY.

## Reviewer intake and grading custody

There is no automatic creation of reviewer identities. A separate authorized
person/account must conduct the review without candidate answers, and an owner
must separately enroll that principal. The trust anchor is a manually verified,
owner-controlled input; a role name, arbitrary JSON claim, generated test key,
or producing agent's signature cannot establish independence.

An optional committed `--review-plan` supplies `reviewer_trust` and
`oracle_review_receipts`. Each enrollment maps a principal to a separately
verified `owner_enrollment_evidence`, `independent_of_producer=true`, an
`allowed_signers_file` and its SHA-256. Use OpenSSH allowed-signers syntax and
namespace `color-team-ops-oracle`; retain owner authorization proof separately.
Trust records and public signer files are not secrets. The verifier authenticates
the signature against that explicit trust anchor; it cannot discover independence
from a public key or authenticate a human's honesty by itself.

Each oracle entry has `payload_path`, `signature_path`, `payload_sha256`, and
`signature_sha256`. The signed JSON includes `reviewer_principal`, `decision`,
`case_id`, `rubric_sha256`, `reviewed_at`, `preoutput_commit` (the reviewed source
ancestor), `technical_outcome`, `valid_alternatives`, `legitimate_refusal`,
`critical_flaws`, and `difficulty_fairness`. Both payload and detached signature
must be committed before the freeze. Review timestamps must precede the freeze.
An intake failure cannot increment the approval count.

Run `python -B -m devtools.cli_eval prepare-grading --freeze <committed-freeze>`
to write neutral, arm-label-withheld packets and a separate assignment custody
map in ignored local storage. This is best-effort label withholding, not protected
blind custody: output text or access to the Git evidence may reveal an arm.
The raw local receipt links true arm, case, raw output, source and input. Grade
custody must provide only neutral IDs and response text to the separate grader;
withhold arm assignment where practical. Formal grade entries bind the raw digest,
case/source, certified oracle digest, reviewer, signed payload and signature.
They require reasoned per-criterion findings and response evidence, and explicit
critical-violation review. Bare booleans and model self-reported roles never pass.
Semantic correctness is supplied by the authorized external reviewer; the local
deterministic verifier only checks provenance/structure. No keyword-only grader
can independently certify technical correctness.

## Evidence retention, redaction, export and import

`.cli-eval-private/<freeze SHA256>/pilot/<ordinal>-<attempt>/` retains exact
stdout JSONL, stderr, response text and a receipt; raw data stays ignored by Git.
Only hash-indexed metadata is tracked. Session IDs are hashed in tracked records;
there are no raw credentials, response bodies, private paths or account IDs in
the exported audit report. No raw transcript should be uploaded without a
separate content review. Local filesystem access remains the owner's access;
this process does not provision a protected blind-test custody service.

Generate a new immutable nonsecret report:

```powershell
python -B -m devtools.cli_eval audit --freeze evaluation/v0.0.2/CLI-EVAL-FREEZE-2026-11-04.json --output evaluation/v0.0.2/CLI-EVAL-RESULTS-2026-11-04.json
```

For authorized private transfer, use `devtools.cli_eval_evidence export` to a new
local ZIP and `import` to a new empty directory. The archive index binds every
byte with SHA-256. Import verifies paths, sizes, hashes and no overwrites before
materializing files. A hash index proves integrity, not model authenticity;
compare its digest to the original trusted owner's evidence and audit report.
Neither command uploads evidence, creates a reviewer, or changes release gates.

Without authentic semantic grades, per-team/band/arm accuracy denominators are
zero, confidence intervals and paired deltas are NOT_MEASURED, and all executions
are EXPLORATORY_CLI_TEST_UNVERIFIED_INDEPENDENCE. Token usage and elapsed time
are reported when surfaced; subscription monetary cost is NOT_OBSERVABLE.
H-01–H-11 require a real staging-enabled ChatGPT host. Smoke A/B stays LAST,
followed by final audit and explicit owner release authorization.
