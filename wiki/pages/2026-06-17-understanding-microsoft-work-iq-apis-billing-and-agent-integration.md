---
title: "Understanding Microsoft Work IQ APIs, Billing, and Agent Integration"
source: "https://www.linkedin.com/posts/henryjammes_workiq-share-7472686844321898496-9Dmz/?utm_source=social_share_send&utm_medium=ios_app&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY&utm_campaign=share_via"
date: "2026-06-17"
tags: [microsoft-365, copilot, agentic-ai, apis, enterprise-search]
source_type: "web"
topics: [ai-agents, microsoft-365, rag-and-retrieval]
kind: "news"
depth: 2
actionability: 2
---

## TL;DR

> Work IQ is presented as Microsoft’s unified business-context layer for agents, separating enterprise grounding, response generation, actions, and tenant-bounded state. This can reduce custom Microsoft 365 integration work, but custom and third-party agents must be designed around consumption-based Copilot Credit costs and governance controls.

## Key Takeaways

1. Use Context for retrieval and grounding, Chat for cited responses, Tools for Microsoft 365 actions, and Workspaces for tenant-bounded task state.
2. Require user approval before invoking side-effecting Tools operations such as sending email, scheduling meetings, or uploading files.
3. Microsoft’s announcement says Work IQ can ground agents in email, chats, meetings, files, people data, and line-of-business systems through a semantic organizational model.
4. First-party Copilot experiences reportedly include Work IQ for licensed users, while custom and third-party agents are billed by consumption through Copilot Credits.
5. Treat Chat and Context as variable-cost operations and Tools as fixed-cost operations when estimating per-task spending.
6. Reuse appropriate context and Workspace state to avoid repeated grounding and generation calls during multi-step workflows.
7. Pair technical access controls with FinOps controls, including usage monitoring, spending limits, alerts, throttling, and API permissions by tenant, group, or user.

## Overview

Work IQ is Microsoft's enterprise intelligence layer for grounding agents and applications in Microsoft 365 business context. The announcement describes its general availability API surface and positions it as the semantic layer that turns raw organizational signals—email, chats, meetings, files, people, and line-of-business systems—into context that AI agents can use safely and productively.

This matters to engineers building enterprise agents, copilots, and workflow automation inside Microsoft environments. Instead of wiring custom retrieval and action logic against many disconnected systems, developers can use Work IQ APIs for contextual responses, actionable tools, and tenant-bounded state, while planning around a consumption-based billing model tied to Copilot Credits.

## Key Concepts

- **Enterprise grounding**: Grounding means supplying an AI system with relevant business context so it can produce useful, accurate outputs. In Work IQ, that context comes from M365 sources such as email, meetings, chats, files, and people data, plus line-of-business systems.
- **Semantic organizational model**: The post describes Work IQ as a real-time semantic model of an organization. Rather than exposing only raw documents and events, it presents relationships and business context in a way that is easier for agents to reason over.
- **Chat API**: The Chat surface provides programmatic Copilot-style responses with citations. This is useful when developers want conversational outputs that remain tied to enterprise evidence and can be embedded into custom apps or agents.
- **Context API**: The Context surface provides agent-ready context and source data. It likely serves as the retrieval and grounding layer that lets an agent understand a user, task, or business situation before generating a response or taking action.
- **Tools API**: The Tools surface exposes M365 actions through simple verbs, such as sending mail, scheduling, or uploading files. This turns an agent from a read-only assistant into a system that can carry out work across Microsoft 365.
- **Workspaces**: Workspaces are secure, tenant-bounded storage areas where agents can keep intermediate task state. They are important for multi-step agent workflows that need memory, drafts, or temporary artifacts without moving data outside the organization's boundary.
- **Consumption billing with Copilot Credits**: Custom and third-party agents using Work IQ APIs are billed based on usage rather than per-user licensing. Charges use Copilot Credits, with variable pricing for Chat and Context operations and fixed pricing for Tools operations.

## How It Works

At a high level, Work IQ sits between enterprise data sources and the agent runtime. Instead of requiring an application to separately query mail, calendar, chat, files, user profiles, and business systems, Work IQ presents a unified intelligence layer. The goal is not just access to data, but access to **business context**—the facts, relationships, and signals an agent needs to answer questions or perform actions correctly.

A practical interaction model looks like this:

1. A user asks a question or initiates a task in a custom agent.
2. The agent calls **Context** to gather relevant enterprise grounding for that user and task.
3. The agent may call **Chat** to generate a Copilot-style response based on that grounded context, ideally with citations.
4. If the user wants the system to do something, the agent invokes **Tools** to execute M365 actions such as sending email, scheduling, or uploading content.
5. For multi-step flows, the agent stores intermediate state in **Workspaces**, keeping task memory inside the tenant boundary.

This API surface implies a clean separation of responsibilities:

- **Context** handles retrieval and grounding.
- **Chat** handles response generation over grounded data.
- **Tools** handle side-effecting business actions.
- **Workspaces** handle state persistence for in-flight tasks.

