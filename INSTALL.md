# Install Batman

Batman is model-independent instruction text. Installation depends on the **coding agent**, not whether it runs GPT, Claude, Gemini, Kimi, DeepSeek, Qwen, Llama, or another model. Choose a model your agent supports with the file-reading, command, and editing capabilities your task needs. This does not certify every model's reasoning quality or make an unsupported provider available in your agent.

## Codex and Claude Code marketplaces

One GitHub repository hosts the catalogs and one plugin containing the five focused skills plus the selector. No hooks, MCP servers, API keys, or Node runtime are required by the plugin itself. The host still needs its normal model authentication. No official-directory listing or endorsement is implied.

Use the GitHub-hosted marketplace commands below, or test a local checkout using the isolated configuration examples. Restart your host after installation.

Codex CLI (restart the CLI/app after installing):

```sh
codex plugin marketplace add smhimran/batman
codex plugin add batman@batman
```

Claude Code (send these as two separate prompts):

```text
/plugin marketplace add smhimran/batman
/plugin install batman@batman
```

Plugin skills have a namespace. In Codex, select `batman:batman-review` in the skill picker or use:

```text
Use $batman:batman-review to review this branch against the ticket.
Use $batman:batman to investigate why these requests time out.
```

In Claude Code:

```text
/batman:batman-review review this branch against the ticket
/batman:batman investigate why these requests time out
```

Replace `batman-review` with `batman-investigate`, `batman-design`, `batman-challenge`, or `batman-execute` for a focused task. Project-local standalone installs use the unnamespaced names instead. Choose one installation method for each host to avoid duplicate skills from overlapping discovery locations; the plugin manager and project installer do not migrate each other's copies.

### Test a local catalog

Use a separate host configuration so your usual installed plugins and settings are untouched. On macOS/Linux, from the Batman checkout:

```sh
BATMAN_CODEX_STATE=$(mktemp -d)
CODEX_HOME="$BATMAN_CODEX_STATE" codex plugin marketplace add "$PWD"
CODEX_HOME="$BATMAN_CODEX_STATE" codex plugin add batman@batman
CODEX_HOME="$BATMAN_CODEX_STATE" codex plugin list --marketplace batman --json

BATMAN_CLAUDE_STATE=$(mktemp -d)
CLAUDE_CONFIG_DIR="$BATMAN_CLAUDE_STATE" claude plugin marketplace add "$PWD"
CLAUDE_CONFIG_DIR="$BATMAN_CLAUDE_STATE" claude plugin install batman@batman
CLAUDE_CONFIG_DIR="$BATMAN_CLAUDE_STATE" claude plugin list --json
```

These fresh configurations do not carry your model login. Authenticate through the host's normal process before attempting model execution. Plugin registration/installation alone does not verify invocation.

## Project-local installation for other coding agents

Clone the repository, then install into an **existing** project. Python 3.11+ is sufficient; there are no third-party Python dependencies:

```sh
git clone https://github.com/smhimran/batman.git
cd batman
python3 scripts/install.py --host cursor --project /absolute/path/to/project
python3 scripts/install.py --host cursor --project /absolute/path/to/project --check
```

Substitute a host from this table. The host documentation links establish the supported layout, not a completed Batman runtime test on that host.

