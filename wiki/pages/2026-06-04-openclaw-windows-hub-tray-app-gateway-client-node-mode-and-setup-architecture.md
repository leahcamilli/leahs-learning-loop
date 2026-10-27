---
title: "OpenClaw Windows Hub: Tray App, Gateway Client, Node Mode, and Setup Architecture"
source: "https://github.com/openclaw/openclaw-windows-node"
date: "2026-06-04"
tags: [csharp, winui, websocket, windows, tray-app, wsl]
source_type: "github"
topics: []
kind: "deep-dive"
depth: 3
actionability: 1
---

## TL;DR

> OpenClaw Windows Hub separates gateway communication, connection management, setup, chat state, and Windows UI into reusable layers. This matters because the design supports resilient connectivity and independently enforced safety gates for remotely invoked Windows capabilities.

## Key Takeaways

1. Treat the gateway as the system’s runtime hub: status, sessions, channels, pairing, node registration, usage, and chat depend on a healthy WebSocket connection.
2. Keep protocol code outside the desktop UI; `OpenClaw.Shared` lets the tray app, CLI, and future frontends reuse gateway communication, models, identity handling, and safety checks.
3. Model connectivity explicitly with `GatewayConnectionManager`, `ConnectionStateMachine`, retry policies, credential resolution, gateway records, node registration, and optional SSH tunneling.
4. Gate node actions at multiple layers: device pairing, `gateway.nodes.allowCommands`, local `%LOCALAPPDATA%\OpenClawTray\exec-policy.json`, command and environment sanitization, and Windows capability consent.
5. Use the CLI to validate connection and message paths independently of WinUI, including direct testing with `--url`, `--token`, and `--message`.
6. Treat onboarding as a resilient workflow: the lesson describes setup pipelines, retries, transaction journaling, existing-configuration detection, cleanup, and a managed WSL gateway path.
7. Trace responsibilities by layer: CLI or tray UI → `OpenClaw.Connection` → `OpenClaw.Shared` WebSocket client → gateway; node requests return through policy checks before reaching Windows capabilities.

## Overview

OpenClaw Windows Hub is a C# monorepo that turns a Windows machine into both a desktop companion for OpenClaw and, optionally, a controllable node in the OpenClaw ecosystem. It combines a WinUI 3 tray application, a shared WebSocket client library, a connection-management layer, a setup engine, and a CLI validator. The system is designed to connect to a local or remote OpenClaw gateway, surface operational state in a Windows-native UX, and expose device capabilities like notifications, canvas control, screen capture, camera access, and command execution under policy control.

This repo matters if you build Windows-native integrations around AI assistants, need a reference architecture for a resilient tray app talking to a WebSocket gateway, or want to see how onboarding, device pairing, deep links, node capability advertisement, and Windows-specific permissions fit together in a production-oriented codebase. The interesting part is not just the UI: the architecture is split into reusable libraries for connection state, protocol access, setup orchestration, and local policy enforcement.

## Key Concepts

- **Companion suite monorepo**: The repository is organized as multiple focused projects rather than a single app. The tray UI, shared gateway client, connection logic, setup engine, chat state logic, and CLI are separate assemblies, which makes protocol logic reusable and testable outside the GUI.
- **Gateway-centric architecture**: The Windows app is fundamentally a client of an OpenClaw gateway over WebSocket. Most runtime features—status, sessions, channels, usage, pairing, node registration, and chat send—depend on maintaining a healthy gateway connection and interpreting gateway events correctly.
- **Connection state machine**: The repo isolates connection handling into OpenClaw.Connection with types like ConnectionStateMachine, GatewayConnectionManager, RetryPolicy, and GatewayRegistry. That separation suggests the app treats connection lifecycle, credentials, node mode, and SSH tunneling as first-class operational concerns instead of burying them in UI code.
- **Node mode with policy gates**: When node mode is enabled, the Windows host advertises commands the agent can invoke remotely. Sensitive actions such as command execution, screen recording, camera access, and TTS are bounded by both server-side allowlists and local execution policy files, reducing the chance of accidental overexposure.
- **Windows-native integration surfaces**: The tray app uses WinUI 3 and WebView2 to provide native system tray UX, embedded chat/canvas surfaces, toast notifications, deep-link handling, and onboarding windows. These are integrated with Windows startup, capability prompts, file-system settings, and IPC for forwarding deep links to a running instance.
- **Setup and managed local gateway flow**: The repo includes a dedicated setup engine and UI instead of relying only on manual configuration. It supports guided onboarding, setup codes, local/remote gateway choices, and a managed WSL-based local gateway path, which indicates installation and first-run success are treated as major product requirements.

