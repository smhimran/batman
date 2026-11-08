---
name: batman-investigate
description: Find the cause of a bug or incident using code, logs, and focused checks. Use for unexplained behavior, failures, timeouts, or Batman Detective requests.
---

# Batman Investigate

Investigate what failed, why it failed, and what would prove the explanation. Do a systematice forensic of the issue.

## Investigate

1. Establish what should happen, what happened, who was affected, and when. Follow the failing request or job. Check recent changes without assuming they caused it.
2. Keep only plausible causes. For each, note what supports it, what argues against it, and the smallest check that could tell the causes apart. Use available code, logs, timings, and settings; do not pretend to access systems you cannot read.
3. Try a safe local reproduction when useful. Record the inputs and actual result. A cause is confirmed only when the evidence links it to the failure; two events happening together is not enough.
4. If evidence is missing, ask for the specific trace, time window, or setting that would answer the question. Continue work that does not depend on it. Missing evidence does not rule a cause out.

Report the known facts, leading explanation, remaining uncertainty, and next check or fix. Separate a temporary workaround from a lasting fix when needed. Investigation stays read-only unless the user asks for changes; production changes need authorization. Ask user for things you can't do yourself. Ask user for clarifications when needed.

## Keep the work focused

Check important claims against code or an actual check. Separate what you know from what you suspect. A ticket explains what the user wants; its explanation of current behavior still needs checking.

Follow the relevant code and its callers. Reuse an existing helper only after checking that it does the whole job. Start with the smallest useful read or check; go wider when a dependency or a real risk calls for it. Reuse evidence already gathered and stop checking a question once the answer is clear.

Use plain words. Lead with the result, explain the effect on users, and cite the code or check behind it. Say what you could not verify. Never describe a proposed check as passed. Skip empty report sections and objections based only on taste.
