---
title: "Microsoft Agent Platform Landscape: Copilot, Foundry, Studio, and Agent 365"
source: "https://microsoft.github.io/agent-resources"
date: "2026-04-27"
tags: [microsoft, ai-agents, copilot, governance, architecture]
source_type: "web"
topics: [ai-agents]
kind: "deep-dive"
depth: 1
actionability: 1
---

## TL;DR

> Choose Microsoft’s agent platform by matching the builder, required technical control, user experience, and governance needs—not by treating the ecosystem as one interchangeable stack. The right architecture may span multiple layers, from Microsoft 365 Copilot as the user-facing experience to Agent 365 for fleet-wide oversight.

## Key Takeaways

1. Use Microsoft 365 Copilot when AI assistance should live inside familiar Microsoft 365 productivity workflows and draw on enterprise content.
2. Choose Copilot Studio when business teams need to create or customize agents quickly through a structured, low-code environment.
3. Use Microsoft Foundry when model selection, evaluation, deployment, and production-grade AI engineering require deeper technical control.
4. Choose code-first Agent Development for SDK-level programmability, custom orchestration, external integrations, and protocol interoperability.
5. Adopt Agent 365 when multiple agents create a need for centralized inventory, policy, lifecycle management, visibility, and operational oversight.
6. Evaluate platform fit across four dimensions: who builds the solution, what agent is needed, where users will access it, and how it will be governed.
7. Use the Agent Platform Advisor when requirements remain ambiguous; expect mature solutions to span more than one platform layer.

## Overview

These notes summarize a top-level map of Microsoft’s AI agent ecosystem, focusing on how different product areas fit distinct parts of the agent lifecycle. Rather than presenting one unified platform, Microsoft separates concerns across Microsoft 365 Copilot, Copilot Studio, Microsoft Foundry, code-first agent development paths, and Agent 365 governance.

This matters because platform selection is itself an architectural decision. For teams moving from experimentation to production, the key question is not just how to build an agent, but where it should live, who should own it, how much technical control is needed, and how governance will be handled at scale.

## Key Concepts

- **Platform segmentation**: Microsoft positions agent development as a set of connected but specialized platforms. Each targets a different lifecycle stage or builder persona, such as business users, low-code builders, pro developers, ML engineers, and IT or governance teams.
- **Microsoft 365 Copilot as adoption surface**: Best suited when the agent experience is embedded in Microsoft 365 and tied to employee productivity, enterprise content, and existing workplace workflows.
- **Copilot Studio for low-code agent creation**: A faster path for creating and launching business-facing agents with a more packaged builder experience and less need for custom code.
- **Microsoft Foundry for model and agent engineering**: A stronger fit when teams need deeper control over model choice, evaluation, deployment, and AI engineering practices.
- **Code-first agent development**: The path for teams that need direct programmability, SDK-level control, custom integrations, orchestration, and support for open protocols or broader ecosystem tooling.
- **Enterprise agent governance with Agent 365**: Once many agents exist, governance becomes its own discipline, covering visibility, policy, lifecycle management, oversight, and centralized control.

## How It Works

The source acts as a navigation hub for Microsoft’s agent ecosystem. Its value is in helping teams choose the right platform based on four practical dimensions:

- who is building the solution
- what kind of agent is being built
- where the experience will run
- how the agent will be governed

A useful interpretation is to map each platform to a different layer of enterprise agent delivery:

- **Experience layer**: Microsoft 365 Copilot, where users consume AI assistance in familiar productivity tools.
- **Builder layer**: Copilot Studio, where teams assemble and customize agents with a low-code experience.
- **Model/runtime layer**: Microsoft Foundry, where models and AI systems are evaluated, deployed, and engineered more formally.
- **Code/integration layer**: Agent Development paths using SDKs, frameworks, and protocols for custom implementations.
- **Governance layer**: Agent 365, where organizations manage an agent fleet with policy, inventory, lifecycle, and operational oversight.

From a decision-making perspective, each platform aligns with a different project shape:

1. **Microsoft 365 Copilot**  
   Start here when the main goal is productivity inside Microsoft 365. Typical owners include IT admins, workplace platform owners, and architects focused on organizational adoption.

2. **Copilot Studio**  
   Use this when a business team needs to create or customize an agent quickly in a structured environment, often without building everything in code.

3. **Microsoft Foundry**  
   Use this when the work requires model evaluation, deployment workflows, deeper technical control, and production-style AI engineering practices.

4. **Agent Development**  
   Choose this when you need full programmability, external tool integration, protocol-level interoperability, or custom orchestration.

5. **Agent 365**  
   Use this when the organization already has multiple agents and now needs enterprise-wide governance, control, and visibility.

6. **Agent Platform Advisor**  
   Use this as a decision aid when requirements are still ambiguous and the right platform is unclear.

The broader lesson is architectural: Microsoft is separating the agent lifecycle into distinct domains so teams can choose tooling that matches their delivery model and maturity level. Not every project should begin in the same product, and many real solutions may span more than one layer.

## Test Yourself

<details><summary>Which four dimensions should guide platform selection in Microsoft’s agent ecosystem?</summary>

Identify who will build the solution, what kind of agent is required, where the experience will run, and how the agent will be governed.

</details>

<details><summary>When should a team prefer Microsoft Foundry over Copilot Studio?</summary>

