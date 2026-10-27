---
title: "Using GitHub Copilot CLI BYOK with Custom OpenAI-Compatible Models"
source: "https://linkedin.com/posts/burkeholland_the-github-copilot-cli-now-supports-byok-ugcPost-7454977496137072640-qEYz?rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY"
date: "2026-05-14"
tags: [github-copilot, cli, byok, openrouter, llms]
source_type: "web"
topics: [github-copilot, developer-tools, coding-agents]
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> GitHub Copilot CLI’s BYOK support can route requests to custom models through an OpenAI-compatible provider, giving engineers more control over model choice and cost while preserving the familiar terminal workflow. The `cpm` utility makes this setup repeatable by managing provider, model, token-limit, and API-key environment variables.

## Key Takeaways

1. Use an OpenAI-compatible provider and your own API key to run Copilot CLI with models outside the default Copilot catalog.
2. Configure the provider’s base URL, type (`openai`), API key, exact model ID, prompt/context token limit, and output token limit.
3. Enter model IDs exactly as the provider specifies them; an incorrect identifier will cause requests to fail.
4. Set accurate context and output limits so Copilot CLI does not send requests that exceed the model’s constraints.
5. Use OpenRouter as a gateway when you want one OpenAI-compatible endpoint and account for accessing multiple vendors’ models with prepaid spend controls.
6. Run `cpm add` to register a provider and model once, then run `cpm` to select a configuration and launch Copilot CLI with the appropriate environment variables.
7. Protect API keys stored in local configuration or environment variables with appropriate secret hygiene.

## Overview

These notes explain how to use GitHub Copilot CLI's BYOK (Bring Your Own Key) support with custom models exposed through an OpenAI-compatible API. The main idea is that Copilot CLI does not have to be limited to the default models included in a Copilot subscription; instead, it can be pointed at third-party providers such as OpenRouter and used with alternative models like Qwen, Kimi, or MiniMax.

This matters because it gives engineers more flexibility over model selection, cost, and experimentation while preserving the familiar Copilot CLI workflow in the terminal. The notes also highlight a helper utility called `cpm` that simplifies switching between providers and models by managing the required environment variables interactively.

## Key Concepts

- **BYOK in Copilot CLI**: BYOK means Copilot CLI can authenticate against a model provider using your own API key rather than only using models included with your Copilot plan. In practice, this lets you route Copilot CLI requests to third-party model backends while keeping the same command-line workflow.
- **OpenAI-compatible providers**: Copilot CLI expects providers that speak an OpenAI-compatible API. Many model gateways and hosting platforms expose this interface, which makes them usable without a provider-specific client implementation.
- **Provider configuration**: A provider definition typically includes a base URL, provider type, API key reference, and one or more model definitions. For each model, you also need metadata such as the model ID and token limits so the CLI can correctly format and constrain requests.
- **Model IDs and token limits**: The model ID is the exact string the backend expects when you request inference, such as a specific Qwen or MiniMax variant. Token limits matter because the client needs to know the maximum context window and output size it can safely request.
- **OpenRouter as a model gateway**: OpenRouter provides a single API surface for many different models and vendors. That makes it a practical choice for BYOK because one account and key can give you access to multiple models while also offering straightforward spend control through prepaid credits.
- **Model switching utility**: The `cpm` utility described in the source wraps the tedious parts of configuring environment variables and selecting providers/models. Instead of manually exporting settings each time, you can add providers once and switch interactively.

## How It Works

At a high level, the process is straightforward: get an API key from an OpenAI-compatible provider, tell Copilot CLI where that provider lives, specify the model and its limits, and launch the CLI with that configuration active.

The notes use **OpenRouter** as the example because it exposes many models behind one OpenAI-compatible endpoint. This is useful operationally because you can try different models without changing tools. OpenRouter also acts as a billing and routing layer, which can help with cost control through prepaid usage.

To make this work, Copilot CLI needs a small set of configuration values:

- a friendly **provider name**
- the provider **base URL**
- a **type**, typically `openai`
- an **API key**
- the exact **model ID**
- the **prompt/context token limit**
- the **output token limit**

These details matter more than they may first appear. The model ID must exactly match the provider’s expected identifier or requests will fail. Token limits are also important because the client needs to know how much input it can send and how much output it can request without exceeding the model’s constraints.

The `cpm` helper utility makes this less error-prone by wrapping configuration and switching in a dedicated workflow. Instead of manually exporting environment variables every time, you can register providers and models once, then select them interactively.

Typical flow:

```text
cpm add
```

Then provide values such as:

- provider name: `openrouter`
- base URL: OpenRouter's OpenAI-compatible endpoint
- provider type: `openai`
- API key label: any friendly name
- API key value: your OpenRouter key
- model ID: for example, a Qwen model ID
- prompt/context token limit
- output token limit

After that, you can list and activate configured entries with:

```text
cpm
```

Selecting one activates the relevant provider/model settings and opens Copilot CLI with the correct environment variables in place. In the demonstration described by the notes, the active model indicator in Copilot CLI updates to show the selected custom model, confirming that requests are being routed away from the default Copilot model.

