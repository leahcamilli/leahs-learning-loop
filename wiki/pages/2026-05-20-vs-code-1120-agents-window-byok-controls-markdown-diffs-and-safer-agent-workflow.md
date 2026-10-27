---
title: "VS Code 1.120: Agents Window, BYOK Controls, Markdown Diffs, and Safer Agent Workflows"
source: "https://code.visualstudio.com/updates/v1_120"
date: "2026-05-20"
tags: [vscode, agents, copilot, markdown, extensions, developer-tools]
source_type: "web"
topics: [developer-tools, coding-agents, ai-agents]
kind: "news"
depth: 2
actionability: 1
---

## TL;DR

> VS Code 1.120 makes agent-driven development easier to orchestrate, inspect, and approve through a dedicated Agents window, accurate BYOK controls, compressed terminal output, command-risk badges, and rendered Markdown diffs. Together, these features reduce wasted model context and make AI-generated work safer and faster to review.

## Key Takeaways

1. Use the Stable-preview Agents window to create, revisit, compare, and switch among agent sessions across multiple projects.
2. Enable `chat.tools.compressOutput.enabled` to reduce token use from verbose `git diff`, `ls -l`, and `npm install` output while preserving notice that compression occurred.
3. Enable `chat.tools.riskAssessment.enabled` to triage proposed commands as safe, caution, or review carefully, but still review commands before approving them.
4. Monitor actual token counts and context-window fullness for BYOK models to control costs and avoid losing important conversation state.
5. Set reasoning effort for compatible BYOK models served through OpenAI-compatible endpoints to trade response quality against latency and API cost.
6. Associate `*.md` with `vscode.markdown.preview.editor` to review headings, lists, images, and structure as rendered Markdown instead of raw syntax.
7. Extension authors can use the proposed `customEditorDiffs` API for purpose-built comparisons and `workspace.getTextDiff(...)` to reuse VS Code’s built-in diff engine.

## Overview

Visual Studio Code 1.120 focuses on making agent-driven development more practical inside the editor. The release promotes the new Agents window to Stable preview, improves bring-your-own-key (BYOK) model controls, adds safety features around terminal command execution, and introduces Markdown-specific review improvements that better fit documentation-heavy workflows.

This matters to engineers who are using VS Code not just as a text editor, but as an orchestration environment for AI-assisted coding, multi-project task management, and extension-based customization. If you maintain internal tooling, rely on custom models, review docs in pull requests, or build extensions, this release changes how VS Code structures agent sessions, exposes model usage, and opens up new diff-related APIs.

## Key Concepts

- **Agents window**: The Agents window is a new VS Code window type designed specifically for agent-driven workflows across multiple projects. Instead of centering everything around one editor workspace, it provides a separate environment for creating, reviewing, and switching between agent sessions while preserving familiar VS Code capabilities like themes, keybindings, and extensions.
- **BYOK model observability**: Bring Your Own Key support now includes accurate token usage reporting for externally hosted models, not just built-in ones. This makes context-window consumption visible, which is important for cost control, prompt quality, and preventing the model from losing important conversation state.
- **Reasoning effort controls**: Some reasoning-capable models expose a configurable thinking or reasoning effort level. VS Code now forwards that setting for BYOK models served through OpenAI-compatible endpoints, allowing engineers to trade response quality against latency and API cost from the chat model picker.
- **Terminal output compression**: Large command output can waste context window budget when passed to an agent. VS Code can now compress common terminal outputs such as diffs, package manager logs, and directory listings before they are sent to the model, preserving useful signal while reducing token load.
- **Command risk assessment**: Before a terminal command is executed by an agent flow, VS Code can display a risk badge and explanation. The system classifies commands into safe, caution, or review carefully, helping engineers identify destructive, networked, or workspace-modifying operations before approving them.
- **Markdown-aware diff review**: Markdown diffs can now be rendered as preview output instead of raw syntax. This shifts review from line-oriented markup inspection to document-oriented change inspection, making edits to headings, lists, images, and structure easier to understand.
- **Diff extensibility APIs**: VS Code 1.120 adds proposed APIs for custom editor diffs and document diff access. These APIs let extensions render purpose-built diff views and reuse VS Code's built-in diff algorithm, which is especially useful when a textual source diff is less meaningful than a semantic or rendered comparison.

## How It Works

VS Code 1.120 is best understood as a set of coordinated improvements around **agentic development**, where the editor mediates between your codebase, terminal, model provider, and review workflow.

