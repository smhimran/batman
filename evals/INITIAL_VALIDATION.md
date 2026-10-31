# Initial validation — 2026-10-31

Two isolated agent trials explicitly loaded `SKILL.md` and the relevant references. Each agent received only its task, a separate fixture directory, and the skill path. Grader outcomes and sibling fixtures were excluded. These were Batman-only trials, not baseline comparisons or native installation tests.

| Trial | Observed response |
| --- | --- |
| Guardian / existing-reuse | Identified the direct email call as a confirmed preference bypass, recommended the existing dispatcher, and requested an opt-out resend regression test. Reported a focused reproduction and distinguished it from the existing dispatch test. |
| Detective / missing-evidence | Kept the database outage unconfirmed, identified both dependencies, and requested a failed request trace with dependency timings. Explicitly stated that no operational systems were queried or incident reproduction performed. |

The offline suite separately verifies the fixtures' behavior and equal task data in the baseline/Batman snapshot prompts. These narrow checks provide initial feedback on the instructions. They do not establish comparative effectiveness, false-positive rate, token overhead, or compatibility with installed Codex and Claude Code discovery.

The initial four fixtures were subsequently expanded to all eight TDD scenarios, including a correct-solution control.

Local checks: 7 Python tests and 5 Node tests passed again after disk space was freed. `git diff --check` passed. The separate skill creator `quick_validate.py` could not run because the Python environment lacks PyYAML. The offline suite checks basic frontmatter and local reference resolution, but does not replace that validator or host installation checks. Promptfoo itself has not been installed or executed here.

## Paired pilot

Four fresh agents inherited the same parent configuration, with one baseline and one Batman run per task. Both received identical task text and source files in separate, neutrally named directories. Only Batman agents received the skill path. All were instructed to keep targets read-only, use `PYTHONDONTWRITEBYTECODE=1`, and exclude sibling directories and external sources. Each trial ran once; token use, equal execution budgets, and exact model version were not independently recorded.

| Task | Baseline response | Batman response |
| --- | --- | --- |
| Correct solution | No meaningful defects; identified preference-aware delegation. Reported one passing test covering opt-in and opt-out. | No meaningful defects; identified preference-aware delegation. Reported one passing test covering opt-in and opt-out. |
| Hidden regression | P1: descending ordering advances sync to sequence 3 and skips 1 and 2; recommended UI-local ordering. | Revise, confirmed P1: same skipped-sequence mechanism; recommended preserving ascending sync and descending UI order. |

Both variants reached the expected conclusions. This pilot provides no evidence that Batman outperforms baseline. The verification above is agent-reported; raw tool traces were not exported, so it is not counted as independently verified repository inspection. Deterministic fixture tests independently reproduce the defects.

After expansion, 16 Python tests and 9 Node tests passed. The new workspace helper was exercised through its CLI and tests, including overwrite refusal, symlink refusal, and fixture-path validation.

Host checks: Claude Code reported version 2.1.114 and displayed help. Its native skill discovery was not tested. The installed Codex launcher failed with ENOENT for its native binary, preventing a local discovery test. Promptfoo is unavailable, and no provider calls or provider credentials were used.

Pending at that stage: native discovery in both hosts, the separate PyYAML-based validator, and repeated provider comparisons across the original eight scenarios with captured traces and resource metadata.

## Subsequent validation

The [16-run pilot](reports/2026-10-31-pilot.md) covers all eight scenarios that existed when it ran, with one fresh baseline and one fresh Batman agent per scenario. Both variants met the expected core conclusion in 8/8 cases. Raw final responses, fixture hashes, requested limits, and missing metadata are retained in the report. This supersedes the earlier two-pair pilot as the broadest available comparison, but still does not establish an advantage. The later Executor fixture is not included in that pilot.

[Native discovery](NATIVE_DISCOVERY.md) now confirms Claude Code's project skill loader recognizes Batman. The control loaded zero skills and rejected `/batman`; the installed case loaded one project skill and reached execution setup before authentication and configuration-access errors. Authenticated execution is still unverified. Codex discovery is still blocked by its launcher, and the app-bundled executable was denied execution.

The project-local installer was exercised with both hosts in a fresh workspace and checked for identical copies. Its tests cover existing-skill preservation, preflight before writes, check-only behavior, and symlink refusal. After adding these checks, 20 Python tests and 9 Node tests passed. No Promptfoo provider run completed, no API credentials were configured, and no global CLI installation or user-level skills were changed.
