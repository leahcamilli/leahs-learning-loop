---
title: "Decomposing an LLM Agent: When to Use Tools, Skills, or Subagents"
source: "https://youtu.be/mWvtOHlZM-I?si=o-fNoy43RFX7v2Ro"
date: "2026-05-23"
tags: [llm-agents, agent-design, prompt-engineering, tool-use, multi-agent-systems]
source_type: "youtube"
channel: "Claude"
published: "2026-05-22"
duration_seconds: 2706
topics: [ai-agents, prompt-engineering, context-engineering]
kind: "tutorial"
depth: 3
actionability: 2
---

## TL;DR

> Use the simplest component that creates a clean contract: tools for bounded system actions, skills for reusable model reasoning, and subagents only for workflows needing independent context and autonomy. This decomposition improves reliability and maintainability while controlling latency, cost, and orchestration complexity.

## Key Takeaways

1. Start decomposition from observed failure modes such as missing system access, overloaded prompting, or conflicting goals.
2. Use a tool for deterministic, execution-oriented operations with explicit schemas, narrow responsibilities, and well-defined failures.
3. Extract repeated model-centric reasoning into a named skill with typed inputs, outputs, and a test set.
4. Reserve subagents for separate goal-directed workflows that require iterative decisions, specialized context, or conflicting instructions.
5. Evaluate statefulness, autonomy, determinism, reuse, and isolation needs before choosing an abstraction.
6. Give every component only the context it needs; sending full conversation history to each subagent can increase cost and degrade performance.
7. Decompose incrementally: convert deterministic operations into tools, extract reusable reasoning into skills, and add subagents only if the main agent remains overloaded.

## Overview

As LLM-based agents grow beyond a single prompt, their behavior often becomes harder to reason about, test, and improve. A common design question is whether new capability should be added as a tool call, a reusable skill, or a separate subagent with its own context and control loop. Getting this decomposition right has a major impact on reliability, latency, cost, and maintainability.

This lesson introduces a practical framework for decomposing an agent that has outgrown its original prompt. It is aimed at engineers building production assistants, coding agents, workflow automations, or research copilots who need a disciplined way to split responsibilities without creating unnecessary complexity.

## Key Concepts

- **Prompt saturation**: Prompt saturation happens when a single system prompt accumulates too many instructions, edge cases, and behavioral rules. At that point, the agent becomes brittle: changes interact in surprising ways, and failures are difficult to localize. Recognizing saturation is the trigger for decomposing the system into clearer components.
- **Tool**: A tool is a bounded external capability the model can invoke, such as search, code execution, database lookup, or API access. Tools are best when the operation is deterministic or when the model mainly needs to choose when and how to call a capability rather than reason through a long internal workflow.
- **Skill**: A skill is a reusable pattern of prompting or logic that encapsulates a specific cognitive behavior, such as summarization, extraction, critique, or plan generation. Skills are useful when the capability is still model-centric, but you want modularity, reuse, testing, and cleaner orchestration than a giant monolithic prompt provides.
- **Subagent**: A subagent is a separately scoped agent with its own instructions, context window, and often its own planning or tool-usage loop. Subagents are appropriate when a task needs sustained autonomy, specialized context, or an independent objective that would otherwise overload the parent agent.
- **Context scoping**: Context scoping is the practice of giving each component only the information it needs to complete its task. Proper scoping reduces distraction, lowers token usage, and improves correctness by preventing unrelated instructions or history from contaminating the model's reasoning.
- **Orchestration boundary**: An orchestration boundary defines where control flow lives: in the main agent, in a helper routine, or inside a delegated subagent. Clear boundaries make systems easier to test and monitor because you can see whether errors come from planning, execution, or handoff design.

## How It Works

A useful way to decompose an overgrown agent is to start from failure modes rather than abstractions. If the current agent is doing too much in one prompt, ask what kind of capability is actually being added:

