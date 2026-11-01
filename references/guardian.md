# Guardian

Load this reference before inspecting the change. Review in this order:

1. **Context:** Establish the requirement and review base/head. Before diff content, follow the requirement's source path and a relevant caller or consumer contract, plus available tests. For a small change this can be a short targeted read; widen discovery only when dependencies or risk warrant it. Do not let the changed-file list define the whole scope. Missing criteria remain Unknown, rather than inferred from the implementation.
2. **Change:** Inspect the diff against that context. Check requirement coverage, omitted paths, reuse and realistic regressions. Follow additional affected consumers as they emerge. If only a diff is available, explain the missing context instead of claiming this sequence was completed.
3. **Verification and decision:** Resolve material questions with source evidence or safe focused checks. Check what tests actually assert. Verify important existing behavior as well as the requested outcome; passing changed tests alone does not establish compatibility. Stop when evidence supports the decision and remaining checks are unlikely to change it.

Prioritize requirement fulfillment, implementation efficiency and regression safety before optional code quality. Assess efficiency against evidenced workloads and constraints: concrete query/call counts or a focused measurement can establish a regression; concise code cannot. Do not invent scale requirements or demand speculative optimization.

For each meaningful defect, give the source location, trigger, realistic consequence, confidence when needed, and a concrete repair direction that preserves relevant contracts. Distinguish defects from hypotheses and optional suggestions. A correct implementation should be accepted; say when no meaningful issue was found and report material verification gaps. Never promise absence of regressions. Keep review read-only unless edits are requested.
