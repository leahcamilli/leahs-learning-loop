---
title: "AI Engineer Coach: Building a Local-First VS Code Analytics Extension for AI Coding Sessions"
source: "https://github.com/microsoft/AI-Engineering-Coach"
date: "2026-05-27"
tags: [typescript, vscode-extension, analytics, agentic-ai, rule-engine, webview]
source_type: "github"
topics: [developer-tools, coding-agents]
kind: "deep-dive"
depth: 3
actionability: 1
---

## TL;DR

> AI Engineer Coach turns local logs from multiple AI coding tools into a shared session model, then uses modular analyzers and configurable rules to surface actionable engineering insights without routinely sending session data off-device. Its architecture matters because normalization cleanly separates changing log formats from reusable analytics, detection, and webview presentation.

## Key Takeaways

1. Normalize every harness’s logs into one typed session schema so analyzers and rules do not need source-specific logic.
2. Keep session analysis local and read-only; according to the lesson, model-backed features run only when explicitly invoked through VS Code’s built-in Copilot APIs.
3. Move expensive parsing, cache writes, and warm-up work into background workers to keep the VS Code extension host responsive.
4. Trace anti-pattern detection end to end: local logs → harness parser → normalized sessions → metrics and detectors → rule engine → findings → webview page.
5. Treat rule evaluation as a pipeline—load, parse, compile, validate, execute, and present—rather than scattering hardcoded checks throughout the application.
6. Add a new harness at the parser and normalization boundary; add a new anti-pattern through metrics, detectors, or the rule DSL.
7. Protect against upstream log-format drift with harness-specific parser tests, rule-engine tests, end-to-end tests, and performance benchmarks.

## Overview

AI Engineer Coach is a TypeScript-based VS Code extension that parses local logs from multiple AI coding harnesses—such as VS Code, Claude, Codex, OpenCode, and Xcode—and turns them into engineering insights. Its focus is practical: help developers understand how they use AI assistants, spot unproductive patterns, measure output, and improve prompt/context discipline without sending session data off the machine.

For working engineers, the repository is interesting for two reasons. First, it demonstrates a real multi-source analytics pipeline inside a VS Code extension: log parsing, normalization, caching, analysis, and webview rendering. Second, it implements a configurable rule engine and a set of domain-specific analyzers that convert raw assistant activity into dashboards, anti-pattern detection, context-health checks, and learning workflows.

## Key Concepts

- **Local-first analytics**: The extension is designed to analyze AI session logs entirely on the developer's machine. It reads local files in a read-only manner, avoids proprietary telemetry, and only uses model-backed features when the user explicitly invokes them through VS Code's built-in Copilot language model APIs.
- **Multi-harness parsing**: The core parser layer supports multiple log formats and sources through harness-specific modules like `parser-vscode.ts`, `parser-claude.ts`, `parser-codex.ts`, `parser-opencode.ts`, and `parser-xcode.ts`. These modules normalize heterogeneous session data into shared internal schemas so downstream analyzers can operate on a consistent representation.
- **Analyzer pipeline**: After parsing, the project runs a set of analyzers that compute higher-level metrics and views. Files such as `analyzer-dashboard.ts`, `analyzer-patterns.ts`, `analyzer-timeline.ts`, `analyzer-context.ts`, and `analyzer-insights.ts` indicate a modular pipeline where each analyzer derives a specific family of insights from the normalized session corpus.
- **Rule engine and DSL**: A major feature of the extension is its anti-pattern detection system, implemented through components like `rule-parser.ts`, `rule-compiler.ts`, `rule-engine.ts`, `rule-loader.ts`, and `rule-pipeline.ts`. This suggests a custom DSL that lets rules be authored in markdown or structured form, compiled, validated, and executed against session data.
- **VS Code webview application**: The user interface is built as a webview-driven mini application inside VS Code. Files under `src/webview/` define page-specific renderers, shared panel infrastructure, RPC wiring, sidebar navigation, and HTML generation for dashboards, explorers, editors, and learning pages.
- **Performance through workers and caching**: The repository includes dedicated worker files such as `parse-worker.ts`, `cache-write-worker.ts`, and `warm-up-worker.ts`, along with `cache.ts`. This indicates an architecture that offloads expensive parsing and cache operations to background processes to keep the extension responsive while handling potentially large log datasets.

