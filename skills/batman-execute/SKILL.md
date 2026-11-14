---
name: batman-execute
description: Implement a scoped software change or bug fix and check that it works. Use for Batman Executor requests or changes needing checks across affected callers.
---

# Batman Execute

Finish the requested outcome with the least code that demonstrably works.

## Implement

1. Read repository guidance and current edits. Establish observable success conditions, trace affected callers, and find existing helpers. Preserve unrelated work.
2. Choose the smallest complete change. Prefer existing code, then standard or installed tools. Preserve validation and error handling; avoid duplicate logic and unnecessary abstractions.
3. Fix the cause and update affected callers, tests, settings, and exports. Address credible failures without dropping requirements. Resolve material uncertainty from evidence; ask only when an important decision remains unresolved.
4. Verify the required behavior through a real caller or public interface where practical. For bugs, prefer a reproduction that fails before and passes after. Check relevant failure and recovery paths. Trivial edits need no new test; risky logic needs meaningful coverage.
5. Run relevant checks and inspect the final diff for missed requirements and accidental changes. Map results to success conditions; identify what remains unverified. Broaden checks only for failures or unresolved risks.

Report the outcome, changes, evidence, and important gaps. Call failures pre-existing only with evidence. Use existing authorization; keep commits, pushes, publication, and deployment within the requested scope.

## Keep the work focused

Ground material claims in source, logs, or actual checks; separate facts from hypotheses. A ticket states the need, not proof of the cause. Check existing code against required behavior, permissions, side effects, and failure handling. Prefer verified reuse over duplicate logic; recommend new logic only for a concrete gap. Choose the supported solution rather than listing unequal alternatives as interchangeable.

Use the smallest check that settles the question. Expand for unresolved risks; stop when evidence is sufficient. Report the result, supporting evidence, and important gaps in plain words. Never claim unrun checks passed. Skip taste-based objections and empty report sections.
