---
title: "How AI Agents Reallocate Software Value Across Data, Workflows, and Interfaces"
source: "https://www.youtube.com/watch?v=0j8wy4jUlsw"
date: "2026-10-07"
tags: [ai-agents, software-strategy, saas, enterprise-ai, workflow-design]
source_type: "youtube"
source_fingerprint: "021cab04fe"
source_characters: 42620
channel: "AI News & Strategy Daily | Nate B Jones"
published: "2026-10-04"
duration_seconds: 2181
topics: [ai-strategy, ai-agents]
kind: "opinion"
depth: 2
actionability: 2
---

## TL;DR

> AI agents can make a software interface easier to abandon while making reliable data, specialized workflows, and accumulated agent context more valuable. Evaluate software by separating its data, application, and agentic layers—and by measuring the business outcomes each layer enables.

## Key Takeaways

1. Separate every software purchase into three layers: data, application workflows, and agentic interaction.
2. Agent accessibility is becoming table stakes, but an API or MCP connection alone does not give customers a reason to keep paying.
3. Preserve dependable applications for high-risk execution such as payroll; an agent can simplify their complexity without replacing their rules, approvals, and compliance controls.
4. Document how employees use AI before changing vendors, because valuable instructions, preferences, feedback, and unwritten procedures may be embedded in individual agent setups.
5. Compare building with buying based on risk and opportunity cost: a custom recruiting search may be practical, while rebuilding compliant payroll could divert engineers from competitive work.
6. Design software so structured data and workflows are accessible from multiple interfaces and agents rather than depending on repeated visits to one graphical interface.
7. Tie AI adoption and software purchasing to outcomes such as sales, revenue, profitability, or operating speed—not merely to whether a product includes AI.

## Key Moments

