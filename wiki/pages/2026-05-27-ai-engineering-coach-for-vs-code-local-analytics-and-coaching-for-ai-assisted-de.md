---
title: "AI Engineering Coach for VS Code: Local Analytics and Coaching for AI-Assisted Development"
source: "https://www.linkedin.com/posts/joeunwin_aiengineering-githubcopilot-vscode-ugcPost-7465062561001136130-Nsgv/?utm_source=share&utm_medium=member_ios&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY"
date: "2026-05-27"
tags: [vscode, ai-engineering, copilot, developer-tools, privacy, agentic-workflows]
source_type: "web"
topics: [coding-agents, github-copilot, developer-tools, prompt-engineering]
kind: "tutorial"
depth: 2
actionability: 1
---

## TL;DR

> Treat AI-assisted coding as an observable engineering practice by measuring prompt quality, context health, review habits, and reusable workflows. Local, read-only analysis can provide coaching while keeping source code and interaction history private.

## Key Takeaways

1. Track prompt quality, context setup, review behavior, and weekly trends instead of relying only on acceptance rates or token counts.
2. According to the source, the VS Code extension analyzes session files locally with read-only access, no telemetry, and no external transmission of source data.
3. Use anti-pattern rules to flag vague prompts, stale sessions, weak context, inadequate code review, and undisciplined tool usage; the source describes a set of 45 checks.
4. Convert repeated prompts into durable templates, instruction files, or reusable skills so successful workflows become repeatable.
5. Before requesting code, specify the file or module, desired behavior, constraints, and tests or acceptance criteria.
6. Start a lightweight weekly review with prompts from 3–5 development sessions and compare vague prompts, context-rich prompts, and repeated prompts converted into templates.

## Overview

This lesson explains the idea behind an open-source VS Code extension that acts as an AI Engineering Coach: it analyzes how you use AI coding assistants, surfaces patterns in your workflow, and helps you improve over time. The source describes a tool focused on measurable practice, anti-pattern detection, context quality, and reusable prompting skills rather than just raw usage metrics.

This matters to engineers who rely on GitHub Copilot or similar assistants and want to become more effective at agentic development. The key design point is that analysis runs locally with read-only access to session files and no telemetry, making it suitable for teams and individuals who care about privacy, governance, and improving AI-assisted coding habits without sending source data to a cloud service.

## Key Concepts

- **AI engineering coach**: An AI engineering coach is a tool that evaluates how a developer works with coding assistants and provides feedback intended to improve outcomes. Instead of only measuring acceptance rates or token usage, it looks at workflow quality, prompt discipline, context setup, and repeatable behaviors.
- **Local-first analysis**: Local-first analysis means the extension performs processing on the developer's machine and avoids transmitting data externally. This reduces privacy risk, makes the tool easier to adopt in sensitive environments, and keeps source code and interaction history under the user's control.
- **Anti-pattern detection**: Anti-pattern detection refers to applying a set of rules to identify unproductive habits when working with AI assistants. Examples include vague prompts, poor session hygiene, weak context management, and over-reliance on generated code without sufficient review.
- **Practice and trend metrics**: Practice metrics turn day-to-day AI assistant usage into signals like scores, daily activity, and weekly trends. These metrics help engineers see whether they are improving, plateauing, or regressing in how they collaborate with AI over time.
- **Reusable skills discovery**: Repeated prompts often indicate an emerging workflow that could be formalized into a template, instruction file, or reusable skill. Discovering these repetitions helps engineers convert ad hoc prompting into structured, repeatable engineering practices.
- **Context health**: Context health is the quality of the information available to the AI assistant when it is asked to perform work. Good context includes clear instructions, organized workspace signals, and enough project-specific information for the assistant to act effectively without hallucinating or drifting.

## How It Works

At a high level, the extension described in the source behaves like an observability layer for AI-assisted software development inside VS Code. It inspects local session artifacts from tools like GitHub Copilot or similar assistants, computes metrics from those artifacts, and presents the results as dashboards, scores, and coaching insights. The stated design is privacy-preserving: analysis stays on the machine, there is no telemetry, and access to session files is read-only.

The core workflow can be understood as a pipeline:

1. **Collect local assistant interaction data** from session files or editor-visible history.
2. **Extract features** such as prompt frequency, repeated instructions, code generation volume, model usage, workspace distribution, and timing patterns.
3. **Apply rule-based analysis** to detect anti-patterns across categories like prompt quality, code review behavior, session hygiene, tool mastery, and context management.
4. **Aggregate metrics** into dashboards showing practice scores, daily activity charts, and weekly trend lines.
5. **Generate coaching outputs** such as warnings, improvement recommendations, context-health checks, and candidate reusable skills.

The source highlights several major functional areas:

- **Progress tracking**: practice scores and trend charts quantify whether your AI usage is becoming more disciplined and effective.
- **Anti-pattern analysis**: a rule set of 45 checks flags behaviors that commonly reduce the quality of AI-assisted coding.
- **Output measurement**: generated code can be broken down by language, workspace, model, and harness, giving teams a practical way to understand where AI is contributing.
- **Skill discovery**: repeated prompts are mined to find latent workflows that should become templates or explicit instructions.
- **Context health scoring**: readiness checks evaluate whether your environment is set up to support strong agentic behavior.

A useful way to think about the mechanics is to separate **descriptive analytics** from **prescriptive coaching**. Descriptive analytics answers questions like: How much AI-generated code did I produce this week? Which languages or workspaces saw the most AI activity? How often am I using the same prompt shape? Prescriptive coaching goes further: It points out what to change, such as tightening prompts, improving project instruction files, cleaning session context, or reviewing generated code more rigorously.

