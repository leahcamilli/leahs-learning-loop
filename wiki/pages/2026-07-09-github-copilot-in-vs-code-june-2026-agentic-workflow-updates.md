---
title: "GitHub Copilot in VS Code: June 2026 Agentic Workflow Updates"
source: "https://github.blog/changelog/2026-07-08-github-copilot-in-visual-studio-code-june-2026-releases/"
date: "2026-07-09"
tags: [vscode, github-copilot, agentic-ai, developer-tools, llm, productivity]
source_type: "web"
topics: [github-copilot, coding-agents, ai-agents, developer-tools]
kind: "news"
depth: 2
actionability: 2
---

## TL;DR

> GitHub says Copilot in VS Code 1.123–1.127 is evolving from a prompt-response assistant into a managed workspace for parallel, autonomous agent tasks. Richer browser context, persistent sessions, cost visibility, model controls, and governance make complex agent workflows easier to organize and supervise.

## Key Takeaways

1. Split implementation, testing, documentation, and review into separate chats or side-by-side sessions to keep complex workstreams focused.
2. Use the integrated browser and screenshot attachments to give Copilot direct visual context when validating UI behavior or diagnosing rendering problems.
3. Review total session cost and delegated subagent usage, because agentic tasks can consume resources through multiple nested operations.
4. Match models to tasks inside VS Code by adjusting provider, context size, and reasoning effort; compatible Anthropic and OpenAI models support context windows up to 1 million tokens.
5. Use Autopilot for multi-step execution when appropriate, while checking whether it completes every requirement instead of stopping early or continuing unnecessarily.
6. Treat sessions as durable engineering artifacts by syncing and searching them, commenting on agent changes in the gutter, and generating pull request drafts from session context.
7. Keep remote validation aligned with the runtime environment by using integrated browsing that proxies HTTP(S) traffic through remote workspaces.

## Overview

This changelog summarizes how GitHub Copilot in Visual Studio Code evolved across VS Code 1.123 through 1.127, with a focus on making agent-driven development more practical in day-to-day engineering work. The updates are not just UI polish: they change how developers coordinate long-running agent tasks, supply browser and workspace context, monitor credit usage, select models, and let agents operate more autonomously.

Engineers who use Copilot regularly in VS Code will care because these features directly affect workflow design. If you split work into parallel tracks, work in remote environments, experiment with multiple model providers, or need tighter operational control over costs, permissions, and team settings, these releases make Copilot feel more like a managed development platform than a simple code-completion assistant.

## Key Concepts

- **Agentic browser tooling**: The integrated browser in VS Code now supports agent-driven web interaction as a first-class capability. Agents can navigate pages, inspect content, capture screenshots, and validate applications without leaving the editor, which reduces context switching during web development and debugging.
- **Parallel agent sessions**: VS Code now supports side-by-side sessions and multiple chats within a single session. This lets developers decompose larger changes into separate streams such as implementation, review, testing, and documentation while still keeping the work organized under a broader task.
- **Cost observability**: Copilot usage is now more visible at the session level, delegated subagent level, and through the status dashboard. This matters because agentic workflows often involve longer chains of actions and delegated tasks, making cost harder to reason about if only individual prompts are tracked.
- **Model provider discovery and tuning**: VS Code now surfaces model provider extensions through the Language Models editor and Marketplace integration. Developers can more easily discover available providers and adjust model-specific settings like context size and reasoning effort based on task needs.
- **Autopilot execution model**: Autopilot is the permission mode that allows agents to continue acting without stopping for confirmation at every step. The updates make agents better at deciding when work is complete and progressing through multi-step tasks with less manual intervention.
- **Session persistence and collaboration**: Features like session sync, searchable coding history, gutter feedback, and session-based pull request generation turn chats into more durable engineering artifacts. Instead of being ephemeral conversations, agent sessions increasingly support review, traceability, and cross-machine continuity.

## How It Works

The central theme of these releases is that Copilot in VS Code is moving from a request-response assistant toward an environment for orchestrating agent work. The new features support four practical layers of that shift: **context gathering**, **task organization**, **execution autonomy**, and **operational control**.