## How It Works

The repository is structured around a classic VS Code extension split: an extension host entrypoint in `src/extension.ts`, a core analytics engine in `src/core/`, and a webview UI in `src/webview/`.

At activation time, the extension registers commands declared in `package.json`, including:

- `aiEngineerCoach.open`
- `aiEngineerCoach.reload`
- `aiEngineerCoach.exportSummary`
- `aiEngineerCoach.reviewLocalRules`

These commands are the main integration points with VS Code. The extension contributes an activity bar container and a webview-based dashboard view, so most of the product experience is delivered through a persistent panel rather than editor decorations or tree views.

### 1. Parsing and normalization

The first major subsystem is parsing. The files under `src/core/parser-*.ts` show a family of source-specific parsers:

- `parser-vscode.ts`, `parser-vscode-files.ts`, `parser-vscode-cli.ts`
- `parser-claude.ts`
- `parser-codex.ts`, `parser-codex-extra.ts`
- `parser-opencode.ts`
- `parser-xcode.ts`
- `parser-harnesses.ts`
- `parser-shared.ts`
- `parser-main.ts`

This layout strongly suggests a layered parser design:

1. Harness-specific readers understand where logs live and how each product structures them.
2. Shared helpers normalize timestamps, prompts, edits, model metadata, workspaces, and token-like fields.
3. A top-level parser orchestrates discovery across all supported harnesses and emits a common typed session model from `types.ts` and `schemas.ts`.

This is the key architectural decision that makes the rest of the app possible. Once sessions from Claude, Codex, VS Code, and others all look the same internally, the analytics layer does not need harness-specific logic everywhere.

### 2. Caching and background work

Raw AI session logs can be large and expensive to re-parse. The project addresses this with background workers and cache modules:

- `cache.ts`
- `cache-write-worker.ts`
- `parse-worker.ts`
- `warm-up-worker.ts`

The likely flow is:

```text
local session files
  -> parser workers
  -> normalized session objects
  -> cache persistence
  -> analyzer input
  -> webview page models
```

This matters in VS Code extensions because the extension host should stay responsive. Parsing in workers and writing cache artifacts asynchronously helps avoid blocking UI interactions when users open the dashboard or reload data.

### 3. Analyzer modules

The core insight generation lives in analyzer files under `src/core/`. The repository exposes several focused analyzers:

- `analyzer-dashboard.ts` for top-level scorecards and summary stats
- `analyzer-timeline.ts` for Gantt-like session views and overlap detection
- `analyzer-patterns.ts` for activity heatmaps and work-hour signals
- `analyzer-context.ts` and `context-management` helpers for prompt/context quality
- `analyzer-consumption.ts` for premium request or token-usage style measurement
- `analyzer-insights.ts`, `analyzer-flow.ts`, `analyzer-workflows.ts`, `analyzer-production.ts` for broader derived metrics
- `analyzer-images.ts` for coding screenshots or visual session moments

The project appears to use a compositional analytics approach: each analyzer computes one slice of the product, and `analyzer.ts` likely coordinates them. This keeps logic isolated by concern and makes it easier to test, which is reflected by the large number of `*.test.ts` files.

### 4. Rule engine for anti-pattern detection

One of the most technically interesting parts of the repo is the rule system. The files:

- `rule-parser.ts`
- `rule-compiler.ts`
- `rule-engine.ts`
- `rule-engine-facade.ts`
- `rule-loader.ts`
- `rule-pipeline.ts`
- `rule-trust.ts`
- `rule-equivalence.ts`
- `detector-registry.ts`
- `detectors.ts`
- `metric-engine.ts`

