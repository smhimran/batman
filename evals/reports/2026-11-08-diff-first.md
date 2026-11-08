# Batman diff-first review: completed confirmation — 8 November 2026

The latest review workflow used **16.2% fewer median reported tokens** than the previous split reviewer in a fresh, matched confirmation. Its review rubric score was **96.7 versus 100.0**: one response correctly diagnosed the preference bypass but offered a duplicated check alongside the existing dispatcher instead of preferring reuse. This is a quality/efficiency tradeoff in a small development suite, not demonstrated general superiority.

## Primary clean comparison

All 80 fresh confirmation trials completed and were graded, with no execution errors. Each cohort has five distinct tasks and two repetitions per variant. Scores use the unchanged legacy v1 outcome rubric, not keyword assertions.

| Review variant | Rubric score / 100 | All criteria met | Median reported tokens |
| --- | ---: | ---: | ---: |
| Plain Codex | 86.7 | 6/10 | 76,773.5 |
| Previous split Batman | 100.0 | 10/10 | 98,979 |
| Updated diff-first Batman | 96.7 | 9/10 | 82,941 |
| Superpowers reviewer template on Codex | 100.0 | 10/10 | 86,377.5 |
| Codex built-in reviewer | 96.7 | 9/10 | Unavailable |

The updated reviewer used **8.0% more** median tokens than plain Codex and **4.0% fewer** than the Superpowers template. Native review reported zero usage counters, treated as unavailable rather than zero cost. All variants identified the core known review defects or accepted the correct-code control according to the graded criteria; the numerical distinctions concern reuse preference, explicit repairs and acknowledgment of test coverage. They are not unique bug discoveries.

The new workflow explicitly starts with the diff, then requirements and source/callers. Old context-before-diff compliance is **inapplicable**; removing that instruction is not an instruction-compliance improvement. Representative updated answers still traced the unchanged sync consumer, unguarded expense mutation and query-count requirement and reproduced their failure paths.

## Usage details and broader tasks

Review median completed shell commands fell from **11 to 8.5** and output tokens from **1,202.5 to 1,157.5**. Median uncached input increased from **5,871 to 6,388**, despite lower total reported tokens. Total tokens include cached input and are not subscription charges. Review median seconds were 36.5 versus 33.5, descriptive only because execution is concurrent and not a controlled latency experiment.

| Broader-task variant | Rubric score / 100 | All criteria met | Median reported tokens |
| --- | ---: | ---: | ---: |
| Plain Codex | 96.7 | 9/10 | 78,397 |
| Previous split Batman | 93.3 | 8/10 | 110,731 |
| Updated snapshot | 96.7 | 9/10 | 103,738.5 |

Only `skills/batman-review/SKILL.md` differs between frozen snapshots. The investigation, design, challenge and execution skill instructions are byte-identical. Broader-task score and token differences therefore must not be attributed to the review edit. The broader deductions concerned requesting dependency traces without an explicit health-evidence request; those answers correctly retained uncertainty. The fixed rubric is narrower than every valid next investigation step.

All six cancellation implementations passed separate hidden checks for repeated cancellation, one audit event, completed-job rejection and reuse of the existing helper. All correct-control answers accepted the implementation. No material unsupported claim was flagged by the judge in the clean cohort. These observations do not establish population false-positive rates.

Across all 20 responses per Batman snapshot, median reported tokens were **100,329 before versus 88,706 after**, an 11.6% decrease; the overall 15% target is not met. Review-only reduction exceeds 15% in this sample but accompanies a small composite-rubric loss. The median task-level token ratio was 0.915; different aggregations answer different questions and should not be treated as significance estimates.

## Isolation repair and excluded execution

The earlier quota-limited batch had 80 attempts: 32 answers, 44 usage-limit errors and four timeouts. After the user reported reset, exactly 48 missing slots were retried and all produced answers. The audit then found **five comparator responses reading the globally installed Batman review skill**. Disabling only the top-level entry had missed nested focused skills and saved snapshot aliases exposed under the symlinked repository.

All initial and recovery results are excluded from the primary comparison. The harness was repaired to enumerate nested aliases and canonical paths; a frozen manifest disabled **177 global paths/aliases** for every trial and grader in the fresh confirmation. Trace audit found no global skill reads or unexpected comparator skill reads in the 80 clean trials. One identical disable configuration was used throughout; frozen input and harness hashes remained unchanged. Changing catalog isolation can change prompt overhead, so direct token comparisons to older reports are not controlled.

**Total trial accounting across the excluded and clean batches: 208 attempts, 160 answers and 48 execution failures.** The clean confirmation itself is 80/80 completed; do not describe the entire history as error-free. Grading calls are additional to these trial counts, and earlier grading errors are retained. The original five contaminated trial IDs and commands are saved in the excluded audit.

## Method and limitations

Promptfoo invoked the existing ChatGPT-authenticated Codex CLI with API-key environment variables removed, requested `gpt-6-sol`, medium reasoning, fresh Git workspaces, the same ten original tasks, two repetitions, 300-second model budgets and read-only access except implementation. Review/broader concurrency was three/two. The same frozen skills and rubric were preserved across recovery and confirmation; only isolation changed for the fresh matched comparison. The backend-resolved model revision was not exposed.

The focused skills are invoked directly by scenario mode, not through a separately tested selector route. Superpowers means its pinned reviewer template on Codex, not its full dispatch/fix/re-review system. No authenticated Claude Code or hosted review service is represented.

Candidate labels were randomized for model-assisted grading. The parent coding agent inspected the numerical deductions, representative review evidence and implementation-verification results; this is not independent human validation. Grader evidence snippets and the skill-read filter have known limitations, so original responses and traces remain authoritative. The tasks are author-controlled development fixtures with only five independent tasks per cohort. Neither nominal scores nor token differences establish a general win. Do not tune the skill to exact grader wording.

Offline verification passed **30 Python tests and 11 Node prompt tests**. The isolation fix and its regression test pass the Python suite. The benchmark guide documents the nested-discovery issue. Skill instructions were not edited during this work. No installation, commit, push or publication was performed.

## Evidence

- [Clean scores and all 80 grades](../results/2026-11-08-diff-first-clean/scoreboard.json)
- [Token metrics and scenario-level ratios](../results/2026-11-08-diff-first-clean/version-metrics.json)
- [Grade audit](../results/2026-11-08-diff-first-clean/grade-audit.json)
- [All-attempt accounting](../results/2026-11-08-diff-first-clean/attempt-accounting.json)
- [Isolation repair](../results/2026-11-08-diff-first-clean/isolation-repair.json)
- [Frozen plan and changed metric](../results/2026-11-08-diff-first-clean/run-plan.json)
- [Excluded-run contamination audit](../results/2026-11-08-diff-first-clean/excluded-recovery/contamination-audit.json)
- [Complete evidence bundle](../results/2026-11-08-diff-first-clean.zip)

The local bundle retains clean and excluded trial answers, tool events, final code, grader inputs/outputs, frozen sources, configuration, hashes and error records. Raw evidence is ignored by Git and must be shared explicitly alongside the report. This completed report supersedes the earlier partial status without erasing its execution history.
