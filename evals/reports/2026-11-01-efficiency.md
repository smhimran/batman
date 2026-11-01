# Batman before/after follow-up — 1 November 2026

**The candidate preserves the measured pilot outcomes but does not meet the
predefined efficiency goal or improve inspection-order compliance.** Keep the
benchmark isolation/reporting fixes and validation evidence. The skill revision
is left as an uncommitted candidate; this evidence does **not** support adopting
it as a demonstrated efficiency/reliability improvement. No further tuning or
expansion was performed after the frozen comparison.

## Changes

The actual dirty working-tree skill was frozen before edits. The candidate
removes repeated protocol prose, puts the review ordering condition near the
entry point, reduces Guardian to context → change → verification, and scales
context gathering to the relevant path and consumer contract. Shared guidance
encourages using already-read evidence and stopping repeated checks once the
question is answered. No tool-call quota or mandatory health checklist was added.

Uncertainty handling, evidence-backed claims, reuse, accepting correct code,
concrete repairs and behavioral regression checks remain. The review instruction
bundle is 21.1% shorter by whitespace word count; other mode bundles are about
11–12% shorter. Instruction length is not a task-efficiency result.

The [trace/grading audit](2026-11-01-pilot-audit.md) distinguishes repeated
inventory/status/source reads from useful reproductions and failed-command
recovery. It also explains why health evidence was not necessarily a consequential
omission when request timings could distinguish the timeout sources.

## Frozen comparison

The [plan](2026-11-01-efficiency-plan.md) was recorded before new outputs: preserve
outcomes and unsupported-finding rates, improve compliance, target at least 15%
lower median reported tokens. Six paired pilot tasks used fresh sessions,
`gpt-6-sol`, medium reasoning, the same tool policy and 300-second Codex budgets through
authenticated CLI/Promptfoo. The backend revision was not exposed. API keys were
removed. Global skills, including the symlinked Batman installation, were disabled
in the isolated run. Both skill snapshots and all task inputs stayed byte-identical.
The frozen discovery scan also enumerated nested fixture aliases inside the linked
repository: disabled-path lists grew during execution and some pairs differed by
one unused alias. No external skill read was observed, but exact settings were
not perfectly constant. The current harness stops at skill roots; that final
fix has offline coverage and was not behaviorally rerun after the usage limit.

| Successful pilot responses, six per variant | Before | After |
| --- | ---: | ---: |
| Frozen required criteria met | 18/18 | 18/18 |
| Material unsupported claims observed | 0 | 0 |
| Known review defects detected / explained / useful repair | 2/2 each | 2/2 each |
| Original correct-control acceptance | 1/1 | 1/1 |
| Reviews with context before diff | 2/3 | 2/3 |
| Median reported total tokens | 96,880 | 95,738 |
| Median uncached input tokens | 9,002 | 7,565 |
| Median output tokens | 1,297.5 | 1,231 |
| Median completed command count | 8 | 10.5 |
| Median seconds, descriptive | 37.4 | 40.7 |

Median total tokens fell **1.2%**, missing the target. The median paired
(after/before) token ratio was **1.071**, or 7.1% higher. Individual changes were
sync review −18.4%, correct control −4.2%, ownership review −22.5%, missing-evidence
investigation +25.5%, health-context investigation +18.4%, cancellation +33.8%.
These are different summaries of six variable tasks, not significance estimates.
Cached input is included in total usage; missing usage is unavailable, never zero
cost. Elapsed time includes noisy local command behavior and concurrency.

Both cancellation implementations passed the existing hidden checks for one
audit event, repeated cancellation, completed-job rejection and helper reuse.
Both added regression coverage, demonstrated failure before repair and ran
verification. Both investigations kept uncertainty and used health evidence
appropriately in the new development case. The strict legacy health-request
criterion passed for both in this valid run, illustrating variation from the
original pilot rather than a proven skill effect.

The ordering failure persisted: before trial `d047432…` read the skill and diff
in one command before the mode/context; after trial `c1d965d…` opened the diff
before reading the skill. Moving prose earlier cannot affect a command issued
before that prose is loaded. Neither version earns a workflow-compliance win.
Repeated inventories and low-value probes also remain in the revised traces.

## Reserved validation and grading limits

Four [new tasks](../validation/manifest.json) are explicitly author-created,
synthetic fixtures, with separate ground-truth checks outside evaluated
workspaces. Two were reserved until the skill freeze and pilot audit; no skill
edit used their outputs. All original ten fixtures and rubric entries remain
unchanged. No earlier variant was rescored and no criterion was weakened.
Detection, explanation and repair audits supplement, rather than replace, the
original composite rubric.

The reserved cache task exposed an **authoring ambiguity**, not a demonstrated
false-positive advantage. Its unqualified at-most-once requirement can encompass
concurrent calls. Before reproduced actual double loading and conditionally
recommended coordination; after accepted sequential behavior and noted the
concurrency limitation. The intended correct-control ground truth tested only
sequential calls. Its quality comparison is quarantined, with the frozen task and
criteria retained. After used 19.8% fewer tokens, but before did additional useful
behavioral investigation. After also never opened the patch content, so full
review-sequence compliance is not established. See [validity notes](../validation/KNOWN_LIMITATIONS.md).

Both reserved refund trials failed at the CLI usage limit without final answers;
no task outcome or token usage can be inferred. No additional model grading was
attempted after that limit. The reserved tasks are now inspected and cannot be
reused as untouched holdouts. Their mechanisms also overlap development cases.

A fully controlled confirmation remains incomplete: the nested-alias settings
variation was fixed only after execution, and the usage limit prevents a clean
behavioral rerun. These results therefore support caution, not a validated win.

## Execution accounting and verification

The valid run has **18 attempts: nine per variant**, with seven final answers
and two execution failures each. Six answers per variant are fully graded and
audited; the seventh is the ambiguous cache task. Each variant had one original
control worker timeout (its one bounded retry succeeded) and one refund usage-limit
failure. Do not report 100% all-attempt success. The wrapper received 330 seconds
on retries/reserved trials to record the unchanged 300-second model budget.

An earlier batch was invalidated because discovery enumeration skipped the global
Batman symlink. Its 14 final answers are excluded from the decision. Its 12 CLI
initialization failures and an earlier 12-case provider setup failure are retained,
not silently replaced. The corrected run reused identical skills/tasks/rubric.

Offline checks passed: **28 Python tests, 11 Node tests, the skill validator,
Python compilation and `git diff --check`**. These include source-only workspace
isolation, fixture behavior, snapshot preservation, symlink disabling, correct
cohort classification and counting outer worker failures. Ground-truth checks
passing did not establish that the cache control was unambiguous.

[Valid local evidence](../results/2026-11-01-efficiency-isolated/) includes frozen
inputs/hashes, initial dirty patch, prompts, commands, answers, grades/mappings,
manual audit, hidden checks, per-task metrics, execution errors and offline logs.
[Excluded batch](../results/2026-11-01-efficiency/) is separately labeled invalid.
Raw evidence is ignored by Git and must be included explicitly when sharing.

The reporting fixes derive task cohorts from declared modes and count outer
worker errors; they change no grade. Existing unrelated dirty patches were
verified unchanged. No project commit, push, publication or new skill installation was made.
This small author-controlled, model-assisted experiment does not establish general
superiority, a population unsupported-finding rate, or a reliable token reduction.
