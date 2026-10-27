---
title: "Prompt Caching in AI Coding Tools: How Cache Misses Inflate Token Costs"
source: "https://linkedin.com/posts/burkeholland_the-vast-majority-of-your-token-spend-is-ugcPost-7485391834861568000-8dmr?rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY"
date: "2026-07-21"
tags: [llm, prompt-engineering, token-optimization, developer-tools, ai-systems]
source_type: "web"
source_fingerprint: "d78b497e80"
source_characters: 13970
topics: [coding-agents, context-engineering, prompt-engineering]
kind: "deep-dive"
depth: 2
actionability: 3
---

## TL;DR

> Burke Holland argues that keeping the prompt prefix stable lets AI coding tools reuse cached computation, sharply reducing input-token costs. Changing models, reasoning levels, skills, tools, or agent configuration can trigger cache misses and erase those savings.

## Key Takeaways

1. Treat prompt caching as a prefix-stability problem: unchanged system instructions, tools, skills, agent definitions, and conversation history enable reuse.
2. Keep the model, reasoning level, enabled skills, MCP servers, and agent setup stable while completing related work.
3. Batch related tasks into one session so the provider can reuse earlier prompt computation instead of repeatedly processing the full context.
4. Expect cache reuse to expire; the source describes roughly a 30-minute TTL for OpenAI 5-6 models and a 5-minute default for Anthropic API caching, with extension options.
5. Reverting to an earlier configuration may restore its cached prompt state if that variant remains within its TTL.
6. Remember that cache misses can be partial because unchanged earlier chunks may still be reusable.
7. Start a new session when instruction-file edits must take effect, because the source claims changes to an `AGENTS.md`-style file were not detected within the existing session.

## Overview

This lesson explains prompt caching as described in Burke Holland’s transcript: why repeated prompts become cheaper, what kinds of changes silently trigger cache misses, and how to structure your workflow to preserve cache reuse. The practical takeaway is that much of your cost comes from input tokens, and small configuration changes can erase most of the savings unless you understand what counts as a changed prompt prefix.

## Key Concepts

- **Input-token cost dominates**: The source claims most token spend comes from input tokens, not output tokens. That makes input-side optimizations, especially caching, a high-leverage cost control.
- **Prompt caching reuses the unchanged prefix**: A chat request is described as a growing prompt made from system instructions, tools, skills, MCP definitions, custom agents, and conversation history. When that earlier portion stays the same, the provider can reuse cached work for it and only compute the new suffix.
- **Caching avoids repeated attention computation**: The transcript describes tokenization, vectorization, and attention as the expensive path. Caching matters because the provider can skip recomputing that earlier work for unchanged prompt content.
- **Cache misses come from prefix changes**: Changing the model, reasoning level, enabled skills, MCP servers, or agent setup can change the prefix and cause a cache miss. The practical lesson is that workflow configuration changes can cost more than message edits.
- **Caches have a time-to-live and multiple variants**: The source says OpenAI 5-6 models have about a 30-minute cache TTL, while Anthropic API caching is described as 5 minutes by default with possible extension. It also describes cached prompt states as keeping multiple variations, so returning to a previous configuration may restore reuse if still within TTL.
- **Misses may be partial, not absolute**: The transcript says prompts are cached in chunks, so a miss does not always mean zero reuse. If only later chunks changed, earlier unchanged chunks may still be reused.
- **Session boundaries matter for instruction files**: The source claims edits to an `AGENTS.md`-style instruction file were not picked up until starting a new session. That means some prompt-affecting files may not influence caching or behavior until the harness rebuilds the session context.

## How It Works

Treat prompt caching as a prefix-stability problem. In the transcript’s model, your tool builds a long request from hidden system material plus your visible chat. The provider caches the expensive processing for that request. If you send another message without changing the earlier structure, the provider can reuse that cached prefix and charge far less. If you switch models, alter reasoning level, enable or disable skills or MCP servers, or move to a different custom-agent setup, you likely change the prefix and lose most of that reuse. The lesson is operational: keep your environment stable during a task, avoid unnecessary toggles, batch related work into the same session, and remember that returning to an earlier configuration may recover cached savings if the TTL has not expired. One uncertainty the source explicitly notes is Anthropic behavior: it is described as similar but not identical, and at least one example is presented as confusing rather than settled.

## Training Exercise

Open your AI coding tool and run a small controlled experiment. First, send the same short prompt twice in the same session and record whether token reuse or lower cost appears on the second run. Next, change one variable at a time: switch the model, change reasoning level, enable or disable one skill or tool, and note which change causes reuse to disappear. Then revert to a previous configuration within a short window and test whether reuse returns. Finish by writing a short rule set for yourself: which settings you will keep fixed during focused work, which changes deserve a fresh session, and how long you can pause before assuming the cache has expired.

## Test Yourself

<details><summary>Why can a small configuration change substantially increase token cost?</summary>

According to Holland, settings such as the model, reasoning level, enabled skills, MCP servers, and agent setup are part of the prompt prefix. Changing them can cause a cache miss, forcing the provider to recompute and bill more of the input.

</details>

<details><summary>What workflow best preserves prompt-cache reuse?</summary>

Keep the environment stable, batch related work into the same session, and avoid unnecessary configuration toggles. If you return to a previous setup before its cache expires, reuse may resume.

</details>

<details><summary>Does a cache miss always mean the entire prompt must be recomputed?</summary>

No. The transcript says prompts are cached in chunks, so unchanged earlier chunks may still be reused even when a later portion changes.

</details>

## Further Reading

- [Original LinkedIn post and transcript](https://linkedin.com/posts/burkeholland_the-vast-majority-of-your-token-spend-is-ugcPost-7485391834861568000-8dmr?rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY)