That separation is valuable architecturally because it maps well to common agent design patterns. A developer can build an orchestrator that first gathers context, then decides whether to answer, ask a follow-up question, or take an action. It also encourages safer systems: retrieval is explicit, action execution is explicit, and state storage is explicit.

From a systems-design perspective, Work IQ appears aimed at reducing the amount of custom integration code enterprises normally write for agentic applications. In a traditional design, an engineer would need:

- connectors into Exchange, Teams, SharePoint/OneDrive, calendars, identity, and business apps
- retrieval and ranking logic across heterogeneous data types
- prompt assembly and citation generation
- action adapters for email, meetings, and file operations
- secure state storage for agent workflows

Work IQ abstracts much of that into a platform layer. That makes it especially relevant for internal productivity agents, knowledge assistants, workflow copilots, and third-party SaaS agents that need to operate inside a customer's M365 context.

The billing model is also part of how the platform works in practice. The post distinguishes between:

- **First-party Copilot experiences and agents**, where Work IQ is included for licensed users.
- **Custom and third-party agents**, where API usage is billed by consumption.

This means engineering teams must think about workload shape. Heavy use of Chat and Context may incur variable costs, while Tools have fixed charges per operation type. In other words, an architecture that repeatedly regrounds and regenerates responses can be more expensive than one that caches context when appropriate, uses Workspaces for task continuity, and invokes actions only when needed.

The new admin-center cost dashboard is operationally important. It suggests that Work IQ usage is intended to be governed like a shared platform service, with controls for:

- monitoring credit usage
- choosing prepaid or pay-as-you-go funding
- setting spending limits
- assigning guardrails across tenants, groups, and users

For an engineering team, that means production rollout should include both technical controls and FinOps controls. A good deployment plan would define which agents are allowed to call which APIs, expected per-task credit burn, and spend thresholds that trigger alerts or throttling.

Although the source is a short announcement rather than deep documentation, the central design idea is clear: Work IQ is not just another chat endpoint. It is a **business-context platform** for enterprise agents, combining retrieval, generation, action execution, and secure task state under a common Microsoft 365-aware model.

## Training Exercise

Build a lightweight design for a tenant-aware meeting follow-up agent that uses the Work IQ model.

### Goal
Design an agent that can answer: "What happened in today's project meeting, and can you draft a follow-up email with action items?" Then extend it to send the email after user approval.

### Steps
1. **Map the user request to Work IQ surfaces**
   - Context: fetch meeting, chat, files, and participant context
   - Chat: summarize outcomes and draft the email with citations
   - Workspace: store the draft and task state
   - Tools: send the approved email

2. **Write the orchestration flow**
   Create a sequence diagram or pseudocode for the request lifecycle.

3. **Add cost-awareness**
   Mark which steps use variable-cost APIs and which use fixed-cost APIs.
   Decide where you can avoid repeated calls by reusing workspace state.

4. **Define security boundaries**
   List what data should remain tenant-bounded and what approvals are needed before invoking Tools.

5. **Implement pseudocode**
   Use the following generic example as a starting point:

```python
user_query = "Summarize today's project meeting and draft a follow-up email."

context = workiq.context.get(
    user_id="user-123",
    scopes=["meetings", "chat", "files", "people"],
    query=user_query
)

summary = workiq.chat.respond(
    prompt=user_query,
    context=context,
    citations=True
)

workspace_id = workiq.workspaces.save(
    user_id="user-123",
    state={
        "request": user_query,
        "summary": summary,
        "status": "drafted"
    }
)

print(summary)
approval = input("Send follow-up email? (yes/no): ")

if approval == "yes":
    workiq.tools.send_mail(
        workspace_id=workspace_id,
        to=["team@example.com"],
        subject="Project meeting follow-up",
        body=summary["draft_email"]
    )
```

### Deliverables
- A one-page architecture note
- A sequence diagram
- A table with each API surface, its role, and expected billing behavior
- One optimization idea to reduce Context/Chat consumption

## Test Yourself

<details><summary>What responsibility does each Work IQ surface have in a typical agent workflow?</summary>

Context retrieves enterprise grounding, Chat generates evidence-linked responses, Tools execute Microsoft 365 actions, and Workspaces preserve intermediate state inside the tenant boundary.

</details>

<details><summary>Why should an engineering team model workload shape before deploying a custom Work IQ agent?</summary>

The lesson says custom and third-party usage consumes Copilot Credits: Chat and Context costs vary with usage, while Tools operations have fixed charges. Repeated grounding or generation can therefore increase the cost of each task.

</details>

<details><summary>How should a meeting follow-up agent use Work IQ safely and efficiently?</summary>

It should gather meeting context, create a cited summary and email draft, save the draft in a Workspace, and send it through Tools only after user approval. Reusing saved state can reduce repeated Context and Chat consumption.

</details>

## Further Reading

- [Microsoft 365 Copilot documentation](https://learn.microsoft.com/microsoft-365-copilot/)
- [Microsoft Graph documentation](https://learn.microsoft.com/graph/)
- [Copilot Studio documentation](https://learn.microsoft.com/microsoft-copilot-studio/)
- [Azure AI Foundry agent and orchestration guidance](https://learn.microsoft.com/azure/ai-foundry/)
