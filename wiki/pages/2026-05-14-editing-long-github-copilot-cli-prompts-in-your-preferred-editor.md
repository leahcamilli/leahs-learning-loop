---
title: "Editing Long GitHub Copilot CLI Prompts in Your Preferred Editor"
source: "https://linkedin.com/posts/burkeholland_editing-prompts-in-terminals-is-the-ick-ugcPost-7460480525078654976-4WvP?rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY"
date: "2026-05-14"
tags: [copilot, cli, terminal, editor, shell]
source_type: "web"
topics: [developer-tools, github-copilot]
kind: "tutorial"
depth: 2
actionability: 3
---

## TL;DR

> Press `Ctrl+G` in GitHub Copilot CLI to edit a long prompt in the editor configured by `EDITOR`, then save and close to return the revised text to the terminal. This makes complex, multiline prompts easier to structure and refine.

## Key Takeaways

1. Press `Ctrl+G` to open the current GitHub Copilot CLI prompt in the configured external editor.
2. Set `EDITOR="code --wait"` for VS Code; `--wait` keeps the CLI paused until editing is complete.
3. Set `EDITOR="nano"` for a lightweight terminal editor that blocks automatically until you exit.
4. Use `export EDITOR="…"` in bash or zsh, and `$env:EDITOR = "…"` in PowerShell.
5. Put the editor setting in the appropriate shell startup file or PowerShell profile to persist it across sessions.
6. Saving and closing the editor returns the modified temporary text buffer to Copilot CLI.
7. The same `EDITOR` concept improves workflows in other command-line tools, including Git commit editing and `crontab -e`.

## Overview
These notes capture a practical workflow improvement for GitHub Copilot CLI: editing long prompts in a real text editor instead of fighting with a cramped terminal input. The key idea is that Copilot CLI can open the current prompt in your configured editor, making it much easier to write, restructure, and refine multi-line requests.

This matters because CLI-based AI workflows are becoming common, and prompt quality often depends on being able to iterate comfortably. Understanding how the `EDITOR` environment variable works—and why some editors need blocking behavior like `--wait`—helps make terminal AI tools significantly more usable across bash, zsh, and PowerShell environments.

## Key Concepts
- **External editor workflow**: Many CLI tools support handing text entry off to a full editor instead of requiring inline terminal editing. This is especially useful for long prompts that need multiline structure, revision, and cleanup.
- **GitHub Copilot CLI prompt editing**: The notes describe using `Ctrl+G` to open the current Copilot CLI prompt in the configured editor. After editing, saving, and closing, the updated prompt returns to the terminal session.
- **`EDITOR` environment variable**: CLI tools commonly use `EDITOR`—and sometimes `VISUAL`—to determine which editor to launch. Setting this correctly defines the default editing experience across compatible command-line tools.
- **Editor wait semantics**: GUI editors may return control immediately unless told to block. For VS Code, `code --wait` is necessary so the CLI pauses until editing is complete.
- **Shell-specific setup**: Bash, zsh, and PowerShell all support editor configuration, but each uses different syntax and startup files. Persistent setup is usually done in shell config files or PowerShell profiles.
- **Editor choice tradeoffs**: VS Code offers a rich GUI experience, while tools like Nano are lightweight and terminal-native. The best choice depends on environment, speed, and whether a desktop session is available.

## How It Works
The workflow is straightforward: instead of composing a long Copilot CLI prompt directly in the terminal, you trigger an edit action, make changes in a full editor, then return to the CLI with the revised prompt loaded. This improves navigation, formatting, and overall prompt clarity.

GitHub Copilot CLI reportedly supports this through `Ctrl+G`:

1. Start or prepare a prompt in the terminal.
2. Press `Ctrl+G`.
3. Copilot CLI opens the prompt in the editor specified by `EDITOR`.
4. Edit the prompt normally.
5. Save and close the editor.
6. Copilot CLI resumes with the updated prompt content.

This works by delegating prompt editing to an external process. The shell provides the editor command, and the CLI waits for that process to finish before reading back the modified content.

Example configurations:

```bash
export EDITOR="code --wait"
```

Use this when you want Visual Studio Code. The `--wait` flag is critical because otherwise Code launches and immediately returns, causing the CLI to continue before editing is finished.

```bash
export EDITOR="nano"
```

Nano is simpler because it blocks by default until you exit, which matches the expectation most CLI tools have for editor-based workflows.

In PowerShell:

```powershell
$env:EDITOR = "code --wait"
```

For persistence, place the setting in your PowerShell profile rather than only setting it in the current session.

A useful mental model:

- Copilot CLI manages the prompt lifecycle.
- Your shell determines which editor gets launched.
- The editor modifies a temporary text buffer.
- Saving and closing hands control—and the final text—back to the CLI.

This pattern also appears in other tools like Git commit editing and `crontab -e`, so learning it improves general command-line ergonomics beyond Copilot CLI.

## Test Yourself

<details><summary>How do you edit a long GitHub Copilot CLI prompt in an external editor?</summary>

Press `Ctrl+G`, edit the prompt in the editor selected by `EDITOR`, then save and close the editor. Copilot CLI resumes with the revised prompt content.

</details>

<details><summary>Why should VS Code be configured as `code --wait` rather than just `code`?</summary>

