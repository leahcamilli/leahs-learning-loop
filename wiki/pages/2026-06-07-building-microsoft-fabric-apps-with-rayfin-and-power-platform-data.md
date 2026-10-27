---
title: "Building Microsoft Fabric Apps with Rayfin and Power Platform Data"
source: "https://www.linkedin.com/posts/andreasadner_rayfin-microsoftfabric-powerplatform-ugcPost-7469457251976577024-p4-N/?utm_source=share&utm_medium=member_ios&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY"
date: "2026-06-07"
tags: [rayfin, microsoft-fabric, power-platform, onelake, semantic-models]
source_type: "web"
topics: []
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> The source presents Rayfin as an open-source SDK and CLI for building managed applications directly in Microsoft Fabric. The pattern matters because it connects operational input, governed data, shared business definitions, and application delivery within one platform.

## Key Takeaways

1. Use Power Apps to capture operational data, Link to Fabric to connect it, OneLake to centralize it, a semantic model to govern it, and Rayfin to deliver the user-facing app.
2. Put a semantic model between the application and raw storage so business entities, relationships, measures, naming conventions, and access patterns remain consistent.
3. Treat Rayfin as the application layer close to Fabric’s governed data assets rather than as a standalone web app with a separately assembled backend and infrastructure stack.
4. Combine low-code and pro-code components: Power Apps handles data entry, Fabric manages data and governance, and Rayfin provides the managed application experience.
5. Apply this architecture to operational scenarios such as equipment maintenance, room reservations, field inspections, project tracking, or asset control.
6. Treat the sample Rayfin CLI commands as illustrative lifecycle steps—not confirmed syntax—for initializing, connecting, binding a semantic model, and deploying an app.

## Overview

This lesson explains the core idea behind Microsoft Rayfin as presented in the source: an open-source SDK and CLI for quickly building fully managed, enterprise-grade applications that run directly in Microsoft Fabric. The example scenario connects a Power App to Fabric through Link to Fabric, stores and organizes data in OneLake, exposes it through a semantic model, and then uses a Rayfin app as the user-facing experience.

This matters to engineers and solution architects working on internal business apps, analytics-driven operational tools, or low-code/data-platform integrations. The interesting shift is that app development is no longer isolated from the data platform: Rayfin suggests a pattern where app UI, governed data, and Fabric-native deployment come together in one managed environment.

## Key Concepts

- **Rayfin**: Rayfin is described as an open-source SDK and CLI for building apps that run directly in Microsoft Fabric. Its value proposition is speed, managed deployment, and enterprise readiness, which suggests developers can create applications without assembling a large amount of hosting and infrastructure plumbing themselves.
- **Microsoft Fabric-native apps**: A Fabric-native app runs in the same broader platform where data storage, transformation, analytics, and governance already exist. This reduces friction between app logic and analytics assets, and can simplify security, deployment, and operational management.
- **OneLake**: OneLake is Microsoft Fabric's unified data lake layer. In the scenario from the post, application data ultimately lands in OneLake, making it available for downstream modeling and consumption by both analytics and operational-facing applications.
- **Semantic model**: A semantic model provides a curated, business-friendly representation of underlying data. Instead of querying raw tables directly, applications and reports can rely on a governed model with consistent metrics, dimensions, and relationships.
- **Power Apps and Link to Fabric**: Power Apps can act as the operational front end for entering and managing business data. Link to Fabric connects that operational data into Fabric so it can be stored, analyzed, modeled, and then surfaced again through other experiences such as Rayfin apps.
- **Managed enterprise app delivery**: The post emphasizes that Rayfin apps are fully managed and enterprise-grade. Practically, this implies a focus on governance, repeatable deployment, integration with Fabric assets, and a developer workflow that is more standardized than building a custom app stack from scratch.

## How It Works

The source describes a simple but important architecture pattern:

1. **Operational data is created in Power Apps**.
2. **That data is connected into Microsoft Fabric using Link to Fabric**.
3. **Fabric stores or exposes the data through OneLake**.
4. **A semantic model is built on top of the OneLake-backed data**.
5. **A Rayfin app reads from that semantic model and provides the application experience**.

This is notable because the application is not presented as a standalone web app with a separate backend and custom data-access tier. Instead, the app is positioned as a Fabric-native experience, where the data platform is already the system of record for analytics and governance.

### End-to-end flow

The post's demo uses a "space program" management app as the example. Even though the domain is playful, the architecture maps well to real business scenarios such as inventory management, project tracking, service operations, or asset control.

- A **Power App** captures data changes from users.
- **Link to Fabric** moves or mirrors that data into the Fabric environment.
- **OneLake** acts as the centralized storage layer.
- A **semantic model** organizes the data into something consumable by business users and applications.
- **Rayfin** uses that semantic layer to create an app quickly.

### Why the semantic model matters

Using a semantic model in the middle is a strong architectural signal. Rather than binding the app directly to raw storage, the app can consume a curated layer that defines:

- business entities
- relationships
- calculations and measures
- naming conventions
- governed access patterns