Conceptually, the data flow is:

- user enters a prompt in Copilot CLI
- Copilot CLI reads the active provider/model configuration
- the request is formatted as an OpenAI-compatible API call
- the third-party backend runs inference
- the response is returned to Copilot CLI and shown in the terminal

A useful practical detail is that the experience still feels like Copilot CLI even when custom models are used. That means teams can keep the same terminal-first interface while gaining more control over where inference happens.

The main tradeoffs noted are:

- **Flexibility**: access models outside the bundled Copilot catalog
- **Cost control**: use gateways such as OpenRouter with prepaid credits
- **Compatibility constraints**: only providers with OpenAI-compatible APIs work cleanly
- **Manual metadata**: model IDs and token limits must be known and entered correctly
- **Security**: API keys now live in local config or environment variables, so secret hygiene matters

If doing this without `cpm`, the real challenge is reproducible environment management. You need to ensure the correct base URL, auth token, model name, and token settings are exported in the shell session before launching Copilot CLI. A wrapper script or shell profile can help, but `cpm` turns that into a simpler, more repeatable workflow.

## Test Yourself

<details><summary>What must a provider support to work cleanly with Copilot CLI’s BYOK configuration?</summary>

It must expose an OpenAI-compatible API. Copilot CLI uses the configured base URL, credentials, model ID, and token limits to format requests for that interface.

</details>

<details><summary>Why must the model ID and token limits be configured accurately?</summary>

The model ID must match the backend’s expected identifier or the request can fail. Accurate limits keep prompts and requested outputs within the model’s supported constraints.

</details>

<details><summary>What problem does `cpm` solve?</summary>

According to the lesson, `cpm` lets users register provider and model settings once, switch among them interactively, and launch Copilot CLI with the required environment variables active instead of managing them manually for each session.

</details>

## Personal Notes

Using GitHub Copilot CLI BYOK with Custom OpenAI-Compatible Models

Source: https://www.linkedin.com/posts/burkeholland_the-github-copilot-cli-now-supports-byok-ugcPost-7454977496137072640-qEYz?utm_source=social_share_send&utm_medium=ios_app&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY&utm_campaign=share_via
Notion page: https://www.notion.so/Using-GitHub-Copilot-CLI-BYOK-with-Custom-OpenAI-Compatible-Models-36001bb0839a817a834ff1e7aaace414

Tags: github-copilot, cli, llms, openrouter, byok, api

Overview

GitHub Copilot CLI's BYOK (Bring Your Own Key) capability lets you use models outside the default Copilot subscription catalog, as long as they are exposed through an OpenAI-compatible API. That opens the door to experimenting with alternative commercial and open-weight models through providers such as OpenRouter, while keeping Copilot CLI as the terminal interface engineers already use.

This matters to engineers who want more control over model choice, cost, and capability. Instead of being locked to bundled models, you can point Copilot CLI at providers like OpenRouter and select models such as Qwen, Kimi, or MiniMax. The source material also highlights a small helper utility, `cpm` (Copilot Models), which simplifies provider/model switching by managing the required environment variables interactively.

Key Concepts

  *   BYOK in Copilot CLI: BYOK means Copilot CLI can authenticate against a model provider using your own API key rather than only using models included with your Copilot plan. In practice, this lets you route Copilot CLI requests to third-party model backends while keeping the same command-line workflow.
  *   OpenAI-compatible providers: Copilot CLI expects providers that speak an OpenAI-compatible API. Many model gateways and hosting platforms expose this interface, which makes them usable without a provider-specific client implementation.
  *   Provider configuration: A provider definition typically includes a base URL, provider type, API key reference, and one or more model definitions. For each model, you also need metadata such as the model ID and token limits so the CLI can correctly format and constrain requests.
  *   Model IDs and token limits: The model ID is the exact string the backend expects when you request inference, such as a specific Qwen or MiniMax variant. Token limits matter because the client needs to know the maximum context window and output size it can safely request.
  *   OpenRouter as a model gateway: OpenRouter provides a single API surface for many different models and vendors. That makes it a practical choice for BYOK because one account and key can give you access to multiple models while also offering straightforward spend control through prepaid credits.
  *   Model switching utility: The `cpm` utility described in the source wraps the tedious parts of configuring environment variables and selecting providers/models. Instead of manually exporting settings each time, you can add providers once and switch interactively.

How It Works

At a high level, the flow is:

1. Obtain an API key from a provider that exposes an OpenAI-compatible endpoint. 2. Tell Copilot CLI how to reach that provider. 3. Specify which model to use, along with its token limits. 4. Start Copilot CLI with that configuration active.

The source uses **OpenRouter** as the example provider because it offers access to many models behind one API. The practical benefit is that you can experiment with non-default models without changing your terminal workflow. OpenRouter also acts as a billing and routing layer, so you can preload credits and stop usage when the balance is exhausted.

The configuration data you need is fairly standard
