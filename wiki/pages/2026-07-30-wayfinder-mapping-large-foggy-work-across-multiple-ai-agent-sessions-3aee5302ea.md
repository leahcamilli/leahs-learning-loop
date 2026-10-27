---
title: "Wayfinder: Mapping Large, Foggy Work Across Multiple AI Agent Sessions"
source: "https://www.youtube.com/watch?v=F3lL98Pj90o"
date: "2026-07-30"
tags: [planning, ai-agents, project-management, software-engineering, knowledge-work]
source_type: "youtube"
source_fingerprint: "3aee5302ea"
source_characters: 17002
channel: "Matt Pocock"
published: "2026-07-30"
duration_seconds: 909
topics: [productivity, ai-agents]
kind: "tutorial"
depth: 2
actionability: 3
---

## TL;DR

> Wayfinder breaks large, ambiguous work into dependency-linked decision tickets that can be resolved across separate AI-agent sessions. This matters because it turns uncertainty into a visible frontier of actionable work while preserving decisions outside any single context window.

## Key Takeaways

1. Use Wayfinder when a task cannot be planned cleanly in one AI-agent session; execute directly when the path is already clear.
2. Define the destination first, then create a map of decision tickets that progressively reduces uncertainty.
3. Give each research, prototype, grilling, or task ticket its own agent session and record the outcome back in the map.
4. Work only on frontier tickets that are currently unblocked; completing them should expose or unlock the next decisions.
5. Use prototypes to test and clarify decisions early instead of relying on low-fidelity, waterfall-style planning.
6. Store maps, dependencies, and ticket outcomes in an issue tracker as durable memory across sessions; the speaker demonstrates GitHub and claims the method can be configured for other trackers.
7. Treat the resulting spec as a temporary coordination artifact that can be converted into implementation tickets, not as a permanent source of truth.

## Overview

This lesson presents Wayfinder as a planning method for work that is too ambiguous or too large for a single AI-agent session. The source argues that instead of forcing a big task into one context window, you create a map of decision tickets, resolve them across multiple sessions, and track what is known, blocked, and still uncertain. The evidence is experiential rather than formal: the speaker describes how the method works, how it is used with issue trackers, and how it supports coding and non-coding projects.

## Key Concepts

- **Fog of war**: Wayfinder is meant for tasks where the destination is roughly known but the path is unclear. The method treats uncertainty as normal and plans to reduce it over time rather than pretending the full path is already known.
- **Map and frontier**: The central artifact is a map of decision tickets. The frontier is the set of tickets that can be worked on now, while other parts remain blocked or hidden by unresolved questions.
- **Decision tickets**: Each node on the map is a ticket handled in its own agent session. The source describes four ticket types: research, prototype, grilling, and task.
- **Blocking relationships**: Some decisions depend on earlier decisions. Wayfinder tracks these dependencies so that finishing one ticket can unlock new work on the frontier.
- **Prototype-driven planning**: The speaker explicitly uses prototypes to avoid low-fidelity, waterfall-style planning. In this approach, prototypes are not implementation polish; they are a fast way to test and clarify decisions.
- **Issue-tracker-backed memory**: Wayfinder stores maps and ticket outcomes in an issue tracker. The source shows GitHub issues and claims the approach is issue-tracker agnostic with setup, but only GitHub is directly demonstrated in the transcript.
- **Spec as a temporary destination document**: In the speaker’s workflow, the map can be converted into a dense spec, then into implementation tickets. The spec is described as a temporary coordination artifact rather than a permanent source of truth.

## How It Works

Start by defining the destination: what 'done' should look like, such as a spec or another concrete outcome. Use an initial session to grill the problem, inspect relevant context, and create the first map of decision tickets. Work only the tickets on the current frontier, usually by opening a fresh agent session per ticket. As tickets are resolved, write the outcome back to the map so the system records what was learned, what remains blocked, and what new tickets are now available. Use research tickets to gather facts, prototype tickets to make ideas concrete, grilling tickets to clarify decisions through discussion, and task tickets for real-world or scheduled actions. When the fog has cleared enough, convert the completed map into a spec or directly into implementation tickets. The practical rule from the source is simple: use Wayfinder when a task cannot be planned cleanly in one session; skip it when the path is already clear enough to execute directly.

## Training Exercise

Pick one real project that feels too large or unclear for a single session. Write a destination in one sentence, then draft an initial map with 6-10 decision tickets split across the four ticket types from the source: research, prototype, grilling, and task. Mark which tickets are immediately takable and which are blocked by dependencies. Resolve two frontier tickets, then update the map with what changed: what uncertainty was removed, what new tickets opened up, and whether the destination now needs refinement. Finish by writing a short temporary spec that summarizes the decisions and links each major decision back to its ticket.

## Test Yourself

<details><summary>When should Wayfinder be used instead of direct execution?</summary>

Use it when the destination is roughly understood but the path is too large or ambiguous to plan cleanly in one agent session. If the work is already well defined and actionable, the source recommends executing it directly.

</details>

<details><summary>What is the frontier in a Wayfinder map?</summary>

The frontier is the set of decision tickets that can be worked on now because their dependencies are resolved. Completing frontier tickets records new knowledge and may unlock previously blocked work.

</details>

<details><summary>What roles do the four ticket types serve?</summary>

Research tickets gather facts, prototype tickets make ideas concrete, grilling tickets clarify decisions through discussion, and task tickets represent real-world or scheduled actions. Together they provide distinct ways to reduce uncertainty on the path to the destination.

</details>

## Further Reading

- [Source video](https://www.youtube.com/watch?v=F3lL98Pj90o)
