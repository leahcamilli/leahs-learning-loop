---
title: "GitHub Copilot CLI’s New Terminal UI for Issues, PRs, and Gists"
source: "https://www.linkedin.com/posts/copilot-cli-just-got-a-new-terminal-user-ugcPost-7475237629266067456-ZE9f/?utm_source=social_share_send&utm_medium=ios_app&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY&utm_campaign=share_via"
date: "2026-06-23"
tags: [copilot, cli, terminal-ui, github, developer-workflow]
source_type: "web"
topics: [github-copilot, developer-tools, coding-agents]
kind: "news"
depth: 2
actionability: 2
---

## TL;DR

> GitHub Copilot CLI’s new terminal UI brings issues, pull requests, gists, local code, and AI assistance into one workflow. This matters because developers can move from task intake to implementation, review, and merge with fewer context switches.

## Key Takeaways

1. Use the Issues, Pull Requests, and Gists tabs to inspect GitHub objects without leaving the terminal.
2. Press `C` in the demonstrated workflow to add the selected issue or pull request as context for Copilot chat.
3. Use `/pr create` to initiate pull-request creation from Copilot CLI instead of manually moving between Git and GitHub interfaces.
4. Treat Copilot CLI as a workflow hub connecting GitHub repository data, the local workspace, and assistant-driven implementation or review.
5. Keep human verification in the loop: inspect changed files, test the implementation, and validate Copilot’s summary before merging.
6. Open an item in the browser when a task benefits from GitHub’s richer web interface; the terminal UI complements rather than completely replaces it.
7. Measure the UI’s value by tracking context switches for issue management, link copying, pull-request inspection, and review during a real task.

## Overview

This update introduces a richer terminal user interface for GitHub Copilot CLI, bringing GitHub platform objects like issues, pull requests, and gists directly into the terminal. Instead of bouncing between shell, editor, browser, and chat, developers can navigate repository work, invoke Copilot, and perform common GitHub actions from one place.

For engineers who spend most of their day in the terminal, this matters because it reduces context switching and tightens the feedback loop between planning, implementation, review, and merge. The announcement is especially relevant to developers using GitHub-heavy workflows, platform engineers standardizing CLI-based tooling, and teams experimenting with agent-assisted development.

## Key Concepts

- **Terminal-native GitHub workflow**: The core idea is to expose GitHub objects directly inside a terminal UI instead of requiring a browser for every repository management action. This keeps operational context close to the code and shell commands where implementation work already happens.
- **Copilot CLI as a workflow hub**: Copilot CLI is positioned not just as a chat interface but as an orchestration layer for coding and repository actions. In the demo, it is used to inspect issues, reference issue and PR context in chat, create pull requests, and request review or merge assistance.
- **Integrated repository context**: The terminal UI surfaces repo-scoped information such as issues and pull requests, plus user-scoped artifacts like gists. This means the assistant can operate with live workflow context rather than relying only on manually pasted links or summaries.
- **Keyboard-driven navigation and actions**: The transcript emphasizes quick navigation with tabs and single-key actions like opening items in the browser or copying references into chat. That interaction model is important because efficient terminal tools rely on low-friction, discoverable shortcuts.
- **Human-agent collaboration**: The demo shows a developer opening an issue, asking Copilot to implement the change, then having Copilot summarize and help validate the resulting pull request. The tool is framed as supporting collaboration across both humans and AI agents, not replacing normal software development lifecycle steps.
- **Reduced context switching**: A major benefit of the new UI is avoiding repeated transitions between terminal and browser during development. Less switching generally improves focus, shortens execution time for routine tasks, and makes AI-assisted workflows feel more continuous.

## How It Works

The announcement describes a new terminal UI layered into GitHub Copilot CLI. While the source is a product demo rather than source code or technical docs, the mechanics are clear enough to outline the workflow model.

At a high level, the terminal UI acts as a **multi-pane GitHub workspace** inside the CLI:

- A chat or command area where the user interacts with Copilot
- Top-level tabs for GitHub entities such as **Issues**, **Pull Requests**, and **Gists**
- Keyboard shortcuts and simple commands to inspect, open, copy, create, and act on those entities

The intended flow is:

1. **Start in the terminal inside a repository**
   - Copilot CLI is launched from the project directory.
   - The UI appears with GitHub-themed styling and repo-aware tabs.

2. **Work with issues without leaving the CLI**
   - The user creates or navigates to an issue related to a feature request.
   - The issues tab can filter to personal issues or all issues.
   - The user can open the selected issue in a browser when needed, which suggests the terminal view is integrated with standard GitHub URLs rather than replacing the web UI entirely.

3. **Inject issue context into Copilot chat**
   - A key action shown in the transcript is pressing `C` to add the issue reference to the chat.
   - This likely passes structured context—such as issue number or link—into the Copilot prompt so the assistant can work from the exact task being discussed.

4. **Delegate implementation to Copilot**
   - Once issue context is attached, the user asks Copilot to handle implementation.
   - In the demo, Copilot edits the app to add drag-and-drop support and returns when the change is ready.
   - Although the source does not expose internals, the implication is that Copilot CLI can inspect the local codebase, modify files, and drive an implementation loop from terminal context.