The anti-pattern categories in the source are especially important because they imply a maturity model for AI-assisted development:

- **Prompt quality**: Are prompts specific, constrained, and outcome-focused?
- **Session hygiene**: Are sessions managed cleanly, or does stale context accumulate?
- **Code review**: Is generated output being validated, tested, and inspected?
- **Tool mastery**: Is the engineer using the assistant intentionally, or just interactively guessing?
- **Context management**: Does the assistant receive the right files, instructions, and workspace cues?

The context-health capability suggests the extension also inspects the surrounding development environment, not just chat transcripts. For example, an instruction-file audit likely checks whether durable guidance exists for the assistant, and a workspace context map likely summarizes what code areas or repositories are being involved in AI-assisted work. This is important for agentic workflows, where the assistant performs better when the environment is well structured and project expectations are explicit.

Because the source is a social post rather than a technical spec, the exact implementation details are not listed. But the architecture implied by the feature set would typically include:

- a **data ingestion layer** for local session files
- a **normalization step** to unify assistant events into a common schema
- a **rules engine** for anti-patterns and readiness checks
- a **metrics layer** for scores and trend aggregation
- a **UI layer in VS Code** for charts, findings, and coaching recommendations

For a working engineer, the biggest insight is that this kind of tool shifts AI coding assistance from a subjective habit into an observable engineering practice. Instead of asking "Do I feel more productive with Copilot?", you can ask: "Am I improving my prompt quality? Am I creating reusable workflows? Is my context setup good enough for agentic tasks?"

## Training Exercise

Build a lightweight version of the coaching approach for your own workflow using local logs or a manual prompt journal.

### Goal
Create a small weekly review that measures three things:

1. repeated prompts
2. anti-patterns in prompting
3. context quality before asking an AI assistant for code

### Step 1: Collect a small dataset
For 3-5 development sessions, save the prompts you gave your AI assistant into a local text or JSON file. If your tool exposes local history, export or copy a subset manually. Keep everything on your machine.

Example JSON format:

```json
[
  {
    "timestamp": "2026-05-27T09:00:00Z",
    "workspace": "payments-service",
    "language": "typescript",
    "prompt": "Add retries to this API client and include tests",
    "notes": "Provided current file and failing test context"
  },
  {
    "timestamp": "2026-05-27T10:30:00Z",
    "workspace": "payments-service",
    "language": "typescript",
    "prompt": "Fix this",
    "notes": "No extra context provided"
  }
]
```

### Step 2: Define three anti-pattern rules
Create a simple ruleset such as:

- prompt shorter than 12 characters => likely too vague
- prompt contains phrases like `fix this` or `make it better` => underspecified
- no notes/context attached => weak context hygiene

### Step 3: Run a local analysis script
Use this Python script to score your prompt set:

```python
import json
from collections import Counter

with open("prompts.json") as f:
    data = json.load(f)

repeated = Counter(item["prompt"].strip().lower() for item in data)

anti_patterns = []
for item in data:
    p = item["prompt"].strip().lower()
    notes = item.get("notes", "").strip()
    issues = []

    if len(p) < 12:
        issues.append("too_short")
    if "fix this" in p or "make it better" in p:
        issues.append("underspecified")
    if not notes:
        issues.append("missing_context")

    anti_patterns.append({
        "timestamp": item["timestamp"],
        "prompt": item["prompt"],
        "issues": issues
    })

print("Repeated prompts:")
for prompt, count in repeated.items():
    if count > 1:
        print(f"- {count}x: {prompt}")

print("\nPrompt issues:")
for row in anti_patterns:
    if row["issues"]:
        print(f"- {row['timestamp']}: {row['prompt']} -> {', '.join(row['issues'])}")
```

### Step 4: Turn one repeated prompt into a reusable skill
Pick a repeated prompt and rewrite it as a stable template. For example:

```text
Task: modify an API client.
Constraints: preserve public interface, add tests, explain tradeoffs.
Context to include: target file, related tests, expected retry behavior, failure modes.
Output: patch plan, code changes, test changes.
```

### Step 5: Add a pre-prompt context checklist
Before your next AI-assisted coding task, answer:

- What file or module is in scope?
- What exact behavior should change?
- What constraints must remain true?
- What tests or acceptance criteria define success?

### Step 6: Review weekly trends
At the end of a week, manually compare:

- number of vague prompts
- number of prompts with explicit context
- number of repeated prompts converted into templates

### Success criteria
You should finish with:

- one local prompt dataset
- one simple anti-pattern detector
- one reusable prompt template
- one context checklist you can use before asking for code generation

This exercise mirrors the extension's core value proposition: turning AI assistant usage into something observable, improvable, and privacy-preserving.

## Test Yourself

<details><summary>How does prescriptive coaching differ from descriptive analytics in AI-assisted development?</summary>

Descriptive analytics reports what happened, such as generated-code volume, model usage, or repeated prompts. Prescriptive coaching recommends changes, such as improving instructions, cleaning session context, or reviewing generated code more rigorously.

</details>

<details><summary>What three simple anti-pattern rules does the training exercise propose?</summary>

Flag prompts shorter than 12 characters, prompts containing phrases such as “fix this” or “make it better,” and entries with no attached notes or context.

</details>

<details><summary>What should a developer establish before asking an AI assistant to generate code?</summary>

Identify the file or module in scope, the exact behavior to change, the constraints that must remain true, and the tests or acceptance criteria that define success.

</details>

## Further Reading

- [Visual Studio Code Extension API](https://code.visualstudio.com/api)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Microsoft Responsible AI Resources](https://www.microsoft.com/ai/responsible-ai)
