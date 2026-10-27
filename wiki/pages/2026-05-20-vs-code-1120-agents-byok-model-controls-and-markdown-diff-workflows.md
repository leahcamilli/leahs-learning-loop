---
title: "VS Code 1.120: Agents, BYOK Model Controls, and Markdown Diff Workflows"
source: "https://code.visualstudio.com/updates/v1_120"
date: "2026-05-20"
tags: [vscode, agents, copilot, markdown, extensions, llm]
source_type: "web"
topics: [developer-tools, coding-agents, ai-agents, github-copilot]
kind: "news"
depth: 3
actionability: 1
---

## TL;DR

> VS Code 1.120 makes AI-assisted development more manageable by adding a dedicated Agents window, visible BYOK token and reasoning controls, safer terminal workflows, and rendered Markdown diffs. These features help developers coordinate agents, control model cost and context, and review changes more effectively.

## Key Takeaways

1. Use the Agents window to run, switch between, and review multiple agent sessions across projects in a dedicated workspace.
2. Enable `chat.tools.compressOutput.enabled` to reduce token-heavy noise from commands such as `git diff`, `ls -l`, and `npm install` before output reaches the model.
3. Enable `chat.tools.riskAssessment.enabled` to add Safe, Caution, or Review carefully classifications and short explanations to terminal command confirmations.
4. Monitor actual token usage for BYOK models and adjust thinking effort on reasoning models served through OpenAI-compatible endpoints to balance quality, latency, and cost.
5. Associate `*.md` diffs with `vscode.markdown.preview.editor` to review headings, tables, images, and document structure as rendered content.
6. Explicitly enable non-static extensions in the Agents window with `extensions.supportAgentsWindow`, keyed by extension ID.
7. Extension authors can explore the proposed `customEditorDiffs` and `documentDiff` APIs to build semantic comparison interfaces without recreating VS Code's diff engine.

## Overview

Visual Studio Code 1.120 is a release centered on agent-driven development, better large-language-model controls, and improved documentation review workflows. The headline feature is the new Agents window in Stable preview, which gives developers a workspace specifically designed for running and reviewing multiple agent sessions across projects rather than treating AI assistance as a single chat sidebar inside one editor window.

This release matters to engineers who are adopting AI-assisted coding in real repositories, especially teams juggling multiple codebases, Bring Your Own Key (BYOK) model providers, and documentation-heavy review processes. It also matters to extension authors, because VS Code is expanding the diff and custom editor APIs in ways that support richer review experiences such as rendered Markdown diffs.

## Key Concepts

- **Agents window**: The Agents window is a new VS Code window type optimized for agent-first workflows across multiple projects and sessions. Instead of embedding all agent activity inside the main editor layout, it provides a dedicated environment for exploring tasks, reviewing edits, switching sessions, and configuring agent behavior independently.
- **BYOK model management**: Bring Your Own Key support lets developers connect models from providers like OpenAI, Anthropic, xAI, OpenRouter, or custom OpenAI-compatible endpoints using their own billing and hosting. In 1.120, VS Code improves practical controls for these models by showing real token usage and exposing reasoning-model thinking effort directly in the UI.
- **Context window optimization**: Agent quality and cost are constrained by the model context window, which is consumed by prompts, code, terminal output, and chat history. VS Code now includes output compression for common terminal commands so noisy command output does not crowd out more relevant context.
- **Command risk assessment**: Before an agent executes terminal commands, VS Code can classify them as Safe, Caution, or Review carefully and provide a short AI-generated explanation. This gives developers a lightweight safety review layer, especially for commands that mutate the workspace, send network traffic, or perform destructive operations.
- **Rendered Markdown diffs**: VS Code can now preview Markdown diffs as rendered content rather than raw Markdown syntax. This is particularly useful for reviewing docs changes, agent-generated README updates, or pull request descriptions where semantic layout matters more than punctuation-level source changes.
- **Proposed diff APIs for extensions**: The release introduces proposed APIs such as customEditorDiffs and documentDiff, allowing extensions to render their own diff UIs or reuse VS Code's built-in diff engine. These APIs enable custom editors to provide much better comparison experiences for formats where raw text diffs are hard to interpret.

## How It Works

VS Code 1.120 extends the editor in three major directions: agent orchestration, model/runtime controls, and richer review surfaces.

