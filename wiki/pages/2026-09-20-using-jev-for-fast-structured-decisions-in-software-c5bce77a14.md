---
title: "Using Jev for Fast, Structured Decisions in Software"
source: "https://www.youtube.com/watch?v=ZgXej_9isxY"
date: "2026-09-20"
tags: [ai-models, decision-systems, structured-output, typescript, application-design]
source_type: "youtube"
source_fingerprint: "c5bce77a14"
source_characters: 19317
channel: "Codevolution"
published: "2026-09-19"
duration_seconds: 1332
topics: [classifiers-and-structured-output]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> Jev is a decision-focused AI model that turns application state and narrowly defined questions into structured probabilities, choices, or scores. It matters when software needs fast, repeated semantic judgments, while deterministic rules and generative tasks should remain with ordinary code or text-generating models.

## Key Takeaways

1. Use deterministic code for exact conditions such as counting basket items, arithmetic, or comparing dates; use Jev when the condition requires semantic judgment.
2. Choose null questions for binary judgments, choice questions for application-defined categories, and score questions for descriptive ordinal scales.
3. Interpret a null result near 0 as evidence for “no” and a result near 0.5 as little preference in either direction.
4. Add an “other” option when choice categories may not cover every input, and describe every score level instead of using an unexplained numeric scale.
5. Write every question so it can be answered from the state alone because Jev evaluates multiple questions independently and in parallel.
6. Calibrate action and review thresholds with representative labeled examples; the source warns that high confidence does not guarantee correctness.
7. Type Safe reported 70–500 millisecond response times and pricing of 4.2 cents per million input tokens with free output tokens, but these time-sensitive vendor claims should be verified before adoption.

## Overview

Jev is a decision-focused AI model from Type Safe. It acts like a semantic “if statement”: an application sends some information, called the state, plus one or more questions, and receives structured probabilities, choices, or scores. Unlike general-purpose generative models, Jev is intended to judge information rather than write replies, summaries, or code. The source reports end-to-end response times of 70–500 milliseconds and a price of 4.2 cents per million input tokens, with output tokens free at the time described. These are vendor-reported and time-sensitive figures, so verify current performance, access, and pricing before designing around them.

## Key Concepts

- **Semantic decision-making**: Jev handles conditions that are difficult to express with exact rules, such as whether a customer sounds frustrated. Use ordinary code when the answer is deterministic—for example, checking whether a basket contains at least three items.
- **State and questions**: A request contains the state—the information to evaluate—as plain text, a JSON object, or an array. It also contains named questions. The response associates each structured answer with its question name.
- **Null questions**: A null question represents a yes-or-no judgment but returns the probability of “yes” between 0 and 1. A result near 0 indicates evidence for “no,” not uncertainty; a value near 0.5 indicates little preference either way.
- **Choice questions**: A choice question selects from options supplied by the application and returns probabilities for every option. Include a fallback such as “other” when inputs may not fit the main categories.
- **Score questions**: A score question evaluates state against a described scale. Levels start at zero, and the result is a probability-weighted average, so it may fall between levels. Descriptive levels are more actionable than an unexplained numeric scale.
- **Parallel, independent evaluation**: Multiple questions about the same state can be submitted in one request. Jev evaluates them independently and in parallel, so each question must make sense from the state alone and cannot depend on another answer.
- **Confidence and thresholds**: Choice and score answers include confidence based on their probability distributions; null answers expose the yes probability directly. Confidence does not guarantee correctness. Production thresholds should be calibrated with representative examples, with ambiguous cases routed to human review.
- **Decision model versus generator**: Jev is suitable for routing, classification, claim-support checks, guardrails, model selection, and other repeated judgments. It is not a replacement for a generative model when the task requires composing text, summarizing material, explaining an answer, or generating code.

## How It Works

Define a narrowly scoped decision and collect representative inputs. Put the relevant input into the request state, preferably as clearly named JSON fields. Add one or more named questions using the appropriate type: null for a binary judgment, choice for a closed set of categories, or score for a described ordinal scale. For choice questions, make the options exhaustive or add an “other” category. For score questions, explain what every level means. Send the request through Type Safe’s playground or SDK; the source demonstrates the TypeScript SDK, a Typesafe client, and client.system1. The response contains the model version, token usage, and an answer for each question. Null returns the probability of yes. Choice returns the selected option, option probabilities, and confidence. Score returns a weighted score, level probabilities, confidence, and a legend. Application code then applies a calibrated threshold: high-confidence results can trigger an action, while uncertain or consequential cases should be reviewed. Test against labeled, realistic examples because even confident judgments can be wrong. Also compare the model with a deterministic implementation first—AI adds value only when the condition requires semantic judgment.

## Training Exercise

Build a customer-support triage prototype. Use JSON state containing a message and submit three questions in one request: (1) a null question asking whether the message expresses frustration; (2) a choice question classifying the main request as update, refund, replacement, or other; and (3) a score question with levels 0 = request without frustration, 1 = dissatisfaction without strong anger, and 2 = strong anger. Create at least 20 representative messages, including polite complaints, implicit frustration, mixed requests, and irrelevant messages. Record the outputs and manually label the expected decisions. Choose action and review thresholds from these examples rather than copying the demonstration threshold of 0.8. Then test new messages and measure incorrect automatic actions, review frequency, latency, and token usage. Finally, identify one condition in the workflow that should remain deterministic code and explain why.

## Test Yourself

<details><summary>When should an application use Jev instead of an ordinary if statement?</summary>

Use Jev when the decision depends on meaning or context, such as whether a message implies frustration. Use ordinary code when the answer can be calculated exactly, such as whether a basket contains at least three items.

</details>

<details><summary>How do null, choice, and score questions differ?</summary>

Null returns the probability that a yes-or-no judgment is yes. Choice distributes probabilities across supplied options and selects one, while score evaluates descriptive levels and returns a probability-weighted value that may fall between them.

</details>

<details><summary>Why should production code not simply copy the demonstration threshold of 0.8?</summary>

The source presents 0.8 only as a demonstration value and warns that confidence does not guarantee correctness. Teams should select thresholds using representative labeled inputs, measuring incorrect automatic actions and routing ambiguous or consequential cases to review.

</details>

## Further Reading

- [Source video: Jev overview and TypeScript demonstration](https://www.youtube.com/watch?v=ZgXej_9isxY)
