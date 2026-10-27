---
title: "Agentic Power BI Development with Skills, Hooks, and Validation Plugins"
source: "https://github.com/data-goblin/power-bi-agentic-development"
date: "2026-04-17"
tags: [power-bi, microsoft-fabric, agentic, pbip, automation]
source_type: "github"
topics: [power-bi-and-fabric, ai-agents, automation-workflows, context-engineering]
kind: "deep-dive"
depth: 2
actionability: 2
---

## TL;DR

> The repository turns Power BI and Microsoft Fabric artifacts into safer, source-controlled engineering workflows by packaging domain instructions, specialist reviews, and deterministic validation as installable plugins. This matters because agents can help create changes while hooks and scripts independently enforce structural, semantic, and operational checks.

## Key Takeaways

1. Treat the repository as a plugin marketplace, not a standalone application; install only the domains needed, such as `pbip`, `pbi-desktop`, `reports`, or `fabric-cli`.
2. Use skills to teach repeatable domain workflows, agents to perform specialized reviews or audits, and hooks to run deterministic checks triggered by tool actions.
3. Validate source-controlled PBIP artifacts before opening them in Power BI by tracing `plugins/pbip/skills/pbip/SKILL.md`, `pbip-validator.md`, `hooks.json`, `config.yaml`, `validate-pbir.sh`, `validate-report-binding.sh`, and `validate-tmdl.sh`.
4. Distinguish static PBIP validation from live-model validation: the `pbip` plugin checks files such as PBIR and TMDL, while `pbi-desktop` connects to a running model and uses scripts including `snapshot-model.ps1` and `check-referential-integrity.ps1`.
5. Apply technology-specific report quality gates through reviewers for Deneb specifications, SVG-in-DAX, R visuals, and Python visuals instead of relying on one general-purpose review.
6. Use `fabric-cli` scripts for remote operations such as downloading workspaces, executing DAX, exporting semantic models as PBIP, analyzing downstream reports, and querying lakehouses or SQL endpoints.
7. Version and validate the automation itself: plugin manifests, skills, agents, hooks, scripts, release notes, and CI checks are maintained as governed engineering assets.

## Overview
These notes describe a GitHub repository that acts as a plugin marketplace for coding agents working on Power BI and Microsoft Fabric tasks. Rather than being a standalone application, the repository packages reusable instructions, validation logic, review agents, helper scripts, and operational tooling into installable plugins for domains like PBIP, semantic models, report assets, Tabular Editor, Power BI Desktop, and Fabric administration.

This matters because it turns loosely guided AI assistance into a more structured workflow: skills provide domain knowledge, agents perform specialized review, and hooks/scripts enforce deterministic validation. For BI engineering teams treating reports and semantic models as code, this creates a safer and more repeatable pattern for automation, source control, and governance.

## Key Concepts
- **Plugin marketplace**: The repository is organized as a set of installable plugins rather than one monolithic tool. Each plugin targets a Power BI or Fabric area such as PBIP, reports, Tabular Editor, Desktop interaction, or Fabric operations.
- **Skills**: Markdown-based instruction packs that teach the agent domain knowledge and repeatable workflows. They live under plugin-specific `skills/.../SKILL.md` paths and may be auto-invoked or called explicitly.
- **Agents**: Specialized helpers for review, debugging, or audit tasks. In this repository they are generally markdown-defined reviewers or validators for assets like Deneb specs, SVG DAX, BPA expressions, and semantic models.
- **Hooks**: Deterministic validations triggered by tool actions rather than model judgment. They are implemented with shell/PowerShell scripts and config files to validate PBIR, TMDL, bindings, metadata, and referential integrity.
- **PBIP and semantic model as code**: A major theme is working directly with source-controlled Power BI artifacts such as PBIP, TMDL, and PBIR files, allowing validation before opening changes in the UI.
- **Operational automation**: The repository also supports remote and admin workflows through Fabric CLI and admin-oriented plugins, including scripts for workspace download, DAX execution, lineage analysis, and tenant auditing.

