---
title: "Spec-Driven Development for AI Coding Agents with GitHub Spec-Kit"
source: "https://www.linkedin.com/posts/akshay-pachaar_github-wants-you-to-stop-vibe-coding-heres-share-7460769031210373120-ser6?utm_source=social_share_send&utm_medium=ios_app&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY&utm_campaign=share_via"
date: "2026-05-20"
tags: [ai-agents, spec-driven-development, prompt-engineering, github, software-process]
source_type: "web"
topics: [coding-agents, prompt-engineering, ai-agents]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> Define what to build before asking an AI coding agent to build it: move from specification to plan to tasks to implementation. This makes requirements traceable, reduces agent guesswork, and gives humans clear checkpoints for review and revision.

## Key Takeaways

1. Use the four-stage workflow—specify, plan, tasks, implement—instead of prompting an agent with a broad product request.
2. Include goals, scope, constraints, assumptions, non-functional requirements, and acceptance criteria in the specification so the agent has a stable target.
3. Chain each artifact into the next: the specification informs the technical plan, the plan becomes executable tasks, and the tasks constrain implementation prompts.
4. Validate generated code against the original acceptance criteria, not merely whether it compiles or passes basic tests.
5. Treat specifications as living artifacts: update the spec, plan, and tasks when implementation reveals hidden assumptions, edge cases, or changing requirements.
6. Keep the workflow agent-agnostic so the same engineering process can work across Copilot, Claude Code, Gemini CLI, and future tools.
7. For a CSV export of up to 10,000 rows, specify measurable conditions such as a 5-second completion limit, authentication requirements, current-filter behavior, column order, and spreadsheet compatibility.

## Overview

This lesson introduces Spec-Driven Development as described in the source post about GitHub's open-source spec-kit. The core idea is simple but powerful: instead of giving an AI coding agent loose, ad-hoc prompts, you first define a structured specification, then derive a plan, then concrete tasks, and only then move into implementation. That workflow turns AI-assisted coding from improvisation into an engineering process with explicit artifacts and handoff points.

This matters to engineers using Copilot, Claude Code, Gemini CLI, or similar tools because the quality of AI output depends heavily on the quality of the instructions and constraints supplied up front. Teams that already work with requirements, design, and task decomposition will recognize this as familiar discipline; spec-kit's contribution is to formalize those practices for agent-driven software development in a repeatable, tool-agnostic way.

## Key Concepts

- **Spec-driven development**: Spec-driven development means writing a structured description of what should be built before asking an AI agent to generate code. The specification captures goals, constraints, behavior, and acceptance criteria so the model has a stable target instead of inferring intent from a vague prompt.
- **Four-step workflow**: The workflow highlighted in the source is: specify, plan, tasks, implement. Each stage produces an artifact that informs the next, reducing ambiguity and making the development process easier to review, revise, and automate.
- **Artifact chaining**: Rather than treating each AI interaction as a one-off request, artifact chaining uses the output of one step as input to the next. This creates traceability from business intent to implementation details and helps keep the agent aligned with the original requirements.
- **Agent-agnostic prompts**: Spec-kit is described as working across many coding agents, which implies its main value lies in the structure of the workflow rather than any vendor-specific model capability. A strong spec can outlive changes in model choice, IDE integration, or orchestration tooling.
- **Prompt quality as bottleneck**: The source emphasizes that poor outcomes from AI coding are often caused less by model limitations and more by weak instructions. Structured specifications improve the signal provided to the model, which generally produces better planning, fewer misunderstandings, and cleaner code generation.
- **Human-in-the-loop refinement**: Comments in the source point out a practical limitation: many projects cannot be fully specified up front. In real-world use, spec-driven development works best when humans revisit and refine specs as implementation reveals hidden assumptions, edge cases, or changing requirements.

## How It Works

At the center of the article is a process shift: move from "vibe coding" to explicit engineering intent. Instead of starting with a prompt like "build me a dashboard with auth and export support," the developer first writes a specification that states what the system should do, what constraints matter, and how success will be judged. That specification becomes the authoritative input for downstream AI interactions.

The workflow described in the source has four stages:

1. **Specify**
   - Define the problem, user needs, scope, constraints, and acceptance criteria.
   - Clarify assumptions that would otherwise be left for the model to invent.
   - Capture non-functional requirements if they matter: performance, security, maintainability, deployment environment, compliance, and testing expectations.

2. **Plan**
   - Convert the spec into a technical approach.
   - Identify architecture, modules, interfaces, data models, and implementation strategy.
   - Call out risks, unknowns, and tradeoffs before code generation begins.

3. **Tasks**
   - Break the plan into small, executable units.
   - Sequence work so an agent or engineer can implement incrementally.
   - Define dependencies and validation checkpoints between tasks.

4. **Implement**
   - Ask the agent to execute against the task list rather than against a broad product request.
   - Use the prior artifacts to constrain code generation and reduce drift.
   - Validate implementation against the original spec, not just whether the code compiles.

A practical way to think about the data flow is:

