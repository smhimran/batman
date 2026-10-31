# Batman

An evidence-driven engineering skill for coding agents. Understand the problem, investigate the system, challenge assumptions, and verify the outcome.

Batman focuses on whether a change solves the actual need, what existing code can be reused, and which consumers could break outside the diff. It also investigates incidents without turning guesses into root causes.

## Use

The core is Markdown with no runtime dependencies. Clone this repository and tell your agent:

```text
Read /absolute/path/to/batman/SKILL.md and use Batman to review this branch.
```

For native project-local discovery, copy the core files with the optional installer:

```sh
python3 scripts/install.py --host both --project /absolute/path/to/project
python3 scripts/install.py --host both --project /absolute/path/to/project --check
```

Choose `codex`, `claude`, or `both`. The installer uses `.agents/skills/batman/` for Codex and `.claude/skills/batman/` for Claude. It leaves identical copies unchanged and refuses to overwrite a different existing skill. `--check` verifies installed bytes; it does not prove native discovery. No runtime CLI for Batman is included.

In the chosen project, invoke `$batman` in Codex or `/batman` in Claude Code. See [native discovery results](evals/NATIVE_DISCOVERY.md) for the tested hosts and remaining blockers.

| Request | Mode |
| --- | --- |
| `batman investigate`: explain a bug or incident | Detective |
| `batman design`: choose a practical solution | Strategist |
| `batman challenge`: test assumptions in a proposal | Challenger |
| `batman review`: assess a PR, diff, or implementation | Guardian |
| `batman execute`: implement and verify a task | Executor |

Examples:

```text
Use Batman Guardian at Standard depth. Does this branch solve the ticket,
and could it break callers outside the diff?

Use Batman Detective. Notifications timed out after deployment.
Investigate the evidence and ask for any specific missing data.

Use Batman Executor to fix the confirmed regression and verify existing behavior.
```

Standard is the default depth. Choose Quick for narrow work or Deep for broader investigation. Batman loads shared principles and the selected mode, using the agent's existing tools. Reviews and investigations stay read-only unless changes are requested. An implementation request supplies authorization within its scope.

## Development and evaluation

Run offline checks with Python 3 and Node.js:

```sh
python3 -m unittest discover -s tests -v
node --test tests/test_prompts.cjs
```

These verify packaging, prompt parity, and the fixtures' known behavior. They do not measure model quality. See [evaluation methodology](evals/METHODOLOGY.md) for the optional Promptfoo comparison, grading rubric, and tool-use follow-up. Promptfoo and provider credentials are needed only for that evaluation, not for the skill itself.

Nine fixtures cover reuse, an unchanged consumer regression, misleading requirements, missing evidence, a correct solution, incomplete implementation, overengineering, an incident with retry evidence, and an idempotent implementation task. See [examples](examples/workflows.md) for expected communication style.

Prepare a clean tool-use trial without copying grader answers into the workspace:

```sh
python3 evals/prepare.py list
python3 evals/prepare.py prepare hidden-regression /tmp/batman-trial-a
```

The destination must be new and its parent must exist. The helper prints the task and workspace path; it writes only source evidence. Use separate fresh directories for baseline and Batman. It never resets or overwrites an existing checkout.

## Status and limitations

This is an initial implementation of the v0.1 TDD. All five workflows and nine benchmark fixtures are present. The historical [16-run pilot](evals/reports/2026-10-31-pilot.md) found the expected core conclusion in its original 8/8 scenarios for both baseline and Batman; the newer Executor fixture has not received a paired pilot run. No advantage over baseline is demonstrated. Raw responses and limitations are included in the report.

Claude Code project-local discovery is confirmed; authenticated skill execution remains unverified. Codex native discovery is blocked by the local CLI installation. Promptfoo provider runs remain pending. See [native discovery](evals/NATIVE_DISCOVERY.md) and [initial validation](evals/INITIAL_VALIDATION.md) for exact scope and evidence.

Batman depends on the host's context, tools, permissions, and model judgment. It cannot guarantee bug detection or access unavailable logs, tickets, or services. No automated PR posting, dedicated CLI, external integrations, persistent state, or multi-agent orchestration is included.

## Contributing

Prefer concise instructions and concrete behavioral examples. For a proposed rule, explain which failure it prevents and add a controlled fixture where practical. Keep expected answers separate from evaluated context. Run the offline checks, report any behavioral trials accurately, and avoid adding dependencies to the core skill.

Licensed under [MIT](LICENSE).
