---
title: "Karpathy-Inspired Agent Coding Rules as a Reusable Claude Code Skill"
source: "https://github.com/multica-ai/andrej-karpathy-skills"
date: "2026-05-22"
tags: [llm-agents, claude-code, prompt-engineering, developer-tools, cursor, coding-workflows]
source_type: "github"
topics: [coding-agents, prompt-engineering, ai-agents, claude]
kind: "deep-dive"
depth: 2
actionability: 3
---

## TL;DR

> Treat coding-agent instructions as version-controlled engineering infrastructure: package a small set of behavioral rules for reuse across projects and tools. This can reduce silent assumptions, overengineering, unrelated edits, and unverified work.

## Key Takeaways

1. Centralize agent guidance in reusable, version-controlled files instead of repeating ad hoc prompts in every session.
2. Require the agent to surface ambiguity, compare plausible interpretations, and discuss tradeoffs before implementing non-trivial changes.
3. Prefer the smallest implementation that satisfies the request; avoid speculative abstractions, unnecessary configurability, and new dependencies.
4. Keep diffs surgical by editing only request-relevant code and preserving surrounding structure, comments, and public interfaces.
5. Turn vague tasks into verifiable outcomes with tests or explicit checks, and require verification before declaring completion.
6. Package the same behavioral policy for each environment: `CLAUDE.md` or a Claude Code skill/plugin, and `.cursor/rules/*.mdc` for Cursor.
7. Evaluate whether the rules work by comparing ruled and no-rules sessions on files changed, code added, clarifying questions, and verification steps.

## Overview

This repository packages a set of coding-behavior guidelines for AI coding agents into reusable configuration files for Claude Code and Cursor. Instead of being a traditional software library with runtime logic, it is an operational repo: its core artifact is a `CLAUDE.md` instruction file and related plugin/rule packaging that steer an agent toward better engineering behavior.

The value is practical: it targets common LLM failure modes in software work such as making silent assumptions, overengineering solutions, editing unrelated code, and stopping before success is verified. Engineers using Claude Code, Cursor, or similar agentic tools would care because this repo shows how to encode high-leverage behavioral constraints as portable project rules rather than relying on ad hoc prompting in every session.

## Key Concepts

- **Behavioral guardrails for coding agents**: The repository treats prompt instructions as durable engineering infrastructure. Instead of asking an LLM to be careful each time, it centralizes guidance in versioned files that can be reused across projects and tools.
- **Think Before Coding**: This principle addresses silent assumptions and hidden confusion. The agent is instructed to surface uncertainty, present interpretations, ask clarifying questions, and explicitly discuss tradeoffs before implementation begins.
- **Simplicity First**: This rule pushes the model toward minimum viable code and away from speculative abstractions. It is a direct response to LLM tendencies to overdesign APIs, add unnecessary configurability, or create too much code for a small task.
- **Surgical Changes**: The repo emphasizes narrow diffs: edit only what is required by the request, preserve surrounding code and comments, and avoid opportunistic cleanup. This reduces regression risk and makes AI-generated changes easier to review.
- **Goal-Driven Execution**: Tasks are reframed as verifiable outcomes, often via tests or explicit checks. This takes advantage of the model's ability to iterate toward a concrete success criterion instead of loosely interpreting commands like 'fix this' or 'add validation.'
- **Cross-tool rule packaging**: The same guidance is distributed in multiple formats: `CLAUDE.md` for Claude Code, plugin metadata for marketplace installation, and `.mdc` rule files for Cursor. The repo demonstrates how one set of instructions can be adapted to multiple agent environments.

## How It Works

At a code-architecture level, this repository is a configuration-and-packaging repo rather than an application repo. There is no executable business logic, server, or library API. The main data flow is:

1. Author a canonical set of agent instructions.
2. Package them for one or more agent platforms.
3. Install or copy those rules into the user's coding environment.
4. Let the agent consume those rules at prompt/runtime and modify its behavior during coding tasks.

