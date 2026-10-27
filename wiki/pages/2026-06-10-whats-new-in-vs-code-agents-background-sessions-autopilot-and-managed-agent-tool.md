---
title: "What’s New in VS Code Agents: Background Sessions, Autopilot, and Managed Agent Tooling"
source: "https://www.linkedin.com/posts/in-the-latest-vs-code-release-the-agents-ugcPost-7470534675556515840-0iWU/?utm_source=share&utm_medium=member_ios&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY"
date: "2026-06-10"
tags: [vscode, agents, ai-tools, developer-workflow, enterprise]
source_type: "web"
topics: [developer-tools, coding-agents, ai-agents, github-copilot]
kind: "news"
depth: 2
actionability: 2
---

## TL;DR

> VS Code is shifting AI assistance from a blocking chat into a session-based workflow where agent tasks can run in the background while developers keep working. Better completion detection, embedded browsing, and enterprise plugin controls aim to make that workflow more efficient, reliable, and governable.

## Key Takeaways

1. Run bounded agent tasks in the background so you can continue editing, reviewing diffs, or testing while the agent works.
2. Use the searchable session picker to move quickly among concurrent or recent agent tasks without hunting through UI state.
3. The release describes Autopilot as enabled by default and better at stopping when work is actually complete, reducing premature stops and unnecessary loops.
4. Revisit documentation faster through integrated-browser URL suggestions based on previously visited pages.
5. Keep high-frequency browser actions persistently visible by customizing the integrated browser toolbar.
6. Enterprise administrators can restrict available agent plugins to support security review, compliance, and standardized tooling.
7. Evaluate agent reliability by checking whether its output is complete, directly reviewable, and produced without excessive iteration.

## Overview

This update focuses on how Visual Studio Code is evolving its AI-assisted workflow through the preview Agents window and related productivity features. The release introduces backgroundable agent sessions, a searchable session picker, improved Autopilot behavior, richer integrated browser ergonomics, and administrative controls for agent plugins in enterprise environments.

For working engineers, these changes matter because they reduce context-switching friction when using AI assistance during development. Instead of treating an agent interaction as a single blocking chat, VS Code is moving toward a multitasking model where multiple AI sessions can continue in parallel while the editor remains the primary workspace.

## Key Concepts

- **Background agent sessions**: Agent sessions can now be sent to the background instead of occupying the foreground interaction surface. This enables developers to keep long-running or exploratory AI tasks active while continuing to edit, review, or test code elsewhere in the editor.
- **Searchable session switching**: A searchable picker lets users move between active or recent agent sessions quickly. This is important when developers are working on multiple tasks, branches, or lines of investigation and need fast recall without manually hunting through UI state.
- **Autopilot completion behavior**: Autopilot is now enabled by default and is described as better at recognizing when work is actually complete. The practical implication is fewer premature stops and fewer runaway loops, which improves trust in automated multi-step assistance.
- **Integrated browser memory**: The integrated browser now remembers visited pages and surfaces them as suggestions in the URL bar. This makes research and documentation lookup inside VS Code more efficient, especially during debugging or implementation tasks that require repeated navigation.
- **Persistent browser toolbar customization**: Users can choose which browser toolbar actions remain persistently visible. This is a workflow optimization feature: high-frequency actions stay accessible, while lower-value controls can be deprioritized to reduce clutter.
- **Enterprise plugin governance**: Enterprise administrators can centrally control which agent plugins are available to teams. This supports compliance, security review, and standardization by constraining AI tool integrations to approved extensions and capabilities.

## How It Works

The release describes a shift from a single-threaded chat interaction model toward **session-oriented AI workflows** inside VS Code. The key idea is that an agent session is no longer something you must stay attached to until it finishes. Instead, you can start a session, move it into the background, and continue using the editor normally. That means the AI system becomes more like an asynchronous collaborator than a modal assistant.

In practice, the workflow appears to look like this:

1. Start an agent task from the Agents window.
2. Let the agent work on a coding or research objective.
3. Send that session to the background if you want to reclaim editor space.
4. Continue writing code, reviewing diffs, or running tests.
5. Return to the session later using a searchable picker.

This matters because AI-assisted development often involves waiting on multi-step operations such as code generation, project-wide reasoning, or follow-up edits. Background sessions reduce the cost of that waiting time by turning idle UI occupancy into parallel work.

A second major change is the behavior of **Autopilot**. The release notes frame this as a quality improvement in the agent’s stopping criteria: it should better detect when a task is truly complete, avoiding two common failure modes:

- **Stopping too early**: the agent leaves the task half-finished and requires manual prompting to continue.
- **Looping too long**: the agent keeps iterating or re-checking beyond the point of useful work.

