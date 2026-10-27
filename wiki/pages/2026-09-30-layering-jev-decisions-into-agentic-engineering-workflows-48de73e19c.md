---
title: "Layering Jev Decisions Into Agentic Engineering Workflows"
source: "https://www.youtube.com/watch?v=_U-O5lYhJ7Q"
date: "2026-09-30"
tags: [agentic-engineering, model-routing, guardrails, context-management, prompt-engineering]
source_type: "youtube"
source_fingerprint: "48de73e19c"
source_characters: 45570
channel: "IndyDevDan"
published: "2026-09-28"
duration_seconds: 2117
topics: [ai-agents, classifiers-and-structured-output, coding-agents]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> Use Jev for narrow, structured decisions—classification, scoring, routing, confidence gates, and file triage—while reserving coding agents for reasoning and code changes. This division can reduce cost and context usage, but each decision policy must be validated against your own production workload.

## Key Takeaways

1. Define decisions as JSON state, questions, allowed answers, and scoring criteria; let application code determine what happens next.
2. Use confidence to control workflow behavior: automate high-confidence, low-risk outcomes and escalate uncertain or costly-to-reverse decisions.
3. Place narrow classification ahead of expensive work to select the appropriate model, agent, or workflow.
4. Add pre-tool guardrails around dangerous shell commands and protected-file writes, but do not treat classification as a substitute for permissions, review, or testing.
5. Ask questions about files without loading them into the coding agent’s context when the agent only needs classification or relevance information.
6. Scale file triage across globs or repositories, then let the coding agent read only the files required for editing.
7. At the most advanced level, expose Jev as a tool so the agent can classify failures and validate assumptions, while keeping actual diagnosis, editing, and testing with the coding agent.

## Key Moments