Without `--wait`, VS Code may return control immediately after opening, causing the CLI to continue before editing is finished. The flag makes the editor process block until the file is closed.

</details>

<details><summary>How do you make the editor choice persist across terminal sessions?</summary>

Add the `EDITOR` assignment to the relevant bash or zsh startup file, or to the PowerShell profile. A setting entered only in the current session is temporary.

</details>

## Personal Notes
Editing Long GitHub Copilot CLI Prompts with Your Preferred Editor

Source: https://www.linkedin.com/posts/burkeholland_editing-prompts-in-terminals-is-the-ick-ugcPost-7460480525078654976-4WvP?utm_source=social_share_send&utm_medium=ios_app&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY&utm_campaign=share_via
Notion page: https://www.notion.so/Editing-Long-GitHub-Copilot-CLI-Prompts-with-Your-Preferred-Editor-36001bb0839a81fbb1d9e64e4ad9308f

Tags: copilot, cli, terminal, editor, shell

Overview

This lesson explains a small but high-leverage terminal workflow improvement: editing long GitHub Copilot CLI prompts in a real text editor instead of struggling inside a one-line terminal input. The source highlights that Copilot CLI supports opening the current prompt in your configured editor with a keyboard shortcut, making prompt authoring much easier for complex requests.

This matters to engineers who increasingly use AI tools from the command line and need to write, revise, and debug multi-line prompts efficiently. If you work in bash, PowerShell, or similar shells, understanding how the `EDITOR` environment variable and editor wait behavior work will make your CLI-based AI workflow much more usable.

Key Concepts

  *   External editor workflow: Many CLI tools can hand off text entry to an external editor instead of forcing you to type directly in the terminal. This is especially useful for long prompts, where navigation, correction, and restructuring are awkward in a compact prompt box.
  *   GitHub Copilot CLI prompt editing: According to the source, GitHub Copilot CLI lets you press `Ctrl+G` to open the current prompt in your configured editor. After you edit, save, and close the editor, the updated prompt is brought back into the terminal session.
  *   EDITOR environment variable: CLI tools commonly discover which editor to launch from environment variables such as `EDITOR` or sometimes `VISUAL`. Setting this variable tells the tool what program to invoke when it needs a full-screen editing experience.
  *   Editor wait semantics: GUI editors often return control immediately unless explicitly told to block until the file is closed. For Visual Studio Code, the `--wait` flag is required so the CLI tool pauses while you edit and only resumes when the editor window or file session is closed.
  *   Shell-specific configuration: The way you set editor-related environment variables depends on your shell and operating system. Bash and PowerShell use different syntax and different startup files, but both support persistent configuration for default editor behavior.
  *   Choosing the right editor: The source mentions Visual Studio Code and Nano, and a comment also suggests Microsoft Edit as another option. The best choice depends on whether you prefer a graphical editor, a terminal-native editor, or a lightweight default tool available across environments.

How It Works

At a high level, the workflow is simple: instead of editing a long Copilot CLI prompt inline in the terminal, you trigger an edit action that opens the prompt content in a proper text editor. You then use normal editing capabilities—cursor movement, search, multiline formatting, deletion, and revision—save the file, close the editor, and return to the CLI with the modified prompt loaded.

The source specifically describes this interaction for GitHub Copilot CLI:

1. Start writing or preparing a prompt in the terminal. 2. Press `Ctrl+G`. 3. Copilot CLI opens the prompt in your configured editor. 4. Edit the text using your preferred tool. 5. Save and close the editor. 6. The terminal prompt updates to reflect your edited content.

This works because the CLI delegates editing to an external process. In most Unix-style and cross-platform CLI ecosystems, that process is determined by the `EDITOR` environment variable. When Copilot CLI needs a richer editing experience, it launches whatever command `EDITOR` points to.

For example, if you want to use Visual Studio Code, your editor command must include the `--wait` flag:

```bash export EDITOR="code --wait" ```

Without `--wait`, Code launches and immediately returns control to the terminal process. From the CLI tool's perspective, editing is already "done," even though you're still typing in the GUI window. That breaks the handoff model because the tool resumes before you've saved final changes.

For a terminal-native editor like Nano, configuration is simpler:

```bash export EDITOR="nano" ```

Nano blocks by default until you exit, which aligns naturally with how CLI tools expect editors to behave. This makes it a good fallback option on remote machines, containers, or environments without a desktop session.

In PowerShell, the same idea applies, but the syntax differs:

```powershell $env:EDITOR = "code --wait" ```

To make the setting persistent, you'd typically add it to your PowerShell profile instead of setting it only for the current session.

A practical mental model is:

- **Copilot CLI owns the prompt lifecycle**. - **Your shell provides the editor configuration**. - **The editor modifies a temporary prompt buffer**. - **Saving and closing hands the final text back to the CLI**.

This pattern is not unique to Copilot CLI. It is a common design in command-line tools such as Git commit message editors, crontab editors, and interactive CLI applications that need richer text entry. Learning it once improves your ergonomics across many tools.

From an engineering workflow standpoint, the main benefit is reduced friction for iterative prompting. Long prompts often include:

- multi-part instructions - code snippets - file paths - formatting constraints - error details - follow-up clarifications

Trying to maintain these inline in a small terminal input increases mistakes and discourages refinement.
