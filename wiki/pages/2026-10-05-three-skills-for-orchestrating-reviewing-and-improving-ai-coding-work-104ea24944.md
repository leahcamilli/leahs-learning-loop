---
title: "Three Skills for Orchestrating, Reviewing, and Improving AI Coding Work"
source: "https://www.youtube.com/watch?v=BsJGo1wFTvQ"
date: "2026-10-05"
tags: [ai-coding, coding-agents, workflow-automation, code-review, developer-productivity]
source_type: "youtube"
source_fingerprint: "104ea24944"
source_characters: 16774
channel: "Matt Pocock"
published: "2026-10-05"
duration_seconds: 874
topics: [coding-agents, ai-agents]
kind: "tutorial"
depth: 3
actionability: 2
---

## TL;DR

> Break large specifications into ticket-sized agent sessions, make pull requests prove that changes work, and retrospectively inspect sessions for recurring friction. Together, these practices improve delivery without trusting long contexts or autonomous self-correction blindly.

## Key Takeaways

1. Treat implementation tickets as a dependency graph: run every unblocked ticket in parallel while preserving blocking relationships.
2. Prefer a deterministic orchestration script once your workflow is mature; /implement-spec is presented as an accessible middle ground for teams that have not built that automation.
3. Require pull requests to include a concise visual summary, before-and-after evidence, reversibility, and blast radius so reviewers can judge changes quickly.
4. Verification builds trust: requesting evidence can prompt an agent to run an additional test, capture a screenshot, or collect runtime results instead of merely reasoning from code.
5. Rename vague agent resources to match their actual purpose; the repository changed context.md to glossary.md so agents and users recognize it as the source of domain language.
6. Run /retro on selected coding sessions to uncover navigation problems, missing checks, context loss, token waste, weak instructions, and unavailable tools.
7. Keep retrospective fixes human-in-the-loop; the presenter warns that automatic remediation can chase false positives and push a repository in an undesirable direction.

## Key Moments

