---
title: "Designing Effective Claude Code Skills from a Documentation-First Repo"
source: "https://github.com/shanraisshan/claude-code-best-practice/blob/main/tips/claude-thariq-tips-17-mar-26.md"
date: "2026-08-03"
tags: [agent-workflows, prompt-engineering, developer-tools, knowledge-management]
source_type: "github"
source_fingerprint: "d9adf4c3a0"
source_characters: 80000
topics: [claude, coding-agents, ai-agents, prompt-engineering]
kind: "tutorial"
depth: 2
actionability: 3
---

## TL;DR

> Design Claude Code skills as reusable folders with clear trigger conditions, outcome-focused guidance, and progressively loaded supporting assets. This matters because concise constraints, known failure modes, and isolated execution can improve reliability without bloating the main context.

## Key Takeaways

1. Write the skill description as a condition for when the skill should run, not as a general summary of its contents.
2. Organize each skill around `.claude/skills/<name>/SKILL.md`, with optional `references/`, `scripts/`, and `examples/` directories for supporting material.
3. Specify the goal, constraints, outputs, and failure modes; avoid rigidly scripting obvious steps that the model can determine itself.
4. Add a `Gotchas` section to every skill and update it with recurring mistakes and high-signal failure cases.
5. Use progressive disclosure so detailed references, scripts, and examples enter context only when they are relevant.
6. Use `context: fork` for workflows with substantial searches, tool output, or dead ends so the main session receives the result without all intermediate context.
7. Treat the folder structure as documented recommended practice: the README names `.claude/skills/<name>/SKILL.md`, but the supplied repository tree does not show that directory in this snapshot.

## Overview

This lesson distills what the supplied repository explicitly shows about Claude Code skills. The strongest evidence comes from the README’s architecture tables, the skills tips attributed to Thariq on March 17, 2026, and the repository file tree. The repo is documentation-first: it includes `best-practice/`, `implementation/`, `reports/`, and `tips/` directories plus `.claude/agents`, `.claude/commands`, `.claude/rules`, hooks, and config files. The README says skills live at `.claude/skills/<name>/SKILL.md`, but that folder is not visible in the provided file tree, so treat skill structure guidance here as recommended practice documented by the repo rather than an observed implemented skill directory in this snapshot.

## Key Concepts

- **Skills as structured folders**: The source says skills are folders, not single files. A skill is centered on `SKILL.md` and may include subdirectories like `references/`, `scripts/`, and `examples/` for progressive disclosure.
- **Progressive disclosure**: A recurring theme is to give the model targeted supporting material only when relevant. The repo links this idea to skills and recommends subfolders and embedded assets so the model can use existing context, scripts, and examples instead of reconstructing them.
- **Skill triggers are operational**: The source says the skill description field should be written as a trigger condition, not as a summary. In practice, that means describing when the skill should fire, so invocation becomes more reliable.
- **Goals and constraints over rigid procedures**: Thariq’s tips explicitly advise against over-explaining obvious steps and against railroading the model. The lesson is to specify the outcome, constraints, and failure modes rather than a brittle step-by-step script.
- **Gotchas as high-signal memory**: The source recommends a 'Gotchas' section in every skill. Its purpose is to accumulate known failure points over time, making the skill more durable and more useful than a generic instruction file.
- **Context isolation with skills**: The README’s skills tips mention `context: fork`, which runs a skill in an isolated subagent so the main context receives the result rather than all intermediate tool output. This is presented as a way to keep the primary session cleaner.

## How It Works

Start by framing a skill as a reusable unit for a repeated workflow. According to the source, the recommended pattern is: define a clear trigger in the skill description, store the skill as a folder with `SKILL.md`, and add only the non-obvious guidance that changes model behavior. Put detailed domain references, reusable scripts, and examples in subfolders so the model can pull them in progressively. Add a 'Gotchas' section to capture mistakes the model keeps making. When a task would otherwise flood the main session with searches and dead ends, use isolated execution patterns such as `context: fork` so only the conclusion returns. In the supplied repo, this skill philosophy sits inside a broader architecture of commands, agents, rules, hooks, reports, and implementation notes, which reinforces that skills are one primitive in a larger workflow system rather than a standalone magic file.

## Training Exercise

Draft a skill for a workflow you repeat often, such as release verification or bug triage. Write a one-paragraph trigger description that says when the skill should be used. Then outline a `SKILL.md` with four sections: goal, constraints, gotchas, and outputs. Add three supporting assets you would want in a real folder structure: one reference note, one script, and one example. Finally, revise the skill by deleting any obvious instructions and replacing them with one or two high-signal failure cases the model should avoid.

## Test Yourself

<details><summary>How should a skill description be written to improve invocation reliability?</summary>

Write it as an operational trigger that states when the skill should be used. The source advises against treating the description as merely a summary of the skill's contents.

</details>

<details><summary>What belongs in a skill folder besides `SKILL.md`, and why?</summary>

The documented pattern allows `references/`, `scripts/`, and `examples/` directories. These assets support progressive disclosure by supplying detailed context or reusable work only when it is needed.

</details>

<details><summary>Why does the source recommend a `Gotchas` section and `context: fork`?</summary>

A `Gotchas` section preserves recurring failure cases so the skill improves over time. The README presents `context: fork` as a way to isolate noisy execution and return only the result to the main context.

</details>

## Further Reading

- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Lessons from Building Claude Code: How We Use Skills (Thariq)](https://x.com/trq212/status/2033949937936085378)
- [Skills for Mono-repos](reports/claude-skills-for-larger-mono-repos.md)
- [Official Skills](https://github.com/anthropics/skills/tree/main/skills)
