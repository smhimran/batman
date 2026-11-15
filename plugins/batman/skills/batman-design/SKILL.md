---
name: batman-design
description: Plan a software change around the actual need and existing code. Use for solution design, implementation plans, or Batman Strategist requests.
---

# Batman Design

Plan the smallest complete solution, including how it behaves when things fail.

## Design

1. Establish the desired outcome, constraints, and observable success conditions. Resolve material uncertainty from available evidence; ask only when an important decision remains unresolved.
2. Trace current behavior, affected callers, and existing helpers. Compare reuse, a smaller change, or leaving things alone against the same requirements. Do not add flexibility for imagined needs.
3. Identify credible failures from the actual flow and dependencies: partial completion, retries, concurrency, or unavailable services where relevant. State what must remain true, how failure is detected, and how recovery works. Avoid claiming a design is fail-proof.
4. Recommend the approach and affected interfaces. For each important outcome and failure, name a check that would demonstrate the intended behavior. Include migration or rollback when needed; keep unresolved assumptions explicit.

Keep safeguards proportional to likelihood and impact. Planning stays read-only unless implementation is requested; then continue without asking again. Report the decision, evidence, trade-offs, and remaining gaps.

## Keep the work focused

Ground material claims in source, logs, or actual checks; separate facts from hypotheses. A ticket states the need, not proof of the cause. Check existing code against required behavior, permissions, side effects, and failure handling. Prefer verified reuse over duplicate logic; recommend new logic only for a concrete gap. Choose the supported solution rather than listing unequal alternatives as interchangeable.

Use the smallest check that settles the question. Expand for unresolved risks; stop when evidence is sufficient. Report the result, supporting evidence, and important gaps in plain words. Never claim unrun checks passed. Skip taste-based objections and empty report sections.
