---
title: "Agentic Power BI Development with a Plugin Marketplace for Claude Code and Copilot CLI"
source: "https://github.com/data-goblin/power-bi-agentic-development"
date: "2026-05-26"
tags: [power-bi, fabric, agentic-development, claude-code, copilot-cli, semantic-models]
source_type: "github"
topics: [power-bi-and-fabric, ai-agents, coding-agents, automation-workflows]
kind: "deep-dive"
depth: 3
actionability: 1
---

## TL;DR

> The repository turns AI-assisted Power BI development into a layered workflow of domain-specific skills, specialized review agents, and deterministic validation hooks. This matters because scripts can catch structural and semantic errors that prompting alone may miss.

## Key Takeaways

1. Treat the repository root as a marketplace catalog; install only the child plugins needed for domains such as PBIP, semantic models, reports, Tabular Editor, or Fabric administration.
2. Use skills for reusable guidance on tasks such as TMDL editing, DAX authoring, Power Query development, Deneb visuals, and Fabric CLI operations.
3. Delegate multi-step audits to specialized agents such as `pbip-validator`, `semantic-model-auditor`, and the content-specific report reviewers.
4. Rely on hooks and executable validators to check PBIR, TMDL, report bindings, DAX references, referential integrity, and model metadata after changes.
5. Keep local PBIP and Power BI Desktop workflows distinct from remote Fabric CLI administration while composing them when a task crosses environments.
6. The repository’s central design claim is that reliable agentic BI development requires scoped instructions, focused reviewers, and mechanical post-action checks—not prompting alone.

## Overview

This repository is not a traditional C# application despite the language tag; it is an Anthropic-format plugin marketplace that packages domain-specific instructions, autonomous agents, validation hooks, and helper scripts for AI coding agents working on Power BI and Microsoft Fabric. Its goal is to make tools like Claude Code and GitHub Copilot CLI materially better at understanding and modifying semantic models, PBIP/TMDL/PBIR files, Tabular Editor assets, and Fabric administration workflows.

A working engineer would care because the repo codifies repeatable operational knowledge: how to author DAX and Power Query safely, how to validate report and model metadata automatically, and how to split responsibilities between promptable skills, autonomous review agents, and deterministic shell/PowerShell hooks. In practice, it acts like an opinionated extension layer for AI-assisted BI engineering, with plugin boundaries aligned to real Power BI work domains.

## Key Concepts

- **Plugin marketplace architecture**: The root of the repository is a marketplace catalog, not an installable plugin by itself. The `.claude-plugin/marketplace.json` file advertises multiple child plugins under `plugins/`, and each child plugin has its own `.claude-plugin/plugin.json` manifest. This lets users register the marketplace once and then install only the Power BI capability areas they need.
- **Skills as embedded domain playbooks**: Skills live under `plugins/*/skills/*/SKILL.md` and provide focused operational guidance for tasks like editing TMDL, using Fabric CLI, writing DAX, or working with Deneb visuals. In Claude Code and Copilot CLI, these are loaded as instruction artifacts that can activate from context or be called explicitly. They are effectively reusable task-specific knowledge modules for agents.
- **Agents for multi-step review and validation**: Agent files such as `pbip-validator.agent.md`, `semantic-model-auditor.agent.md`, and `deneb-reviewer.agent.md` define specialized subprocess personas for complex review flows. Instead of a single chat turn trying to do everything, the main agent can delegate to these targeted reviewers. This is useful when the task requires iterative checking, domain-specific heuristics, or artifact-focused auditing.
- **Hooks as deterministic guardrails**: Hooks are shell or PowerShell scripts registered through `hooks.json` and configured with local `config.yaml` files. They run automatically after matching tool activity, rather than relying on the LLM to remember validation steps. In this repo, hooks enforce PBIR and TMDL correctness, report binding integrity, DAX reference validity, and semantic-model metadata hygiene.
- **Power BI artifact-centric organization**: The plugins are divided by actual engineering surface area: `pbip`, `pbi-desktop`, `semantic-models`, `reports`, `tabular-editor`, `fabric-cli`, and `fabric-admin`. That separation mirrors the different file formats, APIs, and workflows involved in Power BI development. It also makes installation modular so teams can adopt only the pieces relevant to their stack.
- **Hybrid local and remote operations**: Some plugins target local authoring environments, such as Power BI Desktop connections or direct PBIP file editing, while others target remote administration through Fabric CLI. The combination matters because real Power BI engineering spans local project files, in-memory desktop models, and cloud-hosted workspace artifacts. The marketplace treats those as connected but distinct execution contexts.

