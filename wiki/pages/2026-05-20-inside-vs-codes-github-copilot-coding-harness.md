---
title: "Inside VS Code’s GitHub Copilot Coding Harness"
source: "https://code.visualstudio.com/blogs/2026/05/15/agent-harnesses-github-copilot-vscode"
date: "2026-05-20"
tags: [vscode, github-copilot, agentic-ai, tool-calling, evaluation]
source_type: "web"
topics: [ai-agents, coding-agents, github-copilot, context-engineering]
kind: "deep-dive"
depth: 3
actionability: 2
---

## TL;DR

> A coding agent’s quality depends on its harness—not just its model—because the harness assembles context, exposes and executes tools, controls iterative work, and adapts behavior by model. Evaluating that full system against realistic editor workflows is essential for making reliable improvements.

## Key Takeaways

1. Treat context assembly, tool selection, execution, and loop control as core product behavior rather than a thin wrapper around the model.
2. Rebuild the prompt after every tool call so the model receives updated workspace state, conversation history, tool results, custom instructions, and memory.
3. Distinguish a user-visible turn from a round of model-and-tool activity and from the complete run containing all rounds for that turn.
4. Bound agent runs with tool-call limits, cancellation checks, stop hooks, and conversation summarization to control cost, latency, and context usage.
5. Tune prompts and tools by model: the article says Claude uses `replace_string_in_file`, GPT uses `apply_patch`, and Gemini needs stronger instructions to invoke tools explicitly.
6. Validate harness changes on realistic product workflows; the VS Code team says VSC-Bench measures correctness, resolution rate, token efficiency, latency, and agent effort in reproducible workspaces.

## Overview

This lesson explains the coding harness that powers GitHub Copilot’s agent experience in Visual Studio Code. The article’s main point is that model quality alone does not determine developer experience: the harness is the layer that assembles context, exposes tools, executes tool calls, manages the agent loop, and adapts behavior across different model providers.

This matters to engineers building AI-powered developer tools, IDE integrations, or multi-model agent systems. It is especially relevant if you care about practical concerns like prompt construction, tool schemas, loop control, model-specific behavior, and how to evaluate agent changes in a way that reflects real product workflows rather than only benchmark scores.

## Key Concepts

- **Coding harness**: A coding harness is the orchestration layer between a language model and the editor environment. Since models only emit text, the harness is responsible for turning tool requests into real actions like reading files, editing code, running commands, and feeding results back into the next model iteration.
- **Context assembly**: Before each model call, the harness constructs the prompt from multiple sources: system instructions, user input, workspace structure, conversation history, prior tool results, custom instructions, and memory. The quality of this assembled context strongly affects agent behavior because it determines what information and constraints the model sees.
- **Tool exposure and schemas**: The harness decides which tools are available for a given request and defines them with structured JSON schemas. This is critical because tool availability can vary by model, user settings, extension-provided capabilities, MCP servers, or custom agents, and the schema determines whether the model can invoke tools reliably.
- **Agent loop**: The core runtime is a repeated think-act-observe cycle. On each round, the harness rebuilds the prompt, calls the model, executes any requested tools, records results, and decides whether to continue until a final assistant response is produced.
- **Model-specific harness tuning**: Different models require different prompts, tool choices, and conversation handling. The article highlights examples such as Claude preferring one file-editing tool, GPT preferring another, and Gemini needing stronger guidance toward explicit tool usage, which means a multi-model product cannot use a one-size-fits-all harness.
- **Conversation summarization and loop control**: Long-running agent sessions can exceed context limits, so the harness summarizes older rounds to preserve useful state while staying within token budgets. It also enforces tool-call limits, checks cancellation, and runs stop hooks that can decide whether the agent should finish or keep working.
- **Product-specific evaluation**: Public benchmarks are useful but insufficient for measuring real editor-based workflows. VS Code addresses this with VSC-Bench, an evaluation suite focused on realistic agent behavior inside VS Code, including extension workflows, browser and terminal interaction, multi-turn tasks, and efficiency metrics like latency and token usage.

## How It Works

The article frames the coding harness as the part of the system developers actually experience, even though most public discussion focuses on the underlying model. In practice, the harness performs three primary functions:

1. **Assemble context** for the next model call.
2. **Expose tools** the model is allowed to use.
3. **Execute tools** and feed observations back into the loop.

A simplified flow looks like this:

