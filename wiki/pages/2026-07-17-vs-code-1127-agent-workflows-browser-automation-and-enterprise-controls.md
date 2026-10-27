---
title: "VS Code 1.127: Agent Workflows, Browser Automation, and Enterprise Controls"
source: "https://code.visualstudio.com/updates/v1_127"
date: "2026-07-17"
tags: [vscode, agents, copilot, browser, enterprise, developer-tools]
source_type: "web"
topics: [coding-agents, ai-agents, github-copilot, developer-tools]
kind: "news"
depth: 2
actionability: 1
---

## TL;DR

> VS Code 1.127 turns agent-assisted development into a more complete, governable workflow by combining parallel session management, in-editor browser testing, sandboxed command execution, and PR/CI feedback. This matters because teams can move faster with agents while retaining explicit permissions and enterprise policy controls.

## Key Takeaways

1. Use the Agents window to group, reorder, pin, and monitor concurrent agent sessions across projects and machines.
2. Create peer chats within one host session when work streams should run in parallel while sharing session context, aggregated progress, and combined file changes.
3. Let agents validate web apps through the integrated browser by opening pages, inspecting content and console errors, taking screenshots, clicking controls, and typing into forms.
4. Review browser permissions per site for sensitive capabilities such as camera, microphone, location, clipboard, Bluetooth, USB, serial, and HID access.
5. On macOS and Linux, use terminal sandboxing to run eligible agent commands with blocked network access and restricted filesystem access; commands needing broader privileges require approval.
6. Handle failed CI and review comments from chat input banners with actions such as Fix Checks, Reveal Checks, Address Comments, and Reveal Comments.
7. Distribute enterprise Copilot policy through managed-settings.json when MDM or account-based settings are absent, using the documented OS-specific location.

## Overview

Visual Studio Code 1.127 expands the IDE from a coding surface into a more complete agent workspace. The release centers on agent-driven development: a dedicated Agents window for managing concurrent sessions, integrated browser tools that let agents validate web apps in-place, safer execution via terminal sandboxing, and tighter loops around pull requests, CI failures, and code review feedback.

This matters to engineers adopting AI-assisted development at team scale. Individual developers get better workflow control for multi-session agent work, while platform and security teams get more explicit browser permissions, network governance, and file-based enterprise policy delivery. The release is especially relevant for teams building web apps, using Copilot agents, or standardizing managed AI features in VS Code.

## Key Concepts

- **Agents window**: The Agents window is a dedicated interface for creating, reviewing, and organizing agent sessions across projects and machines. In 1.127 it gains grouping, drag-and-drop organization, session-focused keyboard behavior, and better signals for session state, making concurrent agent work more manageable.
- **Multi-chat sessions**: A single agent host session can now contain multiple parallel chats, each with its own tab and progress, while still sharing a higher-level session context. VS Code aggregates status and file changes across those chats so you can reason about the full session instead of only the active conversation.
- **Integrated browser tools for agents**: Agents can now open pages, inspect content and console errors, take screenshots, click elements, type into forms, and navigate pages using the built-in browser tools. This enables a closed loop where an agent can build a web app, run it, test it in-browser, detect failures, and iterate without relying on an external browser automation server.
- **Per-site browser permissions**: The integrated browser now supports permission prompts and per-site management for sensitive web APIs like camera, microphone, location, clipboard, and connected devices. This makes the embedded browser behave more like a normal browser while preserving explicit user approval and site-scoped control.
- **Terminal sandboxing**: On macOS and Linux, agent-invoked terminal commands can run in a sandbox with blocked network access and restricted filesystem access. The goal is to reduce repetitive approval prompts while containing low-risk commands, only escalating to explicit approval when a command needs broader privileges.
- **PR and CI feedback in chat**: Agent sessions with open pull requests can surface banners directly above the chat input for failing CI checks and incoming review comments. That keeps the remediation loop inside the conversation, reducing context switching between the agent UI, source control views, and pull request tooling.
- **Enterprise-managed AI settings**: Organizations can now distribute managed Copilot settings from a local JSON file in a well-known OS-specific path, in addition to MDM or account-based delivery. This gives administrators another control plane for policy enforcement on machines that are not managed through traditional device management.

## How It Works

VS Code 1.127 improves the mechanics of agent-driven development by tightening the control loop around three areas: **session management**, **tool execution**, and **organizational governance**.

At the session-management layer, the **Agents window** acts as the central UI for agent work. Sessions can now be grouped into custom buckets, rearranged with drag and drop, pinned, and batch-moved. This is important because agent usage naturally leads to concurrency: one session may be implementing a feature, another debugging tests, and another preparing a pull request. The release adds workflow structure so those parallel threads do not degrade into a flat, noisy list.