- [1:03](https://www.youtube.com/watch?v=_U-O5lYhJ7Q&t=63s) — See a yes/no prompt-injection check framed as a fast, structured decision.
- [6:43](https://www.youtube.com/watch?v=_U-O5lYhJ7Q&t=403s) — Learn how separately defined criteria become a weighted composite score.
- [9:16](https://www.youtube.com/watch?v=_U-O5lYhJ7Q&t=556s) — Use confidence and reversibility to decide whether a shell command should be blocked or escalated.
- [12:56](https://www.youtube.com/watch?v=_U-O5lYhJ7Q&t=776s) — Route a request to the agent whose tools and harness match the task.
- [14:57](https://www.youtube.com/watch?v=_U-O5lYhJ7Q&t=897s) — Watch a Pi coding-agent pre-tool hook block destructive commands before execution.
- [18:04](https://www.youtube.com/watch?v=_U-O5lYhJ7Q&t=1084s) — Trigger context compaction from token thresholds and evidence that the task has changed.
- [20:38](https://www.youtube.com/watch?v=_U-O5lYhJ7Q&t=1238s) — Question a file through Jev without putting its contents into the coding agent’s context.
- [29:53](https://www.youtube.com/watch?v=_U-O5lYhJ7Q&t=1793s) — Let an agent use Jev to classify a test failure and check assumptions during a fix.

## Overview

Jev is presented as programmable question answering: an application supplies state, structured questions, and allowed answers through JSON, then interprets the returned choices, scores, and confidence values. The lesson progresses from a “smart if statement” through triage, scoring, routing, tool-call guardrails, context compaction, and repository-scale file classification.

The central architectural idea is specialization. Narrow decisions can be delegated to a focused system-one model, while coding agents retain responsibility for complex reasoning and implementation. Agent-harness builders and teams operating high-volume agent workflows should care most, because the presenter reports substantial speed, cost, and context savings; those claims require workload-specific benchmarking before production adoption.

## Key Concepts

- **Structured decision contract**: A Jev request encodes relevant state, questions, permissible answers, and natural-language criteria in JSON. The model answers within that contract, while ordinary application code decides what action follows.
- **Decision types**: The examples use booleans for yes/no checks, choices for bounded categories, and scores for graded criteria. Selecting the narrowest suitable output type makes downstream behavior easier to inspect and test.
- **Composite scoring**: Several independently defined criteria can be scored and combined with weights in code. This separates the model’s judgments from the application’s priority formula, so tuning a policy may involve changing weights rather than rewriting the entire prompt.
- **Confidence gating**: Confidence becomes an input to control flow rather than a decorative number. The system can accept a high-confidence, low-risk result while escalating ambiguity or any decision whose failure would be expensive.
- **Intent and capability routing**: A cheap classification can precede expensive execution and select a model, specialized agent, or complete workflow. In the examples, browsing tasks go to a browser-equipped agent while localized fixes go to a faster agent.
- **Agent guardrail hooks**: A pre-tool hook can classify shell commands or writes before the agent acts. The examples block force pushes, destructive deletion, and writes to protected files, although this probabilistic layer should complement deterministic access controls.
- **Context-aware compaction**: Jev can inspect signals such as context size, task boundaries, and recent activity to recommend or request compaction. This allows a long-running harness to compact because the work has meaningfully changed, not solely because a fixed token limit was crossed.
- **Out-of-context file triage**: The harness can send file contents and a narrow question to Jev without placing those contents in the coding agent’s context. The pattern scales across multiple files or recursive globs, after which the agent reads only the files it must understand or modify.

## How It Works

1. Identify a bounded decision, such as “Is this command reversible?” or “Which files are relevant to this bug?”
2. Encode only the necessary state, questions, allowed answers, and concrete criteria in JSON.
3. Call Jev and retain the selected answer, alternative probabilities, scores, and confidence.
4. Apply an explicit policy in code: proceed, block, route, ask a human, invoke a stronger model, or request more evidence.
5. For agent integration, expose the decision as a pre-tool hook or a narrow tool such as `ask_jev_file_bool` or `ask_jev_files`.
6. Keep execution responsibilities separate: the coding agent reads and edits relevant files, while deterministic controls protect critical resources.
7. Verify consequential outcomes through tests, review, and benchmarks on representative production cases. Measure false positives, false negatives, latency, cost, and context savings rather than relying on the presenter’s comparisons alone.

## Training Exercise

1. Choose one bounded workflow decision, such as classifying shell commands as `read_only`, `reversible`, or `irreversible`.
2. Write JSON criteria for each category and assemble at least 20 examples, including ambiguous commands and variants you did not explicitly name in the criteria.
3. Run the classifier in observation-only mode; do not execute or block commands based on its result yet.
4. Record the predicted class, confidence, expected class, latency, and cost for every case.
5. Define a policy such as: allow high-confidence read-only commands, require confirmation for reversible mutations, and block or escalate irreversible commands.
6. Compare that policy with deterministic allowlists and a stronger model, paying special attention to dangerous false negatives.
7. Only after evaluation, add the classifier as one layer in a pre-tool hook while retaining sandboxing, permissions, logs, and human review for high-impact actions.

## Test Yourself

<details><summary>When should a narrow Jev decision replace a full coding-agent call?</summary>

Use it when the state, question, and permitted outputs can be defined clearly, such as classification, scoring, routing, or relevance checks. Keep the full agent for open-ended reasoning, editing, tool use, and other work requiring broader context.

</details>

<details><summary>Why is confidence part of the workflow rather than merely diagnostic metadata?</summary>

The cost of a wrong answer varies by action. Confidence can determine whether the system proceeds automatically, asks a human, invokes a stronger model, or blocks an irreversible operation.

</details>

<details><summary>How can file-level questioning reduce context consumption without preventing code changes?</summary>

First ask narrow questions across candidate files without loading them into the coding agent’s context. Once relevant files are identified, allow the agent to read and edit only those files, then verify the result with normal tests and review.

</details>

## Further Reading

- [10 Levels of Jev example repository](https://github.com/disler/ten-levels-of-jev)
- [Introducing system-one models and Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- [Agent Swarms](https://youtu.be/S2sjyokoxeE)
- [Self-Compact Pi Agent](https://youtu.be/3b0U4_02bAE)
- [Build Your Software Factory](https://youtu.be/haUfb1ievTE)
