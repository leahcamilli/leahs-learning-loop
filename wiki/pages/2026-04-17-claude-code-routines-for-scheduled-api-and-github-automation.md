---
title: "Claude Code Routines for Scheduled, API, and GitHub Automation"
source: "https://claude.com/blog/introducing-routines-in-claude-code"
date: "2026-04-17"
tags: [claude-code, automation, github, api, devops]
source_type: "web"
topics: [claude, automation-workflows, coding-agents, ai-agents]
kind: "deep-dive"
depth: 1
actionability: 1
---

## TL;DR

> Claude Code routines turn prompts, repository access, and connectors into hosted workflows triggered by schedules, API calls, or GitHub events. This matters because recurring engineering work can run consistently without relying on someone’s laptop or memory.

## Key Takeaways

1. Package instructions, repository context, connectors, and a trigger into one reusable routine.
2. Use scheduled routines for periodic work such as nightly issue triage, maintenance, and documentation checks.
3. Use API-triggered routines when deployment hooks, alerts, or internal tools need to start a Claude Code session with an HTTP POST payload.
4. Use GitHub webhook routines for repository events; the lesson says a pull-request session can continue handling later comments, code pushes, and CI failures.
5. Design routine outputs around concrete actions such as summaries, comments, Slack posts, issues, recommendations, or draft pull requests.
6. Prioritize high-value automations because runs consume Claude Code usage and are subject to plan-based daily limits.
7. Account for the feature’s stated constraints: research preview status, Claude Code on the web, and supported plan tiers.

## Overview

These notes cover Claude Code routines, a hosted automation feature that turns prompts, repository access, and connectors into repeatable workflows. Instead of depending on a developer’s local machine, routines run in Claude Code’s managed environment and can be triggered on a schedule, via API calls, or from GitHub events.

This matters because it shifts AI-assisted engineering work from ad hoc chat sessions into operational workflows. Teams can use routines for recurring tasks like issue triage, PR review, deploy verification, incident response, and cross-repo maintenance, with clearer triggers, shared context, and more reliable execution.

## Key Concepts

- **Routine**: A reusable Claude Code automation configuration that bundles prompt, repository access, and connectors into a repeatable workflow.
- **Hosted execution**: Runs on Claude Code infrastructure instead of a laptop or self-managed cron host, making workflows always-on and easier to operate.
- **Scheduled routines**: Time-based automations for recurring tasks such as nightly triage, maintenance, or docs checks.
- **API-triggered routines**: Routines expose an endpoint and auth token so external systems can start a run with an HTTP POST payload.
- **GitHub webhook routines**: Event-driven automations tied to repository activity, especially useful for PR review and lifecycle-aware updates.
- **Connectors and repository context**: Routines rely on repo access plus external systems like Slack, logs, issue trackers, or deployment metadata to take meaningful actions.
- **Usage and daily limits**: Runs consume Claude Code usage and are subject to plan-based routine limits, so teams should focus on high-value workflows.

## How It Works

Claude Code routines package three things into a managed workflow: instructions, execution context, and a trigger. The instructions define what Claude should do, the context includes repositories and connectors, and the trigger decides when the workflow starts. Once configured, Claude Code creates a hosted session whenever that trigger fires.

The notes describe three trigger models:

1. **Scheduled routines**  
   These run on a fixed cadence such as hourly, nightly, or weekly. They are best for periodic jobs where timing matters more than an external event. An example is a nightly routine that pulls the highest-priority bug from Linear, attempts a fix, and opens a draft PR.

2. **API routines**  
   Each routine gets a dedicated endpoint and authentication token. An external system sends a POST request with a message or structured payload, and Claude Code starts a session in response. This is a good fit for deployment hooks, observability alerts, or internal tooling.

3. **GitHub webhook routines**  
   These subscribe to repository events and create sessions when matching events occur. For pull requests, Claude can keep a session tied to the PR and continue processing updates like comments, code pushes, or CI failures over time.

A simple mental model is:

- **Input context**: prompt, repo, connectors, payload
- **Trigger**: schedule, API call, or webhook
- **Execution**: Claude Code creates a hosted session
- **Output/actions**: comments, summaries, Slack posts, issues, draft PRs, or recommendations

This model is useful because it turns manual AI usage into event-driven automation. A team no longer has to remember to ask Claude to review a PR or investigate an alert. Instead, they define the workflow once and let the system invoke it consistently when the right conditions occur.

The article’s examples span much of the software lifecycle:

- Backlog triage and issue labeling
- Documentation drift detection
- Deploy verification and release recommendations
- Alert triage before on-call intervention
- Feedback-to-code workflows
- Cross-SDK or cross-repo change porting
- Team-specific PR review checks for security or performance

The notes also connect routines to prior Claude Code CLI behavior: users who previously used `/schedule` are effectively moving into a more centralized, hosted automation model. That indicates routines are not just a convenience feature, but a step toward managed agent orchestration for engineering work.

Operationally, routines come with some constraints: the feature is in research preview, requires Claude Code on the web, and depends on supported plan tiers. There are also daily limits and usage implications, which means teams should be selective and measure whether a routine genuinely saves time or improves reliability.

## Test Yourself

<details><summary>What components does a Claude Code routine package into a managed workflow?</summary>

