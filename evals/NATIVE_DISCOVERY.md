# Native installation and discovery — 15 November 2026

## Scope and environment

Tested on macOS with Python 3.11.6, Node.js 22.22.1, Codex CLI 0.166.0, and Claude Code 2.1.114. Temporary Git projects received fresh project-local installations. No user-level skills were installed or replaced. These checks exercise a small synthetic fixture, not a comparative model benchmark or a guarantee of reasoning quality.

The layout agrees with the official [Codex skills documentation](https://developers.openai.com/codex/skills/) and [Claude Code skills documentation](https://code.claude.com/docs/en/skills). Documented support is not a substitute for the observations below.

## Installation checks for both hosts

The public installer CLI completed with `--host both` in a new empty project: all twelve skill destinations reported `installed`. Repeating the command reported all twelve `unchanged`; `--check` also reported all twelve unchanged. Each package contains only `SKILL.md`, `agents/openai.yaml`, and the MIT `LICENSE`. No evaluation, benchmark, test, or script files entered the packages. Relative links from the installed selector resolve to all five sibling skills.

A separate project contained a conflicting `.claude/skills/batman-execute/SKILL.md`. The CLI exited 1 without changing that file or creating any `.agents` destination. Offline tests also cover symlinked parents/source files, missing checks, early/late conflicts, and both-host preflight. Installation byte checks establish package integrity, not host invocation.

## Codex

`codex --version` returned `codex-cli 0.166.0`; `codex login status` reported a ChatGPT login. The first restricted attempt failed before model execution with an app-server permission error. Retrying the same read-only fixture with the normal execution environment completed a model turn: Codex read the local selector and its relative review link and identified an unguarded archived-group mutation. Its attempted runtime check used unavailable `python`, so that first response relied on source and explicitly reported the limitation.

A no-model-call discovery check used `codex app-server` and its schema-documented `skills/list` method with the fixture project as `cwds` and `forceReload: true`. The response listed all six Batman skills with `scope: repo`, `enabled: true`, exact paths under the project's `.agents/skills/`, and no loader errors. This establishes native discovery independently of the model's self-report.

A subsequent set uses the repository's existing `evals/benchmark/provider.py::codex_command` only as a command builder. It disables discovered global skills, ignores user configuration, uses ephemeral sessions, and writes traces outside the repository. Each task receives a separate project containing the installed six packages and only two fixture files:

```python
# group.py
def add_expense(group, expense):
    group["expenses"].append(expense)

def expenses(group):
    return group["expenses"]
```

`requirement.txt` says: `Archived groups must reject new expenses. Existing expenses remain readable.` The fixture does not define an archive-field contract or error convention. Design responses must distinguish their proposed conventions from established requirements.

Every prompt starts `Use $batman to ...`, requests Quick depth, asks the selector to follow its installed relative link, restricts work to the fixture, prohibits delegation, and names `python3` for runtime checks. The requested model is `gpt-6-sol` with medium reasoning. Read-only tasks use the host's read-only setting; only Execute permits project writes.

| Task | Observed route and behavior |
| --- | --- |
| Review `group.py` against the requirement | Read local `batman` and `batman-review`; reproduced the missing archive guard with `python3`. Also demonstrated mutation through the returned list. |
| Investigate why archived groups accept expenses | Read local `batman` and `batman-investigate`; reproduced unconditional append and noted the undefined archive-state contract. |
| Design a minimal fix | Read local `batman` and `batman-design`; proposed a guard and checks while labeling archive-field/error conventions as assumptions. |
| Challenge a plugin framework proposal | Read local `batman` and `batman-challenge`; reproduced the defect and recommended a narrow guard instead of a framework. |
| Execute the fix | Read local `batman` and `batman-execute`; added an archive guard and ran `python3` checks for rejection, active additions, and preserved reads. |

All five model calls exited 0 with completed turns. An independent Python 3 check of Execute's final file passed archived rejection, no mutation on rejection, active additions, and preserved reads. Its `group.get("archived", False)` / `ValueError` convention was a choice for this smoke fixture, not a verified production contract. The mutable-list accessor remains unchanged; the smoke check does not prove enforcement against callers that mutate that list directly.

The four read-only source fixtures were byte-compared afterward and remained unchanged. Successful reads of sibling skill files verify the installed relative references at runtime. This checks explicit selector invocation and selected focused-skill execution; it does not exhaustively test automatic selection, interactive menus, every alias/depth, all operating systems, or every possible task. Global skills were disabled for the five-route set, and captured commands were inspected for actual local skill reads rather than relying on filenames or model self-report alone.

A separate fresh Codex call tested the README's direct form: `Use $batman-review to review group.py against requirement.txt.` No skill path or instruction to read a skill was supplied. With global skills disabled, the model turn completed with exit 0 and identified the missing guard. This trace does not include an explicit skill-file read, so it cannot by itself prove how the host loaded the skill. Native discovery is established separately by the inventory above. Other direct focused invocation forms were not separately exercised.

## Claude Code

`claude --version` returned `2.1.114 (Claude Code)`. `claude auth status` reported `loggedIn: false`, `authMethod: none`. In a fresh installed project, ran:

```sh
claude -p '/batman review group.py against requirement.txt' \
  --no-session-persistence --output-format json \
  --permission-mode plan --tools Read --debug-file LOCAL_LOG_PATH
```

The loader debug log reported `Loaded 6 unique skills`, with `project: 6`, `user: 0`, `managed: 0`. The installed `/batman` command was recognized; execution then failed before a model turn with an EPERM opening the user configuration and a version-lock warning. The result reported zero turns, zero model usage, and zero API duration. Because the account is signed out, authenticated runtime testing was not attempted further. No authentication/configuration files or permissions were changed.

**Verified:** all six project skill packages load. **Unverified:** authenticated Claude invocation of each skill, selector routing, relative-reference loading during a model turn, and task outcomes. Do not advertise Claude execution as verified from these checks.

## Reproduce and close remaining gaps

Install into an existing isolated project:

```sh
python3 scripts/install.py --host both --project /absolute/path/to/project
python3 scripts/install.py --host both --project /absolute/path/to/project
python3 scripts/install.py --host both --project /absolute/path/to/project --check
```

Start the host in that project. Invoke `$batman` in Codex or `/batman` in authenticated Claude Code with a concrete task; confirm the trace actually loads the installed selector and selected focused instruction. Repeat for investigation, design, challenge, review, and execution. Verify the implementation independently. Repeat direct focused invocations for the remaining four skills if validating their UI independently of selector routing. Keep global copies disabled or audit their source paths to avoid mistaking a global install for local discovery. Do not publish raw debug logs without checking them for private information.

Scratch evidence for this preparation is retained locally under the `batman-beta-*` temporary directories and is not included in a clone. The command builder is already in the repository; the fixture, prompt pattern, versions, and observed results above allow reproduction without publishing local session identifiers or authentication data.

## Earlier observations

On 31 October, Claude Code 2.1.114 loaded one legacy project skill versus zero in a control and rejected `/batman` only in the control, but model execution was blocked by authentication/config access. Codex's old launcher failed to locate its native binary and the app-bundled executable was denied. Those observations are historical; they do not describe the current Codex installation or the current six-package layout. The old `references/` packaging description is superseded by the sibling skill layout above.
