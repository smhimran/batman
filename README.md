# Batman

<p align="center">
  <img src="assets/batman-emblem.png" alt="Batman coding emblem" width="560">
</p>

<p align="center">
  <em>"It's not who I am underneath, but what I do that defines me."</em>
</p>

Batman is a collection of five evidence-driven software engineering skills and a selector for coding agents, including Codex, Claude Code, Cursor, Copilot, Gemini CLI, and OpenCode. It helps your coding agent investigate bugs, design changes, challenge proposals, review code, and implement fixes.

A diff-focused review can miss an unmet requirement in unchanged code. Batman asks what must happen, follows affected callers and existing helpers, and supports findings with source, logs, or focused checks. Expect concrete findings, repair guidance, and honest statements about what remains unknown—not guaranteed correctness.

## Install

### Codex

Run these in your terminal:

```sh
codex plugin marketplace add smhimran/batman
codex plugin add batman@batman
```

Restart Codex or the desktop app, open your project, and invoke:

```text
Use $batman:batman-review to review this branch against the ticket.
```

### Claude Code

Send these as **two separate prompts** in Claude Code:

```text
/plugin marketplace add smhimran/batman
```

```text
/plugin install batman@batman
```

Start a new session in your project and invoke:

```text
/batman:batman-review review this branch against the ticket
```

Use `batman:batman` instead of `batman:batman-review` to let the selector choose a skill. A working, signed-in host is required. If your version lacks these plugin commands, update the host or use the project-local installer below.

### Other coding agents

The [installation guide](INSTALL.md) covers project-local installation for Cursor, Copilot, Gemini CLI, OpenCode, Cline, Roo Code, Kiro, Kimi Code, Pi, Antigravity, Windsurf compatibility, and Devin, plus manual use with other models. Additional host layouts are checked offline; their native runtime behavior remains unverified. Codex execution is verified; Claude installation/discovery is verified, with authenticated execution still unverified. See the [compatibility evidence](evals/NATIVE_DISCOVERY.md).

These commands install from Batman's own GitHub-hosted marketplace, not an official-directory listing. Choose either the plugin or the project-local install for each host to avoid duplicate skills. Plugin invocations are namespaced; the project-local examples below use standalone names.

## Quick start (project-local)

Clone Batman and install it into an existing project (Python 3.11+):

```sh
git clone https://github.com/smhimran/batman.git
cd batman
python3 scripts/install.py --host codex --project /absolute/path/to/project
```

Start Codex in that project and invoke:

```text
Use $batman-review to review this branch against the ticket.
```

For Claude Code, replace `--host codex` with `--host claude` and invoke `/batman-review review this branch against the ticket`. Use `--host both` to install both layouts. A signed-in host is required for model execution; see [verified host status and remaining gaps](evals/NATIVE_DISCOVERY.md). The installer has no third-party Python dependencies, and the skills use the host's existing tools and permissions.

### Example: a passing diff can still miss the requirement

**Illustrative example, not a benchmark result.** A ticket says archived groups must reject all edits while existing expenses remain readable. A patch blocks renaming an archived group and adds a passing rename test.

| Review scope | What it sees |
| --- | --- |
| Changed lines and their test | The rename guard works. |
| Requirement plus affected callers | The unchanged `create_expense` still accepts expenses for archived groups. Guard that mutation too, then verify reads still work. |

## Choose a skill

| Skill | Use it for |
| --- | --- |
| [batman-investigate](skills/batman-investigate/SKILL.md) | Reconstruct the failure and test competing explanations |
| [batman-design](skills/batman-design/SKILL.md) | Plan for the required outcome, credible failures, and recovery |
| [batman-challenge](skills/batman-challenge/SKILL.md) | Question assumptions and complexity without dropping requirements |
| [batman-review](skills/batman-review/SKILL.md) | Check the outcome, affected behavior, and opportunities for reuse |
| [batman-execute](skills/batman-execute/SKILL.md) | Implement the smallest complete change and verify its behavior |

Use a focused skill directly:

```text
Use $batman-review to review this branch against the ticket.
Use $batman-investigate to find why these requests time out.
Use $batman-execute to fix the retry bug and check the affected callers.
```

`$batman` selects a skill from the task. Quick, Standard, and Deep requests control how far it explores. Evidence matters at every depth.