It combines instructions, execution context such as repositories and connectors, and a trigger. When the trigger fires, Claude Code creates a hosted session that produces configured actions or outputs.

</details>

<details><summary>When should a team choose a schedule, an API call, or a GitHub webhook as the trigger?</summary>

Choose a schedule for recurring time-based work, an API call for external systems such as deployment or observability tools, and a GitHub webhook for automation driven by repository events.

</details>

<details><summary>Why should teams be selective about which workflows become routines?</summary>

The lesson notes that routine runs consume Claude Code usage and face plan-based daily limits. Teams should therefore favor workflows that measurably save time, improve reliability, or consistently produce valuable engineering outcomes.

</details>

## Personal Notes

Claude Code Routines: Scheduled, API, and GitHub-Triggered Automation

Source: https://claude.com/blog/introducing-routines-in-claude-code
Notion page: https://www.notion.so/Claude-Code-Routines-Scheduled-API-and-GitHub-Triggered-Automation-34501bb0839a819fa74fd4920b5d8aa6

Tags: claude-code, automation, webhooks, api, github, devops

Overview

Claude Code routines are hosted automations that let you package a prompt, repository access, and connectors into a repeatable workflow that runs without relying on a developer laptop. Instead of wiring together cron jobs, glue code, and infrastructure yourself, you define the automation once and let Claude Code execute it on a schedule, from an API call, or in response to repository events.

This matters for engineering teams that want to operationalize AI-assisted development work: backlog triage, PR review, deploy verification, incident response, or cross-repo maintenance. The feature is especially relevant to platform engineers, developer productivity teams, and tech leads who want reproducible, always-on agent workflows integrated with source control and internal systems.

Key Concepts

  *   Routine: A routine is a reusable Claude Code automation configuration. It bundles the execution context—prompt, repository, and connectors—so the same workflow can be triggered repeatedly without manually starting a session each time.
  *   Hosted execution: Routines run on Claude Code's web infrastructure rather than on a local machine. This removes the need to keep a laptop online or manage separate cron hosts, and makes the automation available as an always-on service.
  *   Scheduled routines: Scheduled routines execute on a time-based cadence such as hourly, nightly, or weekly. They are suitable for periodic maintenance tasks like issue triage, docs drift detection, or automated bug-fix attempts.
  *   API-triggered routines: Each API routine gets its own endpoint and authentication token. External systems can POST payloads to that endpoint to create a new Claude Code session, making routines easy to integrate with alerting systems, deploy pipelines, and internal tools.
  *   Webhook routines for GitHub: Webhook routines subscribe to GitHub repository events and automatically start sessions when matching events occur. For pull requests, Claude can maintain one session per PR and continue receiving updates like comments or CI failures as the PR evolves.
  *   Connectors and repository context: Routines ship with access to the configured repositories and connectors, which provide the operational context needed to act on real systems. That context is what lets a routine move beyond chat responses into tasks like reading issues, posting to Slack, or opening draft PRs.
  *   Usage and daily limits: Routine runs consume subscription usage in the same way as interactive Claude Code sessions, and there are plan-based daily routine limits. This introduces an operational consideration: teams should reserve routines for high-value, repeatable workflows and monitor usage as they scale adoption.

How It Works

Claude positions routines as the next step beyond manually invoking Claude Code from a terminal. The core idea is simple: define an automation once, including the instructions you want Claude to follow, the repository it should work against, and any external connectors it may need. After that, Claude Code can instantiate that automation repeatedly whenever a configured trigger fires.

The article describes three trigger models:

1. **Scheduled routines** - You provide a prompt plus a cadence. - Claude Code runs the routine automatically at the specified time. - Example from the article: nightly at 2am, fetch the top bug from Linear, attempt a fix, and open a draft PR.

2. **API routines** - Claude Code creates a dedicated endpoint and auth token per routine. - An external system sends an HTTP POST with a message or payload. - Claude Code starts a session and returns a session URL, allowing downstream systems or humans to inspect the run.

3. **GitHub webhook routines** - A routine subscribes to repository events, initially focused on GitHub. - Matching pull requests trigger a new session automatically. - Claude keeps the session attached to the PR lifecycle, feeding in later updates such as comments and CI failures.

The mechanics are important because they shift AI automation from ad hoc prompting to event-driven workflow design. Instead of saying "review this PR" manually, a team can define a review routine once and let it execute whenever a PR with certain characteristics appears. Instead of waiting for an engineer to open Claude Code after an alert fires, an observability system can call the routine endpoint immediately.

A useful way to think about the runtime model is:

- **Input context**: prompt, repo, connectors, trigger payload - **Trigger**: schedule, API call, or webhook event - **Execution**: Claude Code creates a hosted session - **Output/actions**: comments, Slack messages, triage summaries, draft fixes, or PRs

The examples in the article illustrate how this model applies across the software lifecycle:

- **Backlog management**: nightly issue triage and labeling - **Docs drift detection**: periodic scanning of merged PRs against documentation references - **Deploy verification**: post-deploy smoke checks and release-channel recommendations - **Alert triage**: correlating traces and deployments before on-call responds - **Feedback resolution**: turning user or internal feedback into in-context code changes - **Library porting**: mirroring merged changes from one SDK to another - **Custom code review**: applying team-specific security or performance
