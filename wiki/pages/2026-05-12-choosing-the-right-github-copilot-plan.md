---
title: "Choosing the Right GitHub Copilot Plan"
source: "https://docs.github.com/en/copilot/get-started/plans"
date: "2026-05-12"
tags: [github, copilot, pricing, enterprise, developer-tools]
source_type: "web"
topics: [github-copilot, ai-strategy]
kind: "deep-dive"
depth: 1
actionability: 2
---

## TL;DR

> Choose the minimum GitHub Copilot plan that supports your actual workflow: individuals mainly need to compare usage and model access, while organizations also need governance and administration. This matters because the selected tier determines both developer capabilities and operational control.

## Key Takeaways

1. Choose Copilot Free for experimentation, Student when eligible, Pro for daily professional use, and Pro+ for broader model access and a larger premium-request allowance.
2. Choose Copilot Business when centralized seat management and organization-wide policies are required; choose Enterprise for additional enterprise-scale administration, governance, and premium-request capacity.
3. Free limits completions, while Student, Pro, Pro+, Business, and Enterprise provide unlimited completions according to the lesson.
4. Check cloud agent, agent mode, code review, MCP, and third-party-agent support explicitly because availability differs by plan.
5. Treat monthly premium requests as a capacity constraint for heavy AI-assisted workflows, especially when comparing Pro with Pro+.
6. Verify support in the intended client—such as VS Code, Visual Studio, JetBrains IDEs, Xcode, Eclipse, GitHub Mobile, or Windows Terminal—because features can be platform-specific.
7. The lesson notes that GitHub plans to shift from request-based to usage-based billing on June 1, 2026, and that enterprise offerings apply to GitHub Enterprise Cloud rather than GitHub Enterprise Server.

## Overview

These notes compare GitHub Copilot plans across individual, team, and enterprise use cases, focusing on what actually changes between tiers: model access, completion limits, premium request quotas, agent features, and governance controls. The core takeaway is that plan choice is not just about price; it directly shapes developer workflow, available AI features, and how much administrative control an organization has.

This matters because the “best” plan depends on the problem being solved. An individual may care most about unlimited completions and access to stronger models, while an engineering organization may prioritize policy enforcement, auditability, seat management, and rollout at scale. The notes are especially useful as a practical evaluation guide for matching personas and operational requirements to the minimum viable Copilot plan.

## Key Concepts

- **Plan segmentation**: GitHub splits Copilot into individual plans (Free, Student, Pro, Pro+) and managed plans (Business, Enterprise). This reflects a shift from personal productivity needs to organizational governance and deployment.
- **Premium requests**: Advanced capabilities are governed by monthly premium request quotas. These differ sharply by plan, so request budget can become a meaningful constraint for heavy users or AI-assisted workflows.
- **Included models vs premium models**: Model availability is tier-dependent. Higher plans generally offer broader model choice and better access to premium models, while lower plans may limit access or message volume.
- **Agent capabilities**: Features like cloud agent, agent mode, code review, MCP, and third-party agents are not evenly available across plans. Teams interested in agentic workflows need to verify support before rollout.
- **Governance and policy control**: Business and Enterprise plans introduce organization-wide controls such as policy management, audit logs, content exclusion, and blocking suggestions matching public code.
- **IDE and platform availability**: Copilot capabilities vary by tool and client. Support can differ across VS Code, Visual Studio, JetBrains IDEs, Xcode, Eclipse, GitHub Mobile, and Windows Terminal.

## How It Works

GitHub Copilot uses a shared feature surface—chat, inline completions, agents, customization, and admin controls—but packages access differently by subscription tier.

For individual use, the plans form a capability ladder:

- **Copilot Free** is the low-commitment entry point, with limited chat, capped completions, and a small premium request allowance.
- **Copilot Student** removes major productivity limits for verified students and adds stronger feature access at no cost.
- **Copilot Pro** is the baseline paid plan for professionals who need unlimited completions and premium model access.
- **Copilot Pro+** is for power users who need more premium requests and the broadest model access.

For managed environments, the emphasis shifts from individual productivity to rollout and control:

- **Copilot Business** adds centralized management and policy controls for organizations.
- **Copilot Enterprise** builds on Business with more enterprise-grade administration and higher premium request allowances.

A useful way to evaluate plans is by capability area:

**Chat and conversational workflows**  
Chat exists across plans, but message limits and model availability vary. Lower tiers constrain usage, while paid and managed plans generally support sustained daily use. This affects whether Copilot works as an occasional assistant or a full-time development companion.

**Code completion and inline suggestions**  
This is the clearest dividing line between casual and professional use. Free caps completions, while Student, Pro, Pro+, Business, and Enterprise allow unlimited completions.

**Agent features**  
GitHub’s newer agent-oriented features—cloud agent, agent mode, code review, MCP, and third-party agents—are unevenly distributed across plans. If autonomous or multi-step AI workflows matter, this should be checked explicitly rather than assumed.

**Customization and context control**  
Individuals get personal or repository-level customization, while managed plans extend control to the organization layer. That is important for standardizing prompts, exclusions, and behavior across teams.

**Admin and compliance operations**  
Business and Enterprise introduce policy management, audit logs, content exclusion, and seat administration. These features are essential when legal, security, and platform teams need oversight.

The notes also highlight several operational caveats:

- GitHub is shifting from request-based billing to usage-based billing starting **June 1, 2026**.
- Some plan sign-ups were temporarily paused beginning in **April 2026**, depending on the plan.
- Copilot enterprise offerings apply to **GitHub Enterprise Cloud**, not **GitHub Enterprise Server**.
- Feature availability can be platform-specific depending on IDE, review workflow, and model support.

