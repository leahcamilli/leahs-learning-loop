---
title: "Work IQ, Microsoft Graph, and Dataverse MCP in Microsoft 365 AI Agents"
source: "https://linkedin.com/posts/sean-astrakhan_workiq-microsoft365-mcp-share-7457292115677736960-3LiN?rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY"
date: "2026-05-05"
tags: [microsoft365, mcp, dataverse, microsoft-graph, ai-agents]
source_type: "web"
topics: [ai-agents, microsoft-365, mcp]
kind: "deep-dive"
depth: 2
actionability: 1
---

## TL;DR

> Design Microsoft 365 AI agents around two data lanes: Microsoft Graph for collaboration content and Dataverse for structured business records. Work IQ interprets natural-language intent and routes requests, avoiding unnecessary one-connector-per-app architectures.

## Key Takeaways

1. Treat Work IQ as the orchestration layer that interprets user intent and selects the appropriate Microsoft 365 data source.
2. Route emails, files, meetings, calendars, chats, and documents through the Microsoft Graph-backed collaboration lane.
3. Route accounts, opportunities, custom tables, and relationships through the separate Dataverse business-data lane.
4. Build every agent around three responsibilities: intent classification, source routing, and unified response shaping.
5. Start with simple routing rules, then add more advanced intent models as query variety and ambiguity increase.
6. Ask for clarification or query both systems when a request could refer to Graph content, Dataverse records, or both.
7. Do not assume every Microsoft 365 workload needs its own MCP server; the lesson frames MCP primarily as a standardized tool-access pattern, especially for Dataverse.

## Overview

These notes describe a practical architecture pattern for Microsoft 365 AI agents: Microsoft 365 content is not typically exposed as separate MCP servers for each workload like SharePoint, Outlook, or Teams. Instead, a unified intelligence layer called **Work IQ** interprets natural-language intent, determines where the requested information lives, and routes retrieval accordingly. For collaboration content across the tenant, that usually means **Microsoft Graph**; for structured business records, it means **Dataverse**, which is treated as a separate access path.

This distinction matters when designing agents, Copilot Studio solutions, or Power Platform integrations. The key mental model is a **two-lane system**: Graph-backed retrieval for Microsoft 365 collaboration data, and Dataverse MCP-oriented access for business entities. That helps avoid overcomplicating agent design with one connector per app and instead encourages intentional routing based on the type of user question.

## Key Concepts

- **Work IQ as a unified intelligence layer**: Work IQ acts as a broker for Microsoft 365 tenant data access.
- It lets users ask for information in natural language without needing to know the underlying app.
- It interprets intent and selects the most relevant backend.
- It reduces the need to think in terms of separate app-specific entry points.
- For agent design, it becomes the orchestration layer between question and data source.

- **Microsoft Graph for M365 content**: Microsoft Graph is the common API surface for Microsoft 365 collaboration data.
- It covers artifacts such as email, files, meetings, calendars, chats, and documents.
- Graph-backed retrieval is the right model for tenant-wide M365 content access.
- This explains why engineers may not find dedicated MCP servers for each Microsoft 365 app.
- Outlook, SharePoint, Teams, and OneDrive can all sit behind the same Graph-based access plane.

- **Dataverse as a separate business-data plane**: Dataverse is treated differently from general M365 collaboration content.
- It stores structured business data such as accounts, opportunities, custom tables, and relationships.
- In this framing, Dataverse has its own MCP server or direct structured tool path.
- It is the appropriate backend for CRM-like or operational business records.
- Agent architectures should model Dataverse separately from Graph-backed content retrieval.

- **Natural-language query routing**: Users begin with a request, not an API choice.
- The system must infer whether the request targets collaboration content or business records.
- Correct classification determines whether to use Graph or Dataverse.
- Ambiguous prompts may require clarification or multi-source retrieval.
- Routing quality directly affects agent usefulness and trust.

- **MCP as a tool integration pattern**: MCP is useful as a standard way for agents to access tools and data sources.
- In these notes, MCP is especially relevant for Dataverse integration.
- MCP should not be assumed to be the transport model for every Microsoft 365 workload.
- The pattern is more about interoperable tool access than mirroring every M365 app with its own server.
- This helps separate protocol concerns from Microsoft’s platform abstractions.

- **Agent design implications**: The main architectural takeaway is to avoid one-tool-per-app thinking unless the platform explicitly requires it.
- Instead, model M365 collaboration access as a unified Graph-backed retrieval layer.
- Model Dataverse as a separate connector/tool path for structured records.
- Build routing, permissions, and answer synthesis into the agent layer.
- Treat the complexity as centralized orchestration rather than distributed app-by-app integration.

## How It Works

The notes outline a **two-lane retrieval architecture** for Microsoft-centric AI agents.

In the first lane, a user asks for collaboration content such as emails, files, chats, meetings, or calendars. Work IQ interprets the request and determines that the answer likely lives in Microsoft 365. It then routes retrieval through **Microsoft Graph**, which serves as the consolidated API layer over services such as Outlook, SharePoint, Teams, OneDrive, and Calendar.

In the second lane, the user asks for structured business information such as customer records, account ownership, opportunities, tables, or relationships. In that case, the request is treated as a **Dataverse** query. The notes emphasize that Dataverse is a distinct business-data substrate with its own MCP-oriented access path, making it a more direct tool-style integration target.

A simple request flow looks like this:

1. User submits a natural-language question.
2. Work IQ interprets the intent and predicts the likely source.
3. If the question is about Microsoft 365 collaboration content, route to **Graph**.
4. If the question is about structured business records, route to **Dataverse**.
5. Normalize the results so the agent can return one coherent answer.

A useful design implication is that agents need at least three core responsibilities:

- **Intent classification** to distinguish collaboration content from business data
- **Source routing** to choose Graph vs Dataverse
- **Response shaping** to present unified answers even when the underlying systems differ

The notes also suggest starting with a simple rules-based router before introducing more advanced intent models. For example:

- “Find the latest email from Contoso” → likely **Graph**
- “What file did Sarah share in Teams yesterday?” → likely **Graph**
- “Show the account owner and open opportunities for Fabrikam” → likely **Dataverse**

Some prompts will be ambiguous and may require a clarifying question or retrieval from both systems. For instance, “Show me customer meeting notes” could refer to Teams meeting artifacts in Graph, CRM notes in Dataverse, or both. That makes ambiguity handling an important part of agent design.

The broader architectural lesson is that the platform complexity is not removed but **centralized**. Work IQ handles orchestration and source selection, Graph remains the access plane for Microsoft 365 collaboration workloads, and Dataverse keeps its own structured integration model. This is why searching for separate “SharePoint MCP” or “Outlook MCP” servers may be the wrong design approach in this context.

## Test Yourself

<details><summary>What is the core two-lane architecture described in the lesson?</summary>

Microsoft Graph provides the access lane for Microsoft 365 collaboration content, while Dataverse provides a separate lane for structured business records. Work IQ interprets the request and routes it to the appropriate lane.

</details>

<details><summary>How should an agent handle a request such as “Show me customer meeting notes”?</summary>

It should recognize that the request is ambiguous because the notes might be Teams artifacts in Graph, CRM notes in Dataverse, or both. The agent should ask a clarifying question or retrieve from both sources and combine the results.

</details>

<details><summary>Why might searching for separate SharePoint, Outlook, or Teams MCP servers be the wrong approach in this architecture?</summary>

The lesson presents Microsoft Graph as the shared access plane for those collaboration workloads, with Work IQ handling intent and routing. Separate app-specific MCP servers would therefore add complexity that the unified Graph-backed design is intended to centralize.

</details>

## Personal Notes

Work IQ, Microsoft Graph, and Dataverse MCP in Microsoft 365 AI Agents

Source: https://www.linkedin.com/posts/sean-astrakhan_workiq-microsoft365-mcp-share-7457292115677736960-3LiN?utm_source=share&utm_medium=member_ios&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY
Notion page: https://www.notion.so/Work-IQ-Microsoft-Graph-and-Dataverse-MCP-in-Microsoft-365-AI-Agents-35701bb0839a818a9d63cc27e9706d84

Tags: microsoft365, mcp, dataverse, microsoft-graph, ai-agents, power-platform

Overview

This lesson explains the architecture implied by the source: Microsoft does not expose separate MCP servers for every Microsoft 365 application such as SharePoint or Outlook. Instead, Microsoft 365 data is reached through a unified intelligence layer called Work IQ, which interprets a natural language request, identifies the right data source, and routes the request appropriately across Microsoft 365 and Dataverse.

This matters to engineers building AI agents, Copilot Studio solutions, or Power Platform integrations because it changes how you should think about data access. Rather than looking for app-specific MCP endpoints across M365, you should model Microsoft 365 access as Graph-backed tenant-wide retrieval, while treating Dataverse as a distinct business-data system that can also be addressed through its own MCP-oriented access pattern.

Key Concepts

  *   Work IQ as a unified intelligence layer: Work IQ is presented as a single entry point for AI-driven access across a Microsoft 365 tenant. Instead of forcing a caller to know whether information lives in Outlook, SharePoint, Teams, or OneDrive, it acts as a broker that interprets intent and routes queries to the correct backing system.
  *   Microsoft Graph for M365 content: Emails, files, meetings, chats, calendars, and related collaboration artifacts are accessed through Microsoft Graph. Graph is the common API surface over Microsoft 365 services, so an AI layer can use it to retrieve or reason over content without exposing separate MCP servers for each app.
  *   Dataverse as a separate business-data plane: Dataverse holds structured business records such as tables, relationships, and CRM-like entities. In the source, it is treated differently from general Microsoft 365 content because it has its own MCP server path and can be connected to directly.
  *   Natural-language query routing: A user begins with a natural language request rather than choosing an API manually. The system must classify the request, infer where the answer lives, and dispatch it to either Graph-backed M365 content or Dataverse-backed business records.
  *   MCP as a tool integration pattern: MCP, or Model Context Protocol, is useful for giving agents structured access to tools and data sources. In this framing, MCP is not necessarily the transport for every Microsoft 365 workload, but it is important for Dataverse integration and agent tool interoperability.
  *   Agent design implications: For engineers, the main implication is architectural: do not design one agent tool per M365 app unless the platform specifically requires it. Instead, think in terms of a unified tenant access layer for collaboration content and a separate, structured connector path for enterprise application data in Dataverse.

How It Works

At a high level, the source describes a **two-lane retrieval architecture** for Microsoft-centric AI agents.

**Lane 1: Microsoft 365 collaboration content** If a user asks about emails, documents, chats, meetings, calendars, or files, the request is treated as a Microsoft 365 content query. Work IQ decides
