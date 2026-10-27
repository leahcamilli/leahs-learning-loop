---
title: "Designing Reusable AI Coding Skills for Clearer Workflows and Better Collaboration"
source: "https://www.youtube.com/watch?v=gaDdrDdczO4"
date: "2026-08-05"
tags: [ai-coding, documentation, workflow-design, prompt-engineering, knowledge-management]
source_type: "youtube"
source_fingerprint: "93bc609ba5"
source_characters: 13161
channel: "Matt Pocock"
published: "2026-08-05"
duration_seconds: 697
topics: [ai-agents, prompt-engineering, coding-agents, context-engineering]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> Treat recurring AI coding work as explicit, documented skills instead of repeatedly improvising prompts. The speaker argues that separating always-on guidance from on-demand procedures makes workflows clearer, more consistent, and easier to share with collaborators.

## Key Takeaways

1. Document the complete workflow and each individual skill so the skill library functions as a teachable system, not merely a collection of instruction files.
2. Keep specialized instructions out of the agent’s context until needed; the speaker recommends explicit invocation controls such as `allow implicit invocation false`.
3. Use a clarification skill such as `wait what?` to turn verbose or unclear model output into plain technical language grounded in the team’s vocabulary.
4. Organize discovery questions as a dependency graph, asking currently answerable questions in rounds instead of forcing one-question-per-turn exchanges.
5. Treat agent-facing documents such as `agents.md` as a distinct writing discipline: make instructions concise, predictable, and easy for an agent to follow.
6. Use deterministic, human-guided scripts for sensitive setup steps such as logging in or entering secrets instead of fully autonomous browser workflows.
7. Export unresolved decisions into a shareable questionnaire when collaborators cannot participate directly in the agent conversation.

## Overview

This lesson extracts a practical pattern from a video about a skills repo release. The core idea is to treat AI assistance as a set of explicit, documented, reusable skills rather than a pile of ad hoc prompts. The speaker describes a workflow that starts with documentation, moves through specification and implementation, and adds support skills for clarification, agent-facing writing, deterministic setup flows, and collaboration. Some claims in the source, such as repository ranking, model quality, and tool behavior across coding harnesses, are presented as the speaker's account rather than independently verified evidence.

## Key Concepts

- **Skills as reusable operating procedures**: A skill is presented as a durable instruction bundle that helps an agent perform a recurring task consistently. In the source, skills are documented individually and organized into a broader engineering flow.
- **Documentation as the entry point**: The speaker emphasizes a documentation site that explains both the overall flow and each skill. This turns the skill library into a teachable system, not just a collection of files.
- **Explicit invocation and context control**: A recurring concern is keeping unnecessary skill text out of the agent context until needed. The source describes sidecar OpenAI YAML files and an `allow implicit invocation false` setting so some skills are only pulled in when invoked.
- **Clarification skills for bad model output**: The `wait what?` skill addresses verbose or unclear model responses by forcing simpler language and grounding the reply in the team's own vocabulary from context documents.
- **Question graphs instead of one-question turns**: The updated `Grill Me` skill treats questions as a dependency graph. It asks only the questions that are currently answerable, grouped into rounds, which reduces slow back-and-forth when many questions are easy.
- **Writing for agents as a separate discipline**: The `writing for agents` skill generalizes beyond writing skills themselves. It is meant to improve agent-readable documents such as `agents.md` or similar configuration files so they are concise and predictable.
- **Deterministic human-in-the-loop automation**: The `wizard` skill generates interactive bash wizards for steps an agent should not fully automate, such as logging into services or pasting secrets. The value is guided execution without handing control to an autonomous browser workflow.
- **Exporting decisions for collaboration**: The `to questionnaire` skill converts an agent's questions into a document that other people can review outside the chat. This is a workaround for teams that cannot yet collaborate directly with an agent in shared tools.

## How It Works

A practical way to apply the lesson is to build your knowledge base around repeatable AI workflows. First, document the main path of work in plain language so a reader can see the sequence of tasks and the purpose of each skill. Second, separate always-on guidance from on-demand guidance: keep specialized instructions hidden until explicitly invoked when possible. Third, add repair skills for common failure modes such as unclear output; the source's example is a simplification skill that rewrites answers in plain technical language and the user's own terminology. Fourth, model discovery and planning as structured questioning: instead of asking one question per turn, group only the currently answerable questions into rounds based on dependencies. Fifth, write agent-facing documents intentionally, because the source argues that better-written instructions improve both readability and performance. Sixth, automate only the parts that benefit from automation; for sensitive or awkward setup work, generate deterministic human-guided scripts rather than giving the agent full control. Finally, when other humans need to weigh in, export the open questions into a shareable questionnaire and bring the answers back into the workflow.

## Training Exercise

Pick one recurring task you do with an AI coding agent, such as setting up a service, refining a spec, or reviewing implementation decisions. Write a mini skill pack for it with six parts: 1. a one-paragraph purpose statement, 2. a short step-by-step workflow, 3. one explicit trigger for when the skill should be invoked, 4. one clarification rule that forces plain language, 5. a round-based question list that separates prerequisite questions from follow-up questions, and 6. a questionnaire version that a non-technical collaborator could answer in a document. Then test whether a new reader could use your lesson without extra context.

## Test Yourself

<details><summary>Why should specialized skills be explicitly invoked rather than always included in an agent’s context?</summary>

Explicit invocation keeps irrelevant instructions out of the context until they are needed. According to the speaker, this reduces clutter and gives teams more control over agent behavior.

</details>

<details><summary>How does the `Grill Me` approach improve requirements discovery?</summary>

It models questions as a dependency graph and groups the currently answerable ones into rounds. This reduces slow back-and-forth while ensuring prerequisite answers come before dependent questions.

</details>

<details><summary>When does the lesson recommend using a wizard or questionnaire?</summary>

Use a deterministic wizard when a human should perform sensitive or awkward setup steps, such as authentication or secret entry. Use a questionnaire when other people need to review and answer the agent’s open questions outside the chat.

</details>

## Further Reading

- [Source video](https://www.youtube.com/watch?v=gaDdrDdczO4)
- [Skills documentation site mentioned in the source](aihero.dev/skills)