| Agent | `--host` | Project directory | Invocation / discovery | Evidence |
| --- | --- | --- | --- | --- |
| Codex | `codex` | `.agents/skills/` | `$batman-review` | Native execution verified; [report](evals/NATIVE_DISCOVERY.md) |
| Claude Code | `claude` | `.claude/skills/` | `/batman-review` | Loader verified; authenticated execution unverified |
| [Cursor](https://cursor.com/docs/skills) | `cursor` | `.cursor/skills/` | Type `/` and select the skill | Layout tested offline; runtime unverified |
| [GitHub Copilot](https://docs.github.com/en/copilot/concepts/customizations/agent-skills) | `copilot` | `.github/skills/` | Ask the agent to use `batman-review`; available UI varies by surface/version | Layout tested offline; runtime unverified |
| [Gemini CLI](https://geminicli.com/docs/cli/skills/) | `gemini` | `.gemini/skills/` | `/skills list`, then ask to use `batman-review` | Layout tested offline; runtime unverified |
| [OpenCode](https://opencode.ai/docs/skills/) | `opencode` | `.opencode/skills/` | Ask to load the `batman-review` skill | Layout tested offline; runtime unverified |
| [Cline](https://docs.cline.bot/customization/skills) | `cline` | `.cline/skills/` | Skills menu; ask to use `batman-review` | Layout tested offline; runtime unverified |
| [Roo Code](https://roocodeinc.github.io/Roo-Code/features/skills/) | `roo` | `.roo/skills/` | Ask to use `batman-review` | Layout tested offline; runtime unverified |
| [Kiro](https://kiro.dev/docs/skills/) | `kiro` | `.kiro/skills/` | `/batman-review` | Layout tested offline; runtime unverified |
| [Kimi Code](https://moonshotai.github.io/kimi-cli/en/customization/skills.html) | `kimi` | `.kimi/skills/` | Ask to use `batman-review` | Layout tested offline; runtime unverified |
| [Pi](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md) | `pi` | `.agents/skills/` | `/skill:batman-review` | Layout tested offline; runtime unverified |
| [Google Antigravity](https://antigravity.google/docs/skills) | `antigravity` | `.agents/skills/` | Ask to use `batman-review`; inspect active skills | Layout tested offline; runtime unverified |
| [Windsurf compatibility / Devin Desktop](https://docs.devin.ai/desktop/devin-local/customizations.md) | `windsurf` | `.windsurf/skills/` | Ask to use `batman-review`; legacy layout remains readable | Layout tested offline; runtime unverified |
| [Devin Local / CLI](https://docs.devin.ai/desktop/devin-local/customizations.md) | `devin` | `.devin/skills/` | `/batman-review` | Layout tested offline; runtime unverified |

`--host agents` writes the shared `.agents/skills/` layout for other Agent Skills-compatible hosts. `--host both` retains its original meaning: Codex plus Claude only. `--host all` writes every distinct directory above once, with preflight across all of them. Usually choose just one host; installing every layout can expose duplicate names to agents that read multiple compatibility directories.

All options copy the same six skill packages, including the license. Reinstallation leaves identical copies unchanged. Conflicting skills, unexpected contents, and symlinked destinations are preserved and reported. Back up and remove a conflicting copy deliberately before reinstalling. `--check` only compares files; it does not contact the host or make a model call.

Restart or refresh your host, check its skill inventory, and try a concrete task. Confirm that it reads the installed skill and follows the selector's sibling links. Record the host/version, selected model, and observed outcome if contributing a compatibility result. Organization policies, disabled skills, duplicate global installs, and older versions can affect discovery.

## Any other agent or a plain chat model

With a file-reading coding agent, no installation is required:

```text
Read /absolute/path/to/batman/skills/batman-review/SKILL.md and use it to review this change against the attached requirement.
```

For an agent that only reads `AGENTS.md`, `GEMINI.md`, a rules file, or custom instructions, add a short pointer to the focused skill in your **existing** instructions. Do not replace your project's existing rules with Batman's repository selector. Keep all six sibling directories if you want selector routing.

In a plain chat without repository access, attach or paste a focused skill and the relevant requirement, code, diff, and logs yourself. The model cannot investigate files or run checks it cannot access; that is manual use, not a native integration. This is also the fallback for tools such as Aider or Continue when their installed version has no compatible skill loader. No provider-specific API adapter is required or supplied.

## Maintaining the marketplace

Canonical instructions remain under `skills/`. `plugins/batman/` is the generated distribution copy; catalogs point there so host caches contain no benchmark fixtures, graders, tests, or scripts. Generate it after changing skills or the version:

```sh
python3 scripts/build_plugin.py
python3 scripts/build_plugin.py --check
python3 -m unittest discover -s tests -v
node --test tests/test_prompts.cjs
claude plugin validate plugins/batman
claude plugin validate .claude-plugin/marketplace.json
```

The offline suite rejects stale generated files, mismatched catalogs, broken selector links, and unexpected payloads. Do not edit generated skills independently. Set the next version in `scripts/build_plugin.py` and rebuild both host manifests together. Installed caches are copies; updating the source tree does not prove the cached version updated. Test the host's update/reinstall flow before publishing a new version.

After an authorized commit/push and successful CI, a GitHub prerelease can record the version and notes. A tag/release alone neither updates marketplace catalogs nor submits Batman to a public directory. See [release limitations](RELEASE_NOTES.md#validation-and-limitations), [OpenAI packaging documentation](https://developers.openai.com/plugins/build/plugins), and [Claude distribution documentation](https://code.claude.com/docs/en/plugins/publish).
