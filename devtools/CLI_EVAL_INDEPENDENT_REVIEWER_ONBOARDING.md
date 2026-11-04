# CTO-V002 — Owner-controlled independent reviewer onboarding

**Status (2026-11-04):** `REVIEWER_NOT_IDENTIFIED / NOT_ENROLLED / INDEPENDENT_ORACLES_0_OF_270 / FORMAL_TRIALS_BLOCKED`. This is a live onboarding procedure for the EXISTING signed-reviewer system, not an approval record. The 36 real exploratory CLI_TEST responses have already been exposed to the developer and **cannot be retrospectively certified as a pre-output formal pilot**.

**Product scope:** `vixttha/Color-Team-OPS` product target v0.0.2, existing private stage 0.0.5, accepted runtime source unchanged. Owner self-hosted runners are **developer tools only**. ChatGPT Smoke A/B must remain the LAST functional test after genuine H-01…H-11 host trials and independent model evaluation.

## A. What is a real independent reviewer?

Use **an identifiable, separately controlled person/account** who did not create the original candidate fixture/oracle, build the candidate system, or see the responses before certifying the grading rules. A different agent name, a second Codex thread on the same owner's identity, a self-generated OpenSSH key, a simulated Purple reviewer or a GitHub issue comment that says “approved” is NOT enough.

Identity must be owner-verified through a trusted channel **outside the candidate process**. Acceptable evidence includes a separately authenticated GitHub account associated with the reviewer and a direct owner-confirmed signing-key fingerprint; record the actual independent relationship and conflict-of-interest check. A signature proves possession of a public-key-paired private key; it does **not** prove impartiality, independent employer/account ownership or factual correctness. The owner must explicitly authorize that principal **only for oracle/review scope**, not publish or runtime permissions.

**No actual independent reviewer has been nominated, authenticated or enrolled in this branch.** Do NOT invent a real name, GitHub username, key, independent report, owner consent, or verification receipt. If no reviewer is available, preserve `CAPABILITY_BLOCKED_INDEPENDENT_REVIEWER` with 0/270 certified.

## B. Prepared intake: generate exactly 270 unsigned packets (no candidate outputs)

The source-stage 270-case fixtures and rules are in the repo; this branch now contains a real development-only packet generator and negative tests. From the correct Git checkout:

```powershell
git switch feature/v0.0.2-codex-independent-eval
python -B -m devtools.cli_eval_reviewer_intake --freeze evaluation/v0.0.2/CLI-EVAL-FREEZE-2026-11-04.json --output .cli-eval-private/reviewer-intake-2026-11-04
```

This creates in **ignored local storage**, never Git:

- `reviewer-packets.json`: all 270 frozen case inputs and developer-proposed criteria for review; no model responses or scored outcomes
- `UNSIGNED-REVIEW-TEMPLATES.json`: 270 `PENDING_NOT_APPROVED` entries with blank reviewer/decision/reasons
- `manifest.json`: frozen file hashes, 54 marked `NONBLIND_REGRESSION_ONLY`, explicit zero approvals and an absent identity

The generator verifies each case and rubric digest against the existing freeze, fails on missing or changed sources, and **will not overwrite an existing output directory**. Output must remain under `.cli-eval-private/`. Perform a content/sensitivity review before sending packets to the genuinely independent reviewer. Do **not** share the local raw output archive, prior grading packets or arm custody map during pre-output oracle review.

## C. External reviewer creates and safeguards their OWN signing identity

After the owner has chosen and independently verified a real reviewer, the reviewer—not Codex or this assistant—generates an Ed25519 private key **on the reviewer's own machine**, outside the repository. Example reviewer-side PowerShell, run only by that reviewer:

```powershell
ssh-keygen -t ed25519 -f "$env:USERPROFILE\.ssh\cto_v002_oracle_signing" -C "cto-v002-independent-reviewer"
ssh-keygen -lf "$env:USERPROFILE\.ssh\cto_v002_oracle_signing.pub" -E sha256
```

The reviewer supplies the **public** key and fingerprint to the owner through a separately authenticated channel. **Never** send the private key, password, API tokens or browser credentials to GitHub, Codex, this chat, the candidate, or the reviewer-intake directory. The owner checks the key fingerprint out of band and binds it to the independently verified person/account. Do not put a generic dummy key into a live trust anchor.

Use the existing OpenSSH allowed-signers contract: one line `<verified-principal> ssh-ed25519 <reviewer-public-key-data>` (with actual authenticated values), stored in a new nonsecret Git-tracked path. The per-review signature namespace is `color-team-ops-oracle`. A public-key file alone proves nothing about independent enrollment. Owner-enrollment evidence must reference actual verifiable owner approval, signer fingerprint, scope and source revision, **not** an arbitrary string such as `approved`.

## D. Genuine signed per-case oracle review (before NEW candidate outputs)

The identified reviewer independently checks every submitted case's expected technical result, valid alternative solutions, legitimate abstention/refusal, critical failure boundaries, difficulty-band fairness and evidence limitations. They may **reject or request revision**, not just mass-sign `APPROVED`. For each accepted case, they fill an individual JSON payload with the fields required by `devtools/cli_eval.py:certification`:

```json
{
  "reviewer_principal": "REPLACE_WITH_VERIFIED_SIGNER",
  "decision": "APPROVED",
  "case_id": "yellow-team:normal:01",
  "rubric_sha256": "REPLACE_WITH_FROZEN_REAL_DIGEST",
  "reviewed_at": "REPLACE_WITH_TRUE_UTC_TIMESTAMP",
  "preoutput_commit": "REPLACE_WITH_VALID_ANCESTOR_SHA",
  "technical_outcome": "REVIEWER_WRITTEN_CORRECT_OUTCOME",
  "valid_alternatives": "REVIEWER_WRITTEN_ALTERNATIVE_BEHAVIORS",
  "legitimate_refusal": "REVIEWER_WRITTEN_REFUSAL_CONDITIONS",
  "critical_flaws": "REVIEWER_WRITTEN_CRITICAL_FAILURE_BOUNDARY",
  "difficulty_fairness": "REVIEWER_WRITTEN_NORMAL_EDGE_OR_ADVERSARIAL_CHECK"
}
```

**This JSON is a field-shape illustration ONLY**, with fictitious placeholders and **no approval generated by this repository**. Reviewer must not sign it unchanged. Sign actual *final exact payload bytes* using the reviewer's own key; a reviewer-side example:

```powershell
ssh-keygen -Y sign -f "$env:USERPROFILE\.ssh\cto_v002_oracle_signing" -n color-team-ops-oracle "path\to\actual-reviewed-case.json"
```

That command writes a detached `.sig`. Preserve the exact signed JSON bytes, signature bytes and authenticated account evidence. If a criterion is ambiguous, revise the proposed criterion BEFORE signed approval and BEFORE formal candidate outputs; never silently retrofit a rubric after seeing the candidate answer.

## E. Owner enrollment, review plan and required verifier checks

After the owner verifies identity/key and the reviewer has genuinely signed the case oracles, add **only public** allowed-signers material and signed review artifacts to the development review branch. The owner prepares a reviewed, Git-tracked JSON file passed as `--review-plan` with:

- `reviewer_trust.producer_principal`: original case producer identity
- `reviewer_trust.reviewers[<verified-principal>].owner_enrollment_evidence`: externally verifiable, actual owner-scoped approval reference and key binding
- `independent_of_producer=true` only after real conflict review
- `allowed_signers_file` and `allowed_signers_sha256`: owner-pinned allowlist
- `oracle_review_receipts`: one record per genuine approved case with Git-tracked `payload_path`, `signature_path`, `payload_sha256`, `signature_sha256`

**Do not sign documents with Codex's or the owner's key while labelling them independent.** A verifier cannot infer external independence merely from a boolean. Cross-check Git changes, person/account, custody, pre-output timestamps, the preserved source+rubric hashes and detached OpenSSH signatures. Any missing case or insufficient evidence stays `UNVERIFIED`, not `APPROVED`.

The existing `devtools/cli_eval.py` performs signature verification via `ssh-keygen -Y verify`, source ancestry and pre-output commit checks; it requires **all 270 signed independent oracles** before the full run. The original freeze has 0 reviewers and MUST NOT be modified.

## F. NEW formal freeze and formally graded model trial

Once the signer/receipts/review plan are verified in a clean commit, Codex creates a **NEW** immutable pre-output freeze using the already implemented `--review-plan` mechanism. Verify all 270 are certified before any qualifying new candidate invocation:

```powershell
python -B -m devtools.cli_eval freeze --review-plan path\to\owner-verified-review-plan.json --output evaluation/v0.0.2/CLI-EVAL-FORMAL-FREEZE.json
git add evaluation/v0.0.2/CLI-EVAL-FORMAL-FREEZE.json
git commit -m "Freeze independently reviewed evaluation inputs before formal model outputs"
python -B -m devtools.cli_eval certify --freeze evaluation/v0.0.2/CLI-EVAL-FORMAL-FREEZE.json
```

The freeze must be committed, no source dirty, and all actual signer material already committed. Current time, source revision and SHA must come from actual tools; never copy demo timestamps. Verify exactly 270 authentic approvals; a signed record can still be substantively wrong and require review.

Then run a **fresh qualifying 9-case × 4-arm pilot**, independently grade response evidence using separate signed grading receipts, and, only after actual pilot acceptance and available subscription quota, expand to full 270-case × 4 arms. The previously exposed **36 exploratory responses cannot be retrospectively upgraded**. Continue to mark the original 54 source-visible reserved holdouts **NONBLIND_REGRESSION_ONLY**; genuinely blind generalization requires independently secured fresh cases or an explicit owner policy decision that does not misrepresent them.

**ChatGPT H-01…H-11 hosted tests come after independent model evaluation; Smoke A/B must remain the final two functional host tests.** Product `RELEASE_BLOCKED` and accepted plugin runtime stay unchanged until genuine evidence and separate owner release authorization.

## Owner-required input to finish enrollment

**One essential detail remains:** the independent person's/account's identity (for example a GitHub username), plus their independently supplied **public** signing key and owner-verified relationship. This repo can prepare the packets, verify public signatures and enforce zero fake approvals, but **cannot create a separate independent human/model/account or sign on their behalf**. Until the owner actually identifies and verifies that principal, `CAPABILITY_BLOCKED_INDEPENDENT_REVIEWER`, 0/270 approvals and 0/36 formal grades remain the only truthful status.
