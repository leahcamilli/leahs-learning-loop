---
title: "Auto DCA: Browser-Native Arps Decline-Curve Analysis in TypeScript"
source: "https://github.com/workollab/auto-dca"
date: "2026-06-06"
tags: [decline-curve-analysis, typescript, react, forecasting, optimization, oil-gas]
source_type: "github"
topics: [ai-models]
kind: "deep-dive"
depth: 3
actionability: 2
---

## TL;DR

> Auto DCA performs oil-and-gas decline-curve analysis entirely in the browser while keeping its TypeScript engine separate from the React UI. Its cross-validated model selection and parity tests against Equinor’s Python implementation aim to make private, portable forecasts numerically trustworthy.

## Key Takeaways

1. Fit exponential, harmonic, and hyperbolic Arps models, then select among them using expanding-window cross-validation rather than in-sample fit alone.
2. Use AICc as a fallback or tie-breaker when a production series is short or competing models perform similarly.
3. Fit positive production rates in log-space with a robust p-norm loss where p = 1.4, using transformed parameters, Nelder–Mead optimization, and multi-start initialization.
4. Apply Modified Arps terminal decline to switch an optimistic hyperbolic tail smoothly to exponential decline once it reaches Dmin.
5. Test sensitivity by changing terminal-decline and economic-limit assumptions; the lesson predicts these choices will affect EUR more than the fitted historical parameters.
6. Keep scientific logic in the reusable @workollab/auto-dca-engine package so formulas, optimization, forecasting, parsing, and diagnostics can be tested independently of the React interface.
7. Use golden fixtures from Equinor’s Python implementation as an executable specification; the project reports parity on real field data within 0.02 ppm.

## Overview

Auto DCA is a monorepo that implements decline-curve analysis (DCA) for oil and gas wells entirely in the browser. It rebuilds Equinor's Python-based decline-curve-analysis engine as a dependency-free TypeScript library, then wraps it with a Vite/React frontend for CSV upload, model fitting, forecasting, EUR estimation, diagnostics, and confidence bands. The key promise is privacy and portability: production data never leaves the user's machine, yet the numerical results are validated against a known industry reference implementation.

This project matters to engineers working on scientific computing in the browser, petroleum analytics, or client-side data products. It is also a useful case study in translating a numerically sensitive Python workflow into TypeScript while preserving parity, structuring a reusable engine separate from UI concerns, and building trust through golden tests against a reference codebase.

## Key Concepts

- **Arps decline families**: The engine fits the three classic Arps decline models: exponential, harmonic, and hyperbolic. These models describe how production rate decreases over time using parameters such as initial rate, nominal decline, and the hyperbolic exponent b. The winning family is chosen automatically rather than assumed up front.
- **Cross-validated model selection**: Instead of picking the model with the best in-sample fit, Auto DCA uses expanding-window cross-validation to score forecast performance on held-out future slices. This is more robust when late-life production contains anomalies such as workovers or recompletions. AICc acts as a fallback or tie-breaker for short series.
- **Robust log-space fitting**: Model fitting happens in log-space using a p-norm loss with p = 1.4, which is less sensitive to noisy points than ordinary least squares. This makes the fitter more tolerant of real production data irregularities while still preserving the exponential-like structure of decline behavior.
- **Unconstrained optimization via reparameterization**: Engineering parameters like qi, Di, and b naturally have bounds or positivity constraints. The engine avoids explicit box constraints by optimizing over an unbounded transformed parameter space, then mapping the solution back into physical parameters. That keeps the optimizer simpler and reduces edge-case behavior.
- **Modified Arps terminal decline**: Hyperbolic decline can produce overly optimistic long tails, so many reserves workflows switch to an exponential tail once decline slows below a minimum decline rate Dmin. Auto DCA supports this Modified Arps behavior and computes the switch point as a smooth C1 transition.
- **Reference parity testing**: The repository vendors Equinor's original Python implementation under reference/ and uses generated golden outputs to verify the TypeScript engine. This is a strong engineering pattern for ports or rewrites: use a trusted implementation as an executable specification and continuously compare outputs.

## How It Works

The repository is split into two primary workspaces and one validation area:

- `engine/`: the reusable TypeScript DCA library published as `@workollab/auto-dca-engine`
- `app/`: a Vite + React + Tailwind frontend that consumes the engine
- `reference/`: a vendored copy of Equinor's Python implementation plus fixture-generation scripts

At a high level, the data flow is:

