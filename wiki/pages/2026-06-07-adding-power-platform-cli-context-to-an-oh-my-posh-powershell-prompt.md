---
title: "Adding Power Platform CLI Context to an oh-my-posh PowerShell Prompt"
source: "https://github.com/jukkan/oh-my-pac"
date: "2026-06-07"
tags: [powershell, oh-my-posh, power-platform, pac, cli]
source_type: "github"
topics: [developer-tools]
kind: "deep-dive"
depth: 3
actionability: 2
---

## TL;DR

> Display the active Power Platform CLI authentication context in the PowerShell prompt to reduce the risk of running commands against the wrong environment or tenant. The repository keeps prompt rendering fast by caching a label from `pac auth who` in `PAC_CONTEXT` and refreshing it after authentication changes.

## Key Takeaways

1. Treat the shell prompt as an operational guardrail by keeping the active PAC environment or tenant visible at all times.
2. The repository derives `PAC_CONTEXT` from `pac auth who`, preferring `Organization Friendly Name`, then `Organization Unique Name`, then the username prefix.
3. Store the context label in the `PAC_CONTEXT` environment variable so oh-my-posh does not invoke PAC every time it redraws the prompt.
4. Refresh `PAC_CONTEXT` after successful `pac auth create`, `select`, `delete`, `update`, `name`, or `clear` operations to prevent stale prompt state.
5. Keep state discovery, prompt presentation, and profile installation separate so each layer can be changed independently.
6. Use the manual `Refresh-PacContext` function when PAC state changes outside the wrapper or the displayed context appears stale.
7. Resolve `pac.exe` from `PATH` instead of hard-coding its installation directory to make the setup more portable across developer machines.

## Overview

This repository shows how to surface the active Microsoft Power Platform CLI authentication context directly in a PowerShell prompt powered by oh-my-posh. Instead of manually running `pac auth who` to confirm which environment or tenant is active, the prompt displays a short, readable label derived from the current PAC auth profile.

This matters for engineers who work across multiple Power Platform environments, tenants, or customer contexts and want a low-friction guardrail against running commands in the wrong place. The implementation is intentionally small: a helper script computes a context label, a custom oh-my-posh theme renders it, and an installer updates the PowerShell 7 profile so the prompt stays in sync when PAC auth commands change the active profile.

## Key Concepts

- **Prompt context as operational safety**: The main idea is to move environment awareness into the shell prompt so it is always visible. For tools like the Power Platform CLI, where auth profiles determine which org and tenant commands operate against, this reduces mistakes caused by stale mental context.
- **PAC auth inspection**: The repository relies on `pac auth who` as the source of truth for the current authentication context. The helper script extracts a human-friendly identifier from that command's output and prefers organization labels over lower-value identifiers like usernames.
- **Environment-variable bridge**: Rather than having oh-my-posh call `pac` directly on every prompt render, the design stores the computed label in an environment variable named `PAC_CONTEXT`. This decouples prompt rendering from CLI parsing and keeps the segment simple and fast.
- **Custom oh-my-posh theme segment**: The repo includes a dedicated theme JSON file that adds a Power Apps-style prompt segment. That segment reads the computed context label and renders it with a distinctive color so the active PAC profile stands out visually.
- **PowerShell command wrapping**: The installer updates the PowerShell profile to introduce a wrapper around the `pac` command. For auth-changing subcommands such as `pac auth select` and `pac auth create`, the wrapper refreshes the stored context automatically after successful execution.
- **Idempotent profile installation**: The installation script is intended to be safely rerun. It copies support files into a stable config location and updates the user's PowerShell 7 profile so the setup becomes part of the normal shell startup path.

## How It Works

The repository is organized around three Windows/PowerShell assets:

- `scripts/windows/pac-context.ps1`
- `scripts/windows/oh-my-posh-pac.omp.json`
- `scripts/windows/install-pac-omp.ps1`

At a high level, the data flow is:

1. PowerShell starts and loads the user's profile.
2. The profile imports or defines a `Refresh-PacContext` helper.
3. That helper invokes `pac auth who` using `pac.exe` resolved from `PATH`.
4. The helper parses the output and chooses the best display label in priority order:
   - `Organization Friendly Name`
   - `Organization Unique Name`
   - username prefix fallback
5. The chosen value is written to the `PAC_CONTEXT` environment variable.
6. oh-my-posh initializes with the repo's custom theme.
7. The theme renders a dedicated segment based on `PAC_CONTEXT`.

The helper script is the core integration point. Its purpose is not to do full PAC profile management, but to cheaply answer one question: "what label should the prompt show right now?" The repository description indicates that it dynamically resolves `pac.exe` from `PATH`, which avoids hard-coding an installation location. That makes the setup more portable across developer machines where PAC may be installed via different mechanisms.

The parsing strategy is pragmatic. `pac auth who` exposes several fields, but not all are equally useful in a prompt. An organization-friendly name is typically the best user-facing identifier because it maps closely to how engineers think about environments. If that value is absent, the script falls back to the unique organization name, and then finally to a user-derived identifier. This priority ordering is what turns raw CLI output into something compact and glanceable.

The oh-my-posh theme file is the presentation layer. While the source excerpt does not include the raw JSON contents, the README makes clear that the theme adds a purple Power Apps-style segment dedicated to PAC context. In practice, this means the segment is likely defined as a text or environment-driven block that reads `PAC_CONTEXT` and emits a symbol plus the chosen label, for example:

```text
 Jukka PAYG
```

The installer script handles system integration. Its responsibilities are broader than just copying files:

- copy the helper and theme into `~/.config/oh-my-posh/`
- update the current user's PowerShell 7 profile
- add a `Refresh-PacContext` function
- wrap the `pac` command so certain auth operations trigger a refresh
- initialize oh-my-posh with the PAC-aware theme

