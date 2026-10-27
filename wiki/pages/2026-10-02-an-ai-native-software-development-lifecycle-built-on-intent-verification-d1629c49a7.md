---
title: "An AI-Native Software Development Lifecycle Built on Intent, Verification, and Feedback"
source: "https://www.youtube.com/watch?v=6CaQ9ZFuuKI"
date: "2026-10-02"
tags: [software-development, ai-agents, testing, ci-cd, code-review, observability]
source_type: "youtube"
source_fingerprint: "d1629c49a7"
source_characters: 27135
channel: "Eric Tech"
published: "2026-09-20"
duration_seconds: 1262
topics: [coding-agents, ai-agents, claude]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> AI can accelerate implementation, but the surrounding lifecycle must become more rigorous. Capture intent, turn it into an executable specification and plan, give agents automated verification, constrain risky actions, and feed production evidence into the next development cycle.

## Key Takeaways

1. Separate the artifact chain into intent.md for why the change matters, spec.md for what the system must do, and plan.md for how the work will be completed and verified.
2. Make every implementation task self-checking: the presenter recommends withholding “done” status until tests, linting, and the build are all green.
3. Test from the bottom up: cover functions with Jest or Vitest, UI components with React Testing Library, and complete user flows with Cypress or Playwright.
4. Protect model and instruction changes with continuous evaluations; the presenter relays a recommendation to build evals from 20–50 real tasks the agent has previously completed.
5. Encode team-specific review standards in review.md, including required checks, finding severity, and files or findings that should be ignored.
6. Use hooks as deterministic guardrails to block credential exposure, edits to protected files, unsafe production access, or merges that fail required checks.
7. Monitor releases through tools such as Datadog or Sentry, roll back serious regressions when authorized, and convert recurring production problems into new intent artifacts.

## Key Moments

