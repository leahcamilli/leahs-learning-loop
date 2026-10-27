---
title: "Rubber Duck Debugging with VS Code and GitHub Copilot CLI"
source: "https://www.linkedin.com/posts/in-todays-video-were-showing-how-to-share-7468674363865862144-Emxc/?utm_source=social_share_send&utm_medium=ios_app&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY&utm_campaign=share_via"
date: "2026-06-05"
tags: [debugging, vscode, github-copilot, cli, developer-workflow]
source_type: "web"
topics: [developer-tools, github-copilot]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> Explain code step by step and compare your intent with what the implementation actually does; the mismatch often reveals the bug. VS Code supports inspection and testing, while GitHub Copilot CLI can restate logic and challenge assumptions without replacing your reasoning.

## Key Takeaways

1. Narrate every function, branch, loop, variable change, and return value; uncertainty or contradiction marks the next place to investigate.
2. Compare three things during debugging: intended behavior, code as written, and observed runtime behavior.
3. Use VS Code to trace execution, navigate symbols, inspect related files, reproduce failures, and run focused tests.
4. Use GitHub Copilot CLI as a reasoning mirror by requesting explanations, decompositions, assumptions, and edge cases rather than blindly accepting fixes.
5. For shell commands and scripts, explicitly validate flags, shell expansion, environment assumptions, pipeline inputs, transformations, and outputs.
6. In the example `is_even_sum`, the loop adds `1` per item instead of `n`, so it checks whether the list length is even rather than whether the numeric sum is even.
7. In the training exercise, `len(values) - 1` is the wrong denominator for an average; use `len(values)` and define safe behavior for an empty list.

## Overview

Rubber duck debugging is the practice of explaining your code, line by line, as if you were teaching it to an inanimate listener. The act of verbalizing assumptions, control flow, and expected outcomes often reveals bugs, missing edge cases, and unclear design decisions before you ever run a debugger. The source highlights using this technique inside Visual Studio Code and with GitHub Copilot CLI to make the process faster and more interactive.

This matters to engineers who spend time diagnosing logic errors, unclear intent, or mismatches between what code does and what they think it does. Combining classic rubber duck debugging with modern editor and CLI tooling can turn a vague debugging session into a structured explanation workflow: inspect code, describe it, ask for restatement, and compare expected behavior against actual behavior.

## Key Concepts

- **Rubber duck debugging**: This is a debugging technique where you explain code in simple, explicit terms to an imaginary listener. By forcing yourself to state each assumption and transition, you often notice contradictions, skipped conditions, or incorrect mental models.
- **Externalizing reasoning**: Many bugs persist because the programmer keeps reasoning implicitly. Saying the logic out loud or writing it down makes hidden assumptions visible and gives you a chance to validate each step against the code.
- **VS Code as a debugging workspace**: VS Code provides a convenient environment for reading code, navigating symbols, opening related files, and running integrated terminal commands. That makes it a natural place to inspect implementation details while narrating logic and testing hypotheses.
- **GitHub Copilot CLI as an explanation assistant**: GitHub Copilot CLI can help restate commands, summarize code behavior, or generate explanations you can compare with your own understanding. Used well, it acts less like an oracle and more like a mirror for your reasoning process.
- **Expected vs actual behavior**: A productive debugging session clearly separates what the code should do from what it currently does. Rubber duck debugging is especially effective when you narrate inputs, execution path, and outputs, then identify where reality diverges from expectation.
- **Prompting for clarification instead of answers**: When using AI tools during debugging, the most valuable prompts often ask for explanation, decomposition, or edge-case analysis rather than direct fixes. This preserves your understanding and helps you find the root cause instead of blindly applying changes.

## How It Works

At its core, rubber duck debugging works by slowing your thinking down enough that logic errors become visible. Instead of scanning code and thinking, "this should work," you narrate what each function, branch, loop, and variable is supposed to do. The moment you cannot clearly explain a line, or your explanation does not match the implementation, you have likely found the area worth investigating.

In a VS Code workflow, this usually starts with opening the relevant file and tracing execution through the editor:

- identify the entry point for the failing behavior
- follow function calls using symbol navigation or peek definition
- inspect variable names, conditionals, and return values
- compare comments, function names, and actual implementation
- run or reproduce the issue from the integrated terminal

