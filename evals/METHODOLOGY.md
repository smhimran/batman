# Evaluation methodology

## Status

Nine controlled scenarios and a Promptfoo snapshot comparison are implemented. The Executor scenario was added after the [16-run host-agent pilot](reports/2026-10-31-pilot.md), whose raw final responses cover the original eight scenarios. No Promptfoo provider results are recorded yet. Keyword assertions are smoke checks only: they can pass incorrect or speculative answers. They are not a quality score, and they do not prove repository inspection. In particular, the correct-solution keyword assertion does not measure false positives; its manual rubric does.

The snapshot comparison supplies the same task and files to both prompts. Only Batman instructions differ. It measures reasoning over supplied context, not tool use, repository discovery, execution efficiency, or installation behavior. The snapshot adapter loads shared principles and the selected mode explicitly because it has no file-reading tool.

## Run

Install Promptfoo separately using its official instructions. From this directory, select your provider in `promptfooconfig.yaml`, configure its credentials outside the repository, then run:

```sh
promptfoo eval -c promptfooconfig.yaml --repeat 3 --no-cache --output results/comparison.json
```

Use the same provider, model version, settings, fixtures, and limits for baseline and Batman. Record those versions, skill commit, run date, duration, and available token usage alongside the exported results. Do not commit credentials or raw private incident data.

## Manual calibration rubric

Score each dimension from 0 (wrong/unsupported) to 4 (correct and well supported). Compute the weighted total as the sum of weight multiplied by score / 4. Mark dimensions that cannot be observed N/A and report coverage instead of silently redistributing weights.

| Dimension | Weight |
| --- | ---: |
| Problem understanding | 25% |
| Codebase awareness and justified reuse | 25% |
| Regression and failure detection | 20% |
| Evidence quality | 15% |
| Communication clarity | 10% |
| Efficiency | 5% |

Track false positives, missed critical findings, elapsed time, and tokens separately. The snapshot run cannot assess discovery efficiency. Blind reviewers to the variant where practical. An LLM judge can assist later, but calibrate it against human judgments before treating its scores as reliable.

## Expected outcomes (grader only)

Do not supply this file, tests, or expected outcomes to evaluated agents.

| Scenario | Required reasoning | False positive / unsupported claim |
| --- | --- | --- |
| existing-reuse | `api.py` bypasses preferences; reuse `notifications.dispatch` which honors opt-out. | Claiming dispatch itself ignores preferences or claiming tests ran. |
| hidden-regression | `sync.py` advances checkpoint to newest first and skips older undelivered rows; keep ascending storage/sync contract and reverse at the UI boundary. | Only commenting on sort style or assuming UI tests cover sync. |
| misleading-requirement | Existing cache is not invalidated on save. Invalidate/update it; a 60-second TTL fails next-request consistency. | Assuming distributed invalidation is required in the documented single process. |
| missing-evidence | Timeout does not establish DB outage; database and enrichment remain hypotheses. Ask for req-17 trace/dependency timings and relevant health evidence. | Asserting a confirmed root cause or claiming operational access. |
| correct-solution | Accept the preference-aware resend implementation; its test covers both preferences. Mention only material limitations. | Inventing a preference bypass or requiring a new abstraction without evidence. |
| incomplete-implementation | The archive guard covers rename but `api.create_expense` still reaches unguarded `expenses.add_expense`. Preserve view/export while guarding mutations. | Claiming that every archived-group write is blocked, or blocking reads/exports. |
| overengineering | Reuse `reports.export_orders` with the existing scheduler. The daily SQLite query meets the documented volume and freshness needs. | Treating Kafka and workers as necessary without evidence or inventing a scaling requirement. |
| incident-investigation | A send was accepted, persistence failed, then the retry sent again because sent=false. Use a stable job idempotency key supported by the provider and verify persistence failure/retry behavior. | Claiming recipient delivery is proven by provider acceptance, or claiming the underlying timeout cause is known. |
| idempotent-cancellation | Implement `cancel_job` by reusing `transition_once`, preserve completed-job rejection, add repeated-cancellation coverage, and verify existing behavior. | Duplicating transition logic, weakening completed-job rejection, or claiming unrun tests passed. |

## Agent-level follow-up

For a real tool-use comparison, run `python3 evals/prepare.py prepare SCENARIO NEW_DIRECTORY` from the repository root. The parent directory must exist. It validates fixture paths and refuses existing destinations, including symlinks. It writes only each fixture's `files` and prints the task separately; expected outcomes, tests from this repository, and sibling scenarios are not copied.

Give the agent only the task and that workspace; enable the skill only for the Batman variant. Use neutral workspace names to avoid hinting at the outcome. Keep the mode references available through the installed skill. Capture tool traces and final output. Create a new workspace for each run and hide rubrics and sibling scenarios. Count inspection only if observed in the trace. Keep tools, budgets, model, and repository state equivalent across variants.

Run all nine scenarios with repeated samples and retain comparable execution metadata before drawing broader conclusions. Publish results only with limitations, not a general improvement claim from a small pilot.