## How It Works
At the top level, the repository is structured like a Claude-style plugin marketplace. Marketplace metadata is defined in `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json`, while each plugin under `plugins/` has its own `.claude-plugin/plugin.json`. This allows selective installation of only the relevant domains, such as `pbip`, `pbi-desktop`, or `tabular-editor`.

Core plugin areas include:

- `plugins/tabular-editor/`
- `plugins/pbi-desktop/`
- `plugins/pbip/`
- `plugins/reports/`
- `plugins/semantic-models/`
- `plugins/fabric-cli/`
- `plugins/fabric-admin/`

Within a plugin, the folder structure tends to follow a consistent pattern:

- `skills/`: instruction packs and workflows in `SKILL.md`
- `agents/`: specialized review or validation assistants
- `commands/`: explicit user-invoked workflows such as `/suggest-rule`
- `hooks/`: executable validation logic and hook registration/configuration
- `scripts/` or `references/`: helper utilities and supporting documentation

A useful workflow model is:

`user request -> skill selection -> agent/tool execution -> hook validation -> feedback loop`

For PBIP development, the `pbip` plugin provides skills that explain PBIP, TMDL, and PBIR structure. After an engineer edits files, hooks like `validate-pbir.sh`, `validate-tmdl.sh`, and `validate-report-binding.sh` can run automatically using settings from `plugins/pbip/hooks/config.yaml` and registrations in `plugins/pbip/hooks/hooks.json`. This makes the plugin executable and enforceable, not just descriptive.

The `pbi-desktop` plugin focuses on live interaction with a running Power BI Desktop model. Its `connect-pbid` skill and helper scripts support model-aware workflows, while PowerShell hooks such as `snapshot-model.ps1` and `check-referential-integrity.ps1` perform runtime checks. This distinguishes static project validation from validation against an actively loaded model.

The `tabular-editor` plugin combines instructional content with automation. It includes skills for BPA rule authoring, CLI usage, C# scripting, and docs lookup, plus script-based auditing through `plugins/tabular-editor/scripts/bpa_rules_audit.py`. On top of that, agents like `bpa-expression-helper` and commands like `/suggest-rule` help generate or review quality rules.

The `reports` plugin covers report-level artifacts including Deneb, SVG-in-DAX, R visuals, Python visuals, theme JSON, and PBIR automation. Reviewer agents such as `deneb-reviewer.md`, `svg-reviewer.md`, `r-reviewer.md`, and `python-reviewer.md` act as specialized quality gates tailored to each visual technology.

The `semantic-models` plugin packages authoring and audit knowledge for DAX, Power Query, naming conventions, refresh troubleshooting, lineage, and model audits. Its `semantic-model-auditor.md` complements the `pbip` and `pbi-desktop` plugins by focusing on model quality rather than file format or live session state.

The `fabric-cli` and `fabric-admin` plugins extend the system into remote operations and governance. The `fabric-cli` plugin includes scripts such as:

- `create_direct_lake_model.py`
- `download_workspace.py`
- `execute_dax.py`
- `export_semantic_model_as_pbip.py`
- `get-downstream-reports.py`
- `query_lakehouse_duckdb.py`
- `query_sql_endpoint.py`

These support remote Fabric and Power BI workflows. The `fabric-admin` plugin goes further into governance with scripts like `audit-tenant-settings.py` and `generate_audit_pdf.py`, along with references for delegated overrides and security groups.

The repository also includes a `useful-stuff/` area with safety-oriented hooks to block destructive commands, package manager misuse, or secrets exposure. That shows the architecture is concerned not only with BI semantics but also with safe agent execution.

From a maintenance perspective, the repository treats agent instructions and plugin packaging as versioned, validated assets. Release notes track frequent iteration, and CI assets such as `.github/workflows/validate-plugins.yml` and `scripts/validate-plugins.sh` help enforce packaging quality.

A concise mental model is:

```text
Marketplace -> Plugin -> Skills teach the agent what to do -> Agents review or handle specialized tasks -> Commands expose common workflows directly -> Hooks enforce deterministic checks -> Scripts/references provide executable and factual support
```

Training exercise summary from the notes:

1. Clone the repository:
   ```bash
   git clone https://github.com/data-goblin/power-bi-agentic-development.git
   cd power-bi-agentic-development
   ```

2. Inspect the plugin layout and identify:
   - content layer: `skills/`
   - review layer: `agents/`
   - enforcement layer: `hooks/` or `scripts/`

3. Trace PBIP validation through:
   - `plugins/pbip/skills/pbip/SKILL.md`
   - `plugins/pbip/agents/pbip-validator.md`
   - `plugins/pbip/hooks/hooks.json`
   - `plugins/pbip/hooks/config.yaml`
   - `validate-pbir.sh`
   - `validate-report-binding.sh`
   - `validate-tmdl.sh`

4. Compare that with the live-model path in `pbi-desktop`:
   - `plugins/pbi-desktop/skills/connect-pbid/SKILL.md`
   - `plugins/pbi-desktop/hooks/config.yaml`
   - `snapshot-model.ps1`
   - `check-referential-integrity.ps1`

5. Inspect operational automation in `fabric-cli`:
   - `plugins/fabric-cli/skills/fabric-cli/SKILL.md`
   - pick two scripts and summarize the remote operations they enable

6. Create a personal architecture note template:
   ```text
   Plugin:
   Primary use case:
   Main skills:
   Main agent(s):
   Validation/enforcement assets:
   External tools or APIs involved:
   Typical engineer workflow:
   ```

7. Optional Claude Code installation:
   ```bash
   claude plugin marketplace add data-goblin/power-bi-agentic-development
   claude plugin install pbip@power-bi-agentic-development
   ```

Success criteria captured in the notes:
- Explain the difference between a skill, an agent, and a hook
- Identify the files implementing PBIP validation
- Describe at least one Fabric automation workflow from the codebase

## Test Yourself

<details><summary>What is the difference between a skill, an agent, and a hook in this repository?</summary>

A skill is a Markdown instruction pack that teaches domain knowledge and workflows. An agent is a specialized reviewer, debugger, or auditor, while a hook invokes executable logic to enforce deterministic validation after relevant actions.

</details>

<details><summary>Which assets should you inspect to understand the PBIP validation path?</summary>

Start with `plugins/pbip/skills/pbip/SKILL.md` and `plugins/pbip/agents/pbip-validator.md`, then inspect `hooks/hooks.json`, `hooks/config.yaml`, `validate-pbir.sh`, `validate-report-binding.sh`, and `validate-tmdl.sh`. Together they show the instructional, review, registration, configuration, and enforcement layers.

</details>

<details><summary>How do the `pbip`, `pbi-desktop`, and `fabric-cli` plugins serve different workflows?</summary>

`pbip` validates source-controlled project files, while `pbi-desktop` inspects and validates a model currently loaded in Power BI Desktop. `fabric-cli` supports remote operational workflows such as downloading workspaces, executing DAX, exporting models, and querying Fabric data services.

</details>

## Personal Notes
Agentic Power BI Development with Skills, Hooks, and Validation Plugins

Source: https://github.com/data-goblin/power-bi-agentic-development/
Notion page: https://www.notion.so/Agentic-Power-BI-Development-with-Skills-Hooks-and-Validation-Plugins-34501bb0839a81399eebcb4b030b9ebe

Tags: power-bi, microsoft-fabric, agentic, pbip, tabular-editor, automation

Overview

This repository is a plugin marketplace for coding agents such as Claude Code and GitHub Copilot, focused specifically on Power BI and Microsoft Fabric workflows. Instead of being a traditional application, it packages domain knowledge, validation logic, agent instructions, and helper scripts into installable plugins that teach agents how to work with semantic models, reports, PBIP projects, Tabular Editor, and Fabric operations.

For engineers building BI assets as code, the repo matters because it turns fragile prompt-based assistance into structured, reusable automation.
