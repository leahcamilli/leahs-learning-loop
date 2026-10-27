---
title: "Using Fable 5 for workflow redesign, mission control, and guided vibe coding"
source: "https://www.youtube.com/watch?v=rQUgUKnPsFs"
date: "2026-07-17"
tags: [ai-workflows, prompting, automation, software-tools, vibe-coding]
source_type: "youtube"
source_fingerprint: "a94f5a9d67"
source_characters: 16302
channel: "Alex Finn"
published: "2026-07-17"
duration_seconds: 916
topics: [prompt-engineering, productivity]
kind: "tutorial"
depth: 2
actionability: 3
---

## TL;DR

> Use the strongest AI model for redesigning workflows and discovering valuable product directions, then use cheaper or more available models for routine execution. This matters because separating strategic thinking from implementation can improve results while conserving limited model usage.

## Key Takeaways

1. Inventory each recurring workflow by documenting its current process, pain points, and desired outcomes before asking AI to redesign it.
2. Use reverse prompting: provide the current system and goals, then ask what the model would change and why instead of prescribing the solution.
3. Build a personal “mission control” by combining frequently used tools—such as task management, content capture, and newsletter creation—into one accessible dashboard.
4. Practice exploratory vibe coding by requesting five improvement ideas, choosing the most promising strand, expanding it, and repeating until it becomes a concrete feature.
5. The speaker reports that in-app browser automation can handle tasks such as research, sign-ups, GitHub operations, and Vercel deployment, but users should verify external actions and protect secrets.
6. Reserve high-capability, usage-limited models for workflow redesign, feature ideation, and architecture; assign routine code generation and repetitive edits to less constrained models.

## Overview

This transcript presents a practical, opinionated workflow for getting value from an AI model the speaker calls "Fable 5" before a pricing change. The central claim is that the model is especially useful for higher-level thinking: redesigning personal workflows, proposing novel ideas, guiding software feature discovery, and using an in-app browser to perform computer tasks that previously required manual effort.

The evidence is anecdotal rather than systematic: the speaker reports personal results, preferred prompting patterns, and comparisons with other tools such as ChatGPT, GitHub, YouTube, and Vercel. Even with that limitation, the lesson is useful because it captures reusable patterns: reverse prompting, AI-assisted operating-system redesign, building a personal "mission control," letting the model propose product directions, and reserving different models for ideation versus execution.

## Key Concepts

- **Operating systems**: In the video, "operating systems" means the repeatable workflows a person uses every day: coding, content creation, community management, morning routines, and similar habits. The speaker recommends listing these systems explicitly and asking the model to redesign them against your goals.
- **Reverse prompting**: Rather than telling the model exactly what to do, the speaker asks it what it would do. A prompt includes the current workflow and goals, then ends with an open request such as "How should we improve this?" This is meant to surface novel approaches the user might not have considered.
- **Mission control**: Mission control is the speaker's term for a personal software hub that combines tools they use repeatedly. In the transcript, examples include a newsletter studio, a task board, and a content capture board. The claimed benefits are convenience and replacing paid tools with custom ones.
- **True vibe coding**: The speaker distinguishes ordinary AI coding from "true" vibe coding. In this mode, the model explores the application, suggests directions, and the user follows promising strands rather than prescribing a fixed plan. The process is exploratory and creative rather than tightly specified.
- **In-app browser automation**: A key capability described in the transcript is an in-app browser that can perform web tasks on the user's behalf. The speaker cites examples such as finding YouTube channels, signing up for services, handling deployment steps, and working with environment variables, though these are reported experiences rather than independently verified capabilities.
- **Model role separation**: The speaker advises using Fable 5 for high-level thinking and another model, specifically ChatGPT in a medium setting, for lower-level execution like straightforward code writing. The rationale is to conserve limited usage on the more expensive or constrained model.

## How It Works

## 1. Start by inventorying your recurring workflows

The speaker's first recommendation is to identify the repeatable systems in your life and work.

Examples named in the transcript:

- vibe coding
- content creation
- community management
- morning routines
- evening routines

