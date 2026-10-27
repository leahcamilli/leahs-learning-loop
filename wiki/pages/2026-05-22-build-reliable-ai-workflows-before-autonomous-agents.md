---
title: "Build Reliable AI Workflows Before Autonomous Agents"
source: "https://www.linkedin.com/posts/john-r-rymer-a65b2211_autonomy-isnt-the-goal-reliability-is-ugcPost-7463304891663409152-_a8R?utm_source=social_share_send&utm_medium=ios_app&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY&utm_campaign=share_via"
date: "2026-05-22"
tags: [ai-agents, workflows, reliability, prompt-engineering, llm-systems]
source_type: "web"
topics: [ai-agents, software-engineering]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> Start with a predefined AI workflow whenever you can map the task’s decision points; it will usually be cheaper, faster, easier to debug, and more reliable than an autonomous agent. Add autonomy only when valuable ambiguity makes a fixed execution path inadequate.

## Key Takeaways

1. Optimize production AI systems for dependable task completion, not maximum autonomy.
2. Use a workflow when you can enumerate the stages, branches, tool calls, validation rules, and escalation paths in advance.
3. Reserve agents for ambiguous, changing, or open-ended tasks whose value justifies greater cost, unpredictability, and monitoring burden.
4. Keep a necessary agent minimal: define its environment, tools, and system prompt before adding orchestration, memory, caching, or multi-agent coordination.
5. Write tool descriptions that state inputs, outputs, side effects, failure modes, and conditions for use; the model cannot recover context that was never placed in its context window.
6. Define completion criteria and escalation rules explicitly, and repeat critical constraints near the decisions they govern.
7. Compare workflow and agent implementations on the same cases using correctness, tool misuse, ambiguous outputs, debugging effort, latency, and token consumption.

## Overview

This lesson distills a practical engineering message from Barry Zhang's guidance on agent infrastructure at Anthropic: most teams should not start by building autonomous agents. They should start by building workflows. The core argument is that reliability, speed of iteration, and operational simplicity matter more than autonomy for most production AI systems.

This matters to engineers designing LLM-powered products, internal tools, and automations. If you can enumerate the decision points in your task, a workflow-based design is usually cheaper, faster, easier to debug, and more dependable than an open-ended agent loop. Agents still have a place, but mainly for ambiguous, high-value problems where the environment cannot be fully scripted in advance.

## Key Concepts

- **Reliability over autonomy**: The lesson's central principle is that autonomy is not the product goal; dependable task completion is. A system that does fewer things but does them consistently is usually more valuable in production than a more autonomous system that fails unpredictably.
- **Workflow-first design**: A workflow is a predefined sequence of steps, decisions, and tool calls. If you can map the decision tree ahead of time, a workflow generally outperforms an agent on cost, latency, and observability because the execution path is constrained and easier to validate.
- **Agents for ambiguity**: Agents are best reserved for tasks with unclear paths, changing contexts, or open-ended reasoning requirements. They are justified when the value of handling ambiguity outweighs the additional complexity, unpredictability, and monitoring burden.
- **Minimal agent architecture**: A useful mental model for an agent is just three parts: environment, tools, and system prompt. Everything else—multi-agent coordination, orchestration layers, caching, memory systems—is secondary and should only be added after a simple version proves necessary.
- **Context-window realism**: Engineers often design from their own full understanding of a problem, but the model only sees the tokens in its current context. Tool descriptions, prompts, and visible state must be precise because the agent cannot infer missing intent from the broader project background in your head.
- **Prompt ambiguity testing**: A practical technique is to paste your prompt and tool descriptions back into the model and explicitly ask what is unclear or underspecified. This helps expose vague instructions, hidden assumptions, and missing constraints before those issues become runtime failures.

## How It Works

The article argues for a design hierarchy: start with the simplest structure that can solve the task, and only move toward agency when the task truly requires it.

At a mechanical level, the distinction looks like this:

- **Workflow**: fixed stages, known branches, predictable tool usage
- **Agent**: model decides what to do next, which tools to call, and when to stop

A workflow-oriented system typically follows a pattern like:

1. Accept input
2. Classify or route the request
3. Execute one of a small number of predefined steps
4. Call a tool if needed
5. Validate the output
6. Return or escalate

That structure is operationally attractive because each stage can be measured and tested independently. You can log branch frequencies, detect regressions, set explicit failure policies, and add guardrails at deterministic points.

By contrast, an agent loop might look like:

1. Receive a goal
2. Inspect available tools and current environment state
3. Decide the next action
4. Execute the tool call
5. Observe results
6. Repeat until completion or timeout

That flexibility is powerful, but it creates multiple sources of failure:

- the model may choose the wrong next action
- it may misunderstand a tool description
- it may loop too long or stop too early
- it may miss key context because it only sees a limited token window
- the execution path becomes harder to predict and debug

The source also emphasizes keeping the system "embarrassingly simple" at first. For an engineer, that means resisting common early abstractions:

- don't introduce multi-agent patterns before a single-agent or no-agent design works
- don't build elaborate orchestration if a few explicit stages will do
- don't add memory and caching layers until you can show they solve a measured problem

A minimal agent, when one is truly needed, has three core pieces:

1. **Environment**: the state the agent can observe and act within
2. **Tools**: the explicit actions it can take
3. **System prompt**: the policy defining goals, constraints, and tool usage rules

This framing is useful because it forces clarity. If the task is failing, the problem is often one of these:

- the environment doesn't expose enough relevant state
- the tools are too vague, too broad, or badly documented
- the prompt leaves room for conflicting interpretations

The article's strongest practical advice is to design for the model's perspective rather than the human builder's perspective. Engineers often assume the model has access to all the background knowledge they do, but the model only has what is included in its context. That means:

- tool descriptions should specify inputs, outputs, side effects, and failure modes
- prompts should define completion criteria and escalation rules
- important constraints should be repeated near the decision point, not buried elsewhere

For example, a weak tool description might be:

```text
search_customer_data(query)
Searches customer info.
```

A stronger version would be:

```text
search_customer_data(customer_id: string) -> CustomerRecord
Use only when you already know the exact customer_id.
Returns account status, subscription tier, and recent support tickets.
Do not use for free-text lookup. If customer_id is missing, ask for it.
```

That additional specificity reduces bad tool selection and ambiguous reasoning.

The final implication is organizational as much as technical: teams that ship dependable AI systems often choose boring architectures intentionally. The winning pattern is not maximum cleverness; it is the fastest path to a system that behaves consistently under real usage. In practice, that usually means starting with a workflow, instrumenting it heavily, and only introducing autonomy where deterministic control breaks down.

## Training Exercise

Build the same task twice—first as a workflow, then as a lightweight agent—and compare reliability.

## Goal
Create a small AI system for handling inbound support requests. The system should classify requests into one of three actions:

- answer directly from a knowledge base
- request missing information
- escalate to a human

## Part 1: Build a workflow
1. Define a fixed decision tree for support tickets.
2. Create a prompt that classifies each ticket into one of the three actions.
3. Add explicit rules such as:
   - escalate billing disputes over $100
   - request missing information if order ID is absent
   - answer directly only for known FAQ topics
4. Test the workflow on 10 sample tickets.
5. Measure:
   - classification accuracy
   - number of invalid outputs
   - average latency

Example structured prompt:

```text
You are a support triage system.
Choose exactly one action: ANSWER, REQUEST_INFO, or ESCALATE.
Rules:
- If the issue is a billing dispute over $100, choose ESCALATE.
- If the request requires an order lookup and no order ID is present, choose REQUEST_INFO.
- If the issue matches a known FAQ, choose ANSWER.
Return JSON: {"action": "...", "reason": "..."}
```

## Part 2: Build a simple agent
1. Give the model a broader goal: resolve the support request as effectively as possible.
2. Provide tools such as:
   - `lookup_order(order_id)`
   - `search_faq(question)`
   - `create_escalation(summary)`
3. Write tool descriptions carefully.
4. Let the model decide which tool to call and when to stop.
5. Run the same 10 sample tickets.

## Part 3: Compare results
For each approach, record:

- correctness of final action
- tool misuse frequency
- ambiguous responses
- ease of debugging failures
- total tokens consumed

## Part 4: Prompt ambiguity review
Take your agent system prompt and tool descriptions and ask the model:

```text
Review the following system prompt and tool definitions.
List every ambiguity, missing constraint, or confusing instruction that could cause incorrect behavior.
Prioritize issues that would affect tool selection or stopping behavior.
```

Then revise the prompt and rerun the tests.

## What to learn
By the end, you should be able to answer:

- Was the task actually an agent problem or a workflow problem?
- Which approach was easier to validate and debug?
- What prompt or tool-description ambiguities caused failures?
- At what point, if any, did the extra autonomy pay for itself?

## Test Yourself

<details><summary>When should a team prefer a workflow over an agent?</summary>

Prefer a workflow when the task’s decision points and execution branches can be mapped ahead of time. The lesson argues that constrained paths generally improve reliability, cost, latency, observability, and debugging.

</details>

<details><summary>What are the three core parts of the lesson’s minimal agent architecture?</summary>

The three parts are the environment the agent can observe and affect, the tools it can invoke, and the system prompt that defines its goals, constraints, and tool-use rules.

</details>

<details><summary>How can a team expose prompt and tool-definition problems before deployment?</summary>

Ask the model to identify every ambiguity, hidden assumption, missing constraint, and confusing instruction in the system prompt and tool definitions, prioritizing anything that affects tool selection or stopping behavior. Revise them and rerun the same tests to measure whether failures decrease.

</details>

## Further Reading

- [Anthropic Documentation](https://docs.anthropic.com/)
- [OpenAI Cookbook: Building Reliable LLM Applications](https://cookbook.openai.com/)
- [LangChain: Agents vs Chains](https://python.langchain.com/docs/concepts/)
- [Google Cloud Architecture Framework: Reliability](https://cloud.google.com/architecture/framework/reliability)
