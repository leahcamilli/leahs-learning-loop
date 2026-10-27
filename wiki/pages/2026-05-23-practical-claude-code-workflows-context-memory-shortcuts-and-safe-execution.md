---
title: "Practical Claude Code Workflows: Context, Memory, Shortcuts, and Safe Execution"
source: "https://open.substack.com/pub/nandigamharikrishna/p/claude-shortcuts-and-power-workflows?r=7692ad&utm_medium=ios"
date: "2026-05-23"
tags: [claude, developer-tools, context-management, ai-workflows, cli, productivity]
source_type: "web"
topics: [claude, coding-agents, context-engineering, prompt-engineering]
kind: "tutorial"
depth: 2
actionability: 3
---

## TL;DR

> Reliable AI-assisted engineering depends less on clever prompts than on disciplined context, durable file-based memory, tight execution scope, and proof that changes work. Inspect before editing, interrupt drift early, and preserve handoffs so work remains accurate and recoverable across sessions.

## Key Takeaways

1. Inspect the repository and relevant instructions before editing; request the architecture, likely test commands, task-relevant files, and constraints first.
2. Limit each task to the smallest useful set of files, facts, and tools to reduce token usage and prevent context rot.
3. Interrupt Claude immediately when it targets the wrong layer, broadens scope, or proposes an unnecessary refactor; redirect it to a revised plan before allowing edits.
4. Store recurring rules and state in `CLAUDE.md`, `project_specs.md`, `progress.md`, and `decisions.md` instead of repeatedly supplying them through chat.
5. Use `/compact` at related-work breakpoints with explicit preservation instructions; use `/clear` for unrelated work only after recording a structured handoff.
6. Assign sub-agents independent, bounded investigations with specific outputs, then have the main session compare their findings before edits begin.
7. Require evidence before accepting completion: test results, browser or screenshot checks for UI work, reviewed diffs, executed commands, and documented remaining risks.

## Overview

This lesson explains how to use Claude as a structured development collaborator rather than a generic chat assistant. The source article focuses on operational habits that make Claude Code and Claude Desktop more reliable in real engineering work: scoping context, interrupting drift early, preserving state in files, using slash commands deliberately, and verifying changes with tests and visual checks.

This matters for engineers who use AI on multi-step tasks like debugging, feature delivery, refactors, documentation, and UI fixes. The core message is that prompt quality alone is not enough; durable instructions, session hygiene, external memory, and bounded execution are what keep AI-assisted workflows fast, accurate, and recoverable over hours or days of work.

## Key Concepts

- **Operational steering**: Claude is most effective when treated like a collaborator that needs active supervision. The article emphasizes interrupting early, asking for a plan before edits, and correcting direction before large diffs or polluted context accumulate.
- **Context engineering**: Context is the model's working memory: conversation history, files, tool outputs, screenshots, and instructions. Good workflows intentionally load only the files and facts needed for the current task, because excessive context makes responses slower, less precise, and more prone to 'context rot.'
- **Durable project memory**: Important instructions should live in files like `CLAUDE.md`, `project_specs.md`, `progress.md`, and `decisions.md` instead of being repeated in chat. This makes sessions recoverable, reduces token waste, and prevents the model from re-litigating settled architectural or product decisions.
- **Session boundary management**: The article distinguishes between compaction and clearing. `/compact` should be used at deliberate breakpoints to preserve the right facts, while `/clear` is for unrelated tasks after saving a structured handoff to disk.
- **Scoped automation**: Features like MCP servers, custom commands, and sub-agents are valuable only when tightly scoped. The best results come from enabling the smallest useful toolset, assigning bounded investigation areas, and keeping the main session as the orchestrator.
- **Verification-first execution**: Claude should not be trusted on completion claims without evidence. Engineers should require concrete verification steps such as test commands, browser checks, screenshots, diff reviews, and explicit reporting of remaining risks.

## How It Works

The article presents a workflow model for Claude that looks more like software operations than prompting. Instead of repeatedly asking broad questions in a single long conversation, you create a controlled loop:

1. define durable instructions
2. load only relevant context
3. inspect before editing
4. ask for a plan
5. execute in small scoped steps
6. verify with commands or screenshots
7. save state externally
8. compact or clear at task boundaries

At the center of the method is the idea that AI sessions degrade over time unless you manage them. The article calls out **context rot**: a state where Claude starts forgetting constraints, touching unrelated files, repeating stale plans, or producing generic explanations instead of precise work. The fix is not "better prompting" in the abstract; it is active context hygiene.

A practical pattern is to separate Claude usage into roles:

- **Claude Code** for tactical repo work: file inspection, implementation, tests, diffs, branch-local changes.
- **Claude Desktop** for broader synthesis: screenshots, visual interpretation, long-lived project references, product rules, writing style, and cross-app workflows.

The article's recommended mechanics break down into a few operational layers.

**1. Start with narrow repo orientation**

Before making edits, ask Claude to inspect the repository and summarize architecture, likely build/test commands, and the most relevant files. This avoids the common failure mode where the agent begins coding without understanding boundaries.