- [2:02](https://www.youtube.com/watch?v=0j8wy4jUlsw&t=122s) — See how a recruiter’s agent absorbs selection criteria and becomes harder to replace than the original recruiting interface.
- [4:35](https://www.youtube.com/watch?v=0j8wy4jUlsw&t=275s) — Learn what customers still pay for when agents perform much of the information processing.
- [17:32](https://www.youtube.com/watch?v=0j8wy4jUlsw&t=1052s) — Use DoorDash’s text ordering and limited MCP beta to understand how a business can retain transactions after losing direct interface usage.
- [19:03](https://www.youtube.com/watch?v=0j8wy4jUlsw&t=1143s) — Understand why agent connectivity earns consideration but does not create durable differentiation by itself.
- [21:06](https://www.youtube.com/watch?v=0j8wy4jUlsw&t=1266s) — Compare a custom recruiting workflow built on Crustdata APIs with packaged recruiting software.
- [22:41](https://www.youtube.com/watch?v=0j8wy4jUlsw&t=1361s) — See why an agent may increase Workday payroll’s value instead of replacing its configured rules and execution system.
- [24:30](https://www.youtube.com/watch?v=0j8wy4jUlsw&t=1470s) — Apply the data, application, and agentic-layer framework to employees, buyers, and software vendors.
- [29:56](https://www.youtube.com/watch?v=0j8wy4jUlsw&t=1796s) — Turn the framework into concrete actions for employees, leaders, and software sellers.

## Overview

The presenter proposes a three-layer model for understanding software in an agent-mediated workplace: the data layer supplies information, the application layer provides interfaces and structured workflows, and the agentic layer interprets requests and coordinates work. Agents may reduce direct use of traditional interfaces without eliminating the underlying data, rules, approvals, or execution systems.

This model matters to employees whose working knowledge is becoming embedded in agents, leaders choosing vendors, and sellers redefining software value. The central practical lesson is to identify which layer produces an outcome, what can safely be substituted, and what context or reliability would be lost during a change.

## Key Concepts

- **Data layer**: This layer contains records and structured information that agents need to perform useful work. In the recruiting example, the presenter reports that a business retained the structured candidate-data provider while building its own search workflow above it.
- **Application layer**: Applications combine interfaces with workflows, and those components should not be treated as identical. A graphical interface may become less important while the underlying workflow—especially one involving rules, approvals, or compliance—remains highly valuable.
- **Agentic layer**: This layer interprets goals, processes information, invokes tools, and coordinates tasks. Its value can grow as users teach it preferences, exceptions, and procedures that were never formally documented.
- **Context lock-in**: An agent can accumulate selection criteria, feedback, custom skills, and tacit operating knowledge over time. The presenter argues that changing AI vendors may therefore cost more than leaders realize, even when the new vendor appears cheaper by license or token price.
- **Agent reachability**: APIs and protocols such as MCP let external agents retrieve data or request actions. The DoorDash example illustrates the strategy: preserve the transaction whether a customer uses DoorDash’s own assistant or another agent, although the presenter cautions that reachability alone is only table stakes.
- **Dependable execution**: Some systems remain valuable because they execute consequential work correctly, not because users enjoy their interfaces. The Workday payroll example highlights configured rules, records, approvals, issue detection, and compliance-sensitive execution that an agent can make easier to navigate.
- **Build-versus-buy boundary**: AI lowers the cost of constructing some workflows, making a custom layer over purchased data more plausible. The boundary changes when errors carry substantial compliance risk or when internal engineering effort would be better spent on competitive advantage.
- **Multi-value stack**: The presenter argues that vendors increasingly need to explain their combined value across data, workflows, agent access, trust, and optionality. Buyers should test each claim separately and ask how the complete stack improves a measurable business outcome.

## How It Works

1. Map the data layer: identify each system of record, data supplier, access method, ownership boundary, and source of unique information.
2. Decompose the application layer: distinguish the visible interface from the rules, approvals, integrations, and execution workflows underneath it.
3. Map the agentic layer: record which agents people use, what tools they call, what instructions or skills they contain, and how feedback improves their output.
4. Trace a real outcome through all three layers—for example, candidate selection, customer onboarding, food ordering, or payroll correction.
5. Test substitutability: ask what happens if the interface, workflow provider, data source, or agent is changed independently.
6. Estimate hidden migration costs, including lost context, recreated skills, retraining, validation, compliance review, and temporary productivity loss.
7. Decide whether to build, buy, or combine components according to differentiation, execution risk, engineering opportunity cost, and required vendor optionality.
8. Reassess regularly as agent capabilities improve and the boundary between interface work and automated work shifts.

## Training Exercise

1. Choose one recurring workflow you perform, such as preparing a candidate shortlist, onboarding a customer, or resolving an invoice issue.
2. Draw three columns labeled Data, Application, and Agent. List every source, workflow, interface, rule, and AI tool involved.
3. Mark what is unique or difficult to reproduce: proprietary records, tacit instructions, approval logic, compliance controls, integrations, or agent memory.
4. Simulate four changes separately: remove the graphical interface, replace the data provider, replace the workflow system, and replace the agent.
5. For each change, estimate reconstruction time, validation work, operational risk, and the business outcome affected.
6. Decide which components should remain purchased, which could be built, and which need portability measures such as documented prompts, exported instructions, or vendor-neutral access.
7. Summarize the result for a manager in five sentences: the outcome, the three layers involved, the hardest component to replace, the main risk, and your recommendation.

## Test Yourself

<details><summary>Why can an agent weaken one vendor relationship while strengthening another?</summary>

It can replace the interface or information-arrangement work of a point solution while continuing to depend on an underlying data provider or execution system. Meanwhile, the agent accumulates organization-specific instructions and context that make the agent relationship costly to replace.

</details>

<details><summary>Why is making software reachable through MCP or an API insufficient as a long-term strategy?</summary>

Connectivity allows agents to consider and use a service, but comparable providers can become easier to substitute once they are equally accessible. Durable value must still come from differentiated data, dependable execution, valuable workflows, or specialized agent capabilities.

</details>

<details><summary>How should a leader evaluate an AI-vendor change without accidentally destroying productivity?</summary>

First map how teams actually use agents, including local instructions, data sources, feedback loops, and application workflows. Then compare migration costs and business outcomes across all three layers instead of making the decision from license or token prices alone.

</details>

## Further Reading

- [Full post: AI agents and software buying](https://natesnewsletter.substack.com/p/ai-agents-software-buying?utm_source=youtube&utm_medium=video&utm_campaign=ai-agents-software-buying-launch&utm_content=description)
- [Nate's Library MCP connection guide](https://unlock-ai.natebjones.com/guides/how-to-connect-nates-library?utm_source=youtube&utm_medium=video&utm_campaign=ai-agents-software-buying-launch&utm_content=description)
