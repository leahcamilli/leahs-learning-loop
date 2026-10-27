---
title: "VS Code 1.132: Practical Agent, Dictation, and Markdown Workflows"
source: "https://code.visualstudio.com/updates/v1_132"
date: "2026-08-05"
tags: [editor, developer-tools, ai-agents, markdown, voice-input]
source_type: "web"
source_fingerprint: "e429dcbc68"
source_characters: 12033
topics: [developer-tools, coding-agents, github-copilot]
kind: "news"
depth: 2
actionability: 2
---

## TL;DR

> VS Code 1.132 brings agent sessions, editing, browser feedback, dictation, and document review into one connected workflow, reducing context switching during long-running tasks. The release notes also caution that rollout is gradual and hybrid Markdown diffs remain experimental.

## Key Takeaways

1. Run Copilot, Claude, and Codex harnesses in the dedicated agent host, which the release notes say allows the same agent session to connect across multiple VS Code windows.
2. Use the Agents window and live status pills to start and monitor concurrent sessions, including file changes, Markdown previews, subagent activity, and integrated browser work.
3. Open a contextual side chat with /btw to ask a question without interrupting the primary agent turn; side chats share its context and prompt cache.
4. Use on-device dictation in chat, editors, and the terminal; Nemotron 3.5 supports multilingual input, while terminal dictation applies shell-aware cleanup.
5. Add comments to specific elements in the integrated browser to give agents precise UI feedback instead of describing an entire page.
6. Review and edit Markdown changes in the hybrid Markdown diff editor, but treat the capability as experimental and potentially subject to change.

## Overview

This lesson explains the major workflow changes introduced in Visual Studio Code 1.132, released on August 5, 2026. The release centers on agent-driven work: a separate agent host process, an Agents window for monitoring sessions, side chats that preserve context, multilingual on-device dictation, element-level comments in the integrated browser, and experimental Markdown diffs in the hybrid Markdown editor. A practical takeaway is that VS Code is treating chat, editing, browser feedback, terminal use, and document review as one connected loop rather than separate tools. Evidence is strong for the listed features because they are explicitly described in the release notes, but the notes are brief on implementation details and do not fully specify edge cases or performance behavior.

## Key Concepts

- **Agent host**: VS Code can run agent harnesses such as Copilot, Claude, and Codex in a dedicated process called the agent host. The release notes say this enables connecting to the same agent session from multiple VS Code windows and aligns Copilot behavior with other Copilot products through the Copilot SDK.
- **Agents window and live session tracking**: The Agents window provides a dedicated place to start and monitor multiple agent sessions. Live status pills above chat input expose session activity such as file changes, Markdown previews, subagent work, and integrated browser activity, which helps users follow long-running agent tasks.
- **Side chats with /btw**: Typing /btw opens a side chat so you can ask contextual questions without interrupting the current agent turn. The release notes state that side chats share the context and prompt cache of the primary chat, making them useful for clarification while preserving main-task continuity.
- **Multilingual on-device dictation**: Dictation now uses the multilingual Nemotron 3.5 model by default and keeps audio on device. It follows the agents.voice.language setting, can use automatic language selection, and supports extra cleanup instructions from ~/.copilot/dictation.md and .github/dictation.md in trusted workspaces.
- **Element-level browser feedback**: The integrated browser now lets you select page elements and attach comments before sending feedback to chat. This matters because feedback can target specific UI elements instead of describing a whole page vaguely, which should improve the precision of agent-guided UI iteration.
- **Hybrid Markdown diffs**: Markdown diffs can open in the hybrid Markdown editor, where the modified document stays editable while diff markers show additions, changes, and deletions. The release notes mark this feature as experimental, so it should be treated as promising but not yet fully settled.

## How It Works

A practical workflow in VS Code 1.132 looks like this: start an agent session, monitor its work from the Agents window, and use the live status pills to inspect changes, previews, subagents, or browser actions without losing track of the current turn. If you need clarification during a long task, open a side chat with /btw so the main turn keeps running while you ask context-aware questions. For input, use dictation in chat, editors, or the terminal; terminal dictation applies shell-aware cleanup, so spoken commands are transformed into usable shell syntax rather than literal words. When reviewing documentation or notes, try the experimental hybrid Markdown diff mode so you can inspect rendered changes while continuing to edit. When reviewing web output, use the integrated browser’s element commenting mode to annotate exact UI elements instead of giving broad feedback. Two caveats from the source: rollout is gradual, and some capabilities, such as hybrid Markdown diffs, are explicitly experimental.

## Training Exercise

Open VS Code 1.132 and perform a single end-to-end task: ask an agent to create or revise a Markdown document, monitor progress through the Agents window, open a side chat with /btw to ask one clarifying question, then review the result in the hybrid Markdown diff editor if available. Next, open a web preview in the integrated browser and leave feedback on at least two specific page elements. Finish by dictating one terminal command and one sentence of prose so you can compare shell-aware dictation cleanup with normal text dictation. As you work, note which steps reduce context switching and which still feel manual.

## Test Yourself

<details><summary>How does /btw help during a long-running agent task?</summary>

It opens a side chat that shares the primary chat's context and prompt cache without interrupting the current agent turn. This lets you ask clarifying questions while the main task continues.

</details>

<details><summary>What makes dictation in VS Code 1.132 useful for both prose and terminal commands?</summary>

The release notes say multilingual dictation runs on device and works across chat, editors, and the terminal. Terminal input receives shell-aware cleanup, whereas ordinary text dictation is cleaned up as prose.

</details>

<details><summary>Which VS Code 1.132 feature should be treated most cautiously, and why?</summary>

Hybrid Markdown diffs should be treated cautiously because the release notes label them experimental. They allow editing a modified Markdown document while viewing diff markers, but their behavior may not yet be fully settled.

</details>

## Further Reading

- [Visual Studio Code 1.132](https://code.visualstudio.com/updates/v1_132)