For engineers, this is really about **control-loop tuning**. A useful autonomous assistant must decide when to act again, when to verify, and when to stop. Better termination behavior improves reliability and lowers supervision overhead.

The integrated browser improvements target a different part of the workflow: **in-editor research and navigation**. By remembering visited pages and surfacing them in the URL bar, VS Code reduces repeated lookup effort. If you frequently bounce between API docs, issue trackers, dashboards, and internal tools, browser history suggestions inside the editor keep that context close to the code.

The browser toolbar customization is a small but meaningful UX refinement. Persistent actions act like pinned controls for the subset of commands you use most often. This supports a principle common in developer tooling: optimize the interface for repeated, high-value actions while keeping infrequent controls available but not distracting.

Finally, the enterprise plugin management feature reflects the operational reality of AI tooling in organizations. Agent capabilities are often extended by plugins, and plugins may introduce access to external systems, data movement, or specialized actions. Central administration gives platform teams a way to define the allowed tool surface area. Conceptually, this is a governance layer around agent extensibility.

Taken together, the release suggests a broader architecture of AI in the editor built around:

- **Session management** for concurrent agent work
- **Autonomous execution** with improved completion detection
- **Embedded research tooling** via the integrated browser
- **UI personalization** for faster daily workflows
- **Administrative policy controls** for enterprise deployment

Even though the source is a short announcement rather than a detailed technical spec, the central reasoning is clear: VS Code is making agent-based development feel less like a one-off assistant prompt and more like a persistent, multitasking development environment.

## Training Exercise

Use the new release concepts to design and test a practical AI-assisted workflow in VS Code.

### Goal
Simulate a real development session where you:
- run one agent task in the background,
- switch to another task,
- use the integrated browser for documentation lookup,
- and evaluate whether Autopilot stops at the right time.

### Steps
1. **Update VS Code** to the latest release that includes the Agents window preview.
2. **Open a small project** you can safely experiment with, such as a sample app or internal utility.
3. **Create Task A** in the Agents window:
   - Ask the agent to perform a bounded coding task, such as refactoring a helper function or adding tests for one module.
4. **Send Task A to the background** once it begins working.
5. **Create Task B**:
   - Ask for a different task, such as documenting a module, identifying dead code, or proposing a bug fix.
6. **Use the searchable session picker** to switch between Task A and Task B.
7. **Open the integrated browser** and visit 2-3 relevant documentation pages for your project stack.
8. **Verify URL suggestions** by typing part of a previously visited page and confirming that history is surfaced.
9. **Customize browser toolbar actions** so that the commands you use most often remain visible.
10. **Evaluate Autopilot**:
    - Did it stop before the work was actually complete?
    - Did it continue looping after the task looked done?
    - Did it produce a result you could directly review or apply?

### Suggested prompt examples
```text
Task A: Refactor the date formatting utility to remove duplicated logic and keep behavior unchanged. Show the final diff summary.
```

```text
Task B: Inspect the user service module and propose 3 missing unit tests with edge cases. If possible, implement them.
```

### Reflection checklist
Write down your observations for each item:
- Which kinds of tasks worked well in the background?
- Was session switching fast enough to feel natural?
- Did browser history suggestions save time?
- Which toolbar actions did you choose to pin, and why?
- Would your team need admin restrictions on agent plugins?

### Optional team exercise
If you work in an enterprise environment, draft a one-page policy proposal answering:
- Which agent plugins should be allowed by default?
- Which should require review?
- What data access boundaries should plugins respect?
- Who owns approval and auditing?

## Test Yourself

<details><summary>How do background sessions change the agent workflow in VS Code?</summary>

They let an agent continue a coding or research task without occupying the foreground interaction surface. Developers can keep working in the editor and return through the searchable session picker.

</details>

<details><summary>What two failure modes is the improved Autopilot completion behavior intended to address?</summary>

According to the release description, it aims to avoid stopping before a task is finished and continuing to iterate after useful work is complete. Better stopping criteria should reduce the supervision required for multi-step tasks.

</details>

<details><summary>Why do enterprise plugin controls matter for agent-based development?</summary>

Agent plugins may connect to external systems, access data, or perform specialized actions. Central controls let administrators limit those capabilities to reviewed plugins and enforce organizational security and compliance policies.

</details>

## Further Reading

- [Visual Studio Code Release Notes](https://code.visualstudio.com/updates)
- [Visual Studio Code Documentation](https://code.visualstudio.com/docs)
- [Visual Studio Code AI and Copilot Documentation](https://code.visualstudio.com/docs/copilot/overview)
- [Visual Studio Code Enterprise Administration](https://code.visualstudio.com/docs/setup/enterprise)
