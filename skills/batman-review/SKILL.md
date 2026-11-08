---
name: batman-review
description: Review a PR, branch, commit, or local change for bugs, missed requirements, and broken callers. Use for code review or Batman Guardian requests.
---

# Batman Review

Check whether the change solves the real problem and keeps existing behavior working.

## Review

1. **Read the diff.** Establish the versions being compared and read the change. Note changed behavior and questions to resolve. Keep initial conclusions tentative.
2. **Read the context.** Check the ticket, requirements, and acceptance criteria against the change. Do not infer the intended outcome from the implementation. Look for required behavior missing from the diff. If context is unavailable, state that limit.
3. **Follow the source as needed.** Read the surrounding code, callers, dependencies, and tests needed to answer those questions and check affected behavior. The diff is a starting point, not the full review scope. Look for missed paths, wrong results, data loss, security problems, and useful existing code. Check speed and load against actual usage; use call counts or measurements when needed, not guesses about scale.
4. **Prepare for failure.** Consider the worst case scenarios based on the requirements first, then the code. Verify if the diff holds against all edge cases.
5. **Check each finding.** Give a real input or situation that reaches the problem. Re-read the code to confirm it can happen. Use a focused check when source alone leaves an important question open. Check what tests actually prove, including important behavior the change should preserve.
6. **Report what matters.** For each defect, give the location, trigger, user impact, and smallest useful repair. Keep uncertain concerns and optional improvements distinct from proven bugs. Order findings by impact. Accept a sound change without inventing objections.

Say when no meaningful issue was found, what you checked, and any important limit. If only a diff is available, say which context is missing. A passing test is evidence for what it checks, not a promise that nothing can break. Review stays read-only unless edits are requested.

## Keep the work focused

Check important claims against code or an actual check. Separate what you know from what you suspect. A ticket explains what the user wants; its explanation of current behavior still needs checking.

Follow the relevant code and its callers. Reuse an existing helper only after checking that it does the whole job. Start with the smallest useful read or check; go wider when a dependency or a real risk calls for it. Reuse evidence already gathered and stop checking a question once the answer is clear.

Use plain words. Avoid jargons. Lead with the result, explain the effect on users, and cite the code or check behind it. Say what you could not verify. Never describe a proposed check as passed. Skip empty report sections and objections based only on taste.