First, the **Agents window** changes the interaction model for AI-assisted development. Instead of treating AI as a single task inside the current workspace, VS Code adds a companion window specialized for agent sessions. That window keeps track of session state and now persists preferences like selected harness and isolation mode across new sessions. It also improves the edit-review loop with deterministic Changes panel interactions, direct discard support, and a Files panel sync action that pulls upstream changes from the base branch before the agent begins work. Once a session is complete, the UI defaults to showing the full set of edits so the developer can review the complete patch quickly.

Second, the release tightens **extensibility around the Agents window**. Static extension contributions such as themes, grammars, languages, and keybindings activate automatically. For other extensions, support is opt-in through the `extensions.supportAgentsWindow` setting, keyed by extension ID:

```json
"extensions.supportAgentsWindow": {
  "myextension.id": true
}
```

This tells you something important about the architecture: the Agents window is not just a visual mode, it is a distinct execution surface with its own extension activation expectations. VS Code currently enables low-risk extension categories automatically while preserving explicit control for more complex extensions whose behavior in multi-project agent workflows may be ambiguous.

The release also improves **agent plugin discovery**. Plugins installed with the GitHub Copilot CLI are now discovered automatically by VS Code, eliminating the earlier need to install them separately or manually point VS Code at plugin paths. In practice, this reduces duplication between terminal-based and editor-based agent tooling.

On the model side, VS Code strengthens **BYOK support**. Previously, token accounting in the Chat view only worked properly for built-in models. In 1.120, the context window indicator now displays actual token usage and percentage full for BYOK models as well. This is operationally important because engineers can now see whether a conversation is near context exhaustion and decide whether to summarize, reset, or change tactics.

For **reasoning models**, the model picker now exposes thinking effort for BYOK providers served through OpenAI-compatible endpoints. That setting is forwarded on each request, letting the user choose a point on the quality/latency/cost curve. The model picker is also grouped by provider and supports search, which matters when multiple providers expose similarly named models. The `/models` shortcut in chat is a quick way to jump into this selection flow.

A related optimization is **terminal output compression**. Large outputs from commands such as `git diff`, `ls -l`, and `npm install` are often low-value but high-token. When `chat.tools.compressOutput.enabled` is turned on, VS Code rewrites that output before sending it to the model. Examples include collapsing unchanged diff hunks, removing lockfile or snapshot noise, reducing `ls -l` to filenames, and stripping progress bars or audit chatter from install logs. VS Code prepends a banner explaining which compression filters were applied, so the model still has provenance and can request raw output if needed. Conceptually, this is a pre-transmission normalization step in the agent tool pipeline.

Another safety mechanism is **terminal command risk assessment**. With `chat.tools.riskAssessment.enabled`, command confirmations are enriched with an AI-generated badge and one-sentence summary. Internally, the feature acts as a classification and explanation layer before execution. It does not replace user review, but it shortens the time needed to recognize dangerous actions such as force pushes or deletions outside the workspace.

The release also improves **plan mode** for Claude and Copilot CLI. When the agent proposes a plan, VS Code now lets you edit that plan inline rather than bouncing out to a separate editor tab. This keeps the feedback loop close to execution, which is especially useful for steering multi-step coding tasks. The feature can be disabled if a traditional editor-tab workflow is preferred.

For documentation and content review, 1.120 adds **Markdown preview for diffs**. When opening a Markdown diff from Source Control or any diff editor, the user can reopen it with the Markdown preview editor. This supports both side-by-side and inline modes. You can also make it the default for `*.md` files:

```json
"workbench.diffEditorAssociations": {
  "*.md": "vscode.markdown.preview.editor"
}
```

This is especially helpful when reviewing agent-authored docs because you can inspect headings, lists, images, and section structure directly rather than mentally interpreting punctuation-heavy source changes.

Markdown editing itself also gets smaller quality-of-life improvements. Path completion and link validation now understand HTML `id` attributes inside Markdown files, which matters for documents that mix Markdown with embedded HTML anchors. Smart select now works on Markdown tables, allowing selection growth from cell to row to full table.

