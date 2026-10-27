---
title: "Designing Fast AI Classification Workflows with Typed Outputs and Confidence Scores"
source: "https://www.youtube.com/watch?v=4mTLpuQpB80"
date: "2026-09-18"
tags: [ai-classification, decision-systems, workflow-automation, structured-data, human-in-the-loop]
source_type: "youtube"
source_fingerprint: "cae08480a9"
source_characters: 28324
channel: "Greg Isenberg"
published: "2026-09-18"
duration_seconds: 1704
topics: [classifiers-and-structured-output]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> Use typed, schema-constrained AI outputs and confidence thresholds to turn high-volume inputs into actions without parsing free-form text. This approach is best for low-risk triage; high-stakes or ambiguous decisions still need evaluation and human review.

## Key Takeaways

1. Define only the output fields and types the workflow needs, such as category, priority, spam score, and reply likelihood.
2. Convert confidence scores into explicit routing rules: automate clear cases, escalate urgent items, and send uncertain results to human review.
3. Evaluate reliability on representative labeled examples because the described classifier does not provide a visible rationale.
4. Record inputs, predictions, human decisions, latency, and errors so thresholds can be refined without changing the test labels.
5. Treat the speakers’ claims of roughly 200 ms per query and $0.18 for classifying 1,700 emails as anecdotal, not guaranteed benchmarks.
6. Keep tasks requiring current information, deep analysis, or high-stakes judgment outside full automation; the reported Bitcoin-trading experiment performed poorly.

## Overview

The source presents Jev as a specialized AI classifier rather than a conversational text generator. An application supplies an input object, such as an email or support request, together with a predefined output schema. The model returns structured classifications and probability-like scores that software can use immediately. Demonstrations include email triage, lead scoring, support routing, video-clip selection, service matching, and browser control. The speakers claim very low latency and cost—for example, classifying 1,700 emails containing 4.2 million input tokens and 500,000 output tokens for $0.18, plus roughly 200 ms per query—but the transcript supplies no independent benchmark or methodological details, so these figures should be treated as anecdotal. The model also performed poorly in an experimental Bitcoin-trading use case, illustrating that fast classification is not a substitute for deep analysis, current information, or high-stakes judgment.

## Key Concepts

- **Classifier rather than chatbot**: Jev is described as accepting data and selecting among predefined outcomes. It is not primarily used by asking an open-ended question, and it does not ordinarily generate explanations or conversational prose.
- **Schema-constrained output**: The developer defines the permitted output fields and types in advance—for example, category, priority, spam score, and reply likelihood. The result can then be consumed directly by application code instead of being parsed from free-form text.
- **Confidence-based decisions**: Outputs may represent degrees of confidence rather than absolute truth. A spam score of 0.90, for example, can be interpreted as strong evidence of spam while still preserving uncertainty for downstream policy.
- **Decision thresholds and routing**: Applications convert scores into actions: ignore low-value items, automate routine cases, or escalate important and ambiguous cases to a person. Jev therefore acts like a traffic controller at the front of an information queue.
- **High-volume triage**: The strongest examples involve repetitive decisions over many inputs: categorizing email, ranking inbound leads, routing support requests, matching service inquiries, or scoring moments in a transcript for short-form clips.
- **Speed and cost as design enablers**: The speakers argue that inexpensive, low-latency classification makes per-item decisions practical inside interactive workflows. Their numerical claims are demonstrations rather than independently verified performance guarantees.
- **Task boundaries and risk**: The source reports weak results when the model was used for Bitcoin buy, hold, or sell signals. Classification should remain advisory when mistakes have serious financial or operational consequences, particularly when a task requires external research or sophisticated reasoning.

## How It Works

First, represent the item to be classified as structured input, such as an email containing its sender, subject, body, and metadata. Next, define a compact output schema containing only the decisions the workflow needs—for example, category from a fixed list, priority from a fixed scale, spam probability from 0 to 1, and reply probability from 0 to 1. Submit the input and schema to the classifier. The returned typed object can be evaluated by ordinary program logic: discard messages above a conservative spam threshold, route finance messages to the finance queue, request human review when confidence is weak, and immediately escalate urgent messages with high reply likelihood. Record the input, output, subsequent human decision, latency, and error outcome so that thresholds can be tested and refined. Because the model does not provide a visible rationale in the described interface, reliability must be established through evaluation on representative labeled examples rather than by trusting persuasive explanations.

## Training Exercise

Build a paper prototype for support-ticket triage. Define an input with a subject, body, customer tier, and product name. Define outputs for destination team, urgency score, spam score, and human-review score. Create 20 varied tickets, including obvious cases, ambiguous cases, spam, and one potentially severe account problem. Manually assign expected outcomes before running any classifier. Then design routing rules such as: escalate when urgency is at least 0.85; send to human review when the winning category is below 0.70 confidence; otherwise route automatically. Compare predicted and expected outcomes, inspect false escalations and missed urgent cases, and adjust thresholds without changing the test labels. Conclude by listing decisions that are safe to automate, decisions that require review, and high-stakes decisions—such as trading—that should remain outside the system.

## Test Yourself

<details><summary>Why are typed outputs preferable to free-form text in an automated classification workflow?</summary>

Typed outputs conform to a predefined schema, so application code can use fields such as category and confidence directly instead of parsing prose. This makes routing rules simpler and more reliable.

</details>

<details><summary>How should an application turn confidence scores into actions?</summary>

It should apply explicit thresholds, such as escalating urgency scores of at least 0.85 and requesting human review when category confidence is below 0.70. Clear, low-risk cases can be routed automatically.

</details>

<details><summary>Why should the source’s speed, cost, and trading results affect how Jev is deployed?</summary>

The claimed latency and cost lack independent benchmarking, so teams should validate them in their own environment. The poor Bitcoin-trading result also shows that fast classification is not a substitute for current information, deep reasoning, or human judgment in high-stakes settings.

</details>

## Further Reading

- [Source video: Jev discussion and demonstrations](https://www.youtube.com/watch?v=4mTLpuQpB80)
