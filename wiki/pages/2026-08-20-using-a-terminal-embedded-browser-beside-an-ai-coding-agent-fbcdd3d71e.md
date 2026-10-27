---
title: "Using a Terminal-Embedded Browser Beside an AI Coding Agent"
source: "https://lnkd.in/p/gsN67nwu"
date: "2026-08-20"
tags: [developer-workflow, terminal-tools, browser-automation, ai-coding]
source_type: "web"
source_fingerprint: "fbcdd3d71e"
source_characters: 5189
topics: [developer-tools, coding-agents, github-copilot, productivity]
kind: "demo"
depth: 2
actionability: 3
---

## TL;DR

> Keep an AI coding agent and a live browser preview side by side in one terminal to shorten the prompt–edit–verify loop and reduce context switching. Dan Wahlin’s demo suggests this is especially useful on a single screen, though normal refresh and cache troubleshooting may still be needed.

## Key Takeaways

1. Pair GitHub Copilot CLI with a terminal-embedded browser so code changes and visual results remain visible in one terminal session.
2. Use the observed `!` execute-style mode and `terminal browser` command as demo-specific examples, not guaranteed product behavior.
3. Start the local app with automatic change detection or hot reload to make visual iteration fast enough to be useful.
4. Follow a tight loop for UI work: prompt the agent, change the code, inspect the preview, adjust the prompt, and verify again.
5. Keep refresh and cache-busting techniques available; Dan’s gradient change appeared stale until a cache buster was used.
6. Use the side-by-side terminal layout to preserve agent-plus-preview visibility when working on a single screen.

## Overview

This lesson captures an observed workflow from Dan Wahlin’s demo: a terminal-based browser is opened alongside GitHub Copilot CLI so coding, prompting, and visual verification happen in one terminal window. The source shows a practical benefit rather than a formal specification: less context switching while iterating on a local web app. Evidence is limited to a narrated demo, so treat details such as commands, caching behavior, and browser capabilities as observed examples rather than guaranteed product behavior.

## Key Concepts

- **Context switching cost**: The main problem being solved is jumping between editor, terminal, and browser. The demo’s value proposition is keeping the agent and the live site visible side by side in one terminal session.
- **Terminal-embedded browser**: The source describes launching a browser from the shell with `terminal browser`. Dan characterizes it as effectively running a browser inside the terminal interface, likely as a wrapper rather than a conventional standalone browser window.
- **Agent-plus-preview workflow**: The workflow pairs GitHub Copilot CLI for code changes with an adjacent browser view for immediate feedback. This creates a tight loop: prompt, change code, refresh or auto-reload, inspect result.
- **Live reload verification**: A practical part of the demo is enabling automatic detection of changes, described as hot reload. This matters because the browser pane becomes useful only if it reflects code edits quickly enough to support iteration.
- **Single-screen ergonomics**: The speaker contrasts multi-monitor setups with working on one screen. The terminal-browser approach is presented as a way to preserve side-by-side visibility without manually arranging separate desktop windows.
- **Thin evidence and troubleshooting**: The source includes one concrete hiccup: the gradient color appeared stale until a cache buster was used. That suggests real workflows may still need normal browser-debugging habits such as refreshes and cache awareness.

## How It Works

Observed flow from the source: open GitHub Copilot CLI, enter its execute-style mode with `!`, run `terminal browser`, and use the resulting browser pane to open either an external site or a local development site. Then ask the coding agent to launch the app and enable automatic change detection. Once the app is running on a local port, use the browser pane to inspect the live UI while prompting the agent for changes such as updating a gradient color. When the preview does not reflect the latest change, refresh or use a cache-busting approach. The practical pattern is a short feedback loop: issue command, view result, adjust prompt, verify again.

## Training Exercise

Set up a small local web page with one visible style element such as a background gradient or button color. Recreate the workflow from the lesson: launch your AI coding CLI, open the terminal-based browser beside it, start the local site with auto-reload, and ask the agent to make three small UI changes. After each change, verify whether the browser pane updates immediately. If one change does not appear, document whether refresh or cache busting fixes it. Finish by writing a short note on when this workflow is faster than using a separate browser window.

## Test Yourself

<details><summary>What is the main benefit of placing the coding agent and browser preview in the same terminal window?</summary>

It reduces switching among the editor, terminal, and browser while keeping code changes and their visual effects visible side by side. This can shorten the prompt–edit–verify cycle, particularly on one screen.

</details>

<details><summary>Why is hot reload important to this workflow?</summary>

The preview is most useful when it reflects code edits quickly. Automatic change detection lets the user inspect each agent-generated change without repeatedly restarting the app or manually reloading the page.

</details>

<details><summary>What should you try if a visual change does not appear in the embedded browser?</summary>

Refresh the preview and check for stale cached assets, using a cache-busting approach if necessary. In Dan Wahlin’s demo, cache busting made a gradient-color change appear.

</details>

## Further Reading

- [Agent on the left. Real browser on the right. Same terminal.](https://lnkd.in/p/gsN67nwu)
