---
title: "Building Claude-Powered AI Agents in Microsoft Foundry"
source: "https://youtu.be/TQd_YQvydVg?si=4d3kuA0QQ1qZqnwJ"
date: "2026-05-23"
tags: [ai-agents, claude, microsoft-foundry, llm, agentic-systems]
source_type: "youtube"
channel: "Claude"
published: "2026-05-20"
duration_seconds: 2056
topics: [ai-agents, prompt-engineering, claude, context-engineering]
kind: "tutorial"
depth: 2
actionability: 1
---

## TL;DR

> A reliable Claude-powered agent in Microsoft Foundry requires more than model selection: it needs clear prompt policies, well-defined tools, grounded data, evaluation, and observability. Claude supplies reasoning, Foundry supplies the application platform, and business-specific tools supply trusted data and actions.

## Key Takeaways

1. Treat the system prompt as an operating policy that defines the agent’s role, boundaries, tool-use rules, citation requirements, and escalation behavior.
2. Use tools for current or proprietary facts; for example, require `search_docs` for internal policies and `get_ticket_status` for live ticket data instead of allowing guesses.
3. Define narrow, unambiguous tool schemas and protect side effects and sensitive data, because poorly designed tools can make agent actions unreliable or unsafe.
4. Ground responses in approved enterprise sources and require citations when accuracy depends on organization-specific documentation.
5. Test behavior with task-specific evaluation cases, including when the agent should call a tool, request missing information, escalate, or handle a tool failure.
6. Log traces, tool calls, latency, prompt versions, correctness, safety, and cost so failures and regressions can be diagnosed over time.
7. Design orchestration—not merely model choice—as the core engineering problem connecting prompts, state, tools, safety controls, evaluation, and deployment.

## Overview

This lesson explains how to think about building AI agents with Anthropic Claude inside Microsoft Foundry, based on a product-demo style source. Even though the source content is sparse, the core topic is highly relevant to engineers evaluating enterprise agent platforms: how a hosted AI development environment can connect a frontier model like Claude to tools, prompts, orchestration, and deployment workflows.

Engineers care about this because agentic applications are no longer just prompt wrappers. In practice, you need model selection, system prompts, tool invocation, grounding data, evaluation, and an operational path to deployment. Microsoft Foundry provides the application platform layer, while Claude provides the reasoning and language capabilities; together they form a typical modern enterprise AI stack.

## Key Concepts

- **Agent vs. single prompt app**: A single prompt application sends one request to a model and returns one response. An agent adds planning, state, tool usage, and conditional control flow so it can perform multi-step work such as retrieving data, calling APIs, and refining its own output.
- **Model hosting and selection**: In a platform like Microsoft Foundry, the application developer typically chooses from available model providers and versions rather than self-hosting a model. Selecting Claude means optimizing for capabilities such as instruction following, reasoning quality, safety behavior, latency, and cost within the platform's supported integrations.
- **System prompts and agent policy**: The system prompt acts as the agent's operating policy: role, boundaries, response style, and how to use tools. In enterprise settings, this prompt often encodes compliance constraints, escalation rules, and expectations about citing sources or refusing unsupported actions.
- **Tool calling**: Tool calling allows the model to invoke structured functions such as search, database queries, or business APIs. This is what turns a conversational model into a useful agent, because it can act on live data instead of relying only on model parameters.
- **Grounding and retrieval**: Grounding injects external context into the model's reasoning so responses reflect current or organization-specific information. Common grounding patterns include retrieval-augmented generation, enterprise search connectors, and passing structured records into the prompt or tool interface.
- **Evaluation and observability**: Agent quality cannot be judged by anecdotal demos alone. Production systems need traces, tool-call logs, latency metrics, prompt/version tracking, and task-specific evaluations to measure correctness, safety, and cost over time.

## How It Works

At a high level, building a Claude-based agent in Microsoft Foundry usually follows a layered architecture:

1. **Platform layer**: Microsoft Foundry provides the workspace for model access, configuration, testing, orchestration, and deployment.
2. **Model layer**: Claude handles language understanding, reasoning, summarization, extraction, and decision support.
3. **Agent layer**: prompts, memory/state, and tool definitions define how the model behaves as an agent rather than a plain chatbot.
4. **Data/tool layer**: enterprise search, documents, APIs, databases, or internal services provide the live context and actions.
5. **Application layer**: a chat UI, workflow trigger, API endpoint, or business process consumes the agent.

A typical request flow looks like this:

- A user submits a task, such as "summarize these support tickets and draft a remediation plan."
- Foundry routes the request to the configured Claude model deployment.
- The agent's **system prompt** establishes behavior: e.g. be concise, cite retrieved sources, ask clarifying questions when data is missing, and only use approved tools.
- If the task requires external knowledge, the agent invokes tools such as search, document retrieval, or a line-of-business API.
- Retrieved results are added to context, and Claude synthesizes a final answer or structured output.
- Foundry logs the interaction for inspection, debugging, and evaluation.

The most important engineering decision is usually not just "which model?" but **how the model is orchestrated**. In Foundry-style systems, orchestration often includes:

- Prompt templates for different tasks
- Tool schemas that define callable operations and argument structures
- Conversation/session state
- Safety rules and content filters
- Evaluation sets for regression testing

In practice, a simple agent configuration can be thought of like this:

```json
{
  "model": "claude",
  "system_prompt": "You are an enterprise analyst. Use tools when facts are needed. Cite retrieved sources.",
  "tools": [
    {"name": "search_docs", "description": "Search internal documentation"},
    {"name": "get_ticket", "description": "Fetch support ticket by ID"}
  ],
  "response_format": "markdown"
}
```