Within a single session, **multi-chat sessions** provide a second level of parallelism. Instead of opening a new top-level session for every branch of inquiry, you can create peer chats as tabs in one host session. A fork now becomes a sibling chat in that same session, preserving shared context while allowing independent work streams. VS Code aggregates progress and file changes across all peer chats so the session header reflects the total state of work, not just the visible tab.

The session UI also gets more consistent affordances:

- The header uses compact pills for actions and metadata.
- A **Workspace pill** shows which workspace the session is operating on.
- A **Changes pill** reports the session's file delta and opens the default changeset.
- Focus moves directly to the chat input when a session is opened, which improves keyboard-driven workflows.
- An experimental auto-collapse setting can hide the sessions sidebar on narrow layouts.

A major functional change is the general availability of **browser tools for agents**. These tools are built into VS Code's integrated browser rather than requiring an external MCP-style browser server. The agent can:

- Open web pages
- Read page content
- Inspect console errors
- Take screenshots
- Click and type in the page
- Navigate through flows to verify behavior

This gives agents a practical build-test-fix loop for web applications. A likely flow is:

1. The agent edits app code.
2. The app is run locally.
3. The agent opens the local site in the integrated browser.
4. It checks rendering, interacts with UI controls, and captures runtime errors.
5. It patches code and repeats until the scenario passes.

That browser automation is paired with a new **permission model** in the integrated browser. Pages can request access to location, camera, microphone, sensors, clipboard, or attached devices such as Bluetooth, USB, serial, and HID. VS Code prompts the user per site, and permissions can be managed from the browser menu. This matters because browser automation without clear permission boundaries would be unsafe in enterprise environments.

Agent execution is also improved outside the browser. On macOS and Linux, **terminal sandboxing** reduces friction by allowing many agent-triggered commands to run in a constrained environment without prompting every time. The sandbox blocks network access and restricts filesystem access; only commands that need to escape those limits require explicit approval. Conceptually, the decision flow looks like this:

```text
Agent wants to run command
  -> Can it run inside sandbox?
       -> yes: run with reduced privileges, no prompt
       -> no: request user approval for elevated execution
```

For debugging agent behavior, the `/troubleshoot` skill now works with agent host sessions, including local and remote ones. You invoke it from the chat input, attach a target session with `#session`, and ask a question about ignored instructions, slow responses, or unexpected behavior. Under the hood, VS Code uses session logs as evidence and surfaces likely causes.

The release also shortens the collaboration loop around pull requests. When an agent session has an open PR, **chat input banners** appear above the conversation input. These banners provide single-purpose actions such as:

- **Fix Checks** for failed CI
- **Reveal Checks** to inspect failures in the Changes view
- **Address Comments** to hand incoming review comments back to the agent
- **Reveal Comments** to open comment locations in the editor

This is reinforced by **editor gutter feedback** for agent changes. Instead of describing a code issue in prose, you can hover the gutter on a changed line and leave structured feedback exactly where the agent should revise code. Pull request creation is also smarter: generated titles and descriptions now use session context, producing outputs that better match the actual work done.

For cost visibility, subagent sections in a response expose **credit usage on hover**. This is a small but important operational feature because delegated work can obscure where model spend is coming from.

On the language-model integration side, the built-in **Ollama provider** is being deprecated in favor of the official VS Code extension. The architectural takeaway is that model providers should increasingly ship independently via extensions, which allows faster iteration and clearer ownership than bundling providers into the core editor.

For administrators, 1.127 adds a file-based path for **managed Copilot settings**. VS Code will read `managed-settings.json` from a well-known OS-specific location when MDM or account-based enterprise settings are absent:

- macOS: `/Library/Application Support/GitHubCopilot/managed-settings.json`
- Linux: `/etc/github-copilot/managed-settings.json`
- Windows: `%ProgramFiles%\GitHubCopilot\managed-settings.json`

The file uses the same schema as GitHub enterprise settings, for example:

```json
{
  "permissions": {
    "disableBypassPermissionsMode": "disable"
  },
  "enabledPlugins": {
    "plugin@marketplace": false
  }
}
```

This complements policy controls for browser tools, including the ability to disable them entirely or restrict reachable domains via agent network filtering. In practice, the release shows VS Code maturing from a single-user AI editor feature into a governed platform for agent-assisted engineering.

## Training Exercise

Build a small web-app workflow in VS Code 1.127 that uses an agent, the integrated browser, and PR-style feedback loops.

### Goal
Experience the new agent workflow end to end:

1. create an agent session
2. ask the agent to build or modify a simple web page
3. have it validate the page with browser tools
4. leave targeted feedback in code
5. inspect how session organization and chat actions work

### Prerequisites

