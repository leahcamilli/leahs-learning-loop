---
title: "Deterministic State Machines for Reliable, Self-Improving AI Agents"
source: "https://www.youtube.com/watch?v=1rMgw0Q5MgY"
date: "2026-10-02"
tags: [ai-agents, state-machines, workflow-design, observability, evaluation]
source_type: "youtube"
source_fingerprint: "469795167c"
source_characters: 22104
channel: "Callstack"
published: "2026-09-22"
duration_seconds: 1277
topics: [ai-agents]
kind: "opinion"
depth: 2
actionability: 2
---

## TL;DR

> Keep fixed rules and control flow in an explicit state machine while reserving language models for flexible work such as drafting and clarification. This makes agent behavior inspectable, testable, and easier to improve from execution traces.

## Key Takeaways

1. Separate deterministic rules from generative work: enforce approval, recipient, and sequencing constraints in code while letting the model compose content and ask questions.
2. Do not bury control flow exclusively in a mega-prompt; prompt rules compete with growing context and are difficult to inspect or test.
3. Represent permitted states and transitions explicitly so prohibited actions have no available path—for example, sending should be unreachable before approval and recipient validation.
4. Evaluate states, complete outcomes, and transitions; a workflow can reach the correct result while still forcing users through an inefficient path.
5. Treat the state machine and its traces as durable artifacts that another agent can inspect and revise.
6. Compare workflow versions by running the same scenarios against both and measuring whether the proposed revision actually improves behavior.
7. Implementations do not require a specialized library: the presenter identifies XState, LangGraph, switch statements, and reducer functions as possible approaches.

## Key Moments

- [3:45](https://www.youtube.com/watch?v=1rMgw0Q5MgY&t=225s) — See how unstructured delegation produces unreliable agent behavior.
- [5:17](https://www.youtube.com/watch?v=1rMgw0Q5MgY&t=317s) — Separate fixed email-sending rules from open-ended drafting work.
- [8:07](https://www.youtube.com/watch?v=1rMgw0Q5MgY&t=487s) — Translate a prompt-driven workflow into explicit states and permitted transitions.
- [11:42](https://www.youtube.com/watch?v=1rMgw0Q5MgY&t=702s) — Use structured traces to inspect where a workflow succeeds or fails.
- [12:21](https://www.youtube.com/watch?v=1rMgw0Q5MgY&t=741s) — Evaluate transitions as well as individual states and final outcomes.
- [13:23](https://www.youtube.com/watch?v=1rMgw0Q5MgY&t=803s) — Give an improvement agent the machine, traces, and evaluations so it can propose revisions.
- [15:33](https://www.youtube.com/watch?v=1rMgw0Q5MgY&t=933s) — Implement the minimal state-machine execution loop without depending on a particular library.
- [16:24](https://www.youtube.com/watch?v=1rMgw0Q5MgY&t=984s) — Create, observe, improve, and compare successive workflow versions.

## Overview

Agent reliability improves when fixed process rules are moved out of prose and into an explicit graph of states and transitions. In the presenter’s email example, a model may draft and revise freely, but the workflow determines when sending is allowed and prevents it when required information is missing.

This approach matters to engineers building agents with approvals, tools, side effects, or multi-step interactions. Its main benefit is not merely constraining behavior: the graph creates an inspectable artifact whose states, edges, outcomes, and execution traces can be evaluated and systematically improved.

## Key Concepts

- **Deterministic transition**: A state machine maps a current state and an event to a predictable next state. Determinism belongs in process rules where repeated inputs should produce the same allowed transition, not necessarily in open-ended generated content.
- **Generative work**: Tasks such as drafting an email, choosing clarification questions, and revising prose can have many acceptable outputs. The model handles this flexible work inside boundaries established by the workflow.
- **Unstructured delegation**: The presenter uses this term for handing judgment, structure, implementation, and taste to one agent invocation. It can work, but failures are difficult to localize because both policy and execution are embedded in the same opaque interaction.
- **Mega-prompt control flow**: Instructions such as “first draft, then revise, and send only after approval” encode a workflow as prose. The presenter argues that these rules become less prominent as context grows and restrict the system to one prompt, model, and strategy.
- **Explicit state graph**: States describe meaningful workflow phases, while edges define which events may move execution between them. If no transition from drafting or reviewing leads directly to sending, that action is structurally unavailable from those states.
- **Structured execution trace**: A trace records visited states, received events, transitions, and executed effects. Unlike an undifferentiated transcript, it identifies where behavior diverged or where a workflow imposed needless steps.
- **Edge evaluation**: State evaluation checks work produced at one step, and outcome evaluation checks the final result. Edge evaluation examines whether the workflow chose an appropriate transition, exposing inefficient paths even when the final result is acceptable.
- **Workflow self-improvement**: An improvement agent receives the state machine, representative traces, and evaluation results, then proposes structural changes. The presenter reports that this method produced a second email workflow that drafted earlier and reduced repeated clarification passes.

## How It Works

1. List the non-negotiable invariants, such as “never invent a recipient” and “send only after explicit approval.”
2. Identify the flexible tasks that should remain model-driven, including drafting, clarification, and revision.
3. Model the workflow as named states—for example, requesting, drafting, reviewing, awaiting recipient, sending, and sent.
4. Define permitted events and transitions. Attach guards so sensitive transitions require validated conditions.
5. While the machine is active, execute the work associated with its current state: an LLM call, tool call, or asynchronous process.
6. Feed the resulting event back into the machine, determine the next state, and execute any approved effects.
7. Record structured traces containing states, events, transitions, and outcomes.
8. Evaluate individual state outputs, complete results, and the quality of paths between them.
9. Give the machine, traces, and evaluations to a separate improvement agent, then test its proposed revision against the same scenarios before adopting it.

## Training Exercise

Build a small deterministic email-drafting workflow.

1. Write three invariants: a draft must exist before sending, the user must explicitly approve it, and a recipient must be supplied rather than invented.
2. Define at least five states: drafting, reviewing, awaiting_approval, awaiting_recipient, and sent.
3. Draw or encode the allowed transitions. Verify that no transition from drafting or reviewing can invoke the send effect directly.
4. Keep email composition open-ended by using a model or a human-written placeholder function inside the drafting state.
5. Run three scenarios: complete information, missing recipient, and revision after review. Record every state and transition.
6. Evaluate both the final email and the path: count unnecessary questions, repeated states, and failed guards.
7. Propose a version-two graph that removes one inefficient transition while preserving all three invariants.
8. Replay the same scenarios against both versions and adopt the revision only if it improves the path without weakening the rules.

## Test Yourself

<details><summary>Which parts of an agent workflow should be deterministic, and which should remain generative?</summary>

Safety and process invariants—such as requiring a draft, explicit approval, and a known recipient before sending—should be encoded deterministically. Content generation, clarification questions, and revisions can remain model-driven because they require flexibility.

</details>

<details><summary>Why is a successful final result insufficient evidence that an agent workflow is well designed?</summary>

A workflow may pass outcome evaluations while taking an annoying or wasteful route. Evaluating transitions and reviewing traces reveals unnecessary clarification loops, poor sequencing, and other path-level problems.

</details>

<details><summary>How can a state machine support agent self-improvement without giving an agent unchecked control?</summary>

A separate improvement agent can inspect the explicit machine, execution traces, and evaluation results, then propose a revised version. The original and revised machines can be tested on the same scenarios before any change is accepted.

</details>

## Further Reading

- [Agent Conf event information](https://clstk.com/4rrdiXJ)
- [Agent Conf on X](https://x.com/AgentConf)
- [Callstack content](https://clstk.com/4hgag3F)
