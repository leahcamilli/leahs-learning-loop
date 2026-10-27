---
title: "Understanding Microsoft Power Platform Skills: Plugin Marketplace Architecture and Workflow"
source: "https://github.com/microsoft/power-platform-skills"
date: "2026-07-10"
tags: [power-platform, plugins, claude-code, github-copilot, javascript, pac-cli]
source_type: "github"
topics: [ai-agents, coding-agents, automation-workflows, context-engineering]
kind: "deep-dive"
depth: 2
actionability: 2
---

## TL;DR

> The repository productizes Power Platform development workflows by combining agent instructions with manifests, scripts, hooks, MCP servers, and platform tools. This layered architecture matters because executable guardrails and validation make AI-generated work more reliable than prompts alone.

## Key Takeaways

1. Treat the repository as an operational plugin marketplace, not a conventional SDK or library.
2. Trace plugin discovery from the root `marketplace.json` to each plugin’s `.plugin/plugin.json`; `.claude-plugin/plugin.json` exists for backward compatibility.
3. Expect most agent behavior to come from Markdown assets in `agents/`, `skills/`, `commands/`, and shared references.
4. Use scripts, MCP servers, and external tools such as `pac`, Azure CLI, Node.js, and .NET to turn agent instructions into Dataverse, app, flow, packaging, and deployment operations.
5. Use pre- and post-tool hooks to capture telemetry, validate generated artifacts, and block unsafe or noncompliant changes.
6. Choose architecture by development surface: `mobile-apps` bundles an Expo template and extensive validators, `model-apps` emphasizes Dataverse automation and React samples, and `power-automate` exposes flow operations through an MCP server.
7. Apply repository-level validators and GitHub Actions to keep plugin names, descriptions, compatibility metadata, telemetry keys, keywords, and versions consistent across the marketplace.

## Overview

For a working engineer, the important idea is that this repo is not a typical SDK or library. It is an operational layer that teaches coding agents how to behave in Power Platform projects by combining plugin manifests, agents, skills, references, hooks, scripts, and MCP servers. If you want to understand how AI development workflows are productized for enterprise platforms, or if you need to extend or debug these plugins, this repository is a strong example.

## Key Concepts

- **Marketplace manifest**: The root `marketplace.json` is the top-level registry that lists available plugins in the repository. It separates marketplace metadata from plugin-specific metadata so each plugin can evolve independently while still being discoverable by Claude Code or Copilot CLI.
- **Per-plugin manifests**: Each plugin has a `.plugin/plugin.json` file that defines its installable identity and metadata. The repo also maintains mirrored `.claude-plugin/plugin.json` files for backward compatibility with older subscription mechanisms.
- **Agents, skills, and commands**: The plugins encode behavior primarily through markdown instruction assets such as `agents/`, `skills/`, and sometimes `commands/`. These files are the operational prompt layer that directs the coding agent to plan, generate, validate, and deploy artifacts for specific Power Platform scenarios.
- **Hooks and validation**: Some plugins, especially `mobile-apps` and `power-pages`, include hook definitions and JavaScript validators that run around tool usage. These enforce project rules such as safe writes, dependency hygiene, navigation correctness, accessibility checks, telemetry capture, and connector-first design.
- **PAC CLI and external tools**: The repository assumes integration with external tooling such as the Power Platform CLI (`pac`), Azure CLI, Node.js, and sometimes .NET or MCP servers. The install and execution model is built around agents being allowed to call these tools to create solutions, manipulate Dataverse metadata, deploy apps, or run automation flows.
- **Plugin-specific architecture**: Each plugin targets a different development surface and therefore bundles different assets. For example, `power-automate` ships an MCP server, `mobile-apps` includes a full Expo template and validation scripts, and `model-apps` contains Dataverse automation scripts and React/TypeScript samples for generative pages.

## How It Works

At the top level, this repository acts like a registry plus a collection of self-contained plugin packages. The root `marketplace.json` advertises installable plugins, while `scripts/install.js` automates setup by detecting supported clients, installing `pac` if necessary, registering the marketplace, and enabling auto-update. The root `.claude/settings.json` also predefines tool permissions for common commands such as `pac`, `node`, and `dotnet`, reducing friction when agents need to execute shell actions.

A key architectural choice is the split between **marketplace metadata** and **plugin metadata**. The marketplace lists entries with simple `name` and repository-relative `source`, while each plugin owns its own `.plugin/plugin.json` for description, versioning, licensing, and keywords. The mirrored `.claude-plugin/` files exist only for compatibility with older plugin consumers. This avoids duplicated metadata and lets plugin updates flow cleanly without breaking existing users.

Inside `plugins/`, each directory is effectively a productized AI workflow:

- `power-pages/`
  - Focused on Power Pages code sites.
  - Contains `agents/` for tasks like Web API integration, table-permission design, and data model architecture.
  - Includes `hooks/` such as `run-skill-pretool-telemetry.js` and post-tool validation, showing that the plugin can instrument execution and verify results.

- `model-apps/`
  - Targets generative pages for model-driven apps.
  - Has `agents/` for planning, entity building, page generation, and edits.
  - Contains operational scripts like `create-table.js`, `create-relationship.js`, `add-column.js`, `create-solution.js`, and `generate-page-manifest.js`, which means the agent is not just generating text; it can automate Dataverse and solution packaging tasks.
  - Includes samples in TypeScript/React and references for caching, localization, rules, and dependency constraints.