The point is not just to list tasks, but to describe the current workflow behind each one.

### Practical template

Write each workflow as:

- **Current process:** what you do now, step by step
- **Pain points:** where time or attention is lost
- **Goals:** what outcomes you want more of

Example structure:

```text
Workflow: Morning routine
Current process:
1. Check messages
2. Review email
3. Plan content ideas
4. Start work

Pain points:
- Email distracts me
- I lose time switching contexts
- Content planning is inconsistent

Goals:
- Create more content
- Stay responsive without getting sidetracked
- Improve revenue-generating work
```

## 2. Use reverse prompting to redesign the workflow

Instead of asking the model to directly execute, ask it to assess and redesign.

The transcript's pattern is:

1. Describe the existing system
2. State the goals
3. Ask the model what it would change

Example based on the video:

```text
Here is my current morning routine: [paste it].
My goals are: make more content, handle email better, and increase revenue.
Please rethink this routine to better achieve those goals.
What would you change, and why?
```

The speaker argues this works well because the model can generate "novel" ideas. That claim is subjective, but the prompting pattern is concrete and reusable.

## 3. Apply the same method to coding workflows

A specific coding example in the transcript contrasts:

- **Old loop:** tell the model what to do, then manually test and review
- **New loop:** let the model help define a more structured cycle

The speaker says Fable 5 helped transform their coding workflow into a loop with four phases:

- spec
- morning
- build
- review

The transcript does not fully define each phase, so you should treat this as a reported personal framework rather than a standardized method. Still, the broader lesson is clear:

- stop treating AI coding as one prompt followed by manual cleanup
- ask the model to redesign the workflow itself
- introduce explicit stages for planning, execution, and quality checking

## 4. Build a personal mission control

The second major recommendation is to consolidate recurring tools into one custom application.

Observed examples from the transcript:

- a **newsletter studio** that turns tweets and videos into newsletters
- a **task board** replacing a paid tool
- a **content capture board** for storing ideas

The speaker says they often provide:

- screenshots of other software
- links to products they want to emulate

and ask the model to recreate or adapt the functionality.

### What this architecture looks like from the transcript

There is no repository or file tree in the source, so we should not infer implementation details. What is actually described is a personal app or dashboard containing multiple internal tools, hosted so it can be accessed across devices.

Mentioned supporting services:

- **Vercel** for hosting
- **GitHub** for code-related tasks
- browser access on **phone** and **tablet**

### Suggested prompt

```text
Based on the tools I use regularly, suggest components for a personal mission control.
Prioritize tools that save subscription costs or reduce repetitive work.
For each suggestion, explain the user flow and why it belongs in one dashboard.
```

## 5. Let the model drive feature discovery during vibe coding

The transcript's most distinctive technique is exploratory product development.

Instead of saying:

- "Build feature X"

say something like:

```text
Take a look at this application, its current features, and its purpose.
Come up with five ideas that would improve the app and bring it closer to its goals.
```

Then:

1. Review the options
2. Pick one promising idea
3. Ask the model to expand it
4. Repeat by pulling on the most interesting "strand"

The transcript gives a concrete example:

- the model suggested replacing a static homepage grid with a **daily brief**
- then proposed additional elements for that daily brief
- the user kept developing that direction interactively

This is a form of iterative divergence and convergence:

- **diverge:** ask for several possible directions
- **converge:** choose one
- **expand:** request more detail
- **repeat:** continue until a useful feature emerges

## 6. Use the in-app browser for delegated web work

The speaker claims a newer browser capability lets the model carry out more tasks directly instead of merely instructing the user.

Examples mentioned:

- finding AI-focused YouTube channels
- signing up for websites
- getting API keys
- pushing code live on GitHub
- deploying on Vercel
- uploading environment variables

The phrase the speaker recommends is:

> "No, you do it"

That is, when the model explains a step, ask it to perform the step itself if the browser/tooling allows.

Because these are transcript claims, not product documentation, treat them as capability reports that may depend on the specific app setup, permissions, or timing.

### Safe operational takeaway

When using AI tools with browser access:

- start with low-risk tasks
- verify every external action
- review deployments and environment changes
- avoid assuming the model can safely handle every secret or account action

## 7. Separate ideation from execution across models

The final recommendation is about tool choice under usage limits.

The speaker says:

- use **Fable 5** for ideation, system redesign, and orchestration
- use **ChatGPT** at a medium setting for routine code execution

The reasoning is practical:

- Fable 5 usage is described as limited
- execution work is often less demanding than strategic thinking
- another model may be cheaper or more available for straightforward tasks

Even if you do not share the exact tool preferences, the general pattern is durable:

### A reusable allocation strategy

- **High-level work:** workflow redesign, feature ideation, architectural direction
- **Mid-level work:** transforming ideas into tasks or specs
- **Low-level work:** routine code generation, small edits, repetitive implementation

This lets you preserve scarce capacity for the work where it adds the most value.

## Training Exercise

## Exercise: Redesign one workflow and prototype one mission-control feature

### Part 1: Redesign a personal operating system

1. Choose one recurring workflow, such as:
   - coding
   - research
   - content creation
   - morning routine

2. Write down:
   - the current step-by-step process
   - 3 pain points
   - 3 desired outcomes

3. Paste the following prompt into your AI tool:

```text
Here is my current workflow:
[paste workflow]

My pain points are:
[paste pain points]

My goals are:
[paste goals]

Please rethink this operating system from scratch.
Suggest a better workflow, explain why it is better, and identify the highest-leverage changes first.
```

4. Ask one follow-up question:

```text
What assumptions in my current workflow are probably wrong or outdated?
```

5. Extract the model's suggestions into:
   - things to test this week
   - things to automate later
   - things to stop doing immediately

### Part 2: Design a mission-control module

1. Pick one paid or repetitive tool you use often.

2. Describe it in plain language:
   - what job it does
   - what inputs it needs
   - what output you care about

3. If available, gather:
   - a screenshot
   - a link to the existing tool
   - notes on the exact features you use

4. Prompt the model:

```text
I want to build a small module for my personal mission control.
Its job is:
[describe the job]

The key features I actually use are:
[list features]

Please propose:
1. the simplest version to build first
2. the user flow
3. the minimum interface
4. what can be ignored for now
```

5. Ask for five possible improvements to that module:

```text
Given this module's purpose, suggest five feature directions that would make it more useful.
Focus on practical wins, not flashy additions.
```

6. Choose one suggestion and ask the model to expand it into an implementation plan.

### Part 3: Practice true vibe coding

1. Open an existing project or concept.
2. Do **not** tell the model exactly what to build.
3. Instead use:

```text
Review this project, its current features, and its purpose.
Suggest five ways to improve it that better align it with its goals.
```

4. Pick the most interesting suggestion.
5. Ask:

```text
Expand this idea. What sub-features or design choices make it genuinely useful?
```

6. Repeat once more with the strongest sub-idea.
7. At the end, summarize:
   - the original suggestion
   - the strand you followed
   - the concrete feature you ended up with

### Reflection questions

- Did the model generate ideas you would not have reached on your own?
- Which prompts produced useful novelty versus vague brainstorming?
- Which tasks should remain human-controlled even if browser automation is available?
- If usage is limited, which parts of your workflow deserve the strongest model most?

## Test Yourself

<details><summary>What is reverse prompting, and what information should precede it?</summary>

Reverse prompting asks the model what it would change rather than directing it toward a predetermined solution. It should follow a description of the current workflow, its pain points, and the outcomes you want.

</details>

<details><summary>How does the lesson define “true vibe coding”?</summary>

It is an exploratory process in which the model reviews an application, proposes several directions, and helps expand the most promising idea. The user guides the process by selecting useful strands instead of specifying a fixed feature from the outset.

</details>

<details><summary>Why does the speaker recommend separating ideation from execution across models?</summary>

The speaker claims that a limited, higher-capability model provides more value for strategy, workflow redesign, and novel feature discovery. Routine implementation can then be delegated to a cheaper or more available model, preserving scarce capacity for higher-leverage work.

</details>