### Repository structure

The important files are:

- `CLAUDE.md` — the core instruction document. This is the primary artifact and contains the four principles the agent should follow.
- `skills/karpathy-guidelines/SKILL.md` — the skill-packaged form of the same guidance for Claude Code's skill/plugin system.
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` — metadata that let the skill be distributed and installed through the Claude Code plugin marketplace.
- `.cursor/rules/karpathy-guidelines.mdc` — Cursor-compatible rule file so the same behavior can be applied in Cursor projects.
- `CURSOR.md` — setup documentation for using the Cursor rule in other projects.
- `EXAMPLES.md` — likely examples of how the guidance changes agent behavior in practice.
- `README.md` / `README.zh.md` — user-facing explanation and install steps.

### Core module: `CLAUDE.md`

The functional heart of the repo is the instruction text in `CLAUDE.md`. Conceptually, this file defines the policy layer for an AI coding agent. It encodes four rules:

- Think before coding
- Simplicity first
- Surgical changes
- Goal-driven execution

These are not just abstract principles; they are intended to shape concrete behavior during planning, implementation, and editing. For example:

- Before coding, the agent should identify ambiguity instead of choosing an interpretation silently.
- During coding, the agent should prefer the smallest implementation that satisfies the request.
- During edits, the agent should avoid touching unrelated lines.
- Before finishing, the agent should verify success against tests or explicit checks.

### Packaging for Claude Code

The `.claude-plugin` directory contains the metadata needed to expose the guidance as an installable plugin/skill. While the source excerpt does not show the exact JSON contents, the presence of `plugin.json` and `marketplace.json` indicates a standard packaging layer:

- `plugin.json` likely declares the plugin identity, version, and skill entrypoints.
- `marketplace.json` likely defines how the plugin is published or discovered in the Claude Code marketplace.

The installation flow from the README reflects this packaging architecture:

```text
/plugin marketplace add forrestchang/andrej-karpathy-skills
/plugin install andrej-karpathy-skills@karpathy-skills
```

That means the repo supports two usage modes:

- **Per-project local instructions** by copying/appending `CLAUDE.md`
- **Reusable global skill installation** via Claude Code plugin infrastructure

### Packaging for Cursor

The `.cursor/rules/karpathy-guidelines.mdc` file adapts the same guidance to Cursor's rule system. This is an important implementation detail: agent tooling ecosystems differ, but the repository abstracts the behavioral intent from the platform-specific delivery format.

In practice, the flow is:

- Open a project in Cursor
- Cursor loads `.cursor/rules/*.mdc`
- The agent receives these rules as context when answering or editing code

This is the same conceptual mechanism as `CLAUDE.md`, but encoded for a different toolchain.

### Operational data flow

Even though there is no runtime program, the repo still has a meaningful data flow:

1. **Source guidance** is maintained in markdown form.
2. **Tool-specific wrappers** package that guidance for Claude Code and Cursor.
3. **The developer installs or copies the rules** into their environment.
4. **The coding agent reads the instructions** before or during task execution.
5. **The agent's output changes**: smaller diffs, more clarifying questions, more verification, less incidental refactoring.

### Why this architecture matters

This repo is a good example of treating AI-agent behavior as a deployable artifact. The engineering lesson is that prompt engineering becomes more reliable when it is:

- version-controlled
- portable across tools
- documented like a product
- narrow in scope and observable in outcome

The README even defines acceptance signals for whether the guidance is working: fewer unrelated changes, less overcomplication, and more up-front clarification. That is effectively a lightweight observability model for prompt policies.

### Design tradeoffs

The repository explicitly biases toward caution over speed. That is a deliberate policy decision. It will improve performance on non-trivial engineering tasks, but it may add friction for obvious one-line fixes. In other words, the instruction set optimizes for minimizing costly AI mistakes rather than maximizing throughput on trivial edits.

This is a useful framing for engineers designing agent rules: a behavioral policy should declare what errors it is trying to reduce and what cost it is willing to accept in exchange.

## Training Exercise

Build and evaluate your own project-local agent rule set using this repo as the template.

### Goal

Install the guidance in a small code repository and observe how it changes an agent's coding behavior on an intentionally ambiguous task.

### Step 1: Create a tiny sample project

Create a new directory with a simple function and test target.

```bash
mkdir agent-rules-lab
cd agent-rules-lab
git init
printf 'function sum(a, b) { return a + b; }\nmodule.exports = { sum };\n' > math.js
printf 'const { sum } = require("./math");\nconsole.log(sum(2, 3));\n' > index.js
git add .
git commit -m "initial project"
```

### Step 2: Add the repo's Claude rule file

Copy the rule file into your project.

```bash
curl -o CLAUDE.md https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md
```

If you use Cursor, also create a Cursor rule directory and copy the equivalent rule there.

```bash
mkdir -p .cursor/rules
curl -o .cursor/rules/karpathy-guidelines.mdc https://raw.githubusercontent.com/multica-ai/andrej-karpathy-skills/main/.cursor/rules/karpathy-guidelines.mdc
```

### Step 3: Give the agent an ambiguous task

Ask your coding agent something like:

```text
Improve this project so input handling is safer.
```

Observe whether it:

- asks what kinds of invalid input matter
- proposes tests or verification criteria
- avoids rewriting the whole project
- limits edits to the directly relevant files

### Step 4: Compare against a no-rules baseline

Temporarily rename the rule file and repeat the same prompt.

```bash
mv CLAUDE.md CLAUDE.md.off
```

Run the same task again in a fresh session and compare:

- number of files changed
- amount of code added
- whether clarifying questions are asked
- whether the result includes verification steps

### Step 5: Customize with project-specific constraints

Append your own engineering rules to `CLAUDE.md`.

```markdown
## Project-Specific Guidelines

- Use CommonJS modules only
- Add tests for all bug fixes
- Do not introduce new dependencies
- Preserve existing file structure unless explicitly asked
```

Then ask the agent to perform a concrete change:

```text
Fix sum so non-numeric inputs are rejected. Start by writing a failing test, then make it pass.
```

### Step 6: Evaluate the result

Use this checklist:

- Did the agent convert the request into a verifiable goal?
- Did it avoid speculative abstractions?
- Did it touch only relevant lines?
- Did it explain uncertainty before coding?

### Stretch exercise

Create your own variant of the skill with one additional rule, such as:

- prefer existing utilities over adding helpers
- always list rollback risks before schema changes
- never rename public interfaces unless explicitly requested

Then rerun the same task and note how the behavior changes.

## Test Yourself

<details><summary>What four behavioral principles form the core of the repository&#x27;s agent policy?</summary>

Think before coding, simplicity first, surgical changes, and goal-driven execution. Together, they direct the agent to clarify uncertainty, minimize implementation scope, avoid unrelated edits, and verify results.

</details>

<details><summary>Why is this repository considered configuration and packaging rather than a traditional software library?</summary>

Its primary artifacts are instruction files and tool-specific metadata, not executable business logic or a library API. Those artifacts are installed or copied into coding environments where they influence agent behavior.

</details>

<details><summary>How can you test whether a project-local rule set actually improves agent behavior?</summary>

Run the same ambiguous task in fresh sessions with and without the rules. Compare the number of files and lines changed, whether the agent asks clarifying questions, whether it avoids speculative design, and whether it defines and runs verification checks.

</details>

## Further Reading

- [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)
- [Cursor Rules Documentation](https://docs.cursor.com/context/rules-for-ai)
- [Andrej Karpathy on LLM coding pitfalls](https://x.com/karpathy/status/2015883857489522876)
- [Anthropic Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
