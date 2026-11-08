---
name: batman-challenge
description: Check whether a software proposal is needed and whether its assumptions hold. Use to challenge a plan, question complexity, or handle Batman Challenger requests.
---

# Batman Challenge

Find the assumptions that could change the decision. Agree when the proposal holds up.

## Challenge

1. Identify the desired result and the claims the proposal depends on. Separate required outcomes from a preferred implementation.
2. Read the relevant code and evidence before objecting. Check whether the problem exists, whether current code already solves it, and whether a smaller option meets the same need.
3. Test important claims with realistic examples. Check affected callers and failure cases where they matter. Consider leaving things alone when that is a valid option.
4. For each useful objection, explain the evidence, consequence, and a better option or a specific question that would settle it. Drop objections based on taste or imagined future requirements.
5. Consider the worst case scenarios. All edge cases, scenarios where this decision might go wrong. Suggest disaster recovery plan.

Give a clear recommendation: proceed, revise, or gather specific evidence. Keep the likely impact separate from how certain the claim is. Do not change code or publish a response unless requested.

## Keep the work focused

Check important claims against code or an actual check. Separate what you know from what you suspect. A ticket explains what the user wants; its explanation of current behavior still needs checking.

Follow the relevant code and its callers. Reuse an existing helper only after checking that it does the whole job. Start with the smallest useful read or check; go wider when a dependency or a real risk calls for it. Reuse evidence already gathered and stop checking a question once the answer is clear.

Use plain words. Lead with the result, explain the effect on users, and cite the code or check behind it. Say what you could not verify. Never describe a proposed check as passed. Skip empty report sections and objections based only on taste.
