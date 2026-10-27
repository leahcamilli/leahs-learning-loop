---
title: "VS Code 1.129: Agent Host, Agents Window Workflow, and Modern UI Preview"
source: "https://code.visualstudio.com/updates/v1_129"
date: "2026-07-16"
tags: [vscode, agents, copilot, developer-tools, editor-ui]
source_type: "web"
topics: [coding-agents, developer-tools, ai-agents, github-copilot]
kind: "news"
depth: 2
actionability: 2
---

## TL;DR

> VS Code 1.129 moves supported AI sessions into a dedicated agent host, enabling resumable, multi-window workflows and controlled coordination across sessions. Its docked review panel, worktree isolation, command execution, and skills migration make agent-assisted development more integrated and portable.

## Key Takeaways

1. Enable `chat.agentHost.enabled` and select a host-backed harness to use capabilities such as multi-window session access, cross-session coordination, `!` command execution, GitHub Enterprise authentication, and BYOK support in the Agents window.
2. Enable `sessions.layout.singlePaneDetailPanel` to review generated files and diffs in persistent editor-style tabs with inline or side-by-side views.
3. Use `New Worktree` when an agent task needs a separate filesystem context so its changes remain isolated until review and merge.
4. Prefix a message with `!` in an agent-host session—for example, `!npm test`—to execute it as a terminal command instead of sending a natural-language request.
5. Migrate legacy `*.prompt.md` commands to skills with `chat.customizations.promptMigration.enabled` when customization must work across agent-host harnesses rather than only the Local harness.
6. Agent-host sessions can list, inspect, create, and message other sessions, but VS Code requires confirmation for cross-session messages and applies restrictions and send limits.
7. Custom editors no longer handle diff and merge views by default; extension authors can use `customEditorPriority` to set separate priorities for text, diff, and merge editors.

## Overview

This matters to engineers who use VS Code as both an IDE and an AI-assisted workspace. The changes are not just cosmetic: they alter how agent sessions are isolated, rendered, resumed, and coordinated across windows and tasks. If you rely on Copilot, Claude, Codex, custom prompts/skills, custom editors, or Git worktree-based task isolation, this release introduces architectural and workflow changes worth understanding.

## Key Concepts

- **Agent host**: The agent host is a dedicated process that runs agent harnesses such as Copilot, Claude, and Codex using the Agent Host Protocol (AHP). Moving sessions into their own process allows the same session to be connected to from multiple VS Code windows and creates a clearer execution boundary between the workbench UI and agent runtime.
- **Agent harnesses**: A harness is the concrete agent runtime or integration selected by the user, such as Copilot on the agent host. Different features may depend on both the selected harness and whether it runs on the new host architecture, which is why some capabilities in 1.129 are only available when the harness uses the agent host.
- **Docked editor panel in the Agents window**: The experimental single-pane detail panel merges file review and chat-adjacent details into a docked editor-like surface with tabs. This makes reviewing generated files and diffs behave more like normal editor work, including tab management, diff toggling, and restored session state.
- **Cross-session orchestration**: Agent-host sessions can now enumerate, inspect, create, and message other sessions and chats. This enables delegation patterns such as spinning up a sub-task in a separate session while keeping the current conversation focused, with built-in user confirmation and fan-out limits for safety.
- **Chat command execution with !**: Prefixing a chat message with ! causes the contents to be run as a terminal command. This shortens the loop between discussing an action with an agent and executing it, especially in agent-host sessions where chat and environment manipulation are more tightly integrated.
- **Prompt files to skills migration**: Legacy *.prompt.md files define custom slash commands in the Local agent harness, while agent-host-based harnesses express similar behavior as skills. VS Code 1.129 adds an experimental migration path so teams can move toward a harness-agnostic customization model.
- **Modern UI preview**: The modern UI preview is an experimental update to the workbench appearance, enabled by a feature flag. While largely visual, it signals ongoing work on the shell around editor, chat, and agent workflows, particularly as the Agents window becomes a first-class surface.
- **Custom editor diff and merge priorities**: Custom editors now opt out of diff and merge editors by default, allowing built-in text diffs and merge views to remain the standard fallback. A proposed API adds separate priorities for text, diff, and merge handling so extension authors can precisely control when their editor should be selected.

