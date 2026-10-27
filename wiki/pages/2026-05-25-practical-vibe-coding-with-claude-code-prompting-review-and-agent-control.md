---
title: "Practical Vibe-Coding with Claude Code: Prompting, Review, and Agent Control"
source: "https://www.linkedin.com/posts/eordax_ai-claude-ugcPost-7458734104067563520-x8B_/?utm_source=social_share_send&utm_medium=ios_app&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY&utm_campaign=share_via"
date: "2026-05-25"
tags: [ai-coding, claude-code, developer-tools, prompting, code-review]
source_type: "web"
topics: [coding-agents, claude, prompt-engineering, ai-agents]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> AI-assisted coding works best as guided delegation: give the agent a bounded goal, repository context, constraints, and a definition of done, then verify its work. The critical engineering skill shifts from typing code to detecting drift and confirming semantic correctness.

## Key Takeaways

1. Frame each task with a goal, relevant files, constraints, and verification criteria to reduce ambiguity and keep the agent aligned.
2. Ask for a 3–5-bullet plan before allowing code edits so misunderstandings surface before they spread across files.
3. Prefer narrow, testable changes and review each diff; broad requests such as “improve this app” invite unnecessary work and agent drift.
4. Check generated changes against explicit requirements, not merely whether the code compiles or looks plausible.
5. Run tests, linters, type checks, and manual scenarios because polished explanations do not prove semantic correctness.
6. When output drifts, identify the exact requirement mismatch and restate the constraints instead of simply asking the agent to try again.
7. Treat AI coding as a supervision workflow: define, constrain, inspect, review, verify, and iterate.

## Overview

This lesson distills the core ideas implied by a short LinkedIn post recommending a 30-minute workshop by Boris Cherny, creator of Claude Code, along with Anthropic's Claude Code best-practices documentation. Although the source itself is just a pointer, it highlights an important shift in software engineering: coding assistants are most valuable when used as collaborative agents that can explore, edit, and reason across a codebase, while the human developer remains responsible for intent, constraints, and review.

For working engineers, the practical takeaway is that so-called "vibe-coding" is not about blindly accepting generated code. The real skill is learning to steer the model, keep it grounded in the repository and task, and detect when it has drifted from the requirements. This matters for anyone adopting AI-assisted development in production teams, where the bottleneck often moves from writing code to reviewing and validating changes.

## Key Concepts

- **Vibe-coding as guided delegation**: Vibe-coding is best understood as delegating implementation work to an AI agent while preserving human control over goals and quality. The model can draft, refactor, and investigate quickly, but the engineer must define success criteria and decide what is safe to merge.
- **Prompt specificity**: The quality of the result depends heavily on how concretely the task is framed. Good prompts include the objective, constraints, relevant files, expected behavior, and how to verify success, which reduces ambiguity and keeps the assistant aligned with the task.
- **Drift detection**: Agent drift happens when the assistant gradually solves a different problem than the one you intended, often through overgeneralization or hidden assumptions. Detecting drift requires comparing the produced changes against explicit requirements, not just checking whether the code looks plausible.
- **Review becomes the bottleneck**: When code generation accelerates, the limiting factor shifts to validation: reading diffs, running tests, checking edge cases, and confirming architectural fit. Engineers therefore need strong review habits and verification workflows to use AI tools effectively.
- **Repository grounding**: AI coding tools perform best when grounded in the actual codebase rather than asked to generate generic solutions from scratch. Pointing the tool at existing modules, tests, interfaces, and conventions produces changes that are more consistent and easier to integrate.
- **Human judgment over raw speed**: The value of AI-assisted coding is not simply fewer minutes spent typing. The higher-leverage skill is deciding when to trust the output, when to tighten the prompt, when to ask for alternatives, and when to stop and implement or debug manually.

## How It Works

The source material is not a technical article itself; it is a recommendation to learn Claude Code from the creator's workshop and Anthropic's best-practices guide. From that, the practical mechanics are those of an interactive AI coding workflow rather than a traditional library API.

At a high level, the workflow looks like this:

1. **Start with a bounded task**
   - Choose a concrete goal such as fixing a bug, adding a small feature, or writing tests.
   - Avoid broad prompts like "improve this app" until you have a feel for the tool's behavior.

2. **Ground the assistant in context**
   - Tell it which files, modules, or directories matter.
   - Describe existing patterns it should follow.
   - Provide acceptance criteria such as expected output, API behavior, or test conditions.

3. **Ask for a plan before implementation**
   - A good first step is to have the assistant explain how it intends to change the codebase.
   - This helps catch misunderstandings early, before it edits multiple files.

4. **Let it implement incrementally**
   - Once the plan is sound, ask for the smallest viable change.
   - Review each diff rather than letting the tool perform a large, opaque rewrite.

5. **Verify aggressively**
   - Run unit tests, linters, type checks, and manual scenarios.
   - Ask the assistant to explain why a change is correct, what assumptions it made, and what edge cases remain.

6. **Refine based on failures or drift**
   - If the output is off-target, do not just say "try again."
   - Point to the exact mismatch between requirement and implementation, then restate the constraints.

A practical mental model is that Claude Code acts like a fast junior-to-mid-level engineer with broad knowledge and incomplete local understanding. It can search, summarize, modify, and propose. But it does not automatically know which trade-offs your team cares about most, so you must provide those preferences explicitly.

