# Controlled tool-use comparison

## One-command terminal runner

From the repository root:

```sh
python3 scripts/benchmark.py
```

The Codex desktop app can stay closed. This uses Python 3.11+, Git, and the
installed, signed-in Codex CLI. It reuses the authenticated CLI provider directly;
Promptfoo and API keys are not required for this runner. Model calls use your
account's usage allowance.

By default it freezes the current working tree, the latest local prior Batman
snapshot with a completed scoreboard, and a local pinned Superpowers reviewer
source. With a previous snapshot, it runs the same 80-trial comparison: ten tasks,
two repetitions, `gpt-6-sol`, medium reasoning, at most three trials at once, then
two graders at once. Without a prior snapshot it runs 60 trials against the other
comparators. The default output is a new timestamped directory in `evals/results/`.
Nothing is installed, committed, published, or written to the README.

The runner saves answers and logs, freezes global skill exclusions, grades against
the existing rubric, checks frozen hashes, flags suspicious skill-read commands,
and writes `report.md`, `scoreboard.json`, and `trace-audit.json`. Grades and the
command-level audit are preliminary; inspect the saved evidence before publishing
claims. This does not replace the manual audit in the published reports.

It stops scheduling new trials on failure and retains in-flight results. After
fixing a login, usage-limit, or runner problem, resume using the directory printed
by the script:

```sh
python3 scripts/benchmark.py --resume /absolute/path/to/run
```

Completed trials are skipped. Failed attempts remain in all-attempt counts.
Interrupted calls may finish before the script exits. A resumed run uses frozen
inputs, not subsequent skill edits; use a fresh run to benchmark new changes.

To freeze and inspect inputs without model calls:

```sh
python3 scripts/benchmark.py --prepare-only
```

Use `--previous RUN/inputs/batman`, `--superpowers-source DIR`, or `--output DIR`
to choose sources or a new output directory explicitly. The output must not
already exist. A fresh checkout without the ignored local evidence needs a pinned
Superpowers source supplied as described below. Run `--help` for options.

To leave it running after closing the terminal on macOS/Linux:

```sh
nohup python3 scripts/benchmark.py > /tmp/batman-benchmark.log 2>&1 &
```

Read progress in `/tmp/batman-benchmark.log`; the computer must remain awake.

## Promptfoo workflow

This harness uses Promptfoo to run the installed Codex CLI with its existing
ChatGPT authentication. It does not need the Codex SDK or an API key. It creates
fresh temporary Git repositories containing source evidence only, captures
commands and final answers, and separately grades required outcomes.

The review cohort compares plain Codex, Batman, the Superpowers reviewer prompt
template running on Codex, and Codex's native `exec review` workflow. This is not
an evaluation of the full Superpowers orchestration or of Claude Code. Other
Batman modes compare only against plain Codex because the reviewer is not a
general-purpose incident or implementation workflow.

## Reproduce

Download `skills/requesting-code-review/code-reviewer.md` and `LICENSE` from a
pinned commit of `https://github.com/obra/superpowers`. Put them in a source
directory alongside `source.json` containing the repository URL, commit SHA,
and original template path. Do not install them into the global skill directory.

From the repository root, using a **new** run destination:

```sh
python3 evals/benchmark/prepare_run.py /tmp/my-batman-comparison \
  --superpowers-source /tmp/my-pinned-superpowers-source
cp evals/benchmark/rubric.json /tmp/my-batman-comparison/rubric.json

env -u OPENAI_API_KEY -u CODEX_API_KEY \
  PROMPTFOO_CONFIG_DIR=/tmp/my-promptfoo-state \
  PROMPTFOO_DISABLE_TELEMETRY=1 \
  promptfoo eval -c /tmp/my-batman-comparison/reviews.yaml \
    --repeat 2 --no-cache --max-concurrency 3 --no-share \
    --output /tmp/my-batman-comparison/reviews-results.json
```

Repeat the Promptfoo command with `other.yaml`, then:

```sh
python3 evals/benchmark/grade_run.py /tmp/my-batman-comparison
python3 evals/benchmark/summarize.py /tmp/my-batman-comparison
```

