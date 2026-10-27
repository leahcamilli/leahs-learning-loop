---
title: "Use Fast Mid-Tier Models as Research Subagents, Not Default Coders"
source: "https://www.youtube.com/watch?v=8WbW_n95wc4"
date: "2026-09-29"
tags: [ai-agents, coding-models, model-evaluation, cost-optimization, software-architecture]
source_type: "youtube"
source_fingerprint: "e0f4d27b35"
source_characters: 35980
channel: "Theo - t3․gg"
published: "2026-09-29"
duration_seconds: 1906
topics: [ai-models, ai-agents, claude, coding-agents]
kind: "opinion"
depth: 3
actionability: 2
---

## TL;DR

> Sonnet 5.5 appears most valuable as a fast research subagent that examines large codebases for a stronger model, rather than as the default model for coding or interface design. The practical lesson is to route models by task and evaluate total task cost, token use, latency, and output quality together.

## Key Takeaways

1. Route large-codebase investigation, architectural analysis, and hypothesis checking to Sonnet 5.5 while retaining a stronger model such as Opus 5.5 as the primary orchestrator.
2. Avoid judging model cost from input and output prices alone; cache-read charges, reasoning tokens, and total tokens consumed can erase an apparent price advantage.
3. Avoid max reasoning for ordinary work: the presenter reports cases where moving from x-high to max increased token usage by roughly 1,500% and sometimes reduced accuracy through overthinking.
4. Do not under-budget Anthropic models either; the presented benchmarks showed substantial performance losses at low reasoning effort, making medium, high, or x-high more practical candidates.
5. In the presenter’s large-codebase audit, Sonnet 5.5 reportedly performed slightly better than Opus 5.5, cost about half as much, and finished in roughly five minutes.
6. Higher generation speed does not guarantee faster task completion: the presenter’s game-building test took Sonnet 5.5 about 43 minutes versus 36 minutes for Opus because Sonnet generated far more tokens.
7. Use representative workload tests instead of relying on one benchmark; coding, architecture analysis, interface design, computer use, and long-running artifact creation expose different strengths.

## Key Moments