1. The user loads production data in the React app.
2. The app parses and normalizes the input into elapsed time and rate arrays.
3. The engine fits all Arps families, evaluates diagnostics, selects the best model, and generates a forecast.
4. The app renders charts, result cards, comparison tables, and exportable forecast CSVs.
5. Tests compare the engine's output against golden data generated from the Python reference.

### Engine structure

The engine is intentionally modular, with each source file handling a narrow part of the workflow:

- `engine/src/auto.ts`: orchestration entry point; this is where `autoDCA(...)` likely coordinates fitting, selection, forecasting, and uncertainty generation.
- `engine/src/models.ts`: mathematical definitions for the Arps families and probably rate/cumulative calculations.
- `engine/src/fit.ts`: fitting routines for each model family, including parameter preparation and interaction with the optimizer.
- `engine/src/loss.ts`: robust loss logic, including the p-norm objective in log-space.
- `engine/src/optimize.ts`: from-scratch Nelder-Mead simplex optimizer and multi-start strategy.
- `engine/src/forecast.ts`: forward projection logic, Modified Arps terminal-decline handling, EUR integration, and horizon/economic-limit calculations.
- `engine/src/diagnostics.ts`: metrics such as R², RMSE, and model comparison outputs.
- `engine/src/csv.ts`: parsing and auto-detection of time/rate columns from uploaded CSVs.
- `engine/src/index.ts`: public package exports.

This separation is important: the mathematical models, optimizer, and application-facing orchestration are not tangled together. That makes it feasible to test closed-form formulas independently from optimizer behavior and to use the engine outside the demo UI.

### Fitting pipeline

The core fitting pipeline follows the methodology summarized in the README and formalized in `docs/MATH_SPEC.md`:

1. **Preprocess data**
   - Keep positive production rates.
   - Sort rows by time.
   - Convert date-like columns into elapsed months when needed.
   - Drop empty or non-positive rows.

2. **Fit each Arps family**
   - Evaluate exponential, harmonic, and hyperbolic candidates.
   - Fit in log-space, which is natural for declining-rate data and stabilizes optimization.
   - Use a robust p-norm loss instead of plain least squares.
   - Optimize over an unconstrained transformed space with Nelder-Mead.
   - Use multi-start initialization to reduce the chance of landing in a poor local optimum.

3. **Select the best forecasting model**
   - Use expanding-window cross-validation: fit on an initial prefix, test on the next slice, then repeat with more history.
   - Aggregate forecast errors across folds.
   - Use AICc if the series is too short or models are close.

4. **Generate forecast and EUR outputs**
   - Forecast rates forward in time from the selected fit.
   - Optionally apply terminal decline for hyperbolic tails using `terminalDecline` / `Dmin`.
   - Compute EUR to economic limit, to a finite horizon, and to infinity when the integral is finite.
   - Produce confidence bands with a residual bootstrap.

### UI structure

The React app is a thin consumer of the engine rather than a place where domain logic lives.

- `app/src/App.tsx`: top-level composition, likely wiring uploader, fit state, and results.
- `app/src/components/Uploader.tsx`: CSV ingestion and sample loading.
- `app/src/components/DeclineChart.tsx`: visualization of history, fit, forecast, confidence band, and markers such as economic limit or terminal switch.
- `app/src/components/FitAnimation.tsx`: animates model trials and convergence for the demo experience.
- `app/src/components/ModelTable.tsx`: comparison of exponential/harmonic/hyperbolic results.
- `app/src/components/ResultCards.tsx`: surfaced outputs such as best model parameters, diagnostics, and EUR.
- `app/src/lib/useFitPlayback.ts`: likely drives the fit animation state machine.
- `app/src/lib/format.ts`: formatting helpers for dates, units, and displayed metrics.

Because the engine is packaged separately, the UI can remain mostly stateless with respect to numerical details. That is a good architecture for maintainability and future embedding in other apps.

### Validation and reference architecture

A standout part of this repo is the validation workflow:

- `reference/decline-curve-analysis/` contains Equinor's original Python package.
- `reference/generate_golden.py` produces canonical fixtures used by the TypeScript tests.
- `engine/test/parity.test.ts` verifies that TypeScript outputs match the reference closely.
- `engine/test/models.test.ts` and `engine/test/csv.test.ts` cover formulas and parsing behavior.
- `engine/test/golden/` stores synthetic and real-well fixtures.

This gives the port a measurable correctness target. Rather than claiming conceptual similarity, the project demonstrates numerical parity on real field data to within 0.02 ppm.

### Typical API usage