## How It Works

VS Code 1.129’s central architectural shift is the **agent host**. Instead of treating an agent session as tightly bound to a single window, the session is run in a dedicated process via the Agent Host Protocol. The workbench window becomes a client that connects to and renders that session. That separation enables multi-window attachment to the same session and creates a path for consistent agent behavior across VS Code, Copilot CLI, and other GitHub Copilot surfaces because the Copilot harness is powered by the Copilot SDK.

From a workflow perspective, the new model looks like this:

1. You enable `chat.agentHost.enabled`.
2. You select a harness, such as Copilot, from the harness dropdown.
3. The session runs in the host process rather than being purely window-local.
4. One or more VS Code windows can render and interact with that session.
5. Session-aware tools can inspect or create additional sessions and chats.

This design explains why several release features are explicitly limited to agent-host sessions. Cross-session messaging, `!` terminal command execution, GitHub Enterprise authentication for Copilot in the host, and BYOK support in the Agents window are all layered on top of that dedicated runtime.

The **Agents window** also evolves from a chat-plus-side-panel layout toward something closer to a full editor experience. With `sessions.layout.singlePaneDetailPanel` enabled, the detail area and editor become a shared docked pane with tabs. Practically, this means generated files and diffs no longer feel like second-class views; they behave like editor tabs next to your conversation. The release specifically calls out:

- opening files and diffs directly in the docked panel
- creating new tabs from the same strip
- toggling inline vs side-by-side diffs
- expanding or collapsing all changed files
- exposing follow-up actions like **Create Pull Request** from the tab title
- persisting panel width, active editor, open editors, and collapsed state across reloads and session switches

That persistence is important. It turns agent review into a resumable workspace rather than a transient chat artifact.

A second major capability is **session management across agents**. An agent-host-backed session can now use tools to list other sessions, read recent conversation context from another session, create a new session or a new chat within an existing session, and send a message to work it. This enables controlled delegation. For example, a primary chat can stay focused on feature design while a separate session handles tests or documentation in parallel. VS Code keeps this from becoming chaotic by excluding archived sessions unless requested, requiring confirmation before sending messages to another session, preventing an agent from messaging its own chat, and capping bursts of sends.

The release also refines **session creation ergonomics**. The new-session flow now remembers prior defaults such as selected mode and approval settings, reducing repetitive setup. Isolation choice is simplified into a `New Worktree` checkbox rather than a folder/worktree dropdown. Git worktree isolation matters because it provides a separate filesystem context for agent changes until you choose to review and merge them.

On the chat execution side, `!` command support introduces a tighter integration between conversational input and shell actions. In an agent-host session, sending something like `!npm test` routes the content as a terminal command instead of ordinary natural-language chat. This makes command execution explicit and fast without having to jump into the terminal manually.

Customization is also shifting. Historically, `*.prompt.md` files described custom slash commands, but that mechanism is limited to the Local harness. Agent-host harnesses use **skills** instead. The new prompt migration flow, gated by `chat.customizations.promptMigration.enabled`, scans workspace and user prompt locations, lets you select migratable files, and creates corresponding skills. This is a compatibility and portability move: teams that want the same customization behavior across Copilot, Claude, and other host-based harnesses should standardize on skills.

Outside AI workflows, the release contains a few editor-platform changes. The editor toolbar now exposes **Reopen Editor With**, making it easier to switch between alternative editors for a file or diff without the Command Palette. That pairs with a platform change to **custom editors**: they no longer automatically participate in diff and merge editors by default. Extension authors can use the proposed `customEditorPriority` API to set distinct priorities for normal file opening, diff views, and merge views:

```json
"priority": {
  "textEditor": "default",
  "diffEditor": "option",
  "mergeEditor": "never"
}
```

This means a custom editor can remain the preferred view for a file while built-in text diff and merge experiences stay available and predictable. If a text diff editor cannot handle binary content, VS Code still falls back to a compatible custom diff editor.