5. **Create a pull request from the CLI**
   - The demo uses a slash command like `/pr create`.
   - This suggests Copilot CLI supports high-level workflow commands that bundle lower-level Git and GitHub operations: checking branch state, generating title/body text, and opening the PR against the remote repository.

6. **Review pull requests with AI assistance**
   - After PR creation, the user tabs to the pull requests view and selects the new PR.
   - Pressing `C` again adds PR context into chat.
   - Copilot is then asked to summarize or review the PR, effectively turning the CLI into a review cockpit where GitHub metadata and AI analysis are colocated.

7. **Finalize workflow actions**
   - The transcript ends by asking Copilot to merge, showing that terminal-based interactions can extend beyond coding into repository lifecycle management.

Conceptually, the system combines three layers:

- **Repository data layer**: issues, pull requests, gists, assignments, and links from GitHub
- **Local workspace layer**: source code, branch state, and files in the current checkout
- **Assistant layer**: Copilot chat, command interpretation, summarization, and implementation help

That combination matters because most engineering tasks cross all three layers. A feature request begins as an issue, becomes source changes in a branch, then becomes a pull request and review event. The new terminal UI appears designed to let developers traverse that path without switching interfaces.

The transcript also hints at an important design principle: the terminal UI is **not trying to replace every browser interaction**. Instead, it supports selective handoff. For example, the user can inspect items in the terminal but still press a shortcut to open the full GitHub page in the browser. That is a pragmatic approach for a developer tool because some actions are faster in TUI form, while others still benefit from the richer web interface.

In short, the new Copilot CLI UI works as a workflow concentrator: it brings code, repository state, and AI assistance together so common development tasks can be executed from a single terminal session.

## Training Exercise

Build a terminal-first GitHub workflow and identify where Copilot CLI’s new UI would save you time.

### Goal
Simulate the exact lifecycle shown in the announcement:

- define a task as an issue
- implement a change locally
- create a pull request
- review the change with AI or a structured checklist

### Prerequisites

- A GitHub repository you can push to
- Git installed
- GitHub CLI (`gh`) installed and authenticated
- Optional: GitHub Copilot CLI installed if you have access

### Step 1: Create a small feature task
Pick a very small change in your repo, such as:

- renaming a confusing function
- adding a CLI flag
- improving README setup instructions
- fixing a small UI bug

Create an issue from the terminal:

```bash
gh issue create \
  --title "Add small usability improvement" \
  --body "Implement a small improvement and document the change."
```

### Step 2: Create a branch and implement the change

```bash
git checkout -b feature/small-usability-improvement
```

Make the code or documentation change, then commit it:

```bash
git add .
git commit -m "Add small usability improvement"
```

### Step 3: Push and open a pull request

```bash
git push -u origin feature/small-usability-improvement
gh pr create --fill
```

If you have Copilot CLI with the new TUI, repeat this step there using its PR creation flow or slash command instead of `gh pr create`.

### Step 4: Review the change in a terminal-first way
Use the GitHub CLI to inspect the PR:

```bash
gh pr view --web
```

Then write a short review summary for yourself using this checklist:

- What problem does this PR solve?
- Which files changed?
- Is the implementation minimal and readable?
- What should be tested before merge?

If you have Copilot CLI access, ask it to summarize the PR and compare its output to your own checklist.

### Step 5: Reflect on context switches
Track every time you had to leave the terminal for:

- issue creation or assignment
- PR inspection
- copy/pasting links into prompts
- reviewing changed files

Write down where a built-in TUI with issue/PR tabs and quick-copy actions would reduce friction.

### Stretch exercise
If you want to get closer to the demo, try mapping these terminal actions to a single working session:

1. Open an issue
2. Reference the issue in your implementation notes
3. Create a PR linked to that issue
4. Produce an AI-assisted PR summary
5. Merge after verification

The learning objective is not just using another CLI tool; it is understanding how integrated terminal workflows compress the path from task intake to merged code.

## Test Yourself

<details><summary>What three layers does the lesson say Copilot CLI brings together?</summary>

It combines GitHub repository data such as issues and pull requests, the local workspace containing code and branch state, and the assistant layer for implementation, commands, and summaries.

</details>

<details><summary>How does the demonstrated `C` shortcut support an agent-assisted workflow?</summary>

It adds the selected issue or pull-request reference to Copilot chat, giving the assistant specific workflow context without requiring the developer to copy and paste links or summaries manually.

</details>

<details><summary>Why should the terminal UI not be treated as a complete replacement for GitHub’s browser interface?</summary>

The lesson describes selective handoff: common actions can stay in the terminal, while detailed or visually richer tasks can still be opened in the browser. Developers should use whichever interface best fits the action.

</details>

## Further Reading

- [GitHub Copilot CLI Documentation](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-github-copilot-in-the-command-line)
- [GitHub CLI Manual](https://cli.github.com/manual/)
- [GitHub Issues Documentation](https://docs.github.com/en/issues)
- [About Pull Requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