Freeze the rubric **before** inspecting answers. Promptfoo completion alone is
not a quality score; the separate scoreboard reports outcomes and unsupported
claims. A trial succeeds when all three scenario criteria are met and there is
no material unsupported claim. The outcome score is the fraction of essential
criteria met, expressed as a percentage. Execution failures must be reported
separately and counted as failures in any all-attempt success rate.

The grader receives randomized candidate labels, source evidence, captured
tool activity, and final implementation files where appropriate. Implementation
trials additionally receive independent behavior and helper-reuse checks.
Grades are model-assisted preliminary assessments, not independent human
validation. Audit them against the saved evidence before drawing conclusions.

## Limits

These ten author-controlled development fixtures are small and not held out.
Two repetitions measure some run variability, not generalization. A ceiling
result cannot demonstrate superiority. Requested model/settings, frozen source
hashes, source commit, and dirty working-tree status are saved in provenance.
The backend-resolved model version may not be exposed by the CLI.

All Codex executions use the same requested model and medium reasoning. The
native reviewer has its own system prompt and may report zero token usage;
that usage is unavailable, not zero cost. Concurrent execution makes elapsed
times descriptive rather than controlled latency measurements. Current global
Batman discovery is disabled explicitly; if your installation path differs,
update `codex_command` and audit traces for contamination. The host filesystem
restrictions are not a confidentiality boundary between all readable folders;
the trial instructions also prohibit parent/sibling/external inspection.

The Superpowers template is supplied as benchmark data, with its core review
instructions preserved and its task/commit placeholders filled. Only its
reviewer prompt is evaluated, not the full framework's dispatch/fix/re-review
loop. Source and license are retained with the frozen inputs. No results are
published or sent to GitHub by this harness.

## Frozen before/after efficiency experiment

See `evals/reports/2026-11-01-efficiency-plan.md` for the preregistered measures
and bounded expansion rule. Freeze the **current working-tree** SKILL.md,
LICENSE and references as `RUN/inputs/before/` before editing. Preserve status,
diff and hashes. After editing, use a new run with:

```sh
PROMPTFOO_CONFIG_DIR=/tmp/batman-promptfoo-state PROMPTFOO_DISABLE_TELEMETRY=1 \
  python3 evals/benchmark/prepare_pair.py RUN
```

This freezes the revised skill, provider, grader, fixtures and unchanged legacy
rubric. `pilot.yaml` and `heldout.yaml` use the same provider for both skills.
Run with the same authenticated Promptfoo command above, `--repeat 1` and
`--max-concurrency 2`. Run heldout only after auditing the pilot against the
expansion rule. Use `RUN/harness/grade_run.py RUN` without `--wait` (the original
wait counts describe the older four-variant experiment), then summarize and run
`python3 evals/benchmark/pair_metrics.py RUN`. Audit all answers and order traces;
model-assisted grades alone do not establish quality or instruction compliance.

`evals/validation/` contains separately labeled author-created synthetic tasks.
Only scenario `files` and the selected skill enter evaluated workspaces. The
ground-truth checks and rubric remain outside them. Filesystem read permissions
are not a confidentiality boundary; prompts forbid reading sibling/parent
folders and graders. Global skills in both standard discovery roots are disabled.
The original evidence filter omits commands containing skill reads, including
mixed commands; inspect raw traces before treating absent grader evidence as an
agent omission. Frozen v1 grades are retained; descriptive detection, explanation,
and repair audits do not silently change that rubric or earlier scores.

The paired provider wrapper allows 330 seconds to save the result of Codex's
unchanged 300-second subprocess budget. Preserve outer worker errors separately
as `RUN/execution-errors.json` with scenario, variant and error; they may have no
provider metadata. The current summarizer includes these in all-attempt counts
and derives cohort from scenario mode, including new validation tasks. Older
frozen summarizers hardcode legacy scenario names and omit outer worker errors;
do not use those summaries as overall success rates for a new suite.

## Nested global skill isolation

Hosts can discover nested SKILL.md files under a symlinked repository, including
focused skills and saved evaluation snapshots. Disabling only the top-level
Batman entry is insufficient. The provider now enumerates nested aliases and
canonical paths. For a frozen run, place the captured path list in
`harness/global-disabled-skills.json`; both trial and grader commands then use
the same list throughout execution. Audit raw commands for global skill reads,
and exclude contaminated runs. The 8 November diff-first confirmation report
records the observed contamination and matched rerun with this repair.
