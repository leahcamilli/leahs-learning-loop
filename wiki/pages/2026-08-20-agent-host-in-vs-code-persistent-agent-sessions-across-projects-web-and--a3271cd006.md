---
title: "Agent Host in VS Code: Persistent Agent Sessions Across Projects, Web, and Machines"
source: "https://lnkd.in/p/gj_cmNSu"
date: "2026-08-20"
tags: [developer-tools, vscode, agent-systems, session-management, remote-development]
source_type: "web"
source_fingerprint: "a3271cd006"
source_characters: 5915
topics: [developer-tools, ai-agents]
kind: "demo"
depth: 1
actionability: 1
---

## TL;DR

> VS Code's Agent Host separates an agent session from any single editor window, allowing the session to keep running and be accessed across projects, interfaces, and machines. This architecture matters because clients can reconnect to shared session state without owning the agent’s lifetime.

## Key Takeaways

1. Treat the client, host process, and session state as separate architectural layers; the demo indicates that closing a folder or changing projects does not end a host-owned session.
2. The demo shows one live session synchronizing approved tool calls, chat input, and queue changes across multiple attached clients.
3. The same session can be accessed through VS Code’s chat view, an Agents window, and the web interface at `vscode.dev/agents`.
4. Remote session access allows a browser to connect to an Agent Host machine and interact with sessions that are still running there, according to the demo.
5. Agent Host can reconnect to another machine so users can view or start sessions against folders located on that remote host.
6. Do not infer protocol mechanics, storage design, authentication, security, or failure recovery from the demo; those implementation details are not established by the source.
7. Test host-based persistence by starting a session, closing its folder, switching projects, reconnecting from another client, and checking which actions remain synchronized.

## Overview

This lesson explains the core idea demonstrated in the source: VS Code's Agent Host separates an agent session from the editor window so the session can keep running across project switches, web access, and multiple machines. The practical takeaway is architectural: if agent execution lives in a dedicated host process instead of a single client window, the same live session can be resumed and controlled from different interfaces. Evidence is limited to a product demo transcript and linked resources, so implementation details beyond the demonstrated behavior are not established here.

## Key Concepts

- **Dedicated host process**: The transcript says agent sessions run in their own dedicated process, rather than being tied to a VS Code window, client, or machine session.
- **Session persistence across projects**: A session continues running even after the original folder is closed and another project is opened, which shows that project context and UI context are not the same as process lifetime.
- **Shared live session state**: The demo shows the same session appearing side by side in different clients, with live updates such as approved tool calls, chat input, and queue changes reflected across views.
- **Multiple clients for one session**: The same agent session can be accessed from the VS Code chat view, an Agents window, and the web at `vscode.dev/agents`, implying client attachment to a common backend session.
- **Remote session access**: The source shows enabling remote session access so a browser can connect to an agent-host machine and interact with sessions still running there.
- **Cross-machine agent hosts**: The demo includes reconnecting to a remote host on another machine and viewing or starting sessions against folders on that machine through Agent Host.

## How It Works

Based on the demo, Agent Host changes the execution model from 'session lives inside this editor window' to 'session lives in a host process that clients attach to.' A likely mental model is: 1) start a session from VS Code, 2) the host process owns execution and history, 3) any compatible client such as the chat view, Agents window, or web UI connects to that same running session, and 4) remote hosts expose sessions running on other machines. The source also mentions a 'copilot harness option' powered by the Copilot SDK and running on Agent Host, plus an Agent Host Protocol whose spec is live and under active development. The source does not provide protocol mechanics, storage design, or security details, so those remain unknown from this material alone.

## Training Exercise

Create a short architecture note with three columns: `client`, `host`, and `session state`. Using only the source, map what belongs in each column. Then write a test plan you would run if you had access to the feature: start a session, close the folder, open a different project, reconnect from another client, and verify which actions stay synchronized. Finish by listing two benefits of host-based sessions and two unanswered questions the demo leaves open, such as authentication, failure recovery, or protocol details.

## Test Yourself

<details><summary>How does Agent Host change the relationship between an agent session and a VS Code window?</summary>

The lesson describes the session as living in a dedicated host process rather than inside one editor window. Compatible clients attach to that host-owned session, so changing projects or closing the original folder does not necessarily stop it.

</details>

<details><summary>What evidence in the demo suggests that multiple clients share one live session?</summary>

The same session appears in multiple interfaces, with approved tool calls, chat input, and queue changes reflected across views. The lesson presents this as evidence of clients attaching to common backend session state.

</details>

<details><summary>Which important implementation questions remain unanswered by the source?</summary>

The source does not establish how authentication, storage, security, failure recovery, or the Agent Host Protocol work internally. These should be treated as open questions rather than assumed capabilities.

</details>

## Further Reading

- [Source post](https://lnkd.in/p/gj_cmNSu)
- [Agent Host in VS Code](https://lnkd.in/g2iwf3j6)
- [Agent Host Protocol](https://lnkd.in/g9VjdPd5)
- [VS Code issue tracker](https://lnkd.in/e_vCWA7p)
