---
title: "Karpathy’s LLM Wiki: Persistent Knowledge Files vs Basic RAG"
source: "https://www.youtube.com/watch?v=aGXTV5MTqDY"
date: "2026-05-08"
tags: [llm, rag, context-engineering, knowledge-management, agents]
source_type: "youtube"
channel: "AI Simplified"
published: "2026-04-04"
duration_seconds: 319
topics: [context-engineering, rag-and-retrieval, ai-agents, prompt-engineering]
kind: "deep-dive"
depth: 2
actionability: 2
---

## TL;DR

> An “LLM wiki” gives an agent persistent, inspectable memory through curated text files, improving the quality and continuity of the context it receives. It works best alongside RAG: the wiki supplies durable, high-signal knowledge, while retrieval handles long-tail lookup across raw sources.

## Key Takeaways

1. Treat model memory as maintained documentation: ingest source material, distill it into stable pages, load the relevant pages for each task, and write back reviewed updates.
2. Use explicit files such as indexes, project summaries, concept pages, decision records, entity profiles, and periodic summaries to preserve knowledge across sessions.
3. Prefer canonical summaries over isolated retrieved chunks when the model needs stable explanations, constraints, risks, or decision rationale.
4. Keep memory human-auditable by storing it in readable, editable, and versionable text or markdown files.
5. Review model-proposed write-backs because summarization can omit details, introduce errors, or allow stale knowledge to persist.
6. Combine a wiki for durable, high-signal memory with RAG for broad recall and long-tail lookup in large or rapidly changing document collections.

## Overview

These notes describe the idea of an “LLM wiki”: a persistent, curated set of text or markdown files that acts as an external memory system for an LLM or agent. Instead of relying only on vector search over raw document chunks, the system maintains readable knowledge files such as topic summaries, decision logs, indexes, and periodic updates. This makes the model’s working knowledge more explicit, inspectable, and stable over time.

The main value of this approach is better context management. Many LLM systems underperform not because the model is weak, but because the right information is not presented clearly at the right time. An LLM wiki shifts the design toward human-auditable context engineering, durable memory, and compact summaries. It is especially useful for coding agents, research assistants, and internal tools that need continuity, transparency, and controllable write-back memory.

## Key Concepts

- **LLM wiki**: A collection of structured text documents used as external memory for a model or agent.
- **RAG versus explicit context files**: Traditional RAG relies on similarity-based retrieval from chunked documents, while a wiki emphasizes curated, organized, human-readable files.
- **Persistent memory**: Useful facts, decisions, and summaries are preserved across sessions instead of being lost after a single prompt.
- **Context engineering**: The practice of choosing what information the model sees, in what format, and in what sequence.
- **Human-auditable knowledge**: Because the memory is stored in normal files, engineers can inspect, edit, review, and version it directly.
- **Knowledge compression**: A wiki works best when it distills noisy source material into concise summaries, indexes, and canonical pages.

## How It Works

The core idea is to treat LLM memory like a maintained documentation set rather than a passive retrieval layer. Source material such as notes, transcripts, code docs, and chat logs is ingested and then distilled into durable files. These files can include project summaries, concept pages, decision records, people or entity profiles, and periodic log summaries. When the model performs a task, the system loads a selected subset of these files into context instead of depending only on nearest-neighbor retrieval over raw chunks.

A common workflow is:

1. Ingest source material.
2. Distill it into stable pages.
3. Load the relevant subset for a task.
4. Optionally write back new facts, summaries, or decisions after the task completes.

This differs from naive RAG in several important ways. First, the structure is explicit: a file path can carry meaning, such as a project page versus a decision log. Second, important information is curated into high-signal summaries rather than retrieved as isolated fragments. Third, memory becomes more stable because canonical pages reduce duplication and drift.

A typical layout might look like this:

```text
wiki/
  index.md
  projects/
    payments-service.md
    search-migration.md
  concepts/
    vector-search.md
    prompt-caching.md
  people/
    team-roles.md
  decisions/
    2026-03-auth-refactor.md
  logs/
    weekly-summary-2026-05-01.md
```

Each file has a different job. `index.md` provides a map of the knowledge base. Topic pages summarize systems, constraints, and risks. Decision logs preserve rationale. Periodic summaries compress long-running activity into reusable memory. This improves context quality because the model is given synthesized, structured explanations instead of arbitrary retrieved chunks.

A major advantage is write-back memory. After completing a task, the model can propose updates such as:

- appending a new decision record
- refreshing a project summary
- extracting unresolved questions
- updating an entity page with confirmed facts

Because the memory lives in text files, this write-back loop is simple to inspect and review. Human oversight is still important, especially because summarization can be lossy or wrong.

There are trade-offs. A wiki requires maintenance and can become stale if not curated. It may not replace RAG for very large or rapidly changing corpora where broad recall is important. In practice, the strongest setup is often hybrid:

- wiki for durable, high-signal memory
- RAG for long-tail lookup into raw documents

That combination gives the model a reliable mental map while still allowing deep retrieval when needed.

## Test Yourself

<details><summary>How does an LLM wiki differ from basic RAG?</summary>