```text
Problem statement
  -> structured specification
  -> technical plan
  -> task breakdown
  -> implementation prompts
  -> code + tests + review against acceptance criteria
```

This approach improves AI coding in several ways.

- **Less ambiguity:** The model does not need to infer key requirements from sparse prose.
- **Better decomposition:** Planning and task generation happen before implementation, which aligns with how strong engineering teams already work.
- **Reviewability:** Specs and plans can be reviewed by humans before expensive coding begins.
- **Portability:** Because the process is agent-agnostic, teams can move across Copilot, Claude Code, Gemini CLI, or future tools without discarding their operating model.

The source also hints at an important nuance: spec-driven development is not a claim that all details can be known up front. Several comments challenge that assumption, noting that software design is often iterative. In practice, a good spec process should support feedback loops:

- start with an initial spec,
- generate a plan,
- discover gaps during implementation,
- update the spec and plan,
- continue with revised tasks.

That makes spec-driven development less like heavyweight waterfall documentation and more like structured iteration. The key distinction is that changes are captured explicitly instead of being silently improvised by the agent.

For working engineers, the main lesson is that AI coding quality is strongly tied to input structure. If your team already writes lightweight requirements, design docs, or implementation checklists, spec-kit is essentially a way to operationalize those habits for LLM-based development workflows.

## Training Exercise

Create a small spec-driven workflow for a feature you could plausibly hand to an AI coding agent.

### Goal
Design and implement a minimal feature using the sequence: **spec -> plan -> tasks -> implementation prompt**.

### Suggested feature
Add a `CSV export` capability to an internal reporting web app.

### Step 1: Write the spec
Create a file called `spec.md` and include:

```md
# Feature: CSV Export for Reports

## Objective
Allow authenticated users to export the currently filtered report view as a CSV file.

## User Story
As an analyst, I want to export report data to CSV so I can share it offline and use it in spreadsheets.

## Requirements
- Export only rows visible under current filters.
- Preserve column order shown in the UI.
- File name should include report name and current date.
- Only authenticated users can export.
- Export must complete within 5 seconds for up to 10,000 rows.

## Non-Goals
- Scheduled exports
- XLSX support

## Acceptance Criteria
- Export button appears on report page.
- Downloaded CSV matches filtered table contents.
- Unauthorized users receive an error.
- Exported file opens correctly in Excel and Google Sheets.
```

### Step 2: Turn it into a plan
Create `plan.md` with:

- frontend changes needed
- backend endpoint design
- data query reuse strategy
- CSV formatting library or approach
- authentication and authorization checks
- testing strategy

Example outline:

```md
# Plan
- Add `Export CSV` button to report toolbar.
- Frontend sends current filters to backend `/api/reports/:id/export`.
- Backend reuses existing filtered query builder.
- Serialize rows to CSV with stable column mapping.
- Return `text/csv` response with attachment headers.
- Add unit tests for serializer and integration tests for auth + filtering.
```

### Step 3: Break into tasks
Create `tasks.md` with 5-8 concrete tasks, such as:

1. Add toolbar button and loading state.
2. Serialize UI filter state into export request.
3. Implement backend export route.
4. Reuse report query logic with auth checks.
5. Add CSV serializer tests.
6. Add integration test for filtered export.
7. Validate filename and response headers.

### Step 4: Draft the implementation prompt
Use the artifacts to create an AI-agent prompt:

```text
Using spec.md, plan.md, and tasks.md, implement tasks 1-3 only.
Constraints:
- Do not change unrelated report logic.
- Reuse existing authentication middleware.
- Add tests for any new backend code.
- If any assumption is unclear, list it explicitly before generating code.
```

### Step 5: Review the output
After the agent responds, verify:

- Did it implement only the requested tasks?
- Did it respect the spec's acceptance criteria?
- Did it surface assumptions instead of inventing behavior?
- What was missing from the spec that the implementation exposed?

### Stretch exercise
Revise the spec after review to address one ambiguity, such as CSV formatting for commas, null values, or time zones. Then rerun the plan/task/implementation cycle and compare the quality of the generated result.

## Test Yourself

<details><summary>What are the four stages of the spec-driven development workflow?</summary>

The stages are specify, plan, tasks, and implement. Each produces an artifact that constrains and informs the next stage.

</details>

<details><summary>Why should generated code be reviewed against acceptance criteria rather than only checked for compilation?</summary>

Compiling proves that code is syntactically valid, not that it satisfies user needs, scope, constraints, or expected behavior. Acceptance criteria connect implementation results back to the original intent.

</details>

<details><summary>How does the lesson reconcile up-front specification with the iterative nature of software development?</summary>

It recommends treating specifications as living artifacts. When implementation exposes missing assumptions or edge cases, revise the spec and plan, regenerate the affected tasks, and continue with the updated constraints.

</details>

## Further Reading

- [GitHub Spec-Kit Repository](https://github.com/github/spec-kit)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Writing Great Specifications](https://www.atlassian.com/agile/project-management/requirements)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
