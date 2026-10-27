---
title: "Copilot for SharePoint: Portable Skills, Skill Self-Improvement, and SharePoint-Safe HTML"
source: "https://www.youtube.com/watch?v=yc7foD5cHfs"
date: "2026-08-26"
tags: [sharepoint, copilot, agent-design, prompt-engineering, knowledge-management]
source_type: "youtube"
source_fingerprint: "84a4d3191a"
source_characters: 7924
channel: "Zach Rosenfield"
published: "2026-08-25"
duration_seconds: 464
topics: [microsoft-365, prompt-engineering, ai-agents, context-engineering]
kind: "demo"
depth: 2
actionability: 2
---

## TL;DR

> Turn repeatable work into personal skills that can follow you across SharePoint sites, then test improvements before replacing them. For SharePoint HTML, the demo recommends giving agents the tenant’s `/_html` instructions so their output respects the platform’s sandbox and supported features.

## Key Takeaways

1. Use a personal skill when the same behavior needs to work across multiple SharePoint sites; the transcript says personal skills are stored in OneDrive under a Copilot agent assets folder.
2. Encode 3 to 5 explicit editorial or workflow rules in a skill so a reusable capability replaces repeated one-off prompts.
3. Review the generated happy-path, edge-case, and adversarial tests before accepting changes proposed by the demonstrated “improve skill” workflow.
4. Compare the reported baseline and revised evaluation before overwriting a skill; save a new version or discard the changes when the evidence is insufficient.
5. Separate portable skill logic, evaluation criteria, and publishing constraints instead of resolving all three ad hoc in each chat.
6. The demo claims each Microsoft 365 tenant has a `customer-name.sharepoint.com/_html` page that agents can consult for tenant-specific SharePoint HTML instructions.
7. Point an HTML-generating agent to the tenant’s `/_html` page because, according to the transcript, general-purpose agents may not produce SharePoint sandbox-safe HTML by default.

## Overview

This lesson explains three features demonstrated in the supplied video transcript: personal skills that travel across SharePoint sites, an "improve skill" workflow that tests and revises a skill, and a tenant-specific `/_html` page that gives agents instructions for generating SharePoint-ready HTML. The evidence is a product demo transcript, so the lesson should be read as an explanation of the demonstrated workflow rather than an independently verified product specification.

## Key Concepts

- **Personal skills**: A personal skill is saved in a user's OneDrive under a Copilot agent assets folder and is described as being structured the same way as a regular skill. The practical benefit is portability: the same skill can be used across different SharePoint sites without reinstalling it on each site.
- **Site skills versus personal skills**: The transcript distinguishes skills attached to a specific SharePoint site from skills tagged as personal. This matters operationally because site skills are local to a site collection, while personal skills are intended to follow the user from site to site.
- **Skill creation from reusable principles**: The demo creates a new personal skill from a prompt containing editing principles such as detecting false binaries, throat-clearing openers, and manufactured insights. The lesson is that a skill can encode repeatable editorial rules so they can be invoked consistently later.
- **Skill-guided content revision**: Once created, the skill is called inside a SharePoint chat to revise text according to its rules. This shows a concrete pattern for turning a one-time prompt into a reusable capability for drafting and cleanup.
- **Improve skill workflow**: The transcript says an "improve skill" command generates a test plan, including happy-path, edge-case, and adversarial tests, then evaluates the skill and proposes validated changes. The user is expected to review the test plan before accepting an overwrite, saving a new version, or discarding changes.
- **Evaluation before overwrite**: A key control point in the demo is that the system reports a baseline, tests revisions, and presents options rather than silently replacing the original. Practically, this frames skill improvement as an assisted evaluation loop instead of blind auto-editing.
- **Tenant-specific `/_html` instructions**: Every Microsoft 365 customer is described as having a SharePoint page at `customer-name.sharepoint.com/_html`. In the demo, agents use that page as an instruction source for producing HTML that is compatible with SharePoint's sandbox and features.
- **Sandbox-safe HTML publishing**: The transcript emphasizes that SharePoint HTML runs in a safe sandbox, reducing JavaScript attack risk, but that many general-purpose agents do not produce sandbox-safe HTML by default. The practical implication is to point agents at the tenant `/_html` page so output matches SharePoint constraints and supported features.

## How It Works

Treat the workflow as a three-part system. First, convert repeatable knowledge work into a personal skill when you want the same behavior across many SharePoint sites; the transcript places these skills in OneDrive and says they share the same structure as regular skills. Second, use an improvement loop when the skill behaves too broadly or misses its target: review the generated test plan, check whether the happy-path and adversarial cases reflect the real job, then accept or reject the proposed revision based on the reported evaluation. Third, when generating HTML for SharePoint from any agent, use the tenant `/_html` page as the source of current formatting and safety instructions so the output fits SharePoint's sandbox and built-in capabilities. The durable lesson is to separate portability, evaluation, and deployment constraints rather than handling them ad hoc in each chat.

## Training Exercise

Create a mini knowledge-base workflow on paper or in your notes. Define one portable editing skill with 3 to 5 explicit rules, such as removing throat-clearing openers or simplifying false binaries. Write one example input and one expected revised output. Then draft a test plan with three cases: a normal case, an edge case, and an adversarial case where the skill should avoid over-editing. Finally, write a short checklist for HTML output constraints you would want an agent to read before publishing into a sandboxed environment like SharePoint. The goal is to practice separating reusable skill logic, evaluation criteria, and publishing constraints.

## Test Yourself

<details><summary>When should a personal skill be used instead of a site skill?</summary>

Use a personal skill when the same reusable behavior should follow the user across multiple SharePoint sites. The transcript describes site skills as local to a site collection and personal skills as portable through OneDrive.

</details>

<details><summary>What checks should happen before an improved skill replaces the original?</summary>

Review whether the happy-path, edge-case, and adversarial tests represent the real task, then compare the baseline with the revised evaluation. Only overwrite the original when the reported results justify the change; otherwise save a separate version or discard it.

</details>

<details><summary>Why does the lesson recommend directing agents to the tenant’s `/_html` page?</summary>

The demo presents that page as a source of tenant-specific instructions for generating SharePoint-ready HTML. Following those instructions is intended to keep output compatible with SharePoint’s sandbox and supported features.

</details>

## Further Reading

- [Source video](https://www.youtube.com/watch?v=yc7foD5cHfs)
