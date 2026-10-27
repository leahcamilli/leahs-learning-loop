---
title: "Modular AI Coding Skills for Turning Vague Ideas Into Testable Software"
source: "https://www.youtube.com/watch?v=8D8ewFBJfFM"
date: "2026-08-09"
tags: [ai-agents, prompt-engineering, software-architecture, test-driven-development, code-review]
source_type: "youtube"
source_fingerprint: "f2eac68c26"
source_characters: 29987
channel: "Eric Tech"
published: "2026-08-07"
duration_seconds: 1457
topics: [coding-agents, software-engineering, prompt-engineering]
kind: "tutorial"
depth: 2
actionability: 3
---

## TL;DR

> Reduce AI coding randomness by turning vague ideas into shared context, lightweight specs, feature-sized tickets, tests, and focused reviews. Keeping these skills short and modular lets you revisit the step that needs work without rerunning a rigid pipeline.

## Key Takeaways

1. Interview the user one decision branch at a time until behavior, constraints, style, and priorities are clear enough to record.
2. Freeze agreed decisions in a lightweight spec without embedded code, so the AI must inspect the current codebase instead of copying stale snippets.
3. Slice work by end-to-end features, such as a complete login flow, rather than by technical layers like database, backend, and UI.
4. When requirements are concrete, write tests first, confirm that they fail, and implement until they pass.
5. Review code with compact refactoring vocabulary—including “shotgun surgery,” “feature envy,” and “data clumps”—to identify change-fragile or misplaced logic.
6. Use the skills as independent modules in any order; revisit grooming, specification, ticketing, implementation, or review whenever that stage needs refinement.
7. Favor clear entry points and fewer unnecessary file hops so an AI model can understand behavior with less context and fewer tokens.

## Overview

This lesson explains a modular approach to using AI for software development, based on the video’s description of Matt Pocock-style “skills.” The core idea is to reduce AI randomness by gathering missing context, freezing decisions into lightweight specs, splitting work into feature-based tickets, implementing with tests where possible, and reviewing code with a compact checklist. A key claim in the source is that these skills are intentionally short and modular so they can be run in any order instead of forcing a rigid end-to-end pipeline. Some popularity claims in the video, such as download rankings and totals, are presented by the speaker and not independently verified in the supplied source.

## Key Concepts

- **Context Gathering Before Coding**: The lesson argues that AI often misses the target because it lacks the full story: desired behavior, style, constraints, and priorities. The proposed fix is to interview the user until both sides reach a shared understanding.
- **Modular Skills Instead of One Locked Pipeline**: Rather than forcing brainstorming, planning, implementation, and review into one chained workflow, the source recommends small reusable skills that can be invoked in any order. This makes it easier to revisit one step without rerunning everything.
- **Grooming as Structured Interviewing**: The “grooming” skill is described as asking questions relentlessly until ambiguity is removed. It follows a decision-tree style: focus on one branch at a time, wait for answers, offer recommendations, and avoid acting before confirmation.
- **Specs Without Embedded Code**: After agreement is reached, the next step is to convert decisions into a written spec. The source emphasizes keeping code blocks out of the spec so the AI is pushed to inspect the real codebase later instead of blindly following stale snippets.
- **Feature-Sliced Tickets**: The source contrasts slicing work by feature versus by technical layer. Feature-based tickets are preferred because each ticket can produce an end-to-end testable increment, such as a complete login flow, instead of isolated database or UI work.
- **Test-Driven Implementation**: Implementation is described as triggering TDD when possible: write tests first, observe failure, then implement until tests pass. The lesson frames this as a way to shape code against explicit requirements rather than letting tests merely mirror buggy code.
- **Vocabulary-Driven Code Review**: The review approach uses a short checklist built from refactoring vocabulary like “shotgun surgery,” “feature envy,” and “data clumps.” The point is to compress rich engineering guidance into compact terms that a capable model can act on.
- **Architecture for Token Efficiency**: The source claims AI struggles when logic is scattered across too many files and call chains. The proposed architectural improvement is not one giant file, but clearer entry points and deletion tests so the model can understand behavior with fewer hops and fewer tokens.

## How It Works

Use the workflow as a loop, not a one-way conveyor belt. First, run a grooming-style interview to surface requirements, tradeoffs, and unstated assumptions. Ask one decision at a time, recommend concrete options, and do not move forward until the answer is clear enough to record. Next, freeze the result into a spec that describes behavior, constraints, and design intent without embedding code snippets that may age badly. Then convert the spec into feature-based tickets so each task can produce something testable end to end. During implementation, prefer writing tests first when the behavior is concrete enough to express. After coding, review from a fresh context using compact refactoring vocabulary to check for misplaced logic, duplicated concepts, and change-fragile structure. Finally, inspect the architecture itself: look for dead code, overly shallow wrappers, duplicated modules, and call patterns that force the model to jump through too many files to understand one behavior. The practical principle across all steps is minimal but precise guidance: short prompts, strong shared context, and just enough guardrails to steer a capable model without over-constraining it.

## Training Exercise

Pick a small app feature, such as user login or checkout. First, write 8-12 grooming questions that narrow one branch of decisions at a time, and answer them as if you were the stakeholder. Second, turn the answers into a one-page spec with no code blocks. Third, split the spec into 3 feature-based tickets, each producing a testable slice of value. Fourth, for one ticket, write the tests before the implementation and list what should fail initially. Fifth, perform a review using these terms: shotgun surgery, feature envy, and data clumps. End by naming one architectural change that would make the feature easier for an AI model to understand in fewer file hops.

## Test Yourself

<details><summary>Why should a specification avoid embedded code snippets?</summary>

Code snippets can become stale and encourage the AI to follow outdated implementation details. A behavior-focused spec pushes the model to inspect the actual codebase before implementing.

</details>

<details><summary>Why are feature-based tickets preferred over tickets divided by technical layer?</summary>

A feature-based ticket can deliver a complete, end-to-end behavior that is independently testable. Layer-based tickets often produce isolated pieces that provide no usable value until several tasks are combined.

</details>

<details><summary>How do modular skills reduce randomness without creating a rigid workflow?</summary>

Each skill adds a focused guardrail—such as gathering context, recording decisions, testing behavior, or reviewing structure—while remaining independently reusable. This lets the developer repeat only the step that needs improvement and run the skills in the order the situation requires.

</details>

## Further Reading

- [YouTube Source Video](https://www.youtube.com/watch?v=8D8ewFBJfFM)
