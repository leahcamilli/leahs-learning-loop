---
title: "Building Multi-Model AI Workflows with GitHub Copilot CLI"
source: "https://www.youtube.com/watch?v=rJSsbHwkYAY"
date: "2026-05-12"
tags: [github-copilot, cli, llm, ai-workflows, developer-tools]
source_type: "youtube"
channel: "Burke Holland"
published: "2026-03-31"
duration_seconds: 1095
topics: [github-copilot, developer-tools, coding-agents, automation-workflows]
kind: "tutorial"
depth: 2
actionability: 3
---

## TL;DR

> Use GitHub Copilot CLI as one stage in a shell-based engineering loop: gather focused repository evidence, plan, make a small change, review it, and verify it locally. This matters because narrow, composable prompts keep AI grounded while tests, tooling, and human inspection remain the source of truth.

## Key Takeaways

1. Break broad engineering tasks into context gathering, diagnosis, planning, generation, review, and verification stages.
2. Feed concrete artifacts such as `git diff`, compiler errors, stack traces, logs, and failing test output into prompts instead of relying on abstract descriptions.
3. Use different models or model configurations for the stages where they perform best, such as planning, concise editing, review, or summarization.
4. Separate planning from execution: request a diagnosis and 2–3 possible fixes before asking for a minimal code change and its tests.
5. Compose terminal output into AI input through shell pipelines, while accounting for command differences between Copilot CLI versions.
6. Prefer small, failure-driven loops over one-shot prompts to reduce hallucination and keep each step tied to actual repository state.
7. Verify every generated change with tests, linting, formatting, runtime checks, and manual inspection before accepting it.

## Overview

These notes cover how to use GitHub Copilot CLI as part of terminal-native, multi-step AI workflows for software engineering tasks. The core idea is to move beyond treating an LLM like a single chat interface and instead break work into stages such as context gathering, planning, code generation, review, summarization, and verification.

This matters because many engineering workflows already happen in the terminal: inspecting diffs, running tests, reading logs, and automating repetitive tasks. Using AI through the CLI makes those workflows easier to compose, script, repeat, and verify, while keeping humans in control of repository state and execution.

## Key Concepts

- **Copilot CLI**: GitHub Copilot CLI brings AI assistance directly into the terminal.
- **Multi-model workflow**: Different models or model configurations can be used for different stages of a task.
- **Prompt chaining**: Output from one AI step becomes input to the next step.
- **Terminal-native automation**: CLI access makes AI usable in shell scripts, pipelines, and development loops.
- **Context scoping**: Passing focused artifacts like diffs, stack traces, and test failures improves output quality.
- **Human-in-the-loop verification**: Tests, linters, code review, and runtime checks remain essential safeguards.

## How It Works

A useful mental model is to treat Copilot CLI as one component in a larger shell-based workflow. Instead of asking one broad prompt to solve everything, split the task into smaller stages:

1. Collect relevant context such as `git diff`, failing test output, logs, stack traces, or selected files.
2. Ask for analysis or a plan.
3. Ask for code generation, refactoring, or a specific transformation.
4. Ask for a second-pass review, summary, or edge-case check.
5. Verify the result locally with tests, linting, formatting, and manual inspection.

This staged approach improves reliability because each prompt has a narrow purpose. It also makes it easier to swap AI behavior per step. One model may be stronger at planning, another at concise edits, and another at review or summarization.

A strong pattern is failure-driven prompting: feed concrete artifacts like compiler errors or test failures into the model rather than describing the problem abstractly. This keeps the AI grounded in actual repository state. The shell remains the source of truth, and AI acts as a helper layered onto existing engineering controls.

Example shell composition pattern:

```bash
git diff -- src/auth.py | copilot explain
pytest -q 2>&1 | copilot suggest-fix
cat failing_test_output.txt | copilot summarize
```

Even if exact commands vary by CLI version, the pattern is stable: shell output becomes model input, and model output informs the next action.

Another useful practice is separating planning from execution. For example:

- First ask for a concise diagnosis and 2–3 possible fixes.
- Then ask for a minimal code change.
- Then ask for tests to validate the change.
- Finally ask for a summary suitable for a commit message.

This reduces hallucination, encourages small iterative loops, and makes verification explicit. A practical workflow mindset is:

- keep prompts specific
- pass concrete artifacts rather than vague descriptions
- separate ideation from generation
- verify every generated change
- prefer small loops over one-shot prompts

## Test Yourself

<details><summary>Why is a staged Copilot CLI workflow preferable to one broad prompt?</summary>

Each stage has a narrow purpose, making outputs easier to evaluate, revise, and verify. It also allows different models or configurations to handle planning, editing, review, and summarization.

</details>

<details><summary>What should be passed into a failure-driven prompt?</summary>

Pass concrete evidence from the repository or toolchain, such as a failing test, compiler error, stack trace, log, or relevant diff. This grounds the model in the current state rather than an abstract description.

</details>

<details><summary>What remains the source of truth when AI is used in a terminal workflow?</summary>

The repository state and local engineering controls remain authoritative. Tests, linters, formatters, runtime checks, code review, and human inspection must verify AI-generated suggestions and changes.

</details>

## Personal Notes