At the **context gathering** layer, the integrated browser is now much more capable. Agentic browser tools are generally available and enabled by default, so the agent can interact with web pages directly inside VS Code. That includes navigating pages, inspecting visible content, capturing screenshots, and validating web app behavior. The browser itself also becomes more usable for humans, with favorites, history, search, and permissions for capabilities like camera or microphone. In practice, this means a developer can keep implementation, UI inspection, and validation in one workspace instead of switching between editor and external browser constantly.

A related improvement is **new ways to send browser context to the agent**. Rather than only describing a UI problem in text, a developer can attach a screenshot or an area screenshot to chat. This changes the quality of debugging and review interactions, especially for CSS issues, rendering bugs, and stateful flows that are easier to show than explain.

For teams working in containers, SSH sessions, or other remote setups, **remote workspace browsing** extends this capability by proxying HTTP(S) traffic over the remote connection. The important operational idea is that the browser context can stay aligned with the actual runtime environment. If your app is only reachable from the remote workspace, the integrated browser can still participate in the workflow.

At the **task organization** layer, the Agents window now supports more complex work patterns. You can run sessions side by side, which makes it easier to compare or monitor separate tasks simultaneously. You can also create multiple chats inside one session, letting you divide a large initiative into focused sub-conversations. For example:

- Chat 1: implement the feature
- Chat 2: add tests
- Chat 3: draft documentation
- Chat 4: review edge cases

This structure matters because agentic work is often non-linear. Instead of one long chat with mixed concerns, developers can create scoped workstreams while keeping the overall task grouped in one session. Session grouping and drag-and-drop organization reinforce that the Agents window is becoming a lightweight task board for AI-assisted development.

At the **execution autonomy** layer, Autopilot gets more reliable. The changelog emphasizes two improvements: better task completion detection and more independent progress. In other words, agents are improving at understanding whether a request is actually finished and at moving through intermediate steps without constant user steering. This is significant because weak completion logic is one of the main failure modes of autonomous coding agents; they either stop too early or require repeated nudges. These changes aim to reduce that friction.

At the **operational control** layer, cost visibility is expanded. Developers can now see total session cost rather than only per-request cost, inspect delegated subagent usage, and review additional usage via the Copilot status dashboard. This aligns with how real agent workflows consume resources: a seemingly simple task may involve multiple hidden or nested operations. Session-level accounting makes it easier to decide whether a workflow is efficient, and subagent-level visibility helps diagnose where expensive work is happening.

Model management is also pulled into the editor workflow. The Language Models editor can now be used to discover provider extensions, and Marketplace integration can open filtered results for model-contributing extensions. There is also a unified picker for adjusting capabilities such as context size and reasoning effort. The practical takeaway is that model selection is becoming a workflow decision inside VS Code, not something that requires external setup or fragmented configuration.

Several supporting features improve the broader engineering lifecycle:

- **Session sync and chronicle** allow chats to be synced to a GitHub account and searched across machines and workspaces.
- **Gutter feedback** allows review comments on agent-made changes directly in the editor.
- **Smarter PR creation** can generate pull request titles and descriptions from session context.
- **1M token context windows** are supported for compatible Anthropic and OpenAI models, enabling larger codebase and conversation scopes.
- **Model hover cards** make model capabilities and configuration more discoverable.
- **Official Ollama extension** separates Ollama support from a built-in provider for faster updates.
- **Managed settings**, **file-based managed settings**, and **MCP OAuth credential support** add enterprise control and deployment flexibility.
- **Extension auto-update delay** introduces a two-hour buffer before auto-installing newly published extension versions, which acts as a small safety window for teams.
- **Workspace Trust improvements** make it easier to inspect folders before fully trusting them.

Taken step by step, the design logic is clear:

1. Give agents richer environment context.
2. Let developers structure and parallelize agent work.
3. Increase autonomous follow-through where safe.
4. Surface costs, model choices, and governance controls.
5. Turn sessions into reusable, reviewable engineering artifacts.

