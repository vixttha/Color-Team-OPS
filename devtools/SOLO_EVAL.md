# Solo evaluation protocol and versioned grading revisions

Owner policy: SOLO_DEVELOPER / SELF_REVIEWED / AI_ASSISTED_PROVISIONAL.
External identities, signatures and blind custody are not required.
Historical exploratory evidence is immutable and excluded from the new target.

The existing `cli_eval freeze --solo` now binds the semantic grader's prompt,
strict output schema, model/effort, retry policy and maximum four isolated model
subjects. The parent is one supervising Worker. Each subject has read-only
permissions, disabled external tools, stripped credential environment, and a
temporary workspace. Candidate and grader calls have separate raw receipts.

Grader revision 2 constrains each quote to an actual nonblank response line in
the native output schema. Calibration v3 covers the earlier Markdown quote
failures. Solo freeze v1 stopped after six candidate executions; they and all
eight associated grader attempts remain excluded from the replacement v2 run.
Calibration also records a PASS/PARTIAL disagreement about implicit effective-date
reasoning in one historical answer. These semantic judgments remain provisional.

Before the freeze, run real grader calibration against eight deliberate defects
and two historical actual outputs. Unit tests separately reject contradictory
grade JSON, forged quotes, empty-answer PASS, false routing/host claims, incomplete
pilot execution and critical pilot findings. Calibration outputs never count as
new candidate executions. Keep failed calibration versions and count all calls.

Create a new committed freeze, then run:

```powershell
python -B -m devtools.cli_eval freeze --solo --output evaluation/v0.0.2/CLI-EVAL-SOLO-FREEZE-v1.json
# Commit the freeze before invoking pilot.
python -B -m devtools.solo_eval pilot --freeze evaluation/v0.0.2/CLI-EVAL-SOLO-FREEZE-v1.json --workers 4
python -B -m devtools.solo_eval report --freeze evaluation/v0.0.2/CLI-EVAL-SOLO-FREEZE-v1.json
```

Evidence lives in ignored `.cli-eval-private/solo-v1/<freeze digest>/`.
Grader input contains the frozen task/rubric and actual untrusted response;
it omits arm labels. Text can reveal an arm, so this is best-effort withholding.
Deterministic checks bind quotes, criterion indexes, rubric/input/source/raw
hashes, session uniqueness and derived conclusions. These checks cannot prove
semantic truth. Same-family grading can share model biases. Unobservable metrics
are excluded rather than converted into successes or failures.

After examining all pilot grades, the supervising developer records three
logical audit passes in `pilot-acceptance.json`, binding the summary/freeze and
actual evidence. Full execution requires all 36 graded pilot pairs, no unresolved
critical/security finding, no contradictory assessment and no unresolved high
uncertainty. Task-quality failures can remain measured failures; do not hide them.
Resume full to reach 1,080 new candidate pairs total. Separate graders may add up
to two attempts per pair and their usage is reported separately.

Quota/rate/timeout/trace/grade failure stops new submissions; at most the other
already active subjects can finish. Checkpoints retain every attempt, including
invalid grades. Revisions changing frozen behavior require a NEW freeze, never
rewriting or combining incompatible evidence. Report raw verdicts, exclusions,
PASS/FAIL/PARTIAL/NOT_OBSERVABLE, confidence limitations and critical findings.
The directory omission removes registry/table. The revised handoff omission
removes typed exchange/schema guidance while preserving constitutional safety
laws; surrounding paragraphs may still contain related guidance, limiting
strictly causal interpretation. Required specialists are already named in tasks.

No model transcript establishes ChatGPT skill activation, an independent review,
or release authority. H-01–H-11 follow the scored evaluation; Smoke A/B remains
LAST. Staging/canonical sources remain unchanged; RELEASE_BLOCKED persists.
