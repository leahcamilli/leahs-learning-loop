---
title: "Graphify: Building a Personal LLM-Ready Wiki as a Knowledge Graph"
source: "https://youtu.be/zR5tyP4Onkc?si=br9ZvGFixmcb2xj7"
date: "2026-05-28"
tags: [llm, knowledge-graph, retrieval, personal-wiki, rag]
source_type: "youtube"
channel: "DevsKingdom"
published: "2026-04-13"
duration_seconds: 1013
topics: [rag-and-retrieval, knowledge-management]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> Turn isolated notes into connected entities with typed relationships, then combine semantic search with graph traversal. This gives LLMs more complete, precise, and explainable context than retrieving text chunks alone.

## Key Takeaways

1. Model important people, projects, concepts, papers, meetings, and tasks as distinct nodes instead of burying them inside long documents.
2. Use typed edges such as `depends_on`, `implements`, `inspired_by`, and `caused_by` so retrieval can distinguish dependencies from citations or incidental links.
3. Combine embeddings with graph structure: retrieve relevant seed nodes by similarity, then expand to selected neighbors for definitions, prerequisites, sources, and supporting facts.
4. Assemble LLM context from node content, linked references, and relationship metadata rather than supplying only the top-matching chunk.
5. Constrain graph expansion by relationship type and relevance to avoid pulling unrelated neighbors into the prompt.
6. Keep humans responsible for curating durable concepts and important links while automation extracts entities and proposes relationships.
7. Test the approach with 8–12 nodes and typed edges, then compare answers produced from a seed node alone against answers using its expanded neighborhood.

## Overview

This lesson explains the idea behind an LLM-oriented personal wiki that turns notes, documents, and linked concepts into a graph structure that is easier for both humans and language models to navigate. The central theme is that flat document collections are often a poor fit for retrieval and reasoning, while explicit entities, relationships, and backlinks can create a richer substrate for question answering, exploration, and context building.

Engineers who work on RAG systems, developer knowledge bases, note-taking tools, or AI assistants will care because this approach sits at the intersection of information architecture and LLM application design. Even without full source details from the video, the core pattern is clear: represent knowledge as connected nodes, enrich it with metadata and links, and use graph-aware retrieval to assemble better context for generation.

## Key Concepts

- **Knowledge graph over flat files**: A knowledge graph models information as nodes and edges instead of isolated documents. This makes relationships explicit, which helps both navigation and retrieval when answering questions that span multiple concepts.
- **Entity-centric note structure**: Instead of storing only long narrative pages, an entity-centric system creates distinct nodes for people, projects, ideas, papers, or terms. This enables targeted retrieval and lets the system compose context from several precise pieces rather than one large chunk.
- **Backlinks and typed relationships**: Backlinks show which notes reference a concept, while typed edges such as 'implements', 'depends_on', or 'inspired_by' encode stronger semantics. These links improve explainability and can guide traversal during retrieval.
- **Graph-aware retrieval**: Traditional RAG often retrieves the top-k semantically similar chunks and stops there. Graph-aware retrieval can start from a relevant node, expand to neighbors, and gather supporting context that is structurally related, not just textually similar.
- **Context assembly for LLMs**: The quality of an LLM answer depends heavily on how context is assembled. In a graphified wiki, context can be built from the primary node, its linked definitions, source references, and nearby concepts, producing a more grounded prompt.
- **Human-AI co-maintained memory**: A useful personal wiki is not just an index for machines; it is a durable memory system for people. The best systems let humans curate concepts and links while automation extracts entities, suggests relationships, and supports retrieval.

## How It Works

At a high level, a graphified wiki takes a body of notes or documents and transforms it into a set of connected knowledge objects. Each object is usually a node representing something meaningful: a concept, person, company, paper, codebase, meeting, or task. Edges describe how those nodes relate. The resulting structure is more expressive than a folder of markdown files or a vector store full of arbitrary chunks.

A typical pipeline looks like this:

1. **Ingest source material**
   - Notes, markdown pages, PDFs, transcripts, blog posts, bookmarks, or code comments are collected.
   - Each source gets basic metadata such as title, author, timestamp, and origin.

2. **Extract entities and concepts**
   - The system identifies candidate nodes from the text: named entities, technical terms, recurring project names, and references.
   - Depending on the implementation, this may be rule-based, embedding-assisted, or LLM-assisted.

3. **Create links and relationships**
   - Obvious references become backlinks.
   - Stronger semantic links may be inferred, such as one note summarizing another, one project depending on a library, or one idea generalizing another.
   - Typed relationships matter because they let downstream retrieval distinguish between a citation and a dependency.

4. **Index both text and graph structure**
   - The text content of each node can be embedded for semantic search.
   - The adjacency information is stored separately so the system can traverse neighbors after an initial retrieval hit.
   - This hybrid setup combines the strengths of vector search and symbolic structure.

5. **Answer questions by retrieve-then-expand**
   - A user asks a question.
   - The system retrieves likely relevant nodes by keyword or embedding similarity.
   - It then expands to nearby nodes: definitions, source notes, prerequisite concepts, or cited references.
   - The final prompt includes selected node content plus the relationship context, allowing the LLM to answer with better grounding.

This differs from naive chunk retrieval in an important way. In a flat RAG system, the model might retrieve a paragraph mentioning a topic but miss the neighboring ideas that explain it. In a graph-based system, retrieval can intentionally pull the local neighborhood around the topic. That often improves:

- **Coverage**: supporting facts are less likely to be omitted.
- **Precision**: expansion can be constrained by relationship type.
- **Explainability**: you can show which nodes and edges contributed to the answer.
- **Knowledge maintenance**: humans can edit a concept once and have all linked contexts benefit.

A practical mental model is to think of the system as having three layers:

- **Content layer**: the raw notes and source material.
- **Semantic layer**: entities, summaries, tags, and embeddings.
- **Graph layer**: links, backlinks, typed edges, and traversal rules.

When these layers are combined well, the wiki becomes useful for more than search. It becomes a memory substrate for AI workflows such as:

- generating project briefings
- answering questions about prior work
- surfacing dependencies between ideas
- tracing the evolution of a concept over time
- identifying missing documentation or weakly connected nodes

Even without repository code, you can infer the central architectural concern: the value is not just storing text, but structuring knowledge so that an LLM can navigate it intentionally. The graph is the organizing mechanism that turns notes into a reusable reasoning context.

## Training Exercise

Build a tiny graphified wiki from your own engineering notes and use it to answer a question.

### Goal
Create 8-12 nodes, connect them with typed edges, and simulate graph-aware retrieval for one technical question.

### Step 1: Create sample nodes
Make a directory called `mini-wiki` and create a JSON file named `nodes.json` with content like this:

```json
[
  {
    "id": "rag",
    "title": "Retrieval-Augmented Generation",
    "content": "RAG combines information retrieval with LLM generation. It typically retrieves relevant documents or chunks and includes them in the prompt.",
    "tags": ["llm", "retrieval"]
  },
  {
    "id": "vector-search",
    "title": "Vector Search",
    "content": "Vector search finds semantically similar content using embeddings. It is commonly used as the first-stage retriever in RAG systems.",
    "tags": ["embeddings", "search"]
  },
  {
    "id": "knowledge-graph",
    "title": "Knowledge Graph",
    "content": "A knowledge graph represents entities and their relationships as nodes and edges. It helps connect related facts explicitly.",
    "tags": ["graph", "knowledge"]
  },
  {
    "id": "graph-rag",
    "title": "Graph RAG",
    "content": "Graph RAG augments retrieval by traversing structured relationships between entities after an initial match.",
    "tags": ["rag", "graph"]
  }
]
```

Create `edges.json`:

```json
[
  {"source": "graph-rag", "target": "rag", "type": "extends"},
  {"source": "graph-rag", "target": "knowledge-graph", "type": "uses"},
  {"source": "rag", "target": "vector-search", "type": "often_uses"}
]
```

### Step 2: Write a simple retrieval script
Use Python to retrieve a node by keyword and expand to neighbors.

```python
import json

with open("nodes.json") as f:
    nodes = {n["id"]: n for n in json.load(f)}

with open("edges.json") as f:
    edges = json.load(f)

query = "How does graph RAG differ from standard RAG?"
keywords = set(query.lower().replace("?", "").split())

scores = []
for node_id, node in nodes.items():
    text = (node["title"] + " " + node["content"]).lower()
    score = sum(1 for k in keywords if k in text)
    scores.append((score, node_id))

scores.sort(reverse=True)
seed_id = scores[0][1]
print("Seed node:", seed_id, nodes[seed_id]["title"])

neighbors = []
for e in edges:
    if e["source"] == seed_id:
        neighbors.append((e["type"], e["target"]))
    elif e["target"] == seed_id:
        neighbors.append((e["type"], e["source"]))

print("\nContext package:")
print("-", nodes[seed_id]["content"])
for rel_type, nid in neighbors:
    print(f"- [{rel_type}] {nodes[nid]['title']}: {nodes[nid]['content']}")
```

### Step 3: Run it

```bash
python retrieve.py
```

### Step 4: Inspect the result
Answer the following:
- Which node became the seed?
- Which neighboring nodes were pulled in?
- Did the expanded context help explain the difference between RAG and graph RAG?

### Step 5: Extend the graph
Add at least four more nodes from your real work, for example:
- a service you own
- a database technology
- an incident postmortem
- a design doc

Add typed relationships such as `depends_on`, `documents`, `caused_by`, or `replaces`.

### Step 6: Reflect on production implications
Write a short note covering:
- what should become a node versus a tag
- which relationships should be typed
- how you would combine graph expansion with embeddings in a real system
- how you would prevent irrelevant neighbor expansion

If you want an extra challenge, feed the assembled context package into an LLM and compare its answer quality against using only the single top-matching node.

## Test Yourself

<details><summary>How does graph-aware retrieval differ from conventional top-k chunk retrieval?</summary>

Conventional retrieval returns the most textually or semantically similar chunks. Graph-aware retrieval starts with relevant nodes and expands through selected relationships to collect structurally related context that similarity search might miss.

</details>

<details><summary>Why are typed relationships more useful than generic backlinks?</summary>

Typed relationships record how two nodes are connected, such as one service depending on another or one document replacing another. The lesson argues that these semantics improve retrieval precision, traversal control, and explanation of why context was included.

</details>

<details><summary>What three layers make up the lesson&#x27;s practical model of a graphified wiki?</summary>

The content layer holds raw notes and sources, the semantic layer adds entities, summaries, tags, and embeddings, and the graph layer stores links, typed edges, and traversal rules. Together they support both human navigation and intentional context assembly for LLMs.

</details>

## Further Reading

- [Andrej Karpathy](https://karpathy.ai/)
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)
- [Neo4j GraphRAG Developer Guide](https://neo4j.com/developer/genai/)
- [How to Build a Knowledge Graph](https://www.oreilly.com/library/view/building-knowledge-graphs/9781492090893/)