- Is it a **bounded action on the world or a system**? That usually suggests a **tool**.
- Is it a **repeatable reasoning pattern** the same model can perform with better isolation? That suggests a **skill**.
- Is it a **separate goal-directed workflow** that needs its own memory, instructions, or iterative loop? That suggests a **subagent**.

This distinction matters because each option changes the system along different axes:

- **Tools** optimize for precision, determinism, and integration with external systems.
- **Skills** optimize for modular prompting and internal reuse.
- **Subagents** optimize for specialization and task isolation, but add orchestration overhead.

A practical decision framework is to evaluate a new capability on five dimensions:

1. **Statefulness**: Does it need its own evolving context, or can it be done in one shot?
2. **Autonomy**: Does it need to make multiple decisions or tool calls on its own?
3. **Determinism**: Is this mostly an API-shaped operation with clear inputs and outputs?
4. **Reuse**: Will multiple workflows benefit from the same capability?
5. **Isolation need**: Would the main agent perform better if this logic were hidden behind a narrower interface?

### When to choose a tool
Choose a tool when the capability is fundamentally execution-oriented. Examples include querying a datastore, running tests, fetching documents, or sending a message. The model's job is mostly to map user intent into structured parameters.

A good tool interface has:

- explicit schema
- well-defined failure modes
- narrow responsibility
- machine-checkable outputs when possible

For example, instead of telling the agent in natural language how to retrieve customer records, expose a tool like:

```json
{
  "name": "get_customer_record",
  "input": {
    "customer_id": "string"
  },
  "output": {
    "status": "ok|not_found|error",
    "record": "object|null"
  }
}
```

This moves operational complexity out of the prompt and into software where it can be validated.

### When to choose a skill
Choose a skill when the operation is still primarily about language-model reasoning, but you want to isolate it from the main prompt. A skill can be implemented as a small prompt template, helper function, or chain that takes a typed input and returns a typed output.

Examples of skills:

- convert a bug report into a reproduction plan
- summarize a long thread into decision points
- critique a draft answer for missing assumptions
- extract entities from a document into a schema

A skill is often the right answer when engineers are tempted to keep appending "also remember to..." instructions to the main prompt. Instead, give that reasoning pattern a name, a contract, and a test set.

### When to choose a subagent
Choose a subagent when a capability deserves its own working environment. This typically happens when the task requires:

- iterative planning and execution
- specialized instructions that would conflict with the parent prompt
- a distinct context corpus
- long-running work whose intermediate reasoning should be encapsulated

Examples include a dedicated research agent, a code-fixing agent, or a document-analysis agent. The parent agent delegates an objective, receives a summarized result, and avoids carrying the full reasoning trace in its own context.

This can improve quality, but it also introduces new concerns:

- handoff design
- observability across agent boundaries
- duplicated tool access policies
- increased latency and cost
- recovery when a delegated task stalls or fails

### A simple architecture pattern
A practical production setup often looks like this:

1. **Main agent** handles user interaction, high-level planning, and final answer composition.
2. **Tools** provide concrete access to systems and data.
3. **Skills** encapsulate common reasoning transforms used by the main agent or subagents.
4. **Subagents** are reserved for domains where specialization clearly pays off.

In pseudocode:

```python
def handle_request(user_input):
    intent = classify_request(user_input)

    if intent == "simple_lookup":
        data = tools.search_kb(query=user_input)
        return skills.compose_answer(user_input, data)

    if intent == "analysis":
        notes = skills.extract_requirements(user_input)
        critique = skills.review_for_gaps(notes)
        return skills.compose_analysis(notes, critique)

    if intent == "deep_research":
        result = research_subagent.run(objective=user_input)
        return skills.compose_answer(user_input, result.summary)
```

The point is not to maximize the number of components. It is to put each kind of capability in the cheapest, clearest abstraction that supports reliability.

### Anti-patterns to watch for
Several decomposition mistakes are common:

- **Turning everything into a subagent**: this adds coordination cost and makes failures harder to trace.
- **Using prompts where software should exist**: deterministic data access should usually be a tool, not prose instructions.
- **Hiding routing logic inside giant prompts**: if the agent keeps conditionally choosing behaviors, that logic may belong in an orchestrator.
- **Leaking too much context**: passing full conversation history into every subagent often degrades performance instead of improving it.

A good heuristic is to prefer the simplest abstraction that creates a clean contract. Start with a tool for system actions, a skill for reusable reasoning, and a subagent only when the task genuinely needs independent agency.

### How to evolve an existing agent
If you already have a monolithic agent, decompose incrementally:

1. Review logs and cluster repeated failure cases.
2. Identify which failures come from missing system access, overloaded prompting, or conflicting goals.
3. Convert deterministic operations into tools.
4. Extract repeatable reasoning patterns into skills with input/output contracts.
5. Introduce subagents only for workflows that still overwhelm the main agent after the first two steps.
6. Add evaluation for each boundary so you can compare before and after behavior.

This approach keeps architecture grounded in observed problems rather than abstract enthusiasm for multi-agent design.

## Training Exercise

Build a small agent decomposition plan for a support assistant that currently does everything in one prompt.

### Scenario
Your monolithic agent currently does all of the following:

- answers product questions
- looks up account data
- summarizes support tickets
- investigates incident reports
- drafts customer replies

### Goal
Split this into tools, skills, and subagents with clear responsibilities.

### Step-by-step
1. **List the tasks** the current agent performs.
2. **Classify each task** as tool, skill, or subagent.
3. **Define a contract** for each component:
   - input
   - output
   - failure modes
4. **Draw the orchestration flow** for a sample request.
5. **Pick one skill and one tool** and implement them as stubs.

### Example classification
- `lookup_account(account_id)` → **tool**
- `summarize_ticket(thread)` → **skill**
- `incident_investigator(objective)` → **subagent**
- `draft_reply(context)` → **skill**

### Starter template
Use this JSON-like design document:

```json
{
  "main_agent": {
    "responsibilities": [
      "route incoming requests",
      "delegate specialized tasks",
      "compose final response"
    ]
  },
  "tools": [
    {
      "name": "lookup_account",
      "input": {"account_id": "string"},
      "output": {"status": "string", "account": "object|null"}
    }
  ],
  "skills": [
    {
      "name": "summarize_ticket",
      "input": {"thread": "string"},
      "output": {"summary": "string", "actions": ["string"]}
    }
  ],
  "subagents": [
    {
      "name": "incident_investigator",
      "goal": "analyze incident evidence and produce a probable root cause summary"
    }
  ]
}
```

### Stretch task
Take one request such as: "Customer 1842 says they were overbilled after last week's outage. What happened and how should we respond?"

For that request, write:

1. the main agent's routing decision
2. which tool calls happen
3. which skills run
4. whether a subagent is invoked
5. the final output structure

### Success criteria
You should be able to justify every component with one sentence:
- why it is not just part of the main prompt
- why it is or is not a tool
- why it does or does not need its own agent loop

## Test Yourself

<details><summary>How do tools, skills, and subagents differ?</summary>

A tool performs a bounded external action, a skill encapsulates a reusable model-based reasoning pattern, and a subagent pursues an independent objective with its own context and control loop.

</details>

<details><summary>When does the lesson recommend introducing a subagent?</summary>

Use one when a workflow requires sustained autonomy, iterative planning, specialized context, or instructions that would conflict with the parent agent. Do not use one merely to modularize a simple action or reasoning transform.

</details>

<details><summary>How should a team decompose an existing monolithic agent?</summary>

Review logs and group recurring failures, then turn deterministic operations into tools and repeated reasoning patterns into skills. Add subagents only for workflows that remain too complex, and evaluate each new boundary against the original behavior.

</details>

## Further Reading

- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Anthropic: Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [LangChain Docs: Tools, Agents, and Runnables](https://python.langchain.com/docs/)
- [Microsoft AutoGen Documentation](https://microsoft.github.io/autogen/)
