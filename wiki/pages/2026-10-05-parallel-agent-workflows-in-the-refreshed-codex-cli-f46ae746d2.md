---
title: "Parallel Agent Workflows in the Refreshed Codex CLI"
source: "https://www.youtube.com/watch?v=PUBc2G0Tj5E"
date: "2026-10-05"
tags: [codex, cli, developer-tools, ai-agents, terminal-workflows]
source_type: "youtube"
source_fingerprint: "f46ae746d2"
source_characters: 3250
channel: "OpenAI"
published: "2026-10-05"
duration_seconds: 194
topics: [developer-tools, coding-agents, ai-agents]
kind: "demo"
depth: 2
actionability: 2
---

## TL;DR

> The refreshed Codex CLI keeps multiple coding tasks, their status, and their outputs inside one terminal-centered interface. Parallel agents, isolated worktrees, remote control, and rendered technical artifacts can reduce context switching during development.

## Key Takeaways

1. Start independent tasks in parallel when they can proceed without blocking one another, such as changing a website, expanding tests, and documenting a flow.
2. Use the agent view to filter, search, group by status, and open active tasks instead of tracking work across separate terminals and directories.
3. Fork a conversation into a new worktree to explore another implementation direction with the same context but a separate checkout.
4. Enable remote control on a specific computer to check task progress and answer Codex questions from a phone, as demonstrated in the walkthrough.
5. Review completed changes and test results when returning to the terminal; the interface also renders Mermaid diagrams and supported LaTeX inline.
6. Use activity analytics to inspect frequently used chats, plugins, and skills.

## Key Moments

- [0:34](https://www.youtube.com/watch?v=PUBc2G0Tj5E&t=34s) — See how the full-screen interface preserves scrollable output while keeping the next-message footer available.
- [1:04](https://www.youtube.com/watch?v=PUBc2G0Tj5E&t=64s) — Learn how one voice request launches three separate tasks across multiple projects.
- [1:34](https://www.youtube.com/watch?v=PUBc2G0Tj5E&t=94s) — Explore agent filtering, status grouping, search, follow-ups, and conversation forks into isolated worktrees.
- [2:06](https://www.youtube.com/watch?v=PUBc2G0Tj5E&t=126s) — See remote control used to monitor the same computer and respond to a task from a phone.
- [2:37](https://www.youtube.com/watch?v=PUBc2G0Tj5E&t=157s) — View usage analytics plus Mermaid and supported LaTeX rendered directly in the terminal.

## Overview

The OpenAI walkthrough presents a refreshed, full-screen Codex CLI designed for developers who prefer to remain in the terminal. It demonstrates launching multiple agent tasks by voice, monitoring them from a unified task view, and reviewing their outputs without manually searching through terminals or project directories.

The workflow matters most for developers coordinating independent changes across one or more projects. Worktree-based forks support isolated experimentation, while remote control, activity analytics, and in-terminal rendering extend the workflow beyond editing code alone.

## Key Concepts

- **Full-screen terminal interface**: Earlier output remains scrollable while the footer for the next message stays available. The design is intended to keep interaction and task history accessible in one terminal view.
- **Parallel agent tasks**: A single request can start several distinct tasks across multiple projects. The example assigns agents to a website change, CLI test coverage, and a Mermaid order-flow diagram.
- **Agent task management**: The agent view shows running work and supports filtering, status grouping, search, and direct task navigation. Codex can also be asked to inspect other tasks or send follow-up instructions.
- **Conversation forks and worktrees**: A conversation can be forked with the same context into a separate worktree. The presenter describes this as a completely separate checkout for trying another development direction.
- **Remote control**: The walkthrough enables remote control on a laptop, selects that computer from a phone, and accesses the same tasks. This allows progress checks and answers to agent questions while away from the keyboard.
- **Terminal-native artifacts**: The interface renders a Mermaid diagram directly in the terminal and is described as supporting LaTeX rendering. This keeps documentation and mathematical notation alongside the development workflow.
- **Usage analytics**: The demonstrated analytics view reports activity, top chats, and used plugins and skills. It can help a user understand which parts of their Codex workflow they rely on most.

## How It Works

1. Open a project in the Codex CLI's full-screen interface.
2. Describe multiple independent outcomes in one request; the demonstration uses voice mode to request three separate tasks.
3. Enter the agent view to see running tasks, then filter, group by status, search, or open a specific task.
4. Ask Codex to inspect another task or send a follow-up when coordination is needed.
5. Fork the conversation into a separate worktree when testing an alternative direction that should not share the original checkout.
6. Optionally enable remote control for a specific computer, then monitor or unblock the same tasks from a phone.
7. Return to the terminal to inspect completed changes, test results, diagrams, and any work that still needs attention.

## Training Exercise

1. Choose a small project with three independent needs: one visible feature change, one test improvement, and one documentation artifact.
2. Ask Codex to create three separate tasks—for example, adjust a page background, test a price-change and confirmation path, and generate a Mermaid flow diagram.
3. Open the agent view and practice filtering, grouping by status, searching, and jumping directly into each task.
4. Send one task a follow-up that clarifies an acceptance criterion.
5. Fork one conversation into a separate worktree and use it to explore an alternative implementation.
6. Review the resulting changes and test output before accepting anything; confirm that each task met its stated goal and remained within its intended project.
7. Render the Mermaid result in the terminal and record which parts of the workflow reduced manual navigation or context switching.

## Test Yourself

<details><summary>When should separate Codex tasks be run in parallel rather than as one combined task?</summary>

Use separate tasks when the work can advance independently—for example, modifying a website, checking CLI tests, and producing a diagram. The walkthrough shows these running concurrently across multiple projects.

</details>

<details><summary>Why is a worktree useful when exploring a different implementation direction?</summary>

It preserves the conversation context while providing a separate checkout. This lets you experiment without mixing the alternative approach into the original working tree.

</details>

<details><summary>How does the demonstrated workflow reduce context switching?</summary>

The CLI centralizes task creation, agent status, search, follow-ups, changes, test results, and rendered artifacts. Remote control also lets the user monitor and unblock those same tasks away from the terminal.

</details>

## Further Reading

- [Meet the New Codex CLI](https://www.youtube.com/watch?v=PUBc2G0Tj5E)
