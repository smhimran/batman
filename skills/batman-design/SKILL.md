---
name: batman-design
description: Plan a software change around the actual need and existing code. Use for solution design, implementation plans, or Batman Strategist requests.
---

# Batman Design

Choose the simplest approach that meets the need and fits the codebase.

## Design

1. State the outcome and how someone could tell it works. Separate user requirements from guesses about the solution. Check assumptions that could change the plan; keep dependent advice conditional while evidence is missing.
2. Ask user for clarifications when confused about something, or something is not clear. Do not assume, ask instead.
3. Read the existing implementation, useful helpers, and affected callers. Find the actual limits: expected use, ownership, compatibility, and what must happen when something fails.
4. Compare a few practical options. Include reuse, a smaller change, or leaving things alone when those meet the need. Explain only trade-offs that affect the choice. Do not add flexibility for imagined future needs.
5. Prepare for failure. Assume the worst case scenarios and make the solution resilient to them without losing requirements. Include test plan, and recovery plans for when things go wrong.
6. Recommend an approach, the parts it touches, and how to check the result. Include migration, recovery, or rollback only when the change needs them. Name unresolved decisions and the evidence needed to settle them.

Keep the plan as small as the task allows. Planning stays read-only unless implementation is requested. If the user already asked for implementation, continue into that work without asking again.

## Keep the work focused

Check important claims against code or an actual check. Separate what you know from what you suspect. A ticket explains what the user wants; its explanation of current behavior still needs checking.

Follow the relevant code and its callers. Reuse an existing helper only after checking that it does the whole job. Start with the smallest useful read or check; go wider when a dependency or a real risk calls for it. Reuse evidence already gathered and stop checking a question once the answer is clear.

Use plain words. Lead with the result, explain the effect on users, and cite the code or check behind it. Say what you could not verify. Never describe a proposed check as passed. Skip empty report sections and objections based only on taste.