When a user asks a question, the agent decides whether it can answer directly or whether it needs a tool. For example, if the question is about a current policy document, a strong setup instructs Claude to call `search_docs` rather than hallucinating. That design is what makes enterprise agents reliable.

A practical mental model is:

- **Claude supplies intelligence**: reasoning, drafting, summarization, extraction.
- **Foundry supplies the application substrate**: deployment, configuration, integration, and operational controls.
- **Your code and tools supply business value**: access to proprietary data and actions.

Because the source is a web video rather than a code repository, there is no visible code structure to inspect directly. However, the architecture implied by this topic would typically include these modules in a real implementation:

- `agent_config`: model choice, prompts, temperature, safety settings
- `tools/`: wrappers around search, database, CRM, ticketing, or HTTP APIs
- `orchestrator`: request handling, tool loop, retry logic, state management
- `evals/`: golden prompts, expected outputs, and score criteria
- `ui` or `api`: a front-end or service endpoint exposing the agent to users

Data flow across those modules is usually:

1. Request enters UI/API.
2. Orchestrator assembles system prompt, user input, and prior context.
3. Model generates either a response or a tool call.
4. Tool executes against external system.
5. Result is fed back into the model.
6. Final answer is returned and logged.

The main implementation risks are also predictable:

- Weak system prompts that fail to constrain behavior
- Missing grounding, leading to hallucinations
- Poor tool design, where arguments are ambiguous or side effects are unsafe
- No evaluation harness, causing regressions when prompts or models change
- No observability, making it hard to debug why the agent made a bad decision

For an engineer, the key takeaway is that "building an AI agent with Claude in Microsoft Foundry" is less about a magic feature toggle and more about composing a robust pipeline: model selection, prompt policy, tool access, grounding, testing, and deployment discipline.

## Training Exercise

Build a minimal design spec for a Claude-powered support agent you could later implement in Microsoft Foundry.

### Goal
Create an agent that answers employee IT questions using internal documentation and can fetch ticket status by ID.

### Step 1: Define the agent contract
Write down:

- **User**: internal employee
- **Primary tasks**:
  - Answer IT policy and setup questions
  - Retrieve ticket status
  - Escalate when confidence is low
- **Constraints**:
  - Must cite internal docs when answering policy questions
  - Must not invent ticket data
  - Must ask for ticket ID when missing

### Step 2: Draft the system prompt
Use this starter:

```text
You are an internal IT support agent.
Answer using approved internal documentation when possible.
If factual current data is needed, use tools instead of guessing.
Cite document titles in your response.
If you cannot verify an answer, say so and suggest escalation.
```

### Step 3: Define two tools
Describe the tools in structured form:

```json
[
  {
    "name": "search_docs",
    "purpose": "Search internal IT documentation",
    "inputs": {
      "query": "string"
    }
  },
  {
    "name": "get_ticket_status",
    "purpose": "Fetch support ticket status by ID",
    "inputs": {
      "ticket_id": "string"
    }
  }
]
```

### Step 4: Design three evaluation prompts
Create test cases such as:

1. "How do I set up MFA on my laptop?"
   - Expected: agent uses doc grounding or answers with cited documentation.
2. "What's the status of ticket INC-48291?"
   - Expected: agent calls ticket tool.
3. "Can you tell me the status of my ticket?"
   - Expected: agent asks for ticket ID.

### Step 5: Simulate the orchestration loop
For each evaluation prompt, write out:

- User input
- Whether a tool should be called
- Tool arguments
- Expected final response behavior

### Step 6: Stretch goal
Add one safety rule and one failure-handling rule:

- Safety rule example: never expose sensitive ticket metadata not requested by the user
- Failure rule example: if a tool times out, explain the temporary issue and offer a retry

If you want to make this exercise executable in code later, express the orchestration in pseudocode:

```python
def handle_request(user_message, history):
    context = build_context(history)
    response = model.generate(system_prompt, context, user_message, tools=tools)

    if response.type == "tool_call":
        tool_result = run_tool(response.tool_name, response.arguments)
        return model.generate(system_prompt, context, user_message, tool_result=tool_result)

    return response.text
```

The outcome should be a one-page implementation blueprint you could map into Foundry's model, agent, and evaluation configuration screens.

## Test Yourself

<details><summary>What distinguishes an agent from a single-prompt application?</summary>

An agent adds planning, state, tool use, and conditional control flow to the model interaction. These capabilities let it retrieve live information, call APIs, and complete multi-step tasks rather than return only one model response.

</details>

<details><summary>How should the support agent respond when asked for a ticket status without a ticket ID?</summary>

It should ask the user for the missing ticket ID. It must not invent ticket data or call `get_ticket_status` without the required argument.

</details>

<details><summary>Why are evaluation and observability necessary even when an agent performs well in a demo?</summary>

Anecdotal success does not establish production reliability. Regression tests, traces, tool-call logs, latency metrics, and prompt-version tracking reveal correctness, safety, cost, and behavior changes over time.

</details>

## Further Reading

- [Anthropic Claude Documentation](https://docs.anthropic.com/)
- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Prompt Engineering Overview](https://platform.openai.com/docs/guides/prompt-engineering)
- [Retrieval-Augmented Generation (RAG) Overview on Azure](https://learn.microsoft.com/azure/search/retrieval-augmented-generation-overview)
