# CTO-V002 — Independent 270-case scoring preparation (PF-04)

**DEVELOPMENT WORKSHEET ONLY: 0/270 independently approved rubrics; 0/270 actual host evaluations.** Current `reviewer-case-criteria.json` is developer-authored, not an independent oracle. The 54 reserved holdouts are source-visible and **NOT BLINDED**.

Before formal results, a genuinely separate identifiable reviewer must approve each case's expected team/domain result, legitimate refusal, acceptable variants, critical security failures and pass threshold; preserve reviewer receipt and case/criteria digest **before** observing candidate outputs. A model-written “approved” record is insufficient. Either use independently held unseen examples under an authorized process or explicitly report source-visible holdouts as non-blind.

Predeclare installed plugin ID/version/source, model/host/effort if exposed, baseline/candidate/ablation arms, frozen input generation, same tool/permission context, randomization, cost and retry budgets, timeout rules, case×arm denominator, zero-tolerance critical authority gate, receipt capture/redaction and actual evidence refs. A reference Python test is never an actual model trial or a 99% score. Keep real result counters and independent approval counters at zero until verified.

**Separately:** exploratory Smoke A/B do not need 270 oracle approvals; formal Smoke/H requires PF-03 and distinct Purple test-readiness review. **No independent approval or host trial was performed here. RELEASE_BLOCKED.**