Basic RAG typically retrieves similar chunks from raw documents, while an LLM wiki supplies curated, structured, human-readable knowledge files. The wiki prioritizes stable summaries and explicit organization rather than relying only on nearest-neighbor retrieval.

</details>

<details><summary>What does the write-back loop add to an LLM wiki?</summary>

After a task, the model can propose durable updates such as a new decision record, a refreshed project summary, or a list of unresolved questions. Human review remains important because those updates may be incomplete or incorrect.

</details>

<details><summary>Why is a hybrid wiki-and-RAG system often preferable?</summary>

The wiki provides a reliable mental map of durable, high-signal knowledge, but it may not cover every detail or stay current without maintenance. RAG complements it by searching raw documents for long-tail details and rapidly changing information.

</details>

## Personal Notes

Karpathy’s LLM Wiki: Persistent Knowledge Files as an Alternative to Basic RAG

Source: https://youtu.be/aGXTV5MTqDY?si=pCQXA41R0Cpwxuh3
Notion page: https://www.notion.so/Karpathy-s-LLM-Wiki-Persistent-Knowledge-Files-as-an-Alternative-to-Basic-RAG-35a01bb0839a8183a72ee8807d2191ab

Tags: llm, rag, context-engineering, knowledge-management, agents

Overview

This lesson explains the idea behind an "LLM wiki": a curated, persistent set of text files that an AI system can read, update, and use as its working knowledge base. The concept is often framed as a simpler and more controllable alternative to naive retrieval-augmented generation (RAG), especially for personal knowledge, project memory, and agent workflows where the structure of information matters as much as retrieval quality.

Engineers should care because many production LLM systems fail not from model weakness, but from poor context management. An LLM wiki shifts the design focus from embedding-heavy retrieval pipelines toward explicit, human-readable knowledge artifacts: markdown files, indexes, summaries, and update flows. This can improve transparency, debuggability, and long-term memory for coding agents, research assistants, and internal tools.

Key Concepts

  *   LLM wiki: An LLM wiki is a collection of structured text documents that acts as external memory for a model or agent. Instead of treating knowledge as opaque vectors alone, the system keeps readable files that can be searched, summarized, edited, and versioned like normal documentation.
  *   RAG versus explicit context files: Traditional RAG stores chunks in a vector database and retrieves them by similarity at query time. An LLM wiki emphasizes explicit organization, curated summaries, and stable documents, which can make the model’s inputs easier to inspect and less dependent on embedding quality.
  *   Persistent memory: Persistent memory means the system can retain useful information across sessions rather than relying only on the current prompt window. In practice, this is implemented as files that are updated over time with facts, decisions, summaries, and links to source material.
  *   Context engineering: Context engineering is the discipline of deciding what information the model sees, in what format, and at what time. The wiki approach is a form of context engineering that prioritizes compact summaries, canonical references, and predictable document layouts.
  *   Human-auditable knowledge: Because the memory lives in normal text files, engineers can inspect and correct what the model knows. This improves trust and debugging compared with systems where knowledge is buried inside retrieval pipelines, embeddings, or undocumented prompt logic.
  *   Knowledge compression: A useful wiki is not just a dump of raw documents; it compresses information into summaries, indexes, and topic pages. This compression reduces token usage while preserving the most relevant facts and relationships for downstream tasks.

How It Works

The central idea is to treat knowledge for an LLM more like a maintained documentation set than like a passive search index. Instead of chunking every source document into embeddings and hoping similarity search returns the right passages, you build a small file hierarchy of markdown or text pages that summarize key topics, decisions, entities, and references. The LLM then reads from this wiki as part of its prompt context, and in some setups it can also propose updates back into the wiki.

At a high level, the workflow looks like this:

1. **Ingest source material** such as notes, code docs, meeting transcripts, research papers, or chat history. 2. **Distill the material** into durable pages: - topic summaries - entity pages - timeline or decision logs - indexes that point to deeper files 3. **Load the right subset** of those pages into the model depending on the task. 4. **Optionally update the wiki** after a task completes, preserving new findings or decisions.

This differs from basic RAG in a few important ways.

- **Structure is explicit.** The system knows that `projects/foo/decisions.md` contains architectural decisions, while `people/alice.md` contains background on a collaborator. - **Important information is curated.** The context is not merely nearest-neighbor retrieval over raw chunks; it is often a cleaned-up synthesis. - **The memory is stable over time.** A page can become the canonical place for a concept, reducing duplication and drift.

A practical LLM wiki often has a layout like:

```text wiki/ index.md projects/ payments-service.md search-migration.md concepts/ vector-search.md prompt-caching.md people/ team-roles.md decisions/ 2026-03-auth-refactor.md logs/ weekly-summary-2026-05-01.md ```

Each file serves a different context purpose:

- `index.md` gives the model a map of the knowledge base. - Topic pages provide concise summaries and key facts. - Decision logs preserve why something was done. - Periodic summaries compress long event streams into short, reusable memory.

The reason this can outperform naive RAG for many workflows is that retrieval quality alone does not solve context quality. If your source corpus is noisy, redundant, or overly granular, nearest-neighbor search may surface fragments without the surrounding reasoning. A wiki page can instead present the model with a synthesized explanation: what the system is, what changed