The public API is intentionally simple:

```ts
import { autoDCA } from '@workollab/auto-dca-engine';

const t = [0, 1, 2, 3, 4, 5];
const q = [1000, 940, 890, 850, 810, 775];

const result = autoDCA(t, q, {
  economicLimit: 50,
  terminalDecline: 0.005,
});

console.log(result.selection.best.model);
console.log(result.selection.best.fit.params);
console.log(result.forecast.eur.toEconomicLimit);
console.log(result.band);
```

The result object bundles selection details, fitted parameters, forecast outputs, and uncertainty information in one return value, making it easy for downstream consumers to build either dashboards or batch workflows.

## Training Exercise

Build a small local workflow that uses the engine directly, then compare the result to what the browser app shows.

### Goal

Fit a simple well decline series, inspect the chosen Arps model, and experiment with terminal decline and economic limit assumptions.

### Steps

1. **Clone and install**

```bash
git clone https://github.com/workollab/auto-dca.git
cd auto-dca
npm install
npm run build:engine
```

2. **Run the demo app once**

```bash
npm run dev
```

Open `http://localhost:5173` and load one of the bundled sample wells so you understand the expected outputs.

3. **Create a quick engine script**

Create `scratch.mjs` in the repo root:

```js
import { autoDCA } from './engine/dist/index.js';

const t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
const q = [1200, 1110, 1035, 970, 915, 865, 820, 780, 744, 710];

const result = autoDCA(t, q, {
  economicLimit: 100,
  terminalDecline: 0.005,
});

console.log('Best model:', result.selection.best.model);
console.log('Params:', result.selection.best.fit.params);
console.log('EUR to economic limit:', result.forecast.eur.toEconomicLimit);
console.log('Terminal switch time:', result.forecast.terminalSwitchTime);
console.log('R2:', result.selection.best.fit?.diagnostics?.r2 ?? 'n/a');
```

Run it:

```bash
node scratch.mjs
```

4. **Change assumptions**
   - Re-run with `terminalDecline` removed.
   - Re-run with `economicLimit: 50` and then `economicLimit: 200`.
   - Observe how EUR changes more than fit parameters do.

5. **Inspect the code path**
   - Open `engine/src/auto.ts` and trace the sequence of calls.
   - Open `engine/src/fit.ts`, `optimize.ts`, and `forecast.ts` to identify where each output in `result` is produced.
   - Write down which module is responsible for each of these: parameter estimation, model ranking, terminal switch logic, and confidence band generation.

6. **Run tests**

```bash
npm run test:engine
```

Pay special attention to parity tests and CSV tests. Note how the project establishes trust in a numerical rewrite.

### Stretch exercise

Add a second script that reads a CSV file with `date,oil_rate` columns, uses the parser from `engine/src/csv.ts`, then passes the parsed arrays into `autoDCA`. Compare your CLI result to the browser result for the same file.

### What you should learn

By the end, you should be able to explain:
- why the engine is split from the UI,
- how Auto DCA chooses among Arps families,
- how terminal decline changes reserves-style forecasts,
- and how parity tests de-risk a Python-to-TypeScript scientific port.

## Test Yourself

<details><summary>How does Auto DCA choose among exponential, harmonic, and hyperbolic Arps models?</summary>

It fits all three families and primarily compares their forecasting errors through expanding-window cross-validation on held-out future slices. The lesson says AICc is used when the series is too short or results are close.

</details>

<details><summary>Why does Auto DCA support a terminal decline rate for hyperbolic forecasts?</summary>

An unrestricted hyperbolic curve can produce an overly optimistic long tail. Modified Arps switches smoothly to exponential decline when the decline rate reaches Dmin, producing a more conservative reserves-style forecast.

</details>

<details><summary>How does the repository build confidence in its Python-to-TypeScript numerical rewrite?</summary>

It vendors Equinor’s Python implementation, generates golden outputs from that reference, and compares the TypeScript engine against those fixtures in parity tests. Separate model and CSV tests also isolate formula and parsing behavior.

</details>

## Further Reading

- [Auto DCA Repository](https://github.com/workollab/auto-dca)
- [Equinor decline-curve-analysis Reference Repository](https://github.com/equinor/decline-curve-analysis)
- [Nelder–Mead Method](https://en.wikipedia.org/wiki/Nelder%E2%80%93Mead_method)
- [Arps Decline Equations Overview](https://petrowiki.spe.org/Decline_curve_analysis)
- [Vite Guide](https://vitejs.dev/guide/)
