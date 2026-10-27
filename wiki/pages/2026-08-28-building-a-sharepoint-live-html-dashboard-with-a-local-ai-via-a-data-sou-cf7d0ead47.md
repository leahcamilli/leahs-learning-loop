---
title: "Building a SharePoint Live HTML Dashboard with a Local AI via a Data Source Contract"
source: "https://lnkd.in/p/gFQgcTuM"
date: "2026-08-28"
tags: [sharepoint, html-dashboards, ai-workflows, data-contracts]
source_type: "web"
source_fingerprint: "cf7d0ead47"
source_characters: 2557
topics: [web-development, prompt-engineering]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> Separate SharePoint schema discovery from AI code generation: give the local model a Data Source Contract and SharePoint-specific rules, then let SharePoint bind live data at runtime. This can keep business records away from the model while still producing a data-driven dashboard.

## Key Takeaways

1. Use SharePoint-side tooling to describe the target list or library without exporting its records to the local model.
2. Include fields, data types, choices, relationships, views, filters, and KPI hints in the Data Source Contract.
3. Provide the local model with reusable rules for SharePoint `/_html`, LiveData, sandbox restrictions, and dashboard design.
4. Generate the HTML and JavaScript locally from the contract and a short task prompt; the post reports success with `Qwen3-Coder-30B-A3B-Instruct` on a Mac mini M4 with 32 GB RAM.
5. Upload the generated page to SharePoint so LiveData can supply current list or library data when the page opens.
6. Treat the approach as a small proof of concept, not a production-validated pattern across every site in a tenant.

## Overview

This lesson describes a proof-of-concept pattern for generating a SharePoint HTML dashboard with a local AI model that has no direct SharePoint access. The core idea is to separate schema understanding from code generation: SharePoint-side tooling produces a structured description of a list or library, and a local model uses that description plus SharePoint HTML and LiveData rules to generate the dashboard. The evidence is limited to a short LinkedIn post, so treat this as an observed architecture and workflow, not a validated production blueprint.

## Key Concepts

- **LiveData in SharePoint**: The post says SharePoint's LiveData capability lets JavaScript-based HTML pages connect to lists and document libraries while staying inside the SharePoint sandbox.
- **Data Source Contract**: A SharePoint skill analyzes a list or library and creates a contract describing fields, data types, choices, relationships, views, and useful KPI or filter information. This contract is the main input to the local model.
- **No direct model access to SharePoint**: The local AI does not query SharePoint directly. Instead, it receives the Data Source Contract and a reusable system prompt containing the relevant SharePoint and sandbox rules.
- **Reusable system prompt**: The system prompt is described as containing the SharePoint `/_html` specification, LiveData structure, sandbox restrictions, and design guidelines. This gives the model the constraints needed to generate compatible code.
- **Local code generation**: The dashboard HTML and JavaScript are generated locally in LM Studio from the contract plus a short task prompt. The post specifically reports success with `Qwen3-Coder-30B-A3B-Instruct` on a Mac mini M4 with 32 GB RAM.
- **Runtime data binding in SharePoint**: After upload, SharePoint provides current list data when the generated page opens. In this pattern, SharePoint is responsible for live data delivery at runtime, not the local model.

## How It Works

A practical way to understand this pattern is as a four-stage pipeline. First, inspect the target SharePoint list or library and extract a schema-level description rather than exporting records. Second, package that description as a Data Source Contract containing structure, field semantics, and view or KPI hints. Third, give a local model two inputs: the contract and a reusable prompt that explains SharePoint `/_html`, LiveData, sandbox limits, and dashboard design rules. Fourth, upload the generated HTML file to SharePoint, where the page receives live data at runtime through LiveData. The architectural benefit is that business data does not need to be sent to the local model. The main uncertainty is operational breadth: the author says it is a small proof of concept and only hopes it works across all sites in the tenant.

## Training Exercise

Write a mini lesson plan for yourself using this pattern. Define a fictional SharePoint list with 5 fields, 1 relationship, and 2 useful filters. Then draft a compact Data Source Contract for it, including field names, types, allowed values, and one KPI. Next, write a short system prompt section that lists the constraints your HTML generator must follow: sandbox-safe JavaScript, no direct SharePoint access, and runtime binding through LiveData. Finally, outline the HTML dashboard you want the model to generate: one summary KPI card, one filter control, and one table. As a reflection step, note which parts are supported directly by the source and which parts you are inferring for your exercise.

## Test Yourself

<details><summary>Why can the local AI generate a SharePoint dashboard without direct access to SharePoint?</summary>

It receives a Data Source Contract describing the source structure and a reusable prompt containing the relevant SharePoint rules. According to the post, SharePoint supplies the actual live data only when the uploaded page runs.

</details>

<details><summary>What information should a Data Source Contract contain?</summary>

It should describe fields, types, allowed choices, relationships, views, and useful filter or KPI information. This gives the model enough structural and semantic context to generate the dashboard code.

</details>

<details><summary>What is the main limitation of the architecture presented in the lesson?</summary>

The source describes only a small proof of concept and does not establish production reliability or tenant-wide compatibility. Broader operation across SharePoint sites remains an unvalidated goal.

</details>

## Further Reading

- [LinkedIn source post](https://lnkd.in/p/gFQgcTuM)
