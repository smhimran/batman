# Batman comparison pilot — 1 November 2026

Batman solved the controlled fixtures and matched the two comparison review approaches on the strict review rubric. This pilot does **not** establish that Batman outperforms other tools. All four review variants reached the same core diagnosis; Batman's numerical lead over plain Codex came from more explicit repair recommendations.

## Review results

Five review scenarios, two fresh runs each, using the same requested model (`gpt-6-sol`) and medium reasoning:

| Variant | Required-outcome score / 100 | All criteria met | Core review diagnosis | Median seconds | Median reported tokens |
| --- | ---: | ---: | ---: | ---: | ---: |
| Plain Codex | 90.0 | 7/10 | 10/10 | 30.8 | 89,190.5 |
| Codex + Batman | 100.0 | 10/10 | 10/10 | 44.7 | 123,250 |
| Superpowers reviewer template on Codex | 100.0 | 10/10 | 10/10 | 43.5 | 88,613 |
| Codex built-in `exec review` | 100.0 | 10/10 | 10/10 | 33.8 | Unavailable |

The score is the percentage of three frozen essential criteria satisfied per response. An all-criteria success also requires no material unsupported claim. Core diagnosis is a separate descriptive audit: correctly identify the known defect and its mechanism, or accept the correct-solution control. It is not an external benchmark score.

Plain Codex found every review defect. Its three strict rubric misses were: not explicitly locating the sort reversal at the UI boundary; identifying the archive mutation gap without explicitly recommending a guard; and explaining the query regression without explicitly recommending restoration of the bulk SELECT. These are repair-completeness distinctions, not unique bug discoveries by Batman. The UI-order remedy distinction is especially sensitive to how permissively equivalent alternatives are accepted.

No material unsupported claims were flagged by the grader in this sample. All variants accepted the correct-solution control in both repetitions. This does not establish a general false-positive rate.

## Investigation, design, challenge, and implementation

The other five scenarios compare Batman against plain Codex only. Applying a review-only template to these tasks would not be a like-for-like comparison.

| Variant | Required-outcome score / 100 | All criteria met | Median seconds | Median reported tokens |
| --- | ---: | ---: | ---: | ---: |
| Plain Codex | 96.7 | 9/10 | 29.4 | 60,212.5 |
| Codex + Batman | 96.7 | 9/10 | 36.1 | 96,745 |

Both missed the health-evidence request in one missing-evidence response while correctly keeping the database outage unconfirmed and requesting dependency traces. Both produced correct cancellation implementations in both runs. Separate hidden checks verified repeated cancellation, one audit event, completed-job rejection, and reuse of the existing helper in all four resulting implementations. The agents added regression tests and ran verification.

## Observed limitations

Batman did not consistently follow its own inspection protocol. In hidden-regression trial `bfb0e139a9cf494aa49744961fc4ff1f`, the first command read the skill and immediately opened `change.diff`, before inspecting consumers and the Guardian reference. Its eventual diagnosis was correct. Loading a skill is not proof that every instruction was followed.

Batman reported about 38% more median tokens than plain Codex in the review cohort, and about 61% more in the broader cohort. Reported token counts include cached input and are not subscription charges. Native review returned zero usage counters, recorded as unavailable. Concurrent runs make elapsed times descriptive, not controlled latency measurements.

The ten fixtures were authored during Batman development; none is held out. There are only five distinct tasks per cohort, not ten independent tasks. Repetition does not increase task diversity. The judge was the same requested model family as the evaluated systems; candidate labels were randomized and skill-loading evidence removed, but this is model-assisted grading with a coding-agent audit, not independent human validation. Some judge evidence snippets normalize Markdown or join excerpts; consult the saved answers rather than quoting those snippets verbatim. The results do not support significance, generalization, or a public superiority claim.

## Execution and reproducibility

Promptfoo 0.125.1 dispatched 60 real Codex CLI trials through a custom Python provider using the saved ChatGPT login. Codex CLI was 0.166.0; Node was v22.22.1. API-key environment variables were removed. There were no execution failures. Promptfoo's initial 100% completion result has no quality assertions; the separate outcome rubric supplies the scores above.

Every trial used a new Git workspace with the same source evidence, a 300-second limit, and read-only access except for the implementation task. Baseline global Batman discovery was explicitly disabled. Batman's source and references were frozen before execution; source hashes, the dirty working-tree state, requested model/settings, and competitor provenance are retained. The backend-resolved model revision was not exposed. Review and broader cohorts used concurrency 3 and 2 respectively. The rubric was frozen before answer inspection.

The [Superpowers reviewer template](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/requesting-code-review/code-reviewer.md) was pinned to commit `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`, with its license retained. Its reviewer instructions were preserved and task/commit placeholders filled for a fresh Codex reviewer. This evaluates that prompt, **not** the full Superpowers dispatch/fix/re-review harness. Claude Code was installed but unauthenticated, so it was not evaluated. Hosted review services were not evaluated.

- [Machine-readable scores and individual grades](../results/2026-11-01-comparison/scoreboard.json)
- [Frozen rubric](../results/2026-11-01-comparison/rubric.json)
- [Provenance and source hashes](../results/2026-11-01-comparison/provenance.json)
- [Audit notes](../results/2026-11-01-comparison/audit.json)
- [Promptfoo review export](../results/2026-11-01-comparison/reviews-results.json)
- [Promptfoo broader-task export](../results/2026-11-01-comparison/other-results.json)
- [Reproduction instructions](../benchmark/README.md)

The local results directory also retains all 60 final answers, trial prompts, tool events, final source files, frozen inputs, grader inputs/outputs, and mapping files. Raw results are ignored by Git; include the evidence bundle explicitly when sharing the report. Nothing has been published.

A stronger next experiment needs independently sourced, held-out tasks with hidden behavioral checks and independent review grading. Keep this suite as development regression coverage. On the evidence available now, Batman is functional, matches the comparison reviewers on these tasks, and adds overhead; there is no demonstrated general advantage.
