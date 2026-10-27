---
title: "Using Canvas Extensions in the GitHub Copilot App"
source: "https://docs.github.com/en/copilot/how-tos/github-copilot-app/working-with-canvas-extensions"
date: "2026-07-17"
tags: [github-copilot, extensions, collaboration, workflow, artifacts]
source_type: "web"
source_fingerprint: "0e371f3d5e"
source_characters: 5244
topics: [github-copilot, ai-agents]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> Canvas extensions turn GitHub Copilot collaboration into a persistent, shared workspace where you and the agent can directly inspect, edit, and continue work on the same artifact. This matters because structured workflows become easier to steer, verify, and carry across sessions than chat-only work.

## Key Takeaways

1. Use a canvas when a workflow needs structure, iteration, steering, or visible verification beyond chat.
2. Define both human actions and agent actions explicitly in the `/create-canvas` prompt so the generated interface and capabilities match the workflow.
3. Treat the artifact—not the prompt history—as the shared source of state: users edit through the interface, while the agent acts through capabilities such as `get_board`, `add_card`, or `move_card`.
4. Store team-shared canvases in `.github/extensions` and personal canvases in `~/.copilot/extensions`.
5. Expect a canvas extension directory to commonly contain `package.json`, an entry file such as `extension.mjs`, and optional JSON artifacts for persisted state, while recognizing that GitHub Docs does not prescribe a strict fixed layout.
6. After creation, inspect the canvas in the app’s right side panel and iterate by asking the agent to add, remove, or revise capabilities and interface behavior.

## Overview

Canvas extensions in the GitHub Copilot app matter because they move collaboration with an agent beyond chat and into a shared working surface. Instead of relying only on prompts and text responses, you and the agent can work on the same artifact directly, such as a board, document, checklist, dashboard, or markdown file.

According to the GitHub Docs source, canvases are especially useful when work needs structure, iteration, and verification. They let people inspect progress as visible changes, correct the shared surface directly, and continue work across sessions and handoffs. This makes them a practical fit for workflows where chat helps define intent, but the real work happens in interactive tools and persistent artifacts.

## Key Concepts

- **Canvas extension**: A canvas extension is a shared, interactive surface for a work artifact in the GitHub Copilot app. The source lists examples such as a plan, triage board, browser session, release checklist, dashboard, incident, or spreadsheet.
- **Bidirectional collaboration**: Canvases are bidirectional: the agent can update the canvas while it works, and the user can edit the same surface. This creates a shared state where both human and agent contribute to the artifact.
- **Capabilities**: When a canvas is created, the agent generates capabilities based on the prompt and workflow. These capabilities define what the agent can call and what the canvas supports. The documentation gives examples like get_board, add_card, and move_card.
- **When to use a canvas**: The source says canvases are helpful when chat alone is not enough—especially when a workflow needs structure, iteration, steering, and visible verification. They are meant to ground agent work in an actual artifact or environment.
- **Scope and storage location**: A canvas can be either team-shared or personal. Team-shared canvases use project scope under .github/extensions, while personal canvases use user scope under ~/.copilot/extensions.
- **Extension structure**: Each canvas extension lives in its own directory. Common files include a package.json file for metadata and dependencies, an entry file such as extension.mjs for behavior and capabilities, and optional JSON artifacts for persisted data and state.

## How It Works

## What a canvas does

A canvas gives GitHub Copilot app users a persistent, shared work surface. The source contrasts this with chat: chat is useful for defining intent and discussing tasks, but many workflows actually happen in work surfaces like terminals, browsers, documents, and dashboards. A canvas brings the agent into that surface.

## Why this changes the workflow

With a canvas:

- You can **instruct the agent in chat**.
- You can **inspect the resulting work directly on the surface**.
- You can **edit the artifact yourself**.
- The agent can **continue from your edits**.

This means the artifact itself becomes the center of collaboration, not just the prompt history.

## Example use cases from the source

The documentation names several scenarios:

- **Agentic kanban boards** for adding cards, moving work, and kicking off tasks.
- **Issue triage boards** for summarizing top issues, recurring themes, and user pain points for a repository.
- **Markdown canvases** for planning a day, prioritizing issues and pull requests, launching agent sessions, and keeping related work in one editable surface.
- **Document canvases** for opening and editing documents, spreadsheets, slide decks, and other artifacts directly in the app.

These examples show that a canvas is not limited to one interface type. It is a general mechanism for building a shared artifact with agent-driven behavior.

## How to create a canvas

The source says you create a canvas from within an agent session using the `/create-canvas` skill.

### Basic flow

1. Open or start an agent session.
2. In the prompt box, type `/create-canvas`.
3. Describe:
   - the workflow you want the canvas to support
   - what people should be able to do
   - what the agent should be able to do
4. Wait for the agent to build the canvas.
5. The completed canvas opens in the app's right side panel.

### Prompting guidance

The documentation suggests being explicit about both sides of the collaboration:

