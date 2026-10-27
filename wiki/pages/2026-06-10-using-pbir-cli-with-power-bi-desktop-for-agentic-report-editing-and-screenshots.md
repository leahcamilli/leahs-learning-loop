---
title: "Using pbir-cli with Power BI Desktop for Agentic Report Editing and Screenshots"
source: "https://www.linkedin.com/posts/kurtbuhler_microsoftfabric-powerbi-agenticdevelopment-ugcPost-7470590768936628224-UsjC/?utm_source=social_share_send&utm_medium=ios_app&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY&utm_campaign=share_via"
date: "2026-06-10"
tags: [powerbi, microsoft-fabric, cli, agentic-development, automation]
source_type: "web"
topics: [ai-agents, automation-workflows, developer-tools]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> Use `pbir-cli` as the execution layer for programmatic Power BI report edits, while an agent skill supplies the workflow, safeguards, and context. The source argues that combining this separation with Power BI Desktop’s preview integration enables a fast edit-refresh-screenshot validation loop.

## Key Takeaways

1. Treat `pbir-cli` as a low-level editing tool, not as an agent, skill, or report-design framework.
2. Put governance, best practices, task routing, and reusable procedures in the skill or human-review layer rather than expecting the CLI to enforce them.
3. Create a backup before destructive operations such as removing visuals or deleting report pages.
4. Constrain every edit by identifying the open report, target page, affected visuals, and intended formatting changes.
5. Validate visual changes with the closed loop: edit, refresh the Power BI Desktop canvas, capture a screenshot, and inspect the result.
6. Resolve ambiguous page names or visual descriptions before execution instead of allowing the agent to guess.
7. The source recommends treating `pbir-cli` and Desktop’s external interaction capability as development tools while they remain beta and preview features, rather than depending on them in a hardened production pipeline before `1.0.0`.

## Overview

This lesson explains a newly described workflow for automating Power BI report editing through `pbir-cli`, a community CLI tool that can now interact with Power BI Desktop via a Microsoft preview feature for external tools. The source material focuses on agentic development, where an AI agent uses scripted skills to inspect, modify, refresh, and screenshot an open report canvas, but the same tool can also be used manually or from automation.

This matters to engineers building BI developer tooling, report refactoring workflows, or AI-assisted analytics experiences. The key idea is to separate the execution tool (`pbir-cli`) from the agent or skill layer that teaches an AI how to use it, while taking advantage of Power BI Desktop's new external interaction capability for faster visual iteration.

## Key Concepts

- **pbir-cli as an execution tool**: `pbir-cli` is presented as a command-line tool for programmatically modifying Power BI reports. It is not itself an agent, a skill, or an opinionated reporting framework; instead, it acts as the low-level mechanism an engineer or AI system can invoke to inspect and change report artifacts.
- **Agent skills as usage guidance**: The source distinguishes between the CLI and the optional skill layer that helps an AI agent use the CLI correctly. Skills encode workflows, scripts, and patterns so the agent can perform tasks like backups, page cleanup, visual removal, and formatting changes with less prompt ambiguity.
- **External tools integration with Power BI Desktop**: A new preview feature in Power BI Desktop allows external tools to interact with the open desktop application. This enables scenarios such as refreshing the report canvas and taking screenshots, which are especially useful for iterative validation of visual changes.
- **Agentic development for BI artifacts**: Agentic development here means using an AI assistant to carry out concrete report-editing tasks over a live Power BI report. Rather than only generating suggestions, the agent can search for the open report, make changes, refresh the canvas, and verify results visually.
- **Separation of tool, workflow, and policy**: The post explicitly notes that `pbir-cli` does not provide rules or opinions about how Power BI reports should be designed. That separation is important architecturally: the tool edits artifacts, while governance, best practices, and orchestration live in higher-level skills or human review processes.
- **Beta maturity and operational limits**: The tool is still described as beta, and the new desktop interaction capability has meaningful limitations. Practically, that means engineers should treat this workflow as a fast-moving development aid rather than a stable enterprise pipeline dependency until the tool reaches a more mature release.

## How It Works

The source describes a layered workflow for AI-assisted Power BI development.

At the bottom is **Power BI Desktop**, where a report is already open. Microsoft has added a **preview external tools feature** that lets tools outside Desktop interact with the running application. This is the enabling capability that makes live refreshes and screenshots possible.

On top of that sits **`pbir-cli`**, a community CLI utility for programmatic report modification. The post is careful to clarify that the CLI is just a tool. It can be used:

- manually by a developer
- by automation scripts
- by an AI agent through a skill layer

Then comes the **skill layer** for agentic development. The skill teaches the agent how to invoke the CLI, how to sequence operations safely, and how to apply patterns such as taking a backup before editing. In other words, the skill is not doing the editing itself; it is providing a structured operating manual for the agent.

A typical flow implied by the demo prompt looks like this:

1. **Locate the open Power BI Desktop session**
   - The prompt explicitly tells the agent to search for Power BI Desktop first.
   - This matters because the tool is acting against a live report context, not only static files.

2. **Create a backup**
   - The user instructs the agent to take a backup first.
   - This is an important safety pattern whenever a tool is making destructive edits like deleting visuals or pages.

3. **Target a specific report and page**
   - The example references a report named `Data Goblins Flash Report`.
   - The requested modifications are scoped to the `Co-Creation` page.

