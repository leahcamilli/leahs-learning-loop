---
title: "cb365: Safe Microsoft 365 CLI on Microsoft Graph"
source: "https://github.com/nz365guy/cb365"
date: "2026-04-17"
tags: [golang, cli, microsoft-graph, microsoft-365, automation]
source_type: "github"
topics: [developer-tools, automation-workflows]
kind: "deep-dive"
depth: 3
actionability: 1
---

## TL;DR

> cb365 shows how to make Microsoft 365 automation consistent and safer by combining workload-based commands, centralized Microsoft Graph access, secure credential storage, predictable output, and explicit guardrails. These patterns matter because they reduce fragmented authentication logic and lower the risk of unintended high-impact actions.

## Key Takeaways

1. Organize CLI commands by Microsoft 365 workload—such as `todo`, `mail`, `calendar`, `teams`, and `sharepoint`—to keep operations discoverable and aligned with Microsoft Graph domains.
2. Centralize authentication and Graph transport behavior so individual command handlers do not implement OAuth, credential refresh, or HTTP policies independently.
3. Use profiles to support multiple tenants and authentication modes, including delegated device-code authentication and app-only authentication with client secrets or certificates.
4. Prefer OS-native keychains for credentials; cb365 reportedly falls back to AES-256-GCM encrypted file storage for headless environments.
5. Send structured `--json` or `--plain` results to stdout and human-readable status information to stderr so commands compose reliably in shell pipelines.
6. Require explicit intent for write and destructive operations through guardrails such as `--dry-run`, `--confirm`, and `--force`.
7. Expose Microsoft Graph constraints early: the lesson states that To Do is delegated-only, Loop requires app-only authentication and SharePoint Embedded setup, and OneDrive uploads are limited to small files in the documented behavior.

## Overview

These notes cover **cb365**, a Go-based CLI that wraps Microsoft Graph to provide a consistent, scriptable interface to Microsoft 365 services such as To Do, Mail, Calendar, Contacts, Planner, Teams, SharePoint, OneDrive, and Loop. The project is notable not only for its workload coverage, but for its practical engineering choices: Cobra-based command structure, a shared Graph client layer, secure credential storage, and explicit safety guardrails for high-impact actions.

This matters because Microsoft 365 automation often becomes fragmented across one-off scripts, custom OAuth handling, and inconsistent API calls. cb365 presents a reusable pattern for building operational tooling that is secure, automation-friendly, and predictable for both humans and AI agents.

## Key Concepts

- **Workload-oriented CLI design**: The CLI is grouped by Microsoft 365 workload, with command families like `todo`, `mail`, `calendar`, `teams`, and `sharepoint`. This keeps commands discoverable and aligns the surface area with Microsoft Graph domains.
- **Profile-based authentication**: cb365 supports delegated device-code auth and app-only auth via client secrets or certificates. Profiles allow multiple tenants or auth modes to coexist and be selected globally or per command.
- **Shared Graph client layer**: Graph access is centralized under `internal/graph` rather than being implemented ad hoc in each command. This keeps authentication, transport behavior, and HTTP customization consistent.
- **Secure token and secret handling**: The tool prefers OS-native keychains and falls back to AES-256-GCM encrypted file storage on headless systems. This is especially useful for unattended automation.
- **Machine-readable output contracts**: Commands support `--json` and `--plain`, with structured output sent to stdout and human-readable status sent to stderr. This follows a strong Unix-style scripting pattern.
- **Hardcoded safety enforcement**: Safety is built into write and destructive operations with flags like `--dry-run`, `--confirm`, and `--force`, creating explicit intent boundaries for operators and automation.

## How It Works

The repository appears to follow a layered CLI architecture.

At the top, `cmd/cb365` contains the Cobra entrypoints. Files such as `main.go` and `root.go` define the executable, global flags, and base command wiring. Workload-specific files like `todo.go`, `mail.go`, `calendar.go`, `teams.go`, `sharepoint.go`, and `loop.go` register subcommands and bind flags. This makes the command tree easy to inspect in code and keeps workload behavior localized.

Authentication is encapsulated in `internal/auth`. Based on the repo structure, files such as `auth.go` and `credential.go` likely handle profile resolution and login flows, while `keyring.go` manages native secret storage and `store_file.go` supports encrypted fallback storage. This separation prevents command handlers from needing to know whether credentials came from device code, client secret, or certificate auth.

Graph access is centralized in `internal/graph`. A file like `client.go` likely constructs the Microsoft Graph SDK client using Kiota and Azure Identity components, while `transport.go` may define shared HTTP behavior or request policies. Centralizing this logic reduces duplication and helps ensure all workloads behave consistently.

Output handling is isolated in `internal/output/output.go`. That is a practical choice for a CLI intended for scripting: commands can return normalized data and let a shared renderer decide whether to emit JSON, plain text, or human-readable output. The documented stdout/stderr split is especially important for composing cb365 in shell pipelines.

A likely execution path is:

1. User runs a command such as `cb365 todo tasks list --list "My Tasks" --json`
2. Cobra routes the request to the handler in `cmd/cb365/todo.go`
3. The handler resolves the active or explicitly selected auth profile
4. `internal/auth` loads or refreshes credentials
5. `internal/graph` constructs an authenticated Graph client
6. The command performs the workload-specific Graph operation
7. Results are normalized and passed to `internal/output`
8. Structured data is written to stdout; status and informational text go to stderr

