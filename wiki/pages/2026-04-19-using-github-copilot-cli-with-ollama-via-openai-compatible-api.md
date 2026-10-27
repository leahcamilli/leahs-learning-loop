---
title: "Using GitHub Copilot CLI with Ollama via OpenAI-Compatible API"
source: "https://docs.ollama.com/integrations/copilot-cli"
date: "2026-04-19"
tags: [ollama, copilot-cli, openai-api, terminal-ai, developer-tools]
source_type: "web"
topics: [github-copilot, developer-tools, coding-agents]
kind: "tutorial"
depth: 2
actionability: 3
---

## TL;DR

> Point GitHub Copilot CLI at Ollama’s OpenAI-compatible endpoint to keep the Copilot terminal workflow while choosing local or Ollama-hosted models. This enables controlled, repeatable repository analysis in interactive sessions, scripts, and CI/CD.

## Key Takeaways

1. Use `ollama launch copilot` for the simplest setup because Ollama configures the provider automatically.
2. Set `COPILOT_PROVIDER_BASE_URL=http://localhost:11434/v1` and `COPILOT_PROVIDER_WIRE_API=responses` when configuring the integration manually.
3. Leave `COPILOT_PROVIDER_API_KEY` empty for a typical local Ollama instance and select the backend with `COPILOT_MODEL`.
4. Choose a coding-capable model with at least a 64k-token context window for repository-level reasoning and conversation history.
5. For headless automation, specify `--model`, add `--yes` to skip interactive selection, and place native Copilot arguments after `--`.
6. Use interactive mode for repository exploration and architecture questions; use headless mode for scripted summaries, diff explanations, documentation, and CI tasks.
7. The integration requires no custom plugin layer because Copilot CLI communicates directly with Ollama’s OpenAI-compatible API.

## Overview

These notes explain how to configure GitHub Copilot CLI to use Ollama as the model backend through Ollama’s OpenAI-compatible API. The key idea is that Copilot CLI can send requests to a provider exposing an OpenAI-style interface, and Ollama serves that interface locally at `http://localhost:11434/v1`. This makes it possible to keep the Copilot CLI workflow while choosing local or Ollama-hosted models.

This setup is useful for developers who want more control over model selection, prefer local-first workflows, or need repeatable terminal-based AI behavior in scripts, Docker, or CI/CD. It is especially relevant for repository-level reasoning tasks, where larger context windows and coding-capable models matter.

## Key Concepts

- **Copilot CLI**: GitHub Copilot CLI is a terminal coding agent that can inspect repositories, answer codebase questions, suggest edits, and run commands. It supports both interactive shell use and non-interactive automation.
- **Ollama as a provider**: Ollama acts as the backend model server, exposing local and some cloud models through a single interface that Copilot CLI can call.
- **OpenAI-compatible API**: The integration depends on Ollama exposing an OpenAI-style endpoint at `http://localhost:11434/v1`, which matches the request format Copilot CLI expects.
- **Wire API selection**: `COPILOT_PROVIDER_WIRE_API=responses` tells Copilot CLI which API semantics to use when talking to Ollama.
- **Headless mode**: Headless execution lets Copilot CLI run without interactive prompts, which is helpful for scripts and CI. In this mode, `--yes` skips selection prompts and `--model` must be set explicitly.
- **Context window requirements**: Copilot CLI often needs to read large portions of a repository and prior conversation history, so models with at least a 64k token context window are recommended.

## How It Works

At a high level, Copilot CLI remains the terminal interface while Ollama becomes the LLM serving layer. Instead of talking to a default hosted provider, Copilot CLI is redirected to Ollama’s local OpenAI-compatible API.

There are two main ways to launch it:

1. **Quick launcher via Ollama**
   ```bash
   ollama launch copilot
   ```

   Or with an explicit model:

   ```bash
   ollama launch copilot --model kimi-k2.5:cloud
   ```

   This is the simplest approach because Ollama handles the provider configuration automatically.

2. **Manual configuration via environment variables**
   ```bash
   export COPILOT_PROVIDER_BASE_URL=http://localhost:11434/v1
   export COPILOT_PROVIDER_API_KEY=
   export COPILOT_PROVIDER_WIRE_API=responses
   export COPILOT_MODEL=qwen3.5
   copilot
   ```

   You can also run this inline for one-off commands:

   ```bash
   COPILOT_PROVIDER_BASE_URL=http://localhost:11434/v1 \
   COPILOT_PROVIDER_API_KEY= \
   COPILOT_PROVIDER_WIRE_API=responses \
   COPILOT_MODEL=glm-5:cloud \
   copilot
   ```

The environment variables do the following:

- `COPILOT_PROVIDER_BASE_URL`: points Copilot CLI to the Ollama API endpoint.
- `COPILOT_PROVIDER_API_KEY`: typically left empty for a local Ollama instance.
- `COPILOT_PROVIDER_WIRE_API=responses`: ensures compatible request/response behavior.
- `COPILOT_MODEL`: selects the model, such as `qwen3.5` or `glm-5:cloud`.

For automation, headless mode is the important pattern:

```bash
ollama launch copilot --model kimi-k2.5:cloud --yes -- -p "how does this repository work?"
```

How that command is interpreted:

1. `ollama launch copilot` starts the Copilot CLI integration.
2. `--model kimi-k2.5:cloud` selects the backend model.
3. `--yes` disables interactive confirmation and allows model pull behavior.
4. `--` separates Ollama launcher arguments from native Copilot CLI arguments.
5. `-p "..."` passes a prompt directly to Copilot CLI.

