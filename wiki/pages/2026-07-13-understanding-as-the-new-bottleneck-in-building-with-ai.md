---
title: "Understanding as the New Bottleneck in Building with AI"
source: "https://youtu.be/WkBPX-oDMnA?is=FQ_5mJxb3vDfFD2r"
date: "2026-07-13"
tags: [ai, product-design, llms, ux, knowledge-work]
source_type: "youtube"
channel: "AI Engineer"
published: "2026-07-10"
duration_seconds: 1173
topics: [product-and-design, ai-agents, context-engineering]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> As AI makes generation cheap and fast, the harder product problem becomes establishing reliable shared understanding of the user’s intent, constraints, and context. Making assumptions, evidence, and plans visible helps prevent fluent but incorrect outputs and actions.

## Key Takeaways

1. Treat context assembly—including documents, workspace structure, history, permissions, preferences, and domain data—as core product infrastructure.
2. Ask targeted clarifying questions when audience, scope, format, or desired action is ambiguous instead of assuming the first prompt is complete.
3. Expose sources, inferred objectives, assumptions, extracted entities, and proposed plans so users can correct misunderstandings before execution.
4. Design iterative propose–inspect–correct–rerun workflows rather than relying exclusively on one-shot generation.
5. Evaluate understanding with clarification rate, grounding accuracy, correction frequency, action reversal rate, confidence calibration, and time to correct output—not only fluency or completion.
6. Compare one-shot output with clarified output to identify recurring ambiguities that should become structured interface controls.
7. The lesson attributes to Geoffrey Litt the broader claim that understanding is becoming the bottleneck because it precedes every useful generation and trustworthy action.

## Overview

This lesson explores the idea that, in AI-assisted software and knowledge tools, the limiting factor is no longer only generating output but helping humans and systems achieve reliable understanding. The talk framing this idea, attributed to Geoffrey Litt at Notion, points toward a shift from traditional automation concerns toward designing products that clarify intent, context, and meaning before acting.

This matters to engineers building AI features, internal tools, and user-facing assistants. If models can produce text, summaries, code, or plans cheaply and quickly, the harder engineering and product problem becomes ensuring that the system understands the user’s goal well enough to do the right thing, and that the user understands what the system inferred, assumed, and changed.

## Key Concepts

- **Understanding vs. generation**: Earlier generations of AI products treated output generation as the hard problem: write the paragraph, answer the question, or produce the draft. With modern LLMs, generation is abundant, but correctness and usefulness now depend on whether the system accurately understands the user’s intent, constraints, and surrounding context.
- **Intent capture**: Users often express goals incompletely, ambiguously, or incrementally. AI systems need mechanisms to capture intent through clarifying questions, structured inputs, retrieval from prior context, or interactive refinement rather than assuming the first prompt is fully specified.
- **Context as product infrastructure**: Useful AI behavior depends on high-quality context: document state, workspace structure, history, permissions, user preferences, and domain-specific data. Engineers should treat context assembly as a first-class system component, not as an afterthought appended to a prompt.
- **Interpretability in the user interface**: When AI acts on behalf of a user, the UI must expose what the model thinks is happening. That can include showing the source material it used, the assumptions it made, the plan it inferred, and editable intermediate representations before committing changes.
- **Human-AI collaboration loops**: The most effective AI workflows are often iterative rather than one-shot. Systems should support cycles of propose, inspect, correct, and rerun so that understanding improves over time and mistakes are caught before they propagate.
- **Product quality beyond model quality**: A stronger base model helps, but product outcomes often hinge more on workflow design, grounding, safeguards, and feedback channels. Teams that focus only on model benchmarks can miss larger gains available from better context management and interaction design.

## How It Works

The core argument can be understood as a product and systems-design shift: once language models can generate plausible outputs on demand, the scarce resource becomes accurate shared understanding between user, model, and application state.

In a traditional software flow, the user provides explicit commands through forms, menus, or code. The system then executes deterministic logic. In an LLM-enabled flow, the user may provide a high-level request like "summarize this project and draft the next steps." The model can generate an answer immediately, but the real challenge is hidden in several layers:

1. **What does "this project" refer to?**
   - A single page?
   - A database row?
   - A collection of related docs?
   - Recent comments and tasks?

2. **What does "summarize" mean here?**
   - Executive summary?
   - Risks and blockers?
   - Decision log?
   - Status update for a manager?

3. **What counts as "next steps"?**
   - Suggested tasks?
   - Assigned tasks based on current owners?
   - Calendar actions?
   - Open questions requiring clarification?

A strong product cannot leave all of that latent. It needs a way to build and expose understanding.

A practical AI product architecture for this idea usually looks like this:

- **Input layer**: captures raw user requests from chat, commands, selections, or structured forms.
- **Context assembly layer**: gathers relevant state such as current document content, linked items, metadata, user identity, permissions, and recent history.
- **Interpretation layer**: infers the user’s likely goal, identifies ambiguities, and optionally asks follow-up questions.
- **Planning layer**: decides whether the task should be answered directly, decomposed into subtasks, or turned into an editable proposal.
- **Execution/generation layer**: uses the model to draft, transform, summarize, classify, or trigger tool calls.
- **Review layer**: presents output with evidence, assumptions, and opportunities for correction.
- **Feedback layer**: learns from user edits, approvals, and rejections to improve future behavior.