- [0:30](https://www.youtube.com/watch?v=BsJGo1wFTvQ&t=30s) — Learn why a specification should become multiple ticket-sized agent sessions instead of one long context.
- [1:32](https://www.youtube.com/watch?v=BsJGo1wFTvQ&t=92s) — Compare manual orchestration with a reliable, inexpensive deterministic loop.
- [2:34](https://www.youtube.com/watch?v=BsJGo1wFTvQ&t=154s) — See how /implement-spec uses nested subagents as a beginner-friendly orchestration layer.
- [3:37](https://www.youtube.com/watch?v=BsJGo1wFTvQ&t=217s) — Follow the task-graph workflow through worktrees, TDD, integration, review, cleanup, and PR preparation.
- [5:44](https://www.youtube.com/watch?v=BsJGo1wFTvQ&t=344s) — Learn which evidence and risk signals make an agent-generated pull request easier to trust.
- [8:21](https://www.youtube.com/watch?v=BsJGo1wFTvQ&t=501s) — Understand why context.md became glossary.md and how the clearer name improves agent behavior.
- [10:29](https://www.youtube.com/watch?v=BsJGo1wFTvQ&t=629s) — See /retro inspect real sessions for hidden failures that persistence may have concealed.
- [12:32](https://www.youtube.com/watch?v=BsJGo1wFTvQ&t=752s) — Learn why retrospective recommendations require human judgment instead of automatic application.

## Overview

The Skills v1.3 workflow addresses three stages of AI-assisted software delivery: executing a large specification, presenting the resulting change for human review, and learning from completed agent sessions. Its central idea is that agent productivity depends as much on orchestration, evidence, and environment design as on code generation.

The approach is relevant to developers using coding agents for multi-ticket projects. It offers /implement-spec as a bridge toward unattended execution, /pr as a structured review aid, and /retro as a diagnostic process for improving repositories, instructions, tooling, and token efficiency over time.

## Key Concepts

- **Specification and ticket separation**: A specification defines the destination, while tickets divide it into work that fits into individual agent sessions. This avoids forcing a large implementation through one degrading or compacted context.
- **Task graph and execution frontier**: Tickets are modeled as a graph with blocking relationships rather than a strictly ordered list. At any moment, the execution frontier contains every unblocked ticket that can safely be assigned, allowing parallel work where dependencies permit.
- **Deterministic versus agentic orchestration**: A deterministic script reads and dispatches tickets the same way on every run, making it the presenter's preferred mature solution. /implement-spec delegates the orchestration to an agent and its subagents, which is less predictable but easier to adopt than building a software-factory loop immediately.
- **Isolated implementation and integration**: The described /implement-spec process creates an integration branch and has implementation subagents use test-driven development and worktrees. Completed work is merged into the integration branch, reviewed, cleaned up, and delivered as one pull request.
- **Evidence-centered pull requests**: The /pr skill supplies a body template with a concise visual summary and before-and-after evidence. Evidence may include tests, screenshots, or runtime observations that demonstrate the actual behavior rather than an agent's expectation from reading code.
- **Merge danger and blast radius**: Merge danger distinguishes a reversible two-way-door change from a costly or irreversible one-way-door change. Blast radius describes how broadly failure could affect the system; together they help reviewers allocate attention according to risk.
- **Explicit domain glossary**: The repository renamed context.md to glossary.md after its contents had narrowed to domain terminology. The presenter says the former name was vague, while the new name more clearly signals when agents should load and use the project's language.
- **Session retrospective**: /retro reviews completed sessions for hidden friction, including poor navigation, missing automated checks, weak coding standards, unhealthy agent instructions, tool inefficiency, no-op guidance, and missing information. The presenter reports improved token efficiency and output quality from running it regularly, but emphasizes that a human must choose which recommendations deserve action.

## How It Works

1. Write a destination-level specification and decompose it into tickets with explicit dependencies.
2. Read the complete skill instructions before invoking the workflow.
3. Have /implement-spec inspect the specification and tickets, explore the repository, and create an integration branch.
4. Dispatch every currently unblocked ticket to an implementation subagent, using separate worktrees and TDD; merge completed work and repeat as new tickets become unblocked.
5. Run code review against the integrated result, clean up temporary work, and prepare one pull request.
6. Use /pr to create a review-oriented body containing a concise visual explanation, concrete before-and-after evidence, merge reversibility, and blast radius.
7. Periodically run /retro on a sample of recent or suspicious sessions. Review its recommendations manually, implement the valuable fixes, and reject findings that do not fit the repository's actual risk or goals.

## Training Exercise

1. Choose a small feature that can be divided into three tickets, with at least two tickets independent of each other.
2. Draw the dependency graph and mark the initial execution frontier.
3. Give each ticket a success criterion and a concrete verification method such as a test, screenshot, or runtime observation.
4. Simulate the /implement-spec flow: create an integration branch, complete the unblocked tickets in isolated worktrees, merge them, and then complete any newly unblocked ticket.
5. Draft a pull-request body with four sections: concise change summary, before-and-after evidence, one-way versus two-way door assessment, and blast radius.
6. Review the work session as a retrospective. Record one friction point involving navigation, checks, instructions, context, or tools.
7. Decide manually whether the proposed improvement should be adopted, documenting why it helps or why it is a false positive.

## Test Yourself

<details><summary>Why is ticket-based implementation safer than asking one coding agent to implement an entire specification?</summary>

Separate tickets limit the amount of work held in one context, reducing degradation and context-compaction risk. They also expose dependencies so independent work can be parallelized and each task can receive a focused agent session.

</details>

<details><summary>What information should a pull request provide beyond a description of changed code?</summary>

It should provide concrete before-and-after evidence, state whether the change is easy to reverse, and explain its blast radius. These signals let a reviewer evaluate both correctness and merge risk.

</details>

<details><summary>Why should retrospective findings be reviewed by a human before implementation?</summary>

A retrospective agent can rank a harmless issue too highly or identify false positives. Automatic remediation could repeatedly alter the repository or agent instructions in ways that drift from the user's goals.

</details>

## Further Reading

- [AI Coding Crash Course](https://aihero.dev/s/xrT0hb)
- [Skills v1.3 changelog](https://www.aihero.dev/skills/skills-changelog-v13-implement-spec-pr-retro-and-glossary-md)
- [Matt Pocock's skills updates](https://aihero.dev/s/yeL3Jb)
- [Matt Pocock on Twitter](https://twitter.com/mattpocockuk)
- [AI Hero Discord](https://aihero.dev/s/RuRzmc)