The project also reflects strong operational concerns: zero runtime dependencies, signed releases, CI scanning, and reliance on Microsoft-supported libraries such as `azidentity` and `msgraph-sdk-go`. That suggests the repo intentionally minimizes custom security-sensitive code while still providing custom CLI, storage, and safety logic.

Testing seems to be a first-class concern as well. The presence of matching `*_test.go` files for commands and an integration suite under `test/integration/integration_test.go` suggests both command-layer behavior and end-to-end flows are validated. For a CLI wrapper around external APIs, this is especially valuable because many failures occur at integration boundaries.

Finally, cb365 surfaces Microsoft Graph product constraints directly in the CLI:

- To Do is delegated-only because Graph does not support app permissions for it
- Loop uses app-only auth and depends on SharePoint Embedded setup
- OneDrive uploads are currently limited to small files in documented behavior

That is a useful design trait: constraints are made visible early so automation fails predictably instead of hiding API limits until runtime.

## Test Yourself

<details><summary>Why does cb365 centralize Microsoft Graph access instead of implementing it separately in every command?</summary>

A shared Graph layer keeps authentication, transport behavior, and HTTP customization consistent across workloads. It also reduces duplicated security-sensitive code and makes changes easier to apply globally.

</details>

<details><summary>How does cb365 make its output suitable for automation?</summary>

It supports machine-readable modes such as `--json` and `--plain`, writes structured results to stdout, and sends status messages to stderr. Scripts can therefore parse results without human-readable messages corrupting the data stream.

</details>

<details><summary>What mechanisms establish an explicit intent boundary around high-impact operations?</summary>

The lesson identifies `--dry-run`, `--confirm`, and `--force` as hardcoded safety controls. Together they let users preview changes and require deliberate authorization before write or destructive actions proceed.

</details>

## Personal Notes

cb365: Building and Using a Safe Microsoft 365 CLI on Microsoft Graph

Source: https://github.com/nz365guy/cb365
Notion page: https://www.notion.so/cb365-Building-and-Using-a-Safe-Microsoft-365-CLI-on-Microsoft-Graph-34501bb0839a810c90d4fcd71ba07906

Tags: golang, cli, microsoft-graph, microsoft-365, entra-id, automation

Overview

cb365 is a Go-based command-line tool that wraps Microsoft Graph to provide scriptable access to Microsoft 365 workloads such as To Do, Mail, Calendar, Contacts, Planner, Teams, SharePoint, OneDrive, and Loop. Instead of writing custom Graph API code for each workflow, engineers can use a single binary with consistent commands, structured JSON output, and profile-based authentication.

What makes this repo interesting is not just the feature list, but the architecture choices behind it: Cobra-based command organization, a shared Graph client layer, secure credential storage using OS keychains or encrypted file fallback, and hardcoded safety rules around destructive or high-impact operations. It is especially relevant for platform engineers, automation developers, and AI-agent builders who need reliable M365 automation without embedding OAuth and Graph plumbing into every script.

Key Concepts

  *   Workload-oriented CLI design: The CLI is organized by Microsoft 365 workload, with command groups like `todo`, `mail`, `calendar`, `teams`, and `sharepoint`. This maps cleanly to Graph domains and makes commands discoverable while keeping flag semantics consistent across features.
  *   Profile-based authentication: cb365 supports delegated device-code auth and app-only auth using client secrets or certificates. Profiles let users keep multiple tenants or auth modes side by side, then switch globally or per-command using `--profile`.
  *   Shared Graph client layer: Rather than having each command build its own HTTP requests, the repo centralizes Graph access under `internal/graph`. This makes transport behavior, authentication, and HTTP customization consistent across all workloads.
  *   Secure token and secret handling: The project avoids plaintext credential storage by using OS-native keychains where possible and an AES-256-GCM encrypted file fallback for headless Linux. This is important because the tool is intended for automation and agent use, where unattended credentials are common.
  *   Machine-readable output contracts: Every command supports human output and machine-oriented output via `--json` or `--plain`. The design sends readable status to stderr and structured data to stdout, which is a practical Unix pattern for scripting and pipeline composition.
  *   Hardcoded safety enforcement: cb365 bakes in safety rules for writes, deletes, mail sends, and calendar changes rather than treating them as optional UI hints. Flags like `--dry-run`, `--confirm`, and `--force` create explicit intent boundaries that are useful for both humans and AI-driven automation.

How It Works

The repository follows a fairly clean layered structure.

At the top level, `cmd/cb365` contains the Cobra CLI entrypoints. Files like `main.go` and `root.go` set up the executable and global flags, while workload-specific files such as `todo.go`, `mail.go`, `calendar.go`, `teams.go`, `sharepoint.go`, and `loop.go` register subcommands and bind flags. This means the command tree is assembled in code rather than generated, and each workload file becomes the main place to inspect how user input is translated into an operation.

Under `internal/auth`, the repo encapsulates all credential behavior. Based on the README and file names, `auth.go` and `credential.go` manage login flows and profile resolution, while `keyring.go` handles native keychain integration and `store_file.go` provides the encrypted-file fallback for environments without a desktop secret store. This separation is important: command handlers should not need to know whether a token came from device-code auth, a client secret, or a certificate-backed app-only flow. They request a usable credential, and the auth layer provides it.

The `internal/graph` package is the next key piece. `client.go` likely constructs the Microsoft Graph SDK client using Kiota and Azure auth adapters, and `transport.go` likely customizes HTTP behavior such as IPv4-only networking or request policies. Because Graph access is centralized here, every command benefits from the same auth pipeline, HTTP stack, and safety around token handling.

Output formatting is isolated in `internal/output/output.go`. This is a strong
