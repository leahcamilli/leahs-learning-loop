---
title: "Building Guardrailed AI Agents with Ontologies and Validation"
source: "https://www.youtube.com/watch?v=Sir59K8ZDPU"
date: "2026-09-11"
tags: [ai-agents, ontologies, knowledge-graphs, neuro-symbolic-ai, data-validation]
source_type: "youtube"
source_fingerprint: "6e412f7f0f"
source_characters: 16779
channel: "AI Engineer"
published: "2026-07-22"
duration_seconds: 1278
topics: [ai-agents, ai-safety-and-governance, classifiers-and-structured-output, rag-and-retrieval]
kind: "deep-dive"
depth: 2
actionability: 1
---

## TL;DR

> Guard consequential AI-agent actions with typed validation, ontology-based semantic checks, and explicit loop limits before allowing external side effects. This matters because structurally valid tool calls can still be unsafe, nonsensical, duplicative, or too costly.

## Key Takeaways

1. Separate probabilistic planning from deterministic enforcement: let the model propose actions, but let code and domain rules decide what may execute.
2. Validate twice: use typed schemas for required fields and data types, then ontology rules for domain meaning, relationships, roles, vocabulary, and prior state.
3. Keep state-changing operations staged and side-effect-free until validation succeeds or a human explicitly approves them.
4. Set maximum iterations, token or monetary budgets, tool timeouts, and escalation rules to prevent runaway agent loops.
5. Build ontologies from both expert-defined concepts and recurring operational evidence, reusing established vocabularies such as Schema.org, FOAF, and Dublin Core where appropriate.
6. Interpret ontology reasoning carefully: an OWL functional property may merge two recorded values as the same individual instead of reporting a validation error.
7. Maintain an auditable record of every proposed action, validation decision, retry, escalation, and execution.

## Overview

AI agents combine probabilistic language-model decisions with tools and iterative control loops. This flexibility also creates risks: fabricated values, invalid actions, runaway loops, unintended side effects, and mounting token costs. The source proposes a neuro-symbolic design that places formal domain knowledge around an agent. Typed validation checks the shape of tool inputs and outputs, while an ontology checks whether their meaning and relationships are consistent with the domain. The practical goal is not to eliminate probabilistic behavior, but to constrain consequential actions before they change external state.

## Key Concepts

- **Agent perception–decision–action cycle**: An agent receives context, decides what should happen next, and requests an action. A language model itself only produces output; an application must interpret a tool request, execute the selected tool, return its result, and decide whether the loop should continue.
- **Ontologies and knowledge graphs**: An ontology formally describes a shared domain using entities, properties, relationships, and constraints. A graph representation makes relationships explicit and can be extended by adding nodes, properties, or edges. The source contrasts this flexibility with the more rigid table structure of relational databases, though real relational schemas can also evolve.
- **Top-down and bottom-up modeling**: A top-down ontology begins with domain experts identifying concepts such as customers, orders, representatives, and their relationships. A bottom-up ontology extracts recurring entities and relationships from operational evidence such as customer interactions. A practical ontology can combine both approaches and reuse established vocabularies such as Schema.org, FOAF, and Dublin Core where appropriate.
- **RDFS inference**: RDFS domain and range declarations can derive additional classifications. If the property “teaches” has domain Teacher and range Student, then the statement “Bob teaches Scooter” supports inferring that Bob is a Teacher and Scooter is a Student. If Teacher is a subclass of Person, Bob can also be inferred to be a Person.
- **OWL constraints and reasoning**: OWL can express semantics such as transitive, functional, disjoint, and restricted-value relationships. A transitive ancestor relationship can derive an indirect ancestor. A functional property allows at most one value and may cause two recorded values to be treated as identifiers for the same individual rather than automatically reporting an error. These rules depend on the ontology’s explicit assumptions and should not be mistaken for universal facts.
- **Agent loops and termination controls**: A tool-using loop commonly asks the model for the next step, examines its stop reason, executes a requested tool, validates the result, and either finishes, retries, or escalates to a human. Loops enable iterative work but can become infinite, drift away from the goal, or consume excessive tokens. Systems therefore need explicit iteration, cost, timeout, and escalation limits.
- **Syntactic versus semantic validation**: A schema-validation library such as Pydantic can check whether data has the required fields and acceptable types. An ontology-backed validator checks whether the data makes sense in the domain—for example, whether a status belongs to the permitted vocabulary, a recipient has the right role, or an order already has a refund. Passing type validation does not imply semantic correctness.
- **Side-effect isolation**: The source recommends keeping proposed agent actions free of external side effects until validation succeeds. Treat tool calls that modify databases, send payouts, or contact people as staged commands: construct the request, validate its structure, test it against ontology rules, and only then authorize execution or request human review.

## How It Works

A guarded agent can be organized as a staged loop. First, the model receives the user’s goal, relevant context, and descriptions of available tools. It may return either a final response or a structured tool request. Second, a typed model validates the requested arguments; malformed or missing data is rejected before execution. Third, a preferably read-only tool runs and returns structured evidence. Fourth, an ontology-aware reasoner evaluates the proposed conclusion or next action against domain rules—for example, permitted order statuses, disjoint organizational roles, cardinality constraints, and previously recorded transactions. If the result is valid, the controller may finish or authorize a separate state-changing operation. If it is invalid, the controller sends a precise error back to the model or escalates to a human. The controller must also enforce maximum iterations, token or monetary budgets, timeouts, and an auditable record of every proposal, validation decision, and execution. This separates probabilistic planning from deterministic enforcement: the model suggests; code and domain rules decide what is allowed to happen.

## Training Exercise

Design a guarded refund agent for a small online store. Define a graph with Customer, SupportRepresentative, Order, Payment, and Refund entities. Add relationships such as placedOrder, paidFor, requestsRefund, issuedFor, and refundRecipient. Specify a fixed order-status vocabulary: paid, shipped, or refunded. Add rules stating that Customer and SupportRepresentative are disjoint roles and that an order may have no more than one successful refund. Then define typed request and response models for a refund tool. Walk through four test cases: a valid first refund to the buyer; a second refund for the same order; a payout addressed to a support representative; and an order whose status is “probably shipped.” For each case, record whether structural validation or ontology validation catches the problem. Finally, sketch loop controls with a maximum of three model attempts, a tool timeout, a cost budget, and mandatory human review whenever validation continues to fail. Keep the exercise read-only or use a mock ledger so no real payment can occur.

## Test Yourself

<details><summary>Why is typed schema validation insufficient for guarding an agent action?</summary>

It can confirm that fields exist and contain acceptable data types, but it cannot establish that an action makes sense in the domain. An ontology can additionally detect invalid statuses, incompatible roles, prohibited relationships, or a refund that has already occurred.

</details>

<details><summary>How should a guarded agent handle an operation that changes external state?</summary>

The source recommends constructing the operation as a staged command, validating its structure, checking it against ontology rules, and only then authorizing execution. Repeated validation failures should trigger human review rather than an uncontrolled retry loop.

</details>

<details><summary>What controls should bound an iterative agent loop?</summary>

The controller should enforce limits on iterations, cost or token use, and execution time, plus a clear human-escalation policy. The training exercise proposes a maximum of three model attempts, a tool timeout, a cost budget, and mandatory review after continued validation failure.

</details>

## Further Reading

- [Source video on YouTube](https://www.youtube.com/watch?v=Sir59K8ZDPU)
- [Code Supreme](https://codesupreme.ai)
