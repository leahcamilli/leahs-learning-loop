---
title: "Building Durable Agent Instructions and Skills for Faster, Safer Development"
source: "https://www.youtube.com/watch?v=e1snsuY4lTI"
date: "2026-08-11"
tags: [ai-agents, developer-workflows, prompt-engineering, knowledge-management, typescript]
source_type: "youtube"
source_fingerprint: "bd00a09f14"
source_characters: 59212
channel: "Theo - t3․gg"
published: "2026-08-10"
duration_seconds: 3075
topics: [ai-agents, prompt-engineering, coding-agents, context-engineering]
kind: "tutorial"
depth: 2
actionability: 3
---

## TL;DR

> Treat agent instructions and skills as maintainable infrastructure: encode recurring preferences and observed failure modes, then refine them through real work. Theo reports that this makes coding agents faster, safer, and easier to collaborate with, though the evidence presented is experiential rather than experimental.

## Key Takeaways

1. Build global instruction files around durable cross-project defaults such as simplicity, destructive-action safety, proportionate verification, code style, and communication—not repository discovery.
2. Write skill descriptions as intent-based triggers, such as “use when the user asks to file, open, or create a PR,” and keep the detailed workflow inside the skill body.
3. Audit the last 10–20 agent-driven tasks to identify repeated failures before adding rules; useful evidence includes thread histories, shell logs, PRs, review comments, and recurring corrections.
4. Separate skills when their triggers and goals differ—for example, filing a PR and babysitting an existing PR require different workflows and scope controls.
5. Add project-level glossaries, architectural boundaries, supported surfaces, contract locations, and non-negotiables so the agent knows what must remain consistent.
6. Turn concrete local risks into narrow guardrails, including process management, dev servers, credentials, cross-surface updates, verification, and preventing review feedback from expanding scope.
7. Do not copy another person’s setup wholesale; observe your own workflows and encode only rules that address recurring problems you actually experience.

## Overview

This lesson teaches a practical method for improving coding-agent performance by treating instruction files and skills as maintainable infrastructure. In the source, Theo reports large productivity gains after rewriting global agent instructions, adding task-specific skills, auditing real agent histories, and tuning project-level guidance for T3 Code. The core idea is not to build a perfect universal prompt, but to iteratively encode recurring preferences, failure modes, and communication patterns so agents behave more predictably across machines and repositories. Evidence is experiential rather than experimental: the transcript provides concrete examples and observed outcomes, but not controlled benchmarks.

## Key Concepts

- **Instruction Files Are Operational Defaults**: Global files like `AGENTS.md` or `CLAUDE.md` should encode durable defaults: coding preferences, safety boundaries, verification habits, and communication style. They are not README replacements and should be optimized for how an agent should work, not for how a human should discover the project.
- **Skills Should Trigger on Intent, Not Explain Everything**: A skill description should mainly help the agent decide when to load the skill. In the source, descriptions improved when rewritten as trigger phrases such as 'use when the user asks to file, open, or create a PR' rather than long explanations of behavior.
- **Audit Real Histories to Find Failure Modes**: Instead of guessing what to fix, inspect past threads, tool use, PR behavior, and repeated corrections. The source highlights failures like unnecessary draft PRs, overbuilding, killing the wrong processes, weak verification, and scope creep, then turns those observations into explicit instructions.
- **Write for Communication, Not Just Code Generation**: Many of the reported gains came from making agents easier to work with, not just more technically capable. Examples include better PR titles and descriptions, adding model/harness notes to PRs, generating readable HTML artifacts, and uploading videos or files so humans can review outcomes quickly.
- **Project Glossaries and Non-Negotiables Reduce Drift**: Project-level instruction files should define shared terms, architectural boundaries, supported surfaces, and constraints that must not be compromised. In the T3 Code example, the glossary clarifies terms like provider, client, environment, and project, while non-negotiables include performance, openness, and remote-ready behavior.
- **Guardrails Should Match Common Local Failures**: Good rules are specific to actual damage patterns. The source adds guardrails for dev servers, process management, local credentials, reverse states, multi-surface support, contracts, and documentation splits because those were the places agents repeatedly caused trouble.
- **Do Not Blindly Copy Another Person's Setup**: The transcript explicitly warns against copying someone else's global instructions or skills wholesale. The value lies in the process: observe your own workflows, identify recurring pain, and encode only the rules that solve your real problems.

## How It Works

Start with the problems you repeatedly see in real agent sessions. Collect examples from thread history, PRs, shell logs, and review comments. Group them into categories such as unsafe process handling, poor PR hygiene, overengineering, weak TypeScript style, or missing cross-surface updates. Convert the stable patterns into three layers of guidance.

First, create a small global instruction file for cross-project defaults. Keep it focused on durable preferences: simplicity, safety around destructive actions, when to verify, how much testing is appropriate, and what counts as good code style.

Second, create task-specific skills for recurring jobs. Split skills when the trigger and goal differ, such as 'file PR' versus 'babysit PR.' Make the description mostly about when to activate the skill. Put the detailed workflow inside the skill body: what to check first, what to avoid, how to report, and how to keep scope under control.

Third, add project-level instructions that describe the system in agent-friendly terms. Define a glossary, list supported surfaces or adapters, call out where contracts live, explain what must stay in sync, and note the local-development traps most likely to waste time or break the environment.

Then test the setup on real work, not toy prompts. Watch for where the agent still overbuilds, stops early, misses an adapter, files vague PRs, or communicates badly. Update the files with narrow, evidence-backed changes. The transcript's examples show that even short additions, such as 'questions are read only' or 'do not let review feedback expand the PR beyond the user's original goal,' can materially change behavior.

## Training Exercise

Pick one repository you use often and review your last 10-20 agent-driven tasks. Write down 5 recurring failures or annoyances. Create:
1. A global instruction file with 6-10 durable defaults.
2. Two small skills for repeated tasks, each with a trigger-oriented description.
3. A project instruction file with a glossary, 3 non-negotiables, and one checklist for areas that must stay in sync.

Next, run one real task using the new setup. Afterward, compare the result against a recent older task. Evaluate four things: prompt length, number of corrective messages you had to send, clarity of the final PR or summary, and whether the agent avoided the failure modes you targeted. Revise only the rules that clearly helped or clearly failed.

## Test Yourself

<details><summary>What belongs in global instructions rather than a task-specific skill or project instruction file?</summary>

Global instructions should contain durable defaults that apply across projects, such as safety boundaries, simplicity preferences, verification habits, code style, and communication expectations. Task workflows belong in skills, while repository-specific terminology and constraints belong in project instructions.

</details>

<details><summary>Why should a skill description focus on trigger phrases?</summary>

Its primary purpose is to help the agent decide when the skill should be loaded. Detailed checks, cautions, and workflow steps can then live in the skill body without making activation ambiguous.

</details>

<details><summary>How should you evaluate whether new agent guidance is helping?</summary>

Run it on a real task and compare it with an older task using prompt length, corrective-message count, final PR or summary clarity, and avoidance of targeted failure modes. Revise only rules that clearly helped or failed.

</details>
