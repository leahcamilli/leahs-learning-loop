---
title: "Practical Lesson: AI Loops for Verification, Goals, Schedules, and Proactive Work"
source: "https://www.youtube.com/watch?v=r5iBG1s_MDk"
date: "2026-07-21"
tags: [ai-agents, prompt-engineering, automation, evaluation, workflows]
source_type: "youtube"
source_fingerprint: "30a24d77e0"
source_characters: 21098
channel: "Dream Labs AI"
published: "2026-07-12"
duration_seconds: 1114
topics: [ai-agents, automation-workflows, prompt-engineering]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> AI loops turn one-shot prompts into controlled workflows by repeatedly doing work, checking it, and stopping when an explicit condition is met. Clear evaluators and stop rules matter because vague criteria can make a loop drift or continue unnecessarily.

## Key Takeaways

1. Define every AI loop with three parts: the task, the evaluator, and the stop rule.
2. Use a turn-based loop when an output needs one verification pass before delivery, such as confirming that a frontend change works.
3. Use a goal-based loop to revise toward a measurable threshold, such as an 8/10 rubric score or a target Lighthouse score.
4. Use a time-based loop for recurring work triggered at a fixed interval, such as drafting meeting follow-ups every day at 9:00 a.m.
5. Use a proactive loop to monitor for new inputs and continue until every item found in that run is processed or explicitly dismissed.
6. Externalize quality criteria in a reusable rubric, skill, or evaluator so each iteration is judged consistently.
7. Treat the speaker’s product commands, implementation details, and team-practice claims as examples until verified in primary documentation.

## Overview

This lesson distills a YouTube transcript about using "loops" with an AI agent such as Claude Code. In the source, a loop is described as an agent repeating a cycle of work until a stop condition is met. The video presents four loop types: turn-based, goal-based, time-based, and proactive. The practical value is not the specific brand or slash-command syntax, but the operating idea: make the model do work, check the result, and continue only until a defined standard is reached. Evidence is strongest for the general pattern and the examples shown in the transcript; specific claims about official product behavior, commands, or team practices are reported by the speaker and should be treated as secondhand unless you verify them in primary docs.

## Key Concepts

- **Loop**: A loop is a repeated work cycle for an AI agent. The agent performs a task, checks progress against a condition, and either stops or iterates again.
- **Stop condition**: The stop condition is the core control mechanism. It can be a verification pass, a target score, a schedule boundary, or a requirement that all detected items have been handled.
- **Turn-based verification**: This is the simplest loop in the lesson: after completing a prompt, the agent verifies the result before returning it. The source uses a landing-page example where the agent checks that frontend functionality actually works and fixes a bug before finishing.
- **Goal-based evaluation**: A goal loop keeps iterating until the output reaches a measurable threshold, such as a quality score. The source gives examples like improving a webpage until it reaches a Lighthouse score target or rewriting an email until a custom evaluator rates it highly enough.
- **Evaluator or cartridge**: The video describes reusable scoring logic packaged as a skill or cartridge. Examples include checking whether writing sounds human, matches a marketing style, or is likely to get higher open rates. The important idea is externalized criteria, not the branding of the evaluator.
- **Time-based scheduling**: A time loop runs on an interval, such as every five minutes or daily at 9:00 a.m. In the source, this is used for recurring operational work like summarizing a meeting and assigning follow-up tasks.
- **Proactive loop**: A proactive loop combines scheduled triggering with a goal or completion rule. Instead of waiting for a human to prompt each run, it watches for inputs, performs work, and keeps going until all work found in that run is handled.

## How It Works

The source teaches a general control pattern for AI work:

1. Define the task clearly.
2. Define how the result will be checked.
3. Let the agent act.
4. Feed the check result back into the next iteration.
5. Stop only when the condition is satisfied.

Applied to the four loop types from the video:

Turn-based loops add a verification step to an ordinary prompt. You ask for a result, but the agent must inspect the result before presenting it. In the source, this is framed as a skill file that verifies a frontend change actually works.

Goal-based loops add a measurable target. The agent keeps revising until a score or threshold is reached. The transcript uses custom evaluators for email quality and mentions webpage metrics such as Lighthouse.

Time-based loops add a schedule. The agent reruns the task at fixed intervals. The example shown is daily meeting summarization and task follow-up.

Proactive loops combine scheduling with completion criteria. The agent checks for new work, processes it, and does not stop until everything discovered in that run has been triaged or completed. The source illustrates this with bug-report handling and competitor-content monitoring.

The durable lesson is that good looping depends on explicit checks. If your criterion is vague, the loop will drift or spin. If your criterion is measurable and relevant, looping turns a one-shot prompt into a controlled workflow. The transcript is persuasive about the pattern, but many implementation details are examples rather than verified product specifications, so treat the architecture as a method to adapt rather than a guaranteed command set.

## Training Exercise

Pick one recurring task you already do, such as drafting a weekly update, reviewing a landing page, or preparing meeting notes.

Write four versions of the workflow:

1. Turn loop: Ask the AI to produce the output, then verify one concrete property before finishing. Example: "Draft the update, then verify every claim is supported by the notes I provided."
2. Goal loop: Add a threshold. Example: "Revise until the update scores at least 8/10 for clarity using this rubric: concise, specific, action-oriented, evidence-backed."
3. Time loop: Put it on a schedule. Example: "Every Friday at 3:00 p.m., create the first draft from this week's project notes."
4. Proactive loop: Add monitoring plus completion rules. Example: "Every day, scan new project notes, update the weekly draft, and do not stop until every new note is either incorporated or marked irrelevant with a reason."

After writing the four versions, compare them:
- Which stop condition is objectively testable?
- Which loop would fail if the rubric were vague?
- Which parts require outside tools or data access?
- Which loop would save you the most repeated effort?

Finally, refine one version into a reusable template with three parts: task, evaluator, and stop rule.

## Test Yourself

<details><summary>What is the basic control pattern shared by all four AI loop types?</summary>

Define the task and its evaluation method, let the agent act, feed the evaluation result into the next iteration, and stop only when the stated condition is satisfied.

</details>

<details><summary>How does a proactive loop differ from a time-based loop?</summary>

A time-based loop reruns a task on a schedule. A proactive loop adds monitoring and a completion rule, continuing until all work discovered during the run has been handled.

</details>

<details><summary>Why can a vague evaluator make an AI loop unreliable?</summary>

The agent lacks an objective way to decide whether the work has passed, so it may drift, stop too early, or iterate without meaningful improvement. Concrete, relevant criteria make the stopping decision testable.

</details>

## Further Reading

- [YouTube source video](https://www.youtube.com/watch?v=r5iBG1s_MDk)