This is why the release matters: it upgrades Copilot from a feature you invoke to a workflow surface you manage.

## Training Exercise

Build a small workflow experiment in VS Code to practice the new Copilot patterns.

### Goal
Use Copilot to implement, validate, and document a tiny web app change while splitting work into parallel tracks and observing how context, cost, and session organization affect the result.

### Prerequisites
- VS Code updated to a recent version in the 1.123-1.127 range or later
- GitHub Copilot enabled
- A small web project, for example a simple React, Vue, or static HTML app

### Exercise steps
1. **Open a small web app in VS Code**
   - Use an existing project or create a minimal one.
   - Start the local dev server.

2. **Create a feature request for the agent**
   Ask Copilot to make a visible UI change, such as:
   - add a dark-mode toggle
   - improve form validation messages
   - add a loading spinner to a button

3. **Split work into multiple chats in one session**
   In the Agents window, create separate chats for:
   - implementation
   - testing
   - documentation

   Example prompts:
   ```text
   Implementation chat: Add a dark-mode toggle to the header and persist the choice in localStorage.
   ```
   ```text
   Testing chat: Add tests for the dark-mode toggle behavior and persistence.
   ```
   ```text
   Documentation chat: Update the README with a short section describing the dark-mode feature.
   ```

4. **Use the integrated browser for validation**
   - Open the app in the integrated browser.
   - Capture a screenshot or area screenshot of the changed UI.
   - Add that screenshot to chat and ask Copilot to verify whether the result matches the requirement.

   Example prompt:
   ```text
   Compare this screenshot with the requested dark-mode behavior. Point out any mismatches and suggest a fix.
   ```

5. **Run a side-by-side session for review**
   Start a separate session focused only on code review.

   Example prompt:
   ```text
   Review the changes from the implementation session for accessibility, state persistence issues, and unnecessary complexity.
   ```

6. **Check session organization and completion quality**
   - Group related sessions.
   - Rename them clearly.
   - Observe whether Autopilot can finish each track with minimal nudging.

7. **Inspect cost visibility**
   - Review the total session cost if available.
   - Compare the implementation session against the review session.
   - Note whether screenshot-based validation or delegated work appears to increase usage.

8. **Generate a pull request draft**
   Use the session context to create a PR title and description. Evaluate whether the generated summary accurately reflects the technical change.

### Reflection questions
- Did multiple chats make the task easier to manage than one long conversation?
- Was screenshot context more effective than text-only UI descriptions?
- Which session consumed the most resources, and why?
- Did the review session identify issues the implementation session missed?
- Would you trust Autopilot for this task in a production repo?

### Optional extension
Repeat the same task with a different model provider or a different reasoning effort setting, then compare:
- quality of implementation
- amount of manual steering needed
- total session cost
- usefulness of PR summary output

## Test Yourself

<details><summary>What four workflow layers organize the Copilot improvements described in the lesson?</summary>

The lesson groups them into context gathering, task organization, execution autonomy, and operational control. Together they support richer inputs, parallel workstreams, more independent execution, and better oversight.

</details>

<details><summary>Why is session-level and subagent-level cost visibility more useful than per-request cost alone?</summary>

A single agent task may trigger long action chains or delegated work that is not obvious from the initial prompt. Broader accounting helps identify expensive sessions and determine where resource usage occurs.

</details>

<details><summary>How would you structure the lesson’s dark-mode exercise to test the new workflow?</summary>

Create separate chats for implementation, testing, and documentation, then use the integrated browser and a screenshot to validate the UI. Run a separate review session, compare session costs and completion quality, and generate a pull request draft from the session context.

</details>

## Further Reading

- [GitHub Changelog: GitHub Copilot in Visual Studio Code, June 2026 releases](https://github.blog/changelog/2026-07-08-github-copilot-in-visual-studio-code-june-2026-releases/)
- [Visual Studio Code Release Notes](https://code.visualstudio.com/updates)
- [GitHub Copilot Documentation](https://docs.github.com/copilot)
- [VS Code Workspace Trust](https://code.visualstudio.com/docs/editor/workspace-trust)
