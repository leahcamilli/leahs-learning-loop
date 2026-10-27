---
title: "Branching Workflows with GitHub Copilot CLI Sessions"
source: "https://linkedin.com/posts/burkeholland_you-can-now-fork-conversations-in-the-github-ugcPost-7460074801844383746-VexF?rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY"
date: "2026-05-12"
tags: [github-copilot, cli, ai-workflows, sessions, prompt-engineering]
source_type: "web"
topics: [github-copilot, coding-agents, developer-tools]
kind: "tutorial"
depth: 2
actionability: 3
---

## TL;DR

> GitHub Copilot CLI session forking lets you explore multiple approaches from the same accumulated context without disrupting the original conversation. This makes non-linear engineering work easier to compare and turns exploration into a deliberate step before commitment.

## Key Takeaways

1. Use `/fork` after establishing shared requirements, constraints, risks, and goals, so every alternative starts from the same checkpoint.
2. Direct each fork toward a distinct tradeoff or hypothesis, such as minimizing rollout risk, maximizing implementation speed, or improving long-term architecture.
3. Use `/session` to switch among active conversation branches and compare their outputs without relying on memory or copy-paste.
4. Use `/rename` to give branches descriptive names such as `graphql-low-risk`, `graphql-fastest`, and `graphql-clean-schema`.
5. Evaluate competing branches against consistent criteria, including architecture impact, rollout complexity, operational risk, and monitoring needs.
6. Apply session branching to refactor planning, debugging hypotheses, prompt experiments, implementation tradeoffs, and competing architecture proposals.
7. Continue refining only the most promising branch into an implementation plan or checklist after comparing the alternatives.

## Overview
These notes describe a new GitHub Copilot CLI capability: forking conversations into separate branches and navigating them with session commands. The core idea is to treat AI-assisted work more like version control for reasoning, where one shared context can split into multiple paths for experimentation without losing the original thread.

This matters because engineering work is rarely linear. Tasks like refactoring, debugging, architecture evaluation, and implementation planning often benefit from comparing several approaches in parallel. Conversation branching supports that style directly by preserving context, reducing repetition, and making tradeoff analysis easier.

## Key Concepts
- **Conversation forking**: Forking creates a new conversation branch from the current state of a Copilot CLI session. The new branch inherits prior context, allowing you to explore an alternative path without overwriting or polluting the original discussion.
- **Session switching**: The `/session` command lets you move between active conversation branches. This is useful when comparing outputs from multiple approaches, such as different implementation plans or debugging strategies.
- **Named branches for human tracking**: The `/rename` command helps assign meaningful names to session branches. Clear naming is important because once you start branching heavily, identifiers alone are not enough to remember which session represents which idea.
- **Exploratory AI workflows**: AI-assisted development is often non-linear. Engineers frequently want to test multiple plans, prompts, or constraints, and branching sessions supports this iterative style more naturally than restarting a chat from scratch.
- **Context preservation**: A forked session retains the accumulated context of the original conversation up to the fork point. That means you can keep prior requirements, code snippets, and design constraints while asking the model to pursue a different strategy.
- **Comparative decision-making**: Branching enables side-by-side evaluation of alternatives instead of relying on memory or manual copy-paste. This improves decision quality when choosing among plans for refactors, tests, tooling, or architecture.

## How It Works
The feature behaves like branching in Git, but applied to AI conversation state instead of source code. You start with a base session, establish requirements and constraints, and then fork once there are multiple reasonable directions to explore. Each branch continues independently from the same checkpoint.

A practical workflow is:

1. Start a base Copilot CLI conversation for a concrete task.
2. Clarify constraints, risks, and goals.
3. Use `/fork` when you want to test different strategies.
4. In each branch, prompt Copilot toward a specific tradeoff or hypothesis.
5. Use `/session` to switch among branches.
6. Use `/rename` to label branches clearly.
7. Compare outputs and continue with the most promising path.

The main benefit is separating exploration from commitment. In a normal linear chat, changing direction can create confusion, introduce contradictory assumptions, or force you to restate context. Forking avoids that by keeping a clean shared starting point while letting each branch diverge intentionally.

This is especially useful for:
- refactor planning with multiple strategies
- debugging with competing root-cause hypotheses
- testing alternate prompt styles
- comparing implementation tradeoffs
- drafting competing architecture proposals

A simple example from the notes is a migration from REST to GraphQL:
- Base session: plan the migration
- Fork A: optimize for minimal risk and incremental rollout
- Fork B: optimize for speed of implementation
- Fork C: optimize for long-term schema clarity

Because all branches share the same starting context, comparisons are more reliable and require less repetition. Naming branches like `graphql-low-risk`, `graphql-fastest`, and `graphql-clean-schema` makes the workflow easier to manage once several branches exist.

The training exercise extends this into a repeatable decision workflow. For example, when adding caching to a slow Node.js endpoint, you can branch into plans optimized for speed, safety, and scalability, then compare architecture impact, rollout complexity, operational risk, and monitoring needs before selecting one branch to refine into an implementation checklist.

## Test Yourself

<details><summary>Why should a Copilot CLI conversation be forked instead of simply changing direction in the existing session?</summary>

A fork preserves the original discussion while creating an independent path that inherits all context up to the fork point. This prevents conflicting assumptions from polluting a linear conversation and makes alternatives easier to compare.

