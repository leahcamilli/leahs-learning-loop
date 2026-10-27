---
title: "Claude Code Routines: Event-Driven and Scheduled Automations for Engineering Workflows"
source: "https://claude.com/blog/introducing-routines-in-claude-code"
date: "2026-06-06"
tags: [claude-code, automation, webhooks, api, scheduling, devops]
source_type: "web"
topics: [claude, automation-workflows, ai-agents, coding-agents]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> Claude Code routines package a prompt, repository context, and connectors into hosted automations triggered by schedules, API calls, or GitHub events. They can replace substantial automation glue, but reliable production use depends on narrow prompts, explicit contracts, guardrails, and careful usage prioritization.

## Key Takeaways

1. Choose scheduled triggers for recurring work, API triggers for explicit machine-to-machine calls, and webhooks for reactions to source-control events.
2. Define each routine with a precise prompt, target repository, required connectors, expected inputs, and exact output artifacts.
3. According to the article, each invocation creates a traceable Claude session; GitHub webhook routines can keep updating the same session as a pull request evolves.
4. Scope routines to bounded tasks and sensitive paths—for example, review only PRs touching `/auth-provider` against an authentication checklist.
5. Test the workflow manually on a real PR, issue, deploy, or alert before automating it, then refine the prompt until outputs are consistent.
6. Add filters, required payload fields, allowed file scopes, and low-confidence behavior to control noise and reduce unsafe actions.
7. Prioritize repetitive, high-value workflows because routines share the interactive Claude Code usage budget and are also subject to plan-based daily limits.

## Overview

Claude Code routines are hosted automations that let teams package a prompt, repository context, and external connectors into a repeatable workflow. Instead of wiring together cron jobs, bots, webhooks, and custom infrastructure yourself, you define the routine once and let Claude Code run it on a schedule, via an API endpoint, or in response to events such as GitHub activity.

This matters to engineers who want to operationalize AI inside the software development lifecycle without depending on a developer laptop or bespoke automation glue. The feature is especially relevant for platform teams, developer productivity engineers, DevOps/SRE teams, and engineering managers who want reliable backlog triage, PR review, deploy verification, alert handling, and cross-repo maintenance workflows.

## Key Concepts

- **Routine**: A routine is a reusable Claude Code automation configured with a prompt, a target repository, and optional connectors to external systems. Once created, it can be executed repeatedly under different trigger modes without manually starting a new interactive session each time.
- **Hosted execution**: Routines run on Claude Code's web infrastructure rather than on a local machine. This makes them suitable for production-style automation because they continue to run even when no developer workstation is online.
- **Trigger modes**: Claude Code supports three trigger styles for routines: scheduled execution, API-triggered execution, and webhook-driven execution. These modes cover recurring maintenance tasks, ad hoc machine-to-machine calls, and event-driven workflows tied to systems like GitHub.
- **Session-per-run model**: Each routine invocation creates a Claude session that carries the context and execution history of that run. For webhook flows like GitHub PR handling, Claude can continue updating the same session as new events arrive, such as comments or CI failures.
- **Connectors and repository context**: Routines ship with access to the configured repository and any connected tools or services. This enables workflows that combine source code analysis with issue trackers, chat systems, monitoring platforms, and deployment pipelines.
- **Operational limits and usage**: Routines consume the same subscription usage budget as interactive Claude Code sessions, with additional daily routine limits by plan. That makes them powerful but constrained resources, so teams should prioritize high-leverage automations and design prompts that are narrowly scoped.

## How It Works

Claude Code routines turn an interactive coding agent into a background automation primitive. The central idea is simple: define a prompt that describes a recurring engineering task, attach it to a repository and any needed connectors, then choose how it should start. Claude Code hosts the execution environment, so the routine can run on a clock, in response to an HTTP request, or when a subscribed event occurs.

The article describes three execution paths:

1. **Scheduled routines**
   - You specify a cadence such as hourly, nightly, or weekly.
   - Claude Code launches the routine automatically at that time.
   - Example: every night at 2am, inspect the top Linear bug, attempt a fix, and open a draft PR.
   - Existing `/schedule` CLI usage maps into this model.

2. **API routines**
   - Each routine gets its own endpoint and auth token.
   - An external system sends a `POST` request with a message or payload.
   - Claude returns a session URL, giving you a traceable execution artifact.
   - This is useful for deploy hooks, alerting systems, internal tooling, and dashboards.

3. **Webhook routines**
   - Initially focused on GitHub events.
   - A routine subscribes to repository events and filter rules.
   - Claude opens one session per matching PR and continues feeding updates from that PR into the session over time.
   - This makes the routine stateful across the life of a PR rather than a one-shot trigger.

The practical workflow looks like this:

- **Input definition**: you write the prompt and specify the repo plus external connectors.
- **Trigger binding**: you attach a schedule, expose an API endpoint, or subscribe to GitHub events.
- **Execution**: Claude Code starts a hosted session when the trigger fires.
- **Context gathering**: the routine uses repository context and connector data such as issues, traces, or alerts.
- **Action generation**: Claude produces outputs like summaries, PR comments, draft fixes, triage recommendations, or even code changes and pull requests.
- **Continuation**: for some webhook scenarios, the same session is updated as new event data arrives.

A useful way to think about routines is as an AI-native replacement for a chunk of developer automation infrastructure. Traditionally, a team might need:

- a cron scheduler
- a bot account
- webhook receivers
- secret management
- scripts for repository checkout and API access
- notification plumbing to Slack or similar systems

Routines compress much of that into a managed abstraction centered on prompt-driven automation.

The examples in the article reveal the kinds of workflows Claude Code is optimized for:

