# Pilot trace and grading audit

This is the implementing agent's audit, not independent validation. Sources:
`evals/results/2026-11-01-comparison/{scoreboard.json,audit.json,trials/}`.
The current dirty working tree, rather than HEAD, is the before variant.

## Useful work and avoidable overhead

- `083616f470e042cb984cd6ae02d41a1a` reads all four relevant source/test files,
  searches the same symbols, then rereads baseline consumers and tests, a diff,
  and numbered source. Reading consumers and proving skipped delivery are useful;
  repeated inventory/status and rereading unchanged contracts add little.
- `2861f973102d404c8c4a59b472125e71` lists files, finds guidance, reads four files,
  searches already-known symbols, runs the supplied control test, then checks
  status and rereads HEAD:api.py. The test establishes preference behavior; the
  last reread adds no demonstrated distinction in this fixture.
- `b0dce3b5d1ea4cce847de1c0397c4b2d` reads three tiny evidence files in separate
  commands after separately loading skill and references. Related reads could
  be combined. No reproduction is needed to conclude that the culprit is unknown.
- `2f1fd9e5b6d44cf488e945099d7c31d6` inventories again with hidden files after
  inspecting the only implementation. The stale-next-read reproduction is useful;
  searching Git internals is not supported by a remaining causal question.
- `4b9cb37af47d492e865d4cd90591cb7f` measures SELECT counts and tests an
  interleaved deletion. The latter establishes an additional actual failure
  path, rather than mere wasted testing. Keep room for such risk-driven checks.
- `21c6f3addc9f4eb3b5a785398767d274` attempts a heredoc reproduction that cannot
  create a temporary file in read-only mode, then successfully retries with `-c`.
  This retry is necessary recovery, not a redundant successful demonstration.
  The combined first command exits zero because later source reads succeed:
  command exit status alone is insufficient proof that an embedded test ran.
- Tests/reproductions for sync checkpoint loss, archive mutation, query count,
  preference opt-out, cache consistency and cancellation protect meaningful
  contracts. Removing them solely to reduce tokens would lose evidence quality.

The instruction hierarchy repeated context-before-diff and multi-stage review
checks across the entry point, principles and Guardian. Its breadth made small
fixtures invite an architecture survey. The revised entry point puts the review
ordering condition before routing; Guardian gives context → change → verification,
and permits a short source/consumer read. Principles own common evidence and
stopping guidance. No fixed tool-call count or mandatory operational checklist.

## Why ordering failed

`bfb0e139a9cf494aa49744961fc4ff1f` queued `cat SKILL.md` and `cat change.diff` in
one command. The decision to open the diff was made before the instruction was
returned; Guardian was loaded afterward. Repetition of the instruction did not
prevent that failure. Front-loading the condition and making the context gate
concrete may help, but no prompt can guarantee compliance. Judge raw command
order, not whether the final answer says the workflow was followed.

## Separate grading dimensions

The frozen v1 score combines detection/acceptance, explanation, repair specificity
and sometimes evidence acquisition. It is not a pure defect-detection measure.
No rubric or original score is changed in this revision.

| Pilot distinction | Detection | Explanation | Repair usefulness / next evidence |
| --- | --- | --- | --- |
| `75f66b…` hidden regression | Correct | Correct checkpoint mechanism | Ascending sync or separate checkpoint handling is useful but less prescriptive than v1's UI-boundary remedy; alternative handling needs its own compatibility proof. |
| `a1a111…` archive | Correct | Correct API-to-mutation trace | Missing explicit guard recommendation; concrete gap identified but repair left implicit. |
| `07ab58…` query regression | Correct | Measured N+1, plus deletion risk | Original single query mentioned, without an explicit restoration recommendation. |
| `b0dce3…` and `55776f…` timeout | Correctly uncertain | Both dependencies remain plausible | Requested request-specific timings; no explicit health request. |

All four review variants detected the same defects and accepted the control,
according to the pilot audit; the inspected borderline answers support repair
completeness as the distinction. Do not call Batman's 100 versus baseline 90 a
unique detection advantage. UI-boundary wording and whether an implied repair
counts are especially grader-sensitive. Future rubric changes should separate
these axes and accept equivalent contract-preserving remedies, with a new
version and all original variants rescored, rather than silently changing v1.

The missing health request was not demonstrated to be consequential: both
answers kept the outage unconfirmed and requested timings able to distinguish
the sequential dependencies. Health evidence can help establish scope or a
shared outage, but is not invariably needed alongside a discriminating trace.
Retain the strict v1 miss transparently; do not add a universal health checklist.
A new development task supplies healthy liveness probes with unresolved request
latency to test use of health evidence without rewarding a list of keywords.

The grading harness drops whole commands containing skill reads and truncates
other outputs to 1,600 characters. Mixed source/test evidence can be lost. Raw
trace audits are therefore required to interpret a grade; a filter omission is
not evidence that the candidate omitted the work. Grader snippets that normalize
or combine text should not be quoted as exact answer excerpts.
