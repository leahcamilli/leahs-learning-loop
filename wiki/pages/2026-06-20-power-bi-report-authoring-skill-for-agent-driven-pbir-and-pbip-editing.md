---
title: "Power BI Report Authoring Skill for Agent-Driven PBIR and PBIP Editing"
source: "https://learn.microsoft.com/en-us/power-bi/developer/agentic/power-bi-report-authoring-skill-overview"
date: "2026-06-20"
tags: [powerbi, pbip, pbir, ai-agents, copilot, mcp]
source_type: "web"
topics: [ai-agents, power-bi-and-fabric, automation-workflows]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> Use the Power BI Report Authoring skill for deterministic, source-controlled edits to the PBIR report layer inside PBIP projects—not for semantic-model or DAX changes. Reliable automation requires validating the edited files and then reloading Power BI Desktop to verify the rendered result.

## Key Takeaways

1. Treat PBIR files on disk as the source of truth; save Power BI Desktop changes before asking an agent to continue.
2. Use the Report Authoring skill for pages, visuals, filters, slicers, themes, formatting, bindings, and report-definition troubleshooting.
3. Use the Power BI Modeling MCP server first when a request requires a new table, measure, field, or DAX logic.
4. Validate PBIR structure after every editing pass, then reload the PBIP project in Power BI Desktop to catch rendering and interaction problems.
5. Give the authoring skill explicit requests or a locked design; Microsoft recommends Report Design or Report Planner skills for open-ended prompts such as designing an entire dashboard.
6. Commit or copy a baseline before agent edits so PBIR changes can be reviewed, diffed, and reverted.
7. Prefer modern visuals and verify bindings and roles when replacing legacy visuals such as Q&A, Bing maps, or filled maps.

## Overview

The Power BI Report Authoring skill is a preview AI-agent capability for creating, modifying, and validating the report layer of Power BI projects using natural language. It operates directly on PBIR files inside PBIP projects, making schema-correct edits to pages, visuals, filters, slicers, themes, and formatting rather than changing the semantic model itself.

This matters to engineers building agentic developer workflows around Power BI because it separates concerns cleanly: semantic modeling stays with the Modeling MCP server, report composition stays with the Report Authoring skill, and live verification happens through Power BI Desktop tooling. If you are automating report generation, modernizing legacy reports, or using GitHub Copilot CLI and similar coding agents to work against Power BI project files in source control, this skill is the report-editing piece of that pipeline.

## Key Concepts

- **PBIR and PBIP**: PBIR is the Power BI Report definition format, and PBIP is the Power BI Project structure that stores report assets as files on disk. The skill works only against PBIP projects and treats the PBIR report definition as the authoritative artifact to modify.
- **Report-layer authoring**: The skill focuses on the presentation layer of a Power BI solution: pages, visuals, filters, slicers, layout, themes, and formatting. It is not intended for table design, measure creation, or DAX authoring, which belong to semantic modeling tools.
- **Agentic workflow separation**: Microsoft positions this skill as one component in a broader agent ecosystem. Modeling MCP handles schema and DAX, the remote Power BI MCP server handles querying and insights, and the Report Authoring skill handles report JSON edits.
- **Validation and verification loop**: A reliable workflow includes editing the PBIR files, validating the report structure, then reloading Power BI Desktop and visually checking the result. This creates a practical closed loop where an agent can make changes and then verify both schema correctness and rendered output.
- **Design versus implementation**: The Report Authoring skill is for deterministic implementation of an already-specified design or explicit edit request. For open-ended prompts like 'make this dashboard look professional,' Microsoft recommends using the companion Report Design or Report Planner skills first.
- **Source-of-truth discipline**: Because the skill edits files on disk, the PBIR content is the canonical state. Unsaved manual edits in Power BI Desktop are invisible to the agent, so engineers must save Desktop changes before asking the agent to continue iterating.

## How It Works

At a high level, the Power BI Report Authoring skill lets an AI agent translate natural-language requests into direct edits on Power BI report definition files. The core idea is that report authoring becomes a file-manipulation problem rather than a UI automation problem. Instead of clicking through Power BI Desktop, the agent updates PBIR JSON in a PBIP project and then uses validation and Desktop reload tools to confirm the report still works.

The skill is meant for the report layer only. In practical terms, that means it can:

- create new report pages
- add or modify visuals
- bind visuals to an existing semantic model
- update slicers and filters
- change themes and formatting
- modernize older visual definitions
- diagnose report-definition issues that lead to empty visuals or error icons

It should not be the tool you reach for when the request is about data modeling. If the report needs a new measure, new table, or DAX logic, the expected flow is to use the Power BI Modeling MCP server first. Once the semantic model contains the needed fields and measures, the Report Authoring skill can wire those assets into visuals.

A typical agent-driven workflow looks like this:

1. **Prepare the semantic model**
   - Ensure required tables, columns, and measures exist.
   - Use the Modeling MCP server for model changes.

2. **Edit the report definition**
   - Use the Report Authoring skill to update PBIR files.
   - Create pages, charts, cards, tables, slicers, and layout changes.

3. **Validate the report**
   - Run report validation to catch structural or schema issues.
   - Fix problems such as invalid bindings, malformed query state, or mismatched roles.

4. **Verify in Power BI Desktop**
   - Reload the report using the Power BI Desktop bridge or CLI tooling.
   - Capture screenshots or inspect the rendered report.

5. **Iterate**
   - Refine layout, formatting, and bindings until both validation and visual review pass.

The article also defines where this skill fits relative to companion skills:

- **Report Authoring skill**: implement explicit report edits or a locked design.
- **Report Design skill**: decide what the report should look like for open-ended design requests.
- **Report Planner skill**: orchestrate end-to-end report creation, including requirements gathering and handoff between tools.

This distinction is operationally important. If the prompt is 'add a card showing Total Sales,' the Report Authoring skill is the right tool. If the prompt is 'design a sales dashboard,' a design-oriented skill should first produce a structured brief with page archetypes, layout, chart choices, and color decisions. The authoring skill then converts that brief into concrete PBIR edits.

The supported environment is explicitly file-based and source-control friendly. Because the skill edits JSON on disk, several engineering practices matter:

- commit a baseline before allowing the agent to edit the report
- save all Power BI Desktop changes before asking the agent to continue
- treat PBIR as the source of truth
- prefer modern visuals over soon-to-be-deprecated ones such as Q&A, Bing maps, and filled maps

From an implementation perspective, the important architectural takeaway is that the report definition is decoupled from interactive editing in Desktop. The agent can operate in editors and CLIs such as GitHub Copilot CLI, VS Code Copilot, Claude Code, Cursor, Codex/Jules, and Windsurf, then rely on Power BI Desktop only for runtime-style verification. That makes it possible to build reproducible, reviewable report changes through normal engineering workflows like branching, diffing, and reverting.

A practical mental model is:

```text
Natural-language request
  -> agent interprets request
  -> skill edits PBIR JSON in PBIP project
  -> validation catches structural issues
  -> Desktop reload verifies rendering
  -> engineer reviews diffs and screenshots
```

This is especially useful for scenarios such as:

- creating a new report from an existing semantic model
- adding pages and visuals to an existing report
- applying a new theme across a report
- converting legacy visual definitions to modern ones
- troubleshooting broken visuals caused by incorrect bindings or query state

## Training Exercise

Build a small, repeatable report-editing workflow using a PBIP project and an explicit authoring request.

### Goal
Practice separating semantic-model work from report-layer work, then verify the result using a validate-and-review loop.

### Prerequisites
- A Power BI project in **PBIP** format
- An existing semantic model with at least:
  - a date field
  - one category field
  - one numeric measure such as `Total Sales`
- Access to an agent environment that can use the Power BI Report Authoring skill
- Power BI Desktop installed

### Exercise steps
1. **Create a safety baseline**
   - Open your PBIP project folder.
   - Commit or copy the current state so you can diff and revert.

2. **Inspect the semantic model**
   - Confirm the model already contains fields needed for the report.
   - If `Total Sales` or a date field is missing, add it using your modeling workflow before continuing.

3. **Issue an explicit authoring request**
   Use a prompt like:

   ```text
   Add a new report page named Executive Summary.
   Place three card visuals for Total Sales, Total Orders, and Gross Margin.
   Add a clustered column chart showing Total Sales by Category.
   Add a date slicer bound to Order Date.
   Apply a dark theme with readable labels and consistent data colors.
   ```

4. **Review the PBIR file changes**
   - Inspect the modified project files in source control or your diff tool.
   - Look for changes related to page definitions, visual containers, formatting, and theme settings.

5. **Validate the report**
   - Run the report validation step provided by your tooling.
   - If validation fails, note whether the problem is structural, binding-related, or formatting-related.

6. **Reload in Power BI Desktop**
   - Open or reload the PBIP project in Power BI Desktop.
   - Check that all visuals render correctly and that the slicer filters the page as expected.

7. **Perform one iterative fix**
   Issue a focused follow-up request such as:

   ```text
   On the Executive Summary page, increase spacing between the KPI cards, sort the column chart descending by Total Sales, and ensure all labels are visible on the dark background.
   ```

8. **Compare before and after**
   - Review the second diff.
   - Note which changes are layout-only versus data-binding changes.

### What to learn from the exercise
- Which requests are precise enough for deterministic PBIR edits
- How report-layer changes appear as file diffs
- Why validation and Desktop verification are both necessary
- How saved project files, not unsaved Desktop state, drive the agent's understanding

### Stretch task
Try a modernization pass on an older report:
- replace a legacy card or matrix visual with its modern equivalent
- reapply formatting after replacement
- verify that bindings and visual roles still match the semantic model

## Test Yourself

<details><summary>When should you use the Report Authoring skill instead of the Modeling MCP server?</summary>

Use Report Authoring for presentation-layer changes such as pages, visuals, slicers, filters, themes, formatting, and bindings. Use Modeling MCP when the semantic model needs tables, measures, fields, or DAX logic.

</details>

<details><summary>Why are both report validation and Power BI Desktop verification necessary?</summary>

Validation detects structural, schema, query-state, and binding problems in PBIR files. Desktop verification confirms that visuals render correctly, formatting remains readable, and interactions such as slicers behave as intended.

</details>

<details><summary>What state does the agent consider authoritative during report editing?</summary>

The saved PBIR content in the PBIP project is authoritative. Unsaved Power BI Desktop edits are invisible to the agent, so Desktop changes must be saved before another agent-driven iteration.

</details>

## Further Reading

- [Power BI developer documentation](https://learn.microsoft.com/power-bi/developer/)
- [Power BI Project (PBIP) and developer mode documentation](https://learn.microsoft.com/power-bi/developer/projects/projects-overview)
- [Model Context Protocol specification](https://modelcontextprotocol.io/)
- [Power BI Desktop developer documentation](https://learn.microsoft.com/power-bi/developer/visuals/)
- [Microsoft Learn: Power BI agentic development overview](https://learn.microsoft.com/en-us/power-bi/developer/agentic/)
