---
title: "Building Interactive Microsoft 365 Copilot Widgets with an MCP App"
source: "https://www.linkedin.com/posts/shoebsayyed_microsoftcopilot-mcp-modelcontextprotocol-ugcPost-7468777854634422272-0D2N/?utm_source=social_share_send&utm_medium=ios_app&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY&utm_campaign=share_via"
date: "2026-06-06"
tags: [microsoft365, copilot, mcp, azure, dotnet, agents]
source_type: "web"
topics: [ai-agents, mcp, microsoft-365]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> Build rich Microsoft 365 Copilot experiences by using a declarative JSON package to guide tool selection and a separately hosted MCP server to execute logic and return structured widget data. This separation makes interactive dashboards easier to deploy, debug, and scale without embedding custom runtime code in Copilot.

## Key Takeaways

1. Treat `declarativeAgent.json`, `ai-plugin.json`, and `mcp-tools.json` as the contract connecting Copilot to the MCP backend.
2. Design for two contracts: discovery must help Copilot select the correct tool, while execution and rendering must return the exact structure the widget expects.
3. Return structured fields for charts, metrics, and sortable queues instead of relying only on generated prose.
4. The source recommends Azure Container Apps for an existing .NET MCP service because it can run the service with limited refactoring and scale to zero when idle.
5. Use `-developer on` to inspect Copilot tool calls and inline errors when invocation or widget rendering fails.
6. If a tool runs but no widget appears, check output schemas and rendering compatibility before assuming the backend logic is broken.

## Overview

For engineers building enterprise AI assistants, this pattern matters because it separates conversational orchestration from tool execution and UI rendering. You define a declarative Copilot app package, expose capabilities through an MCP server, and let Copilot invoke tools that return structured content suitable for rich visual experiences such as charts, queues, and dashboards.

## Key Concepts

- **MCP app architecture**: An MCP app for Copilot splits responsibilities between a hosted server and a lightweight Microsoft 365 package. The package declares the agent, instructions, and plugin metadata, while the MCP server executes the actual logic and exposes tools over the expected protocol.
- **Declarative packaging**: In Microsoft 365 Copilot, you do not deploy custom runtime code directly into the client for this pattern. Instead, you ship a small JSON package containing files such as `declarativeAgent.json`, `ai-plugin.json`, and `mcp-tools.json`, which tell Copilot what the agent is, how to call tools, and how capabilities should be presented.
- **Interactive widget responses**: Rather than returning only narrative text, a tool can drive a rich response that renders as an interactive widget. In the example, the widget includes a donut chart, bar chart, and sortable incident priority queue, turning a chat response into an operational dashboard.
- **Azure Container Apps for MCP hosting**: Azure Container Apps is a strong fit for MCP servers because it can run existing .NET code without major rewrites, supports the needed transport model, and can scale to zero when idle. That makes it operationally simpler and often cheaper than alternatives like always-on web hosting.
- **Developer-mode debugging**: Copilot developer mode helps diagnose why a tool invocation or widget render failed. Enabling `-developer on` exposes tool calls and errors inline, giving you observability into how Copilot interpreted the request and what happened during execution.
- **Tool-to-UI data flow**: The user asks a natural-language question, Copilot selects the appropriate tool based on agent instructions and manifest metadata, the MCP server executes and returns structured data, and Copilot renders the result into the chat surface. The quality of the final experience depends on both the schema of the tool output and the clarity of the declarative metadata.

## How It Works

At a high level, the system has three layers:

1. **Microsoft 365 Copilot surface**: the user asks for something like "show me the current incident dashboard."
2. **Declarative app package**: JSON files describe the agent, plugin, and tool definitions so Copilot knows what capabilities exist.
3. **Hosted MCP server**: a .NET service receives tool calls, fetches or computes incident data, and returns a response that can be rendered as a rich UI.

The source highlights an important design choice: in this model, Microsoft 365 primarily consumes metadata and instructions from your package rather than your app code directly. That package is composed of files with distinct responsibilities:

- `declarativeAgent.json` defines the agent identity and behavioral instructions.
- `ai-plugin.json` describes the plugin interface and how Copilot should think about invoking it.
- `mcp-tools.json` maps or declares the MCP tools available to Copilot.

These files collectively act as the contract between Copilot and your backend. If the contract is incomplete or inconsistent, Copilot may fail to select the tool, call the wrong thing, or render nothing useful even if your backend works.

The runtime flow looks like this:

- A user enters a request in Microsoft 365 Copilot or Teams.
- Copilot evaluates the request against the declarative agent instructions.
- Based on the plugin and tool manifests, Copilot decides to invoke an MCP tool.
- The MCP server, hosted separately, receives the tool call.
- The server executes application logic, such as loading current IT incidents, aggregating severity counts, and sorting a queue by priority.
- The response is returned in a structured form suitable for rich presentation.
- Copilot renders the output as an interactive widget inside the conversation.

In the proof of concept, that rendered widget contains several dashboard-like elements:

- a **donut chart** for categorical distribution,
- a **bar chart** for comparative counts,
- a **sortable queue** for operational triage.

This is the key shift from standard chatbot behavior: the LLM is not only generating prose, but coordinating with external tools to return a task-oriented interface.

The hosting decision is also central. The MCP server was implemented in **.NET** and deployed to **Azure Container Apps**. That is notable because it avoids a common trap: rewriting a working service to fit a different hosting model. Container Apps can run the service largely unchanged, expose the proper transport behavior, and scale to zero when idle. For enterprise engineers, this means faster iteration, lower idle cost, and less platform-specific refactoring.

From an engineering perspective, the practical architecture likely looks like this:

```text
User -> M365 Copilot -> Declarative app metadata
                      -> MCP tool selection
                      -> .NET MCP server on Azure Container Apps
                      -> incident data retrieval/aggregation
                      -> structured widget payload
                      -> interactive render in Copilot/Teams
```

