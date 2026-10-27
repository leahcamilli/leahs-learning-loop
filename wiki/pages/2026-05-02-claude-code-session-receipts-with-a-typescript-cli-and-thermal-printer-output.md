---
title: "Claude Code session receipts with a TypeScript CLI and thermal printer output"
source: "https://github.com/chrishutchinson/claude-receipts"
date: "2026-05-02"
tags: [typescript, cli, claude-code, escpos, receipts]
source_type: "github"
topics: [developer-tools, claude]
kind: "deep-dive"
depth: 3
actionability: 1
---

## TL;DR

> Claude Receipts is a thin TypeScript orchestration layer that turns completed Claude Code sessions into accurate, polished receipts by combining `ccusage` accounting with local transcript metadata. Its normalized receipt model and separate renderers make it straightforward to add fields or support HTML, terminal, and ESC/POS outputs without duplicating core logic.

## Key Takeaways

1. Use Claude Code’s `SessionEnd` hook to run `claude-receipts generate` automatically when a coding session finishes.
2. Delegate token and cost accounting to `ccusage session --id <session-id>` instead of duplicating pricing rules that can drift over time.
3. Combine authoritative `ccusage` data with transcript JSONL metadata such as session name, timestamps, project path, and message counts.
4. Build one normalized receipt model, then pass it to independent HTML, console, and ESC/POS rendering backends.
5. Resolve settings deterministically in this order: CLI flag, `~/.claude-receipts.config.json`, `geoip-lite`, then the fallback `The Cloud`.
6. Treat thermal printers as a device-specific output adapter supporting ESC/POS over USB or raw TCP, rather than mixing hardware concerns into receipt generation.
7. Run the CLI on Node 22+; generated HTML receipts are stored under `~/.claude-receipts/projects/`.

## Overview
These notes cover **Claude Receipts**, a TypeScript CLI that converts Claude Code sessions into receipt-style summaries showing token usage, model-level breakdowns, session metadata, and total cost. The tool integrates with Claude Code’s `SessionEnd` hook, uses `ccusage` as the source of truth for pricing and token accounting, parses local transcript artifacts for context, and renders output as HTML, terminal text, or ESC/POS thermal printer output.

This is a useful reference for building polished developer tooling around an existing CLI ecosystem. It demonstrates a clean architecture for command parsing, local configuration, event-hook integration, data fetching via another CLI, transcript parsing, and multi-backend rendering. It is especially relevant if I want to add new output formats, extend receipt fields, or study how modern Node/TypeScript code can interface with older hardware like receipt printers.

## Key Concepts
- **SessionEnd hook integration**: The tool installs itself into Claude Code by updating `~/.claude/settings.json` and registering a `SessionEnd` hook. That hook runs `claude-receipts generate` automatically at the end of a coding session, making receipt creation feel native and event-driven.
- **Authoritative usage via `ccusage`**: The project does not estimate costs from transcript text. Instead it shells out to `ccusage session --id <session-id>` to retrieve accurate token and pricing data, reducing duplication and pricing drift.
- **Transcript metadata parsing**: Session usage comes from `ccusage`, but session context comes from Claude transcript JSONL files. Parsing those files fills in details like session name, timestamps, project path, and message counts.
- **Multi-target rendering**: A single receipt model is rendered into multiple formats: HTML, terminal-friendly ASCII, and ESC/POS-compatible printer output. This keeps business logic separate from presentation logic.
- **Config-driven behavior**: Persistent settings live in `~/.claude-receipts.config.json`. CLI flags can override config values at runtime, allowing both automation and ad hoc usage.
- **Hardware-aware printer support**: Thermal printing targets ESC/POS-compatible devices such as Epson TM-T88V-style printers over USB or raw TCP, requiring low-level formatting and device-aware output handling.

## How It Works
The CLI entrypoint is in `src/cli.ts`, exposed through `bin/claude-receipts.js`, with command parsing handled by `commander`. The main subcommands are organized under `src/commands/`:

- `generate.ts` for receipt generation
- `setup.ts` for installing or removing the Claude Code hook
- `config.ts` for reading, setting, or resetting persistent configuration

The `generate` flow is roughly:

1. Resolve runtime options from CLI flags and config via `src/core/config-manager.ts`
2. Determine which Claude session to process
3. Fetch authoritative usage and cost data through `src/core/data-fetcher.ts`
4. Parse the local transcript with `src/core/transcript-parser.ts`
5. Build a normalized receipt model in `src/core/receipt-generator.ts`
6. Render the receipt through one or more backends:
   - HTML via `src/core/html-renderer.ts`
   - Console output via helpers like `src/utils/ascii-art.ts` and `src/utils/formatting.ts`
   - Printer output via `src/core/thermal-printer.ts`

A key design decision is that accounting logic stays outside the project. `data-fetcher.ts` calls `ccusage` using `execa`, which avoids re-implementing token pricing rules inside this codebase. Transcript parsing then adds the metadata `ccusage` does not provide, such as human-readable names and local project context. The result is a receipt that is both accurate and informative.

Configuration is intentionally simple and lives in `~/.claude-receipts.config.json`. Settings include values such as `location`, `timezone`, and `printer`. Resolution follows a clear precedence order: CLI flag first, then config file, then `geoip-lite`, and finally the fallback string `The Cloud`. This is a good CLI UX pattern because behavior is deterministic and easy to reason about.

