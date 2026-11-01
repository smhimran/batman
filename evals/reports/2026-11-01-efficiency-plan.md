# Frozen efficiency comparison plan — 1 November 2026

Recorded before new behavioral outputs. The current dirty skill is frozen as
`evals/results/2026-11-01-efficiency/inputs/before`; original status, patch and
SHA-256 manifest accompany it. Preserve the original ten fixtures and rubric.

Success measures, evaluated separately:
- Outcomes: no loss of known-defect detection, causal explanation, useful repair,
  correct-control acceptance, or hidden implementation behavior in paired tasks.
- Unsupported findings: no increase in material unsupported claims. Record raw
  counts; this small sample cannot estimate a general false-positive rate.
- Compliance: relevant source/consumer context before diff content; selecting
  a mode before task inspection. Count observable violations, ambiguous cases
  separately. Do not use command count as a compliance target.
- Efficiency: target at least 15% lower median reported total tokens, without
  sacrificing outcomes; also report paired ratios, uncached input, output,
  command activity, elapsed time, and task-level regressions. Cached input is
  included in reported totals; these are not charges or controlled latency.

Start with one fresh before/after pair on hidden-regression, correct-solution,
missing-evidence, idempotent-cancellation and two newly constructed development
validation tasks. Requested model gpt-6-sol, medium reasoning, same tools and
300-second timeout per trial; Promptfoo no-cache, concurrency 2. Authenticated
Codex CLI, no API keys. Freeze both skills, fixtures, harness and grading before
execution. Disable global skill discovery, audit session instructions and traces.
No skill changes during comparison. Answers/ground truth stay outside evaluated
workspaces. Only raw task evidence and the selected skill enter each workspace.

If no outcome/unsupported regression appears in this initial pilot, run one pair
on each of two reserved tasks. These are newly constructed, author-created
synthetic tasks, not independent real-world evidence. Their outputs must not
inform skill changes. Retain them as held-out confirmation for this revision;
after inspection they are no longer a reusable untouched holdout. No broader
expansion or significance claims from this sample.

Keep v1 rubric unchanged, including its strict repair/health criteria. Report
its composite separately from detection, explanation and repair audits. Accept
substantively equivalent fixes in the descriptive audit; do not retroactively
rescore comparison variants. Any future changed rubric requires a new version
and consistent rescoring of all old variants. Audit model grades against raw
answers/tools; they are not independent human grading.

Decision: keep only if outcomes remain comparable, compliance improves or is
at least consistent on this small sample, and tokens materially decrease.
Otherwise report mixed/inconclusive evidence and the failed measures; never
force a winning aggregate. Offline tests validate fixture ground truth and
harness isolation, not model quality.
