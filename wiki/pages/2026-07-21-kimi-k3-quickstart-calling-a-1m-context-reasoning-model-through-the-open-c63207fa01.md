---
title: "Kimi K3 Quickstart: Calling a 1M-Context Reasoning Model Through the OpenAI SDK"
source: "https://platform.kimi.ai/docs/guide/kimi-k3-quickstart"
date: "2026-07-21"
tags: [llm-api, python, tool-calling, structured-output, multimodal]
source_type: "web"
source_fingerprint: "c63207fa01"
source_characters: 12882
topics: [python]
kind: "tutorial"
depth: 2
actionability: 3
---

## TL;DR

> Use the OpenAI Python SDK with Kimi’s custom base URL to access Kimi K3 while preserving its full assistant messages across multi-turn and tool-calling workflows. Correct message handling matters because reasoning, tool calls, structured output, and multimodal data use separate fields and formats.

## Key Takeaways

1. Point the OpenAI client at `https://api.moonshot.ai/v1` and authenticate with `MOONSHOT_API_KEY` to call `model="kimi-k3"`.
2. Treat reasoning as always on; set the top-level `reasoning_effort` to `low`, `high`, or `max`, which the source says is the default, to balance depth and latency.
3. Preserve the complete assistant message—not only `message.content`—in multi-turn and tool workflows because tool calls and metadata are stored on that message object.
4. Handle streaming `reasoning_content` and final-answer `content` separately, and parse structured results only from the final `message.content`.
5. Represent multimodal content as an array of typed parts; the source says images should use base64 data URLs rather than public URLs, while uploaded videos can use `ms://<file-id>`.
6. Enforce structured output with a strict `json_schema`, execute every returned tool call yourself, and append each result with its matching `tool_call_id` before requesting the final answer.
7. Keep long prompt prefixes unchanged to attempt automatic cache hits; the source says the preceding request must contain more than 256 prompt tokens to be cache-eligible.

## Overview

This lesson teaches how to use Kimi K3 from the Kimi API Platform quickstart page. The source presents Kimi K3 as a flagship 2.8-trillion-parameter model with native visual understanding, a 1M-token context window, always-on reasoning, and OpenAI SDK compatibility through `base_url="https://api.moonshot.ai/v1"`. Practically, the page is most useful as an API integration guide: authenticate with `MOONSHOT_API_KEY`, send chat completion requests, control `reasoning_effort`, stream reasoning and answer deltas, pass image/video inputs in the required message format, enforce JSON output with `json_schema`, and run tool-calling loops correctly by preserving the full assistant message. Some broader claims, such as being the first open-source model in its class or having roughly 2.5x K2 scaling efficiency, are stated by the source but not independently substantiated within it.

## Key Concepts

- **OpenAI SDK compatibility via custom base URL**: The examples use the Python `openai` package with `OpenAI(api_key=os.environ["MOONSHOT_API_KEY"], base_url="https://api.moonshot.ai/v1")`. The key practical point is that you keep the SDK interface but target Kimi's API endpoint.
- **Always-on reasoning with configurable effort**: Kimi K3 always runs in thinking mode. You cannot disable chain-of-thought behavior, but you can adjust the top-level `reasoning_effort` field to `low`, `high`, or `max` to trade off depth and latency; the source says the default is `max`.
- **Message integrity in multi-turn and tool workflows**: The source repeatedly warns to carry forward the complete assistant message returned by the API, not just `message.content`. This matters because tool calls and other metadata live on the assistant message object.
- **Streaming separates reasoning from final answer**: When streaming, deltas may contain `reasoning_content` and `content` separately. A client should handle both streams distinctly and avoid parsing intermediate reasoning as the final structured result.
- **Multimodal input requires structured content arrays**: For vision, `content` must be an array of typed objects such as text, `image_url`, or `video_url`, not a serialized string. Public image URLs are not supported according to the page; examples use base64 data URLs for images and `ms://<file-id>` for uploaded video.
- **Structured output uses strict JSON Schema**: To constrain the final answer, the quickstart uses `response_format={"type":"json_schema", ...}` with `strict: true`. The source explicitly says to parse only `message.content`, not `reasoning_content`.
- **Tool calling is explicit and stateful**: You can require at least one tool call with `tool_choice="required"`, execute each returned call yourself, append matching tool messages with `tool_call_id`, and call the model again. The page also shows dynamic tool loading by placing tool definitions in a `system` message.
- **Large-context usage benefits from stable prefixes**: The source says K3 has a 1M-token context window and automatic context caching. Cache eligibility depends on a previous request having more than 256 prompt tokens, and later requests should keep the long prefix unchanged to attempt cache hits.

## How It Works

A minimal working flow is: install `openai>=1.0`, set `MOONSHOT_API_KEY`, create an `OpenAI` client pointed at `https://api.moonshot.ai/v1`, and call `client.chat.completions.create(model="kimi-k3", messages=[...])`. From there, choose the advanced behavior you need. For deeper reasoning, set `reasoning_effort`. For streaming, read both `delta.reasoning_content` and `delta.content`. For vision, build `messages` so `content` is an array of typed parts and use base64 or uploaded-file references instead of public URLs. For JSON extraction, provide a strict `json_schema` and parse only the final `message.content`. For tool use, preserve the entire assistant message, execute every returned tool call, append corresponding tool results, and request the final answer in a second round. For long documents or knowledge bases, keep a stable long prefix so automatic caching can potentially help on later requests. Also note the documented limits: several sampling parameters are fixed and should be omitted, `max_completion_tokens` defaults to 131072 and can be raised to 1048576, and web search is described as not recommended for production workflows in the near term.

## Training Exercise

Build a small Python script that does three things with the same `client`: first, asks Kimi K3 for a one-sentence summary of a local markdown file inserted as a system prompt; second, extracts two fields from a sentence using strict `json_schema`; third, runs a single required tool call using a toy function like `get_weather`. Success criteria: you preserve the complete assistant message during the tool loop, parse structured data only from `message.content`, and keep the long markdown prefix unchanged between two related summarization questions so your code is compatible with the source's caching guidance.

## Test Yourself

<details><summary>How do you configure the OpenAI Python SDK to call Kimi K3?</summary>

Create an `OpenAI` client using `MOONSHOT_API_KEY` and set `base_url="https://api.moonshot.ai/v1"`. Then call the chat completions interface with `model="kimi-k3"`.

</details>

<details><summary>Why must a tool-calling loop preserve the complete assistant message?</summary>

The complete message contains tool calls and related metadata that are absent from `message.content`. After executing each call, append a tool message with the matching `tool_call_id` before sending the conversation back to the model.

</details>

<details><summary>Which data should be parsed when Kimi K3 produces strict JSON output, especially during reasoning or streaming?</summary>

Parse only the final `message.content` against the requested schema. Keep `reasoning_content` separate because it is intermediate reasoning, not the structured result.

</details>

## Further Reading

- [Kimi K3 - Kimi API Platform](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart)