- **Backlog management**: review new issues nightly, classify them, assign owners, and summarize changes in chat.
- **Docs drift detection**: inspect merged PRs and identify documentation that now mismatches changed APIs.
- **Deploy verification**: after deployment, run smoke-check logic, inspect logs, and produce a go/no-go recommendation.
- **Alert triage**: receive monitoring alerts, correlate with recent changes, and prepare an initial diagnosis or draft fix.
- **Feedback resolution**: turn inbound product or docs feedback into repository-aware changes.
- **PR review and governance**: apply custom team rules to code review, especially for sensitive modules.
- **Cross-language/library porting**: trigger a matching change in a parallel SDK or service after a merge.

The design implication is important: routine quality depends heavily on prompt precision and scope control. A broad prompt like "review this PR" may produce inconsistent behavior, while a constrained prompt such as "for PRs touching `/auth-provider`, summarize authentication-relevant changes, identify security implications, and post a summary to `#auth-changes`" is much more operationally reliable.

Because routines consume usage and have plan-based daily caps, teams should treat them like production automations with prioritization and observability. Start with tasks that are repetitive, bounded, and high-value:

- triage work that follows a checklist
- notifications that depend on repository context
- post-deploy analysis with a clear output format
- code review gates for narrow, high-risk components

The article also signals an architectural direction: Claude Code is evolving from a developer-operated assistant into a hosted automation platform. Scheduled jobs, API endpoints, and webhook subscribers are standard building blocks in software platforms; here, they are wrapped around an AI coding agent that already understands repositories and developer tools.

## Training Exercise

Build a design for a routine-driven engineering automation, then test it manually.

### Goal
Create a concrete routine spec for one recurring task in your team, choosing the right trigger mode and defining the prompt, inputs, and outputs.

### Step 1: Pick a realistic task
Choose one of these examples or your own:

- Nightly issue triage from Linear or GitHub Issues
- Post-deploy verification after CI/CD completes
- PR review for a sensitive module like auth, billing, or infra
- Alert triage for a specific Datadog or PagerDuty event

Write down:

- the repository involved
- the external systems involved
- the expected output artifact
  - Slack message
  - draft PR
  - PR comment
  - triage summary

### Step 2: Choose the trigger type
Use this decision rule:

- **Scheduled** if it happens on a time cadence
- **API** if another tool should explicitly call it
- **Webhook** if it should react automatically to source-control events

Document your choice in one sentence. Example:

- "Use a webhook routine because the task should start whenever a PR touching `/auth-provider` is opened or updated."

### Step 3: Draft the routine prompt
Write a prompt that is narrow and operational. Use this template:

```text
You are an engineering automation routine for the repository <repo-name>.

Trigger context:
- Source: <schedule/api/webhook>
- Event payload: <describe expected payload>

Your job:
1. Inspect the relevant code changes or alert context.
2. Apply this checklist:
   - <rule 1>
   - <rule 2>
   - <rule 3>
3. Produce exactly these outputs:
   - <output 1>
   - <output 2>
4. If confidence is low, say what additional information is needed.

Constraints:
- Do not modify files outside <allowed scope>.
- Prioritize <security/reliability/clarity/etc.>.
- Keep the response format machine-readable when possible.
```

### Step 4: Define the payload and output contract
For an API or webhook routine, sketch the input payload and expected response. Example:

```json
{
  "service": "payments-api",
  "environment": "prod",
  "deploy_sha": "abc123",
  "timestamp": "2026-04-14T02:00:00Z",
  "alert": "5xx rate increased after deploy"
}
```

Expected output:

```text
Summary: Elevated 5xx likely correlated with deploy abc123.
Suspected owner: payments platform team.
First step: Roll back feature flag X and inspect error logs for /charge.
Confidence: medium.
```

### Step 5: Simulate one run manually
Before automating, run the process by hand:

1. Pick a real PR, issue, or deploy event from your system.
2. Paste the routine prompt and the event context into an interactive Claude Code session.
3. Compare the output against your desired artifact.
4. Tighten the prompt until the result is consistent.

### Step 6: Add guardrails
List at least three failure modes and mitigations. Example:

- PR is too large → only analyze changed files in specific directories
- Alert lacks deploy metadata → require `service` and `deploy_sha` fields
- Routine comments too noisily on every update → filter to specific file paths or event types

### Stretch task
Design two versions of the same routine:

- a broad version: handles all PRs in the repo
- a narrow version: handles only `/auth-provider`

Then compare which one is more likely to be reliable, cheaper to run, and easier to trust in production.

## Test Yourself

<details><summary>Which trigger type should be used for scheduled maintenance, an explicit deployment callback, and a GitHub PR event?</summary>

Use a scheduled routine for maintenance on a cadence, an API routine when the deployment system should call it directly, and a webhook routine for GitHub PR activity.

</details>

<details><summary>Why is a prompt limited to PRs touching `/auth-provider` likely to outperform a generic “review this PR” prompt?</summary>

The narrower prompt supplies a clear scope, checklist, and expected output, making behavior more consistent, cheaper to run, and easier to trust. It also limits irrelevant analysis and comments.

</details>

<details><summary>What should a team do before putting a routine into production?</summary>

Simulate it manually with a real event, compare the result with the desired artifact, and refine the prompt. Then add guardrails for predictable failures, including missing inputs, oversized changes, excessive triggering, and low-confidence conclusions.

</details>

## Further Reading

- [Introducing routines in Claude Code](https://claude.com/blog/introducing-routines-in-claude-code)
- [Claude Code documentation](https://docs.anthropic.com/)
- [GitHub Webhooks documentation](https://docs.github.com/en/webhooks)
- [Cron expression and scheduling concepts](https://en.wikipedia.org/wiki/Cron)