point to a full pipeline rather than a handful of hardcoded checks.

A reasonable mental model is:

1. Rules are authored as markdown or DSL-backed definitions.
2. The loader reads built-in and possibly local/custom rules.
3. The parser converts textual rule expressions into an internal AST or executable structure.
4. The compiler validates and optimizes the rule.
5. The metric engine exposes computed fields and aggregate metrics.
6. The engine executes the rules over sessions or aggregated features.
7. The UI presents severity, coverage, example prompts, and suggested remediations.

This is reinforced by the UI pages `page-antipatterns.ts`, `page-rule-editor.ts`, `page-rule-playground.ts`, and `page-dsl-reference.ts`. The product is not just showing static heuristics; it exposes the underlying detection language to the user for tuning and experimentation.

### 5. Webview frontend architecture

The UI lives under `src/webview/` and is organized by page rather than by low-level component framework. Notable files include:

- `panel.ts`, `panel-html.ts`, `panel-sidebar.ts`
- `panel-rpc.ts`, `panel-request-service.ts`, `panel-shared.ts`
- `render.ts`, `shared.ts`
- `page-dashboard.ts`
- `page-output.ts`
- `page-patterns.ts`
- `page-timeline.ts`
- `page-antipatterns.ts`
- `page-rule-editor.ts`
- `page-rule-playground.ts`
- `page-data-explorer.ts`
- `page-context-mgmt.ts`
- `page-learning.ts`
- `page-achievements.ts`
- `page-sdlc.ts`
- `page-skills.ts`

This suggests a lightweight in-house rendering approach instead of React. Page modules likely generate HTML fragments and bind events through a shared RPC layer. In a VS Code webview, this can be a pragmatic choice: less bundling complexity, simpler CSP management, and tighter control over payload size.

The RPC layer is important because webviews are sandboxed. The normal pattern is:

```text
webview page action
  -> postMessage / RPC request
  -> extension host handler
  -> core analysis / file reads / optional LLM invocation
  -> response sent back to webview
  -> page rerender
```

The presence of `panel-llm.ts` indicates that some UI actions can trigger optional AI-assisted features like reviewing instruction files or matching prompt patterns to community skills.

### 6. Export, summaries, and learning features

Beyond dashboards, the repo includes:

- `summary-export.ts` and `summary-export-vscode.ts`
- `page-learning.ts`, `page-learning-state.ts`, `page-learning-templates.ts`
- `page-achievements.ts`
- `page-sdlc.ts`
- `skill-cache.ts`, `panel-catalog.ts`

These indicate a product direction beyond simple observability. The extension turns usage data into outputs engineers can act on:

- exported markdown/JSON summaries
- reusable prompt skill suggestions
- quizzes based on actual behavior
- gamified achievement progress
- SDLC-stage analysis of AI usage patterns

In other words, the app is trying to close the loop from observation to improvement.

### 7. Quality and test strategy

The repository has strong evidence of engineering discipline:

- unit tests across parsers, analyzers, rules, and webview helpers
- Playwright end-to-end tests via `playwright.config.ts`
- benchmarks for parser performance and extension stability
- size checks and static analysis in scripts and CI

This is useful to study because VS Code extensions that parse real user data are easy to break with format drift. The harness-specific parser tests and rule-engine tests are likely critical to maintaining correctness as upstream tools evolve.

### 8. Build and packaging

The project uses `esbuild.mjs` for bundling and `@vscode/vsce` for packaging. The standard lifecycle is:

```bash
npm install
npm run build
npm run test
npm run package
```

`npm run package` wraps packaging logic in `scripts/package-readme-swap.mjs`, likely to prepare marketplace-friendly artifacts or swap README variants before generating the `.vsix`. The extension entrypoint is emitted as `dist/extension.js`.

Overall, the architecture is a good example of a production-style VS Code extension where the core value comes from a local analytics engine, not from simple editor commands. The repository shows how to combine file-system ingestion, typed analysis modules, a configurable rule DSL, and webview UI into a cohesive developer tool.

