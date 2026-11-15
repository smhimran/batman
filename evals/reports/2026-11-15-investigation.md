# Batman investigation refinement — 15 November 2026

Completed slots: 80/80.

Execution failures (including earlier resumed attempts): 0.
Flagged skill-read commands: 1.

| Cohort | Variant | Score / 100 | Successful trials | Median tokens |
| --- | --- | ---: | ---: | ---: |
| other | baseline | 100.0 | 10/10 | 61,501.5 |
| other | batman | 100.0 | 10/10 | 106,631.5 |
| other | before | 93.3 | 8/10 | 105,197.0 |
| reviews | baseline | 86.7 | 6/10 | 85,351.0 |
| reviews | batman | 100.0 | 10/10 | 96,575.0 |
| reviews | before | 100.0 | 10/10 | 94,805.5 |
| reviews | codex-review | 100.0 | 10/10 | Unavailable |
| reviews | superpowers-reviewer | 100.0 | 10/10 | 87,079.0 |

Scores cover graded answers. All-attempt counts are in scoreboard.json.
Small author-controlled development fixtures; no statistical significance implied.
Model-assisted grades and the trace heuristic need manual review. Inspect grading/
and trials/ before publishing claims. Native review token counters may be unavailable.
Reported tokens include cached input and are not subscription charges.
before = previous frozen Batman; batman = current frozen working tree.

## Interpretation and audit

The current focused skills match the frozen evaluated files byte-for-byte. The previous snapshot is the current-skill snapshot from the 14 November 20:44 run. The requested model was `gpt-6-sol`, medium reasoning, with two repetitions per task and variant. Each cohort contains five distinct development tasks. All 80 trials were graded, with no ungraded trials or recorded execution failures.

Batman met all criteria in both cohorts. The previous snapshot lost one criterion in each missing-evidence investigation: both requested request-level traces but omitted a request for corroborating health evidence. Both current responses requested traces and follow-up dependency health data while leaving the suspected outage unconfirmed. Those answers and their grades were inspected. This is evidence of the desired behavior in this fixture, not proof of general improvement.

The four plain-Codex review deductions concerned missing explicit repairs: guarding an archived group's mutations, reusing the notification dispatcher, and restoring a bulk query in two trials. The published scores remain the model-assisted grades; this update does not regrade the run or establish independent human validation.

The single trace-audit flag is trial `d23ed315ba404a3791f50293b6dd0d7a`, a native-review correct-code control. Its raw commands were inspected. The flagged command ran `find` for `AGENTS*` and `SKILL.md` within its fixture; it did not read skill contents. Subsequent commands read fixture source and ran its unit test. The flag does not demonstrate skill contamination. The heuristic alone cannot establish complete isolation.

Batman used 13.1% more median review tokens than plain Codex and 10.9% more than the Superpowers template. Broader-task tokens were 73.4% above plain Codex and 1.4% above the previous snapshot. A perfect rubric score in this small suite does not establish superiority or token savings. Comparisons across separately dated runs are not controlled measurements of the instruction change. Selector invocation and authenticated Claude Code behavior were not evaluated here.

## Local evidence

The ignored `evals/results/2026-11-15-113813/` directory contains `scoreboard.json`, `grading/`, `trials/`, `trace-audit.json`, frozen inputs and hashes, provenance, and the run plan. These files are not included in a Git clone; share the raw bundle separately for a full audit. Historical reports are unchanged.