## How It Works

The codebase is best understood as a layered Windows client stack.

At the bottom is **`OpenClaw.Shared`**, which contains protocol-facing and cross-cutting primitives. Important files here include:

- `OpenClawGatewayClient.cs`: the WebSocket client implementation for talking to the gateway
- `Models.cs`, `ChannelRecord.cs`, `ChannelsSnapshot.cs`, `NodeCapabilities.cs`: protocol/domain models
- `DeviceIdentity.cs`, `DeviceIdentityFileReader.cs`: device identity management support
- `DeepLinkParser.cs`: parsing `openclaw://...` URLs into app actions
- `ExecApprovalPolicy.cs`, `ExecShellWrapperParser.cs`, `ExecEnvSanitizer.cs`: execution policy and command sanitization logic
- `NotificationCategorizer.cs`: notification classification support

This project gives higher layers a stable API for gateway communication, data parsing, and local safety checks. The existence of both execution-policy and environment-sanitization code is a strong architectural signal: node-side command execution is not a raw shell passthrough.

The next layer is **`OpenClaw.Connection`**, which centralizes runtime connectivity concerns. Its files show the major responsibilities:

- `GatewayConnectionManager.cs`: coordinates connection lifecycle
- `ConnectionStateMachine.cs`: models state transitions and triggers
- `CredentialResolver.cs` / `InteractiveGatewayCredentialResolver.cs`: obtain gateway credentials or tokens
- `DeviceIdentityStore.cs`: persist local device identity used for authentication/pairing
- `GatewayRegistry.cs`, `GatewayRecord.cs`: track configured gateways or active targets
- `NodeConnector.cs`: bring node-mode registration into the connection flow
- `SshTunnelService.cs`: support managed SSH tunnel scenarios
- `OperatorScopeHelper.cs`: inspect scopes such as `operator.write` required for actions like Quick Send

This separation is important because the tray app has to deal with more than “connected vs disconnected.” It needs to distinguish operator connectivity, node connectivity, pairing required, missing scopes, local tunnel state, credential source, and configuration changes. The connection project acts as the orchestration layer between raw WebSocket transport and the UI.

On top of that sits **`OpenClaw.Tray.WinUI`** (described in the README, though its file list was not included in full). It is the Windows desktop frontend responsible for:

- system tray icon and flyout UI
- status pages such as Command Center and Activity
- embedded web chat via WebView2
- toast notifications and deep links
- settings persistence under `%APPDATA%\OpenClawTray\settings.json`
- startup behavior and first-run onboarding entry
- node mode status display and operator-facing diagnostics

The tray app consumes the connection manager and shared client library, then renders the gateway/node state into Windows-native surfaces. Deep links such as `openclaw://commandcenter`, `openclaw://activity`, or `openclaw://send?message=Hello` are parsed and routed internally; when a second invocation occurs while the app is already running, the request is forwarded via IPC rather than starting a duplicate UX flow.

The repo also includes **`OpenClaw.Chat`**, which contains files like `ChatTimelineReducer.cs` and `ChatModels.cs`. That suggests chat state is maintained using a reducer-style model rather than ad hoc UI mutations. Even without full source here, this points to a deliberate separation between chat event processing and presentation.

A distinct subsystem is the **setup engine**:

- `OpenClaw.SetupEngine`: core setup logic, logging, transaction journal, retries, default config, pipeline orchestration
- `OpenClaw.SetupEngine.UI`: Windows UI wrapper for setup
- `OpenClaw.SetupPreview`: likely a preview/test harness for setup UX

