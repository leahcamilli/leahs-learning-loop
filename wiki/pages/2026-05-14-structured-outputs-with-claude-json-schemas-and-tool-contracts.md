---
title: "Structured Outputs with Claude: JSON Schemas and Tool Contracts"
source: "https://claude.com/blog/structured-outputs-on-the-claude-developer-platform?hsa_acc=515731155&hsa_cam=780502254&hsa_grp=454823704&hsa_ad=1228202364&hsa_net=linkedin&hsa_ver=3"
date: "2026-05-14"
tags: [claude, json-schema, api-design, tool-calling, agent-systems]
source_type: "web"
topics: [claude, classifiers-and-structured-output, ai-agents]
kind: "deep-dive"
depth: 1
actionability: 1
---

## TL;DR

> Define JSON schemas or tool input contracts in the API request so Claude returns the exact structure downstream software expects. According to the lesson, this reduces parsing, repair, retry, and integration failures, allowing engineers to focus on whether the content and chosen actions are correct.

## Key Takeaways

1. Treat output structure as an API contract instead of prompting Claude to “return valid JSON.”
2. Use JSON Schema responses for extraction, classification, and converting unstructured content into typed records.
3. Use schema-conformant tool calls for assistants, multi-agent systems, workflow engines, and API orchestration.
4. Replace raw-text parsing, key and type repair, and formatting retries with schema definition followed by business-rule validation.
5. Keep validating semantic correctness: schema conformance does not prove that an extracted value, selected filter, tool, or action is appropriate.
6. Use structured contracts for reliable agent handoffs involving plans, observations, task states, and action parameters.
7. Apply structured outputs where exact fields and types matter, including OCR, invoices, support tickets, documents, and complex search tools.

## Overview

These notes cover Claude’s structured outputs feature, which enforces response shape at the API level using either JSON Schema or tool definitions. The main idea is to stop relying on prompts like “return valid JSON” and instead define output structure as part of the request contract, making responses far more reliable for programmatic use.

This matters for production AI systems where model output feeds automation, workflows, external APIs, or multi-agent communication. By turning schema adherence into a platform guarantee, engineers can reduce parsing failures, retries, repair logic, and downstream errors, and focus more on semantic correctness than formatting recovery.

## Key Concepts

- **Structured outputs**: API-level guarantees that Claude returns data matching a developer-defined structure, either through JSON Schema or tool input definitions.
- **JSON schema enforcement**: A schema is included in the request and the response is constrained to match it, reducing fragile parsing and type-coercion code.
- **Tool definition conformance**: When tools are defined with structured inputs, Claude emits arguments that conform to those contracts, which is especially useful for agents and workflow systems.
- **Production reliability**: Strict output shape reduces runtime failures when downstream systems require exact fields, types, or patterns.
- **Agent communication contracts**: Multi-agent systems benefit from reliable machine-readable handoffs for plans, task state, and action parameters.
- **Reduced defensive code**: Validation can shift away from formatting repair toward actual business rules and semantic checks.

## How It Works

The core mechanism is simple: instead of asking the model to produce structured text and then trying to parse it afterward, you provide the expected structure in the API call itself. Claude then generates output that conforms to that declared structure.

There are two main modes:

1. **JSON-structured response mode**
   - You send a JSON Schema in the request.
   - Claude returns a response that matches that schema.
   - Best suited for extraction, classification, and converting unstructured input into typed records.

2. **Tool-based structured mode**
   - You define tools with structured input schemas.
   - Claude emits tool calls with arguments matching those definitions.
   - Best suited for assistants, agent systems, workflow engines, and API orchestration.

The practical engineering shift is important. In a non-structured setup, the application often has to:

- Prompt for JSON
- Parse raw text
- Validate keys and types
- Retry or repair malformed output
- Handle downstream failures caused by bad arguments

With structured outputs, the flow becomes:

- Define the schema or tool contract
- Send request
- Receive conformant structured data
- Apply business validation
- Pass output to downstream systems

This narrows the failure surface. Formatting problems become less central, while semantic correctness becomes the main concern: whether the extracted value is correct, whether selected filters make sense, or whether the chosen tool/action is appropriate.

High-value scenarios called out in the notes include:

- **Data extraction**: OCR, invoices, support tickets, and documents where exact fields and types matter.
- **Multi-agent systems**: Reliable exchange of plans, observations, task states, and structured actions.
- **Complex search and workflow tools**: Calls with typed parameters, optional filters, allowed values, and downstream constraints.

A useful architectural takeaway is that structured outputs improve interface guarantees without requiring prompt-heavy formatting tricks. This can simplify integration design and reduce operational complexity in production systems.

## Test Yourself

<details><summary>What engineering change distinguishes structured outputs from prompting a model to return JSON?</summary>

The expected JSON Schema or tool input definition becomes part of the API request contract. The lesson says Claude then produces output conforming to that declared structure rather than leaving the application to recover structure from raw text.

</details>

<details><summary>When should JSON-structured response mode be used instead of tool-based structured mode?</summary>

Use JSON-structured responses for extraction, classification, and typed-record generation. Use tool-based mode when Claude must supply conformant arguments for assistants, agents, workflows, or external API actions.

</details>

<details><summary>What validation remains necessary after structural conformance is guaranteed?</summary>

Applications must still enforce business rules and evaluate semantic correctness. A structurally valid response can contain the wrong value, an illogical filter, or an inappropriate tool or action.