## Training Exercise

Build a mental model of the extension by tracing one end-to-end feature: **anti-pattern detection for AI sessions**.

### Goal

Understand how raw logs become rule-based findings shown in the webview.

### Steps

1. **Clone and install the project**

```bash
git clone https://github.com/microsoft/AI-Engineering-Coach.git
cd AI-Engineering-Coach
npm install
```

2. **Map the feature entrypoints**
   - Open `package.json` and find the commands and view contributions.
   - Open `src/extension.ts` and identify where the dashboard panel is created and where reload/export commands are registered.

3. **Trace parsing**
   - Inspect `src/core/parser-main.ts`, `src/core/parser.ts`, and one harness parser such as `src/core/parser-vscode.ts`.
   - Write down the normalized fields you think every session object must contain: timestamp, workspace, prompt text, model, harness, edits, etc.

4. **Trace the rule pipeline**
   - Read these files in order:
     1. `src/core/rule-loader.ts`
     2. `src/core/rule-parser.ts`
     3. `src/core/rule-compiler.ts`
     4. `src/core/rule-engine.ts`
     5. `src/core/rule-pipeline.ts`
   - Answer these questions in your notes:
     - Where do rules come from?
     - What intermediate representation is used?
     - How are metrics and detectors plugged in?
     - What constitutes a finding or violation?

5. **Connect the backend to the UI**
   - Open `src/webview/page-antipatterns.ts`, `src/webview/page-rule-editor.ts`, and `src/webview/panel-rpc.ts`.
   - Identify how the page requests rule results and how data is rendered back to the user.

6. **Run the tests for just this subsystem**

```bash
npm run test -- rule-engine
npm run test -- antipatterns
```

If your shell does not pass the filter correctly, run the full suite with `npm test` and inspect the relevant test files:
- `src/core/rule-engine.test.ts`
- `src/core/rule-compiler.test.ts`
- `src/core/antipatterns-e2e.test.ts`

7. **Create a design note**
   - Write a one-page summary with four sections:
     - Inputs
     - Processing stages
     - UI integration
     - Failure modes

8. **Stretch exercise: add a tiny rule**
   - Read `docs/AUTHORING_RULES.md`.
   - Add or modify a simple local anti-pattern rule, then use the Rule Editor or Playground page to validate it against sample data.

### Deliverable

Produce a short architecture diagram like this:

```text
local logs
 -> harness parser
 -> normalized sessions
 -> metrics/detectors
 -> rule engine
 -> findings
 -> webview anti-pattern page
```

Then explain, in 5-10 bullet points, where you would extend the system to support a new harness or a new anti-pattern category.

## Test Yourself

<details><summary>Why is the normalized session model the central architectural decision?</summary>

It converts heterogeneous VS Code, Claude, Codex, OpenCode, and Xcode logs into a common representation. Downstream analyzers, rules, and UI models can therefore remain independent of each harness’s file locations and formats.

</details>

<details><summary>How does a raw session become an anti-pattern finding in the webview?</summary>

A harness parser reads local logs and emits normalized sessions; metrics and detectors derive features that the compiled rules evaluate. The resulting findings are passed through the extension host’s RPC boundary and rendered by the anti-pattern webview page.

</details>

<details><summary>Where should you extend the system for a new harness versus a new anti-pattern?</summary>

A new harness belongs in the source-specific parser and shared normalization layer, supported by parser tests. A new anti-pattern belongs in the rule definitions and, when necessary, the metric engine or detector registry, with rule-engine and end-to-end coverage.

</details>

## Further Reading

- [Visual Studio Code Extension API](https://code.visualstudio.com/api)
- [VS Code Webview API Guide](https://code.visualstudio.com/api/extension-guides/webview)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [esbuild Documentation](https://esbuild.github.io/)
- [Playwright Documentation](https://playwright.dev/docs/intro)
