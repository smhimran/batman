# Batman diff-first revision — partial benchmark, 8 November 2026

**Incomplete: Codex subscription usage was exhausted during execution. No full comparative score or token-efficiency conclusion is supported.**

The latest change is in `batman-review`: it now explicitly reads the diff first, then requirements/context, source paths and callers, failure paths, and checks. Old context-before-diff compliance is inapplicable to this revision. It must not be reported as improved compliance merely because that requirement was removed.

The run froze the current split skills, the previous split snapshot, the same ten tasks, original v1 rubric, requested `gpt-6-sol` model, medium reasoning and two repetitions. Review comparators remain plain Codex, the pinned Superpowers reviewer template on Codex, and native Codex review. Broader tasks compare plain Codex and both skill versions. The focused skills are read directly; selector routing is not tested.

## Execution accounting

- Planned/attempted trials: 80.
- Final answers: 32.
- Execution failures: 48, comprising 44 explicit usage-limit errors and four 300-second timeouts.
- Fully graded answers: 22.
- Completed grading groups: correct-solution, idempotent-cancellation, incident-investigation.
- Other grading calls failed or timed out; their logs are retained.

The CLI returned: “You’ve hit your usage limit” and “try again at 8:49 PM.” No further model retries were made after confirming the limit. Execution errors are not incorrect engineering answers, and completed-only grades are not an all-attempt success rate.

The correct-control and cancellation groups passed their available grading checks. The updated reviewer identified the preference bypass in both completed reuse trials. These observations are narrow partial results. Incomplete cohort coverage prevents a fair full ranking or an efficiency comparison. The unchanged rubric retains the known cache-removal alternative issue; no criterion was altered to favor this revision.

Offline checks passed: **30 Python tests and 11 Node tests**. Frozen source hashes remain unchanged. No skill instructions were changed during execution. No installation, commit, push or publication was performed.

## Evidence and continuation

[Run status](../results/2026-11-08-diff-first-partial/run-status.json) records counts. [Partial graded results](../results/2026-11-08-diff-first-partial/scoreboard.json) must be read with the missing-answer and failure accounting above. [Frozen plan](../results/2026-11-08-diff-first-partial/run-plan.json), [provenance](../results/2026-11-08-diff-first-partial/provenance.json), original exports, all answers/tool traces and grading errors are retained in the [evidence bundle](../results/2026-11-08-diff-first-partial.zip).

After usage access resets, retry failed cases with unchanged frozen sources and retain all original errors and extra attempts. Grade missing groups only when coverage is adequate. If a recovery step repeats successful variants, prerecord a balanced selection rule, as in the previous run. Do not combine partial success-conditioned scores with historical scores to claim a complete benchmark result.
