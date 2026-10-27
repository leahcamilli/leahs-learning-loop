---
title: "Scaffold First: Engineering Maintainable Software with Coding Agents"
source: "https://www.youtube.com/watch?v=mkN4uRZYPfs"
date: "2026-10-21"
tags: [coding-agents, software-architecture, context-engineering, code-review, developer-workflow]
source_type: "youtube"
source_fingerprint: "db94c332b3"
source_characters: 71351
channel: "Beyond Coding"
published: "2026-10-14"
duration_seconds: 4523
topics: [coding-agents, ai-agents, software-engineering]
kind: "interview"
depth: 2
actionability: 2
---

## TL;DR

> Coding agents are strongest when humans define the product intent, architecture, boundaries, and interfaces before generation begins. Treat generated code as cheap and replaceable: inspect it early, reject work you cannot readily understand, and strengthen the scaffold before trying again.

## Key Takeaways

1. Scaffold directories, dependency boundaries, core files, types, signatures, examples, deployment constraints, and short Markdown instructions before assigning implementation work to an agent.
2. Separate deliberation from execution: Kelkboom keeps his main conversational agent away from files until it has clarified the request sufficiently to dispatch implementation agents.
3. Prefer a well-specified, substantial one-shot task over repeated patching; the participants report that agents often duplicate concepts or layer patches during long iterative changes.
4. Run alternative implementations in separate Git worktrees, then compare them and merge only the useful parts.
5. Review generated work early—sometimes after one or two hours—and discard the worktree if the structure is unrecognizable or inconsistent with the scaffold.
6. Build context progressively: locate relevant information, rank brief metadata, inspect diffs or commits, and only then load complete files.
7. Keep human collaboration in the workflow; fast agent feedback should not replace product conversations, team review, mentorship, or time spent internalizing new knowledge.

## Key Moments

