---
title: "VS Code 1.122: Agents, Air-Gapped BYOK, and Integrated Browser Device Emulation"
source: "https://code.visualstudio.com/updates/v1_122"
date: "2026-05-28"
tags: [vscode, ai-agents, byok, opentelemetry, web-debugging, remote-development]
source_type: "web"
topics: [developer-tools, github-copilot, coding-agents, ai-agents]
kind: "news"
depth: 2
actionability: 1
---

## TL;DR

> VS Code 1.122 makes agent sessions, self-managed AI models, and responsive browser testing more integrated with the editor. It enables chat in restricted or offline environments without GitHub sign-in while shortening the loop from reproducing a UI problem to sharing it with an agent.

## Key Takeaways

1. Configure a BYOK provider through Manage Language Models to use chat, tools, and MCP servers without GitHub authentication; inline suggestions and Next Edit Suggestions still require GitHub sign-in.
2. Map chat.utilityModel and chat.utilitySmallModel to configured BYOK models when signed out, or helper features such as chat-title and commit-message generation remain unavailable.
3. Use the Stable Custom Endpoint provider with compatible Chat Completions, Responses, or Messages APIs to connect VS Code to self-hosted or enterprise-managed model gateways.
4. Review Agents window metadata—including the harness, project, worktree, and changed files—to understand where and how each agent session operated.
5. Export local agent telemetry through the canonical github.copilot.* OpenTelemetry namespace to analyze repository context, agent type, tool parameters, and hook outcomes.
6. Expect terminal sandboxing only in Default Approvals mode; Bypass Approvals and Autopilot no longer attempt commands inside the sandbox before retrying outside it.
7. Open Show Emulation Toolbar in the integrated browser to test viewport, touch, and user-agent behavior, then use Add Screenshot to Chat to provide visual debugging context.

## Overview

Visual Studio Code 1.122 expands VS Code’s AI and web-development workflows in three important ways: a more capable Agents window, Bring Your Own Key (BYOK) support that no longer requires GitHub sign-in, and built-in browser device emulation for responsive testing. The release also improves issue reporting and refines sandbox behavior for agent-driven terminal actions.

This matters to engineers building with AI-assisted workflows, teams operating in restricted or air-gapped environments, and frontend developers who want to test responsive behavior without leaving the editor. If you already use VS Code for coding, debugging, or remote environments, this release shows how AI model configuration, observability, and browser tooling are increasingly becoming part of the core IDE experience.

## Key Concepts

- **Agents window**: The Agents window is a dedicated companion UI for exploring and reviewing agent sessions across projects, worktrees, and machines. Rather than treating chat as a side panel inside a single editor window, it makes agent activity a first-class workflow surface with session metadata and model management.
- **BYOK without sign-in**: VS Code now allows Bring Your Own Key language model providers to power chat, tools, and MCP servers without requiring GitHub authentication. This is significant for enterprise, restricted-network, and fully offline scenarios, especially when using local providers like Ollama.
- **Utility models**: Some VS Code AI features use smaller helper models for tasks such as chat title generation, commit message generation, and feedback flows. When signed out and using BYOK, those utility model settings must be explicitly mapped to a configured BYOK model or those helper features remain unavailable.
- **Custom Endpoint provider**: The Custom Endpoint provider connects VS Code to endpoints that implement common LLM APIs such as Chat Completions, Responses, or Messages. This lets teams wire VS Code into self-hosted or enterprise-managed model gateways without depending on a single hosted provider.
- **Agent observability with OpenTelemetry**: Local agent sessions now emit telemetry using a canonical github.copilot.* OpenTelemetry attribute namespace. These signals include repository context, agent type, tool parameters, and hook outcomes, making agent usage easier to monitor and analyze in standard observability pipelines.
- **Integrated browser device emulation**: The integrated browser can now emulate device characteristics like viewport size, touch behavior, and user-agent strings. This makes responsive UI testing available directly inside VS Code, reducing context switching to external browsers or devtools.
- **Approval-mode-aware sandboxing**: Terminal sandboxing behavior for agents has been narrowed so it applies only under Default Approvals mode. This makes command execution easier to reason about because commands run with Bypass Approvals or Autopilot are no longer retried in and then outside the sandbox.

## How It Works

VS Code 1.122 is best understood as a set of connected workflows rather than a single feature. The release strengthens three layers of the editor stack:

1. **Interaction layer**: the Agents window and richer issue reporting UI
2. **Model/runtime layer**: BYOK providers, custom endpoints, and utility model configuration
3. **Execution/inspection layer**: sandboxing, OpenTelemetry signals, and integrated browser emulation

### 1) Agents become a more explicit workflow surface
The Agents window is no longer just a place to send prompts. It is a session-oriented interface for reviewing agent work across projects and machines. Session hover details expose operational metadata such as:

- session title
- harness used
- project
- worktree
- files changed

