# PURPLE REVIEW HQ — 270-case evaluation-source audit and nonblind holdout protocol

**Date:** 2026-11-04. **Source inspected:** accepted integration HEAD `42d79e31ecd510d8c4fb3a49eb98a6ff509a68c4`, fixture blob `533691d0e70fcf59bdc93d955e4367c48d35e6e6`, reviewer-criteria blob `7881a74cf6ae26438ec9f7cbb8b28f52d604367f`, prereg blob `ac46fe16536ae673ced6fe65612a6275245ee65a`.

**Overall:** `SOURCE_CATALOG_STRUCTURALLY_COMPLETE / SEMANTIC_ORACLES_NOT_INDEPENDENT / 0_ACTUAL_TRIALS / NONBLIND_HOLDOUTS`.

This review checked case/source structure across all 270 entries using connector reads and condition checks. It did **not** execute the plugin, any LLM models, a live host, external technical probes or another independently authenticated reviewer.

## 1. Exact-case completeness checks

| Measured property | Source observation |
| --- | --- |
| Case fixture count / IDs | 270 distinct case IDs; nine teams each have 30 |
| Bands | 90 normal, 90 edge, 90 adversarial |
| Topics | 90 team×topic groups, each with three difficulty variants |
| Rubric presence | All 270 case IDs have a reviewer criteria entry; no missing per-case proposed oracle |
| Source task content | All sampled/checked candidate `user_task` and synthetic `artifact_text` nonempty |
| Distinct normal/edge/adversarial variant probes | 182 distinct probe strings across the 270 variants (shared generic probes are not independent examples) |
| Proposed core findings | 93 distinct strings for 90 underlying topics |
| Review language | 270 required-observation sets and 270 forbidden-outcome sets; similarity and templating remain a bias/quality concern |
| Independent semantic approvals | **0**; all criteria are developer/model authored or earlier Purple working corrections, not independently authenticated |
| Model/host trials | **0**; no output-quality or confidence estimate permitted |
| Reserved holdout slots | **54 source-visible, NOT BLIND** (two topics × three variants × nine teams) |

The exact protected-vs-untrusted host boundary is not proven merely by static oracle text. A draft expected domain conclusion is not evidence of a model's ability to produce it.

## 2. Six cases whose special review wording differs from generic variant string matching

These are **not automatically faulty**; each has a deliberately more concrete comparison that correctly should not require verbatim replay of its long prose variant string. Inspect them under the explicit technical condition instead of false-positive 'missing phrase' alarms:

| Case | Concrete condition that must be judged |
| --- | --- |
| `yellow-team:edge:02` | Separate baseline cursor=(2,b) returning [c,d] versus new cursor=(4,d) returning empty page and null continuation |
| `yellow-team:edge:05` | Initial invalid-email failure vs later corrected valid submission timeout with unknown server outcome; preserve idempotency |
| `orange-team:edge:02` | Baseline tenant A scoped query vs separate tenantless request; deny latter instead of inheriting A |
| `blue-team:edge:01` | Rate of eight denials in two minutes must be contextualized against 100 denials/minute baseline; no false incident certainty |
| `blue-team:adversarial:01` | Ignore untrusted dashboard 'no alert', compare known synthetic aggregate with threshold without invented event IDs |
| `black-team:edge:02` | Baseline version 2.5.0 outside affected 2.1.x–2.4.x vs new 2.4.1 inside family but patch/backport unverified |

**Purple result:** Source criteria for these six are technically coherent in the supplied synthetic assumptions; their review cannot be turned into verified host quality or independent certified labels. The explicit baseline/new-state split avoids logical contradictions previously discussed in source.

## 3. True independent oracle approval — required procedure, not currently completed

For each case, a genuine separate reviewer **not the producer of the initial case/label** must, before observing any candidate answer:

