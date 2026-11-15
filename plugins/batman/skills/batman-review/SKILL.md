---
name: batman-review
description: Review a PR, branch, commit, or local change for bugs, missed requirements, and broken callers. Use for code review or Batman Guardian requests.
---

# Batman Review

Determine whether the change achieves the intended outcome and preserves existing behavior.

## Review

1. Read the diff to establish the compared versions and changed behavior. Keep conclusions tentative; the diff does not define the review's scope.
2. Read the ticket, requirements, and acceptance criteria. Establish what success must look like independently of the implementation. If context is missing, state what cannot be assessed.
3. Trace required behavior through relevant source, callers, dependencies, and tests, including unchanged paths. Look for missing work and existing code that could satisfy the requirement without duplicate logic. Check performance against actual constraints, not imagined scale.
4. Check credible failure paths and preserved behavior. For each material requirement, identify supporting source or check results and what remains unverified. Passing tests establish only what they exercise.
5. Confirm each defect with a reachable input or situation; run a focused check when source leaves important uncertainty. Give its location, trigger, user impact, and recommended repair with the evidence for choosing it. Separate proven bugs, missing evidence, and optional improvements.

Lead with whether the intended outcome is demonstrated, partly demonstrated, or unverified, and why. Order defects by impact. Accept sound changes without inventing objections; no findings alone does not prove the outcome. Stay read-only unless edits are requested.

## Keep the work focused

Ground material claims in source, logs, or actual checks; separate facts from hypotheses. A ticket states the need, not proof of the cause. Check existing code against required behavior, permissions, side effects, and failure handling. Prefer verified reuse over duplicate logic; recommend new logic only for a concrete gap. Choose the supported solution rather than listing unequal alternatives as interchangeable.

Use the smallest check that settles the question. Expand for unresolved risks; stop when evidence is sufficient. Report the result, supporting evidence, and important gaps in plain words. Never claim unrun checks passed. Skip taste-based objections and empty report sections.
