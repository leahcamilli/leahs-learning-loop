---
title: "Building an LLM-Maintained Wiki for Compounding Knowledge"
source: "https://open.substack.com/pub/nandigamharikrishna/p/andrej-karpathys-llm-wiki-full-breakdown?r=7692ad"
date: "2026-05-08"
tags: [llm, knowledge-management, rag, obsidian, markdown]
source_type: "web"
topics: [rag-and-retrieval, knowledge-management, ai-agents]
kind: "deep-dive"
depth: 2
actionability: 2
---

## TL;DR

> An LLM-maintained wiki turns raw sources and useful answers into a persistent, linked knowledge base instead of rebuilding understanding for every query. Its value compounds when immutable sources, schema-driven workflows, and regular maintenance keep the synthesis traceable and consistent.

## Key Takeaways

1. Compile source material into curated, cross-referenced markdown pages so future queries reuse prior synthesis rather than repeatedly processing raw chunks.
2. Separate the system into three layers: immutable files in `raw/`, LLM-maintained pages in `wiki/`, and a schema file such as `CLAUDE.md` or `AGENTS.md` that governs maintenance.
3. Define naming, frontmatter, linking, contradiction handling, page-creation criteria, and ingest/query/lint workflows in the schema file to reduce drift between sessions.
4. Start queries at `wiki/index.md`, open only the relevant pages, and save valuable answers under `wiki/queries/` so recurring questions become durable assets.
5. Run lint passes to find orphan pages, stale or contradictory claims, missing links, under-sourced areas, and frequently referenced topics that deserve dedicated pages.
6. Use the pattern when long-term synthesis and contradiction tracking matter; favor conventional retrieval when the corpus is extremely large and fast lookup is the main requirement.
7. Test the architecture with three source documents, one schema file, one saved query, one lint pass, and Git commits after each ingest.

## Overview

These notes describe the **LLM Wiki** pattern popularized by Andrej Karpathy: a file-based, LLM-maintained knowledge base that sits between raw source material and future questions. Instead of relying on standard RAG to retrieve raw chunks at query time, the system continuously compiles source material into linked markdown pages, updates concepts and entities over time, tracks contradictions, and saves valuable answers back into the wiki.

This matters because it shifts knowledge work from one-off retrieval to **compounding synthesis**. For engineers, researchers, and technical teams working over long time horizons, the pattern offers a practical architecture built around immutable sources, a generated wiki, and a schema file that makes maintenance behavior consistent and repeatable.

## Key Concepts

- **Compiled knowledge vs retrieval**: Traditional RAG retrieves raw source fragments at query time and synthesizes answers on demand. The LLM Wiki compiles knowledge ahead of time into structured pages, so later queries operate on curated, cross-referenced summaries rather than rediscovering facts from scratch.
- **Three-layer architecture**: The system is split into immutable raw sources, an LLM-written wiki, and a schema file that defines maintenance behavior. This preserves source fidelity, gives the LLM a persistent artifact to improve, and makes workflows more repeatable.
- **Schema-driven maintenance**: A schema file such as `CLAUDE.md` or `AGENTS.md` tells the LLM how to name files, structure frontmatter, update indexes, handle contradictions, and follow ingest/query/lint workflows. Without this, the wiki tends to drift across sessions.
- **Ingest, query, lint**: The core operating loop consists of ingesting new sources, answering questions from the compiled wiki, and linting the wiki for consistency issues such as stale claims, orphan pages, and missing links.
- **Index-first navigation**: Queries typically begin with `wiki/index.md`, which acts as an explicit navigation layer. This keeps the system understandable and often avoids the need for full-text or vector search at moderate scales.
- **Compounding artifact**: Each newly ingested source and each saved answer improves the wiki for future work. Over time, concept pages deepen, recurring questions become durable assets, and contradictions become visible instead of staying hidden in chat history.

## How It Works

At a high level, the LLM Wiki replaces a **search-centric** workflow with a **maintenance-centric** one. In standard RAG, documents are chunked, embedded, and searched when a user asks a question. In this pattern, the LLM processes sources earlier and writes persistent syntheses into markdown files on disk. The result is a knowledge base that can evolve incrementally rather than rebuilding context from scratch every time.

The notes describe a **three-layer design**:

1. **`raw/`**: immutable source documents such as articles, papers, transcripts, or images  
2. **`wiki/`**: markdown pages generated and maintained by the LLM  
3. **Schema file**: a control document like `CLAUDE.md` that defines conventions and workflows  

A minimal layout looks like this:

```text
your-wiki/
├── CLAUDE.md
├── raw/
│   ├── articles/
│   ├── papers/
│   └── assets/
└── wiki/
    ├── index.md
    ├── log.md
    ├── overview/
    ├── entities/
    ├── concepts/
    ├── sources/
    └── queries/
```

The **raw layer** should be treated as write-protected from the LLM’s perspective. That separation preserves source integrity and makes it easy to verify whether the wiki faithfully represents a claim. The **wiki layer** then becomes the working knowledge graph, containing source summaries, entity pages, concept pages, overviews, saved query answers, an index, and an append-only log.

The **schema file** is what makes the pattern operational rather than ad hoc. It usually defines:

- directory semantics
- YAML frontmatter requirements
- file naming conventions
- internal link syntax such as `[[page-name]]`
- contradiction handling rules
- criteria for when to create a new page
- exact ingest, query, and lint workflows

A representative ingest workflow is:

