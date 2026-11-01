# Batman

**Evidence-driven engineering for coding agents.** Investigate the problem, follow the relevant code and consumers, and verify what actually happens.

Batman is a portable Markdown skill for reviewing changes, investigating incidents, designing solutions, challenging assumptions, and implementing fixes. It helps an agent ask whether a change meets the real requirement, whether existing code already solves the problem, and what could break beyond the diff.

The core skill has no runtime dependencies. It uses the host agent's model, tools, context, and permissions.

## Quick start

Clone the repository:

```sh
git clone https://github.com/smhimran/batman.git
cd batman
```

Then give your coding agent a task with the skill's absolute path:

```text
Read /absolute/path/to/batman/SKILL.md and use Batman to review this branch.
Check the requirement, affected consumers, and regression risks.
```

This direct approach works without installing a separate Batman command or service.

### Optional project-local installation

From this repository, install the core files into an existing project:

```sh
python3 scripts/install.py --host codex --project /absolute/path/to/project
python3 scripts/install.py --host codex --project /absolute/path/to/project --check
```

Choose `--host codex`, `--host claude`, or `--host both`:

| Host | Installation directory | Invocation |
| --- | --- | --- |
| Codex | `.agents/skills/batman/` | `$batman` |
| Claude Code | `.claude/skills/batman/` | `/batman` |

The installer copies `SKILL.md`, mode references, agent metadata, and the license. It excludes evaluation fixtures and grader answers. Identical installations stay unchanged; differing installations and symlinked destinations are rejected rather than overwritten. To update a differing copy, back it up and remove it before reinstalling.

`--check` verifies file contents, not discovery or execution. Host behavior depends on the installed version and configuration. See the dated [native discovery observations](evals/NATIVE_DISCOVERY.md); the later CLI benchmarks use explicit skill-loading instructions and do not establish native invocation behavior for every host.

## Choose a workflow

Batman selects a mode from your task. You can also name it explicitly.

| Mode | Use it to… | Example request |
| --- | --- | --- |
| **Detective** | Investigate a bug or incident and distinguish hypotheses from evidence. | “Investigate these timeouts. What is established, and which evidence would distinguish the causes?” |
| **Strategist** | Design the simplest solution that meets the actual constraints. | “Design daily exports using the existing code where practical.” |
| **Challenger** | Test a proposal's assumptions and necessity. | “Challenge this cache proposal against our consistency requirement.” |
| **Guardian** | Review requirements, affected consumers, correctness, and regression safety. | “Review this branch against the ticket, including callers outside the diff.” |
| **Executor** | Implement a scoped change and verify meaningful behavior. | “Fix the confirmed retry bug and add regression coverage.” |

For example:

```text
Use Batman Guardian at Standard depth to review this branch against the ticket.
Inspect the relevant source and consumer contracts before the diff. Give concrete
repair recommendations for demonstrated defects and accept correct implementations.
```

Depth controls exploration, not evidence standards:

- **Quick:** narrow tasks with limited impact.
- **Standard:** the default; relevant context, alternatives, and regressions.
- **Deep:** broader impact, unclear contracts, security, data integrity, or difficult incidents.

The agent reads shared principles and the relevant mode reference. You do not need to load every workflow. See [workflow examples](examples/workflows.md) for sample communication.

## Engineering principles

- **Verify consequential claims.** Separate observed behavior from hypotheses and missing information. Do not invent requirements, logs, access, or test results.
- **Understand the contract.** In reviews, inspect relevant source and consumer behavior before diff content; widen exploration when dependencies or risk warrant it.
- **Reuse with evidence.** Inspect existing helpers and alternatives before proposing another implementation. Accept a correct solution without manufacturing objections.
- **Make findings useful.** Explain the trigger, realistic consequence, inspected evidence, and a concrete repair or next check.
- **Verify actual behavior.** Use focused reproductions and meaningful regression checks; passing output tests alone may not establish compatibility or efficiency.
- **Keep effort proportional.** Avoid repeated discovery and checks once the decision has sufficient evidence.

Reviews, investigations, and design work remain read-only unless changes are requested. An implementation request authorizes changes within its scope. Batman grants no additional permissions and does not automatically post reviews, deploy, or publish.

These are instructions to a model, not enforced guarantees. The benchmarks show that loading the skill does not ensure every step is followed.

## What the benchmarks show

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
| [`SKILL.md`](SKILL.md) | Skill entry point and workflow selection |
| [`references/`](references/) | Shared principles and five mode workflows |
| [`agents/`](agents/) | Agent interface metadata |
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