Prefer Microsoft Foundry when the project requires deeper control over models, evaluation, deployment, and formal AI engineering. Copilot Studio is better suited to faster, structured, low-code agent creation.

</details>

<details><summary>Why might one enterprise solution use more than one Microsoft agent platform?</summary>

The platforms address different lifecycle layers rather than serving as complete substitutes. A solution might use custom development or Foundry for engineering, Microsoft 365 Copilot for the user experience, and Agent 365 for centralized governance.

</details>

## Personal Notes

Navigating Microsoft’s Agent Platform Landscape: Copilot, Foundry, Studio, and Agent 365

Source: https://microsoft.github.io/agent-resources/
Notion page: https://www.notion.so/Navigating-Microsoft-s-Agent-Platform-Landscape-Copilot-Foundry-Studio-and-Agent-365-34f01bb0839a8179ba30f4e108da051a

Tags: ai-agents, microsoft, copilot, copilot-studio, azure-ai-foundry, enterprise-governance

Overview

This page is a top-level map of Microsoft’s agent ecosystem rather than a deep technical article. Its main value is helping engineers, architects, and platform teams decide which Microsoft product area to use when adopting, building, deploying, or governing AI agents across an organization.

The important idea is that Microsoft splits the agent lifecycle into several concerns: end-user productivity with Microsoft 365 Copilot, low-code agent creation with Copilot Studio, model and agent engineering with Microsoft Foundry, code-first agent development using SDKs and protocols, and enterprise-scale governance through Agent 365. If you are deciding where a project should live, what team should own it, or how to move from prototype to production, this resource is the entry point.

Key Concepts

  *   Platform segmentation: Microsoft presents agent development as a set of specialized but related platforms instead of one monolithic product. Each platform addresses a different stage of the lifecycle or a different builder persona, such as business users, pro developers, ML engineers, or IT administrators.
  *   Microsoft 365 Copilot as adoption surface: Microsoft 365 Copilot is positioned around organizational adoption, deployment, and extension of AI capabilities in the productivity stack. It matters when the agent experience is tightly connected to Microsoft 365 applications, enterprise content, and end-user workflows.
  *   Copilot Studio for low-code agent creation: Copilot Studio is framed as the place to create, customize, and launch AI agents with a more packaged builder experience. This is typically relevant when teams want faster delivery, conversational orchestration, and business-managed customization without building everything from scratch in code.
  *   Microsoft Foundry for model and agent engineering: Microsoft Foundry is positioned for building, evaluating, and deploying AI models and agents. This suggests a stronger fit for technical teams that need control over model selection, evaluation, deployment pipelines, and more advanced AI application engineering.
  *   Code-first agent development: The Agent Development section highlights SDKs, frameworks, protocols, and samples for developers building agents with Microsoft tools and the wider ecosystem. This represents the path for teams that need direct programming control, custom integrations, and interoperability with emerging agent standards.
  *   Enterprise agent governance: Agent 365 is described as a control plane for managing an entire agent workforce at enterprise scale. The key idea is that once many agents exist, governance becomes a separate problem involving visibility, policy, lifecycle management, and operational oversight.
  *   Decision support through platform advisory: The Agent Platform Advisor acknowledges that platform choice is itself a design problem. It exists to guide teams toward the right Microsoft platform based on goals, constraints, and likely implementation style.

How It Works

This source functions as a **navigation hub** for Microsoft’s AI agent ecosystem. Rather than teaching one implementation technique, it organizes the space into five major product areas plus a decision tool. The practical takeaway is that Microsoft expects teams to choose a platform based on the combination of **who is building**, **what is being built**, **where it will run**, and **how it will be governed**.

A useful way to interpret the page is by mapping it to the agent lifecycle:

1. **Adopt and extend AI for business users** → **Microsoft 365 Copilot** - Use this when the primary goal is user productivity inside Microsoft 365. - The emphasis is organizational rollout, extension, and operational adoption. - Typical stakeholders: IT admins, productivity platform owners, solution architects.

2. **Create and launch business-facing agents quickly** → **Copilot Studio** - Use this when you want a structured environment for designing and deploying agents. - It is aimed at faster assembly and customization, often with less hand-written code. - Typical stakeholders: solution builders, power users, platform teams, application owners.

3. **Build and evaluate AI systems with deeper technical control** → **Microsoft Foundry** - Use this when your work includes model choice, evaluation, deployment, or AI engineering workflows. - This is the likely fit for teams treating agents as software systems with measurable quality and release processes. - Typical stakeholders: ML engineers, AI engineers, backend developers, platform engineers.

4. **Develop agents with SDKs and protocols** → **Agent Development** - Use this when you need full programmability, custom orchestration, external tool integration, or protocol-level interoperability. - The wording strongly implies support for both Microsoft-native tooling and broader ecosystem standards. - Typical stakeholders: application developers, SDK consumers, systems integrators.

5. **Operate a fleet of agents safely at scale** → **Agent 365** - Use this once multiple agents exist across departments or business units. - The problem shifts from creation to governance: inventory, controls, lifecycle, policy, and centralized management. - Typical stakeholders: enterprise architects, security teams, IT operations, governance teams.

6. **Choose a path** → **Agent Platform Advisor** - Use this when requirements are still being clarified. - It acts like a decision tree for platform fit.

From an engineering perspective, the page suggests a layered architecture for enterprise agent delivery:

- **Experience layer**: where users interact with copilots or agents. - **Builder layer**: where agents are designed
