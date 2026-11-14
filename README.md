# Batman

Five focused skills for investigating, planning, questioning, reviewing, and fixing software. Read the relevant code, choose the smallest complete solution, and check what actually happens.

Each skill works on its own. There is no runtime dependency: it uses the coding agent's existing tools and permissions.

## Choose a skill

| Skill | Use it for |
| --- | --- |
| [batman-investigate](skills/batman-investigate/SKILL.md) | Find why a bug or incident happened |
| [batman-design](skills/batman-design/SKILL.md) | Plan a change that fits the need and existing code |
| [batman-challenge](skills/batman-challenge/SKILL.md) | Test whether a proposal is needed and its assumptions hold |
| [batman-review](skills/batman-review/SKILL.md) | Find concrete bugs, missed requirements, and broken callers |
| [batman-execute](skills/batman-execute/SKILL.md) | Make a complete change and check the result |

Use a focused skill directly:

```text
Use $batman-review to review this branch against the ticket.
Use $batman-investigate to find why these requests time out.
Use $batman-execute to fix the retry bug and check the affected callers.
```

`$batman` selects a skill from the task. Quick, Standard, and Deep requests control how far it explores. Evidence matters at every depth.

Batman takes inspiration from [Ponytail](https://github.com/DietrichGebert/ponytail/tree/main/skills): short instructions, plain words, and the smallest change that finishes the job. Reviews read the diff first, then the ticket and requirements, then relevant source code and tests as needed. Findings need concrete evidence, including affected behavior outside the diff.

## Use without installing

Clone this repository, then give your coding agent the absolute path of a skill:

```sh
git clone https://github.com/smhimran/batman.git
cd batman
```

```text
Read /absolute/path/to/batman/skills/batman-review/SKILL.md and use it to review this branch.
```

The root `SKILL.md` provides the Batman selector. The installable skills live in `skills/`.

## Optional project installation

Install the five skills and the Batman selector into an existing project:

```sh
python3 scripts/install.py --host codex --project /absolute/path/to/project
python3 scripts/install.py --host codex --project /absolute/path/to/project --check
```

Choose `--host codex`, `--host claude`, or `--host both`:

| Host | Installation directory | Example invocation |
| --- | --- | --- |
| Codex | `.agents/skills/batman-*/` and `.agents/skills/batman/` | `$batman-review` |
| Claude Code | `.claude/skills/batman-*/` and `.claude/skills/batman/` | `/batman-review` |

The installer includes skill instructions, agent metadata, and the license. It excludes evaluations, tests, and scripts. It checks all destinations before writing. Identical copies stay unchanged; differing copies and symlinked destinations are preserved and reported as conflicts. To replace a conflicting copy, back it up and remove it before reinstalling.

`--check` verifies copied contents, not host discovery or execution.

## How the skills work

- Check important claims against code or actual results. Keep facts separate from guesses.
- Follow affected callers and existing behavior. A changed-file list is only a starting point.
- Reuse code when it does the whole job. Avoid features and layers nobody needs.
- Give findings a real trigger, user impact, evidence, and a useful repair.
- Run focused checks and report actual results. Stop repeating checks once they answer the question.

Reviews, investigations, proposals, and plans stay read-only unless changes are requested. An implementation request authorizes work within its scope. The skills grant no extra permission to post, deploy, or publish.

## What the benchmarks show

The [benchmark report](evals/reports/2026-11-08-diff-first.md) evaluates the skills using fresh Codex sessions, the same requested `gpt-6-sol` model with medium reasoning, ten development fixtures, and two repetitions per task and variant.

| Review approach | Rubric score / 100 | Median reported tokens |
| --- | ---: | ---: |
| Batman | 96.7 | 82,941 |
| Plain Codex | 86.7 | 76,773.5 |
| Superpowers reviewer template on Codex | 100.0 | 86,377.5 |
| Codex built-in reviewer | 96.7 | Unavailable |

The Batman reviewer used about **8% more median tokens than plain Codex** and **4% fewer than the Superpowers template**. Its one rubric deduction concerned offering a duplicated preference check alongside reuse, rather than a missed defect. The rubric also measures explanation and repair completeness; it is not a pure bug-detection score.

Broader tasks scored **96.7/100**. Reported token counts include cached input and are not subscription charges. Native review usage counters were unavailable.

The benchmark harness disables global skill aliases and canonical paths using a frozen manifest to keep comparator runs isolated from installed Batman instructions. The report includes execution accounting and isolation checks.

These are small, author-controlled development fixtures with model-assisted grading, not independent real-world benchmarks. They do not establish general superiority, statistical significance, or a population false-positive rate. Superpowers means its pinned reviewer template on Codex, not its full orchestration framework. Authenticated Claude Code execution was not compared.

See [validation task limitations](evals/validation/KNOWN_LIMITATIONS.md) for synthetic task provenance and the ambiguous cache control. Raw trial bundles are excluded from Git. Reports identify their local evidence locations; share those bundles separately for a complete trace audit.

## Development and evaluation

Run the offline checks from the repository root with Python 3 and Node.js:

```sh
python3 -m unittest discover -s tests -v
node --test tests/test_prompts.cjs
```

These check packaging, installation behavior, source-only workspace preparation, fixture behavior, prompt parity, and benchmark reporting. They do not establish model reasoning quality.

Prepare an isolated source-only task:

```sh
python3 evals/prepare.py list
python3 evals/prepare.py prepare hidden-regression /tmp/batman-trial-a
```

The destination must be new and its parent must exist. The helper prints the task separately and refuses to overwrite an existing workspace.

For behavioral comparisons, follow the [benchmark guide](evals/benchmark/README.md). It uses Promptfoo and the authenticated Codex CLI; **no API key is required for that harness**. The separate snapshot evaluation in [evaluation methodology](evals/METHODOLOGY.md) uses configured provider credentials and measures reasoning over supplied context rather than tool use.

Freeze skills, tasks, settings, and grading criteria before execution. Keep grader answers outside evaluated workspaces, disable global discovery that could contaminate comparisons, audit actual traces, and count execution failures. Model-assisted grades need review; completion is not a quality score.

## Repository guide

| Path | Purpose |
| --- | --- |
| [`SKILL.md`](SKILL.md) | Batman selector entry point |
| [`skills/`](skills/) | Five standalone skills and the Batman selector |
| [`agents/`](agents/) | Batman selector metadata |
| [`scripts/install.py`](scripts/install.py) | Optional project-local installer |
| [`examples/`](examples/) | Workflow and communication examples |
| [`tests/`](tests/) | Offline behavioral and packaging checks |
| [`evals/benchmark/`](evals/benchmark/) | Authenticated CLI comparison harness |
| [`evals/scenarios/`](evals/scenarios/) | Ten development fixtures |
| [`evals/validation/`](evals/validation/) | Additional synthetic tasks, ground truth, and validity notes |
| [`evals/reports/`](evals/reports/) | Results, audits, and limitations |

## Contributing

Prefer concise instructions that change an engineering decision over longer checklists. Explain the observed failure behind a proposed rule, preserve uncertainty and useful repair guidance, and add behavioral coverage where it helps. Keep expected answers separate from evaluated context and label synthetic or author-created tasks honestly.

Run the offline checks and report behavioral trials with their actual limits. Do not optimize instructions for grader keywords, change grading to manufacture a win, or claim verification that did not run.

## License

[MIT](LICENSE).