The `setup` command modifies Claude’s global settings to register the `SessionEnd` hook. In hook mode, Claude sends session information over stdin, which the tool uses to identify the completed session. The README notes that generated HTML receipts may be auto-opened in the browser, tightening the feedback loop and making the tool feel integrated rather than bolted on.

Rendering is where the project becomes a product rather than a raw report generator. HTML receipts are saved under `~/.claude-receipts/projects/`, console rendering provides a lightweight text view, and thermal printing produces narrow-paper layouts for ESC/POS printers. The receipt includes branding touches such as a Claude ASCII logo and a QR code pointing to the repository.

The repository also includes a separate `worker/` directory, which appears to be an adjacent deployment target rather than part of the local CLI path. Its structure suggests a Cloudflare Worker-style service with routes, validation helpers, rate limiting, and page/API separation. That likely supports hosted rendering or sharing workflows.

A practical mental model for the pipeline is:

```text
Claude Code SessionEnd
-> claude-receipts generate
-> read config
-> resolve session id
-> ccusage fetch for costs/tokens
-> transcript parse for metadata
-> compose receipt view-model
-> render: html | console | printer
```

Implementation details worth remembering:

- Node 22+ is required
- `fs-extra` is used for filesystem ergonomics
- `ora`, `chalk`, and `boxen` improve CLI UX
- `usb` is present for direct printer interaction on supported systems

Overall, this is a strong example of a thin orchestration layer connecting external CLI integration, local file parsing, configuration management, and multiple output adapters.

## Test Yourself

<details><summary>Why does Claude Receipts call `ccusage` instead of calculating token costs from transcripts?</summary>

The lesson describes `ccusage` as the authoritative source for token and pricing data. Delegating accounting avoids duplicated pricing logic and reduces the risk of cost calculations drifting out of date.

</details>

<details><summary>What information comes from transcripts, and how does it complement `ccusage`?</summary>

Transcript JSONL files provide context such as session names, timestamps, project paths, and message counts. That metadata is combined with `ccusage` token and cost figures to produce an accurate and informative receipt.

</details>

<details><summary>How does the architecture make a new output format easier to add?</summary>

Receipt generation first creates a normalized view-model that is independent of presentation. A new renderer can consume that model alongside the existing HTML, console, and thermal-printer adapters without reimplementing session resolution or accounting.

</details>

## Personal Notes
Building Claude Code Session Receipts with a TypeScript CLI and Thermal Printer Output

Source: https://github.com/chrishutchinson/claude-receipts
Notion page: https://www.notion.so/Building-Claude-Code-Session-Receipts-with-a-TypeScript-CLI-and-Thermal-Printer-Output-35401bb0839a81e3a422cb25bb14b13b

Tags: typescript, cli, claude-code, escpos, html, session-hooks

Overview

Claude Receipts is a TypeScript CLI that turns Claude Code sessions into itemized receipts showing token usage, model breakdowns, and session cost. It integrates with Claude Code's `SessionEnd` hook, fetches authoritative usage data via `ccusage`, parses transcript metadata from Claude session files, and renders the result as HTML, terminal output, or ESC/POS-compatible thermal printer output.

This project is interesting to engineers who want to understand how to build polished developer tooling around an existing CLI ecosystem: command parsing, local config management, shelling out to another tool for source-of-truth data, parsing local artifacts, and supporting multiple output backends. It is also a good example of a small but complete product with a clear flow from event hook to data collection to formatted rendering.

Key Concepts

  *   SessionEnd hook integration: The tool installs itself into Claude Code by modifying `~/.claude/settings.json` and registering a `SessionEnd` hook. That hook invokes `claude-receipts generate`, allowing receipt generation to happen automatically when a coding session ends. This is the event bridge that makes the tool feel native rather than manual.
  *   Authoritative usage via ccusage: Instead of estimating cost from transcript content, the project delegates pricing and token accounting to `ccusage`. The CLI calls `ccusage session --id <session-id>` so it can retrieve accurate totals and per-model breakdowns. This keeps cost logic out of the project and reduces drift when model pricing or accounting behavior changes.
  *   Transcript metadata parsing: Usage totals come from `ccusage`, but session context comes from Claude transcript JSONL files. The transcript parser extracts information such as session name, timestamps, project path, and message counts. Combining these two data sources produces a receipt that is both financially accurate and context-rich.
  *   Multi-target rendering: The project supports several output modes: HTML, console, and thermal printer. The core receipt data is assembled once, then different renderer modules format the same logical receipt into browser-friendly markup, terminal ASCII, or ESC/POS printer commands. This separation helps keep business logic independent from presentation.
  *   Config-driven CLI behavior: The tool stores persistent settings in `~/.claude-receipts.config.json`, including location, timezone, and printer interface. Command-line flags can override config at runtime, and defaults are used when no explicit value is present. This is a common pattern for developer tools that need both automation and ad hoc control.
  *   Hardware-aware thermal printing: Thermal printer output targets Epson TM-T88V-style ESC/POS devices over USB or raw TCP. Supporting this requires handling device selection, formatting constraints, and command-oriented output rather than high-level print dialogs. It is a practical example of bridging modern Node.js code with old-school peripheral protocols.

How It Works

The repository is centered on a TypeScript CLI entrypoint in `src/cli.ts`, exposed through `bin/claude-receipts.js`. Command parsing is handled by `commander`, and the user-facing subcommands map cleanly to files under `src/commands/`:

- `generate.ts` handles receipt creation - `setup.ts` installs or removes the Claude Code hook - `config.ts` displays, sets, or resets persistent configuration

At a high level, the flow for `
