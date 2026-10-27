---
title: "Google OKF: Structuring Knowledge for Agent-Centric Systems"
source: "https://youtu.be/MY9F9K7wWX4?is=j8oyCcP_y8Ae1eBU"
date: "2026-06-17"
tags: [knowledge-graphs, ai-agents, information-architecture, semantic-modeling, retrieval]
source_type: "youtube"
channel: "Marie Haynes"
published: "2026-06-16"
duration_seconds: 1089
topics: [rag-and-retrieval, ai-agents, classifiers-and-structured-output]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> Google’s OKF, as presented in the lesson, organizes knowledge into explicit entities, attributes, relationships, provenance, and action context so agents can retrieve and use it reliably. This matters because agents can assemble precise, auditable context for multi-step tasks instead of inferring structure from scattered prose.

## Key Takeaways

1. Treat agent quality as a knowledge-modeling problem, not only a model-selection or prompting problem.
2. Represent domain knowledge as canonical objects with stable identifiers, typed attributes, and explicit relationships such as `depends_on`, `owned_by`, or `supersedes`.
3. Attach provenance and metadata to each fact so agent outputs can be verified, debugged, and updated safely.
4. Retrieve only the entities, relationships, policies, and procedures required for the current task to reduce token use and irrelevant context.
5. Normalize duplicated prose into reusable knowledge units so one update can propagate consistently across agent workflows.
6. Test the structure with multi-step questions—for example, identify a service, trace its dependencies, find its owner, and verify the applicable policy.
7. Add action context and safety constraints before allowing an agent to recommend or execute operational steps.

## Overview

This lesson explains the core idea behind Google's OKF as presented in the source: a structured way to organize knowledge so software agents can reliably understand, retrieve, and act on it. Rather than treating knowledge as unstructured text blobs, the approach emphasizes explicit structure, relationships, and machine-usable context that improve agent performance on search, planning, and task execution.

Engineers building agent systems, internal knowledge platforms, retrieval pipelines, or enterprise AI tooling should care because the quality of an agent's behavior is tightly coupled to the shape of the knowledge it can access. A well-structured knowledge layer can make agent responses more grounded, composable, and maintainable than ad hoc prompt stuffing or naive document retrieval alone.

## Key Concepts

- **Agent-oriented knowledge**: Traditional documentation is written primarily for humans, but agents need data that is explicit, consistent, and easy to traverse programmatically. Agent-oriented knowledge captures not just content, but also entities, relationships, metadata, and action-relevant context.
- **Structured representations**: A structured knowledge format encodes facts in a way that supports deterministic lookup and reasoning. This often means moving from long-form prose toward schemas, typed objects, linked records, and relationship graphs that reduce ambiguity.
- **Entity and relationship modeling**: A key part of knowledge structuring is identifying the important entities in a domain and how they connect. Agents can use these connections to answer multi-hop questions, trace dependencies, and assemble relevant context more precisely than keyword search alone.
- **Grounded retrieval**: When an agent retrieves knowledge from a structured source, it can ground its outputs in named objects, canonical records, and verifiable links. This reduces hallucination risk and makes answers easier to inspect and debug.
- **Composable context**: Agents perform better when context can be assembled from modular pieces instead of one giant document. Structured knowledge allows systems to combine only the relevant facts, policies, procedures, and constraints for the current task.
- **Knowledge maintenance**: A structured knowledge layer is easier to update incrementally than duplicated prose scattered across documents. When knowledge is normalized into reusable units, changes can propagate consistently across many agent workflows.

## How It Works

At a high level, OKF can be understood as a shift from **document-centric knowledge** to **agent-consumable knowledge**. In a document-centric system, an agent searches text, extracts likely answers, and hopes the relevant information is present in the retrieved passages. In an agent-centric system, the knowledge is modeled so the agent can locate exact entities, follow relationships, and assemble context from well-defined records.

A practical mental model is to think of the knowledge layer as having several parts:

- **Objects/entities**: the core things in the domain, such as products, APIs, policies, users, incidents, or tasks
- **Attributes**: properties of those objects, like version, owner, status, permissions, or deadlines
- **Relationships**: links between objects, such as "depends on," "owned by," "supersedes," or "approved by"
- **Evidence/source links**: pointers back to source material so outputs remain auditable
- **Action context**: instructions, constraints, and procedures the agent can use to decide what to do next

This structure matters because many agent tasks are not simple fact lookups. They involve multi-step reasoning such as: identify the right component, determine its owner, verify the current policy, check dependencies, and then choose the next action. If all of that information is buried in free-form text, the agent must infer both the data model and the answer at the same time. If the knowledge is already structured, the agent can traverse the model directly.

A common workflow for an OKF-style system looks like this:

1. **Ingest source knowledge** from documents, databases, tickets, manuals, or APIs.
2. **Normalize the content** into a canonical schema so similar concepts share one representation.
3. **Extract entities and relationships** to create a connected knowledge layer.
4. **Attach provenance and metadata** so every fact can be traced back to a source.
5. **Retrieve context selectively** based on the agent's task, rather than dumping whole documents into the prompt.
6. **Use the structured result** to answer, plan, or trigger downstream actions.

For example, instead of storing a deployment runbook only as prose, you might represent it as:

```text
Service: billing-api
Owner: payments-sre
Environment: production
DependsOn: postgres-cluster-3
RollbackProcedure: runbook://rollback-billing-v2
ApprovalPolicy: policy://prod-change-window
```

Now an agent handling an operational question can do more than summarize the runbook. It can identify the service, discover dependencies, fetch the correct rollback procedure, and check the approval policy before recommending or executing a step.

Another important idea is that structured knowledge improves **context assembly**. In many retrieval-augmented systems, the agent gets a few chunks of text and must infer what is relevant. In an OKF-style approach, the retrieval system can construct a compact context package containing exactly the objects and relations needed for the task. That means lower token usage, less irrelevant text, and more reliable outputs.

This also changes how you evaluate knowledge quality. Instead of asking only whether documents are readable, you ask:

- Are the important entities explicit?
- Are identifiers consistent?
- Are relationships complete enough for agent traversal?
- Is provenance attached to each fact?
- Can the agent assemble task-specific context without manual prompt engineering?

The broader engineering implication is that building useful agents is partly a **knowledge modeling** problem, not just a model selection problem. Better models help, but the system becomes much more robust when the underlying knowledge is represented in a way that supports retrieval, reasoning, and action.

## Training Exercise

Build a small OKF-style knowledge layer for a domain you know, such as internal services, project tasks, or team policies.

### Goal
Convert messy human-oriented notes into a structured format an agent could query reliably.

### Step 1: Pick a small domain
Choose one of these:

- 3-5 microservices in a system
- 5-10 team policies or procedures
- 5 project tasks with owners and dependencies

### Step 2: Define a simple schema
Create a JSON schema mentally or in a file with fields like:

- `id`
- `type`
- `name`
- `owner`
- `depends_on`
- `status`
- `source`
- `related_policies`

### Step 3: Encode the knowledge
Create a file named `knowledge.json`:

```json
[
  {
    "id": "svc.billing-api",
    "type": "service",
    "name": "billing-api",
    "owner": "payments-sre",
    "depends_on": ["db.postgres-3", "svc.auth-api"],
    "status": "production",
    "source": "runbook-billing.md",
    "related_policies": ["policy.change-window"]
  },
  {
    "id": "policy.change-window",
    "type": "policy",
    "name": "production change window",
    "owner": "platform-ops",
    "depends_on": [],
    "status": "active",
    "source": "ops-policies.md",
    "related_policies": []
  }
]
```

### Step 4: Ask agent-style questions
Test whether your structure can answer questions like:

- What services depend on `auth-api`?
- Who owns the policy required for billing deployments?
- What must be checked before changing a production service?

### Step 5: Write a tiny query script
Use Python to query your structured data:

```python
import json

with open("knowledge.json") as f:
    items = json.load(f)

by_id = {item["id"]: item for item in items}

target = "svc.billing-api"
item = by_id[target]

print("Service:", item["name"])
print("Owner:", item["owner"])
print("Dependencies:", item["depends_on"])
for policy_id in item["related_policies"]:
    print("Policy:", by_id[policy_id]["name"])
```

### Step 6: Reflect
After modeling the data, compare this to storing the same information in one long markdown document. Note which questions become easier, which relationships were missing, and what additional metadata an agent would need to act safely.

### Stretch task
Add provenance and timestamps, then design one more relation such as `approved_by`, `supersedes`, or `runbook_for`. This will show how quickly structured knowledge becomes more useful than flat text for multi-step tasks.

## Test Yourself

<details><summary>How does an agent-centric knowledge system differ from a document-centric one?</summary>

A document-centric system retrieves passages and requires the agent to infer both their structure and the answer. An agent-centric system exposes canonical entities, attributes, relationships, and evidence that the agent can traverse directly.

</details>

<details><summary>Why should each structured fact include provenance?</summary>

Provenance links a fact to its source, making agent outputs auditable and easier to verify, debug, and maintain. It also helps prevent unsupported claims from being treated as authoritative.

</details>

<details><summary>What should the training exercise reveal about structured knowledge?</summary>

Questions involving ownership, dependencies, and required policies should become easier to answer than they are from one long document. The exercise should also expose missing relationships and metadata that an agent would need to act safely.

</details>

## Further Reading

- [Google Research](https://research.google/)
- [Schema.org](https://schema.org/)
- [W3C Resource Description Framework (RDF)](https://www.w3.org/RDF/)
- [Knowledge Graphs at Google](https://blog.google/products/search/introducing-knowledge-graph-things-not/)
