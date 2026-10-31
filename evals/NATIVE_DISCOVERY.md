# Native discovery check — 31 October 2026

## Claude Code

**Project-local discovery confirmed with Claude Code 2.1.114. Skill execution remains unverified.**

Two isolated project directories received the same source fixture and fresh Git metadata. The control had no skill installed. The other contained only Batman core files under `.claude/skills/batman/`. Both ran:

```sh
claude -p '/batman review change.diff' --no-session-persistence --output-format json --permission-mode plan --tools Read --debug-file LOCAL_LOG_PATH
```

| Observation | Without skill | With skill |
| --- | --- | --- |
| Loader debug line | `Loaded 0 unique skills` | `Loaded 1 unique skills` with `project: 1` |
| Command dispatch | `Unknown command: /batman` | Proceeded to execution/authentication setup |
| Model execution | None | Blocked before a model turn |

`claude auth status` reported `loggedIn: false`. The installed case failed to resolve authentication and also reported an EPERM opening the user configuration. No model calls completed; reported API duration and usage were zero. Those environment failures do not negate the observed loader difference, but they prevent validating reference loading, mode selection, and runtime behavior through Claude.

The project installer was also run into a fresh isolated project. It copied core files to both host locations, its `--check` verified the copies, and a repeated Claude invocation again reported one project skill before the same execution blockers. Debug logs remain local scratch evidence; only the relevant loader observations are recorded here.

## Codex

**Native discovery blocked. Project-local packaging verified only.**

The installed `codex` launcher failed with ENOENT for its expected native binary. Attempting the app-bundled `codex-cli` returned permission denied. No binary, global installation, configuration, or file permissions were changed. Copying the skill into `.agents/skills/batman/` and verifying its bytes is an installation-layout check; it is not proof that Codex discovered or invoked it.

## Reproduce locally

From the Batman repository, install project-local copies into an existing project you choose:

```sh
python3 scripts/install.py --host both --project /absolute/path/to/project
python3 scripts/install.py --host both --project /absolute/path/to/project --check
```

The installer copies `SKILL.md`, `references/`, `agents/`, and the MIT license notice; it excludes benchmarks and grader answers. Identical copies are left unchanged. Existing differing skills and symlinked skill locations are rejected rather than overwritten. This changes no user-level skill directory. `--check` checks file contents, not native discovery.

After authenticating Claude through `claude auth login`, start it in that project and invoke `/batman review ...`. After repairing the local Codex CLI through its normal installation process, start it in that project and explicitly invoke `$batman`. Confirm the host actually loaded the skill and its selected references, then verify behavior on the same isolated fixture. Do not treat a successful install command as a successful invocation.

The location choices follow the official [Claude Code skill documentation](https://code.claude.com/docs/en/skills) and [Codex skill documentation](https://developers.openai.com/codex/skills/). The skill stays portable; project-local installation is optional.