Batman takes inspiration from [Ponytail](https://github.com/DietrichGebert/ponytail/tree/main/skills): short instructions, plain words, and the smallest change that finishes the job. Reviews read the diff first, then the ticket and requirements, then relevant source code and tests as needed. Findings need concrete evidence, including affected behavior outside the diff.

## Use without installing

After cloning, give your coding agent the absolute path of a skill:

```text
Read /absolute/path/to/batman/skills/batman-review/SKILL.md and use it to review this branch.
```

The root `SKILL.md` provides the Batman selector. The installable skills live in `skills/`.

## Optional project installation

The quick-start installer copies the five skills and Batman selector. Verify an existing installation with:

```sh
python3 scripts/install.py --host codex --project /absolute/path/to/project --check
```

Choose a host such as `codex`, `claude`, `cursor`, `copilot`, `gemini`, or `opencode`; see the [full host table](INSTALL.md#project-local-installation-for-other-coding-agents). `--host both` still means Codex plus Claude. `--host all` installs every distinct supported layout.

| Host | Installation directory | Example invocation |
| --- | --- | --- |
| Codex | `.agents/skills/batman-*/` and `.agents/skills/batman/` | `$batman-review` |
| Claude Code | `.claude/skills/batman-*/` and `.claude/skills/batman/` | `/batman-review` |

The installer includes skill instructions, agent metadata, and the license. It excludes evaluations, tests, and scripts. It checks all destinations before writing. Identical copies stay unchanged; differing copies and symlinked destinations are preserved and reported as conflicts. To replace a conflicting copy, back it up and remove it before reinstalling.

`--check` verifies copied contents, not host discovery or execution.

## How the skills work

- Establish success independently of the proposed implementation.
- Trace behavior beyond changed files; test explanations against contrary evidence.
- Reuse existing code after checking its behavior and failure handling against the requirement.
- Plan safeguards and recovery for credible risks, proportional to their impact.
- State what the evidence demonstrates and what remains unverified. Stop when the question is settled.

These instructions guide the agent's work; they cannot guarantee correctness or prevent every failure. A clean diff or passing test suite alone does not establish that the user's goal was reached.

Reviews, investigations, proposals, and plans stay read-only unless changes are requested. An implementation request authorizes work within its scope. The skills grant no extra permission to post, deploy, or publish.

## What the benchmarks show

The [15 November benchmark report](evals/reports/2026-11-15-investigation.md) records 80 completed trials with zero execution failures. These are small, author-controlled fixtures with model-assisted grades; they do not establish general superiority. Plain Codex matched Batman on broader tasks, and other reviewer configurations matched its review score.

Batman used more reported tokens in that run. Additional useful investigation can justify extra tokens; assess quality, tokens, and latency separately. Reported tokens include cached input and are not subscription charges. Authenticated Claude Code execution was not compared.

See the [full results and audit](evals/reports/2026-11-15-investigation.md), [methodology](evals/METHODOLOGY.md), and [fixture limitations](evals/validation/KNOWN_LIMITATIONS.md). Historical reports remain intact. Raw trial bundles are excluded from Git and must be shared separately for a complete trace audit.

## Development and evaluation

Run the offline checks from the repository root with Python 3.11+ and Node.js 22+ (CI uses Python 3.11 and Node.js 22):

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

Run the full behavioral comparison from a terminal without opening the Codex desktop app:

```sh
python3 scripts/benchmark.py
```

This uses the installed, signed-in Codex CLI and saves a timestamped report and evidence in `evals/results/`. It can resume interrupted runs. See the [benchmark guide](evals/benchmark/README.md) for options, prerequisites, and the alternative Promptfoo workflow. **No API key is required for this harness.** The separate snapshot evaluation in [evaluation methodology](evals/METHODOLOGY.md) uses configured provider credentials and measures reasoning over supplied context rather than tool use.

Freeze skills, tasks, settings, and grading criteria before execution. Keep grader answers outside evaluated workspaces, disable global discovery that could contaminate comparisons, audit actual traces, and count execution failures. Model-assisted grades need review; completion is not a quality score.

## Repository guide

| Path | Purpose |
| --- | --- |
| [`SKILL.md`](SKILL.md) | Batman selector entry point |
| [`skills/`](skills/) | Five standalone skills and the Batman selector |
| [`agents/`](agents/) | Batman selector metadata |
| [`scripts/install.py`](scripts/install.py) | Optional project-local installer |
| [`INSTALL.md`](INSTALL.md) | Marketplace and cross-agent installation instructions |
| [`plugins/batman/`](plugins/batman/) | Clean generated marketplace payload |
| [`scripts/build_plugin.py`](scripts/build_plugin.py) | Build/check the marketplace payload |
| [`examples/`](examples/) | Workflow and communication examples |
| [`tests/`](tests/) | Offline behavioral and packaging checks |
| [`evals/benchmark/`](evals/benchmark/) | Authenticated CLI comparison harness |
| [`evals/scenarios/`](evals/scenarios/) | Ten development fixtures |
| [`evals/validation/`](evals/validation/) | Additional synthetic tasks, ground truth, and validity notes |
| [`evals/reports/`](evals/reports/) | Results, audits, and limitations |

## Contributing

[Open an issue](https://github.com/smhimran/batman/issues) with the host/version, invocation, expected behavior, actual behavior, and a minimal reproduction. Remove credentials and private code from shared logs. Pull requests should explain the observed problem and checks run. See the [beta release notes](RELEASE_NOTES.md) for validation status and release gates.

Prefer concise instructions that change an engineering decision over longer checklists. Explain the observed failure behind a proposed rule, preserve uncertainty and useful repair guidance, and add behavioral coverage where it helps. Keep expected answers separate from evaluated context and label synthetic or author-created tasks honestly.

Run the offline checks and report behavioral trials with their actual limits. Do not optimize instructions for grader keywords, change grading to manufacture a win, or claim verification that did not run.

## License

[MIT](LICENSE), copyright 2026 Shah Habibul Imran. Inspired by [Ponytail](https://github.com/DietrichGebert/ponytail/tree/main/skills). Branding and quotation provenance still need review; see the [release limitations](RELEASE_NOTES.md#validation-and-limitations). No affiliation or endorsement is claimed.