The source mentions GitHub Copilot CLI, which can add structure to this process. Rather than asking it to "fix the bug," you can use it to support explanation-first debugging. Typical uses include:

- asking for a plain-English summary of a function
- having it describe possible edge cases in a code path
- asking what assumptions a shell command or script is making
- comparing your stated intent with the current implementation

A practical loop looks like this:

1. Reproduce the problem in VS Code.
2. Open the smallest function or script responsible.
3. Explain the code out loud, line by line.
4. Note any point where your explanation becomes uncertain.
5. Use Copilot CLI to summarize that section or identify likely edge cases.
6. Re-run the program or test with a specific input.
7. Confirm whether the explanation and actual behavior now match.

For command-line or script debugging, Copilot CLI is especially useful because many failures come from misunderstood flags, shell expansion, environment assumptions, or pipeline behavior. You can ask for a command explanation, then verbally validate each piece: what input it expects, what it transforms, and what output it should produce.

Here is an example of explanation-first debugging on a small bug:

```python
def is_even_sum(nums):
    total = 0
    for n in nums:
        total += 1
    return total % 2 == 0
```

If you explain this out loud, you might say: "This function computes the sum of the numbers in `nums`, then returns whether that sum is even." But while narrating the loop, you notice it adds `1` for each element instead of adding `n`. The spoken explanation exposes the mismatch between intent and implementation.

You could then use an assistant prompt like:

```bash
copilot explain "What does this Python function actually compute, and how does that differ from checking whether the sum of nums is even?"
```

The key is that the tool reinforces your analysis rather than replacing it. The debugging value comes from comparing three things: your intent, the code as written, and the runtime behavior. VS Code helps you inspect and run; Copilot CLI helps you restate and challenge assumptions.

This approach scales from tiny functions to larger systems. In a multi-file bug, explain the data flow across boundaries: input parsing, transformation, storage, and output. If your explanation breaks at an interface boundary, that often points to the bug: wrong field shape, incorrect default, stale state, or unhandled null case. Rubber duck debugging is simple, but it works because most software bugs are really reasoning bugs made visible through careful explanation.

## Training Exercise

Use rubber duck debugging to diagnose and fix a small bug with VS Code and, if available, GitHub Copilot CLI.

1. Create a file named `buggy.py` with this code:

```python
def average(values):
    total = 0
    for v in values:
        total += v
    return total / (len(values) - 1)

print(average([10, 20, 30]))
```

2. Open the file in VS Code.
3. Before running it, explain the code out loud:
   - what input `average` expects
   - how `total` changes in the loop
   - what denominator should represent
   - what output you expect for `[10, 20, 30]`
4. Run the script in the VS Code terminal:

```bash
python buggy.py
```

5. Compare the actual output with your expected result.
6. Identify the exact line where the implementation differs from your explanation.
7. If you have GitHub Copilot CLI, ask for an explanation instead of a fix, for example:

```bash
copilot explain "Explain what this average function does step by step and identify any logic error in the denominator."
```

8. Fix the code.
9. Re-run the script and verify the result.
10. Extend the function to handle an empty list safely, then explain your updated logic out loud again.

Expected learning outcomes:

- you practice translating code into plain language
- you learn to isolate mismatches between intent and implementation
- you use AI tooling to clarify reasoning, not shortcut it
- you build a repeatable debugging workflow for both code and shell commands

## Test Yourself

<details><summary>What three things should you compare in an explanation-first debugging session?</summary>

Compare your intended behavior, the code as written, and the observed runtime behavior. The point where they diverge identifies the likely source of the bug.

</details>

<details><summary>Why should you ask GitHub Copilot CLI for explanations or edge cases instead of immediately asking for a fix?</summary>

Explanation-first prompts make assumptions and control flow visible while preserving your understanding of the code. The lesson presents the tool as a mirror for reasoning, not an oracle whose changes should be accepted blindly.

</details>

<details><summary>What is wrong with the training exercise&#x27;s `average` function, and what additional case must be handled?</summary>

It divides the total by `len(values) - 1`, although the denominator should be the number of values, `len(values)`. It must also handle an empty list safely to avoid division by zero.

</details>

## Further Reading

- [Visual Studio Code Documentation](https://code.visualstudio.com/docs)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Debugging in Visual Studio Code](https://code.visualstudio.com/docs/editor/debugging)
- [The Pragmatic Programmer: Rubber Ducking](https://pragprog.com/)