Building Multi-Model AI Workflows with GitHub Copilot CLI

Source: https://youtu.be/rJSsbHwkYAY?si=KWmq4S2HT9rkJAMY
Notion page: https://www.notion.so/Building-Multi-Model-AI-Workflows-with-GitHub-Copilot-CLI-35e01bb0839a81b585c2c68e3ecce143

Tags: github-copilot, cli, llm, ai-workflows, developer-tools

Overview

This lesson explains the idea of using GitHub Copilot from the command line to orchestrate multi-step, multi-model workflows for day-to-day engineering tasks. Instead of treating an LLM as a single chat box, the workflow mindset breaks work into stages such as planning, code generation, validation, summarization, and refinement, potentially using different models or prompts for each step.

This matters to engineers who want AI assistance embedded directly in terminal-based development. CLI-driven workflows are especially useful for automation, repeatability, shell composition, and integrating AI into existing tools like git, test runners, linters, and build pipelines.

Key Concepts

  *   Copilot CLI: GitHub Copilot CLI brings AI assistance into the terminal, where many engineering workflows already live. Instead of switching to an editor chat window, developers can invoke AI from shell commands, making it easier to compose with existing Unix-style tools.
  *   Multi-model workflow: A multi-model workflow uses more than one LLM or model configuration across a task. For example, one model may be better at planning, another at code transformation, and another at concise summarization or review.
  *   Prompt chaining: Prompt chaining means taking the output of one AI step and feeding it into the next. This allows complex tasks to be decomposed into smaller, more reliable stages such as analyze -> propose -> implement -> verify.
  *   Terminal-native automation: When AI is available in the CLI, it can participate in scripts, shell pipelines, and local development loops. That makes workflows reproducible and easier to standardize across a team compared with one-off interactive chat sessions.
  *   Context scoping: Effective CLI AI usage depends on passing the right context: files, git diffs, error messages, test output, or command history. Narrow, relevant context generally produces better results than dumping an entire codebase into a prompt.
  *   Human-in-the-loop verification: Even in automated AI workflows, engineers should validate outputs with tests, linters, code review, and runtime checks. The model can accelerate work, but the terminal environment should also make verification an explicit step.

How It Works

A practical way to think about multi-model AI workflows in GitHub Copilot CLI is as a pipeline of terminal tasks, not a single request. In a typical engineering loop, you already gather context, inspect files, edit code, run tests, and review diffs. Copilot CLI can be inserted into that loop so each AI interaction has a clear purpose.

A common structure looks like this:

1. **Collect context** - `git diff` - test failures - stack traces - selected source files - README or API docs

2. **Ask for analysis or a plan** - summarize the issue - identify likely root causes - propose an implementation strategy

3. **Use a model for generation or transformation** - write code - refactor functions - generate tests - produce shell commands

4. **Use another step for review or compression** - summarize changes - check for edge cases - propose safer alternatives

5. **Verify locally** - run unit tests - run linters/formatters - inspect git diff - execute the program

The “multi-model” part is conceptually important even if the CLI abstracts some model selection details. Different models often have different strengths: one may be better at broad reasoning and planning, while another is faster or better at deterministic code edits. In practice, this means choosing the right AI behavior for each stage rather than expecting one prompt to do everything well.

A terminal-native workflow also encourages composition. For example, you can feed structured context into Copilot CLI from shell commands:

```bash git diff -- src/auth.py | copilot explain pytest -q 2>&1 | copilot suggest-fix cat failing_test_output.txt | copilot summarize ```

The exact subcommands may vary by version, but the pattern stays the same: shell output becomes model input, and model output can guide the next command. This is especially useful for failure-driven development, where you want AI to react to concrete compiler or test output rather than vague natural-language descriptions.

Another useful pattern is separating planning from execution. First, ask for a short implementation plan based on the current repository state. Then, ask for a patch, file-by-file changes, or a specific function implementation. Finally, ask for tests and a review checklist. Breaking the work apart reduces hallucination and makes it easier to catch mistakes.

For example, an end-to-end bug-fix workflow might look like:

- Capture the failing test output. - Ask Copilot CLI to explain the failure in one paragraph. - Ask for 2-3 candidate fixes with tradeoffs. - Choose one fix and ask for a minimal patch. - Apply the change manually or with an editor. - Run tests again. - Ask Copilot CLI to summarize the final diff for a commit message.

This workflow matters because it aligns AI usage with established engineering controls. The model contributes analysis and acceleration, but the shell remains the source of truth for repository state, executable commands, and verification artifacts.

A good operational mindset is:

- keep prompts specific - pass concrete artifacts, not vague descriptions - separate ideation from code generation - verify every generated change - prefer small iterative loops over giant one-shot prompts

Training Exercise

Create a small terminal-based AI workflow for fixing a bug in a sample project.

### Goal Use a CLI-driven prompt chain to analyze a failure, propose a fix, generate code, and verify the result.

### Steps 1. **Create a tiny buggy program**

```bash mkdir copilot-cli-workflow-demo cd copilot-cli-workflow-demo cat > app.py <<'PY' def is_even(n): return n % 2 == 1 PY

cat > test_app.py <<'PY' from app import is_even

def test_even_number(): assert is_even(4) is True

def test_odd
