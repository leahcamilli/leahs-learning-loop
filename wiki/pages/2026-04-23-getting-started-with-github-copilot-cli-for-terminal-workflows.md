---
title: "Getting Started with GitHub Copilot CLI for Terminal Workflows"
source: "https://www.youtube.com/watch?v=fgHk28xljYw"
date: "2026-04-23"
tags: [github-copilot, cli, terminal, shell, developer-tools]
source_type: "youtube"
channel: "Dan Wahlin"
published: "2026-03-15"
duration_seconds: 1408
topics: [github-copilot, developer-tools]
kind: "tutorial"
depth: 2
actionability: 1
---

## TL;DR

> GitHub Copilot CLI can turn plain-language intent into shell commands and explain unfamiliar commands without leaving the terminal. Treat every suggestion as a draft: review its paths, scope, flags, assumptions, and platform compatibility before running it.

## Key Takeaways

1. Use “do mode” to translate a plain-language task into a candidate shell command or pipeline.
2. Use “explain mode” to understand a command’s flags, arguments, recursion, and pipeline behavior.
3. Review generated commands for incorrect paths, destructive operations, quoting problems, permissions, and unintended recursive scope.
4. Verify that required tools and syntax are compatible with the current shell and operating system.
5. Edit and refine suggestions directly in the terminal; Copilot CLI is most valuable as a fast first draft, not trusted automation.
6. Keep learning core shell concepts such as quoting, pipes, redirection, and command semantics because Copilot CLI does not replace shell knowledge.
7. Practice potentially risky commands in a safe workspace before applying them to repositories, files, or infrastructure that matter.

## Overview

These notes cover how GitHub Copilot CLI brings AI-assisted help directly into terminal workflows. The focus is on using natural language to generate shell commands, explain existing commands, and reduce context switching for engineers who spend much of their day in the command line.

This matters because terminal work often includes high-impact tasks such as Git operations, file manipulation, search, build tooling, and environment management. Copilot CLI can speed up command discovery and learning, but it must be used with careful review since generated commands may be risky, incorrect, or environment-specific.

## Key Concepts

- **Terminal-native AI assistance**: Copilot CLI is meant to work inside the shell rather than pulling you into a separate chat or IDE workflow. This helps reduce context switching during command-line tasks.
- **Prompt-to-command generation**: You can describe a task in plain English and receive a shell command or pipeline suggestion. This is useful for remembering syntax, flags, or command combinations.
- **Command explanation**: Copilot CLI can break down existing commands and explain flags, arguments, and pipeline behavior. This helps with learning and understanding unfamiliar shell usage.
- **Human-in-the-loop execution**: Generated commands should be treated as drafts, not trusted automation. The engineer is responsible for reviewing, editing, and deciding whether to run them.
- **Shell integration**: Good shell integration makes AI suggestions easier to insert, modify, and rerun within normal terminal workflows. The tool is most useful when it feels like an extension of the shell.
- **Safety and verification**: Terminal commands can delete files, change repositories, or affect infrastructure. Always verify paths, flags, assumptions, permissions, and platform compatibility before execution.

## How It Works

GitHub Copilot CLI acts as an interface between natural-language intent and shell-oriented output. You describe what you want to do, and it returns either a candidate command or an explanation of an existing one. The value is not full automation, but faster iteration and better in-context learning.

A typical workflow looks like this:

1. You express an intent in natural language.
   - Example: “Find all large files in this repo”
   - Example: “Explain this grep command”
   - Example: “Create a tar archive excluding node_modules”

2. Copilot CLI interprets the request.
   - For action-oriented prompts, it usually returns a shell command or short pipeline.
   - For explanation-oriented prompts, it describes the command structure, flags, and behavior.

3. You review the output before running anything.
   - Check whether paths are correct.
   - Confirm recursive behavior and scope.
   - Look for quoting issues, destructive actions, and platform-specific syntax.
   - Make sure required tools exist in the current environment.

4. You run, inspect, and refine.
   - If the suggestion is close but imperfect, edit it directly in the shell.
   - This is where Copilot CLI is most useful: it accelerates the first draft, while human judgment improves correctness and safety.

A helpful mental model is that Copilot CLI supports two primary modes:

- **Do mode**: turn intent into a command.
- **Explain mode**: turn a command back into human understanding.

This dual use makes it useful for both experienced and newer engineers. Experienced users gain speed on rarely used syntax and flags, while newer users gain contextual shell learning without leaving the terminal.

Common high-value use cases include:

- Git operations
- File and directory management
- Search and text processing
- Archive and compression tasks
- Environment inspection
- Build and test command recall

Example generated command:

```bash
# Natural language intent
"show me the 10 largest files under the current directory"

# Candidate output you might receive
find . -type f -exec du -h {} + | sort -hr | head -n 10
```

This should still be validated. Questions to ask include:

- Does `du` behave the same way on this platform?
- Is the current directory the intended scope?
- Will hidden folders, generated files, or mounted volumes affect the output?

For explanation mode, consider:

```bash
grep -Rin --exclude-dir=node_modules "TODO" .
```

A useful explanation would include:

- `grep` searches text
- `-R` searches recursively
- `-i` ignores case
- `-n` shows line numbers
- `--exclude-dir=node_modules` skips that directory
- `"TODO"` is the search pattern
- `.` means start searching in the current directory

The main practical takeaway is that Copilot CLI improves terminal productivity, but it does not replace shell knowledge. Understanding quoting, pipes, redirection, command semantics, and platform differences remains essential for safe and effective use.

The training exercise in these notes is especially useful because it encourages hands-on practice in a safe workspace. It reinforces a strong habit: use Copilot CLI to accelerate thinking and command discovery, but always validate output manually before execution.

## Test Yourself

<details><summary>What are Copilot CLI’s two primary modes?</summary>

“Do mode” converts natural-language intent into a candidate command. “Explain mode” translates an existing command into a description of its structure, flags, arguments, and behavior.

</details>

<details><summary>What should you verify before executing a generated command?</summary>

Check paths, scope, recursive behavior, quoting, destructive effects, permissions, required tools, and platform-specific syntax. The lesson recommends treating every generated command as a draft that requires human approval.

</details>

<details><summary>Why does Copilot CLI not eliminate the need for shell knowledge?</summary>

A plausible command may still be unsafe, incorrect, or incompatible with the current environment. Understanding shell fundamentals lets you evaluate and refine suggestions before they affect files, repositories, or infrastructure.

</details>

## Personal Notes

Getting Started with GitHub Copilot CLI for Terminal Workflows

Source: https://youtu.be/fgHk28xljYw?si=D4JI59L025adroyr
Notion page: https://www.notion.so/Getting-Started-with-GitHub-Copilot-CLI-for-Terminal-Workflows-34b01bb0839a817098f4c8493df17723

Tags: github-copilot, cli, terminal, developer-tools, shell

Overview

GitHub Copilot CLI brings AI-assisted help directly into the terminal, where many engineers already spend much of their day. Instead of switching to a browser or IDE for common tasks, you can ask for command suggestions, explanations, and shell-friendly guidance in place.

This matters for engineers who work heavily with shell commands, DevOps tasks, Git workflows, and local development environments. A practical understanding of Copilot CLI helps you move faster while still keeping control over what runs on your machine, which is especially important when using AI to generate commands that can modify files, processes, or infrastructure.

Key Concepts

  *   Terminal-native AI assistance: Copilot CLI is designed to fit directly into command-line workflows rather than pulling you into a separate chat interface. The main value is reducing context switching while giving you help with commands, syntax, and task execution.
  *   Prompt-to-command generation: A core feature is turning natural-language requests into shell commands. For example, you might describe a Git task or file-processing job and receive a candidate command that you can inspect before running.
  *   Command explanation: Copilot CLI can also help interpret existing commands, flags, and shell pipelines. This is useful when dealing with unfamiliar one-liners, inherited scripts, or commands copied from documentation.
  *   Human-in-the-loop execution: The tool suggests commands, but the engineer remains responsible for reviewing and executing them. This review step is critical because generated commands may be incorrect, environment-specific, or risky if run without validation.
  *   Shell integration: Copilot CLI typically integrates with common shells so that suggested commands can be inserted, edited, and rerun in a familiar workflow. Good shell integration makes the tool feel like an augmentation of the terminal instead of a separate application.
  *   Safety and verification: Because terminal commands can delete data, alter repositories, or affect infrastructure, safety practices are essential. Engineers should verify paths, flags, environment assumptions, and permissions before executing AI-generated output.

How It Works

GitHub Copilot CLI is best understood as an interface layer between a natural-language prompt and your shell workflow. You describe what you want to do in plain English, and the tool returns a suggested command or explanation tailored to terminal usage. The practical goal is not full automation but faster command discovery, learning, and iteration.

In a typical workflow, the mechanics look like this:

1. **You express an intent** in natural language. - Example: "Find all large files in this repo" - Example: "Explain this grep command" - Example: "Create a tar archive excluding node_modules"

2. **Copilot CLI interprets the request** and produces terminal-oriented output. - For task requests, this is usually a shell command or small pipeline. - For explanation requests, it breaks down what the command and flags do.

3. **You review the suggestion before execution.** This is the most important step. Terminal commands often have side effects, so generated output should be treated as a draft. You may need to adjust paths, flags, quoting, platform-specific syntax, or assumptions about available tools.

4. **You run, inspect, and refine.** If the command is close but not quite right, you edit it directly in the shell. This makes Copilot CLI particularly useful for iterative work, where the first command gets you near the solution and terminal expertise closes the gap.

A useful mental model is that Copilot CLI supports two high-value terminal tasks:

- **"Do" mode**: generate a command from an intent. - **"Explain" mode**: translate a command back into human understanding.

That combination is powerful for both experienced and newer engineers. Experienced users benefit from speed on rarely used commands and flags, while newer users get a way to learn shell semantics in context.

In practice, the kinds of tasks where Copilot CLI is most helpful include:

- Git operations - File and directory manipulation - Search and text processing - Archive and compression tasks - Environment inspection - Build and test command recall

Example interaction pattern:

```bash # Natural language intent "show me the 10 largest files under the current directory"

# Candidate output you might receive find . -type f -exec du -h {} + | sort -hr | head -n 10 ```

You should then validate:

- Does `du