Key files include `SetupPipeline.cs`, `SetupSteps.cs`, `SetupWizardRunner.cs`, `TransactionJournal.cs`, `ExistingConfigDetector.cs`, and `TrayArtifactCleanup.cs`. This is more than an installer helper. It looks like a resilient workflow engine for first-run and local gateway provisioning, likely including rollback/retry semantics and structured logs. Combined with docs like `WSL_GATEWAY_ADMIN.md` and scripts validating WSL gateway behavior, the intended flow is: the Windows app can provision or work against a managed local gateway running in a dedicated WSL distro, then connect to it as an operator/node client.

The **CLI project** (`OpenClaw.Cli/Program.cs`) is a lightweight but useful operational tool. It reads the same tray settings when desired and can validate WebSocket connect/send/probe paths without launching the GUI. This is a good pattern in desktop systems: isolate the transport and protocol path so support engineers and CI can test connectivity independently of WinUI.

### Runtime data flow

A typical runtime flow looks like this:

1. The tray app starts and loads local settings from `%APPDATA%\OpenClawTray\settings.json`.
2. It initializes connection services from `OpenClaw.Connection`.
3. Credential resolution occurs, potentially using stored device identity, tokens, setup-code-derived values, or interactive configuration.
4. `OpenClawGatewayClient` establishes a WebSocket connection to the configured gateway.
5. The app subscribes to gateway state/events and builds snapshots for sessions, usage, channels, nodes, and health.
6. The tray UI renders this data into menu sections, Command Center pages, activity stream, and notification surfaces.
7. If node mode is enabled, the app advertises node capabilities and awaits pairing/approval on the gateway.
8. Approved node commands flow from the gateway back to the Windows client, where local policies and sanitizers decide whether and how to execute them.

### Node mode mechanics

Node mode effectively makes the Windows host an RPC endpoint under gateway control. The README lists commands in categories like system, canvas, screen, camera, STT, location, device, and TTS. The architecture enforces several gates:

- **Gateway-side allowlist**: commands must be explicitly allowed in `gateway.nodes.allowCommands`
- **Device pairing**: the Windows node must be approved as a device
- **Local exec policy**: command execution is filtered through `%LOCALAPPDATA%\OpenClawTray\exec-policy.json`
- **Environment sanitization**: dangerous environment variables are rejected
- **Windows permissions**: camera, microphone, and location may require system consent

That means the execution path is not simply “gateway says run; client runs.” It is closer to:

```text
Gateway invoke request
  -> paired/authorized node?
  -> command in server allowlist?
  -> local command/category supported?
  -> local exec approval rules permit it?
  -> wrapped shell command parsed and sanitized?
  -> protected Windows capability available/consented?
  -> execute and return structured result
```

### Why the architecture is practical

Several design choices stand out as production-friendly:

- **Protocol logic is decoupled from UI**, so the CLI and future tools can reuse it.
- **Connection handling is explicit**, with state machine and retry abstractions.
- **Onboarding is a dedicated subsystem**, not a one-off wizard embedded in the tray code.
- **Security boundaries are layered**, especially around remote execution and sensitive device capabilities.
- **Diagnostics are treated as product features**, with Command Center, activity streams, JSONL logs, support-context generation, and deep links for operational tasks.

### Build and packaging notes

The repo targets modern Windows with .NET 10, WinUI 3, and WebView2. The `build.ps1` script checks prerequisites and builds the suite. WinUI builds require a runtime identifier, and MSIX packaging is supported for capability prompts such as camera/microphone access. The root `package.json` exists only to pull `@microsoft/mxc-sdk`, used to copy `wxc-exec.exe` into the app output for the tray build, so this is primarily a .NET/C# repo with a small Node-based build dependency.

## Training Exercise

Build a mental model of the architecture by validating the connection path end to end, then inspect how node mode is gated.

### Goal

Use the CLI and project layout to trace how a message or node action would flow through the system, without needing to reverse-engineer every file.

### Steps

1. **Clone and build the repo**
   ```powershell
   git clone https://github.com/openclaw/openclaw-windows-node.git
   cd openclaw-windows-node
   .\build.ps1 -CheckOnly
   .\build.ps1
   ```