- [1:44](https://www.youtube.com/watch?v=6CaQ9ZFuuKI&t=104s) — Learn how an AI interview can refine requirements and preserve decisions in intent.md or a ticket system.
- [4:10](https://www.youtube.com/watch?v=6CaQ9ZFuuKI&t=250s) — See why intent captures the “why” while a specification defines technical requirements and expected behavior.
- [6:05](https://www.youtube.com/watch?v=6CaQ9ZFuuKI&t=365s) — Turn intent and specifications into ordered, file-specific tasks with risks and completion evidence.
- [8:53](https://www.youtube.com/watch?v=6CaQ9ZFuuKI&t=533s) — Give the coding agent a verification loop based on tests, linting, builds, or other observable checks.
- [12:15](https://www.youtube.com/watch?v=6CaQ9ZFuuKI&t=735s) — Choose tests by layer: functions first, then UI components, then complete user journeys.
- [14:00](https://www.youtube.com/watch?v=6CaQ9ZFuuKI&t=840s) — Use 20–50 previously completed tasks as regression evaluations when models, rules, or skills change.
- [15:46](https://www.youtube.com/watch?v=6CaQ9ZFuuKI&t=946s) — Standardize AI code review with review.md and enforce non-negotiable safety rules through hooks.
- [18:13](https://www.youtube.com/watch?v=6CaQ9ZFuuKI&t=1093s) — Connect deployment failures and production monitoring to repair, rollback, and a new development cycle.

## Overview

An AI-native software development lifecycle uses agents throughout planning, design, implementation, testing, review, deployment, and maintenance. Faster code generation does not eliminate engineering discipline; it shifts more attention toward precise requirements, reliable verification, controlled permissions, and production feedback.

The approach is useful to developers and teams adopting coding agents such as Claude Code. Its central pattern is an auditable chain of artifacts and checks: intent → specification → plan → implementation → automated verification → review and guardrails → deployment → monitoring → new intent.

## Key Concepts

- **Intent artifact**: intent.md records why a change should exist, including the problem, desired outcome, affected users, constraints, and open questions. A project may have one intent per change, and the source of truth may live in the repository or in a ticket system such as Jira, GitHub Projects, or Linear.
- **Specification artifact**: spec.md translates intent into what the system must do, including technical requirements and expected behavior. It creates a clearer contract for implementation without collapsing the business reason and technical design into the same document.
- **Execution plan**: plan.md converts the intent and specification into actionable work. The described template includes the files to change, work order, risks, and evidence that will prove completion; teams can retain their existing planning format if it already works.
- **Agent verification loop**: An agent needs observable feedback so it can check and repair its own work. The presenter highlights tests, linting, builds, screenshots, and behavioral output as possible checks, with tests, linting, and build all expected to pass before completion is reported.
- **Layered testing**: Tests follow dependency direction: functions form the lowest layer, UI components may depend on several functions, and end-to-end tests exercise complete flows across pages. The source associates Jest or Vitest with functional tests, React Testing Library with components, and Cypress or Playwright with end-to-end flows.
- **Continuous agent evaluations**: Automated tests check the product, while agent evaluations check whether a model, skill, or ruleset can still perform representative tasks. The presenter reports a recommendation to derive 20–50 eval cases from successful real tasks and run them in continuous integration when models or instructions change.
- **Review policy and hooks**: review.md can encode a team's pull-request procedure, including required tests, finding categories and severity, and exclusions such as generated files. Hooks add deterministic controls around agent actions, such as preventing secrets, protected-file edits, unsafe database access, or unapproved merges.
- **Closed-loop operations**: Deployment is divided into pre-release diagnosis and post-release observation. Build failures can initiate a proposed repair, while production signals from systems such as Datadog or Sentry can trigger investigation, authorized rollback, and a new intent-driven cycle.

## How It Works

1. Interview stakeholders or the requester until the problem, outcomes, constraints, affected users, and unresolved choices are explicit.
2. Store those decisions in intent.md or the team's ticket system as the durable source of truth for why the change exists.
3. Convert the intent into spec.md, defining technical requirements and expected behavior.
4. Produce plan.md with ordered tasks, exact files or interfaces where known, risks, and proof-of-completion checks.
5. Write the relevant tests before or alongside implementation, beginning with functions and moving upward to components and complete user flows.
6. Let the agent implement against a feedback loop, correcting its work until required tests, linting, builds, and other checks pass.
7. Run representative agent evaluations in CI so model, rule, or skill changes do not silently weaken established workflows.
8. Review the pull request against review.md and enforce hard safety boundaries with hooks before permitting a merge or production action.
9. Diagnose deployment failures, inspect production metrics after release, and turn recurring operational findings into a fresh intent artifact.

## Training Exercise

1. Choose a small change, such as adding validation and an error message to an existing form.
2. Draft intent.md with the problem, desired outcome, affected users, constraints, and open questions.
3. Write spec.md with accepted inputs, invalid cases, visible behavior, and any relevant interfaces.
4. Create plan.md listing the files to inspect or change, task order, major risks, and completion checks.
5. Add one function-level test, one component test, and one end-to-end happy or failure path where the application supports those layers.
6. Implement the change while repeatedly running tests, linting, and the build; do not mark the work complete until every required check passes.
7. Draft a short review.md covering bugs, security, compliance, severity levels, and ignored generated files. Review the change against it.
8. Define one hook or CI rule that blocks a realistic unsafe action, such as committing a credential or merging after failed tests.
9. Specify the production signal you would monitor and write the intent statement that a regression in that signal would generate for the next cycle.

## Test Yourself

<details><summary>Why are intent.md, spec.md, and plan.md separate rather than combined into one prompt?</summary>

They preserve three different decisions: why a change is needed, what behavior and technical requirements define it, and how the agent should implement and prove it. This separation makes assumptions and omissions easier for humans and agents to inspect.

</details>

<details><summary>What makes an agent task verifiable instead of merely well described?</summary>

It includes observable completion checks, such as passing tests, linting, a successful build, screenshots, or expected outputs. The agent can use those checks as a feedback loop and correct its work before requesting human review.

</details>

<details><summary>How does production monitoring become part of planning?</summary>

Logs and metrics can reveal recurring errors, slow queries, or user drop-off after deployment. Those findings become new intent artifacts, which restart the specification, planning, implementation, testing, review, and deployment cycle.

</details>

## Further Reading

- [AI-Native SDLC Playbook](https://academy.claude.com/courses/ai-native-sdlc-playbook/introduction)
- [Eric Tech community](https://www.skool.com/erictech/about)
- [BookZero](https://bookzero.ai)
- [Certificate Program in Agentic AI](https://online.lifelonglearning.jhu.edu/jhu-certificate-program-agentic-ai?utm_source=Brand_Mktg&utm_medium=YT+Influencer&utm_campaign=Eric)
