---
title: "Power BI Project Files and Agentic Authoring in Microsoft Fabric"
source: "https://www.youtube.com/watch?v=-YH-Yue_pPY"
date: "2026-08-07"
tags: [powerbi, microsoft-fabric, source-control, semantic-modeling, ai-agents]
source_type: "youtube"
source_fingerprint: "7cd5d51f00"
source_characters: 38045
channel: "RADACAD"
published: "2026-08-06"
duration_seconds: 2808
topics: [power-bi-and-fabric, ai-agents, automation-workflows]
kind: "interview"
depth: 2
actionability: 1
---

## TL;DR

> Power BI Project (PBIP) turns reports and semantic models into inspectable files that teams, scripts, and AI agents can version, edit, and test. Reliable agentic authoring requires both supported tools for changing and verifying artifacts and explicit skills that encode team standards.

## Key Takeaways

1. Use PBIX for convenient single-file packaging and sharing; use PBIP for source control, collaboration, scripted changes, and AI-assisted development.
2. Treat TMDL as the textual, diffable representation of a semantic model and PBIR as the finer-grained structure for report metadata.
3. Build automation only on supported metadata-editing paths hardened to tolerate changes made outside Power BI Desktop.
4. Give agents tools such as MCPs, APIs, and a desktop IPC bridge so they can edit artifacts, reload projects, capture screenshots, and verify results.
5. Encode naming conventions, modeling rules, and repeatable procedures in skills so agents follow the team’s preferred development practices.
6. Treat the speaker’s statements about GA timing, default-on behavior, and automatic reloading as time-bound roadmap claims rather than current guarantees.

## Overview

This lesson explains how Power BI project artifacts make report and semantic-model development easier to inspect, version, automate, and hand off to AI agents. The interview’s strongest evidence is around architecture and intent: PBIP exposes Power BI work as files and folders, TMDL gives semantic models a textual form, PBIR restructures report metadata for safer editing, and agent tooling layers on top through MCPs, APIs, desktop bridging, and skills. Roadmap claims in the interview such as GA timing, default-on behavior, and upcoming auto-reload should be treated as time-bound statements from the speaker, not guaranteed current product status.

## Key Concepts

- **PBIP as the code-behind for Power BI artifacts**: PBIP, or Power BI Project, represents a report and semantic model as a folder-based project instead of a single PBIX file. In the interview, its main purpose is enabling collaboration, source control, scripting, and supported metadata edits that are difficult with an opaque packaged file.
- **PBIX remains useful for packaging and sharing**: The speaker explicitly says PBIX is not going away and may remain the main sharing format because it is easy to send as one file. The practical distinction is that PBIX is convenient for distribution, while PBIP is better for team development and automation.
- **TMDL for semantic models**: TMDL is described as a declarative textual representation of a semantic model. Its value is that developers and tools can inspect, diff, script, and modify model definitions directly instead of relying only on the desktop UI.
- **PBIR for report metadata**: PBIR is the enhanced report format intended to replace an older single-JSON internal structure that was poor for source control and machine editing. The interview frames PBIR as a key enabler for safer report diffs, finer-grained files such as page and visual artifacts, and more reliable AI or scripted edits.
- **Hardening enables supported automation**: A major theme is product hardening: Power BI must tolerate metadata changes made outside the desktop UI. That matters for external tools, scripts, and AI agents, because unsupported edits can otherwise break desktop or service behavior.
- **Agentic authoring needs tools plus knowledge**: The speaker separates AI success into two parts. Tools include MCPs, service APIs, and a desktop IPC bridge for reloading, testing, and screenshots. Knowledge lives in skills, which provide process guidance, conventions, and reusable context so agents behave more like a team’s preferred developer.

## How It Works

Start by choosing the right artifact form for the job. Use PBIX when the main need is simple packaging or sharing. Use PBIP when you need version control, parallel development, scripted bulk changes, or AI-assisted authoring. Within PBIP, treat the semantic model and report as editable code assets: TMDL represents the model textually, while PBIR organizes report metadata into smaller, more manageable pieces. Once artifacts are file-based, standard engineering workflows become possible: diffing changes, reviewing pull requests, applying conventions, and generating edits with scripts or agents. AI then becomes practical only when two layers are present. The first layer is tooling: MCPs and APIs let an agent read and write artifacts, while the desktop IPC bridge lets it reload a project, capture screenshots, and verify results instead of editing blindly. The second layer is knowledge: skills encode steps, constraints, and style rules such as naming conventions. The lesson’s operational takeaway is that durable AI workflows are not just “prompt the model.” They depend on observable files, supported mutation paths, and explicit team standards the agent can follow and test against.

## Training Exercise

Create a short written workflow for a fictional three-person BI team. First, decide when they should use PBIX and when they should use PBIP. Second, define three naming or modeling conventions an AI skill should enforce. Third, describe how an agent would make a report change, reload the project, and verify the result using the interview’s tool pattern of editable files plus desktop testing. Finish by listing two risks the team should watch for, such as relying on preview features or assuming roadmap statements are already shipped.

## Test Yourself

<details><summary>When should a team choose PBIP instead of PBIX?</summary>

Choose PBIP when the work requires version control, parallel development, scripted bulk changes, inspectable diffs, or AI-assisted authoring. PBIX remains useful when easy packaging and sharing as one file are the priority.

</details>

<details><summary>What roles do TMDL and PBIR play in a Power BI project?</summary>

TMDL expresses semantic-model definitions as editable text. PBIR divides report metadata into smaller artifacts, such as pages and visuals, making changes easier to inspect, compare, and automate.

</details>

<details><summary>What two layers are needed for reliable agentic authoring?</summary>

Agents need tools—including MCPs, APIs, and desktop bridging—to edit, reload, test, and observe artifacts. They also need skills that encode procedures, constraints, naming conventions, and other team knowledge.

</details>

## Further Reading

- [Source video](https://www.youtube.com/watch?v=-YH-Yue_pPY)
