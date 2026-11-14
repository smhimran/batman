---
name: batman-investigate
description: Find the cause of a bug or incident using code, logs, and focused checks. Use for unexplained behavior, failures, timeouts, or Batman Detective requests.
---

# Batman Investigate

Reconstruct what happened and why; test the explanation against evidence.

## Investigate

1. Establish expected behavior, observed failure, affected users, and timing. Trace the failing request or job through relevant code, logs, and state changes. Recent changes are leads, not proof.
2. Keep plausible causes. For each, identify supporting and conflicting evidence and the smallest check that distinguishes it from alternatives. Seek evidence that could disprove the leading explanation.
3. Reproduce safely when useful. Link the symptom to the failing path and causal mechanism. Distinguish an immediate failure from its underlying cause; a reproduction of the symptom alone does not explain it.
4. Mark what is confirmed, inferred, or unknown. When evidence is unavailable, request the specific trace, input, or timing needed and continue independent work. Do not invent access or rule out an untested cause.

Conclude with the best-supported explanation and its causal evidence. If causes remain unresolved, choose the next check that distinguishes them; otherwise recommend a repair that addresses the confirmed mechanism. Separate containment from a lasting fix. Stay read-only unless changes are requested; production changes need authorization.

## Keep the work focused

Ground material claims in source, logs, or actual checks; separate facts from hypotheses. A ticket states the need, not proof of the cause. Check existing code against required behavior, permissions, side effects, and failure handling. Prefer verified reuse over duplicate logic; recommend new logic only for a concrete gap. Choose the supported solution rather than listing unequal alternatives as interchangeable.

Use the smallest check that settles the question. Expand for unresolved risks; stop when evidence is sufficient. Report the result, supporting evidence, and important gaps in plain words. Never claim unrun checks passed. Skip taste-based objections and empty report sections.