A practical selection rule emerges:

- Choose **Free** for experimentation.
- Choose **Student** if eligible.
- Choose **Pro** for daily professional use.
- Choose **Pro+** for maximum model choice and larger premium request volume.
- Choose **Business** for centralized team rollout and policy control.
- Choose **Enterprise** for enterprise-scale administration and governance.

## Test Yourself

<details><summary>What is the main distinction between individual and managed Copilot plans?</summary>

Individual plans primarily scale usage limits, premium-request capacity, and model access. Managed Business and Enterprise plans add centralized rollout, policy, auditing, exclusion, and seat-management capabilities.

</details>

<details><summary>When is Copilot Pro+ a better fit than Copilot Pro?</summary>

Pro+ is intended for power users who need a larger premium-request allowance and the broadest available model choice. Pro is the baseline paid option for sustained professional use with unlimited completions.

</details>

<details><summary>What should an organization verify before selecting a plan for agentic workflows?</summary>

It should confirm that the plan and intended IDE or platform support the required features, including cloud agent, agent mode, code review, MCP, and third-party agents. These capabilities should not be assumed to be available uniformly across tiers or clients.

</details>

## Personal Notes

Choosing the Right GitHub Copilot Plan: Features, Limits, and Admin Tradeoffs

Source: https://docs.github.com/en/copilot/get-started/plans?utm_source=chatgpt.com
Notion page: https://www.notion.so/Choosing-the-Right-GitHub-Copilot-Plan-Features-Limits-and-Admin-Tradeoffs-35e01bb0839a81738f55e84cbf15a98a

Tags: github, copilot, pricing, enterprise, developer-tools

Overview

GitHub Copilot is offered through several plans aimed at different audiences: individuals trying the product, students, professional developers, teams, and enterprises. The plans differ not just in price, but in model access, request quotas, completion limits, agent capabilities, policy controls, and administrative features.

For engineers and engineering managers, understanding these differences matters because plan selection affects both day-to-day developer experience and organizational governance. A solo developer may optimize for model access and completion volume, while a platform team or security-conscious enterprise will care more about centralized policy, auditability, content exclusion, and seat management.

Key Concepts

  *   Plan segmentation: GitHub splits Copilot offerings into individual plans (Free, Student, Pro, Pro+) and organization or enterprise plans (Business, Enterprise). The segmentation reflects different needs: low-cost experimentation for individuals, richer model access for power users, and centralized controls for managed environments.
  *   Premium requests: Several advanced Copilot capabilities are governed by monthly premium request allowances. The included quota varies significantly by plan, from 50 per month on Free to 1500 on Pro+ and 1000 per user on Enterprise, with some paid plans allowing additional requests to be purchased.
  *   Included models vs premium models: Not all plans expose the same set of AI models in Copilot Chat. Higher-tier plans, especially Pro+ and Enterprise, provide broader access to premium and advanced models, while lower tiers may offer limited access, auto-selection only, or reduced message counts.
  *   Agent capabilities: Copilot increasingly includes agent-oriented features such as cloud agent, agent mode, code review, MCP, and third-party agents. These are not universally available across plans, so teams evaluating AI-assisted workflows should map required agent features to the correct subscription tier.
  *   Governance and policy control: Business and Enterprise plans add administrative controls that matter in managed environments. These include organization-wide policy management, custom instructions at the org level, content exclusion, audit logs, and controls such as blocking suggestions matching public code.
  *   IDE and platform availability: Many Copilot features are cross-tool but not universally supported in every interface. Chat, inline suggestions, review workflows, and model-specific features vary by IDE or client, such as VS Code, Visual Studio, JetBrains IDEs, Xcode, Eclipse, GitHub Mobile, and Windows Terminal.

How It Works

At a high level, the GitHub Copilot plan matrix is a packaging model around a shared set of AI coding features. GitHub exposes a common capability surface—chat, inline suggestions, agents, customization, and admin controls—but gates access based on user type and subscription level.

For **individual users**, the progression is:

- **Copilot Free**: entry point with limited access - 50 premium requests/month - 2,000 completions/month - 50 chat messages/month in IDEs - limited review capability in VS Code (`Review selection` only) - **Copilot Student**: free for verified students, but materially more capable than Free - unlimited completions - premium model access in Copilot Chat - cloud agent access - 300 premium requests/month - **Copilot Pro**: paid individual plan for regular professional use - unlimited completions - premium model access in chat - cloud agent - 300 premium requests/month - **Copilot Pro+**: power-user individual plan - everything in Pro - larger premium request pool: 1500/month - full access to all available chat models

For **organizations and enterprises**, GitHub shifts the focus from individual productivity to managed deployment:

- **Copilot Business** - intended for organizations on GitHub Free or Team, and enterprises on Enterprise Cloud - includes cloud agent - adds centralized management and policy control - 300 premium requests per user per month - **Copilot Enterprise** - available for enterprises on GitHub Enterprise Cloud - includes all Business capabilities plus additional enterprise-grade features - 1000 premium requests per user per month - enterprise owners can assign Enterprise or Business at organization scope, or Business directly to users and teams

The functional comparison is easiest to understand by capability area.

**1. Chat and conversational workflows**

Copilot Chat is available across plans, but the volume and model set differ. Free users get a small monthly message budget in IDEs, while paid and managed tiers get effectively unlimited chat with included models. Higher tiers also expose more