The source also emphasizes debugging. Early failures were related not necessarily to backend logic, but to the end-to-end integration path: whether Copilot recognized the tool, whether the tool invocation succeeded, and whether the result could actually render. Enabling developer mode with `-developer on` exposed those internal tool calls and errors directly in the Copilot experience. This is especially useful because problems in agent systems often come from metadata mismatches, instruction ambiguity, or schema issues rather than simple code exceptions.

A practical way to reason about the system is to treat it as two contracts:

- **Discovery contract**: can Copilot discover and choose your tool based on agent instructions and manifests?
- **Execution/render contract**: once called, does the backend return data in the exact structure needed for successful rendering?

If either contract is weak, the experience degrades quickly. That is why the JSON package files, backend hosting choice, and developer-mode diagnostics are all equally important in this pattern.

## Training Exercise

Build a minimal design for an interactive Copilot dashboard app, even if you do not yet have a full tenant integration.

### Goal
Create the declarative package skeleton and a mock MCP backend contract for an "IT incident dashboard" tool.

### Step 1: Create the app manifest files
Create a folder named `copilot-incident-dashboard` and add these placeholder files:

```text
copilot-incident-dashboard/
  declarativeAgent.json
  ai-plugin.json
  mcp-tools.json
  sample-response.json
```

### Step 2: Define a simple agent
In `declarativeAgent.json`, describe an agent whose job is to answer questions about IT incidents and prefer dashboard-style responses when available.

Example starter structure:

```json
{
  "name": "Incident Dashboard Agent",
  "description": "Shows current IT incident status using dashboard-style responses.",
  "instructions": "When the user asks about current incidents, call the dashboard tool and present the results as a visual summary when possible."
}
```

### Step 3: Describe the plugin
In `ai-plugin.json`, define a plugin with one operation such as `getIncidentDashboard`. Keep it high level if you do not have the exact production schema yet.

```json
{
  "schema_version": "v1",
  "name_for_human": "Incident Dashboard Plugin",
  "name_for_model": "incident_dashboard_plugin",
  "description_for_model": "Provides current incident dashboard data including counts by severity and priority queue items."
}
```

### Step 4: Define the MCP tool contract
In `mcp-tools.json`, declare a tool that returns summarized incident data.

```json
{
  "tools": [
    {
      "name": "getIncidentDashboard",
      "description": "Return current IT incident metrics and queue data",
      "inputSchema": {
        "type": "object",
        "properties": {
          "team": { "type": "string" }
        }
      }
    }
  ]
}
```

### Step 5: Mock the backend response
Create `sample-response.json` to represent what your .NET MCP server would return.

```json
{
  "summary": {
    "totalOpen": 18,
    "critical": 2,
    "high": 5,
    "medium": 7,
    "low": 4
  },
  "byService": [
    { "service": "Email", "count": 4 },
    { "service": "Identity", "count": 6 },
    { "service": "Teams", "count": 8 }
  ],
  "priorityQueue": [
    { "id": "INC-1024", "priority": "P1", "title": "Identity outage" },
    { "id": "INC-1028", "priority": "P1", "title": "Mail flow degradation" },
    { "id": "INC-1032", "priority": "P2", "title": "Teams meeting delays" }
  ]
}
```

### Step 6: Implement a tiny mock server
If you want a hands-on backend, expose the sample response from a local web service.

Example with .NET minimal API:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/incident-dashboard", () => Results.Json(new {
    summary = new { totalOpen = 18, critical = 2, high = 5, medium = 7, low = 4 },
    byService = new[] {
        new { service = "Email", count = 4 },
        new { service = "Identity", count = 6 },
        new { service = "Teams", count = 8 }
    },
    priorityQueue = new[] {
        new { id = "INC-1024", priority = "P1", title = "Identity outage" },
        new { id = "INC-1028", priority = "P1", title = "Mail flow degradation" },
        new { id = "INC-1032", priority = "P2", title = "Teams meeting delays" }
    }
}));

app.Run();
```

Run it with:

```bash
dotnet run
```

### Step 7: Validate your design
Review your package and answer these questions:

1. What user prompt should trigger the tool?
2. What metadata tells Copilot that this tool is relevant?
3. What structured fields are needed to render charts and sortable tables?
4. What would you check first if the tool executes but no widget appears?
5. Why would Azure Container Apps be a better first hosting target than rewriting for a serverless runtime?

### Stretch goal
Containerize the mock service and prepare it for Azure Container Apps deployment with a simple `Dockerfile`. Even if you do not deploy it, this forces you to think through how the MCP backend would be hosted independently of the Microsoft 365 package.

## Test Yourself

<details><summary>What responsibilities belong to the declarative app package versus the hosted MCP server?</summary>

The package describes the agent, behavioral instructions, plugin metadata, and available tools. The MCP server performs the application logic and returns structured data for Copilot to render.

</details>

<details><summary>What are the two contracts engineers should validate in this architecture?</summary>

The discovery contract determines whether Copilot can find and select the appropriate tool. The execution/render contract determines whether the server successfully executes and returns data in the structure required by the widget.

</details>

<details><summary>Why does the source favor Azure Container Apps for the example .NET MCP server?</summary>

The source says Container Apps can host the existing service without a major rewrite, support the required transport behavior, and scale to zero. This can reduce refactoring effort and idle infrastructure cost.

</details>

## Further Reading

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Microsoft 365 Copilot extensibility documentation](https://learn.microsoft.com/microsoft-365-copilot/extensibility/)
- [Azure Container Apps documentation](https://learn.microsoft.com/azure/container-apps/)
- [.NET documentation](https://learn.microsoft.com/dotnet/)