- `mobile-apps/`
  - Provides the richest workflow packaging in the repo.
  - Includes multiple planning/build agents, a `template/` Expo application, script helpers for Dataverse and offline profile management, and many validators under `hooks/`.
  - The hook names reveal architectural guardrails: protecting file paths, checking package dependencies, enforcing navigation idempotency, validating color contrast, and verifying Dataverse payload usage.

- `code-apps/`
  - Focused on Power Apps code apps with React/Vite/TypeScript.
  - Organized around `agents/`, `skills/`, and `shared/` references such as development standards, connector references, planning policy, and version checks.
  - This suggests a lighter-weight plugin where most behavior comes from structured guidance rather than many executable scripts.

- `mcp-apps/`
  - Designed for generating widget-style MCP apps.
  - Provides references and HTML samples like flight-status and weather widgets, making it a narrower but concrete plugin for interactive tool UIs.

- `canvas-apps/`
  - Centers on authoring `.pa.yaml` canvas app assets through the Canvas Authoring MCP server.
  - Uses agents and reference guides rather than bundled runtime code.

- `power-automate/`
  - Includes an actual server implementation at `server/mcp.mjs`.
  - This plugin is notable because it exposes a machine control surface for flow operations through MCP rather than relying only on static instructions.

The data flow is roughly:

1. A user installs the marketplace or loads a plugin locally.
2. Claude Code or Copilot reads the plugin manifest and makes its skills/agents/commands available.
3. During a task, the agent consults plugin instructions in markdown, shared references, and any samples.
4. If needed, it calls scripts or external CLIs such as `pac`, `az`, `node`, or MCP servers.
5. Hooks may run before or after tool execution to capture telemetry, validate changes, or block unsafe output.
6. The resulting artifacts are written into the user's project and optionally deployed into the Power Platform environment.

There are also repository-level quality controls. The `scripts/` folder contains validators for plugin names, skill descriptions, legacy compatibility, keyword casing, telemetry keys, and version checks. GitHub Actions run these validations continuously. This indicates the repo is maintained as a curated marketplace with consistency requirements, not as an ad hoc set of prompts.

One subtle but important implementation detail is that the plugins are **instruction-heavy but workflow-aware**. Much of the repository is markdown, samples, and references, yet there are enough JavaScript utilities, hooks, and MCP servers to turn those instructions into reliable automated behavior. In practice, this is how enterprise AI plugins become trustworthy: not by relying on a single prompt, but by combining prompts with code-based guardrails and platform-native tooling.

## Training Exercise

Build a mental model of one plugin by tracing the `model-apps` workflow from manifest to automation script.

### Goal
Understand how a plugin in this marketplace turns agent instructions into concrete Power Platform actions.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/microsoft/power-platform-skills.git
   cd power-platform-skills
   ```

2. Inspect the marketplace entry points:
   - Open `marketplace.json`
   - Open `plugins/model-apps/.plugin/plugin.json`
   - Compare with `plugins/model-apps/.claude-plugin/plugin.json`

3. Map the plugin structure:
   - Read `plugins/model-apps/README.md`
   - Inspect `plugins/model-apps/agents/`
   - Inspect `plugins/model-apps/references/`
   - Inspect `plugins/model-apps/samples/`
   - Inspect `plugins/model-apps/scripts/`

4. Trace a likely task flow such as “create a generative page backed by a new Dataverse table”:
   - Which agent would plan the work?
   - Which script would create the table?
   - Which script would add columns or relationships?
   - Which sample could guide the page UI?
   - Which script would generate the page manifest?

5. Write a short architecture note in your own words with these sections:
   - Entry point
   - Planning assets
   - Reference material
   - Executable automation
   - Deployment dependency

6. Optional: inspect one executable script to see how tool integration is implemented. For example:
   ```bash
   sed -n '1,220p' plugins/model-apps/scripts/create-table.js
   ```
   Then answer:
   - Does it call `pac`, Dataverse APIs, or both?
   - What inputs would an agent need to supply?
   - What failure modes should a hook or validator catch?

### Stretch exercise
Compare `model-apps` with `mobile-apps` and list three architectural differences. Focus on why `mobile-apps` needs a bundled template and many validation hooks while `model-apps` emphasizes Dataverse scripts and React page samples.

## Test Yourself

<details><summary>How are marketplace metadata and plugin metadata separated?</summary>

The root `marketplace.json` lists discoverable plugins using names and repository-relative sources. Each plugin owns its identity, version, licensing, description, and keywords in `.plugin/plugin.json`, while `.claude-plugin/plugin.json` supports older consumers.

</details>

<details><summary>What happens after an agent loads a plugin and receives a Power Platform task?</summary>

The agent consults instructions, references, and samples, then may invoke scripts, external CLIs, or MCP servers. Hooks can run around those tool calls to record telemetry, validate results, or block unsafe output before artifacts are written or deployed.

</details>

<details><summary>Why is `mobile-apps` packaged differently from `model-apps`?</summary>

The lesson describes `mobile-apps` as needing a complete Expo starting point plus guardrails for dependencies, navigation, accessibility, file writes, offline behavior, and Dataverse payloads. `model-apps` instead centers on Dataverse creation scripts, solution packaging, page manifests, and React/TypeScript samples for generative pages.

</details>

## Further Reading

- [Power Platform CLI reference](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference)
- [Power Apps code apps documentation](https://learn.microsoft.com/power-apps/developer/code-apps/)
- [Generative Pages with External Tools](https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/generative-page-external-tools)
- [Power Pages code sites](https://learn.microsoft.com/en-us/power-pages/configure/create-code-sites)
- [GitHub Copilot CLI agent documentation](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli)
