---
title: "Choosing AI Coding Models by Workflow Fit, Reliability, and Total Cost"
source: "https://www.youtube.com/watch?v=vu8X3YroB-w"
date: "2026-09-29"
tags: [ai-coding, coding-agents, model-evaluation, code-review, agentic-workflows, llm-costs]
source_type: "youtube"
source_fingerprint: "86469d5d8a"
source_characters: 34257
channel: "Theo - t3․gg"
published: "2026-09-29"
duration_seconds: 1858
topics: [ai-models, ai-agents, llm-evaluation, coding-agents]
kind: "opinion"
depth: 2
actionability: 2
---

## TL;DR

> GPT 6.1 Soul is presented as a fast, inexpensive model for scoped coding tasks, investigation, and deep review, but not as the strongest choice for autonomous rewrites or frontend design. The practical strategy is to pair it with a stronger implementation model rather than choose one model for every job.

## Key Takeaways

1. Match models to roles: use GPT 6.1 Soul for investigation, codebase audits, and review, while retaining Opus 5.5 for long, unattended implementation work.
2. Evaluate reliability alongside peak intelligence; the presenter found GPT 6.1 Soul less prone than Astra to sudden low-quality behavior, even though Astra retained higher peaks in some tasks.
3. Account for cache reads when estimating agent costs: the presenter reports prices of $2 per million input tokens, $10 per million output tokens, and $0.10 per million cached input tokens.
4. Treat benchmark results as directional evidence; the presenter discloses incomplete runs, configuration mistakes, excluded GPU-dependent tasks, and scores that changed as runs completed.
5. Keep humans in control for consequential actions: the reported invoice workflow prepared browser tabs and payment details but left the final send action to the user.
6. Do not infer implementation quality from visual fidelity; the generated game looked impressive but reportedly had poor movement, frame rate, gameplay, and interface design.
7. A reviewer–implementer loop can outperform a single-model workflow: GPT 6.1 Soul reportedly found regressions and unused code that other models missed, while Opus handled implementation more effectively.

## Key Moments

