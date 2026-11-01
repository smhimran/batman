# Validation task validity audit — 1 November 2026

These are newly constructed, author-created synthetic tasks, not independently
sourced production cases. The first two are development validation; the latter
two were reserved until the skill was frozen and the paired pilot audited.
Their outputs have now been inspected and they are no longer untouched holdouts.

`heldout-empty-cache` is **quarantined as a false-positive control**. Its intended
ground truth assumes sequential calls, but `requirements.md` promises each key
is loaded at most once without explicitly scoping concurrency. The before trial
reproduced concurrent double loading (two results, two loads, no errors) and
conditioned its repair on concurrent callers being within the contract. This is
real behavior with an ambiguous relevance judgment, not a demonstrated invented
finding. The after trial accepted sequential behavior and noted the concurrency
gap. Neither response establishes that this is an unambiguous correct control.
The ground-truth script verifies sequential behavior only, so passing it did not
establish validity of the intended negative control.

The frozen task and criteria remain unchanged for audit. Do not use the original
“do not require concurrency” assertion to claim a lower unsupported-finding rate
for the revision. A future task version must explicitly state its execution
model and be applied consistently to all variants. Do not silently edit or
retroactively score this task to create a win.

`heldout-refund-retry` produced no final answers in the isolated run because the
authenticated CLI reached its usage limit. Its outcome is unmeasured; the offline
ground-truth check passes. It is also structurally similar to the original retry
fixture, limiting its contribution to task diversity. No retry or additional
model grading was attempted after the usage-limit errors.
