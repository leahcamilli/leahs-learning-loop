---
title: "GitHub Copilot App Technical Preview: Agentic Development Across Repos, Worktrees, and GitHub"
source: "https://www.linkedin.com/posts/burkeholland_github-just-released-a-new-ai-development-ugcPost-7462169690942132225-6Ou0?utm_source=social_share_send&utm_medium=ios_app&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY&utm_campaign=share_via"
date: "2026-05-20"
tags: [github, copilot, ai-agents, worktrees, developer-tools]
source_type: "web"
topics: [github-copilot, coding-agents, ai-agents, developer-tools]
kind: "deep-dive"
depth: 2
actionability: 1
---

## TL;DR

> The preview presents the GitHub Copilot App as a GitHub-centered development workspace where agents can handle multiple isolated tasks through branches and worktrees. This matters because repository context, code changes, review, execution, and UI inspection can stay within one workflow.

## Key Takeaways

1. Use a separate Git worktree for each concurrent task to prevent branch collisions and keep changes isolated.
2. Create full agentic sessions for branch-scoped implementation work; reserve quick chat for temporary questions such as build instructions.
3. Ground prompts in repository artifacts such as issues, pull requests, selected code, and UI elements instead of relying only on free-text descriptions.
4. Review every agent-generated change with status and diff tools before committing, checking for unrelated edits and clean task boundaries.
5. The preview claims integrated terminals and browser views close the loop between generating changes, running the application, inspecting results, and iterating.
6. The preview positions MCP servers, skills, and plugins as extension points for connecting the agent to external or organization-specific capabilities.

## Overview

The GitHub Copilot App, as described in this preview walkthrough, is positioned as more than an AI chat client: it is a desktop surface for development workflows centered on GitHub. The key idea is a unified environment where agentic coding sessions, repository context, issues, diffs, notifications, workflows, terminal access, and even browser-based UI inspection live in one place.

This matters to engineers who already use GitHub as the center of their software lifecycle and want AI assistance that is tightly integrated with real development artifacts instead of isolated prompts. The preview suggests a shift from an assistant embedded in an editor to an orchestration layer that can manage multiple workstreams, reason over repository state, and let developers move between coding, issue triage, reviewing changes, and running apps without constantly switching tools.

## Key Concepts

- **Single pane of glass**: The app is presented as a unified interface over many GitHub activities rather than just a coding chatbot. It combines repository work, notifications, workflows, search, chat, diffs, and local execution into one desktop application.
- **Agentic development sessions**: Instead of one linear prompt history, the app supports discrete sessions for specific development tasks. Each session can be tied to a branch or worktree, allowing the agent to operate with isolated context and making concurrent tasks easier to manage.
- **Git worktrees for parallel work**: A worktree lets a single repository checkout support multiple working directories attached to different branches. In this app, worktrees appear to be created automatically for new tasks, making it possible to investigate an issue and implement a feature simultaneously without branch collisions.
- **Repository-native context**: The app can reference repository artifacts like issues, pull requests, and code directly from chat. That means prompts are not purely free text; they can be grounded in actual project state, such as asking the agent to investigate issue #7 or to modify a selected UI element.
- **Integrated execution environment**: The preview shows built-in terminals and an integrated browser, allowing developers to run applications, inspect output, and iterate without leaving the app. This closes the loop between generating changes and validating them in a live environment.
- **Extensibility through MCP servers, skills, and plugins**: The app exposes extension points such as MCP servers, installed skills, and plugins. These mechanisms suggest that the model can be connected to external systems or organization-specific capabilities, expanding what the agent can access and do.

## How It Works

The walkthrough describes the GitHub Copilot App as a desktop client organized around projects and sessions. On the left side, the user sees multiple projects they are working on. Starting a new task appears to create a new worktree automatically, giving that task an isolated workspace. This is important because it maps AI-driven changes onto a real source control primitive rather than a temporary scratch buffer.

A typical flow looks like this:

1. Open a project.
2. Start a new agentic session.
3. The app creates a worktree.
4. Choose a model and reasoning level.
5. Ask for a task, such as adding a feature or investigating an issue.
6. Let the session run independently while other sessions continue in parallel.

The key architectural idea from the article is concurrency. The user can run multiple sessions at once in the same repository, each apparently attached to its own worktree. One session may implement a feature while another investigates an issue. The UI provides status indicators so the engineer can see which tasks are still running and which are complete.

The app also appears to treat GitHub itself as first-class context. The walkthrough mentions searching across repositories, pull requests, and issues, as well as opening repository-backed sessions without manually cloning first. In that model, the app is doing the repository acquisition and workspace setup for you on demand. That reduces friction for drive-by contributions, exploration, or issue triage because the engineer can begin from a GitHub URL instead of preparing a local clone manually.

Another important mechanic is that chat is not the only interaction surface. The app includes:

- **Rich diffs** for reviewing generated changes
- **Commenting on diffs** as part of the review loop
- **Integrated terminals** for builds, tests, and runtime commands
- **Integrated browser views** for web app development
- **Element-aware UI interactions** where selecting something in the browser adds it to chat context

That browser-to-chat handoff is especially notable. In the example, the user runs a web application inside the app, clicks a UI element such as a navigation bar, and the selection becomes part of the prompt context. This changes the AI interaction from "describe the thing in words" to "point at the thing and ask for a change," which can reduce ambiguity for front-end work.