1. Read the raw source file  
2. Ask for emphasis or framing notes  
3. Create a source summary page  
4. Update relevant entity and concept pages  
5. Update overview synthesis if needed  
6. Update `wiki/index.md`  
7. Append to `wiki/log.md`  

### Ingest flow

Ingest is the main entry point for new knowledge. A source is read, summarized, and integrated into multiple existing pages. This is a key difference from RAG: the source becomes not just retrievable, but **structurally incorporated** into a growing graph of knowledge.

A single paper or article may update several files at once, for example:

- `wiki/sources/<paper>-summary.md`
- `wiki/concepts/speculative-decoding.md`
- `wiki/concepts/inference-optimization.md`
- `wiki/entities/<author>.md`
- `wiki/overview/synthesis.md`
- `wiki/index.md`
- `wiki/log.md`

### Query flow

Queries run against the compiled wiki, not directly against the raw corpus. The agent usually reads `wiki/index.md`, selects relevant pages, opens a small subset, and synthesizes an answer with references to internal wiki pages. If the answer is worth keeping, it is saved under `wiki/queries/`.

This makes answers reusable. A question like “When should I use RAG vs an LLM Wiki?” can become a permanent page that other concept pages link to later.

### Lint flow

Lint is the maintenance pass that improves consistency and integrity. Instead of adding new knowledge, it checks the wiki for structural and semantic issues such as:

- orphan pages with no inbound links
- contradictions between pages or with newer source summaries
- stale or superseded claims
- heavily referenced topics missing dedicated pages
- under-sourced areas needing more evidence

This makes the wiki behave more like a codebase: regular refactoring improves quality over time.

### Why the pattern works

The central idea is that the LLM should act less like a search engine and more like a maintainer of a persistent artifact. Obsidian serves as the reader or IDE, the LLM behaves like the programmer, and the wiki becomes the codebase. The value comes from stable files, repeatable conventions, explicit links, version history, and incremental improvement.

The pattern works especially well when:

- the domain matters over time
- the corpus is limited enough to curate
- cross-source synthesis matters
- contradictions need to be tracked
- improving future answers is more important than one-time retrieval

It is weaker when:

- the corpus is extremely large and mainly lookup-oriented
- low-latency search across thousands of documents is the priority
- hallucination risk requires heavy review
- the team will not maintain ingest discipline

The notes also include a practical exercise: build a small wiki on a known technical topic using three source documents, one schema file, one query, and one lint pass. This makes the “wiki as codebase” analogy concrete, especially when paired with Git commits after each ingest.

## Test Yourself

<details><summary>How does an LLM Wiki differ from standard RAG?</summary>

Standard RAG retrieves raw fragments and synthesizes an answer at query time. An LLM Wiki compiles sources earlier into persistent, linked pages, allowing later questions to reuse and improve accumulated synthesis.

</details>

<details><summary>What roles do the three architectural layers play?</summary>

The `raw/` layer preserves immutable source evidence, the `wiki/` layer holds evolving summaries and relationships, and the schema file defines the conventions and workflows the LLM must follow.

</details>

<details><summary>Why are ingest, query, and lint all necessary?</summary>

Ingest integrates new material, query turns compiled knowledge into reusable answers, and lint repairs structural or semantic problems. Together they let the wiki accumulate knowledge without silently accumulating disorder.

</details>

## Personal Notes

Building an LLM-Maintained Wiki for Compounding Knowledge

Source: https://open.substack.com/pub/nandigamharikrishna/p/andrej-karpathys-llm-wiki-full-breakdown?r=7692ad&utm_medium=ios
Notion page: https://www.notion.so/Building-an-LLM-Maintained-Wiki-for-Compounding-Knowledge-35a01bb0839a81debcaff967d9d4d2c1

Tags: llm, knowledge-management, rag, obsidian, markdown

Overview

This lesson explains the LLM Wiki pattern popularized by Andrej Karpathy: a file-based, LLM-maintained knowledge base that sits between your raw sources and your future questions. Instead of retrieving raw chunks at query time like standard RAG systems, the LLM continuously compiles sources into linked markdown pages, updates concepts and entities over time, flags contradictions, and files useful answers back into the wiki.

The pattern matters for engineers, researchers, and technical teams who care about long-horizon learning rather than one-off document lookup. If you routinely read papers, design docs, transcripts, or internal notes and need synthesis that compounds over weeks or months, this approach gives you a practical architecture: immutable raw sources, a generated wiki, and a schema file that enforces consistent behavior across sessions.

Key Concepts

  *   Compiled knowledge vs retrieval: Traditional RAG retrieves raw source fragments at query time and synthesizes answers on demand. The LLM Wiki instead compiles knowledge ahead of time into structured pages, so later queries operate on curated, cross-referenced summaries rather than rediscovering facts from scratch.
  *   Three-layer architecture: The system is organized into immutable raw sources, an LLM-written wiki, and a schema file that defines maintenance behavior. This separation preserves source fidelity, gives the LLM a persistent artifact to improve, and makes behavior repeatable across sessions.
  *   Schema-driven maintenance: A schema file such as `CLAUDE.md` or `AGENTS.md` tells the LLM how to name files, structure frontmatter, update indexes, handle contradictions, and perform workflows. Without this, the wiki drifts and each session behaves like a fresh chat instead of a disciplined maintenance pass.
  *   Ingest, query, lint: The pattern revolves around three core operations