Finally, the **modern UI preview** is an experimental workbench appearance refresh behind `workbench.experimental.modernUI`. It does not change the underlying editor model, but it signals that the shell around editors, tabs, agents, and review surfaces is being updated in parallel with the new agent-centric architecture.

## Training Exercise

Exercise: Enable the new agent-host workflow and compare it to classic window-local behavior.

### Goal
Explore how VS Code 1.129 changes agent execution, review, and task delegation.

### Prerequisites
- VS Code 1.129 or newer
- Access to an agent-capable setup such as Copilot
- A sample Git repository with a few files

### Steps
1. **Enable the agent host**
   Open Settings and enable:
   - `chat.agentHost.enabled`

   If available in your environment, also select a host-backed harness such as Copilot from the harness dropdown in chat or the Agents window.

2. **Enable the experimental docked editor panel**
   Enable:
   - `sessions.layout.singlePaneDetailPanel`

   Reload the window after changing it.

3. **Create an isolated session**
   Open the Agents window and start a new session.
   - Leave folder isolation selected for the first run.
   - Note whether your last-used approvals and mode are remembered.

4. **Ask the agent to make a concrete code change**
   Use a prompt such as:
   ```text
   Add a small utility function that validates email addresses, include unit tests, and show me the diff.
   ```

5. **Review the output in the docked editor panel**
   In the new editor panel:
   - open the generated file
   - open the diff
   - switch between inline and side-by-side diff views
   - collapse and expand changed files
   - switch tabs and confirm the layout feels like the normal editor

6. **Test session persistence**
   Reload the VS Code window.
   Verify that:
   - the side pane width is restored
   - your open editor tabs are restored
   - the active editor is restored
   - per-file collapsed state is restored

7. **Run a command from chat**
   In the same session, execute a terminal command using the `!` prefix:
   ```text
   !npm test
   ```
   Or use a repository-appropriate command such as `!pytest` or `!git status`.

   Observe that the message is treated as a shell command rather than a natural-language request.

8. **Create a second session using a worktree**
   Start another session and enable `New Worktree`.
   Ask it to work on a different task, for example:
   ```text
   Refactor the validation helper to support reusable regex patterns and update docs.
   ```

9. **Compare isolation strategies**
   Inspect how the worktree-backed session keeps changes separate from the original folder-isolated session. Record what is easier to review or merge.

10. **Optional: explore customization migration**
   If you have `*.prompt.md` files in `.github/prompts/`, enable:
   - `chat.customizations.promptMigration.enabled`

   Open AI Customizations and inspect the migration flow to skills.

### What to write down
- Which features only worked after enabling the agent host?
- Did the docked editor panel improve diff review compared to side-pane review?
- When would you prefer a new worktree over folder isolation?
- How does `!` command execution change your chat-to-terminal workflow?
- If you use custom prompts, what would be required to migrate them to skills?

## Test Yourself

<details><summary>Why does the agent host enable workflows that window-local sessions cannot provide?</summary>

It runs the agent harness in a dedicated process and lets VS Code windows act as clients. This separation allows the same session to appear in multiple windows and supports session-aware coordination features.

</details>

<details><summary>When should an engineer choose `New Worktree` for an agent session?</summary>

Use it when a task's filesystem changes should remain separate from the current working folder until they are reviewed and merged. This is especially useful for parallel or potentially disruptive work.

</details>

<details><summary>Why should teams migrate `*.prompt.md` files to skills?</summary>

Legacy prompt files define slash commands only for the Local harness. Skills provide a more portable customization model for agent-host-based harnesses such as Copilot or Claude.

</details>

## Further Reading

- [Visual Studio Code Release Notes](https://code.visualstudio.com/updates)
- [Visual Studio Code AI Documentation](https://code.visualstudio.com/docs/copilot/overview)
- [Git Worktree Documentation](https://git-scm.com/docs/git-worktree)
- [VS Code Custom Editor API](https://code.visualstudio.com/api/extension-guides/custom-editors)
