---
title: "Practical Prompting Patterns for Claude Code from Anthropic Engineer Workflows"
source: "https://youtu.be/qOvc9IUKEIc"
date: "2026-05-22"
tags: [prompting, claude-code, ai-coding, llm-workflows, developer-tools]
source_type: "youtube"
channel: "Austin Marchese"
published: "2026-05-15"
duration_seconds: 645
topics: [prompt-engineering, coding-agents, claude]
kind: "tutorial"
depth: 2
actionability: 3
---

## TL;DR

> Treat a code-focused LLM like a fast junior engineer with imperfect judgment: give it sufficient repository context, explicit scope, constraints, acceptance criteria, and verification steps. A disciplined gather–plan–implement–verify loop makes its work safer, easier to review, and more likely to be production-useful.

## Key Takeaways

1. Ground each request with the failing behavior, relevant error output, likely files, scope constraints, and a concrete definition of success.
2. Split nontrivial work into reviewable stages: diagnose the problem, identify affected files, propose a plan, implement a narrow change, update tests, and summarize risks.
3. State invariants and prohibitions explicitly—for example, preserve public APIs, keep the session-cookie format unchanged, prefer minimal diffs, and avoid unrelated cleanup.
4. Require verification as part of the task: run or name relevant tests, examine edge cases, compare behavior before and after, and note remaining risks.
5. Narrow an uncertain response one dimension at a time by focusing on one file, comparing specific root causes, requesting tests first, or asking why an earlier patch failed.
6. Use task-specific prompts: debugging needs errors and reproduction steps; refactoring needs invariants and scope boundaries; migrations need old and new APIs plus compatibility guarantees.
7. Create reusable templates for bug fixes, refactors, and test generation with sections for the task, current and desired behavior, relevant files, constraints, output format, and verification requirements.

## Overview

This lesson distills practical prompting techniques for Claude Code based on the theme of how Anthropic engineers actually work with code-focused LLMs. Even though the source page provides minimal transcript detail, the core topic strongly suggests a real-world workflow centered on giving the model better context, clearer constraints, and structured tasks so it can act like a reliable engineering assistant rather than a generic chatbot.

This matters for engineers who use AI for implementation, debugging, refactoring, and codebase exploration. The difference between a weak prompt and a strong one is often the difference between toy output and production-useful results. A disciplined prompting style helps reduce hallucinations, improve iteration speed, and make the model's output easier to review and trust.

## Key Concepts

- **Context packing**: Code models perform best when given the right local context: relevant files, interfaces, error messages, and constraints. Instead of asking broad questions, effective users gather the minimal but sufficient context needed for the model to reason accurately about the task.
- **Task decomposition**: Large coding requests should be split into smaller, verifiable steps such as understanding the problem, locating affected modules, proposing a plan, implementing a narrow change, and validating results. This reduces ambiguity and makes failures easier to detect and correct.
- **Explicit operating constraints**: A strong prompt tells the model what not to do as well as what to do: avoid changing public APIs, preserve tests, limit edits to certain files, or prefer minimal diffs. These constraints shape behavior and prevent the model from taking overly broad or risky actions.
- **Plan-then-execute prompting**: Before generating code, it is often useful to ask the model for a short plan, affected files, and tradeoffs. This gives the engineer a review checkpoint and improves output quality by forcing the model to reason before acting.
- **Verification loops**: Good prompting includes a built-in validation step: run tests, explain edge cases, compare before and after behavior, or generate a checklist for manual review. LLMs are more dependable when asked to verify rather than simply produce.
- **Prompt templates for recurring tasks**: Engineers benefit from reusable prompt patterns for debugging, refactoring, onboarding to a codebase, writing tests, or preparing a migration. Templates reduce cognitive overhead and make interactions more consistent across tasks and teams.

## How It Works

A practical Claude Code workflow usually starts with **grounding the model in the repository and task**. Rather than asking, "Fix this bug," an effective engineer supplies:

- the failing behavior
- the relevant stack trace or test failure
- the files likely involved
- constraints on scope
- what successful completion looks like

That turns an underspecified request into an engineering task the model can actually execute.

A common structure looks like this:

1. **Orient the model**
   - Describe the system or feature area.
   - Point to the relevant files or pasted code.
   - Explain the current behavior and desired behavior.

2. **Ask for a plan first**
   - Request a short diagnosis.
   - Ask which files need inspection or modification.
   - Require assumptions to be stated explicitly.

3. **Constrain the implementation**
   - Keep public interfaces unchanged.
   - Prefer minimal diffs.
   - Add or update tests.
   - Avoid unrelated cleanup.

4. **Require verification**
   - Ask what tests should pass.
   - Ask for edge cases.
   - Request a summary of risks and follow-up checks.

For example, a weak prompt might be:

```text
Fix the authentication bug.
```

A stronger version would be:

```text
We have a bug in our login flow: users with expired sessions sometimes get a 500 instead of being redirected to /login.

Relevant files:
- auth/middleware.ts
- api/session.ts
- tests/auth.test.ts

Constraints:
- Do not change the session cookie format.
- Keep the public API of api/session.ts unchanged.
- Prefer the smallest safe fix.
- Add or update tests.

First, explain the likely root cause and propose a minimal patch plan. Then implement the change and show the diff. Finally, list the tests you would run and any edge cases you considered.
```

