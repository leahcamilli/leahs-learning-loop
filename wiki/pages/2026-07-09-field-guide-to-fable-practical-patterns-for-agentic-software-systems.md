---
title: "Field Guide to Fable: Practical Patterns for Agentic Software Systems"
source: "https://youtu.be/9fubhllmsBU?is=naMYCD__pKA4lox4"
date: "2026-07-09"
tags: [agents, llm, system-design, ai-engineering, workflows]
source_type: "youtube"
channel: "AI Engineer"
published: "2026-07-06"
duration_seconds: 1168
topics: [ai-agents, context-engineering, prompt-engineering, classifiers-and-structured-output]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> Production-grade agentic systems pair an uncertain reasoning model with deterministic tools, validation, safety controls, and evaluation. This separation makes multi-step automation more reliable, auditable, and safe.

## Key Takeaways

1. Treat prompts as versioned, testable policies that define goals, constraints, output formats, and escalation rules.
2. Let the model choose and synthesize, while deterministic code executes actions, validates inputs, enforces permissions, and applies stopping conditions.
3. Manage context deliberately: keep stable instructions in the system prompt, retrieve task-specific evidence on demand, and compress older state.
4. Require structured outputs such as validated JSON to create a dependable contract between the model and application.
5. Design every tool with a narrow purpose, strict input schema, authorization checks, defined failure behavior, and audit logs.
6. Test prompt, model, retrieval, and tool changes against representative tasks to catch regressions and analyze failures.
7. Automate low-risk, well-specified tasks; require confirmation for ambiguous or medium-risk actions; and route irreversible, high-risk, or policy-sensitive actions to human review.

## Overview

This lesson distills the likely core ideas behind a technical talk titled "Field Guide to Fable" by an Anthropic speaker into a practical engineering-oriented framework for building software around large language models. Because the source content available here contains only video metadata and not a transcript, this lesson focuses on the common architectural and operational themes that a field guide for LLM-based systems would cover: task decomposition, tool use, memory, reliability, and evaluation.

## Key Concepts

- **Agentic workflow**: An agentic workflow is a software loop where a model does more than generate one answer: it plans, calls tools, observes results, and iterates toward a goal. This matters because many real engineering tasks require stateful interaction with external systems rather than a single completion.
- **Prompt as policy**: In LLM systems, prompts often act like lightweight control logic that specifies goals, constraints, output format, and escalation rules. Treating prompts as policy helps engineers version, test, and review them as part of the application rather than as ad hoc strings.
- **Tool use and environment access**: Models become much more useful when they can access retrieval, code execution, APIs, and business systems through explicit tools. The critical engineering challenge is exposing just enough capability to solve tasks while preserving safety, observability, and predictable behavior.
- **Context and memory management**: Useful LLM applications need to decide what information belongs in the immediate prompt, what should be retrieved on demand, and what can be stored as durable memory. Poor context design causes hallucinations, token waste, and inconsistent behavior across turns.
- **Evaluation-driven iteration**: LLM systems are hard to improve by intuition alone, so teams need representative tasks, expected outcomes, and regression checks. Evaluation turns vague prompt tuning into disciplined engineering with measurable quality and failure analysis.
- **Human-in-the-loop reliability**: For ambiguous, risky, or high-impact tasks, humans should remain part of the decision path. Good systems define when the model can act autonomously, when it must ask clarifying questions, and when it must escalate to a person.

## How It Works

A practical field guide to LLM systems usually starts from one core shift: you are no longer just calling a text-generation API, you are designing a runtime around an uncertain but capable reasoning component. The model is one part of the system. The rest of the value comes from task framing, state management, tool integration, safeguards, and evaluation.

A useful mental model is to structure the application into four layers:

1. **Interface layer**
   - Accepts a user request or upstream job.
   - Normalizes input and attaches metadata such as user identity, permissions, and task type.
   - Decides whether the request should be answered directly or routed to a multi-step workflow.

2. **Reasoning layer**
   - Builds the model prompt from system instructions, user input, context, and tool schemas.
   - Requests a plan, next action, or final answer from the model.
   - Interprets structured output rather than relying on free-form text whenever possible.

3. **Tooling layer**
   - Exposes functions like search, retrieval, database lookup, calculator, code execution, ticket creation, or API calls.
   - Validates arguments before execution.
   - Returns results in a machine-friendly format that the model can inspect and reason about.

4. **Control and safety layer**
   - Enforces permissions, rate limits, retries, and termination conditions.
   - Logs prompts, tool calls, outputs, errors, and latencies.
   - Detects low-confidence or policy-sensitive cases and escalates them.

In a typical agent loop, data flows like this:

- The user asks for a task, for example: "Summarize this incident and draft a status-page update."
- The system classifies the task and retrieves relevant context such as incident notes and previous status updates.
- The model is prompted with role instructions, task constraints, and available tools.
- The model either answers directly or selects a tool call.
- The application executes the tool call and appends the result to the running context.
- The model receives the observation and decides the next step.
- The loop ends when the system receives a valid final response or hits a stopping rule.

This architecture is effective because it separates responsibilities. The model chooses and synthesizes; deterministic code performs execution, validation, and policy enforcement. That separation is often the difference between a toy demo and a production system.

A major theme in real-world LLM design is that **context is expensive and fragile**. Engineers must be deliberate about what goes into the prompt:

- Stable instructions belong in the system prompt.
- Task-specific data belongs in the user or tool context.
- Large knowledge sets should be retrieved selectively.
- Intermediate reasoning state should be summarized periodically rather than appended forever.

