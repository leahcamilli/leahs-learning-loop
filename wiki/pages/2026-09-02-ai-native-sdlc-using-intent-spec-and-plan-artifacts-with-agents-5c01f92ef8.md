---
title: "AI-Native SDLC: Using Intent, Spec, and Plan Artifacts with Agents"
source: "https://www.youtube.com/watch?v=LoMOPj-lO8U"
date: "2026-09-02"
tags: [software-development, ai-agents, sdlc, testing, workflow-design]
source_type: "youtube"
source_fingerprint: "5c01f92ef8"
source_characters: 18986
channel: "Rob Shocks"
published: "2026-09-01"
duration_seconds: 981
topics: [ai-agents, coding-agents]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> An AI-native SDLC shifts the bottleneck from writing code to defining intent, producing durable specifications and plans, and validating agent output. High-quality artifacts matter because they let humans and agents collaborate safely without relying on shared conversational context.

## Key Takeaways

1. Treat `intent.md`, `spec.md`, and `plan.md` as durable handoff documents rather than depending on a single long agent conversation.
2. Start with `intent.md` that records the problem, user impact, goals, constraints, and relevant context; the transcript says the originator need not be an engineer.
3. Make `plan.md` detailed enough for another engineer or agent to implement without revisiting earlier conversations.
4. Use parallel agents or Git worktrees only when tasks are independent and the supporting artifacts provide sufficient context.
5. Require deterministic proof—including linting, builds, automated tests, and browser or end-to-end checks—before human review.
6. Version artifacts and constrain agents with hooks, permissions, policy files, and review gates to improve safety and auditability.
7. Route alerts, incidents, tickets, or messages back into the lifecycle by having an agent diagnose the issue and draft a new `intent.md`.

## Overview

This lesson explains an AI-native software development life cycle (SDLC) as described in the supplied video transcript. The core claim is that coding is no longer the main bottleneck; process design, artifact quality, governance, and testing become the limiting factors once agents speed up implementation. Evidence is moderate rather than primary: the source is a speaker's walkthrough of Anthropic's playbook, not the playbook itself, so details should be treated as an informed summary.

## Key Concepts

- **Process Becomes the Bottleneck**: The transcript argues that agents compress the time spent writing code, which shifts attention to planning, design, testing, deployment, and maintenance. Improving only implementation speed is not enough; the rest of the lifecycle must also be redesigned.
- **Artifact Chain**: The workflow is organized around durable documents passed between humans and agents. The transcript names an artifact chain that begins with `intent.md`, then moves to `spec.md`, then `plan.md`, with later stages producing pull requests, test results, and review outputs.
- **Intent as the Starting Point**: Instead of beginning with a traditional backlog handoff, the originator of a feature, bug, or improvement works with an agent to capture goals, context, and pain points in `intent.md`. The source emphasizes that the originator can be anyone, not just an engineer.
- **Spec and Plan as Handoff Documents**: After intent is reviewed, an agent generates a spec that translates goals into requirements and design. A later planning step produces `plan.md`, which should be detailed enough that an engineer or another agent could implement the work without revisiting earlier conversations.
- **Parallel Agent Execution**: The transcript describes using multiple agents or subagents, sometimes with Git worktrees, to execute independent tasks in parallel. This only works well if the artifacts are strong enough to replace missing conversational context.
- **Deterministic Checks and Evals**: Testing is not just human QA. The source stresses linting, build checks, automated tests, browser or end-to-end checks, and longer-lived eval suites used to detect regressions when models, skills, or workflows change.
- **Governance and Hooks**: Hooks, permissions, policy files, and review gates constrain what agents may do. The transcript frames governance as essential for safety, auditability, and measurement, including versioning artifacts and tracking who changed them.
- **Maintenance as an Automated Entry Point**: In the most ambitious form of the workflow, operational signals such as alerts, tickets, or messages can trigger an agent to diagnose issues and generate a new `intent.md`. Maintenance becomes another agent-driven entry point into the same lifecycle.

## How It Works

Treat the SDLC as a document-driven loop rather than a conversation-driven one. First, an originator works with an agent to produce `intent.md`, capturing the problem, goals, constraints, and relevant context. Second, an agent converts that intent into `spec.md`, adding requirements and design details while applying team policies, style guides, or skills. Third, an engineer or agent turns the spec into `plan.md`, listing files to change, work order, risks, constraints, and proof or success checks. Fourth, agents implement the plan, ideally inside bounded permissions and with hooks that prevent unsafe actions. Fifth, the system runs deterministic checks such as linting, builds, tests, and possibly browser-based validation before human review. Sixth, deployment flows through pull requests, policy checks, security review, and release gates. Finally, maintenance events can re-enter the loop by generating a fresh intent from logs, incidents, or tickets. The practical lesson is that durable artifacts let separate humans and agents collaborate without depending on a single long context window.

## Training Exercise

Pick one small feature or bug in a real project and run it through the artifact chain. Write a short `intent.md` with problem statement, user impact, constraints, and desired outcome. Then draft `spec.md` with requirements, design notes, and non-goals. Next, create `plan.md` listing files to change, implementation order, risks, and tests you will use as proof. Before coding, check whether the plan is complete enough that another engineer could execute it without the prior chat. After implementation, run linting, tests, and one manual or browser-based verification step. End by writing a brief retrospective: which parts of the work were accelerated by the agent, and which process bottlenecks remained.

## Test Yourself

<details><summary>What is the purpose of the `intent.md` → `spec.md` → `plan.md` artifact chain?</summary>

It progressively translates a problem and desired outcome into requirements, design decisions, and an executable implementation plan. According to the transcript, these durable documents allow different humans and agents to collaborate without sharing the original conversation.

</details>

<details><summary>When is parallel agent execution most likely to work well?</summary>

It works best when tasks are independent and the artifacts contain enough context, constraints, and success criteria to guide each agent. Git worktrees can isolate concurrent implementation work.

</details>

<details><summary>Why are deterministic checks and governance necessary even when agents accelerate coding?</summary>

Faster implementation does not prove correctness or safety. The lesson recommends automated checks, evals, bounded permissions, policy enforcement, and review gates to catch regressions, control agent behavior, and preserve an auditable record.

</details>

## Further Reading

- [Source video](https://www.youtube.com/watch?v=LoMOPj-lO8U)