The app also separates long-lived task sessions from ephemeral Q&A. The walkthrough shows a quick-chat mode for one-off questions like "How do I build this?" without creating another full project conversation. This is a practical workflow distinction: use full sessions for code changes and branch-scoped work, and use quick chat for transient repository understanding.

Configuration and extensibility are also part of the model. Settings include default model selection, storage location, themes, accessibility, and multi-account support. More strategically, the app includes support for MCP servers, installed skills, and plugins. Even though the source does not document implementation details, these features indicate a tool architecture where the base chat/model runtime can be augmented with external tools and enterprise-specific integrations.

If you compare this to a traditional editor plugin, the difference is scope. A plugin usually starts from an already-open folder and helps inside the editor. This app starts from the broader development lifecycle:

- discover work
- open repo context
- create isolated task workspaces
- ask agents to perform changes
- inspect diffs
- run the code
- browse the app
- iterate on UI and implementation

So the central reasoning is that the product is not only "AI in development" but a GitHub-centered operating surface for development tasks.

## Training Exercise

Build a practical evaluation of the workflow using tools you likely already have: Git, a sample repository, and your current AI coding assistant. The goal is to simulate the concepts in the preview, especially parallel worktrees and repository-grounded tasks.

### Exercise: Reproduce the multi-session worktree workflow manually

#### Prerequisites
- Git 2.35+
- A GitHub repository you can modify
- A local terminal
- Optional: an AI coding tool such as GitHub Copilot, Claude, or another assistant

#### Step 1: Clone a sample repository
Choose a small web app or CLI project.

```bash
git clone https://github.com/your-org/your-repo.git
cd your-repo
```

#### Step 2: Create two parallel worktrees
Simulate the app's session isolation by creating two task-specific worktrees.

```bash
git switch -c main-work
cd ..
git -C your-repo worktree add ../your-repo-feature -b feature/add-copy-command
git -C your-repo worktree add ../your-repo-bugfix -b fix/investigate-issue-7
```

You now have:
- `your-repo-feature` for a feature task
- `your-repo-bugfix` for a bug investigation

#### Step 3: Define two tasks
In the feature worktree, pick a small enhancement:
- Add a copy-to-clipboard button
- Add dark mode toggle
- Improve CLI help output

In the bugfix worktree, pick a real issue from the repo or invent one:
- Reproduce a failing command
- Inspect logs or tests
- Identify the likely source file

#### Step 4: Run both workflows independently
Open two terminal tabs.

Feature terminal:
```bash
cd ../your-repo-feature
# Run build or dev server
npm install
npm run dev
```

Bugfix terminal:
```bash
cd ../your-repo-bugfix
# Run tests or reproduce the issue
npm install
npm test
```

#### Step 5: Use an AI assistant with repository-specific prompts
Ask targeted questions that mimic the previewed workflow.

Examples:
- "In this worktree, add a copy-to-clipboard action next to the command output. Show the files to change first."
- "Investigate why issue #7 might produce a JQ parsing error. Start by locating all references to jq or JSON parsing."
- "How do I build and run this project locally? Give me only the exact commands."

#### Step 6: Review diffs before committing
In each worktree, inspect the generated or manual changes.

```bash
git status
git diff
```

Ask yourself:
- Are changes isolated to the correct task?
- Did the assistant modify unrelated files?
- Are commit boundaries cleaner because work is separated by worktree?

#### Step 7: Commit each task separately
```bash
git add .
git commit -m "Add copy-to-clipboard feature"
```

In the other worktree:
```bash
git add .
git commit -m "Investigate and fix issue #7"
```

#### Step 8: Reflect on the product design
Write short answers to these prompts:
1. What friction disappeared when tasks were isolated by worktree?
2. What still required manual coordination?
3. Which parts would be improved by an integrated terminal, diff viewer, and browser?
4. When is a quick one-off chat enough, and when do you need a full task session?

### Stretch goal
If your repository is a web app, run it locally and inspect one UI element you want to change. Then write a prompt that references the exact component or DOM area, as if you had the app's element-to-chat handoff:

```text
Update the navbar component to be 8px taller, preserve responsive behavior, and keep contrast accessible in dark mode.
```

This exercise teaches the underlying engineering model even if you do not yet have access to the GitHub Copilot App preview.

## Test Yourself

<details><summary>Why does the preview associate each agentic session with a Git worktree?</summary>

A worktree gives each task its own working directory and branch, allowing multiple sessions to operate concurrently without colliding. It also makes diffs and commits easier to review by keeping task changes separate.

</details>

<details><summary>When should you use a full task session instead of quick chat?</summary>

Use a full session for code changes, investigation, or other work that needs persistent repository context and branch isolation. Use quick chat for transient questions that do not require a dedicated workstream.

</details>

<details><summary>How does the browser-to-chat handoff improve front-end development according to the lesson?</summary>

It lets a developer select a visible UI element and add it directly to the agent's context. The preview suggests this can reduce ambiguity compared with describing the target only in words.

</details>

## Further Reading

- [Git Worktree Documentation](https://git-scm.com/docs/git-worktree)
- [GitHub Copilot Features](https://github.com/features/copilot)
- [GitHub Documentation](https://docs.github.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