This makes the integration practical for repository summaries, diff explanations, scripted architecture questions, and CI-based documentation tasks.

Model choice matters because Copilot CLI is usually operating on more than a short prompt. It may need to reason across multiple files and previous turns, so larger-context models generally perform better. Recommended examples from the notes include:

- `kimi-k2.5:cloud`
- `glm-5:cloud`
- `minimax-m2.7:cloud`
- `qwen3.5:cloud`
- `glm-4.7-flash`
- `qwen3.5`

A practical workflow is:

- Use **interactive mode** during local development to explore a repository and ask architecture questions.
- Use **headless mode** in scripts or CI to generate summaries, notes, or implementation guidance.

The integration is lightweight: there is no custom plugin layer involved. Copilot CLI simply talks to a compatible API, and Ollama provides that API.

## Test Yourself

<details><summary>Which settings redirect Copilot CLI to Ollama and select compatible API behavior?</summary>

Set `COPILOT_PROVIDER_BASE_URL` to `http://localhost:11434/v1` and `COPILOT_PROVIDER_WIRE_API` to `responses`. Use `COPILOT_MODEL` to choose the model, and normally leave `COPILOT_PROVIDER_API_KEY` empty for a local instance.

</details>

<details><summary>How do you run Copilot CLI non-interactively through Ollama?</summary>

Run a command such as `ollama launch copilot --model kimi-k2.5:cloud --yes -- -p "how does this repository work?"`. The `--` separator ensures that `-p` is passed to Copilot CLI rather than interpreted by the Ollama launcher.

</details>

<details><summary>Why do these notes recommend models with at least a 64k-token context window?</summary>

Copilot CLI may need to reason across many repository files plus prior conversation history. A larger context window gives the model more room to consider that information together.

</details>

## Personal Notes

Using GitHub Copilot CLI with Ollama via the OpenAI-Compatible API

Source: https://docs.ollama.com/integrations/copilot-cli
Notion page: https://www.notion.so/Using-GitHub-Copilot-CLI-with-Ollama-via-the-OpenAI-Compatible-API-34701bb0839a8198b825ffe9a4af6f15

Tags: ollama, copilot-cli, openai-api, terminal-ai, llm, developer-tools

Overview

This lesson explains how to run GitHub Copilot CLI against models served by Ollama instead of a default hosted provider. The integration works because Copilot CLI can talk to an OpenAI-compatible API, and Ollama exposes one locally at `/v1`, letting you use local or Ollama cloud-hosted open models from the terminal.

This matters for engineers who want more control over model choice, local-first workflows, CI automation, or access to models like `qwen3.5`, `glm-5:cloud`, or `kimi-k2.5:cloud` while keeping the Copilot CLI terminal experience. If you build, review, or automate code from the shell, this setup gives you a flexible path to AI-assisted development without changing tools.

Key Concepts

  *   Copilot CLI: GitHub Copilot CLI is a terminal-based coding agent that can inspect a repository, answer questions about the codebase, propose edits, and run commands. It is designed for interactive shell workflows, but it can also run in non-interactive automation scenarios.
  *   Ollama as a model provider: Ollama can serve both local models and certain cloud models through a unified interface. In this integration, Ollama acts as the backend model provider that Copilot CLI sends requests to.
  *   OpenAI-compatible API: Copilot CLI connects to Ollama through environment variables that point it at an OpenAI-style API endpoint. The important base URL is `http://localhost:11434/v1`, which matches the API shape Copilot expects.
  *   Wire API selection: The `COPILOT_PROVIDER_WIRE_API=responses` setting tells Copilot CLI which request/response format to use when speaking to the provider. This ensures that the client and Ollama agree on the API semantics.
  *   Headless mode: Headless mode lets you run Copilot CLI without interactive prompts, which is useful in scripts, Docker containers, and CI/CD jobs. In this mode, `--yes` skips selectors and auto-pulls the model, but you must explicitly provide `--model`.
  *   Context window requirements: Copilot CLI works best with large-context models because it may need to ingest significant portions of a codebase and conversation history. Ollama recommends at least a 64k token context window for this integration.

How It Works

At a high level, the integration is straightforward: Copilot CLI remains the user-facing terminal agent, while Ollama becomes the LLM serving layer. Instead of Copilot CLI calling a default remote provider, it is configured to send requests to Ollama's OpenAI-compatible endpoint.

The simplest path is the Ollama-managed launcher:

```bash ollama launch copilot ```

This command starts Copilot CLI preconfigured to use Ollama. You can also select a model directly:

```bash ollama launch copilot --model kimi-k2.5:cloud ```

In this flow, Ollama handles the provider wiring for you, so you do not need to manually set environment variables first.

For more explicit control, you can configure Copilot CLI manually with environment variables:

```bash export COPILOT_PROVIDER_BASE_URL=http://localhost:11434/v1 export COPILOT_PROVIDER_API_KEY= export COPILOT_PROVIDER_WIRE_API=responses export COPILOT_MODEL=qwen3.5 copilot ```

The mechanics of each variable are:

- `COPILOT_PROVIDER_BASE_URL`: points Copilot CLI at the Ollama API. - `COPILOT_PROVIDER_API_KEY`: left empty here because a local Ollama server typically does not require an API key. - `COPILOT_PROVIDER_WIRE_API=responses`: selects the API style expected by this integration. - `COPILOT_MODEL`: names the model to use, such as `qwen3.5` or `glm-5:cloud`.

You can also provide these inline for
