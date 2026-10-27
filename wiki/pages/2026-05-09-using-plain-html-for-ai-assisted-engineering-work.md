---
title: "Using Plain HTML for AI-Assisted Engineering Work"
source: "https://thariqs.github.io/html-effectiveness"
date: "2026-05-09"
tags: [html, prototyping, engineering-workflows, visualization, ux]
source_type: "web"
topics: []
kind: "opinion"
depth: 2
actionability: 3
---

## TL;DR

> Plain HTML can make AI-assisted engineering work easier to understand and act on because it preserves spatial layout, visual hierarchy, and lightweight interactivity. A self-contained HTML artifact can function as both a thinking surface and a disposable, task-specific interface that feeds decisions into the next step.

## Key Takeaways

1. Use a single self-contained HTML file with inline CSS and light JavaScript when a task is difficult to understand as linear prose.
2. Match the layout to the work: tables for trade-offs, SVG for diagrams, tabs for alternatives, timelines for incidents, and collapsibles for secondary details.
3. Present multiple concrete options side by side so engineers can compare trade-offs directly instead of reconstructing them from prose.
4. Build narrow, temporary interfaces for tasks such as implementation planning, PR review, incident analysis, feature-flag editing, or prompt tuning.
5. Include a copy, export, or editable-output path so decisions can move into a PR, source control, or the next AI prompt.
6. Judge the artifact by whether another engineer can quickly identify its purpose, main components, risks, and next actions.

## Overview
These notes capture a practical lesson: plain HTML can be a much better medium than markdown or prose for many AI-assisted engineering tasks. The core argument is that HTML preserves spatial layout, visual hierarchy, and lightweight interactivity, making plans, reviews, diagrams, reports, and prototypes easier to scan and act on.

This matters because a lot of engineering work is not fundamentally linear. Comparing alternatives, reviewing diffs, understanding architecture, triaging tickets, or tuning prompts often benefits from side-by-side structure, callouts, controls, and diagrams. A self-contained HTML file can serve as both a communication artifact and a disposable task-specific interface that improves clarity and speeds iteration.

## Key Concepts
- **HTML as a working artifact**: Treat HTML as a fast, flexible medium for thinking and collaboration, not just final publishing.
- **Spatial information beats linear text**: Layout, grouping, and side-by-side comparison reduce cognitive load for inherently visual or relational tasks.
- **Multiple concrete options**: HTML makes it easy to present alternatives in parallel so teams can compare trade-offs directly.
- **Low-friction interactivity**: Tabs, collapsibles, sliders, and clickable flows can turn a static answer into a usable tool.
- **Artifacts that feed the next prompt**: HTML outputs can be copied, exported, edited, and reused as inputs in iterative AI workflows.
- **Throwaway interfaces for narrow tasks**: A temporary UI tailored to a specific task can be more effective than forcing everything through chat.

## How It Works
The notes describe HTML as a high-leverage output format when asking AI to generate something more structured than prose. Instead of producing another text document, the AI creates a single-file HTML artifact with inline CSS and light JavaScript. That artifact can encode summaries, comparisons, diagrams, timelines, tables, and controls in a way that matches how engineers actually inspect and make decisions.

A useful pattern is to start with a task that is difficult to understand in plain text, then ask for a self-contained HTML page optimized for scanning. The structure should fit the task: tables for trade-offs, SVG for diagrams, tabs for alternatives, timelines for incidents, and collapsibles for secondary detail. Keeping everything in one file makes the artifact cheap to generate, easy to open locally, and easy to share.

The examples in the notes span several engineering workflows:

- **Exploration and planning**: implementation plans, visual alternatives, milestone timelines, architecture diagrams, and risk tables.
- **Code review and understanding**: annotated PRs, reviewer-focused summaries, module maps, and highlighted hot paths.
- **Design and prototyping**: design token viewers, component variant matrices, animation sandboxes, and clickable flows.
- **Diagrams and explainers**: SVG-based figures, flowcharts, mini slide decks, glossary-driven explainers, and tabbed concept pages.
- **Reports and custom editors**: incident timelines, status reports, triage boards, feature flag editors, and prompt tuning tools.

A recurring theme is the **export path**. The HTML artifact should not just look good; it should help the next step happen. That might mean a copyable summary, markdown export, or editable output that can be moved into a PR, source control, or another AI prompt. This turns HTML into both a thinking surface and a bridge between decision-making and execution.

The notes also include a concrete prompt pattern: ask for a single self-contained HTML file for a task, include a clear summary, optimize the layout for scanning, include the key comparisons or controls, keep CSS and JS inline, and provide an export or copy mechanism if decisions need to be reused.

The training exercise reinforces the idea with two practical options:
- Build an **implementation plan page** with a summary, timeline, architecture or data-flow diagram, risks table, and open questions.
- Build a **PR review page** with summary, file-by-file changes, highlighted risky areas, reviewer focus points, and anchors for navigation.

The success criteria are simple and useful: another engineer should quickly understand what the artifact is for, what the main moving parts are, where the risks are, and what should happen next.

## Test Yourself

<details><summary>Why can plain HTML be more effective than markdown or prose for some AI-assisted engineering tasks?</summary>

The lesson argues that many engineering tasks are spatial or relational rather than purely linear. HTML can express grouping, side-by-side comparisons, diagrams, callouts, and controls, reducing the effort needed to understand and act on the information.

</details>

<details><summary>What makes a self-contained HTML artifact practical for iterative engineering work?</summary>