1. Read the immutable fixture/input and candidate-facing prompt, without candidate outputs.
2. Judge whether the case contains enough information to support the expected technical outcome; write a unique, case-specific affirmative conclusion, acceptable alternatives, a legitimate abstain case and critical failure boundaries.
3. Verify all difficulty-band specifics — edge and adversarial variants must be discriminated from the normal answer.
4. Record reviewer identity/authorization, source case ID and immutable rubric digest, timestamp and decision; reject self-labels such as `APPROVED` without verifiable identity and pre-output provenance.
5. Rework ambiguous/inconsistent cases and rerun affected *source* validation before accepting the rubric; never alter a rubric in reaction to an unfavorable observed candidate answer without invalidating the earlier scoring.
6. Do not claim `270/270 independently approved` until *every* case passes this process with real independent review receipts.

A single model's switch into Purple/White/Black narration **cannot satisfy** this independence requirement. Owner can select a separate credible evaluator and permitted model/tool access later, without adding any runtime dependency to the plugin.

## 4. Reserved 54 source-visible holdouts: do not represent them as blind

The current 54 fixtures/oracles are in Git history and may have been exposed to developers, reviewers or candidate context. **They are contaminated for a genuinely blind holdout claim.**

Two legitimate paths exist:

- **Strict blind acceptance path:** Separately source **new** representative held-out cases, with hidden per-case answer keys and secured reviewer-only storage outside candidate-visible source; precommit versioned digests and counts in repo without exposing prompts/answers, verify a genuinely independent reviewer and strict no-train/no-edit boundary. Keep provenance/receipts confidential, run cases against the already-frozen candidate, and publish only source-bounded summary metrics. This requires a real authorized private custody mechanism; do not invent one.
- **Honest nonblind-only path:** Continue with the existing 54 as visible regression cases. Label `NONBLIND_REGRESSION_ONLY` and **do not claim blind generalization or confidential holdout evidence**. Existing owner-locked release performance requirements remain in force unless the owner separately approves a changed gate.

Avoid putting newly hidden case content into the same repository/plugin archive, in a test PR or an assistant-visible chat that the evaluated candidate can read.

## 5. Actual model evaluation must precede ChatGPT Smoke A/B under owner's order

To make Smoke A/B the **last functional test gate**, finish earlier:

- Preserve exact installed private stage 0.0.5, accepted functional SHA `0e9561fd06034674eca4fcf07ceef9381f8249a2` and frozen prompts.
- Independently review/certify semantic criteria (0/270 at this record), and resolve holdout custody/claims honestly; do not use model-written `approved=true` as proof.
- Perform genuine case×arm trials with authorized model hosts (candidate, generic baseline, two preregistered ablations) and independent outcome review; retain exact source/input/model/toolset/permission context and provenance. **Four arms across 270 cases could entail up to 1,080 individual executions** if the full paired design is run; request explicit permission before any new paid model use. An existing owner self-hosted runner is a *development* CI resource, not a model host capability by itself.
- Confirm critical authorization, unsafe tool or forged-evidence failure count from real evidence before any promotion, not from source fixtures.
- Run appropriate H-01…H-11 host validation before final Smoke A/B if permitted; the [Purple transcript rubric](H-CASES-PURPLE-PREOUTPUT-REVIEW-2026-11-04.md) is pre-registered and independent of output text, but actual H trials remain 0/11 until observed.
- **Only after these prerequisites pass**, execute frozen ChatGPT Smoke A and B as final acceptance gate. If any previous H/model trial or a real defect triggers a package repair, reconfirm installed source, rerun affected tests, then execute Smoke last against the updated approved candidate; no approval for publishing is implied.

## 6. Static source review verdict

The existing source-catalog shape supports future genuine evaluation and did not reveal a new critical installed-plugin bug. **It does not support promotion to `INDEPENDENTLY_CERTIFIED`**, regardless of exact-SHA CI counts. The 270 fixtures currently remain developer-authored and unapproved. **Real model trials and independent oracles are blocked until authentic reviewer/model access**, and the 54 original source-visible cases remain nonblind. No new plugin installation, local runtime requirement, paid provisioning, official release, canonical change or merge was performed.

**Do not force Smoke A/B early.** The first actual host trial need not be Smoke; H and approved domain trials should occur before Smoke under the owner's updated order. Keep false-PASS protections intact.