That detail matters because AI-assisted development increasingly involves multiple runs, different harnesses, and multiple codebases. Surfacing session metadata makes it easier to audit what an agent did and where it did it.

There is also early support for a **local VS Code harness** in Insiders, gated by the setting:

```json
{
  "sessions.chat.localAgent.enabled": true
}
```

This suggests the agent architecture is becoming more modular: a session is tied not only to a model, but also to a harness that determines how the agent interacts with the workspace and tools.

### 2) BYOK is now decoupled from GitHub identity
Previously, using your own API key still required a GitHub sign-in. In 1.122, that dependency is removed for chat-centric AI workflows. After configuring one or more models through **Manage Language Models**, VS Code can enable the Chat view and send requests directly to the configured provider.

Supported provider patterns include:

- Anthropic
- Azure
- Gemini
- OpenAI
- Ollama
- OpenRouter
- Custom endpoint

The key architectural change is that **model configuration now gates chat availability**, rather than GitHub identity alone. Once a BYOK model is configured, the editor can operate in restricted environments where GitHub auth is not allowed.

There is an important boundary: **inline suggestions and Next Edit Suggestions still require GitHub sign-in**. So the AI feature set is effectively split into two categories:

- **BYOK-capable**: chat, tools, MCP servers
- **GitHub-sign-in-required**: inline completions and NES

This is useful when planning enterprise rollout because it clarifies which capabilities can run fully offline and which still depend on Copilot-backed services.

### 3) Utility models fill in non-chat AI tasks
VS Code uses smaller models for lightweight tasks like generating chat titles and commit messages. In a signed-out BYOK setup, those default utility models are unavailable. The editor therefore prompts you to map these settings to your own configured models:

```json
{
  "chat.utilityModel": "your-provider:model-a",
  "chat.utilitySmallModel": "your-provider:model-b"
}
```

Operationally, this means there are at least two classes of model references in the product:

- the main model used for conversational or tool-driven tasks
- one or more utility models used by ancillary product features

If you skip utility model configuration, chat still works, but those smaller AI-assisted conveniences remain disabled.

### 4) Model management is becoming an editor-wide service
Model management is available both from the main editor and from the Agents window, and configuration is shared between them. That implies a centralized model registry/configuration layer inside VS Code rather than per-window state.

The release also improves provider-group maintenance with targeted actions such as:

- Update API Key
- Add Model
- Rename Group
- Delete

This reduces direct JSON editing and suggests that provider definitions are schema-driven. VS Code can expose different actions depending on the provider type and configuration schema.

### 5) Custom endpoints broaden enterprise deployment options
The Custom Endpoint provider is now in Stable. Its purpose is to let VS Code connect to model-serving endpoints that implement common API contracts:

- Chat Completions
- Responses
- Messages

This matters architecturally because VS Code is not limited to branded first-party integrations. If an internal platform team exposes a compatible endpoint behind corporate auth and policy controls, developers can use that endpoint as a model backend inside the editor.

### 6) Agent activity is now easier to observe
Local agent sessions emit richer OpenTelemetry data in a canonical `github.copilot.*` namespace. The emitted attributes include:

- repository context
- agent type
- structured tool parameters
- hook outcomes

This is important because AI usage in engineering environments increasingly needs observability comparable to CI, APIs, or background jobs. With OTel-compatible signals, teams can answer questions like:

- Which repositories are using agents most heavily?
- Which tools are invoked during sessions?
- How often do hook failures occur?
- What kinds of agent sessions correlate with successful outcomes?

In practical terms, VS Code is integrating with existing telemetry backends instead of inventing a separate monitoring stack for agent behavior.

### 7) Sandboxing behavior is simpler and more predictable
In prior behavior, commands run under Bypass Approvals or Autopilot were attempted in a sandbox first, then retried outside it if they failed. Since those modes already bypassed approval, that retry model introduced complexity without much safety value.

Now, terminal sandboxing only applies under **Default Approvals**. That creates a clearer execution model:

- **Default Approvals**: sandboxing can provide guardrails
- **Bypass Approvals / Autopilot**: run behavior is more direct and easier to reason about

The related setting is organization-managed:

```json
{
  "chat.agent.sandbox.enabled": true
}
```

Because it is org-controlled, sandbox policy is treated as an administrative governance concern rather than a personal preference.

### 8) The integrated browser now covers a common frontend testing loop
The integrated browser adds built-in device emulation, including:

- screen sizes
- mobile/touch emulation
- custom user-agents

This closes a practical gap for frontend engineers. Instead of launching an external browser and switching into separate devtools, you can open the site in VS Code’s integrated browser and use **Show Emulation Toolbar** from the overflow menu.

The release also adds **Add Screenshot to Chat**, which turns the current browser viewport into chat context. That creates a direct loop:

1. Render the app in the integrated browser
2. Emulate a mobile device
3. Capture a screenshot
4. Attach it to chat
5. Ask the agent to diagnose layout or responsiveness issues

