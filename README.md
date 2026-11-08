# Batman

Five focused skills for investigating, planning, questioning, reviewing, and fixing software. Read the relevant code, choose the smallest complete solution, and check what actually happens.

Each skill works on its own. There is no runtime dependency: it uses the coding agent's existing tools and permissions.

## Choose a skill

| Skill | Use it for | Old mode |
| --- | --- | --- |
| [batman-investigate](skills/batman-investigate/SKILL.md) | Find why a bug or incident happened | Detective |
| [batman-design](skills/batman-design/SKILL.md) | Plan a change that fits the need and existing code | Strategist |
| [batman-challenge](skills/batman-challenge/SKILL.md) | Test whether a proposal is needed and its assumptions hold | Challenger |
| [batman-review](skills/batman-review/SKILL.md) | Find concrete bugs, missed requirements, and broken callers | Guardian |
| [batman-execute](skills/batman-execute/SKILL.md) | Make a complete change and check the result | Executor |

Use a focused skill directly:

```text
Use $batman-review to review this branch against the ticket.
Use $batman-investigate to find why these requests time out.
Use $batman-execute to fix the retry bug and check the affected callers.
```

`$batman` still selects a skill from the task and understands the old mode names. Quick, Standard, and Deep requests still control how far it explores. Evidence matters at every depth.

The rewrite takes inspiration from [Ponytail](https://github.com/DietrichGebert/ponytail/tree/main/skills): short instructions, plain words, and the smallest change that finishes the job. Reviews read the diff first, then the ticket and requirements, then relevant source code and tests as needed. Findings still need concrete evidence, including affected behavior outside the diff.

## Use without installing

Clone this repository, then give your coding agent the absolute path of a skill:

```sh
git clone https://github.com/smhimran/batman.git
cd batman
```

```text
Read /absolute/path/to/batman/skills/batman-review/SKILL.md and use it to review this branch.
```

The root `SKILL.md` is a compatibility entry point for existing paths. The installable skills live in `skills/`.

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

The installer includes skill instructions, agent metadata, and the license. It excludes evaluations, tests, and scripts. It checks all destinations before writing. Identical copies stay unchanged; differing copies and symlinked destinations are preserved and reported as conflicts. To update an old copy, back it up and remove it before reinstalling.

`--check` verifies copied contents, not host discovery or execution. The dated [discovery observations](evals/NATIVE_DISCOVERY.md) describe the earlier single-skill layout; they do not verify discovery of this split layout.

## What the skills keep

- Check important claims against code or actual results. Keep facts separate from guesses.
- Follow affected callers and existing behavior. A changed-file list is only a starting point.
- Reuse code when it does the whole job. Avoid features and layers nobody needs.
- Give findings a real trigger, user impact, evidence, and a useful repair.
- Run focused checks and report actual results. Stop repeating checks once they answer the question.

Reviews, investigations, proposals, and plans stay read-only unless changes are requested. An implementation request authorizes work within its scope. The skills grant no extra permission to post, deploy, or publish.

## What the benchmarks show

These results describe earlier versions of the combined skill. They do not measure this rewrite or the split skills. Shorter instructions alone do not prove lower token use or better results.

The latest [80-trial rerun](evals/reports/2026-11-01-rerun.md) used fresh Codex sessions, the same requested model and reasoning settings, ten development fixtures, and two repetitions. It compared the previous and revised skill alongside plain Codex and, for reviews, two reviewer approaches.

The revised skill preserved the measured task outcomes and matched the comparison reviewers on the frozen review rubric. **Every review variant identified the same core defects or accepted the correct-code control.** Numerical differences from plain Codex primarily concern reuse and explicit repair recommendations, rather than unique defect detection.

| Previous → revised Batman | Result |
| --- | --- |
| Overall median reported tokens | 104,648 → 100,455, a 4.0% decrease |
| Review median reported tokens | 6.6% lower |
| Broader-task median reported tokens | 17.3% higher |
| Strict context-before-diff compliance | 9/10 → 7/10 review trials |

The 15% token-reduction target was missed. The revision did not demonstrate a reliable efficiency or inspection-order improvement. Reported tokens include cached input and are not subscription charges.

These are small, author-controlled development fixtures with model-assisted grading, not independent real-world benchmarks. They do not establish general superiority or a population false-positive rate. The Superpowers comparison evaluates its pinned reviewer template on Codex, not its full orchestration framework. Authenticated Claude Code execution was not compared.

Additional evidence:

- [Original comparison pilot](evals/reports/2026-11-01-comparison.md): outcome scores, repair-specificity distinctions, and overhead.
- [Focused before/after experiment](evals/reports/2026-11-01-efficiency.md): predefined measures, execution failures, and validation limitations.
- [Trace and grading audit](evals/reports/2026-11-01-pilot-audit.md): useful verification versus avoidable overhead.
- [Validation task limitations](evals/validation/KNOWN_LIMITATIONS.md): synthetic task provenance and the ambiguous cache control.

Raw trial bundles are excluded from Git. Reports identify their local evidence locations; those bundles must be shared separately for a complete trace audit.

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
| [`SKILL.md`](SKILL.md) | Compatibility entry point |
| [`skills/`](skills/) | Five standalone skills and the Batman selector |
| [`agents/`](agents/) | Compatibility entry point metadata |
| [`scripts/install.py`](scripts/install.py) | Optional project-local installer |
| [`examples/`](examples/) | Workflow and communication examples |
| [`tests/`](tests/) | Offline behavioral and packaging checks |
| [`evals/benchmark/`](evals/benchmark/) | Authenticated CLI comparison harness |
| [`evals/scenarios/`](evals/scenarios/) | Original ten development fixtures |
| [`evals/validation/`](evals/validation/) | Additional synthetic tasks, ground truth, and validity notes |
| [`evals/reports/`](evals/reports/) | Results, audits, and limitations |

## Contributing

Prefer concise instructions that change an engineering decision over longer checklists. Explain the observed failure behind a proposed rule, preserve uncertainty and useful repair guidance, and add behavioral coverage where it helps. Keep expected answers separate from evaluated context and label synthetic or author-created tasks honestly.

Run the offline checks and report behavioral trials with their actual limits. Do not optimize instructions for grader keywords, change grading to manufacture a win, or claim verification that did not run.

## License

[MIT](LICENSE).