- **Human actions**: for example, creating, assigning, or moving cards.
- **Agent actions**: for example, calling capabilities that update state or take actions.

Example requests from the source include:

- Create an agentic kanban canvas with actions to create, assign, and move cards.
- Create a markdown canvas that combines meetings with prioritized issues and pull requests, then lets the user launch and track agent sessions.

## Personal vs shared canvases

The GitHub Docs page distinguishes two scopes.

### Project scope

- Location: `.github/extensions`
- Purpose: team-shared canvases committed to the repository

### User scope

- Location: `~/.copilot/extensions`
- Purpose: personal canvases on your machine

This distinction matters because it affects whether the canvas is part of team workflow or just local personal tooling.

## Observed extension structure

The source does not define a strict required layout beyond the directory placement, but it says a canvas extension commonly includes:

- `package.json` for extension metadata and dependencies
- an entry file such as `extension.mjs` that defines behavior and capabilities
- optional JSON artifacts, such as files under an `artifacts` directory, for persisted data and state

A practical mental model is:

- **Metadata and dependencies** live in `package.json`
- **Runtime behavior** lives in the entry file
- **Persistent shared state** may live in JSON artifact files

The page also notes that implementations can vary, so this should be read as a common pattern rather than a guaranteed fixed schema.

## How interaction works after creation

Once open, the canvas becomes a fast iteration loop between human and agent.

You can:

- ask the agent to add, remove, or revise capabilities
- use UI controls such as buttons, cards, or filters to update the surface directly
- ask the agent to call exposed capabilities to update data or take actions

The important architectural point from the source is that both people and agents interact with the **same shared state** through UI actions and agent-callable capabilities.

## Core benefit

The main benefit is continuity. Work can persist across turns, sessions, and handoffs, while remaining visible and editable. Instead of the agent only narrating progress in chat, the work appears directly in the artifact you both share.

## Training Exercise

## Exercise: Design and create your first canvas prompt

This exercise focuses on using the documented workflow to define a useful canvas. It does not assume undocumented implementation details.

### Goal

Create a clear `/create-canvas` prompt for a workflow that benefits from a shared artifact.

### Step 1: Pick a workflow

Choose one workflow from the source examples or a close equivalent:

- kanban board
- issue triage board
- markdown planning surface
- document-centered collaboration

Write down:

- what artifact will be shared
- what a human should be able to do on it
- what the agent should be able to do on it

### Step 2: Decide the scope

Choose whether your canvas should be:

- **team-shared** in `.github/extensions`, or
- **personal** in `~/.copilot/extensions`

Briefly justify your choice. For example, use team-shared if the workflow belongs in a repository, or personal if it is just for your own planning.

### Step 3: Draft the prompt

Open or start an agent session, then draft a `/create-canvas` request.

Use this template:

```text
/create-canvas Create a [type of canvas] for [workflow].
People should be able to: [human actions].
The agent should be able to: [agent actions].
Keep this canvas [personal/team-shared].
```

Example:

```text
/create-canvas Create a markdown canvas for daily planning.
People should be able to edit priorities, track meetings, and review issues and pull requests.
The agent should be able to update the markdown surface, help prioritize work, and track related agent sessions.
Keep this canvas personal.
```

### Step 4: Review the result in the right side panel

After the agent creates the canvas, inspect whether it supports:

- the intended artifact type
- visible controls or editable surfaces
- the workflow you requested
- agent-usable capabilities that match your description

### Step 5: Iterate on capabilities

Ask the agent to revise the canvas in one specific way. For example:

- add a capability
- remove a capability
- change the interface
- adjust the shared state the canvas manages

Write one follow-up instruction such as:

```text
Please revise the canvas so the agent can also summarize recurring themes from issues.
```

### Step 6: Reflect

Answer these questions:

1. Why was chat alone not enough for this workflow?
2. What part of the canvas gave you direct verification of progress?
3. Would this work better as a personal or repository-shared canvas?
4. What shared state did both you and the agent interact with?

### Success criteria

You have completed the exercise if you can:

- explain what the canvas artifact is
- describe at least two human actions and two agent actions
- identify the correct storage scope
- explain how the canvas supports bidirectional collaboration

## Test Yourself

<details><summary>When is a canvas more appropriate than chat alone?</summary>

According to GitHub Docs, a canvas is useful when work needs a structured, editable artifact, repeated iteration, steering, or direct visual verification. Examples include kanban boards, issue triage, planning documents, dashboards, and release checklists.

</details>

<details><summary>What should a strong `/create-canvas` prompt specify?</summary>

It should name the artifact and workflow, the actions people must be able to perform, the actions or capabilities the agent needs, and whether the canvas is personal or team-shared.

</details>

<details><summary>How do project-scoped and user-scoped canvases differ?</summary>

Project-scoped canvases are stored in `.github/extensions` and can be committed for team use. User-scoped canvases are stored in `~/.copilot/extensions` for personal use on the local machine.

</details>