That wrapper behavior is the most interesting architectural choice in the repo. Instead of expecting the user to manually run `Refresh-PacContext` after changing PAC auth state, the profile intercepts calls to `pac` and checks whether the subcommand is one of the auth-mutating operations:

- `pac auth create`
- `pac auth select`
- `pac auth delete`
- `pac auth update`
- `pac auth name`
- `pac auth clear`

If one of those commands succeeds, the wrapper refreshes `PAC_CONTEXT` so the prompt in the same terminal session reflects the new state immediately. This keeps the prompt accurate without forcing a new shell session.

From a code-architecture standpoint, the repo is a good example of shell customization split into three layers:

- **state discovery**: `pac-context.ps1` asks PAC for the active auth context
- **presentation**: `oh-my-posh-pac.omp.json` renders that state in the prompt
- **bootstrapping and lifecycle**: `install-pac-omp.ps1` wires everything into the user's profile and refresh flow

This separation is useful because each part can evolve independently. You could swap the theme without changing PAC parsing, or adapt the helper to another shell while preserving the same context-selection logic.

One practical design tradeoff is storing context in an environment variable instead of evaluating `pac auth who` every prompt render. That reduces prompt latency and avoids repeated CLI invocations, which is especially important for shells where the prompt is redrawn frequently. The cost is that the value can become stale unless refreshed explicitly or via command wrapping; the repository addresses that with both automatic refresh on known auth mutations and a manual `Refresh-PacContext` command.

## Training Exercise

Build and test a minimal PAC-aware PowerShell prompt segment yourself.

1. **Verify prerequisites**
   Make sure these commands work in PowerShell 7:

   ```powershell
   oh-my-posh --version
   pac help
   ```

2. **Inspect current PAC context manually**
   Run:

   ```powershell
   pac auth who
   ```

   Note which fields appear in your output, especially any organization-friendly or unique name values.

3. **Create a simple context refresh function**
   In a temporary PowerShell session, define:

   ```powershell
   function Refresh-PacContext {
       $output = pac auth who 2>$null
       if (-not $output) {
           $env:PAC_CONTEXT = "no-pac-context"
           return
       }

       $friendly = ($output | Select-String "Organization Friendly Name").ToString()
       $unique = ($output | Select-String "Organization Unique Name").ToString()
       $user = ($output | Select-String "User").ToString()

       if ($friendly -match ":\s*(.+)$") {
           $env:PAC_CONTEXT = $matches[1].Trim()
       }
       elseif ($unique -match ":\s*(.+)$") {
           $env:PAC_CONTEXT = $matches[1].Trim()
       }
       elseif ($user -match ":\s*([^@\s]+)") {
           $env:PAC_CONTEXT = $matches[1].Trim()
       }
       else {
           $env:PAC_CONTEXT = "unknown"
       }
   }
   ```

4. **Run the function and inspect the result**

   ```powershell
   Refresh-PacContext
   $env:PAC_CONTEXT
   ```

5. **Create a minimal oh-my-posh config**
   Save this as `pac-demo.omp.json`:

   ```json
   {
     "$schema": "https://raw.githubusercontent.com/JanDeDobbeleer/oh-my-posh/main/themes/schema.json",
     "blocks": [
       {
         "type": "prompt",
         "alignment": "left",
         "segments": [
           {
             "type": "text",
             "style": "powerline",
             "foreground": "#ffffff",
             "background": "#7b2cbf",
             "template": "  {{ env . \"PAC_CONTEXT\" }} "
           }
         ]
       }
     ]
   }
   ```

6. **Preview the theme**

   ```powershell
   oh-my-posh init pwsh --config .\pac-demo.omp.json | Invoke-Expression
   ```

   Your prompt should now show the current PAC context label.

7. **Simulate an auth change workflow**
   If you have multiple auth profiles configured, switch one:

   ```powershell
   pac auth list
   pac auth select --index 1
   Refresh-PacContext
   ```

   Confirm the prompt label changes after refresh.

8. **Extend the exercise**
   Add your own wrapper function around `pac` that calls the real executable and then runs `Refresh-PacContext` whenever the arguments start with `auth select` or `auth create`. This reproduces the key behavior of the repository and helps you understand how profile-based command interception works in PowerShell.

Success criteria:

- `PAC_CONTEXT` is populated from `pac auth who`
- the prompt displays that value through oh-my-posh
- changing PAC auth context updates the prompt after refresh
- you can explain why the repository uses an environment variable instead of executing PAC directly in the prompt segment

## Test Yourself

<details><summary>Why does the repository write the PAC context to an environment variable instead of running `pac auth who` during every prompt render?</summary>

Caching the label in `PAC_CONTEXT` avoids repeated CLI calls and reduces prompt latency. The tradeoff is possible staleness, which the repository addresses with automatic and manual refresh mechanisms.

</details>

<details><summary>What priority order does the helper use when selecting the prompt label?</summary>

It prefers `Organization Friendly Name`, falls back to `Organization Unique Name`, and then uses the username prefix. This turns PAC output into a compact label that is useful at a glance.

</details>

<details><summary>How does the prompt remain synchronized after the active PAC authentication profile changes?</summary>

The PowerShell profile wraps `pac` and refreshes `PAC_CONTEXT` after successful auth-mutating commands such as `pac auth select` or `pac auth create`. A user can also call `Refresh-PacContext` manually.

</details>

## Further Reading

- [oh-my-posh Documentation](https://ohmyposh.dev/)
- [oh-my-posh Configuration Reference](https://ohmyposh.dev/docs/configuration/overview)
- [Microsoft Power Platform CLI Overview](https://learn.microsoft.com/power-platform/developer/cli/introduction)
- [PowerShell Profiles](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_profiles)