4. **Modify visuals programmatically**
   - Remove the waterfall visual.
   - Remove the labels above that waterfall.
   - Remove the neighboring combo chart.
   - Change all bar charts from beige to blue.
   - Delete all pages except the target page.

5. **Refresh and validate the canvas**
   - With the new preview capability, the external tool can refresh the Power BI canvas.
   - It can also capture a screenshot, giving the agent or developer visual confirmation that the edits were applied as intended.

This creates a closed-loop development workflow: **edit -> refresh -> screenshot -> inspect**. For visual analytics work, that loop is especially valuable because correctness is not only structural but also visual.

The source also hints at an architectural evolution in the skills themselves. The author mentions moving away from passive, prescriptive workflows toward more active context management with routing and reusable patterns. That suggests a future design where:

- the engineer owns the task context and constraints
- the AI updates or enriches that context
- the skill routes the task to the right workflow or script
- the CLI executes the concrete report changes

From an engineering perspective, this is a useful separation of concerns:

- **Power BI Desktop** provides the live report surface.
- **Microsoft's preview feature** exposes external interaction points.
- **`pbir-cli`** performs report operations.
- **Skills** provide task recipes and context shaping.
- **The agent** interprets user intent and chooses the right sequence.

Because the tool is beta and the feature is preview, this setup is best viewed as a development and experimentation workflow rather than a hardened production pipeline. The post explicitly says pipeline use is possible but not recommended until the tool reaches `1.0.0`.

A practical mental model is:

```text
User request
  -> agent prompt interpretation
  -> skill-selected workflow/scripts
  -> pbir-cli commands
  -> Power BI Desktop external tool interaction
  -> refresh/screenshot for verification
```

That model helps explain why this is interesting beyond AI hype: it gives BI engineers a programmable interface for repetitive visual refactoring tasks while preserving the option to run the same underlying tool manually.

## Training Exercise

Build a small validation workflow for AI-assisted Power BI editing using the concepts from the source.

### Goal
Simulate a safe report-editing loop where you prepare a report for automated changes, make a scoped visual cleanup, and verify the result with a refresh and screenshot step.

### Prerequisites
- Power BI Desktop installed
- Access to a sample `.pbix` report with multiple pages and several visuals
- `uv` installed
- Ability to enable the Power BI Desktop preview feature for external tools, if available in your environment
- `pbir-cli` installed

Install the CLI:

```bash
uv tool install pbir-cli
```

### Steps
1. **Open a sample report in Power BI Desktop**
   - Choose a report with at least two pages.
   - Ensure one page has multiple visuals, including at least one bar chart.

2. **Enable the preview external tool capability**
   - In Power BI Desktop, turn on the relevant preview feature if your build exposes it.
   - Restart Desktop if required.

3. **Create a manual safety checkpoint**
   - Save a copy of the report as `sample-report-backup.pbix`.
   - Write down the target page name you plan to edit.

4. **Define a constrained edit request**
   Use a prompt like this with your agent or as a manual checklist:

   ```text
   Find the open Power BI Desktop report. Take a backup first. On the page named "Overview", remove one selected visual, change all bar charts to blue, and delete every other page except "Overview". Then refresh the canvas and capture a screenshot.
   ```

5. **Execute the task through your chosen path**
   - If using an agent, let the skill route the task to `pbir-cli`.
   - If working manually, use the CLI capabilities available in your environment to inspect the report structure and apply equivalent changes.

6. **Validate the result**
   - Confirm only the target page remains.
   - Confirm the intended visual is removed.
   - Confirm bar chart colors changed.
   - Refresh the canvas.
   - Capture a screenshot and compare it to the original layout.

7. **Reflect on failure modes**
   Document answers to these questions:
   - What happens if the page name is ambiguous?
   - What if multiple visuals match the same description?
   - What if the preview feature is disabled or unsupported?
   - What metadata or context would make the automation safer?

### Stretch exercise
Design your own skill contract for this workflow. Write a short specification that requires the agent to always:

- locate Power BI Desktop first
- create a backup before destructive changes
- summarize intended edits before execution
- refresh and screenshot after execution
- report any unresolved ambiguity instead of guessing

This exercise reinforces the core lesson: the real value comes from combining a low-level editing tool with a disciplined orchestration pattern.

## Test Yourself

<details><summary>What responsibilities belong to `pbir-cli`, and what responsibilities belong to the agent skill?</summary>

`pbir-cli` performs concrete report inspection and modification operations. The skill teaches the agent how to sequence those operations, manage context, apply safeguards such as backups, and follow workflow or governance rules.

</details>

<details><summary>Why does the workflow use an edit-refresh-screenshot loop?</summary>

Power BI report correctness is visual as well as structural. Refreshing the canvas and capturing a screenshot lets the agent or developer verify that removals, formatting changes, and layout results appear as intended.

</details>

<details><summary>What safeguards should precede destructive agentic report editing?</summary>

Locate the correct open Desktop report, create a backup, scope the request to named pages and visuals, and resolve ambiguity before making changes. Afterward, refresh the canvas, capture a screenshot, and confirm the requested result.

</details>

## Further Reading

- [Power BI Desktop documentation](https://learn.microsoft.com/power-bi/fundamentals/desktop-getting-started)
- [Use external tools in Power BI Desktop](https://learn.microsoft.com/power-bi/transform-model/desktop-external-tools)
- [Microsoft Fabric documentation](https://learn.microsoft.com/fabric/)
- [uv Python package manager and tool runner](https://docs.astral.sh/uv/)