2. **Inspect the project boundaries**
   Open these files/directories and write down one sentence for each responsibility:
   - `src/OpenClaw.Shared/OpenClawGatewayClient.cs`
   - `src/OpenClaw.Connection/GatewayConnectionManager.cs`
   - `src/OpenClaw.Connection/ConnectionStateMachine.cs`
   - `src/OpenClaw.Connection/NodeConnector.cs`
   - `src/OpenClaw.Cli/Program.cs`
   - `src/OpenClaw.SetupEngine/SetupPipeline.cs`

3. **Run the CLI against your configured or local gateway**
   ```powershell
   dotnet run --project src/OpenClaw.Cli -- --help
   dotnet run --project src/OpenClaw.Cli -- --message "architecture validation"
   ```
   If you do not have tray settings configured, point it directly at a test gateway:
   ```powershell
   dotnet run --project src/OpenClaw.Cli -- --url ws://127.0.0.1:18789 --token "<token>" --message "override test"
   ```

4. **Trace the send path in code**
   Starting from `Program.cs`, follow the calls into shared/connection code and answer:
   - Where is the gateway URL sourced from?
   - Where is the token or identity resolved?
   - Which class actually sends over WebSocket?
   - Where would scope errors like `missing scope: operator.write` be detected or surfaced?

5. **Inspect node-mode safety controls**
   Read these files:
   - `src/OpenClaw.Shared/ExecApprovalPolicy.cs`
   - `src/OpenClaw.Shared/ExecShellWrapperParser.cs`
   - `src/OpenClaw.Shared/ExecEnvSanitizer.cs`

   Then summarize in a short note:
   - how wrapper commands are interpreted
   - which environment variables are considered risky
   - how local policy differs from gateway allowlists

6. **Optional: launch the tray app locally**
   ```powershell
   .\run-app-local.ps1 -NoBuild
   ```
   Open Command Center and compare what you see in the UI with the models and connection abstractions you identified in code.

### Deliverable

Produce a short architecture memo with three sections:

1. **Message send path**: CLI/UI -> connection layer -> shared gateway client -> gateway
2. **Node invoke path**: gateway -> node connector -> policy/sanitizer -> Windows capability/command execution
3. **Operational diagnostics**: where settings, logs, and support artifacts live

### Stretch task

Add a simple note or diagram showing which parts are reusable in another frontend. For example:

```text
Reusable core:
  OpenClaw.Shared
  OpenClaw.Connection
  OpenClaw.Chat

Windows-specific shell:
  OpenClaw.Tray.WinUI
  OpenClaw.SetupEngine.UI
```

This exercise forces you to connect the repository layout, runtime behavior, and security model into a coherent engineering understanding.

## Test Yourself

<details><summary>What are the main responsibilities of `OpenClaw.Shared` and `OpenClaw.Connection`?</summary>

The lesson describes `OpenClaw.Shared` as the reusable protocol layer containing the WebSocket client, domain models, identity support, deep-link parsing, and execution safeguards. `OpenClaw.Connection` orchestrates credentials, connection state, retries, configured gateways, tunnels, scopes, and node registration.

</details>

<details><summary>Why is node mode not equivalent to unrestricted remote shell access?</summary>

According to the lesson, an invocation must pass gateway authorization and allowlists, device pairing, local capability support, execution policy, wrapper and environment sanitization, and any required Windows permission checks. These independent gates limit what the gateway can cause the Windows host to do.

</details>

<details><summary>How would you validate the message-send architecture without launching the tray application?</summary>

Run `OpenClaw.Cli` using existing tray settings or supply a gateway URL and token directly, then trace calls from `Program.cs` through the connection layer to `OpenClawGatewayClient`. Check where the URL and credentials are resolved, which method performs the WebSocket send, and where missing scopes such as `operator.write` surface.

</details>

## Further Reading

- [OpenClaw Windows Hub Repository](https://github.com/openclaw/openclaw-windows-node)
- [OpenClaw Windows Platform Documentation](https://docs.openclaw.ai/platforms/windows)
- [WinUI 3 Documentation](https://learn.microsoft.com/windows/apps/winui/winui3/)
- [WebView2 Documentation](https://learn.microsoft.com/microsoft-edge/webview2/)
- [ClientWebSocket Class in .NET](https://learn.microsoft.com/dotnet/api/system.net.websockets.clientwebsocket)
