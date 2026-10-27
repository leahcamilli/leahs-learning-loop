---
title: "Using Built-In Mermaid Diagram Support in Visual Studio Code"
source: "https://www.linkedin.com/posts/mermaid-diagrams-are-now-built-directly-into-ugcPost-7470236547636760576-tAgO/?utm_source=share&utm_medium=member_ios&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY"
date: "2026-06-09"
tags: [vscode, mermaid, diagrams, markdown, documentation]
source_type: "web"
topics: [developer-tools]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> VS Code’s built-in Mermaid support lets teams create and preview diagrams as text inside Markdown without a separate extension. Keeping diagram sources beside code makes architecture and process documentation easier to version, review, and update.

## Key Takeaways

1. Embed a diagram in Markdown by placing valid Mermaid syntax inside a fenced code block labeled `mermaid`, then open VS Code’s Markdown preview.
2. Treat Mermaid text—not an exported image—as the source of truth so diagram changes remain editable, diffable, and reviewable.
3. Update Mermaid diagrams in the same pull request as related implementation changes to reduce stale documentation.
4. Use flowcharts for processes and architecture, sequence diagrams for component interactions, and state diagrams for entity lifecycles.
5. Keep diagrams small and focused; split large documentation when complexity makes a diagram difficult to understand or maintain.
6. Use the short edit-and-preview loop to refine diagram structure, labels, and layout without switching to a separate drawing tool.

## Overview

Visual Studio Code now includes Mermaid diagram support directly in the editor, removing the need for a separate extension in common documentation workflows. That matters because Mermaid lets engineers define diagrams as text, store them in source control, review them in pull requests, and keep architecture or process documentation close to the code it describes.

This is especially useful for developers, technical writers, platform engineers, and team leads who maintain README files, design docs, runbooks, or system documentation in Markdown. Built-in support lowers setup friction and makes diagram-as-code a more natural part of everyday editing in VS Code.

## Key Concepts

- **Diagram as code**: Mermaid uses a plain-text syntax to describe diagrams such as flowcharts, sequence diagrams, and state diagrams. Because the source is text, it can be versioned, diffed, reviewed, and edited with the same tooling used for code and documentation.
- **Built-in editor support**: When support is built into VS Code, users no longer need to discover, install, and maintain a separate extension just to preview Mermaid content. This reduces onboarding time and avoids extension compatibility or maintenance issues.
- **Markdown integration**: Mermaid is commonly embedded inside fenced code blocks in Markdown documents using the language tag `mermaid`. This allows architecture diagrams and workflow visuals to live directly inside README files, design documents, or wiki-style content.
- **Live preview workflow**: A core benefit of editor integration is the ability to edit diagram source and immediately preview the rendered result. This short feedback loop makes it easier to iterate on structure, labels, and layout without leaving the editor.
- **Docs in source control**: Keeping Mermaid definitions in the repository means diagrams evolve alongside the codebase and can be updated in the same pull request as the implementation. This helps reduce the common problem of architecture diagrams becoming stale.

## How It Works

The core idea is simple: Mermaid turns structured text into diagrams, and VS Code now understands that content natively enough to make the workflow feel first-class. In practice, engineers usually write Mermaid inside Markdown fenced code blocks like this:

```md
# Service Flow

```mermaid
flowchart TD
    A[Client] --> B[API Gateway]
    B --> C[Auth Service]
    B --> D[Orders Service]
    D --> E[(Database)]
```
```

With built-in support, the typical editing loop is:

1. Create or open a Markdown file.
2. Add a fenced code block labeled `mermaid`.
3. Write the diagram definition in Mermaid syntax.
4. Open Markdown preview in VS Code to render the diagram.
5. Edit the text until the diagram communicates the intended structure clearly.

This matters because it collapses what used to be a multi-tool process into a single environment. Instead of switching to a separate drawing application, exporting images, and committing binary assets, you define the diagram directly in the document. That improves maintainability and makes documentation changes easier to review in diffs.

A practical way to think about Mermaid support in VS Code is as part of the Markdown rendering pipeline. Markdown provides the document structure, fenced code blocks carry the Mermaid source, and the preview layer renders the diagram for human consumption. The source of truth remains the Mermaid text, not a generated image.

Common use cases include:

- **Architecture diagrams** for services, databases, and external systems
- **Sequence diagrams** for request flows across components
- **State diagrams** for lifecycle-heavy entities
- **Flowcharts** for deployment, approval, or operational processes
- **Onboarding docs** where visual explanation helps new team members understand a system quickly

The biggest engineering advantage is that diagrams become reviewable artifacts. A pull request can show that a new service was added to a flowchart or that an interaction path changed in a sequence diagram. Reviewers can inspect the exact textual change, which is much harder with screenshots or manually drawn diagrams.

There are still some practical considerations. Mermaid syntax is expressive but specific, so correctness depends on writing valid definitions. Teams should also treat diagrams like code: keep them small and focused, split large docs when needed, and update them as part of feature or architecture changes.

## Training Exercise

Create a small Markdown design note in VS Code that uses built-in Mermaid support to document a service flow.

### Goal
Produce a `design.md` file containing a Mermaid diagram and view it in the Markdown preview.

### Steps
1. Open VS Code.
2. Create a new folder for the exercise.
3. Add a file named `design.md`.
4. Paste the following content:

```md
# Order Processing Overview

This document describes the high-level request flow.

```mermaid
flowchart LR
    U[User] --> W[Web App]
    W --> A[API]
    A --> AU[Auth Service]
    A --> O[Order Service]
    O --> DB[(Orders DB)]
    O --> Q[Event Queue]
    Q --> N[Notification Worker]
```
```

5. Open the Markdown preview in VS Code.
6. Confirm that the diagram renders without installing an extension.
7. Modify the diagram to add a `Payment Service` between `Order Service` and `Orders DB`.
8. Add a second Mermaid block using a sequence diagram:

```md
```mermaid
sequenceDiagram
    participant User
    participant WebApp
    participant API
    participant Orders
    User->>WebApp: Submit order
    WebApp->>API: POST /orders
    API->>Orders: Create order
    Orders-->>API: Order ID
    API-->>WebApp: 201 Created
```
```

### What to observe
- How quickly you can iterate by changing text and re-opening preview
- How easy it is to keep diagrams next to explanatory prose
- How the diagram source would appear in a code review

### Stretch task
Commit the file to a Git repository and make one follow-up change to the diagram. Inspect the diff to see how diagram changes are represented in source control.

## Test Yourself

<details><summary>Why is Mermaid’s text-based format useful for engineering documentation?</summary>

Its source can be stored, diffed, and reviewed with the same version-control workflow used for code. This also lets teams update a diagram alongside the implementation it describes.

</details>

<details><summary>How do you create and view a Mermaid diagram in VS Code according to the lesson?</summary>

Add Mermaid syntax to a Markdown fenced code block labeled `mermaid`, then open the Markdown preview. Edit the source and refresh or reopen the preview until the diagram communicates the intended structure.

</details>

<details><summary>What practices help prevent Mermaid documentation from becoming stale or unwieldy?</summary>

Teams should update diagrams as part of relevant feature or architecture changes, preferably in the same pull request. They should also keep diagrams focused and split overly large documents or diagrams when needed.

</details>

## Further Reading

- [Mermaid Official Documentation](https://mermaid.js.org/)
- [Visual Studio Code Documentation](https://code.visualstudio.com/docs)
- [Markdown in Visual Studio Code](https://code.visualstudio.com/docs/languages/markdown)
- [Mermaid Syntax Reference](https://mermaid.js.org/intro/syntax-reference.html)
