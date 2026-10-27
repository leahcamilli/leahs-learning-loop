---
title: "Generative UI in Microsoft 365 Copilot with MCP and LangGraph"
source: "https://linkedin.com/posts/andreasadner_microsoftcopilot-agui-copilotkit-ugcPost-7460401668283854850-wqmW?rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY"
date: "2026-05-14"
tags: [mcp, copilot, generative-ui, langgraph, agents]
source_type: "web"
topics: [classifiers-and-structured-output, ai-agents]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> Generate constrained, machine-readable UI schemas from user prompts, then let a trusted renderer decide which components and actions appear. This separation enables dynamic interfaces inside Microsoft 365 Copilot while improving safety, validation, and portability.

## Key Takeaways

1. Use Microsoft 365 Copilot as the chat and app-hosting surface, with a custom MCP server defining the boundary to external capabilities.
2. Pass requests through an AG-UI-compatible bridge to a LangGraph agent that can reason, use tools, and produce a structured UI description.
3. Return a constrained schema containing fields such as component type, props, layout, allowed actions, validation rules, and data bindings—not arbitrary React, HTML, or executable UI code.
4. Validate every generated response against an allowlist of supported components before rendering it; the lesson’s prototype starts with text, form, input, select, button, and card.
5. Keep generation separate from rendering so the same UI definition can be validated consistently and potentially rendered across multiple host environments.
6. Prototype the pattern with a POST endpoint that accepts a prompt, maps it to a JSON UI specification, and returns either a task-specific form or a fallback card.
7. Test the prototype with prompts such as “Create a project intake form” and “Show me an expense approval card,” then extend it with conditional fields, schema versioning, and form submission.

## Overview
These notes describe an architecture for generating interactive UI inside Microsoft 365 Copilot at runtime, using a combination of MCP, AG-UI, LangGraph, and CopilotKit’s OpenGenerativeUI ideas. The central pattern is that a user submits a prompt in Copilot, an external MCP app/server handles the request, and an agent produces a structured UI definition that Copilot can render safely in chat.

This matters because it shifts AI experiences from plain text output to dynamic, task-specific interfaces such as forms, cards, and workflows. The key takeaway is the separation between generation and rendering: the model or agent proposes structured UI intent, while a trusted renderer decides what can actually be shown.

## Key Concepts
- **Generative UI**: UI is created dynamically from user intent instead of choosing only from prebuilt screens. The AI outputs a structured representation of components rather than arbitrary frontend code.
- **MCP server**: A custom MCP server exposes app capabilities to Microsoft 365 Copilot via the Model Context Protocol. It acts as the integration boundary between Copilot and downstream services.
- **Microsoft 365 Copilot app rendering**: Copilot can host app experiences directly in chat. The important distinction is that it renders supported app responses rather than executing arbitrary UI code invented by the model.
- **AG-UI bridge**: AG-UI serves as an interchange layer for transporting AI-generated interface structures between the MCP side and the agent side.
- **LangGraph deep agent**: LangGraph orchestrates multi-step reasoning, planning, and stateful execution. It can interpret prompts, decide on tool usage, and emit a structured UI schema.
- **OpenGenerativeUI**: CopilotKit’s approach separates UI generation from UI rendering. This improves safety, composability, and portability across hosts.

## How It Works
The end-to-end flow looks like this:

1. A user enters a natural-language prompt in Microsoft 365 Copilot.
2. Copilot invokes an MCP app exposed by a custom MCP server.
3. The MCP server forwards or translates the request into an AG-UI-compatible interaction.
4. A LangGraph-based agent interprets the request and generates a structured UI description using OpenGenerativeUI-style concepts.
5. The UI definition travels back through the bridge and is rendered inside the Copilot chat experience.

A useful way to think about the system is as a layered contract:

- **Copilot** handles the chat surface and app hosting.
- **MCP server** exposes the capability boundary.
- **AG-UI** carries the generated UI representation.
- **LangGraph agent** reasons about the request and produces structured output.
- **Renderer** turns the approved schema into visible, interactive controls.

The practical design principle is that the agent should emit constrained, machine-readable output instead of raw React or HTML. Typical fields in this contract include:

- component type
- props
- layout structure
- allowed actions
- validation rules
- optional data bindings

Example structured UI schema:

```json
{
  "type": "form",
  "title": "Project Intake",
  "fields": [
    { "type": "text", "name": "project_name", "label": "Project name" },
    { "type": "select", "name": "priority", "label": "Priority", "options": ["Low", "Medium", "High"] },
    { "type": "date", "name": "due_date", "label": "Due date" },
    { "type": "text", "name": "owner", "label": "Owner" }
  ],
  "actions": [
    { "type": "submit", "label": "Create" }
  ]
}
```

This pattern is valuable because it improves:

- **Safety**: only approved components are renderable.
- **Determinism**: outputs can be validated against a schema.
- **Portability**: the same UI definition can be rendered in multiple environments.
- **Composability**: the agent can add planning, retrieval, or tools before producing UI.

### Minimal prototype exercise
A practical exercise from the notes is to build a local prototype that turns prompts into structured UI.

