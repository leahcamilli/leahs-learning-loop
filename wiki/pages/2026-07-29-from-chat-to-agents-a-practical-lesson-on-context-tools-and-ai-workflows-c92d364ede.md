---
title: "From Chat to Agents: A Practical Lesson on Context, Tools, and AI Workflows"
source: "https://www.youtube.com/watch?v=5p-sq8v3OXw"
date: "2026-07-29"
tags: [ai-agents, prompt-engineering, knowledge-management, automation, workflows]
source_type: "youtube"
source_fingerprint: "c92d364ede"
source_characters: 80000
channel: "Open Residency"
published: "2026-07-22"
duration_seconds: 8651
topics: [ai-agents, prompt-engineering, context-engineering]
kind: "tutorial"
depth: 2
actionability: 3
---

## TL;DR

> AI agents become useful when you delegate a concrete result and onboard them with focused context, necessary tool access, and repeatable processes. Clear completion criteria and durable markdown files help agents work across multiple steps without repeatedly losing important business knowledge.

## Key Takeaways

1. Frame work as a goal with a concrete deliverable: chat provides answers, while agents can pursue a result through multiple steps.
2. Define “done” explicitly because, according to the speaker, the agent’s observe-think-act loop continues until it reaches the stop condition implied by the goal.
3. Onboard an agent like a capable new employee by supplying business context, access to required tools, and guidance for repeatable workflows.
4. Store portable context in lean markdown files covering your role, business, offers, ideal customer, and brand voice rather than relying only on opaque application memory.
5. Use a top-level `CLAUDE.md` or `AGENTS.md` to orient each session and direct the agent to relevant context and memory files.
6. Record preferences and corrections in a memory file so later sessions can apply lessons instead of repeating the same mistakes.
7. Connect only the external systems needed for the task, begin with conservative permissions such as read-only access, and expand access after establishing trust and reliability.

## Overview

This lesson teaches a durable mental model for using AI agents productively at work. In the source, the speaker contrasts chat systems with agents: chat is "question to answer," while agents are "goal to result." The practical claim is that agents become useful when you onboard them like an employee: give them context about you and the business, connect the tools they need, and teach them repeatable ways of working. The strongest evidence in the excerpt supports context design, connector setup, and the basic agent loop. Evidence for the later "skills" layer is thinner here because the transcript excerpt ends before that section is fully developed.

## Key Concepts

- **Chat vs. agents**: The source frames chat as answering questions and agents as pursuing a goal until they deliver a finished result. The important shift is from advice you must execute yourself to delegated work that can continue through multiple steps.
- **Observe-think-act loop**: The speaker says an agent repeatedly observes the situation, thinks about the next step, and acts, looping until the defined output is complete. This explains why clear definitions of done matter: the stop condition comes from the goal you gave it.
- **Onboard the agent like an employee**: The core teaching is to treat an agent as a capable stranger. To make it useful, you must supply business context, tool access, and process guidance, just as you would for a new hire.
- **Context as owned markdown assets**: The source recommends storing durable context in simple markdown files such as an about file, business info, offer catalog, brand voice, and ideal customer profile. The point is to own and transport this context across tools instead of relying on opaque app memory.
- **North-star session file**: A central file such as `CLAUDE.md` or `AGENTS.md` is described as the file that loads at the start of each session and points the agent toward other context files. This gives the agent immediate orientation without forcing it to rediscover key information every time.
- **Memory and lessons**: The speaker adds a separate memory file for preferences and corrections, such as style rules or recurring instructions. The practical idea is to capture lessons explicitly so future sessions improve instead of repeating the same mistakes.
- **MCPs and connectors**: MCPs are explained as the mechanism that lets an agent use outside tools like email, calendars, project management apps, and web scrapers. The useful mental model is translation: connectors let the model act through external systems without custom glue each time.
- **Lean context and permission boundaries**: The source warns that too much context can fill the session window and degrade performance. It also recommends starting tool permissions conservatively, such as read-only access, then expanding once trust and reliability are established.

## How It Works

Use this workflow. First, define a task as a goal with a concrete deliverable, not as a vague request. Second, create a small set of markdown files that state who you are, what the business does, who the customer is, what the offer is, and how the brand should sound. Third, place a session-start file such as `CLAUDE.md` or `AGENTS.md` at the top level and make it direct the agent to those context files plus a memory file for learned preferences. Fourth, connect the external tools the task actually needs through connectors or MCPs, starting with low-risk read access when appropriate. Fifth, run the task and watch for failures caused by missing context, unclear done criteria, or missing tools. Sixth, when you correct the output, save the correction as a durable rule in memory so the next session starts better. One limitation from the supplied excerpt: the speaker names "skills" as a third pillar and describes them as SOP-like guidance, but the transcript segment provided here does not fully show the implementation details for that layer.

## Training Exercise

Create a folder for one recurring task you do every week. Add three files: `CLAUDE.md` or `AGENTS.md`, `context/about.md`, and `memory.md`. In `about.md`, write a factual summary of your role, audience, and priorities. In the main session file, instruct the agent to read the context and memory before any task and to ask questions when facts are missing. In `memory.md`, add 3 style or workflow preferences you care about. Then give the agent a concrete goal such as: "Draft a weekly performance summary for my team with 5 bullets, 2 risks, and 2 next actions." Review the result, make 3 corrections, and save those corrections back into `memory.md`. Repeat once and compare whether the second run needs fewer edits.

## Test Yourself

<details><summary>What distinguishes an agent workflow from a chat interaction in the speaker’s model?</summary>

Chat follows a question-to-answer pattern, while an agent receives a goal and works through multiple steps toward a finished result. The user delegates execution rather than merely requesting advice.

</details>

<details><summary>What information should be included when onboarding an agent for recurring work?</summary>

Provide focused context about the user, business, audience, offers, and brand voice; connect the tools required for the work; and document the process or preferences it should follow. A top-level session file can point the agent to these assets.

</details>

<details><summary>How can you improve reliability without overwhelming the agent or taking unnecessary security risks?</summary>

Keep context lean, define the deliverable and completion criteria precisely, and save useful corrections as durable memory. Start connectors with limited permissions such as read-only access, then expand them only after the workflow proves trustworthy.

</details>

## Further Reading

- [Source video](https://www.youtube.com/watch?v=5p-sq8v3OXw)