Example prompt pattern:

```text
Read the project instructions and inspect the repo structure.
Do not edit files.
Tell me:
1. the app architecture
2. the likely test/build commands
3. the files most relevant to this task
4. any constraints I should know before implementation
```

This is a recurring theme: first inspect, then plan, then edit.

**2. Scope context aggressively**

The article strongly advises against prompts like "search the whole repo and fix auth." Instead, specify exact files and a limited objective. For example:

```text
Read @src/auth/session.ts and @src/auth/session.test.ts.
Find why refresh token rotation fails.
Do not inspect unrelated routes yet.
```

This improves precision and reduces token usage. If the session has already touched many files, check `/context` and decide whether to compact or reset.

**3. Interrupt drift immediately**

The most important steering shortcut is not a slash command but the habit of pressing `Esc` as soon as Claude goes down the wrong path. The article argues that waiting for a bad plan to finish wastes tokens and fills the session with noisy edits.

A good corrective response is concrete and directional:

```text
Stop. That is the wrong layer.
First inspect the service boundary and propose a plan only.
```

This keeps the session recoverable and prevents large unrelated diffs.

**4. Use slash commands as control surfaces**

The article highlights two high-value commands:

- **`/compact`**: use at natural breakpoints, not as a last-minute cleanup. Give explicit preservation instructions so the summarized context keeps decisions, changed files, failing tests, constraints, and next steps.
- **`/clear`**: use when the next task is unrelated. Before clearing, write a handoff file such as `progress.md` so the next session can restart from stable external memory.

Example compaction prompt:

```text
/compact focus on preserving:
- the auth refactor decisions
- files already changed
- tests still failing
- constraints from CLAUDE.md
- next exact implementation steps
```

**5. Move repeated context into files**

The article proposes a layered memory model:

- `CLAUDE.md`: repo-specific operational rules
- `project_specs.md`: product goals and workflow intent
- `progress.md`: current task state and handoff notes
- `decisions.md`: durable architecture choices
- `memory.md`: recurring lessons or preferences

This architecture matters because chat history is volatile and expensive, while files are durable and versionable. A good `CLAUDE.md` should be concrete and enforceable, for example:

```md
# Project Instructions
- Use TypeScript strict mode.
- Prefer existing service helpers over new abstractions.
- Run `npm test` before final responses.
- Do not edit generated files.
- Keep API response shapes backward compatible unless explicitly asked.
```

The effect is to convert recurring verbal guidance into a reusable local policy layer.

**6. Encode repeated work as skills and commands**

The article describes reusable workflows as "skills" and narrower shortcut prompts as custom commands. These are most useful when they define a stable SOP rather than a vague request. A strong command like `/prepare-pr` has a checklist and expected output; a weak command like `/make-good` creates ambiguity.

The same principle applies to repeated engineering tasks such as API review, writing tests, summarizing diffs, or generating release notes. The more structured the task, the less prompting overhead per session.

**7. Add tools selectively with MCP**

Model Context Protocol integrations let Claude access live resources such as browser automation, docs, databases, issue trackers, and internal APIs. The article's caution is important: every connected tool increases operational surface area and often increases context load. The right practice is to enable the smallest tool set that can complete the task.

Typical combinations include:

- repo + browser automation for UI debugging
- repo + database for migration work
- repo + docs lookup for upgrades
- file output + notebook/research tools for content pipelines

In other words, tools should be task-shaped, not always-on.

**8. Use sub-agents for independent bounded work**

Sub-agents are framed as useful for parallel investigation, not open-ended delegation. Good sub-agent tasks own a narrow module or question and return a specific artifact such as hypotheses, test gaps, or a constrained implementation. Poor sub-agent prompts are broad role-play instructions like "be a senior architect" or "fix everything."

A strong pattern from the article is three-way debugging:

1. one agent inspects recent code changes
2. one agent inspects failing tests and logs
3. one agent inspects architectural assumptions

The main session then compares hypotheses before any edits are made. This keeps independent reasoning separate and reduces context pollution in the top-level thread.

**9. Pair terminal discipline with Git discipline**

Because Claude Code is a CLI tool, terminal setup matters. The article recommends separate branches or worktrees for separate active sessions and suggests `tmux` panes for Claude, tests, logs, and Git status/diffs. The goal is visibility: even if Claude can run commands, the engineer should still observe failing tests, live logs, and change boundaries.

It also suggests non-interactive shell usage for bounded tasks:

```bash
claude -p "Summarize this diff and list risky files"
git diff | claude -p "Review this diff for regressions and missing tests"
```

Interactive mode is better when you expect ambiguity and need steering; piped mode is better for narrow text transformations or review passes.

**10. Finish with verification and handoff**

A recurring anti-pattern in AI-assisted development is accepting "it should work". The article argues for explicit verification requirements in the task statement itself: run tests, inspect browser behavior for UI changes, summarize commands executed, and call out remaining risks.

A clean end-of-session workflow is:

- update `progress.md`
- summarize changed files
- record verification commands and results
- note risks and unresolved questions
- recommend the next task
- compact if continuing related work, or clear if switching domains

Example handoff flow:

```bash
claude -p "Create or update progress.md with the goal, completed work, changed files, verification commands and results, known risks, and next recommended task. Keep it concise and useful for a fresh session."

claude -p "Read progress.md first, summarize the current state, then continue with the next recommended task."
```

Overall, the article's mechanism is simple but operationally disciplined: externalize memory, minimize context, verify aggressively, and keep Claude on a short leash. The payoff is not just better answers; it is more reliable multi-session engineering work with less drift, lower token burn, and cleaner recovery when tasks span days.

## Training Exercise

Build a minimal Claude workflow kit for one repository you actively work on. The goal is to convert an ad hoc AI chat habit into a repeatable engineering loop.

### Step 1: Create durable project memory
In the repo root, create these files:

- `CLAUDE.md`
- `project_specs.md`
- `progress.md`
- `decisions.md`

Populate them with a small but realistic baseline.

Example `CLAUDE.md`:

```md
# Project Instructions
- Inspect before editing.
- Prefer the smallest working fix.
- Do not edit generated files.
- Run targeted tests before claiming completion.
- Summarize changed files and risks in final responses.
```

Example `project_specs.md`:

```md
# Product Specs
This service generates internal reports from uploaded CSV files.
Primary goal: reliable ingestion and export.
Non-goals: redesigning the architecture during bug fixes.
```

### Step 2: Run an orientation prompt
Open Claude Code in the repo and ask:

```text
Read CLAUDE.md and inspect the repo structure.
Do not edit files.
Summarize:
1. the architecture
2. likely test/build commands
3. the files relevant to the CSV export path
4. constraints I should keep in mind
```

Your job is to check whether the answer is grounded and specific. If it is vague, restate with narrower file references.

### Step 3: Practice a scoped task
Pick a tiny real or synthetic task, such as:

- add filename sanitization to exports
- fix a failing unit test
- tighten a TypeScript type in one module

Prompt Claude with explicit boundaries:

```text
Inspect only the export module and related tests.
Do not edit yet.
Return:
- root cause or needed change
- smallest fix
- files to edit
- tests to run
- risks
```

Review the plan before allowing edits.

### Step 4: Interrupt on drift
If Claude proposes touching unrelated modules or broad refactors, stop it immediately and redirect:

```text
Stop. Keep scope to the export module only.
No refactor.
Revise the plan to the smallest fix and test change.
```

This step is the point of the exercise: build the reflex to intervene early rather than after the model has produced a large diff.

### Step 5: Record session state
After implementation, update `progress.md` manually or via Claude with:

- goal
- files changed
- tests run and result
- risks
- next task

You can use a prompt like:

```text
Create or update progress.md with:
- goal
- completed work
- changed files
- verification commands and results
- known risks
- next recommended task
Keep it concise.
```

### Step 6: Compact or clear intentionally
If you will continue related work, use a compaction prompt:

```text
/compact focus on preserving:
- current goal
- changed files
- test results
- constraints from CLAUDE.md
- next implementation step
```

If you are switching to an unrelated task, clear the session after confirming `progress.md` is complete.

### Step 7: Reflect
Write a short note for yourself answering:

1. What repeated instruction should be moved into `CLAUDE.md`?
2. Where did Claude try to broaden scope?
3. What evidence did you require before accepting completion?
4. What would you automate next as a custom command or skill?

### Optional terminal variant
Try one bounded headless review command:

```bash
git diff | claude -p "Review this diff for regressions, missing tests, and risky files. Return a concise checklist."
```

Success criteria:

- You used file-based memory instead of repeating instructions in chat.
- You asked for plan-before-edit.
- You corrected scope when needed.
- You ended with a reusable handoff in `progress.md`.
- You required evidence-based verification rather than trusting a completion claim.

## Test Yourself

<details><summary>What workflow should occur before Claude edits repository files?</summary>

Have Claude read the project instructions, inspect only the relevant repository areas, and report the architecture, commands, files, constraints, proposed change, and risks. Review that plan before authorizing edits.

</details>

<details><summary>When should `/compact` be used instead of `/clear`?</summary>

Use `/compact` when continuing related work and explicitly preserve decisions, changed files, test status, constraints, and next steps. Use `/clear` when switching to an unrelated task, after saving the current state in a handoff file such as `progress.md`.

</details>

<details><summary>Why are passing tests and explicit verification part of the task rather than an optional final check?</summary>

The article warns that Claude's completion claims are not sufficient evidence. Commands, test results, visual checks, diff review, and stated residual risks make the outcome verifiable and expose incomplete or unintended changes.

</details>

## Further Reading

- [Anthropic Claude Documentation](https://docs.anthropic.com/)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [tmux Getting Started](https://github.com/tmux/tmux/wiki)
- [Git Worktree Documentation](https://git-scm.com/docs/git-worktree)