**Goal**: create a small service that accepts a prompt and returns a JSON UI schema for a simple renderer.

**Step 1: Define a tiny UI schema**

```json
{
  "allowedComponents": ["text", "form", "input", "select", "button", "card"]
}
```

**Step 2: Implement a mock agent service**
Create a small Node.js or Python server that:

1. accepts a POST request with `prompt`
2. maps the prompt to a UI JSON spec
3. returns the JSON spec

Example Express handler:

```js
app.post('/generate-ui', (req, res) => {
  const prompt = req.body.prompt || '';

  if (prompt.toLowerCase().includes('project intake')) {
    return res.json({
      type: 'form',
      title: 'Project Intake',
      fields: [
        { type: 'input', inputType: 'text', name: 'project_name', label: 'Project name' },
        { type: 'select', name: 'priority', label: 'Priority', options: ['Low', 'Medium', 'High'] },
        { type: 'input', inputType: 'date', name: 'due_date', label: 'Due date' }
      ],
      actions: [
        { type: 'button', action: 'submit', label: 'Create' }
      ]
    });
  }

  return res.json({
    type: 'card',
    title: 'Fallback UI',
    body: 'No matching template found for prompt: ' + prompt
  });
});
```

**Step 3: Build a tiny renderer**
Render based on the returned `type`:

- `card` → title and text block
- `form` → loop through fields and create native inputs/selects
- `button` → render action buttons

**Step 4: Add validation**
Validate that the response contains only supported component types before rendering.

**Step 5: Simulate the architecture**
Map the prototype to the larger design:

- frontend form = Copilot host surface
- `/generate-ui` endpoint = MCP server + AG-UI bridge
- prompt-to-schema logic = LangGraph/OpenGenerativeUI generation layer

**Step 6: Extend it**
Possible next steps:

- add another prompt type such as an expense approval form
- support conditional fields
- add schema versioning
- post submitted form data back to the server

**Success criteria**
Prompts like these should render different UIs without manually creating each page:

- `Create a project intake form`
- `Show me an expense approval card`

## Test Yourself

<details><summary>Why should the agent emit a structured UI schema instead of raw React or HTML?</summary>

A structured schema can be restricted to approved components and validated before rendering. According to the lesson, this makes the interface safer, more deterministic, and easier to reuse across hosts.

</details>

<details><summary>What role does each architectural layer play in the request flow?</summary>

Copilot hosts the chat experience, the MCP server exposes the capability boundary, AG-UI transports the UI representation, and LangGraph interprets the request and generates structured output. A trusted renderer converts the approved schema into interactive controls.

</details>

<details><summary>What is the minimum validation requirement for the prototype?</summary>

Before rendering, verify that the returned schema contains only supported component types from the allowlist. Unsupported or malformed components should not be rendered.

</details>

## Personal Notes
Generative UI in Microsoft 365 Copilot with MCP, AG-UI, LangGraph, and OpenGenerativeUI

Source: https://www.linkedin.com/posts/andreasadner_microsoftcopilot-agui-copilotkit-ugcPost-7460401668283854850-wqmW?utm_source=social_share_send&utm_medium=ios_app&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY&utm_campaign=share_via
Notion page: https://www.notion.so/Generative-UI-in-Microsoft-365-Copilot-with-MCP-AG-UI-LangGraph-and-OpenGenerativeUI-36001bb0839a81bf98aad7ffac34e235

Tags: mcp, copilot, generative-ui, langgraph, agents, ag-ui

Overview

This lesson explains the architecture behind a generative UI demo for Microsoft 365 Copilot where a user types a prompt and receives an interactive UI component rendered directly in chat. The source post describes a pipeline in which Microsoft 365 Copilot invokes an MCP app served by a custom MCP server, which then bridges to AG-UI and a LangGraph-based agent using CopilotKit's OpenGenerativeUI approach to synthesize UI dynamically.

This matters to engineers building agentic applications because it moves beyond text responses into runtime-generated interfaces. Instead of hardcoding every form, card, or workflow screen in advance, the system can interpret user intent and produce fit-for-purpose UI on demand, opening up new patterns for enterprise copilots, workflow automation, and adaptive frontends.

Key Concepts

  *   Generative UI: Generative UI is the idea that an AI system can create interface components dynamically based on user intent rather than selecting from a fixed set of predefined screens. In practice, this means the model or agent outputs a structured UI description that a renderer can safely display as interactive components.
  *   MCP server: An MCP server exposes tools, apps, or capabilities to a host AI system using the Model Context Protocol. In this scenario, the MCP server acts as the integration point that Microsoft 365 Copilot can call to obtain an app payload or UI-producing capability.
  *   Microsoft 365 Copilot app rendering: Microsoft 365 Copilot can host and render app experiences inside its chat surface. The important architectural point is that Copilot is not directly inventing arbitrary UI markup on its own; instead, it calls into an external app/service that returns a supported renderable experience.
  *   AG-UI bridge: AG-UI provides a way to represent or transport AI-generated interface structures between systems. In this architecture it serves as the bridge layer between the MCP app/server boundary and the downstream agent that decides what UI should be produced.
  *   LangGraph deep agent: Lang