## How It Works

The repository is structured as a **plugin marketplace** with a lightweight root and multiple installable child plugins.

At the top level:

- `.claude-plugin/marketplace.json` declares the marketplace catalog.
- `plugins/<name>/` contains each actual plugin.
- `useful-stuff/` contains reusable supporting assets such as defensive hooks, agent settings, and status-line scripts.
- `scripts/validate-plugins.sh` and `.github/workflows/validate-plugins.yml` indicate the repo validates plugin structure in CI.
- `release-notes/` shows the repo is versioned and frequently updated, which matters because the instruction layout is still evolving.

Each plugin follows a recognizable architecture:

- `.claude-plugin/plugin.json` — plugin manifest
- `skills/.../SKILL.md` — task-oriented instructions and references
- `agents/*.agent.md` — specialized autonomous reviewers/helpers
- `commands/*.md` — prescriptive entry points exposed as commands
- `hooks/` — deterministic post-tool validations and helper scripts
- optional scripts, examples, and references

### Main plugin areas

**1. `plugins/pbip` — file-based Power BI project authoring**

This plugin is centered on PBIP project structure and two critical text-based formats:

- **TMDL** for semantic model definitions
- **PBIR** for report metadata

The code and assets here show a practical validation pipeline:

- `skills/pbip`, `skills/tmdl`, and `skills/pbir-format` teach the agent how these file formats are organized and edited.
- `agents/pbip-validator.agent.md` gives the agent a dedicated reviewer for project structure and schema correctness.
- `hooks/validate-pbir.sh`, `hooks/validate-report-binding.sh`, and `hooks/validate-tmdl.sh` enforce correctness after file edits.
- `hooks/bin/tmdl-validate-*` bundles platform-specific validator binaries, which is a notable implementation detail: validation is not purely prompt-based; it relies on executable tooling.
- `hooks/config.yaml` lets teams selectively disable checks.

The data flow is: the agent edits PBIP/TMDL/PBIR files → a hook fires based on matching file operations → shell scripts validate syntax and bindings → failures are surfaced immediately so the agent can repair before drift accumulates.

**2. `plugins/pbi-desktop` — live model interaction in Power BI Desktop**

This plugin focuses on working against a running Desktop model rather than static project files.

Key assets include:

- `skills/connect-pbid/SKILL.md` for connecting to and manipulating the live model
- `skills/connect-pbid/daxlib.sh`, likely a shell helper for DAX-related interactions
- `agents/query-listener.agent.md` for capturing DAX queries emitted by visuals
- Hook scripts like `check-referential-integrity.ps1` and `snapshot-model.ps1`
- `hooks/pbi-hooks.sh`, `hooks/hooks.json`, and `hooks/config.yaml` for orchestration and toggles

The mechanics here are interesting because they add **runtime awareness** to agent behavior. After changes to a model or relationship, the hooks can validate DAX references, enforce required measure metadata, check referential integrity, and refresh cached metadata snapshots. This reduces a common failure mode in AI-assisted BI work: the model compiles syntactically, but is semantically inconsistent.

**3. `plugins/semantic-models` — model logic and quality reviews**

This plugin is instructional and review-oriented rather than hook-heavy.

It includes skills for:

- DAX authoring and optimization
- Power Query / M development
- naming standardization
- lineage analysis
- refresh troubleshooting
- broader model review

Its main agent, `semantic-model-auditor.agent.md`, is designed as a focused reviewer for model quality, memory usage, DAX issues, and design problems. Architecturally, this is the repository's pattern for “deep expertise”: put broad task knowledge in skills, then provide a narrower audit agent for structured review passes.