- [11:54](https://www.youtube.com/watch?v=mkN4uRZYPfs&t=714s) — Learn how files, comments, signatures, examples, and directory boundaries steer an agent before it writes an implementation.
- [15:54](https://www.youtube.com/watch?v=mkN4uRZYPfs&t=954s) — Use existing open-source projects and agent-led comparison to learn unfamiliar architectural patterns before scaffolding.
- [40:12](https://www.youtube.com/watch?v=mkN4uRZYPfs&t=2412s) — Treat code as disposable by exploring several implementations in parallel Git worktrees.
- [41:45](https://www.youtube.com/watch?v=mkN4uRZYPfs&t=2505s) — See how deeply Kelkboom scaffolds projects, including project names, diagrams, folder structures, core files, and domain types.
- [53:33](https://www.youtube.com/watch?v=mkN4uRZYPfs&t=3213s) — Build a distributed context graph with Markdown nodes, searchable metadata, ranking, and progressive disclosure.
- [58:18](https://www.youtube.com/watch?v=mkN4uRZYPfs&t=3498s) — Separate an inquiry-focused main agent from sub-agents that are allowed to modify files.
- [1:03:07](https://www.youtube.com/watch?v=mkN4uRZYPfs&t=3787s) — Reject unfamiliar generated code early, diagnose the conflicting assumptions, improve the scaffold, and rerun from a fresh context.
- [1:06:25](https://www.youtube.com/watch?v=mkN4uRZYPfs&t=3985s) — Reconsider reviews and testing through smaller changes, commit history, static analysis, and mutation testing.

## Overview

This lesson presents a scaffold-first workflow for using coding agents on software intended to remain understandable and maintainable. The central division of labor is that humans establish intent, architecture, terminology, deployment constraints, and quality boundaries; agents then perform implementation inside those decisions.

It is most relevant to senior engineers, architects, technical leads, and developers moving beyond short-lived prototypes. The discussion also warns that agent speed can weaken learning and collaboration when it replaces product clarification, code-review dialogue, mentoring, and deliberate reflection.

## Key Concepts

- **Intent before implementation**: Decide whether the goal is experimentation, learning, a quick outcome, or a durable product. A disposable proof of concept may justify minimal structure, while a system expected to evolve warrants greater architectural preparation and review.
- **Structural scaffolding**: Create the project shape before generation: directories, projects or packages, Markdown boundary notes, dependency direction, key files, type definitions, signatures, examples, and diagrams. Kelkboom reports spending roughly 20 minutes to an hour on this preparation, depending on the project.
- **One-shot implementation bias**: Kelkboom reports that agents handle a large, clearly prepared implementation better than a long series of conceptual revisions. In his examples, repeated changes led to patched-over designs and one compiler feature being implemented five times, so the workflow moves more reasoning ahead of execution.
- **Open-mode coordinator**: The main agent is reserved for conversation, teaching, clarification, and retrieval rather than file modification. Only after the request is considered sufficiently understood does it dispatch sub-agents that can implement the task; Kelkboom describes using multiple models and a greater-than-90% confidence threshold in his own experimental harness.
- **Progressive context graph**: Knowledge is represented as distributed Markdown nodes and connections carrying summaries, paths, URLs, folder references, or commit hashes. Search and ranking identify likely information first, after which the agent follows relevant links and examines changes before loading full source files.
- **Disposable worktrees**: Each implementation can run in an isolated Git worktree, allowing several agents to explore alternatives without contaminating the main codebase. A separate comparison pass can select useful pieces, while unrecognizable or structurally wrong attempts can simply be removed.
- **Deterministic back pressure**: Non-deterministic agent behavior is constrained with stronger scaffolds, scripts, tests, static analysis, deployment rules, and other machine-checkable boundaries. When a failure repeats, the goal is to convert the relevant expectation into an explicit and repeatable control.
- **Human learning and collaboration**: Instant answers can reduce the reflection needed to internalize a domain, while private agent workflows can erode team coordination. The discussion advocates studying fundamentals, talking with experienced people, retaining substantive reviews, and creating communities where people can learn and make mistakes together.

## How It Works

1. Define the outcome and lifespan. State whether the work is a disposable experiment, a learning exercise, or a product expected to evolve.
2. Clarify the product. Specify users, desired behavior, domain terms, constraints, deployment environment, storage choices, and security expectations.
3. Study unfamiliar territory. Examine established projects, ask the agent to contrast their strengths and weaknesses, and translate unfamiliar language conventions into terms from a language you know.
4. Scaffold the solution. Create folders, packages, dependency directions, boundary notes, core types, signatures, examples, diagrams, and required infrastructure decisions.
5. Validate understanding without editing. Use a conversational agent to surface ambiguity and conflicting assumptions before authorizing file changes.
6. Execute in isolation. Assign the prepared task to one or more implementation agents working in separate Git worktrees.
7. Inspect early. Review the emerging structure, diffs, and recognizable architectural landmarks after a limited interval instead of waiting for the full run.
8. Reject or accept decisively. If the work violates the scaffold or is not readily understandable, discard the attempt, diagnose the missing constraint, improve the scaffold, and rerun from a fresh context.
9. Verify the path as well as the result. Examine commit progression and use tests, mutation testing where appropriate, static analysis, and scaffold-aware checks before merging.
10. Review with people. Keep changes reviewable and discuss the reasoning and product intent, not only the generated lines of code.

## Training Exercise

1. Choose a small feature that normally takes a few hours, such as importing a CSV file and validating its records.
2. Write a one-paragraph objective that identifies the user, expected behavior, failure cases, deployment target, and whether the feature is experimental or durable.
3. Create only the scaffold: directories, a dependency-flow note, core record types, public function signatures, two representative input examples, and empty test cases. Do not implement the feature.
4. Ask a conversational agent to critique the scaffold without modifying files. Resolve ambiguous terminology, ownership, data flow, and error-handling decisions.
5. Give the same finalized scaffold to two implementation agents in separate Git worktrees.
6. After a fixed checkpoint, inspect each diff. Record whether the implementation follows the expected boundaries, duplicates concepts, adds unexplained infrastructure, or remains immediately understandable.
7. Discard any attempt that violates the architecture rather than patching it. Add one concrete constraint to the scaffold for each observed failure and rerun once from a fresh context.
8. Run the prepared tests and static checks. If available for the chosen language, run a small mutation-testing pass to see whether the tests detect intentionally introduced faults.
9. Compare the first and second attempts in a short note: which scaffold changes improved the result, what still required human judgment, and what should become a reusable project rule.

## Test Yourself

<details><summary>Why does scaffolding improve an agent-generated codebase rather than merely constrain implementation style?</summary>

The scaffold records decisions about boundaries, dependency flow, data shapes, deployment, and expected extension points. According to Kelkboom, this keeps an agent from optimizing only for the immediate request and reduces duplication, God objects, and concepts that are difficult to change later.

</details>

<details><summary>What should you do when generated code works but does not resemble the architecture you expected?</summary>

Do not merge it merely because it runs. Kelkboom recommends discarding the isolated worktree, identifying which instruction, scaffold element, or underlying idea was ambiguous or conflicting, and rerunning from a fresh context after correcting that source problem.

</details>

<details><summary>How does progressive context disclosure help an agent work on a large system?</summary>

It begins with small, ranked clues such as summaries, paths, URLs, or commit hashes, then follows the most relevant connections into diffs and complete files. This limits context size while giving the agent a structured route to the information needed for the task.

</details>

## Further Reading

- [Lead Architect Reveals His Rules for Coding Agents](https://www.youtube.com/watch?v=mkN4uRZYPfs)
- [Carlos Kelkboom on LinkedIn](https://www.linkedin.com/in/carlos-k-4016b8225)
- [Patrick Akil on LinkedIn](https://www.linkedin.com/in/patrick-akil)
- [Patrick Akil on X](https://twitter.com/PatrickAkil_)