A common pattern is retrieval-augmented generation, where the system first searches or embeds documents, then injects only the most relevant snippets into the model context. Another common pattern is state compression, where earlier turns are condensed into a short working memory summary to preserve important facts without overflowing the context window.

Reliability depends heavily on **structured outputs**. Instead of asking for unconstrained prose, a robust system asks the model to emit JSON or a fixed schema such as:

```json
{
  "action": "search_docs",
  "query": "recent incident timeline",
  "reason": "Need exact timestamps before drafting update"
}
```

The application can validate the structure, reject invalid outputs, and retry with clarification if needed. This creates a cleaner contract between model and application.

Another likely field-guide point is that **tool use should be narrow and auditable**. Each tool should have:

- A clear name and purpose
- A strict input schema
- Validation and authorization checks
- Well-defined failure behavior
- Logs that capture who invoked it, with what arguments, and what happened

For example, a `create_ticket` tool should not accept arbitrary free text for every field if some fields should be selected from an allowlist. Good tool design reduces prompt ambiguity and limits unsafe actions.

Evaluation is the operational backbone of these systems. A practical team maintains a small but representative suite of tasks, such as:

- Answer a support question using documentation only
- Generate a customer-safe summary from internal notes
- Refuse to perform an unauthorized action
- Ask for clarification when required information is missing
- Correctly call the right tool with valid arguments

Each application change, whether a prompt edit, model upgrade, retrieval tweak, or tool modification, can then be tested against the suite. This is how teams avoid shipping regressions that only show up in edge cases.

Finally, a good field guide emphasizes that not every task should be fully autonomous. Use a decision framework:

- **Low risk + well specified**: allow automation
- **Medium risk or partial ambiguity**: require confirmation before acting
- **High risk, external side effects, or policy sensitivity**: human review required

That framing keeps the model in the role it performs best: accelerating cognition and workflow orchestration, while deterministic systems and people handle authority, accountability, and irreversible actions.

## Training Exercise

Build a minimal tool-using support assistant that answers questions from a small document set and escalates when it lacks enough evidence.

### Goal
Create a command-line prototype that:
1. Accepts a support question
2. Retrieves relevant documentation snippets
3. Asks an LLM to either answer, ask a clarifying question, or escalate
4. Returns a structured JSON decision

### Step 1: Create a tiny knowledge base
Make a file called `docs.json`:

```json
[
  {"id": 1, "title": "Password Reset", "text": "Users can reset passwords from the login page. Support cannot see existing passwords."},
  {"id": 2, "title": "Refund Policy", "text": "Refunds are available within 30 days for annual plans. Monthly plans are non-refundable after billing."},
  {"id": 3, "title": "Account Deletion", "text": "Account deletion is irreversible and requires email confirmation from the account owner."}
]
```

### Step 2: Implement a retrieval tool
Write a simple keyword matcher in Python:

```python
import json

with open("docs.json") as f:
    DOCS = json.load(f)

def search_docs(query: str, limit: int = 2):
    q = set(query.lower().split())
    scored = []
    for doc in DOCS:
        text = (doc["title"] + " " + doc["text"]).lower()
        score = sum(1 for token in q if token in text)
        scored.append((score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for score, doc in scored[:limit] if score > 0]

print(search_docs("Can I get a refund for my annual plan?"))
```

### Step 3: Define the model contract
Prompt the model to return JSON with this schema:

```json
{
  "decision": "answer | clarify | escalate",
  "message": "string",
  "citations": [1, 2]
}
```

System rules:
- Answer only from retrieved documents
- If evidence is weak or missing, ask a clarifying question or escalate
- Never invent policy details

### Step 4: Run the loop
For each user question:
1. Call `search_docs(question)`
2. Insert the returned snippets into the prompt
3. Ask the model for a structured decision
4. Validate the JSON before printing it

### Step 5: Test with cases
Try these prompts:
- `Can you tell me your refund rules for annual plans?`
- `Delete my account right now.`
- `What's my current password?`
- `Can I get a refund for last month's monthly invoice?`

### Step 6: Add one safety improvement
Implement one of these:
- Reject answers with no citations
- Escalate automatically on irreversible actions like deletion
- Add a confidence threshold based on retrieval score

### What to observe
- When does retrieval provide enough evidence?
- Which requests should be answered vs clarified vs escalated?
- How often does the model try to overgeneralize beyond the documents?
- How does structured output simplify control flow?

If you want to extend the exercise, replace the keyword retriever with embeddings, add a second tool like `create_ticket`, and record evaluation results for 10 test prompts before and after each change.

## Test Yourself

<details><summary>Why should execution and policy enforcement remain outside the language model?</summary>

Model behavior is uncertain, while execution, validation, permissions, and stopping rules need predictable enforcement. Keeping those responsibilities in deterministic code limits unsafe actions and improves auditability.

</details>

<details><summary>How should an agentic system decide what information to place in context?</summary>

Stable instructions belong in the system prompt, task-specific evidence should be retrieved when needed, and older working state should be summarized. This reduces token waste, hallucinations, and inconsistent behavior.

</details>

<details><summary>What should the support-assistant exercise do when retrieved evidence is weak or an action is irreversible?</summary>

It should return a structured decision to clarify or escalate rather than inventing details. Irreversible actions such as account deletion should be escalated automatically or require human confirmation.

</details>

## Further Reading

- [Anthropic Documentation](https://docs.anthropic.com/)
- [OpenAI Cookbook: Building Reliable LLM Applications](https://cookbook.openai.com/)
- [LangChain Agents Conceptual Guide](https://python.langchain.com/docs/concepts/agents/)
- [Martin Fowler: What AI Engineering Teams Need to Know About Evaluations](https://martinfowler.com/articles/ai-evaluations.html)