- VS Code 1.127 or newer
- GitHub Copilot agent features enabled in your environment
- Browser tools enabled by your organization or local setup
- A local project folder

### Step 1: Create a minimal app
Open a terminal and create a tiny static app:

```bash
mkdir vscode-agent-demo
cd vscode-agent-demo
cat > index.html <<'EOF'
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Agent Demo</title>
  <style>
    body { font-family: sans-serif; margin: 2rem; }
    button { padding: 0.5rem 1rem; }
    #msg { margin-top: 1rem; color: #0a7; }
  </style>
</head>
<body>
  <h1>Agent Demo</h1>
  <button id="go">Click me</button>
  <div id="msg"></div>
  <script>
    document.getElementById('go').addEventListener('click', () => {
      document.getElementById('msg').textContent = 'Hello from VS Code 1.127';
    });
  </script>
</body>
</html>
EOF
python3 -m http.server 8000
```

Keep the server running.

### Step 2: Open the project in VS Code and start an agent session

1. Open the folder in VS Code.
2. Open the **Agents window**.
3. Create a new session in a group called `demo`.
4. Ask the agent: 

```text
Open the local app at http://localhost:8000 in the integrated browser, verify the button click behavior, and improve the page styling if needed.
```

### Step 3: Observe browser-tool behavior
Watch for these actions from the agent:

- page open/navigation
- content inspection
- screenshot capture or validation steps
- interaction with the button
- possible code changes based on what it sees

If the page requests a permission in another experiment, inspect the **Site Permissions** menu and note the per-site model.

### Step 4: Create a peer chat in the same session
Use **+ New Chat** to open a second chat in the same session. Ask it:

```text
In parallel, add a dark mode toggle to the page and keep the existing behavior intact.
```

Now compare:

- progress indicators on each chat tab
- aggregated session progress
- combined file changes in the session header

### Step 5: Leave targeted feedback from the editor gutter
When the agent has changed `index.html`:

1. Open the file diff or changed file.
2. Hover the gutter next to a changed line.
3. Use **Add Feedback**.
4. Leave a specific instruction such as:

```text
Move the inline script into a separate file and keep behavior identical.
```

Ask the agent to address that feedback.

### Step 6: Test session organization
In the Agents window:

1. Create another session named `cleanup`.
2. Drag it into the `demo` group.
3. Reorder sessions.
4. Pin the main session.
5. Collapse and expand the group.

This helps you build muscle memory for working with multiple long-running agent tasks.

### Step 7: Troubleshoot intentionally
Ask one chat to do something vague, for example:

```text
Refactor this app to be cleaner.
```

If the response is unhelpful, run:

```text
/troubleshoot #session
```

Attach the session and ask:

```text
Why did the agent produce a broad refactor instead of a minimal structural change?
```

### What to reflect on
Document your answers to these questions:

- What information did the browser tools give the agent that plain code editing would not?
- How did multi-chat sessions differ from separate top-level sessions?
- Did gutter feedback improve precision compared with normal chat instructions?
- Where would terminal sandboxing matter in your real workflow?
- If you manage developer machines, how would file-based Copilot settings help policy rollout?

### Stretch exercise
Simulate team governance by drafting a sample `managed-settings.json` for your OS that disables a plugin or bypass permission mode, then compare it against your organization's preferred Copilot policy model.

## Test Yourself

<details><summary>How do multi-chat sessions differ from separate top-level agent sessions?</summary>

Peer chats are parallel tabs inside one host session, so they share higher-level context while maintaining independent conversations and progress. VS Code aggregates their status and file changes into the host session.

</details>

<details><summary>What safety boundaries apply when an agent uses browser tools or runs terminal commands?</summary>

Browser access to sensitive APIs requires explicit, site-scoped permission, while terminal sandboxing on macOS and Linux blocks network access and restricts filesystem access. Operations that exceed the sandbox require user approval.

</details>

<details><summary>How does VS Code 1.127 help organizations govern agent-assisted development?</summary>

According to the release, administrators can manage Copilot through a local managed-settings.json file when other enterprise delivery methods are absent, and can control browser tools and reachable domains. This adds enforceable policy controls alongside user-facing permission prompts and sandboxing.

</details>

## Further Reading

- [Visual Studio Code 1.127 Release Notes](https://code.visualstudio.com/updates/v1_127)
- [Build and test web apps with browser agent tools](https://code.visualstudio.com/docs/copilot/chat/browser-tools)
- [Agent sandboxing in VS Code](https://code.visualstudio.com/docs/copilot/chat/sandbox)
- [Configure AI settings for your organization](https://code.visualstudio.com/docs/setup/enterprise)
- [GitHub Copilot Enterprise managed client settings](https://docs.github.com/copilot)