That is a notable product pattern: browser state becomes direct input to AI assistance.

### 9) Issue reporting is becoming richer and more reproducible
The new issue reporting wizard, behind the setting below, guides users through producing better bug reports with screenshots and video recordings:

```json
{
  "issueReporter.wizard.enabled": true
}
```

From an engineering-process perspective, this improves the quality of diagnostic data collected at bug-report time. Instead of relying on free-form text alone, the product nudges users to capture reproducible evidence, which should improve triage and debugging efficiency.

### 10) Remote development note
The release notes also mention Remote Development updates, including end-of-life for 32-bit ARM Linux hosts. While not deeply detailed here, it is a reminder that VS Code’s AI and browser improvements are layered on top of a broader multi-environment development platform that includes Dev Containers, SSH, Tunnels, and WSL.

## Training Exercise

Set up a practical VS Code 1.122 workflow that combines BYOK chat and browser device emulation.

### Goal
Use a BYOK model without GitHub sign-in, open a simple web page in the integrated browser, emulate a mobile device, and capture a screenshot for AI-assisted debugging.

### Prerequisites
- VS Code 1.122 or later
- A local or remote model provider, such as Ollama or OpenAI-compatible endpoint
- A small local web project

### Step 1: Create a minimal responsive page
Create `index.html` with the following content:

```html
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Responsive Test</title>
  <style>
    body { font-family: sans-serif; margin: 0; }
    .container {
      display: flex;
      gap: 16px;
      padding: 16px;
    }
    .card {
      flex: 1;
      min-height: 120px;
      background: #ececec;
      border-radius: 8px;
      padding: 16px;
    }
    @media (max-width: 600px) {
      .container {
        flex-direction: column;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="card">Card A</div>
    <div class="card">Card B</div>
    <div class="card">Card C</div>
  </div>
</body>
</html>
```

### Step 2: Serve the page locally
From the project folder, run one of these commands:

```bash
python -m http.server 8000
```

or

```bash
npx serve .
```

### Step 3: Configure a BYOK model
In VS Code:
1. Open the Command Palette.
2. Run `Chat: Manage Language Models`.
3. Add a provider such as Ollama, OpenAI, or Custom Endpoint.
4. Confirm the Chat view appears even if you are not signed in to GitHub.

If prompted, configure utility models too.

### Step 4: Open the app in the integrated browser
1. Open the local URL, for example `http://localhost:8000`.
2. In the integrated browser tab, open the overflow menu.
3. Select `Show Emulation Toolbar`.
4. Switch to a mobile-sized viewport and enable touch emulation if available.

### Step 5: Intentionally introduce a layout bug
Edit the CSS to break the mobile behavior:

```css
@media (max-width: 600px) {
  .container {
    flex-direction: row;
  }
}
```

Reload the page in the integrated browser and verify the mobile layout is now cramped or overflowing.

### Step 6: Use screenshot-to-chat
1. Use `Add Screenshot to Chat` from the browser integration.
2. In chat, ask:
   - `Why does this layout break on small screens?`
   - `Suggest the smallest CSS fix.`
   - `Explain how to test this across multiple device sizes.`

### Step 7: Apply and verify the fix
Update the CSS based on the response and retest in at least two emulated device sizes.

### Step 8: Optional observability exercise
If your environment supports agent telemetry collection, inspect emitted OpenTelemetry data and identify which session attributes capture repository or tool context.

### What to learn from the exercise
By the end, you should be able to:
- configure BYOK models without GitHub sign-in
- understand the boundary between chat features and utility-model-backed features
- use integrated device emulation for responsive testing
- feed visual browser context into AI chat for UI debugging

## Test Yourself

<details><summary>Which AI capabilities can operate through BYOK without GitHub sign-in, and which still require it?</summary>

Chat, tools, and MCP servers can use a configured BYOK provider without GitHub authentication. Inline suggestions and Next Edit Suggestions still require GitHub sign-in.

</details>

<details><summary>Why might some AI conveniences remain disabled after a signed-out BYOK setup begins working?</summary>

VS Code uses separate utility models for tasks such as generating chat titles and commit messages. In a signed-out setup, chat.utilityModel and chat.utilitySmallModel must be mapped explicitly to configured BYOK models.

</details>

<details><summary>How does VS Code 1.122 support a faster responsive-debugging loop?</summary>

The integrated browser can emulate screen size, touch behavior, and user-agent strings. Developers can reproduce a mobile layout issue, attach the current viewport with Add Screenshot to Chat, apply a suggested fix, and retest without leaving VS Code.

</details>

## Further Reading

- [VS Code Release Notes 1.122](https://code.visualstudio.com/updates/v1_122)
- [VS Code Agents Window Documentation](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode)
- [VS Code Language Models and BYOK Documentation](https://code.visualstudio.com/docs/copilot/customization/language-models)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Playwright Emulation Guide](https://playwright.dev/docs/emulation)