```text
user request
  -> harness builds prompt
  -> model response
  -> if tool calls: validate + execute tools
  -> collect outputs
  -> rebuild prompt with updated state
  -> repeat
  -> final assistant response
```

The first major responsibility is **context assembly**. The harness does not simply forward the user’s message to the model. It constructs a richer prompt that can include behavioral instructions, the user query, workspace structure such as languages and frameworks, open files, prior conversation turns, previous tool outputs, custom instructions, and memory from earlier sessions. Because this prompt is rebuilt on every round, the model sees an updated view of the workspace after every edit or command execution.

The second responsibility is **tool exposure**. The harness defines what actions are possible in the current run, such as:

- `read_file`
- `replace_string_in_file`
- `apply_patch`
- `run_in_terminal`
- `semantic_search`

Each tool is described with a schema and natural-language guidance so the model knows when and how to use it. Importantly, the available toolset is dynamic. Some tools may only be enabled for certain models, some may require user confirmation, and others can be contributed by extensions, MCP servers, or custom `.agent.md` configurations. This means the harness is not just a runtime wrapper; it is also a policy layer controlling agent capability.

The third responsibility is **tool execution**. When the model emits a structured call such as:

```json
{"name":"run_in_terminal","arguments":{"command":"npm test"}}
```

the harness validates the request, executes the command, captures output, handles failures, and passes the result back into the next model round. The same pattern applies to file reads, code edits, and searches. Without this layer, the model would only be narrating intended actions rather than actually performing them.

The article distinguishes between a **turn**, a **round**, and a **run**:

- A **turn** is a user-visible chat exchange.
- A **round** is one cycle of prompt build -> model call -> tool execution -> state update.
- A **run** is the full sequence of rounds that happen during a turn.

This distinction matters because one user request can trigger many hidden iterations. For example, an agent may search for files, inspect implementation details, edit code, run tests, parse failures, apply another patch, and only then produce a final answer.

To keep this process safe and bounded, the harness implements **loop-control mechanisms**. These include maximum tool-call limits, cancellation checks between rounds, and stop hooks that can inspect state and decide whether the current result is sufficient or whether the agent should continue. This is a practical engineering requirement: without loop controls, agentic systems can become slow, costly, or stuck in unproductive cycles.

Another important mechanism is **conversation summarization**. As the run grows, including every prior prompt, response, and tool result may exceed the model’s context window. The harness compresses older history into summaries so the agent can preserve relevant state without carrying the full raw transcript. This is especially important for long multi-turn coding sessions.

A major theme in the article is that the harness must be **model-aware**. VS Code supports multiple providers and model families, and they do not behave identically. Some differ in tool-calling APIs, context windows, structured output fidelity, error patterns, or prompt sensitivity. The article gives concrete examples:

- Claude models use `replace_string_in_file` for edits.
- GPT models use `apply_patch`.
- Gemini needs stronger reminders to call tools instead of merely describing them.
- Some models need concise prompts; others benefit from verbose, structured prompts.
- Some support extended reasoning modes and need effort controls.

This means integrating a new model is not just adding it to a dropdown. The harness may need per-model system prompts, different tool sets, special conversation handling, and validation of tool schemas and defaults before release.

The final third of the article focuses on **evaluation**. Public benchmarks like SWE-bench and Terminal-Bench are useful, but the authors argue they do not fully represent the work developers ask agents to do in an editor. Real tasks include scaffolding, migration, refactoring, extension interaction, browser and terminal use, and multi-language workflows. To measure these, VS Code built **VSC-Bench**, an offline benchmark suite using reproducible containerized workspaces. The harness launches VS Code, opens a workspace, submits prompts, lets the full agent loop run, and then scores outcomes across dimensions such as:

- solution correctness
- resolution rate
- token efficiency
- latency
- agent effort

This evaluation is used not only for selecting and tuning models, but also for validating harness changes. For pull requests that could change agent behavior, the VS Code team can trigger an automated eval flow with a `~requires-eval-assessment` label. That flow builds the PR, publishes a versioned eval agent, opens an evaluation issue in internal benchmarking infrastructure, runs the benchmark, and reports links back to the original PR. The key takeaway is that harness changes are treated like product changes: they are benchmarked before merging, not assumed to be safe.

Overall, the article argues that for coding agents, the model is necessary but insufficient. The real product experience emerges from the harness: how context is assembled, which tools are available, how the loop is managed, how model-specific quirks are handled, and whether all of that is continuously validated against realistic developer tasks.

