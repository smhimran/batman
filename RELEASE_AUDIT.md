# Public beta audit — 15 November 2026

Status: local preparation complete; public beta is not yet ready to publish. See [release notes](RELEASE_NOTES.md) and [native checks](evals/NATIVE_DISCOVERY.md).

## Findings and scope

The audit inspected all six skill instructions and their host metadata, the installer, offline tests, benchmark preparation/provider/reporting code, published methodology, current report, and historical limitation statements, README, license, tracked paths, and release configuration. No repository `AGENTS.md` was found. The starting tree had only a modified tracked `evals/.DS_Store` and an untracked root `.DS_Store`; both were removed as requested. No skill or benchmark result files were changed.

| Previous gap | Evidence and action |
| --- | --- |
| No CI | Added one job for pushes to `main` and pull requests, running the existing Python and Node suites. Python 3.11 and Node 22 match locally tested major versions. No package installs, credentials, model calls, or benchmarks. |
| Installation safety | Existing installer preflights every destination, rejects conflicts and symlinks, preserves identical installs, and resolves installed selector links. Existing tests cover these behaviors; no installer rewrite needed. Added a package metadata/content assertion for every skill. |
| Stale host evidence | Replaced the October discovery status with dated native checks and explicit limits. |
| README overwhelms newcomers | Moved installation and a labeled illustrative requirement example to the opening; linked detailed reports instead of reproducing score tables. |
| OS metadata committed | Removed `evals/.DS_Store`, deleted the untracked root copy, and ignored `.DS_Store` at all depths. Extended the existing project-install ignores to the five focused skill copies for both hosts. |
| No release notes | Prepared `RELEASE_NOTES.md`; no commit, push, tag, or publication performed. |

CI uses `contents: read`, disables persisted checkout credentials, and pins the three official Actions to commit SHAs verified against their upstream v6 tags. It uses `pull_request`, not `pull_request_target`. GitHub-hosted execution remains pending because these edits have not been pushed. The design follows [GitHub's secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use). Version lifecycle references: [Python](https://devguide.python.org/versions/) and [Node.js](https://nodejs.org/en/about/previous-releases).

## Hygiene, license, and provenance

A local scan of all 73 originally tracked paths and 117 reachable historical blobs across the repository's ten commits found no private-key headers, GitHub token patterns, OpenAI-style key patterns, AWS access-key patterns, or credential-file path candidates. The only tracked generated-path candidate was `evals/.DS_Store`. This bounded pattern scan is not a guarantee that all private information or secrets are absent. Historical removal of `.DS_Store` was not attempted; normal source history is preserved.

The MIT license retains `Copyright (c) 2026 Shah Habibul Imran`; the installer includes the notice with each skill. Ponytail inspiration is still attributed. Benchmark comparator licensing/provenance instructions remain in the benchmark guide; ignored local evaluation evidence is not shipped in installed skill packages.

The emblem at `assets/batman-emblem.png` visibly uses Batman-like bat imagery, and README contains a film quotation. Git history records their addition but supplies no creator/source/license or permission evidence. The project name also refers to the character. The repository's MIT notice does not establish rights to third-party imagery, quotations, or marks. Their clearance remains unknown; this audit does not make a legal determination. Existing branding is preserved pending an owner decision. Before public beta, document appropriate provenance/permission and attribution, or replace/remove the uncertain artwork and quotation and decide whether the name needs changing. Do not claim affiliation or endorsement. Adding a disclaimer alone does not resolve missing rights evidence.

## Benchmark integrity

Historical reports, fixtures, graders, and skill instructions are unchanged. No model benchmark was rerun. Native smoke checks are installation/invocation evidence only, not a new comparative benchmark. README retains the small author-controlled fixture and model-assisted grading caveats, notes equal results from plain Codex/other reviewers where observed, and distinguishes quality, token usage, and latency. Additional useful investigation can justify more tokens.

## Offline validation

On macOS, Python 3.11.6: `python3 -m unittest discover -s tests -v` passed all **37 tests**. Node.js 22.22.1: `node --test tests/test_prompts.cjs` passed all **11 tests**. Runner-test output contains an intentional simulated `FAILED 0: runner unavailable`; the unittest suite itself passed. `git diff --check` passed, local links in changed/new documents resolved, and the workflow YAML parsed with the installed Ruby YAML parser (one job, five steps). The exact pinned GitHub Actions workflow has not executed remotely.

The actual installer CLI was also run against a fresh isolated directory with `--host both`, repeated, and checked with `--check`: twelve destinations were installed, then all twelve reported unchanged on both subsequent commands. A separate conflicting Claude Execute skill caused exit 1, preserved the user's bytes, and prevented any Codex writes. Unit tests additionally cover symlink refusal and late conflicts. Package assertions restrict the current release payload to `SKILL.md`, `agents/openai.yaml`, and `LICENSE` for each of six skills.

A historical report includes the author's local installation path; it was identified and retained as existing benchmark provenance rather than silently rewriting historical evidence. No new personal paths or raw authentication data are included in the public documents.

## Native runtime validation

Codex CLI 0.166.0's native `skills/list` inventory independently reported all six installed skills as enabled at repository scope, with correct local paths and no loader errors. Codex then completed five isolated model calls using the project-local selector, one per focused skill, with global skills disabled. Traces show reads of the selector and the intended sibling skill in each case. All five exited 0. A separate direct `$batman-review` call, without supplying a skill path, completed successfully, though that trace alone does not prove skill-body loading. Four read-only fixtures were unchanged. Execute's archived-rejection, active-addition, and preserved-read behavior passed an independent Python check. This is a small invocation smoke check, not broad task-quality certification. Claude Code 2.1.114 loaded six project skills but could not execute a model turn; its account is signed out. Full details and reproduction limits are in the [native report](evals/NATIVE_DISCOVERY.md).

## Release gates

- Complete authenticated Claude Code runtime checks before claiming both hosts verified, or explicitly narrow the release's runtime support claim.
- Resolve the branding/provenance decision above.
- Run the new workflow on GitHub after an authorized commit/push; local checks do not establish hosted CI success.
- Review and authorize the exact release commit and publication separately.

On 15 November 2026, `git tag --list` found no local tags; `git ls-remote --tags origin 'refs/tags/v0.1.0-beta*'` completed with no matches; `gh release view v0.1.0-beta --repo smhimran/batman` returned `release not found`. This is a dated observation, not a reservation of the tag name. Recheck before publication.