Finally, the release contains meaningful **extension API evolution**. The `customEditorDiffs` proposed API lets custom editors render their own inline or side-by-side diff interfaces through methods like `resolveCustomEditorInlineDiff` and `resolveCustomEditorSideBySideDiff`. Alongside that, custom editors can now specify different priorities for standard editing, diffing, and merging with `priority`, `diffEditorPriority`, and `mergeEditorPriority`. The new `documentDiff` proposed API exposes VS Code's built-in text diff engine to extensions via `workspace.getTextDiff(...)`, returning a stream of changes and a completion object with summary metadata. Together, these APIs signal a broader architectural direction: VS Code wants custom editors to integrate with native compare workflows without each extension having to reinvent diff logic.

In short, VS Code 1.120 is not just a feature bundle. It shows a pattern: agent workflows are becoming first-class, model economics are becoming visible and tunable, and review surfaces are becoming more semantic and extension-friendly.

## Training Exercise

Set up a small workflow that exercises the three most practical parts of this release: agent controls, model context awareness, and Markdown diffs.

1. **Enable the preview features** in your VS Code `settings.json`:

```json
{
  "chat.tools.compressOutput.enabled": true,
  "chat.tools.riskAssessment.enabled": true,
  "chat.planWidget.inlineEditor.enabled": true,
  "workbench.diffEditorAssociations": {
    "*.md": "vscode.markdown.preview.editor"
  }
}
```

2. **Create a test repository** with both code and docs:
   - Initialize a Git repo.
   - Add a `README.md` with headings, lists, a table, and an embedded HTML anchor.
   - Add a small script file and make one or two changes on a new branch.

3. **Exercise Markdown review**:
   - Edit `README.md` by adding a section, changing a table row, and inserting a link to an HTML anchor such as `<div id="install-guide"></div>`.
   - Open the diff from Source Control.
   - Use `Reopen Editor With...` and choose the Markdown preview diff editor.
   - Compare how quickly you can understand the rendered diff versus the raw text diff.

4. **Exercise context compression**:
   - In the integrated terminal, run a command with noisy output such as:

```bash
npm install
```

   - Then ask an agent or chat tool to summarize what happened in the terminal output.
   - Observe whether the model receives a compressed summary rather than the full raw output.
   - Repeat with a large `git diff` and compare the quality of the model response.

5. **Exercise command safety**:
   - Ask an agent to propose terminal commands for a task that includes a harmless read command and a mutating command, such as checking Git status and deleting a generated directory.
   - Review the risk badges in the confirmation flow.
   - Note which commands are labeled Safe, Caution, or Review carefully.

6. **Exercise BYOK model controls** if you have access to an external provider:
   - Configure a BYOK model in VS Code.
   - Open Chat and verify that the token usage indicator is no longer stuck at zero.
   - Switch between providers in the model picker and change the thinking effort on a reasoning-capable model.
   - Ask the same question at two effort levels and compare latency and response quality.

7. **Reflection task**:
   - Write down answers to these questions:
     - Which terminal outputs should always be compressed in your workflow?
     - Which command categories deserve mandatory human review?
     - Should Markdown preview diffs be the default in your team for docs-heavy repos?
     - Would your current extensions need explicit enablement in the Agents window?

If you want an extra challenge, create a tiny extension prototype and review the proposed `customEditorDiffs` and `documentDiff` APIs. Sketch how you would render a semantic diff for a structured file type instead of falling back to raw text.

## Test Yourself

<details><summary>Why is terminal output compression useful in agent workflows?</summary>

Terminal output can consume a large portion of a model's context window without adding proportional value. Compression removes noise such as unchanged diff hunks, progress bars, lockfile changes, and audit chatter while preserving provenance and access to raw output when needed.

</details>

<details><summary>What practical controls does VS Code 1.120 add for BYOK models?</summary>

It shows actual token usage and context-window percentage for BYOK models. For reasoning models on OpenAI-compatible endpoints, it also exposes thinking effort so users can tune the tradeoff among response quality, latency, and cost.

</details>

<details><summary>How do rendered Markdown diffs improve documentation review?</summary>

They show semantic structure—such as headings, lists, tables, images, and sections—instead of requiring reviewers to interpret raw Markdown punctuation. They support side-by-side and inline modes and can be configured as the default diff editor for `*.md` files.

</details>

## Further Reading

- [Visual Studio Code 1.120 Release Notes](https://code.visualstudio.com/updates/v1_120)
- [VS Code Agents Documentation](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode)
- [VS Code Markdown Extension Documentation](https://code.visualstudio.com/docs/languages/markdown)
- [VS Code Extension API](https://code.visualstudio.com/api)
- [GitHub Pull Requests and Issues Extension](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github)