The biggest structural change is the **Agents window**. Instead of forcing all agent work into a normal editor window optimized for a single workspace and task, VS Code now offers a dedicated window type for running and reviewing agent sessions across projects. The design goal is orchestration: you can create sessions, revisit completed work, compare changes, sync upstream branch updates before an agent starts, and navigate among recent sessions. Several interaction details were refined in this release, including persisted session preferences, deterministic changes-panel actions, easier discard behavior, and automatic full-change visibility for completed sessions.

This new window also has an **extension compatibility model**. Static contributions such as themes, languages, grammars, and keybindings activate automatically. Other extensions can be explicitly enabled using the `extensions.supportAgentsWindow` setting:

```json
"extensions.supportAgentsWindow": {
  "myextension.id": true
}
```

That means the Agents window is not a completely separate product surface; it reuses the VS Code extension ecosystem with controlled opt-in for behaviors that may not yet be safe or meaningful in an agent-oriented environment.

For teams using external model providers, **BYOK support** becomes more operationally useful in 1.120. Previously, token accounting in the chat UI did not accurately represent externally configured models, so context usage always appeared as zero. Now the chat context window indicator reports actual token counts and fullness percentages for BYOK models. This is important because context budget is the resource that agents burn through fastest when they ingest code, terminal output, diffs, and chat history.

The release also standardizes **thinking effort** controls for reasoning models served through OpenAI-compatible endpoints. From the model picker, you can choose a reasoning effort level, and VS Code forwards that value on every request. In practical terms, this turns the model picker into an execution policy surface: you choose not just *which model* to call, but *how hard it should think* and therefore how much time and money to spend.

The model picker itself is now grouped by **provider**, which solves a real usability problem when multiple vendors expose similarly named models. Recent models now show provider metadata next to the name, and `/models` offers a shortcut for selecting one directly from chat.

The next set of features focuses on **agent safety and context efficiency** in terminal-integrated workflows.

When `chat.tools.compressOutput.enabled` is turned on, VS Code post-processes terminal output before handing it to the model. The heuristics are command-specific:

- `git diff`: collapse large unchanged hunks and remove noisy artifacts such as lockfile or snapshot diffs.
- `ls -l`: reduce output to entry names instead of verbose metadata.
- `npm install`: strip progress bars, deprecation spam, and audit summaries.

A banner is prepended so the model knows compression occurred and can request raw output if needed. This is a notable design choice: compression is not hidden from the model, which preserves transparency and lets the agent reason about missing detail.

When `chat.tools.riskAssessment.enabled` is enabled, terminal confirmations add an AI-generated **risk badge**. The classification is lightweight but useful:

- **Safe**: mostly read-only commands.
- **Caution**: commands that modify files, install dependencies, or communicate over the network.
- **Review carefully**: destructive or hard-to-undo actions like deleting files outside the workspace or force-pushing.

This does not replace review, but it acts as a fast triage layer in agent workflows where many commands may be proposed in sequence.

For plan-first agent interactions, VS Code improves the **inline plan control** used with Claude agents and Copilot CLI plan mode. Rather than opening a separate editor tab to revise a generated plan, the user can now edit it inline, give feedback with clearer state indicators, and disable this inline behavior if they prefer a regular text editor. This keeps the review loop close to the execution UI instead of scattering planning state across tabs.

On the language tooling side, the standout feature is **Markdown preview for diffs**. Normally, Markdown diffs are reviewed as text, which forces the reviewer to interpret syntax changes mentally. In 1.120, you can reopen Markdown diffs using the rendered Markdown preview, either inline or side by side. That makes agent-generated documentation changes, PR docs edits, and content refactors significantly easier to evaluate.

You can opt into Markdown preview diffs by default with:

```json
"workbench.diffEditorAssociations": {
  "*.md": "vscode.markdown.preview.editor"
}
```

Markdown also gained smaller quality-of-life changes: path completion and validation now understand HTML `id` attributes embedded in Markdown documents, and smart selection can expand from a table cell to a row and then to the entire table. In parallel, two older preview behaviors are now disabled by default because they were considered confusing or less useful in modern workflows.

Finally, this release includes **proposed extension APIs** that explain how some of the new built-in functionality is implemented and how third-party extensions can follow suit.

The `customEditorDiffs` proposed API allows custom editors to implement purpose-built diff UIs through methods such as:

```ts
resolveCustomEditorInlineDiff(documents, webviewPanel, token)
resolveCustomEditorSideBySideDiff(documents, webviewPanels, token)
```

This is the API family that powers the new Markdown preview diff experience. It means extensions are no longer constrained to showing a raw textual diff if a richer rendered comparison is more appropriate.

