---
name: batman-challenge
description: Check whether a software proposal is needed and whether its assumptions hold. Use to challenge a plan, question complexity, or handle Batman Challenger requests.
---

# Batman Challenge

Test whether a proposal achieves the needed outcome with justified complexity.

## Challenge

1. Identify the desired result, constraints, and assumptions that could change the decision. Separate the requirement from the proposed implementation.
2. Check relevant code and evidence: does the problem exist, what already works, and what can be reused? Test consequential claims with realistic examples, including evidence against your objection.
3. Compare the proposal with reuse, a smaller change, or doing nothing. Require each alternative to meet the same essential outcomes; simplicity must not discard requirements.
4. Examine credible failures where they affect the decision. Check whether safeguards address actual risks or add unnecessary work. Do not demand disaster recovery for every task.
5. For each supported objection, give evidence, consequence, and a better option or a specific check that would settle it. Drop objections based on taste or speculative needs.

Recommend proceeding, revising, or gathering specific evidence. Agree when the proposal holds up. Keep impact separate from certainty. Do not change code or publish a response unless requested.

## Keep the work focused

Ground material claims in source, logs, or actual checks; separate facts from hypotheses. A ticket states the need, not proof of the cause. Check existing code against required behavior, permissions, side effects, and failure handling. Prefer verified reuse over duplicate logic; recommend new logic only for a concrete gap. Choose the supported solution rather than listing unequal alternatives as interchangeable.

Use the smallest check that settles the question. Expand for unresolved risks; stop when evidence is sufficient. Report the result, supporting evidence, and important gaps in plain words. Never claim unrun checks passed. Skip taste-based objections and empty report sections.
