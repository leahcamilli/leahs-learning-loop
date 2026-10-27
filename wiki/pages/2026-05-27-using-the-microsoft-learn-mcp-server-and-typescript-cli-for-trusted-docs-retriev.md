---
title: "Using the Microsoft Learn MCP Server and TypeScript CLI for Trusted Docs Retrieval"
source: "https://github.com/microsoftdocs/mcp"
date: "2026-05-27"
tags: [mcp, typescript, cli, documentation, llm, rag]
source_type: "github"
topics: [mcp, developer-tools, ai-agents, rag-and-retrieval]
kind: "deep-dive"
depth: 3
actionability: 2
---

## TL;DR

> Use the Microsoft Learn MCP server and its TypeScript CLI to retrieve current, official Microsoft documentation and code samples instead of relying on generic search or stale model knowledge. The repository also demonstrates how to build resilient MCP clients through dynamic tool discovery, caching, refresh-on-failure, and separate output formatting.

## Key Takeaways

1. Connect to `https://learn.microsoft.com/api/mcp` through an MCP transport; do not treat it as a conventional webpage or fixed REST API.
2. Discover tools and input schemas dynamically, cache their metadata, and refresh it after relevant invocation failures or `listChanged` notifications.
3. Use `microsoft_docs_search` for conceptual and configuration documentation, `microsoft_docs_fetch` for retrieving a specific Learn page, and `microsoft_code_sample_search` for official examples and snippets.
4. Keep command handling, MCP discovery, caching, invocation, error normalization, and presentation as separate, testable concerns.
5. Use `--json` when integrating `@microsoft/learn-cli` with shell scripts, `jq`, agents, or other automated workflows.
6. Run `npx @microsoft/learn-cli doctor` to diagnose endpoint, configuration, or MCP connectivity problems.
7. Pair retrieval tools with agent skills that explain when to search documentation, verify APIs, or look for code samples.

## Overview

This repository packages Microsoft's official Learn MCP server integration story and a TypeScript-based CLI that exposes the same documentation and code-sample retrieval capabilities outside an MCP-aware client. Its purpose is straightforward: give AI agents and engineers a reliable path to current Microsoft documentation and samples, reducing hallucinations compared with generic web search or stale model knowledge.

Working engineers who build agent workflows, IDE integrations, internal developer tools, or terminal-based research utilities will care about this repo. Beyond the public endpoint documentation, the repository is useful because it shows how to build a resilient MCP client: dynamically discover tools, cache schemas, invoke them safely, and present results through a practical command-line interface.

## Key Concepts

- **Remote MCP endpoint**: The repo centers on a hosted MCP server at `https://learn.microsoft.com/api/mcp`, which exposes Microsoft documentation and code-sample retrieval tools over the Model Context Protocol. Clients are expected to connect through an MCP transport rather than treating the URL like a normal browser page or fixed REST API.
- **Dynamic tool discovery**: A core architectural rule in MCP is that tools are not hard-coded forever. Clients should ask the server which tools exist, cache that information, and refresh when the server signals changes or when invocations fail due to stale assumptions.
- **CLI as a thin MCP client**: The `cli/` package is effectively a terminal-friendly MCP client. It translates user commands like search, fetch, and code search into MCP tool discovery and invocation calls, then formats the returned content for humans or JSON consumers.
- **Trusted retrieval over open web search**: The server intentionally narrows retrieval to official Microsoft documentation and code samples. That constraint matters in agent systems because it improves provenance, reduces supply-chain risk from random sites, and makes generated code more likely to match current platform behavior.
- **Result formatting and markdown conversion**: The repo includes utilities for formatting search results and normalizing fetched documentation into markdown. This is important because raw tool payloads are rarely ideal for direct terminal output or for feeding into downstream automation.
- **Agent skills**: The `skills/` folders provide reusable instruction packages that tell agents when to use docs search, code reference lookup, or custom skill generation. These are not executable code modules, but they are operational artifacts that improve tool use quality in agents such as Claude Code, Copilot, and Cursor.

## How It Works

At a high level, the repository has three layers:

1. **Hosted service contract** documented in the root README: the Microsoft Learn MCP server exposes tools such as `microsoft_docs_search`, `microsoft_docs_fetch`, and `microsoft_code_sample_search`.
2. **Local TypeScript CLI** under `cli/`: a consumable package (`@microsoft/learn-cli`) that connects to the server and exposes those capabilities from the shell.
3. **Agent skill definitions** under `skills/`: instruction bundles that help LLM agents choose the right tool and query style.

### Repository structure

The most implementation-heavy part of the repo is the CLI:

- `cli/src/index.ts` — CLI entrypoint; wires commands together.
- `cli/src/context.ts` — builds shared runtime context used across commands.
- `cli/src/commands/search.ts` — executes documentation search requests.
- `cli/src/commands/fetch.ts` — retrieves a specific Learn page and renders markdown.
- `cli/src/commands/code-search.ts` — searches official code samples.
- `cli/src/commands/doctor.ts` — diagnostic command for validating connectivity/configuration.
- `cli/src/mcp/client.ts` — low-level MCP client logic for talking to the remote endpoint.
- `cli/src/mcp/tool-discovery.ts` — discovers and resolves server tools dynamically instead of assuming static names/schemas.
- `cli/src/mcp/cache.ts` — caches discovered tool metadata to avoid rediscovery on every call.
- `cli/src/formatters/search-results.ts` — turns returned search data into readable terminal output.
- `cli/src/utils/contracts.ts` — shared types/contracts for data structures moving through the app.
- `cli/src/utils/errors.ts` — normalizes user-facing and operational errors.
- `cli/src/utils/markdown.ts` — markdown cleanup/transformation utilities.
- `cli/src/utils/options.ts` and `cli/src/utils/text.ts` — command option parsing helpers and text formatting support.

The unit tests in `cli/test/unit/` mirror these responsibilities, especially around cache behavior, tool discovery, markdown processing, and CLI output. That test layout is a strong hint about the intended architecture: protocol handling and formatting are treated as separable, testable concerns.

### Data flow through the CLI

A typical command, such as:

```sh
mslearn search "azure functions timeout"
```

follows a flow like this:

1. The CLI entrypoint parses the command and options.
2. A shared context object is created, including endpoint configuration and any output mode flags such as `--json`.
3. The command requests an MCP tool by capability, not by blindly assuming a static local implementation.
4. `tool-discovery.ts` asks the MCP server for the current tool list, possibly consulting `cache.ts` first.
5. Once the appropriate tool is identified, `client.ts` invokes it with the user-supplied arguments.
6. The raw response is formatted either as human-readable text (`search-results.ts`, `text.ts`) or structured JSON.
7. Errors are caught and mapped into actionable diagnostics via `errors.ts`, and `doctor.ts` can be used when connectivity or protocol assumptions fail.

That separation is important: the command modules focus on user intent, the MCP modules focus on protocol safety, and the formatter/utils layer focuses on presentation.

### Why dynamic discovery matters

The README's guidance for custom clients is reflected in the CLI architecture. MCP is treated as a **dynamic protocol**. In practice, that means:

- You should not permanently hard-code available tool names or input schemas.
- Your client should refresh tool metadata when an invocation fails due to a missing or changed tool.
- Your client should be prepared for server-driven updates like `listChanged` notifications.

The presence of dedicated `tool-discovery.ts` and `cache.ts` modules shows that the CLI was designed around this operational reality. This is one of the most valuable implementation lessons in the repo: even if today's server exposes three familiar tools, the client is built to survive schema evolution.

### Commands and likely behavior

From the file layout and README, the CLI provides these main user workflows:

- **Search docs**: maps to `microsoft_docs_search` with a text query.
- **Fetch page**: maps to `microsoft_docs_fetch` with a Learn URL and returns markdown content.
- **Search code samples**: maps to `microsoft_code_sample_search` with query and optional language filter.
- **Doctor**: validates that the endpoint is reachable and that MCP interactions are functioning.

The `--json` flag allows the CLI to function as both a human tool and a scriptable building block. For example, a shell pipeline can search for docs, extract titles with `jq`, and feed selected URLs into `fetch`.

### Skills as operational guidance for agents

The `skills/` folder is separate from the TypeScript CLI, but it is part of the repo's architecture for real-world agent use:

- `skills/microsoft-docs/` helps with conceptual, tutorial, and configuration lookups.
- `skills/microsoft-code-reference/` helps with API verification, samples, and troubleshooting.
- `skills/microsoft-skill-creator/` is a meta-skill for generating new skills for specific Microsoft technologies.

These files do not change the protocol; they change agent behavior. In practice, they help an LLM decide when to call docs search versus code sample search, how to phrase queries, and when to verify uncertain implementation details against official sources.

### Practical engineering takeaways

If you are building your own retrieval tool or agent connector, this repo demonstrates a few sound patterns:

- Wrap protocol access behind a client abstraction.
- Separate discovery, caching, invocation, and formatting.
- Design for schema evolution and refresh-on-failure.
- Offer both human output and machine-readable JSON.
- Pair tools with behavioral guidance so agents actually use them effectively.

Even though the hosted MCP server itself is not implemented in this repository, the CLI and skills make the repo a solid reference for building consumers of a live, evolving MCP service.

## Training Exercise

Build a small terminal workflow around the Microsoft Learn CLI and observe dynamic, trusted retrieval in practice.

### Goal

Use the CLI to:
1. Search official Microsoft docs
2. Search official code samples
3. Fetch one documentation page as markdown
4. Pipe JSON output into another tool

### Prerequisites

- Node.js 18+ recommended
- `jq` installed if you want to follow the JSON-processing steps exactly

### Steps

1. **Run the CLI without installing it globally**

```sh
npx @microsoft/learn-cli search "azure functions timeout"
```

Confirm that you get search results from Microsoft Learn content.

2. **Inspect machine-readable output**

```sh
npx @microsoft/learn-cli search "azure openai authentication" --json
```

Look at the shape of the payload. Note which fields would be useful in an automated workflow, such as titles, URLs, and snippets.

3. **Extract URLs from the JSON**

```sh
npx @microsoft/learn-cli search "asp.net core dependency injection" --json | jq '.results[].url'
```

This demonstrates that the CLI is suitable for scripting, not just interactive use.

4. **Fetch a specific page as markdown**

Take one URL from the previous step and fetch it:

```sh
npx @microsoft/learn-cli fetch "https://learn.microsoft.com/aspnet/core/fundamentals/dependency-injection"
```

Observe how the page is converted into markdown-like terminal output rather than raw HTML.

5. **Search for code samples with a language filter**

```sh
npx @microsoft/learn-cli code-search "azure container apps managed identity" --language python
```

Compare the result style with regular docs search. Notice that this search targets official examples/snippets rather than conceptual docs.

6. **Run diagnostics**

```sh
npx @microsoft/learn-cli doctor
```

Use this to understand how the CLI helps isolate endpoint or configuration issues.

### Extension exercise

Write a tiny shell script that searches docs and fetches the first result automatically:

```sh
URL=$(npx @microsoft/learn-cli search "dotnet minimal api httpclientfactory" --json | jq -r '.results[0].url')
npx @microsoft/learn-cli fetch "$URL"
```

Then answer these questions:

- When would you use docs search vs. code search?
- Why is `--json` important for integrating the CLI into agent pipelines?
- Why is dynamic tool discovery safer than hard-coding tool names in a long-lived client?

## Test Yourself

<details><summary>Why should a long-lived MCP client discover tools dynamically instead of permanently hard-coding their names and schemas?</summary>

The server's available tools and schemas can evolve. Dynamic discovery, caching, and refresh-on-failure let the client adapt to changes instead of breaking when its assumptions become stale.

</details>

<details><summary>When should you use documentation search rather than code-sample search?</summary>

Use documentation search for concepts, tutorials, configuration, and platform guidance. Use code-sample search when you need official implementation examples, API usage, or troubleshooting references, optionally filtered by language.

</details>

<details><summary>Why does the CLI provide both formatted terminal output and `--json` output?</summary>

Formatted output makes results easy for people to read, while JSON makes the same retrieval capabilities composable in scripts and agent pipelines. For example, `jq` can extract a result URL and pass it directly to the fetch command.

</details>

## Further Reading

- [Microsoft Learn MCP Server product documentation](https://learn.microsoft.com/training/support/mcp)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [OpenAI MCP documentation](https://platform.openai.com/docs/mcp)
- [VS Code MCP servers guide](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
- [Microsoft Learn](https://learn.microsoft.com)