</details>

<details><summary>What roles do `/fork`, `/session`, and `/rename` play in a branching workflow?</summary>

`/fork` creates an alternative conversation from the current state, `/session` switches between branches, and `/rename` assigns meaningful labels that make multiple experiments easier to track.

</details>

<details><summary>How could session branching support a REST-to-GraphQL migration decision?</summary>

Start with one session containing the migration requirements, then create separate branches optimized for low-risk incremental rollout, implementation speed, and long-term schema clarity. Compare them using the same criteria before refining the strongest approach.

</details>

## Personal Notes
Branching Workflows with GitHub Copilot CLI Sessions

Source: https://www.linkedin.com/posts/burkeholland_you-can-now-fork-conversations-in-the-github-ugcPost-7460074801844383746-VexF?utm_source=social_share_send&utm_medium=ios_app&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY&utm_campaign=share_via
Notion page: https://www.notion.so/Branching-Workflows-with-GitHub-Copilot-CLI-Sessions-35e01bb0839a8102bf31c187c871df47

Tags: github-copilot, cli, ai-workflows, sessions, prompt-engineering

Overview

GitHub Copilot CLI now supports forking conversations, which gives engineers a branching workflow for AI-assisted work. Instead of forcing a single linear chat history, you can split a conversation into multiple alternative paths, explore different implementation ideas, and later switch among them using session management commands.

This matters for practical engineering work because many tasks are inherently exploratory: planning a refactor, comparing architectural options, debugging with different hypotheses, or drafting multiple automation approaches. Conversation forking makes Copilot CLI feel more like version control for reasoning, helping you preserve context while testing divergent directions without losing your original thread.

Key Concepts

  *   Conversation forking: Forking creates a new conversation branch from the current state of a Copilot CLI session. The new branch inherits prior context, allowing you to explore an alternative path without overwriting or polluting the original discussion.
  *   Session switching: The /session command lets you move between active conversation branches. This is useful when comparing outputs from multiple approaches, such as different implementation plans or debugging strategies.
  *   Named branches for human tracking: The /rename command helps assign meaningful names to session branches. Clear naming is important because once you start branching heavily, identifiers alone are not enough to remember which session represents which idea.
  *   Exploratory AI workflows: AI-assisted development is often non-linear. Engineers frequently want to test multiple plans, prompts, or constraints, and branching sessions supports this iterative style more naturally than restarting a chat from scratch.
  *   Context preservation: A forked session retains the accumulated context of the original conversation up to the fork point. That means you can keep prior requirements, code snippets, and design constraints while asking the model to pursue a different strategy.
  *   Comparative decision-making: Branching enables side-by-side evaluation of alternatives instead of relying on memory or manual copy-paste. This improves decision quality when choosing among plans for refactors, tests, tooling, or architecture.

How It Works

The source describes a new workflow feature in GitHub Copilot CLI: the ability to **fork conversations** and later move among them with **/session**. Conceptually, this works like branching in Git, but for the state of an AI conversation rather than for source code. You begin with a base interaction, establish context, constraints, and goals, and then split that thread when you want to pursue multiple possible directions.

A typical flow looks like this:

1. Start a conversation in Copilot CLI around a concrete engineering task. 2. Reach a point where there are multiple valid next steps. 3. Use `/fork` to create an alternate branch of the conversation. 4. In each branch, ask Copilot to pursue a different strategy. 5. Use `/session` to switch between branches. 6. Use `/rename` to give each branch a meaningful label. 7. Compare results and continue with the best path.

This is especially useful when the model's usefulness depends on accumulated context. In a normal single-thread chat, changing direction can contaminate the session with contradictory assumptions or force you to restate earlier requirements. Forking avoids that by preserving the shared context up to a checkpoint, then letting each branch diverge independently.

Here is a practical example:

- Base session: "Help me plan a migration from REST endpoints to GraphQL in this service." - Fork A: "Optimize for minimal delivery risk and incremental rollout." - Fork B: "Optimize for fastest implementation." - Fork C: "Optimize for long-term schema clarity and client ergonomics."

All three branches start with the same project context, but each evolves toward a different engineering tradeoff. Later, `/session` lets you hop among them and inspect the outputs before choosing one to refine.

The recommendation to use `/rename` is operationally important. Once you have several forks, branch management becomes a usability problem. Renaming sessions to something like `graphql-low-risk`, `graphql-fastest`, or `graphql-clean-schema` makes the workflow much easier to navigate and turns session history into a durable working set rather than a pile of anonymous branches.

From a reasoning standpoint, the main value is that it separates **exploration** from **commitment**. You can explore multiple hypotheses without losing the original line of thought. That is valuable in tasks such as:

- planning a refactor in several ways - debugging with different root-cause theories - trying alternate prompts for code generation - evaluating multiple test strategies - drafting competing architectural proposals

Although the source is a short product announcement rather than a full technical spec, the underlying interaction model is clear: Copilot CLI is adding stateful conversation management primitives that make iterative engineering work more structured. The commands mentioned imply a lightweight session graph where one prompt history can branch into several descendants, and users can navigate those branches intentionally instead of relying on one long chat log.

Training Exercise

Create a small decision-making workflow using forked Copilot CLI sessions.

### Goal Use conversation branching to compare three different implementation plans for the same task.

### Scenario You need to add caching to a