Related to that, custom editors can now set separate priorities for normal editing, diffing, and merging using `priority`, `diffEditorPriority`, and `mergeEditorPriority`. That gives extension authors fine-grained control over when their editor should take over.

The proposed `documentDiff` API exposes the built-in diff engine through `workspace.getTextDiff(...)`, returning a stream of line-level changes plus summary metadata. This helps extension authors avoid shipping their own inconsistent diff algorithm and instead reuse the same logic VS Code uses internally.

Overall, the mechanics of 1.120 revolve around a consistent architectural theme: **agent interactions should be more observable, safer, easier to review, and more extensible**.

## Training Exercise

Set up a small VS Code 1.120 workflow that exercises the release's agent, Markdown, and safety features.

1. **Create a test workspace**
   - Make a folder with:
     - `README.md`
     - `CHANGELOG.md`
     - a small JavaScript or TypeScript file
   - Initialize Git.

```bash
mkdir vscode-120-lab
cd vscode-120-lab
git init
printf "# Demo Project\n\n## Install\nRun setup.\n" > README.md
printf "console.log('hello');\n" > app.js
git add .
git commit -m "initial commit"
```

2. **Enable the new settings**
   Open `settings.json` and add:

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

3. **Create a Markdown diff worth reviewing**
   - Edit `README.md` by adding a new section, changing a heading, and inserting a list or image link.
   - Open Source Control and inspect the diff.
   - Use **Reopen Editor With...** if needed to confirm the rendered Markdown diff experience.
   - Compare how much easier it is to review semantic document changes in preview mode than in raw text mode.

4. **Exercise Markdown link intelligence**
   - Add an HTML anchor to `README.md`:

```md
<div id="install-guide"></div>

## Installation
Follow the steps.

See [Install notes](#install-guide).
```

   - Verify that link completion and validation recognize the HTML `id` target.

5. **Test terminal-output compression behavior**
   - Generate verbose terminal output, such as:

```bash
ls -l
npm install
```

   - If you use a chat/agent session that consumes terminal output, inspect whether VS Code indicates that the output was compressed before being sent to the model.
   - Note which parts of the output are likely preserved versus removed.

6. **Test command risk assessment**
   - Compare how you would classify these commands:

```bash
cat README.md
git status
npm install
git push --force
rm -rf ../some-other-folder
```

   - In an agent or command confirmation flow, verify that the displayed badge aligns with the expected level: safe, caution, or review carefully.

7. **Explore the model picker if you use BYOK**
   - Add or use an existing BYOK provider configuration.
   - Open Chat, inspect model grouping by provider, and look for the context window token display.
   - If your provider supports it, change the reasoning or thinking effort and observe how the option is surfaced.

8. **Optional extension-author task**
   - If you build VS Code extensions, review the proposed APIs mentioned in the release notes.
   - Sketch how your custom editor could benefit from `customEditorDiffs` or `workspace.getTextDiff(...)`.

**Goal:** by the end, you should be able to explain which 1.120 features improve agent orchestration, which reduce model waste, which improve review ergonomics, and which open new possibilities for extension developers.

## Test Yourself

<details><summary>Which VS Code 1.120 features reduce context-window waste and improve BYOK observability?</summary>

Terminal-output compression removes predictable noise from supported command output before it reaches the model, while explicitly telling the model that compression occurred. BYOK token reporting shows actual token consumption and context fullness for externally configured models.

</details>

<details><summary>How does command risk assessment help, and what limitation does the lesson emphasize?</summary>

It labels proposed terminal commands as safe, caution, or review carefully based on behaviors such as file modification, network access, or destructive effects. The lesson says this is a fast triage layer, not a replacement for human review.

</details>

<details><summary>How does VS Code 1.120 improve diff review for users and extension authors?</summary>

Users can inspect Markdown changes as rendered inline or side-by-side previews, making document structure easier to evaluate. Extension authors can build custom diff interfaces with `customEditorDiffs` and access VS Code’s diff algorithm through `workspace.getTextDiff(...)`.

</details>

## Further Reading

- [Visual Studio Code 1.120 Release Notes](https://code.visualstudio.com/updates/v1_120)
- [VS Code Copilot and AI Features Documentation](https://code.visualstudio.com/docs/copilot/overview)
- [VS Code Markdown Extension Documentation](https://code.visualstudio.com/api/extension-guides/markdown-extension)
- [VS Code Custom Editors API](https://code.visualstudio.com/api/extension-guides/custom-editors)
- [VS Code Extension API Overview](https://code.visualstudio.com/api)