Keeping CSS and JavaScript inline makes the artifact inexpensive to generate, easy to open locally, and simple to share. Adding copy or export features also lets its conclusions become inputs to later prompts, PRs, or source-controlled documents.

</details>

<details><summary>What should an engineer include when asking AI to create an HTML working artifact?</summary>

Specify a single self-contained file, a clear summary, a scan-friendly layout, and the comparisons, diagrams, or controls appropriate to the task. Include an export or copy mechanism when the artifact's decisions need to be reused.

</details>

## Personal Notes
Using Plain HTML as a High-Leverage Medium for AI-Assisted Engineering Work

Source: https://thariqs.github.io/html-effectiveness/
Notion page: https://www.notion.so/Using-Plain-HTML-as-a-High-Leverage-Medium-for-AI-Assisted-Engineering-Work-35b01bb0839a81e080e5c29674ae0c8c

Tags: html, ux, engineering-workflows, prototyping, visualization

Overview

This article argues that plain HTML is an unusually powerful output format for AI-assisted engineering tasks because it preserves spatial structure, interactivity, and visual hierarchy that markdown and linear text often lose. Instead of asking an agent to produce another wall of prose, you can ask it to generate a single self-contained HTML artifact that makes trade-offs, diagrams, plans, diffs, prototypes, or reports immediately scannable and actionable.

The material is relevant to engineers, tech leads, designers, and anyone using AI tools for planning, review, documentation, or communication. The core idea is practical: many work products are easier to understand when rendered as boxes, timelines, tables, tabs, callouts, and small interactive controls. HTML is cheap to generate, easy to open locally, and can act as both a communication format and a lightweight interface for refining ideas.

Key Concepts

  *   HTML as a working artifact: The article treats HTML not as a final publishing format but as a fast, flexible medium for thinking and collaboration. A single file can combine layout, styling, interactivity, and copyable content in a way that is much closer to how engineers actually inspect plans, diffs, flows, and designs.
  *   Spatial information beats linear text: Many engineering problems are inherently spatial: code diffs, module relationships, timelines, variant matrices, and flow diagrams all benefit from side-by-side comparison and visual grouping. Markdown tends to flatten these structures into a sequential reading experience, which increases cognitive load.
  *   Exploration through multiple concrete options: When requirements are fuzzy, generating several alternatives at once helps teams compare approaches directly instead of mentally juggling separate descriptions. HTML makes this easy by placing options in parallel cards, panels, or sections with trade-offs inline.
  *   Low-friction interactivity: Simple controls like tabs, sliders, collapsible sections, and clickable flows can make an explanation dramatically more useful. The article emphasizes that even lightweight JavaScript can turn a static answer into a tool for learning, review, or tuning.
  *   Artifacts that feed the next prompt: An HTML output is not only something to read; it can become the next input to an iterative workflow. Design tokens, implementation plans, prompt templates, or edited triage results can be copied, exported, or refined further, tightening the loop between human judgment and AI generation.
  *   Throwaway interfaces for narrow tasks: Instead of forcing every task through a chat box, you can generate a temporary UI tailored to the job at hand. Examples like ticket triage, feature flag editing, and prompt tuning show how a bespoke micro-interface can reduce ambiguity and speed decision-making.

How It Works

The article is organized as a gallery of example HTML artifacts, grouped by engineering use case. Its central claim is that AI becomes more effective when asked to produce interfaces and structured documents rather than only prose. Each example demonstrates a task where HTML's native strengths—layout, typography, forms, links, tables, SVG, and modest JavaScript—create a clearer and more useful result.

A useful way to read the examples is by mapping them to common engineering workflows:

1. **Exploration and planning** - Side-by-side code approaches - Visual design directions - Implementation plan with milestones, diagrams, risky code, and risk tables

These examples show how HTML helps when the team does not yet know the answer. Instead of a linear brainstorm, the agent can present multiple candidate solutions at once. The reader can compare trade-offs visually, choose a direction, and then convert that choice into a structured implementation plan.

2. **Code review and understanding** - Annotated pull request - Reviewer-focused PR writeup - Module map with hot paths and entry points

Here the article highlights a mismatch between text-based tooling and code comprehension. A diff is easier to scan when rendered with margin notes, severity tags, and jump links. An unfamiliar module becomes easier to understand when drawn as boxes and arrows rather than described paragraph by paragraph.

3. **Design and prototyping** - Living design system from tokens - Component variant contact sheet - Animation sandbox - Clickable flow prototype

These examples use HTML as a lightweight design surface. Tokens become visible swatches; component states become reviewable matrices; interaction ideas become clickable pages. The insight is that many design decisions need to be seen or felt, not merely described.

4. **Diagrams, decks, and explainers** - Inline SVG figures - Flowcharts with annotations - Arrow-key slide deck - Feature and concept explainers with glossary, tabs, and collapsibles

HTML also serves as a thin presentation layer. Because browsers already support SVG, keyboard navigation, and semantic sections, an agent can generate diagrams and decks without requiring a specialized toolchain.

5. **Reports and custom editors** - Weekly status report - Incident timeline - Ticket triage board - Feature flag editor - Prompt tuner

This category extends the idea from 'document' to 'task-specific UI.' The most important pattern is the presence of an **export path**: after interacting with the artifact, the user should be able to copy markdown, a diff, or another textual representation back into source control or an AI prompt.

The article's practical reasoning can be summarized as a