That makes the app more resilient to physical data changes and better aligned with the same definitions used in reports and dashboards.

### What Rayfin likely contributes

The post does not include implementation details, but from the description we can infer the main developer workflow:

- install the **Rayfin CLI**
- initialize a new app project
- connect the app to Fabric resources
- bind views or components to a semantic model
- deploy into Fabric as a managed app

The key idea is acceleration. Instead of setting up hosting, authentication layers, custom APIs, deployment pipelines, and environment plumbing independently, Rayfin appears to package these concerns into a Fabric-aware app model.

### Reasoning behind this pattern

This pattern is attractive in enterprise environments because it unifies app development and analytics governance:

- **Data lives where the platform already governs it**.
- **Apps consume shared business definitions** via semantic models.
- **Operational and analytical workflows converge** rather than being duplicated.
- **Low-code and pro-code assets can cooperate**: Power Apps for capture, Fabric for data, Rayfin for app experiences.

### Mental model for engineers

Think of Rayfin as an app layer sitting close to Fabric's governed data assets. In a traditional architecture, you might build:

- a frontend
- a backend API
- a database
- ETL pipelines
- a BI model

In the pattern described here, Fabric already provides much of the data and governance foundation, and Rayfin reduces the amount of custom application scaffolding needed to turn that foundation into a usable managed app.

## Training Exercise

Build a small architecture blueprint for a Fabric-native operational app using the pattern from the post.

### Goal

Design a lightweight app where business users submit and review records in Power Apps, and a Rayfin app later consumes the same data through a semantic model in Fabric.

### Steps

1. **Pick a simple business domain**
   Choose one of these examples:
   - equipment maintenance requests
   - office room reservations
   - field inspection tracking
   - launch mission tracking, inspired by the post

2. **Define the operational data**
   Write down 2-3 entities and their fields. Example:
   - `Mission`
     - `MissionId`
     - `MissionName`
     - `LaunchDate`
     - `Status`
   - `Spacecraft`
     - `SpacecraftId`
     - `Name`
     - `Type`
   - `MissionAssignment`
     - `MissionId`
     - `SpacecraftId`

3. **Map the platform flow**
   Create a short design note describing:
   - what users edit in **Power Apps**
   - how data reaches **Fabric via Link to Fabric**
   - where it lands in **OneLake**
   - what the **semantic model** exposes
   - what screens the **Rayfin app** would need

4. **Draft the semantic model**
   Define:
   - dimensions and fact-like tables
   - one or two measures

   Example:
   ```text
   Tables:
   - DimMission
   - DimSpacecraft
   - FactMissionAssignment

   Measures:
   - Total Missions = COUNTROWS(DimMission)
   - Active Missions = CALCULATE(COUNTROWS(DimMission), DimMission[Status] = "Active")
   ```

5. **Describe the Rayfin app experience**
   Write a one-page spec for three screens:
   - overview dashboard
   - mission detail page
   - status summary page

   For each screen, specify:
   - which semantic model entities it uses
   - what filters it supports
   - what actions a user can take

6. **Optional CLI practice**
   Since the source references an SDK and CLI, sketch the commands you would expect in a project workflow:
   ```bash
   rayfin init mission-control
   cd mission-control
   rayfin connect fabric
   rayfin bind semantic-model mission-analytics
   rayfin deploy
   ```
   These commands are illustrative, not confirmed syntax. The point is to think through the lifecycle: initialize, connect, bind data, deploy.

### Deliverable

Produce a short design document with:
- the entity model
- the data flow diagram
- the semantic model definition
- the Rayfin screen list
- 2-3 reasons why this architecture is preferable to a standalone custom app for your scenario

## Test Yourself

<details><summary>What is the end-to-end data and application flow described in the lesson?</summary>

Users create or update data in Power Apps, Link to Fabric connects it to Fabric, and OneLake provides the centralized data layer. A semantic model organizes the data, and a Rayfin app consumes that model to provide the application experience.

</details>

<details><summary>Why should a Rayfin app consume a semantic model instead of querying raw tables directly?</summary>

The semantic model supplies governed business entities, relationships, calculations, naming conventions, and access patterns. This can make the app more resilient to storage changes and keep its definitions aligned with reports and dashboards.

</details>

<details><summary>What developer burden does the source claim Rayfin can reduce?</summary>

The source presents Rayfin as reducing custom scaffolding for hosting, authentication, APIs, deployment, and environment setup. It does so by packaging application delivery into a managed, Fabric-aware SDK and CLI workflow.

</details>

## Further Reading

- [Introducing Rayfin: A new AI-first way to build, deploy, and govern apps in Microsoft Fabric](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Introducing-Rayfin-A-new-AI-first-way-to-build-deploy-and-govern/ba-p/5191676)
- [Microsoft Fabric documentation](https://learn.microsoft.com/fabric/)
- [OneLake in Microsoft Fabric](https://learn.microsoft.com/fabric/onelake/)
- [Power Apps documentation](https://learn.microsoft.com/power-apps/)
- [Power BI semantic models documentation](https://learn.microsoft.com/power-bi/connect-data/service-datasets-understand)