The most important engineering implication is that prompt construction alone is insufficient. You need explicit machinery for context retrieval and state modeling. For example, in a workspace product like Notion, context might include:

- The current page and its block structure
- Parent/child relationships between pages
- References to people, projects, and deadlines
- Prior edits and comments
- User role and access scope
- Templates or conventions used by the team

Without this, the model can produce fluent output that is structurally disconnected from the user’s actual work.

Another key mechanism is **interactive disambiguation**. Rather than immediately acting, the system can improve reliability by asking small, targeted questions. For example:

```text
You asked for next steps for the launch plan.
Do you want:
1. A short executive summary
2. Action items grouped by owner
3. Risks and open decisions
```

This pattern reduces hidden assumptions and transforms understanding into an explicit interface concern.

A related product design principle is to expose intermediate representations. Instead of only showing the final answer, the system can show:

- the sources it used,
- the inferred objective,
- extracted entities,
- a proposed outline or action plan,
- fields the user can edit before generation.

That matters because users are often better at spotting a misinterpreted assumption than at diagnosing a fully generated bad output after the fact.

From an engineering quality perspective, this reframes evaluation. Instead of measuring only output fluency or task completion, teams should also measure:

- clarification rate,
- source grounding accuracy,
- user correction frequency,
- action reversal rate,
- confidence calibration,
- time-to-correct-output.

These metrics better capture whether the system truly understood the task.

The broader lesson is that AI product value increasingly comes from reducing ambiguity. Better systems do not just generate more; they help users specify, inspect, and refine meaning. In that sense, understanding becomes the new bottleneck because it sits upstream of every useful generation and every trustworthy action.

## Training Exercise

Build a small prototype that turns an ambiguous user request into a clarified, grounded workflow.

### Goal
Create a command-line or simple web tool that accepts a vague task like:

```text
Summarize this project and suggest next steps.
```

The tool should not answer immediately. Instead, it should:
1. Gather context from a local file or note.
2. Detect ambiguities.
3. Ask 2-3 clarifying questions.
4. Produce a final summary and action list using the clarified intent.

### Step-by-step
1. **Create a sample project note**
   Put this in `project.txt`:

```text
Project: Mobile onboarding refresh
Status: Engineering is blocked on final copy. Design mockups are approved. QA found two analytics issues. Launch target is August 15. Owner is Mia. Stakeholders want a weekly update and risk visibility.
```

2. **Write a small script**
   Use any language. The script should:
   - load `project.txt`
   - accept a user request
   - identify likely ambiguities such as audience, format, and level of detail
   - prompt the user for answers
   - compose a final prompt using both the note and the clarifications

3. **Implement simple ambiguity rules**
   For example, if the request contains words like `summarize`, ask for the audience. If it contains `next steps`, ask whether the user wants tasks, risks, or decisions.

4. **Generate the result**
   Send the assembled prompt to your model or simulate the result manually if you are not using an API.

5. **Inspect the difference**
   Compare:
   - one-shot generation from the original request
   - clarified generation after asking questions

6. **Add an explainability section**
   Print:
   - the context source used
   - the clarifications collected
   - the final interpreted task

### Minimal Python skeleton
```python
from pathlib import Path

context = Path("project.txt").read_text()
request = input("Request: ")

clarifications = {}

if "summarize" in request.lower():
    clarifications["audience"] = input("Who is the summary for? ")

if "next steps" in request.lower():
    clarifications["next_steps_type"] = input(
        "Do you want tasks, risks, or open decisions? "
    )

clarifications["length"] = input("Short or detailed output? ")

final_prompt = f"""
You are helping with project analysis.

Context:
{context}

User request:
{request}

Clarifications:
{clarifications}

Produce:
1. A summary tailored to the audience
2. Next steps in the requested format
3. A short note listing any remaining uncertainties
"""

print("\n=== Final interpreted task ===")
print(final_prompt)
```

### What to observe
- How often the initial request was underspecified
- Whether clarifying questions materially improved usefulness
- Which ambiguities recur and could become structured UI fields later
- How showing the interpreted task helps users catch mistakes early

### Stretch goal
Turn repeated clarifications into product affordances. For example, replace free-text follow-up questions with dropdowns for audience, output type, and confidence level. This demonstrates how an AI feature evolves from open-ended chat toward a more reliable hybrid interface.

## Test Yourself

<details><summary>Why does the lesson describe understanding as the new bottleneck?</summary>

Modern language models can generate plausible content quickly, but useful results still depend on correctly interpreting the user’s goal, constraints, and surrounding state. A misunderstanding upstream can make every later generation or action wrong.

</details>

<details><summary>What components should a reliable AI workflow include beyond model generation?</summary>

It should capture input, assemble relevant context, interpret intent, resolve ambiguity, plan the work, execute it, present evidence and assumptions for review, and collect feedback from corrections or approvals.

</details>

<details><summary>How can a team test whether clarification improves an AI feature?</summary>

Run the same ambiguous request through a one-shot workflow and a workflow that asks 2–3 targeted questions, then compare usefulness and remaining uncertainty. Track recurring ambiguities and convert them into structured controls such as audience, output type, and detail level.

</details>

## Further Reading

- [Notion AI](https://www.notion.so/product/ai)
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Context Engineering for AI Agents](https://www.pinecone.io/learn/context-engineering/)