</details>

## Personal Notes

Structured Outputs with Claude: Enforcing JSON Schemas and Tool Contracts

Source: https://claude.com/blog/structured-outputs-on-the-claude-developer-platform/?utm_campaign=B2C_ADIR_US_CODE_SOC_CODR_BA_STATIC&utm_source=linkedin&utm_medium=paid&hsa_acc=515731155&hsa_cam=780502254&hsa_grp=454823704&hsa_ad=1228202364&hsa_net=linkedin&hsa_ver=3
Notion page: https://www.notion.so/Structured-Outputs-with-Claude-Enforcing-JSON-Schemas-and-Tool-Contracts-36001bb0839a81fe9169f8c04fa2b272

Tags: claude, json-schema, api-design, tool-calling, agent-systems

Overview

Structured outputs on the Claude Developer Platform let you require model responses to conform exactly to either a JSON schema or a tool definition. Instead of treating structured data generation as a prompt-engineering problem, this feature moves schema adherence into the API contract, reducing parsing failures, malformed tool calls, and retry-heavy recovery logic.

This matters most for production systems where LLM output feeds downstream automation: extraction pipelines, agent-to-agent messaging, API orchestration, and search or workflow tools with strict parameter requirements. Engineers building reliable AI applications care because schema guarantees simplify application code, improve operational stability, and reduce the risk that one formatting error cascades into larger system failures.

Key Concepts

  *   Structured outputs: Structured outputs are API-level guarantees that Claude's response will match a developer-specified structure. The structure can be expressed either as a JSON schema for direct data output or as a tool definition for function-style invocation.
  *   JSON schema enforcement: When using the JSON path, the developer includes a schema in the API request, and the model is constrained to return data that matches it. This reduces the need for fragile post-processing logic that attempts to coerce free-form text into typed objects.
  *   Tool definition conformance: When using tools, the model's output is shaped to match declared tool inputs automatically. This is especially valuable in agentic systems where a malformed argument object can cause failed calls, retries, or inconsistent execution paths.
  *   Production reliability: A key motivation for structured outputs is preventing schema-related failures in real systems. If downstream services expect exact fields, types, or patterns, guaranteed conformance reduces runtime errors and improves system predictability.
  *   Agent communication contracts: Multi-agent architectures often pass structured state, plans, and task parameters between agents. Structured outputs make those handoffs more reliable by ensuring every message follows an agreed machine-readable contract.
  *   Reduced defensive code: Without schema guarantees, application code often includes retries, validators, parsing heuristics, and fallback branches. Structured outputs let engineers remove much of that complexity and keep validation focused on business rules rather than formatting repair.

How It Works

The core idea is straightforward: instead of asking Claude to "please return valid JSON" and hoping the response is well-formed, you define the shape of the desired output in the API call. Claude then produces an output that matches that declared structure.

There are two main usage modes:

1. **JSON-structured response mode** - You provide a JSON schema in the request. - Claude returns a response that conforms to that schema. - This is a good fit for extraction, classification, summarization into typed records, or any workflow where your application wants a data object rather than prose.

2. **Tool-based structured mode** - You define one or more tools with structured input parameters. - Claude emits output that conforms to those tool definitions. - This is a good fit for assistants, agents, and workflow engines that need to call internal functions or external APIs.

The article's main engineering argument is that reliability improves when structure is enforced by the platform rather than reconstructed after generation. In a typical non-structured integration, the flow often looks like this:

- Prompt model for JSON - Receive text that is usually, but not always, valid - Parse JSON - Validate fields and types - Retry or repair if parsing fails - Handle downstream tool/API errors caused by malformed arguments

With structured outputs, the flow becomes simpler:

- Define the target schema or tool contract - Send request to Claude - Receive conformant structured output - Apply business validation if needed - Pass directly to downstream systems

This changes the failure surface. Instead of spending engineering effort on formatting recovery, teams can focus on semantic correctness: whether the extracted invoice total is right, whether the chosen search filters are sensible, or whether the selected tool is appropriate.

The article highlights several high-value scenarios:

- **Data extraction**: For OCR or document/image extraction pipelines, downstream systems often require exact keys and consistent types. Structured outputs reduce ingestion failures. - **Multi-agent systems**: Agents frequently exchange plans, observations, task states, and action parameters. Strict output shape improves interoperability and stability. - **Complex search tools**: Search requests often have multiple fields with specific patterns or allowed values. Tool-definition conformance helps ensure every field is correctly populated.

An important practical point is that the feature is described as improving reliability **without impacting model performance**. From an application architecture perspective, this means engineers can strengthen interface guarantees without redesigning prompts around defensive output formatting.

A minimal conceptual request for JSON-structured output might look like this:

```json { "model": "claude-sonnet-4.5", "messages": [ { "role": "user", "content": "Extract the customer name, invoice number, and total from this document." } ], "response_format": { "type": "json_schema", "schema": { "type": "object", "properties": { "customer_name": { "type": "string" }, "invoice_number": { "type": "string" }, "total": { "type": "number" } }, "required": ["customer_name", "invoice_number", "total"] } } } ```

A conceptual tool-based setup might instead define a search tool like this:

```json { "name": "search_catalog", "description": "Search product catalog with structured filters", "input_schema": { "type": "object", "properties": { "query": { "type": "string" }, "category": { "type": "string" }, "max_price
