# v0.1.0-beta — prepared release notes

**Unpublished draft, 15 November 2026. Release gates remain open.**

Batman provides five focused engineering skills—Investigate, Design, Challenge, Review, Execute—and a selector that chooses the appropriate skill. It helps a coding agent question assumptions, follow behavior beyond changed files, find existing implementations, and verify the intended outcome with evidence. Findings should distinguish proven defects, missing evidence, and optional improvements.

## Distribution options

A single skills-only plugin and in-repository Codex/Claude marketplace catalogs are prepared, with a clean payload excluding evaluations and tests. The [installation guide](INSTALL.md) provides namespaced plugin invocations and project-local options for 14 coding agents. Marketplace installation uses the catalogs in this GitHub repository. Existing project installation remains available. No official marketplace-directory submission has been made.

## Installation and quick start

Requires Python 3.11+ for the dependency-free installer and a working, authenticated Codex or Claude Code host for model execution:

```sh
git clone https://github.com/smhimran/batman.git
cd batman
python3 scripts/install.py --host codex --project /absolute/path/to/project
python3 scripts/install.py --host codex --project /absolute/path/to/project --check
```

Start Codex in that project:

```text
Use $batman-review to review this branch against the ticket.
Use $batman to investigate why these requests time out.
```

Use `--host claude` for `.claude/skills` and invoke `/batman-review review this branch against the ticket`; `--host both` installs both layouts. Codex uses `.agents/skills`. Identical reinstalls are unchanged; differing skills and symlinked destinations are rejected. Back up and remove a conflicting copy deliberately before reinstalling. `--check` verifies files, not host execution.

Alternatively, clone and tell your coding agent to read the absolute path of a focused `skills/batman-*/SKILL.md`. No registry, service, or global installation is required. Installed packages contain instructions, host metadata, and the MIT notice; evaluations and tests are excluded.

## Validation and limitations

The [native discovery report](evals/NATIVE_DISCOVERY.md) records actual host versions, invocation evidence, and remaining gaps. Codex CLI 0.166.0 completed all five selector routes and loaded the intended installed skills. The README's direct Review invocation also completed successfully, and Execute passed an independent check of its fixture change. Claude Code's loader detects all six project skills, but its local account is signed out and authenticated execution is unverified. Do not describe both hosts as runtime-verified.

All 44 local Python tests and 11 Node tests passed using Python 3.11.6 and Node.js 22.22.1. They cover metadata, packaging, conflict handling, references, fixtures, and benchmark tooling. The new GitHub workflow runs those suites without model calls or API keys; the baseline CI passed after correcting a test that assumed global skills existed. For the current commit's CI status, check [GitHub Actions](https://github.com/smhimran/batman/actions). See the [native report](evals/NATIVE_DISCOVERY.md) for exact host evidence and remaining gaps.

Skills guide the agent; they cannot guarantee correctness, complete discovery of bugs, or safety of a proposed change. Host tools, permissions, authentication, and model behavior affect results. Native smoke checks are small synthetic examples, not cross-platform certification or comparative evaluations. Windows and other host versions have not been verified in this preparation.

Existing [benchmark results](evals/reports/2026-11-15-investigation.md) and [methodology](evals/METHODOLOGY.md) are preserved. Fixtures are small and author-controlled; grades are model-assisted. Results do not establish general superiority; plain Codex and other reviewer configurations may perform equally well. Quality, token usage, and latency need separate evaluation. More useful investigation can justify extra tokens. No expensive benchmark was rerun for this release.

Batman-themed artwork, quotation, and naming provenance require an owner decision before publication. The MIT notice covers the project's licensed work; it does not establish third-party rights. These notes do not claim release readiness.

## Feedback and contributions

[Report an issue](https://github.com/smhimran/batman/issues) with the host/version, exact invocation, expected and actual behavior, and a minimal reproduction. Redact credentials and private source. For pull requests, explain the observed failure and checks run; preserve the focused skills, uncertainty, and honest benchmark reporting. Run:

```sh
python3 -m unittest discover -s tests -v
node --test tests/test_prompts.cjs
```

See [README contributing guidance](README.md#contributing). Licensed under [MIT](LICENSE), copyright 2026 Shah Habibul Imran, with Ponytail inspiration credited in README.

No release tag or GitHub Release existed at the initial 15 November check. Preparation commit `1827605` and CI correction `e96c172` have since been pushed at the user's request; the marketplace work adds the installation options documented above. No release or tag has been created. Recheck both before any authorized publication.
