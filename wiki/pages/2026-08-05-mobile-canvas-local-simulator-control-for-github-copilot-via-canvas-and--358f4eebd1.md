---
title: "Mobile Canvas: local simulator control for GitHub Copilot via canvas and MCP"
source: "https://github.com/Redth/mobile-canvas-ghcp"
date: "2026-08-05"
tags: [csharp, mcp, mobile-testing, simulators, developer-tools]
source_type: "github"
source_fingerprint: "358f4eebd1"
source_characters: 14473
topics: [github-copilot, mcp, ai-agents, developer-tools]
kind: "deep-dive"
depth: 3
actionability: 2
---

## TL;DR

> Mobile Canvas uses a loopback-only local host as the shared control plane for humans and agents to discover, boot, view, and control mobile simulators. Its key architectural advantage is parity between 24 canvas actions and 24 MCP tools, while platform-specific behavior stays behind separate iOS and Android backends.

## Key Takeaways

1. Use the per-user `mobile-canvas host` as the system of record for both the canvas UI and MCP clients; it binds to `127.0.0.1`, authenticates panels with a bootstrap secret, and exits after an idle period.
2. Keep human and agent capabilities aligned: the README states that 24 canvas actions map one-to-one to 24 `mobile_device_*` MCP tools.
3. Put shared device coordination in `src/MobileCanvas.Core`, tool definitions in `src/MobileCanvas.Tool/Mcp`, and platform command execution in the iOS and Android backend projects.
4. Decouple video capture from input handling to reduce bandwidth and isolate failures; iOS uses ScreenCaptureKit plus `idb`, while Android uses emulator gRPC with frames encoded before reaching the browser.
5. Treat prebuilt files under `runtimes/` as product artifacts: changes affecting shipped executables must be rebuilt and recommitted because installations run the bundle rather than the raw source tree.
6. Republish after changing `web/` because those assets are embedded in the binary; `extension.mjs` is copied separately and follows a different packaging path.
7. Account for platform constraints: iOS support requires macOS, Xcode simulators, and `idb_companion`, while Android is cross-platform but uses screenshot polling for video on non-macOS systems.

## Overview

This repository shows how to turn local mobile simulators into an interactive tool surface for both humans and agents. It packages a GitHub Copilot canvas extension, a CLI/MCP server, platform-specific iOS and Android backends, embedded web UI assets, and prebuilt runtime bundles. The practical lesson is that the project is not just a viewer: it is a loopback-only local control plane for discovering devices, booting them, streaming their screens, sending input, and exposing the same actions to an agent through MCP.

## Key Concepts

- **Canvas and MCP parity**: The README states that 24 canvas actions map one-to-one to 24 MCP tools named `mobile_device_*`. This makes the UI and automation surface consistent, so an agent can perform the same operations a human can trigger from the canvas.
- **Per-user local host**: The observed architecture centers on a `mobile-canvas host`, described as a per-user singleton that starts on demand, binds only to `127.0.0.1`, authenticates canvas panels with a bootstrap secret, and exits after an idle period. This keeps the system local-first and avoids implicitly shutting down devices.
- **Platform backends split by responsibility**: The repo separates cross-platform logic from device-specific implementations. `src/MobileCanvas.Core` holds shared service and process-running logic, while `src/MobileCanvas.iOS` and `src/MobileCanvas.Android` implement lifecycle, input, parsing, recording, and live-video behavior for each platform.
- **Video and input are intentionally decoupled**: The README explicitly says video is split from input on both platforms. On iOS, capture uses ScreenCaptureKit and input uses `idb`; on Android, emulator gRPC handles both video and input, with encoding done before frames reach the browser. This separation supports lower-bandwidth streaming and clearer failure boundaries.
- **Shipped binaries are part of the product**: The file tree includes `runtimes/` with prebuilt compressed binaries for multiple platforms and a native Swift helper under `native/mobile-screencap`. The README warns that source changes affecting shipped executables require rebuilding and recommitting runtime artifacts because plugin installs execute that bundle, not the raw source tree.
- **Embedded web UI with a copied extension shell**: The lesson from the development notes is that `web/` assets are embedded resources inside the binary, while `extension.mjs` is copied directly. That affects iteration: web changes need republishing, but extension changes do not follow the same packaging path.

## How It Works

At a high level, the Copilot app loads `extension.mjs`, which exposes canvas actions to a local host. That host also serves the browser-facing UI over HTTP/WebSocket and exposes MCP over stdio for VS Code, CLI, or agent use. Shared contracts live in `src/MobileCanvas.Contracts`, reusable orchestration lives in `src/MobileCanvas.Core`, and the executable entrypoint is in `src/MobileCanvas.Tool` with grouped MCP tool files such as `DeviceDiscoveryTools.cs`, `DeviceLifecycleTools.cs`, `DeviceInteractionTools.cs`, and `DeviceMediaTools.cs`. iOS support is macOS-only and depends on Xcode simulators plus `idb_companion`; Android support depends on the Android SDK tools and works cross-platform, though non-macOS video falls back to screenshot polling. The repository also includes scripts for build, install, bundle verification, and release, plus tests covering parsers, CLI behavior, services, serialization, and UI tree logic. A practical architectural pattern to reuse here is: keep a shared local host as the system of record, let both UI and agent clients talk to it, and keep device-specific code behind backend interfaces rather than inside the UI layer.

## Training Exercise

Map one end-to-end flow without assuming anything beyond the repository. Start from the README's agent flow `list -> select -> read udid -> deploy -> drive input`. Then inspect the file tree conceptually: use `src/MobileCanvas.Tool/Mcp/DeviceDiscoveryTools.cs` and `DeviceInteractionTools.cs` as the MCP surface, `src/MobileCanvas.Core/DeviceService.cs` as shared orchestration, and `src/MobileCanvas.iOS/IosSimulatorBackend.cs` or `src/MobileCanvas.Android/AndroidEmulatorBackend.cs` as concrete execution paths. Write a short note answering three questions: which layer owns tool definitions, which layer owns cross-platform device coordination, and which files likely hold platform-specific command execution. As a stretch goal, explain why the repo keeps `web/` embedded but `extension.mjs` copied separately, and what that implies for rebuilding after UI changes.

## Test Yourself

<details><summary>Which layers own MCP tool definitions, shared device coordination, and platform-specific execution?</summary>

MCP tool definitions live in `src/MobileCanvas.Tool/Mcp`, shared coordination lives in `src/MobileCanvas.Core`, and concrete execution lives in `src/MobileCanvas.iOS` or `src/MobileCanvas.Android`.

</details>

<details><summary>Why does one-to-one parity between canvas actions and MCP tools matter?</summary>

It gives human users and agents the same operational surface, reducing duplicated logic and making UI-triggered workflows reproducible through automation.

</details>

<details><summary>What rebuilding implications follow from the repository&#x27;s packaging model?</summary>

Changes to embedded `web/` assets require republishing, and changes affecting shipped executables require rebuilding and recommitting the runtime bundles. `extension.mjs` is copied separately, so it does not use the same embedded-resource path.

</details>

## Further Reading

- [Redth/mobile-canvas-ghcp](https://github.com/Redth/mobile-canvas-ghcp)
- [idb_companion / fbidb](https://fbidb.io)