- [3:41](https://www.youtube.com/watch?v=vu8X3YroB-w&t=221s) — Learn why the presenter treats his benchmark results as provisional rather than definitive.
- [7:19](https://www.youtube.com/watch?v=vu8X3YroB-w&t=439s) — See how discounted cache reads can dominate the economics of agentic coding workloads.
- [10:59](https://www.youtube.com/watch?v=vu8X3YroB-w&t=659s) — Understand the reported reliability improvement over Astra and the limits that remain.
- [13:03](https://www.youtube.com/watch?v=vu8X3YroB-w&t=783s) — See why deep code review and codebase auditing emerge as the model’s strongest roles.
- [16:10](https://www.youtube.com/watch?v=vu8X3YroB-w&t=970s) — Learn where the model reportedly stalls during long, unattended rewrites.
- [21:24](https://www.youtube.com/watch?v=vu8X3YroB-w&t=1284s) — Derive a task-routing strategy that combines Soul’s investigation with Opus’s implementation.
- [24:34](https://www.youtube.com/watch?v=vu8X3YroB-w&t=1474s) — Observe the gap between strong 3D asset generation and weak UI or gameplay judgment.
- [26:37](https://www.youtube.com/watch?v=vu8X3YroB-w&t=1597s) — Follow a real review loop in which the model identifies regressions missed by other models.

## Overview

The source evaluates GPT 6.1 Soul as a coding-agent model through provisional benchmarks and hands-on work involving code review, computer use, codebase improvement, a Rust rewrite, and game generation. Its central lesson is that model selection should be based on task shape, behavioral reliability, and real workload cost—not a single leaderboard score.

The presenter’s preferred workflow assigns GPT 6.1 Soul scoped analytical work and uses Opus 5.5 for extended implementation. This matters to engineers operating coding agents because a model can be excellent at finding defects yet poor at sustaining progress, or visually impressive yet weak at interaction design.

## Key Concepts

- **Task–model fit**: Model quality is multidimensional: review, implementation, computer use, visual generation, and product design require different capabilities. The presenter considers GPT 6.1 Soul strong for bounded investigation and review but weaker for long autonomous rewrites and frontend work.
- **Behavioral spikiness**: Spikiness is the tendency to alternate between excellent and inexplicably poor behavior. The presenter reports that GPT 6.1 Soul has lower peaks than Astra in some areas but is substantially less spiky, making it easier to trust for routine work.
- **Cached-token economics**: Agents repeatedly reuse large prompts, repository context, and conversation history, so cached input can be a major share of consumption. The presenter reports a cached-input price of $0.10 per million tokens and cites an analysis in which agent sessions were 96% cache reads, making this price more consequential than headline input pricing.
- **Scoped versus unattended work**: Scoped work has a defined objective and bounded search space, such as reviewing a pull request or locating a bug. Unattended work requires sustained judgment and recovery across a long sequence; the presenter reports that Soul followed process rules even when they stopped progress and did not ask for help.
- **Reviewer–implementer separation**: One model can implement while another independently audits its work. In the reported workflow, Opus produced changes while GPT 6.1 Soul inspected them for regressions, hidden gaps, and unnecessary code.
- **Benchmark uncertainty**: Benchmark scores depend on harness configuration, hardware, reasoning settings, and completed samples. The presenter explicitly warns that his numbers were still changing, some runs were incomplete, earlier configurations were wrong, and three H100-dependent tasks were removed.
- **Output quality versus product quality**: High-fidelity assets do not guarantee good interaction design or usable software. The generated aquarium reportedly had attractive fish and 3D elements but suffered from cluttered UI, weak movement, poor frame rate, and a shallow or confusing gameplay loop.

## How It Works

1. Classify the task before selecting a model: distinguish review, investigation, bounded implementation, long autonomous work, computer use, and design.

2. Test candidates on representative repository tasks rather than relying solely on public benchmarks. Record correctness, regressions found, completion rate, elapsed time, token use, and human cleanup.

3. Calculate effective cost from input, output, and cached-input usage. For repetitive agent workflows, inspect the cache-read share because it can dominate total spend.

4. Route bounded analysis and independent review to GPT 6.1 Soul when local tests confirm the reported strengths. Preserve a human approval step for payments, merges, deployments, and other consequential actions.

5. Route prolonged implementation or major rewrites to the model that demonstrates sustained progress and good judgment. In the presenter’s tests, that remained Opus 5.5.

6. Run a second-model audit before merging. Return concrete findings to the implementing model, request fixes, and repeat until the review finds no material gaps.

7. Escalate or stop agents that obey a process without advancing the objective. Long loops can waste time even when low token prices make them financially affordable.

## Training Exercise

1. Choose a small pull request or isolated bug in a non-production repository and define acceptance criteria plus a fixed spending limit.
2. Ask one model to investigate the relevant code and produce a risk-ranked review without editing files.
3. Ask a second model to implement the fix using the review and acceptance criteria.
4. Send the resulting diff back to the first model for an independent audit covering correctness, regressions, dead code, and missing tests.
5. Run the project’s tests and manually verify the affected behavior; do not merge based only on either model’s report.
6. Record elapsed time, input/output/cache usage, defects found, false positives, stalled steps, and human corrections.
7. Repeat with the model roles reversed, then choose default routing rules based on observed completion quality and total workflow cost.

## Test Yourself

<details><summary>Why is the lowest token price not sufficient for choosing a coding model?</summary>

Total value depends on cache pricing, token utilization, task duration, reliability, and whether the model completes the work correctly. A cheap run that stalls for days can cost more in engineering time than a pricier model that finishes.

</details>

<details><summary>What evidence supports assigning GPT 6.1 Soul a reviewer role rather than making it the sole implementer?</summary>

The presenter reports that it uncovered regressions, deeply audited codebases, and identified 1.3 million unused lines. He also reports that it stalled on a long Rust rewrite and produced code that was harder to justify merging than Opus-generated code.

</details>

<details><summary>How should the benchmark claims in the source influence a purchasing decision?</summary>

Use them as hypotheses to test on representative internal tasks, not as universal rankings. The presenter acknowledges incomplete runs, setup errors, excluded tasks, variable scores, and imperfect correspondence between benchmarks and daily coding work.

</details>