## Training Exercise

Build a minimal local simulation of a coding harness to understand the think-act-observe loop.

### Goal
Create a small script that:
1. Accepts a user task.
2. Exposes a tiny set of tools.
3. Simulates one or more tool-calling rounds.
4. Logs the evolving prompt state after each round.

### Step 1: Define a tiny workspace and tools
Create a directory with a sample file:

```bash
mkdir mini-harness && cd mini-harness
printf 'def add(a, b):\n    return a-b\n' > math_utils.py
```

Implement two tools in Python:
- `read_file(path)`
- `replace_string_in_file(path, old, new)`

### Step 2: Write a harness script
Create `harness.py`:

```python
import json
from pathlib import Path

history = []


def read_file(path):
    return Path(path).read_text()


def replace_string_in_file(path, old, new):
    p = Path(path)
    text = p.read_text()
    updated = text.replace(old, new)
    p.write_text(updated)
    return {"status": "ok", "path": path}


def build_prompt(user_request, tool_results):
    return {
        "system": "You are a coding agent. Use tools when needed.",
        "user": user_request,
        "history": history,
        "tool_results": tool_results,
    }


def fake_model(prompt):
    if not prompt["tool_results"]:
        return {
            "tool_call": {
                "name": "read_file",
                "arguments": {"path": "math_utils.py"}
            }
        }

    last = prompt["tool_results"][-1]
    if "return a-b" in str(last):
        return {
            "tool_call": {
                "name": "replace_string_in_file",
                "arguments": {
                    "path": "math_utils.py",
                    "old": "return a-b",
                    "new": "return a+b"
                }
            }
        }

    return {"final": "Fixed the bug in math_utils.py"}


def run(user_request):
    tool_results = []
    for round_num in range(5):
        prompt = build_prompt(user_request, tool_results)
        print(f"\n=== ROUND {round_num + 1} ===")
        print(json.dumps(prompt, indent=2))
        response = fake_model(prompt)

        if "final" in response:
            history.append({"user": user_request, "assistant": response["final"]})
            print("FINAL:", response["final"])
            return

        call = response["tool_call"]
        if call["name"] == "read_file":
            result = read_file(**call["arguments"])
        elif call["name"] == "replace_string_in_file":
            result = replace_string_in_file(**call["arguments"])
        else:
            result = {"error": "unknown tool"}

        tool_results.append(result)

run("Fix the add function")
```

### Step 3: Run it

```bash
python harness.py
cat math_utils.py
```

Observe how the script rebuilds prompt state every round and how tool outputs feed the next decision.

### Step 4: Extend the exercise
Add one or more of these features:
- A `run_tests` tool that executes `python -m pytest`.
- A tool-call limit to stop infinite loops.
- A summarization step that replaces old tool results with a short summary string after 3 rounds.
- Per-model behavior flags, for example one fake model using `replace_string_in_file` and another using an `apply_patch`-style tool.

### Step 5: Reflect
After implementing the extension, answer these questions:
1. What data must be preserved between rounds for the agent to behave coherently?
2. Which part of your harness is policy, and which part is pure execution?
3. How would you benchmark whether a prompt or tool-schema change actually improved outcomes?

This exercise mirrors the article’s central lesson: reliable coding agents are built from orchestration, tooling, and evaluation, not just a strong base model.

## Test Yourself

<details><summary>What three primary responsibilities does a coding harness perform?</summary>

It assembles context for each model call, exposes the tools permitted for the task, and executes requested tools before returning their results to the model.

</details>

<details><summary>Why does a multi-model coding product need model-specific harness behavior?</summary>

The article says model families differ in tool-calling APIs, prompt sensitivity, context limits, structured-output reliability, and preferred editing tools. A single prompt and tool configuration therefore may not work equally well across providers.

</details>

<details><summary>Why are public coding benchmarks insufficient for evaluating harness changes?</summary>

The authors argue that they do not fully represent editor workflows such as scaffolding, migrations, extension interaction, browser and terminal use, and multi-turn tasks. Product-specific evaluations can test those workflows while also measuring latency, token usage, and agent effort.

</details>

## Further Reading

- [Visual Studio Code Source Repository](https://github.com/microsoft/vscode)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [SWE-bench](https://www.swebench.com/)
- [OpenAI Function Calling and Structured Tool Use](https://platform.openai.com/docs/guides/function-calling)
- [Anthropic Tool Use Documentation](https://docs.anthropic.com/)