This style works because it mirrors how experienced engineers delegate work: clear problem statement, known context, constraints, and acceptance criteria.

Another important mechanic is **iterative narrowing**. If the first answer is too broad or uncertain, do not restate the whole task from scratch. Instead, tighten one dimension at a time:

- ask it to focus on one file
- ask it to compare two possible root causes
- ask it to produce only tests first
- ask it to explain why a previous patch failed

This creates a feedback loop where the model gradually becomes more useful as it accumulates task-specific context.

For code generation, effective users often separate **reasoning artifacts** from **final outputs**. A useful flow is:

- ask for diagnosis
- ask for an implementation plan
- review the plan
- ask for the code change
- ask for test updates
- ask for a concise change summary

That makes the model easier to supervise, especially on nontrivial edits.

A related pattern is **use-case-specific prompting**:

- **Debugging:** Provide the error, reproduction steps, and recent changes. Ask for likely causes ranked by confidence.
- **Refactoring:** State the quality goal, scope boundary, and invariants that must remain true.
- **Codebase exploration:** Ask for the architecture of one feature, entry points, key abstractions, and where side effects happen.
- **Test generation:** Give the function or module and ask for high-value edge cases, not just happy-path tests.
- **Migration work:** Specify old and new APIs, rollout constraints, and what compatibility guarantees must hold.

In practice, the real skill is not writing one magical prompt. It is building a disciplined loop of:

- gather context
- scope the task
- ask for a plan
- constrain the output
- verify the result
- iterate on failures

That is likely the central lesson behind how experienced Claude Code users prompt: they treat the model like a fast junior engineer with broad knowledge but imperfect judgment, and they shape its work with context, constraints, and review checkpoints.

## Training Exercise

Build and use a reusable prompt template for a small coding task.

### Goal
Practice turning a vague coding request into a structured Claude Code workflow with planning, implementation, and verification.

### Step 1: Pick a small bug or feature
Use any local project, or create a simple one with a failing test. For example, create a small JavaScript function that mishandles empty input.

```js
// formatName.js
export function formatName(name) {
  return name.trim().toUpperCase();
}
```

This function will throw if `name` is `null` or `undefined`.

### Step 2: Write a weak prompt
Start with something intentionally underspecified:

```text
Fix formatName.
```

Note what is missing: no failure mode, no constraints, no file references, no test expectations.

### Step 3: Rewrite it as a strong engineering prompt
Use this template:

```text
Task: Fix a bug in `formatName.js`.

Current behavior:
- `formatName(name)` throws when `name` is null or undefined.

Desired behavior:
- Return an empty string for null, undefined, or all-whitespace input.
- Preserve current behavior for normal strings.

Relevant files:
- formatName.js
- formatName.test.js

Constraints:
- Keep the exported function name unchanged.
- Prefer the minimal safe code change.
- Add or update tests for edge cases.
- Do not refactor unrelated code.

First, explain the bug and propose a minimal fix plan.
Then provide the updated implementation and tests.
Finally, summarize edge cases covered and any remaining risks.
```

### Step 4: Evaluate the response
Check whether the model:

- identified the real failure mode
- kept the change small
- added tests for `null`, `undefined`, and whitespace input
- avoided unrelated edits

### Step 5: Add a verification prompt
After getting code back, ask:

```text
Review the patch critically. What edge cases might still fail? Are there any behavior changes for existing callers? Suggest 2 additional tests if needed.
```

### Step 6: Generalize into your own prompt library
Create 3 saved templates for recurring tasks:

1. Bug fixing
2. Refactoring
3. Test generation

For each template, include these sections:

- task
- current behavior
- desired behavior
- relevant files
- constraints
- requested output format
- verification requirements

### Success criteria
You should finish with:

- one weak prompt rewritten into a strong prompt
- one implemented fix with tests
- one follow-up verification pass
- three reusable prompt templates for future coding tasks

## Test Yourself

<details><summary>What information should replace a vague request such as “Fix the authentication bug”?</summary>

Provide the observed failure, reproduction details or stack trace, relevant files, scope constraints, desired behavior, and acceptance criteria. Also request a diagnosis, minimal plan, implementation, tests, and edge-case review.

</details>

<details><summary>Why separate diagnosis, planning, implementation, and verification into distinct stages?</summary>

The separation creates review checkpoints before code changes and makes errors easier to locate and correct. It also helps constrain nontrivial work to a small, auditable change.

</details>

<details><summary>How should you respond when the model’s first answer is too broad or uncertain?</summary>

Iteratively narrow one dimension instead of restarting the entire prompt. Focus it on a file, ask it to compare a few possible causes, request tests first, or have it explain why the proposed patch could fail.

</details>

## Further Reading

- [Anthropic Documentation](https://docs.anthropic.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [OpenAI Cookbook: Prompting and Evaluation Patterns](https://cookbook.openai.com/)
- [Software Engineering at Google: Chapter on Code Review and Change Management](https://abseil.io/resources/swe-book)