The comments in the source capture an important operational insight: AI coding changes the bottleneck from production to supervision. That means the engineering loop becomes:

- define the task clearly
- constrain the search space
- inspect the proposed plan
- review the diff
- run verification
- iterate until the implementation matches intent

In this model, the highest-value prompts often include structure like:

```text
Goal: Add request timeout handling to the payment client.
Context: Relevant files are src/payment/client.ts and tests/payment/client.test.ts.
Constraints:
- Keep the public API unchanged.
- Use the existing retry helper.
- Add unit tests for timeout and retry exhaustion.
Verification:
- npm test should pass.
- TypeScript build must remain clean.
First, explain your plan in 3-5 bullets. Do not edit code yet.
```

That structure improves reliability because it gives the assistant four things it needs: desired outcome, codebase anchors, non-negotiable constraints, and a definition of done.

Another key mechanic is **reviewing for semantic correctness**, not just syntactic correctness. AI-generated code often compiles and looks polished while still violating subtle expectations such as transaction boundaries, error-handling rules, caching behavior, or naming conventions. The workshop recommendation and best-practices link both imply that expert use of Claude Code is less about magical prompts and more about disciplined interaction patterns.

Finally, effective usage tends to converge on a few habits:

- prefer narrow, testable tasks
- ask for plans before patches
- provide examples of correct behavior
- request explicit assumptions and risks
- keep diffs small
- rely on tests and tooling rather than confidence in the prose explanation

Used this way, AI coding tools become force multipliers. Used without those controls, they can create fast but expensive-to-review changes that look right while quietly missing the real requirement.

## Training Exercise

Build a repeatable AI-assisted coding workflow on a small project.

### Objective
Use an AI coding assistant such as Claude Code on a toy repository and practice controlling scope, reviewing output, and detecting drift.

### Step 1: Create a small project
Make a simple CLI or service with one behavior you can extend safely.

Example:
```bash
mkdir ai-coding-practice && cd ai-coding-practice
npm init -y
npm install --save-dev typescript vitest @types/node
npx tsc --init
```

Create `src/math.ts`:
```ts
export function divide(a: number, b: number): number {
  return a / b;
}
```

Create `test/math.test.ts`:
```ts
import { describe, it, expect } from 'vitest';
import { divide } from '../src/math';

describe('divide', () => {
  it('divides two numbers', () => {
    expect(divide(6, 3)).toBe(2);
  });
});
```

### Step 2: Give the assistant a tightly scoped task
Use a prompt like:

```text
Goal: Make divide() reject division by zero with a clear error.
Context: Edit src/math.ts and test/math.test.ts.
Constraints:
- Keep the function name and parameters unchanged.
- Throw an Error with message "Division by zero".
- Add tests for the new behavior.
Verification:
- Tests should pass.
First, explain your plan in 3 bullets. Do not write code yet.
```

### Step 3: Review the plan
Check whether the plan:
- mentions both implementation and tests
- preserves the public API
- reflects the exact error message requirement

If not, correct it before asking for code.

### Step 4: Ask for the implementation
After the plan looks good, ask the assistant to make the change. Review the diff carefully.

Questions to ask during review:
- Did it change more files than necessary?
- Did it preserve the function signature?
- Did the test verify the exact error message?
- Did it introduce unnecessary abstractions?

### Step 5: Validate with tooling
Run tests and inspect behavior:

```bash
npx vitest run
```

If a test fails, ask the assistant to explain the failure before proposing a fix.

### Step 6: Practice drift detection
Now give a second prompt designed to tempt overreach:

```text
Improve the math module to be production-ready.
```

Observe what happens. Then rewrite it into a better prompt:

```text
Goal: Add a modulo(a, b) function to src/math.ts.
Constraints:
- Do not modify divide().
- Add exactly two tests for modulo.
- Keep the file structure unchanged.
Verification:
- Existing tests must still pass.
```

Compare the outputs. This teaches the difference between vague delegation and controlled tasking.

### Step 7: Reflect
Write down:
1. What prompt details most improved the output?
2. Where did the assistant drift?
3. What review checks caught problems fastest?
4. How would you turn your best prompt into a reusable team template?

By the end of the exercise, you should have a concrete feel for the real skill in AI-assisted development: not generating code, but shaping and validating it.

## Test Yourself

<details><summary>What four elements should a well-structured coding-agent prompt include?</summary>

It should state the desired outcome, identify relevant codebase files or modules, specify non-negotiable constraints, and define how success will be verified.

</details>

<details><summary>What is agent drift, and how should an engineer detect it?</summary>

Agent drift occurs when the assistant gradually solves a different problem through overgeneralization or hidden assumptions. Detect it by comparing the plan and diff with explicit requirements, including scope, API behavior, conventions, and edge cases.

</details>

<details><summary>Why does review become the bottleneck in AI-assisted development?</summary>

Code can be generated faster than engineers can safely validate it. Humans must still inspect diffs, run tooling, test edge cases, and confirm that changes fit the intended architecture and behavior.

</details>

## Further Reading

- [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)
- [Claude Code Documentation](https://code.claude.com/docs)
- [Anthropic Developer Documentation](https://docs.anthropic.com/)
- [Boris Cherny Workshop / Claude Code YouTube Session](https://www.youtube.com/live/6eBSHbLKuN0)