- [7:12](https://www.youtube.com/watch?v=8WbW_n95wc4&t=432s) — See how unchanged list prices can hide the model’s real per-task cost.
- [11:25](https://www.youtube.com/watch?v=8WbW_n95wc4&t=685s) — Learn why reasoning settings are token budgets rather than simple intelligence levels.
- [12:26](https://www.youtube.com/watch?v=8WbW_n95wc4&t=746s) — See how max reasoning reportedly caused a 1,500% token increase and possible overthinking.
- [16:06](https://www.youtube.com/watch?v=8WbW_n95wc4&t=966s) — Identify the practical reasoning range: avoid both low and max for most Anthropic workloads.
- [17:39](https://www.youtube.com/watch?v=8WbW_n95wc4&t=1059s) — Understand why high token throughput can still produce slower end-to-end completion.
- [21:19](https://www.youtube.com/watch?v=8WbW_n95wc4&t=1279s) — Reframe Sonnet as a tool called by stronger agents rather than a default interactive model.
- [22:52](https://www.youtube.com/watch?v=8WbW_n95wc4&t=1372s) — Review the large-codebase audit where Sonnet reportedly beat Opus slightly at about half the cost.
- [30:05](https://www.youtube.com/watch?v=8WbW_n95wc4&t=1805s) — Turn the evaluation into a routing strategy for research and verification subagents.

## Overview

The source evaluates Sonnet 5.5 through published benchmarks and the presenter’s own coding, repository-analysis, interface-design, and game-building experiments. Its central conclusion is counterintuitive: the model is not necessarily the best direct replacement for Opus 5.5, but it may be a particularly useful worker inside a multi-model agent system.

This matters to engineers designing coding-agent workflows because model selection should happen per task, not per project. Teams working with large repositories can potentially improve responsiveness and cost by delegating search-heavy analysis to a faster model while reserving the primary model for synthesis, implementation, and judgment.

## Key Concepts

- **Task-aware model routing**: Different tasks reward different model characteristics. The source recommends keeping Opus 5.5 or Fable 5.1 in charge while routing bounded repository research and verification to Sonnet 5.5.
- **Orchestrator and subagent roles**: An orchestrator decomposes work, delegates narrow investigations, and integrates the findings. A subagent does not need to be the best general-purpose coder if it can quickly return reliable evidence for a specific question.
- **Total task economics**: Headline token prices do not represent the full cost of an agent run. Cache reads, cache writes, reasoning consumption, output length, retries, and the number of tokens needed to finish all affect the final bill.
- **Reasoning budget**: The presenter characterizes low, medium, high, and x-high as ceilings that permit progressively more reasoning when needed. Max is described differently: it may force a large reasoning floor, which can increase consumption even when the task does not benefit.
- **Token efficiency versus generation speed**: Tokens per second measures how quickly text is emitted, not how quickly useful work finishes. A faster model can take longer overall if it produces substantially more tokens, as the presenter reports in the fish-game experiment.
- **Workload-specific benchmarking**: A single benchmark cannot establish the best model for every workflow. The source compares terminal operation, code analysis, interface design, computer use, and artifact creation, with noticeably different outcomes.
- **Repository-analysis workload**: The presenter’s most favorable Sonnet test required examining a very large codebase and proposing how to split a giant pull request. This tested comprehension, architectural reasoning, and explanation more than direct code generation.
- **Qualitative usability**: Formatting, clarity, instruction following, and interaction quality influence whether a model works well as a collaborator. The presenter reports clearer writing than earlier Sonnet generations but weaker frontend design results than Fable 5.1 and Opus 5.5.

## How It Works

1. Keep the strongest judgment-oriented model as the orchestrator.
2. Decompose the job into implementation tasks and bounded research questions.
3. Delegate repository searches, behavior tracing, architectural inventories, and hypothesis checks to the faster research model.
4. Ask each subagent for evidence: relevant files, relationships, risks, and uncertainties rather than an ungrounded recommendation.
5. Return those findings to the orchestrator for synthesis and implementation decisions.
6. Start with medium or high reasoning, raising it only when measured task quality justifies the extra cost; avoid max by default.
7. Record total cost, elapsed time, token consumption, and output usefulness for the complete task.
8. Adjust routing using results from your own representative workloads rather than benchmark rankings alone.

## Training Exercise

1. Choose a real repository and define one bounded question, such as how authentication state travels from an incoming request to database access.
2. Run the investigation with your primary model and save its findings, elapsed time, token totals, and estimated cost.
3. Run the same investigation with a cheaper or faster candidate model at medium reasoning, requiring file-level evidence and an explicit uncertainty list.
4. Repeat at high reasoning; use max only if you deliberately want to measure its overhead.
5. Score each result on evidence coverage, correctness, clarity, latency, and total cost.
6. Give the best candidate’s report to the primary model and ask it to verify the evidence and propose an implementation plan.
7. Adopt subagent routing only if the combined research-and-synthesis workflow improves cost or time without materially reducing correctness.

## Test Yourself

<details><summary>Why can a model with lower advertised input and output prices still cost as much as a premium model on an agentic coding task?</summary>

Agentic work repeatedly reads cached context and may generate large numbers of reasoning and output tokens. The presenter argues that Sonnet 5.5’s cache-read price and high token consumption can therefore offset its lower headline prices.

</details>

<details><summary>When does the source suggest using Sonnet 5.5 instead of Opus 5.5?</summary>

Use it as a delegated worker for bounded investigation: exploring a large repository, locating behaviors, checking a hypothesis, or preparing architectural findings. Opus remains the suggested primary model for general coding, judgment-heavy work, and orchestration.

</details>

<details><summary>Why is max reasoning not automatically the safest setting for a difficult task?</summary>

Max may impose a high minimum amount of reasoning instead of merely raising the allowed ceiling. According to the presenter’s tests, that can dramatically increase cost and latency while encouraging second-guessing that sometimes worsens results.

</details>

## Further Reading

- [Original YouTube source](https://www.youtube.com/watch?v=8WbW_n95wc4)
- [Presenter’s website and community links](https://t3.gg)
- [CodeRabbit sponsor link from the source](https://soydev.link/coderabbit)