**4. `plugins/reports` — report design and custom visuals**

This plugin covers report-facing artifacts and custom visual authoring patterns:

- Deneb / Vega / Vega-Lite
- R visuals
- Python visuals
- SVG via DAX measures
- Theme JSON edits
- PBIR CLI usage

The paired reviewer agents (`deneb-reviewer`, `svg-reviewer`, `r-reviewer`, `python-reviewer`) illustrate a scalable architecture: each content type gets its own style-and-correctness reviewer instead of one generic “report reviewer.” That separation improves signal quality because each reviewer can enforce conventions specific to its language and rendering model.

**5. `plugins/tabular-editor` — Tabular Editor automation and BPA workflows**

This plugin mixes skills, commands, and executable code:

- `skills/bpa-rules`, `skills/c-sharp-scripting`, `skills/te2-cli`, `skills/te-docs`
- `commands/suggest-rule.md`
- `agents/bpa-expression-helper.agent.md`
- `scripts/bpa_rules_audit.py`

The presence of `bpa_rules_audit.py` is one of the clearest examples that the repo is not just instruction text. There is actual supporting automation for analyzing or generating Best Practice Analyzer-related content. The `te-docs` skill also references an external CLI (`pbi-search`), suggesting the repo expects agents to use real tooling for documentation retrieval instead of hallucinating vendor behavior.

**6. `plugins/fabric-cli` and `plugins/fabric-admin` — remote platform operations**

These plugins target cloud-side operations using Fabric CLI (`fab`) and admin workflows.

Notable structure:

- `skills/fabric-cli/SKILL.md` plus a large `references/` directory covering object types such as dashboards, gateways, deployment pipelines, connections, and notebooks
- examples in notebook form under `examples/`
- commands like `audit-context.md`
- `fabric-admin/skills/audit-tenant-settings/` with Python scripts `audit-tenant-settings.py` and `generate_audit_pdf.py`

This reveals a second major pattern in the repo: **instruction + reference corpus + automation script**. The agent can use the skill for high-level workflow guidance, dip into references for object-specific details, and execute Python or CLI scripts for evidence-based auditing.

### Cross-cutting patterns

Several implementation choices appear throughout the repository:

1. **Instructions are first-class artifacts.** The `SKILL.md` and `*.agent.md` files are the primary logic surface.
2. **Validation is externalized into scripts.** Shell, PowerShell, Python, and packaged binaries do the deterministic work.
3. **Configuration is local and explicit.** Hook behavior is controlled with plugin-local `config.yaml` files.
4. **Compatibility matters.** The README documents Copilot CLI support details, plugin install modes, and caveats like `CLAUDE_PLUGIN_ROOT` handling and Windows MAX_PATH issues.
5. **Tooling is compositional.** The repo expects agents to combine Power BI Desktop access, file edits, Tabular Editor automation, and Fabric CLI operations depending on the task.

### Practical execution model

A realistic end-to-end flow using this marketplace looks like this:

1. Register the marketplace with Claude Code or Copilot CLI.
2. Install one or more child plugins, for example `pbip`, `semantic-models`, and `reports`.
3. Ask the agent to modify a PBIP project or semantic model.
4. The agent loads relevant skills from the installed plugins.
5. If the task needs review, it can delegate to a specialized agent such as `pbip-validator` or `semantic-model-auditor`.
6. After file writes or model modifications, hooks fire and run shell/PowerShell validation scripts.
7. Validation failures are fed back into the agent loop, enabling automatic correction.

That architecture is the core lesson of the repository: effective agentic development for BI is not “better prompting,” but a layered system of scoped instructions, specialized subagents, and deterministic post-action checks.

## Training Exercise

Build a minimal Power BI agent workflow around the `pbip` and `semantic-models` plugins, then observe how skills and hooks complement each other.

### Goal

Simulate a text-first Power BI engineering workflow where an agent edits PBIP/TMDL artifacts and then validates them automatically.

### Prerequisites

- Claude Code or GitHub Copilot CLI
- Git installed
- A local clone of a sample PBIP project, or any folder with representative `definition.pbir` / TMDL-like files
- On Windows, enable long paths if needed:

```powershell
git config --system core.longpaths true
```

### Step 1: Register the marketplace

Using Claude Code:

```bash
claude plugin marketplace add data-goblin/power-bi-agentic-development
claude plugin install pbip@power-bi-agentic-development
claude plugin install semantic-models@power-bi-agentic-development
```

Or with Copilot CLI:

```bash
copilot plugin marketplace add data-goblin/power-bi-agentic-development
copilot plugin install pbip@power-bi-agentic-development
copilot plugin install semantic-models@power-bi-agentic-development
```

### Step 2: Verify what loaded

Inside the interactive CLI session, inspect the environment:

```text
/env
/plugin list
/skills list
/skills info pbip
```

Look for the `pbip`, `tmdl`, and semantic-model-related skills. This confirms the agent now has targeted instructions available.

### Step 3: Create a tiny PBIP-style sandbox

Make a scratch directory with a fake report metadata file and a fake model folder:

```bash
mkdir -p demo-pbip/report demo-pbip/model
cat > demo-pbip/report/report.json <<'EOF'
{
  "name": "Sales Report",
  "version": "1.0"
}
EOF
```

If you have a real PBIP project, use that instead; the exercise works better with real files because the hooks can validate meaningful structure.

### Step 4: Ask the agent to perform an artifact edit

Use a prompt like:

```text
Review this PBIP-like project. Explain the expected structure, identify likely missing PBIR/TMDL metadata, and propose fixes. Then validate the result using the installed pbip workflow.
```

What you should observe:

- The agent uses the **skill** to reason about PBIP/TMDL/PBIR conventions.
- If supported in your environment, it can invoke the **pbip-validator agent** for a focused review.
- File writes can trigger **hooks** that run structural checks.

### Step 5: Intentionally introduce an error

Edit a report or TMDL-related file to include something obviously inconsistent, such as a wrong path, malformed JSON, or missing expected field. Then ask:

```text
Validate this project and fix the errors reported by hooks or validators.
```

This step demonstrates the key repository design principle: let deterministic scripts catch issues, and let the LLM repair them.

### Step 6: Compare skill reasoning vs hook enforcement

Document the difference between these two behaviors:

1. **Skill behavior** — the agent explains what a good PBIP project should look like.
2. **Hook behavior** — scripts actually block or report invalid structure.

Write a short note answering:

- Which problems were detected by instruction alone?
- Which required script-based validation?
- How would you extend this pattern for your own BI team?

### Optional extension

Install the `reports` plugin and ask the agent to review a Deneb spec or theme JSON. Then compare the `reports` review-agent pattern to the `pbip` hook-validation pattern. The takeaway should be that different artifact types need different control surfaces: some are best reviewed semantically, others must be validated mechanically.

## Test Yourself

<details><summary>What different roles do skills, agents, and hooks play in this marketplace?</summary>

Skills provide task-specific operating guidance, agents conduct focused multi-step reviews, and hooks run deterministic checks after relevant actions. The repository uses all three layers so reasoning and mechanical validation complement each other.

</details>

<details><summary>Why is the repository root described as a marketplace rather than a plugin?</summary>

Its marketplace manifest advertises multiple installable child plugins under `plugins/`. Users register the marketplace once, then install only the capability areas relevant to their Power BI or Fabric workflows.

</details>

<details><summary>How does the `pbip` plugin demonstrate the repository’s core execution model?</summary>

An agent edits PBIP, TMDL, or PBIR artifacts using embedded skills; specialized review can then inspect the work, while hooks validate syntax, structure, and bindings. Reported failures return to the agent for repair before errors accumulate.

</details>

## Further Reading

- [Anthropic Claude Code Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [GitHub Copilot CLI Plugin Reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)
- [Power BI Project (PBIP) and TMDL Documentation](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview)
- [Microsoft Fabric CLI Documentation](https://learn.microsoft.com/en-us/fabric/fundamentals/fabric-command-line-interface)
- [Tabular Editor Documentation](https://docs.tabulareditor.com/)
