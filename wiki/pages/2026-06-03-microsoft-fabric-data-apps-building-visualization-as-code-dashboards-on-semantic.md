---
title: "Microsoft Fabric Data Apps: Building Visualization-as-Code Dashboards on Semantic Models"
source: "https://tabulareditor.com/blog/fabric-apps-explained-visualization-as-code-in-a-data-app-dashboard"
date: "2026-06-03"
tags: [fabric, powerbi, dax, vega-lite, react, webapps]
source_type: "web"
topics: [power-bi-and-fabric, data-and-analytics]
kind: "deep-dive"
depth: 3
actionability: 2
---

## TL;DR

> A Microsoft Fabric data app is a code-first web frontend that queries a governed semantic model with DAX and renders results with libraries such as Vega-Lite or D3.js. It enables more customized analytics experiences than Power BI reports, but teams must manage it as a software project with source control, testing, deployment, and governance.

## Key Takeaways

1. Treat each data app visual as a software assembly: a `.dax` query template retrieves data, a `.json` specification defines the visualization, and a `.ts` file connects the query, filters, metadata, and renderer.
2. Use placeholders such as `{{YEAR}}`, `{{FILTERS}}`, and `{{TOPN}}` in DAX templates, then replace them from TypeScript at runtime to implement slicers, drill context, and cross-filtering.
3. Validate the final substituted DAX in DAX Studio or Tabular Editor before connecting it to a visual; visible query logic can be inspected, tested, and optimized directly.
4. Keep governed metrics and security in the semantic model while using the data app as a customizable presentation layer; the lesson says the user's Entra identity allows configured model permissions and row-level security to apply.
5. Choose Vega-Lite for declarative chart specifications and helper-supported behavior; choose D3.js or another library when greater freedom justifies implementing more behavior yourself.
6. Use the CLI workflow described in the lesson: scaffold with `bun create @microsoft/rayfin@latest`, preview with `bun run dev`, and deploy with `bunx rayfin up`.
7. Apply normal web engineering discipline—including consistent styling, code review, automated testing, CI/CD, and scrutiny of AI-generated code—because a data app is not a low-code report artifact.

## Overview

Microsoft Fabric Apps introduce a code-first way to build and host browser-based applications inside Fabric. One important template type, the data app, lets engineers connect a web app directly to a published semantic model and query it with DAX, then render the results with libraries such as Vega-Lite or D3.js. This effectively brings visualization-as-code to the Fabric ecosystem.

This matters for BI engineers, analytics engineers, and frontend developers who want more control than Power BI reports offer. Data apps trade low-code convenience for flexibility: every query, visual spec, interaction, and layout is authored in code, which enables highly bespoke dashboards and integrations but also introduces software engineering concerns like maintainability, consistency, deployment workflow, and governance.

## Key Concepts

- **Fabric App vs data app**: A Fabric App is a managed web application hosted in Microsoft Fabric with built-in authentication. A data app is a specific analytical template of a Fabric App that connects to a semantic model and queries it with DAX instead of provisioning its own managed SQL database.
- **Visualization as code**: In a data app, visuals are not configured through a drag-and-drop UI. Instead, engineers define visual behavior and appearance in source files such as Vega-Lite JSON, TypeScript, CSS, and DAX, which gives full control over rendering, layout, and interactivity.
- **Semantic model querying via DAX**: A data app queries a published semantic model similarly to a Power BI report, using DAX sent through Fabric's executeQueries API. Because the app authenticates with the user's Entra identity, model permissions and row-level security can still apply when configured correctly.
- **Multi-file visual composition**: A single chart commonly spans several files: a .dax query, a .json visual specification, and a .ts file that binds data, metadata, and filters together. This explicit separation makes the app more verbose than a report but easier to inspect, debug, version, and customize.
- **String-replaced DAX templates**: The DAX used in data apps often contains placeholders like {{YEAR}} or {{FILTERS}}. TypeScript code performs string replacement at runtime to inject selections, filter state, and drill context, enabling interactions similar to slicers and cross-filtering.
- **Agentic development workflow**: The intended authoring model heavily assumes use of AI coding agents. The scaffolded project can include agent guidance files and skills so an agent can inspect the semantic model, draft DAX, generate visual specs, and iterate on the app more quickly than manual web development.
- **Code-first deployment**: Unlike Power BI reports, data apps are created, previewed, and deployed through CLI-driven build steps. Engineers scaffold locally, run a development server for testing, and publish the app back to Fabric, where static assets are hosted and served as a managed item.
- **Tradeoffs versus Power BI reports**: Data apps offer higher flexibility, more precise control, and potentially faster bespoke dashboard development, especially with AI assistance. In exchange, they are more complex, require web development practices, and may create new risks around consistency, maintainability, and AI dependence.

## How It Works

A Fabric data app is best understood as a browser-based frontend that sits on top of a Fabric semantic model. Instead of opening a Power BI report authored in a visual designer, the user opens a web application hosted in Fabric. That app authenticates with Fabric single sign-on, issues DAX queries against the semantic model through the `executeQueries` API, and renders the returned data using a charting or visualization library.

At a high level, the request flow looks like this:

1. A user opens the deployed app in the Fabric portal.
2. The app authenticates with the user's Entra identity.
3. The frontend constructs DAX queries based on current state, filters, or interactions.
4. Fabric executes those queries against the semantic model.
5. The result set is transformed and passed into a renderer such as Vega-Lite or D3.
6. The browser displays the resulting visual and wires up interactions like filtering or navigation.

This is conceptually similar to Power BI reports, but the implementation is radically different. In Power BI, visuals, layouts, and interactions are mostly configured through UI actions and the platform generates the DAX and metadata behind the scenes. In a data app, the engineer authors the app directly in source files. That means the app is not a report artifact; it is a real web project with frontend code, stylesheets, configuration files, and build/deploy commands.

Typical project ingredients include:

- `fabric.yaml`: identifies Fabric-specific configuration such as workspace and semantic model connection.
- `rayfin.yml`: backend/runtime configuration used by the Fabric app tooling.
- `global.css`: shared styling for the app, similar in role to a report theme but using standard CSS.
- React/TypeScript source files (`.ts`, `.tsx`): app logic, layout, and component wiring.
- DAX files (`.dax`): explicit semantic model queries for visuals.
- Visual specification files (`.json`): chart grammar definitions, commonly Vega-Lite specs.

A common pattern is that each visual is assembled from three cooperating files:

- A **`.dax` file** defines the query template.
- A **`.json` file** defines the visual encoding.
- A **`.ts` file** binds the query to the semantic model, injects filter values, maps column metadata, and returns the final configuration for rendering.

For example, the DAX file might contain placeholders:

```dax
EVALUATE
CALCULATETABLE(
  FILTER(
    SUMMARIZECOLUMNS(
      'Regions'[{{LEVEL}}],
      "OTD %", [OTD % (Lines)]
    ),
    NOT ISBLANK([OTD %])
  ),
  'Date'[Calendar Year Number (ie 2021)] = {{YEAR}}{{FILTERS}}
)
```

The corresponding TypeScript file imports that DAX as raw text and performs runtime substitution:

```ts
const query = baseQuery
  .replace(/{{LEVEL}}/g, level)
  .replace(/{{YEAR}}/g, String(filter.year))
  .replace(/{{FILTERS}}/g, buildFilterDax(filter, "region"));
```

This string-replacement approach is important because it is how the app turns user state into an executable DAX query. It is also one of the major differences from Power BI: the query logic is visible, editable, and testable. Engineers can inspect it directly, validate it with tools like Tabular Editor or DAX Studio, and optimize it for performance or clarity.

Once data is returned, a Vega-Lite spec can describe how to render it. For example, a bar chart spec might map `Region` to the y-axis and `OTD` to the x-axis. Microsoft provides helper packages for this path, including support for formatting and some interaction behaviors. If you instead choose D3.js or another library, you gain more freedom but must wire up more behavior yourself.

Development is CLI-first. The article describes scaffolding a project with Rayfin, for example:

```bash
bun create @microsoft/rayfin@latest -- "MyApp" --template dataapp --workspace "WorkspaceName"
```

This generates the app template plus AI-oriented support files such as `AGENTS.md`, `.mcp.json`, and skill files under `.agents/skills/`. These artifacts are meant to help coding agents understand the project structure, semantic model references, DAX patterns, and styling conventions.

Local iteration then happens with a development server:

```bash
bun run dev
```

The app is previewed in the browser, often at `localhost:5173`, where you verify the visuals and interactions. Finally, deployment is also command-driven:

```bash
bunx rayfin up
```

That build step uploads static assets to OneLake and creates or updates the Fabric App item in the target workspace.

From an architecture perspective, the biggest lesson is that data apps separate the semantic model from the presentation layer much more cleanly than bespoke Power BI report workarounds often do. The model continues to provide governed metrics and security, while the app layer becomes a customizable frontend. That can be a major advantage for enterprise teams that want stronger source control, CI/CD alignment, reusable frontend patterns, or custom user experiences.

But that flexibility comes with real cost. Teams must own web app structure, styling systems, runtime behavior, testing strategy, and code quality. They also need discipline around AI-generated code, since many prospective app authors will rely on coding agents to create files they may not fully understand. In practice, Fabric data apps are most powerful when treated as software projects that happen to use semantic models—not as a drop-in replacement for low-code reporting.

## Training Exercise

Build a minimal mental model of a Fabric data app by designing one visual as three files: DAX, TypeScript, and Vega-Lite JSON.

### Goal
Create the source structure for a single "Sales by Region" chart that could live inside a Fabric data app.

### Prerequisites
- Access to a published semantic model in Fabric or Power BI
- Permission to execute queries against it
- Basic familiarity with DAX
- A local editor

### Steps
1. **Create a working folder**
   Make a folder named `sales-data-app-prototype`.

2. **Add a DAX template file**
   Create `sales-by-region.dax` with placeholders for a year filter:

   ```dax
   EVALUATE
   CALCULATETABLE(
     SUMMARIZECOLUMNS(
       'Region'[Region Name],
       "Sales", [Total Sales]
     ),
     'Date'[Calendar Year] = {{YEAR}}
   )
   ORDER BY [Sales] DESC
   ```

3. **Add a Vega-Lite spec**
   Create `sales-by-region.json`:

   ```json
   {
     "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
     "title": "Sales by Region",
     "mark": { "type": "bar", "tooltip": true },
     "encoding": {
       "y": {
         "field": "Region",
         "type": "nominal",
         "sort": "-x",
         "axis": { "title": null }
       },
       "x": {
         "field": "Sales",
         "type": "quantitative",
         "axis": { "title": "Total Sales" }
       }
     }
   }
   ```

4. **Add the binding TypeScript file**
   Create `sales-by-region.ts`:

   ```ts
   import baseQuery from "./sales-by-region.dax?raw";
   import vegaLiteSpec from "./sales-by-region.json";

   const connection = "my-semantic-model";

   export function salesByRegion(year: number) {
     const query = baseQuery.replace(/{{YEAR}}/g, String(year));

     return {
       connection,
       query,
       columnMetadata: {
         "Region[Region Name]": { name: "Region", displayName: "Region" },
         "[Sales]": { name: "Sales", displayName: "Total Sales", format: ",.2f" }
       },
       vegaLiteSpec
     };
   }
   ```

5. **Validate the DAX manually**
   Replace `{{YEAR}}` with a real value such as `2024`, then run the resulting query in DAX Studio or Tabular Editor against your semantic model.

6. **Inspect the design**
   Ask yourself:
   - Which parts are data logic versus visual logic?
   - What changes if you add a region slicer?
   - What metadata does the chart need for labels and formatting?

7. **Extend the exercise**
   Modify the DAX and TypeScript to support a second placeholder, `{{TOPN}}`, then limit the visual to the top N regions by sales.

### Stretch task
If you have a Fabric environment available, scaffold a real app with Rayfin and compare your hand-written files to the generated project:

```bash
bun create @microsoft/rayfin@latest -- "SalesApp" --template dataapp --workspace "YourWorkspace"
```

Then identify where the generated project stores:
- workspace/model connection settings
- global styles
- visual components
- agent support files

This exercise reinforces the core model: a data app visual is not a single report object, but a small software assembly of query template, rendering spec, and application code.

## Test Yourself

<details><summary>How does a Fabric data app differ from a conventional Power BI report?</summary>

A data app exposes the presentation layer as web source code: engineers write the DAX, visual specifications, layout, styles, and interactions. Power BI reports primarily configure those elements through a visual designer while the platform generates much of the underlying query and metadata behavior.

</details>

<details><summary>What responsibilities belong to the `.dax`, `.json`, and `.ts` files in the three-file visual pattern?</summary>

The `.dax` file defines the semantic-model query template, the `.json` file defines the visual encoding, and the `.ts` file performs substitutions and binds the query, connection, column metadata, filters, and visual specification together.

</details>

<details><summary>Why should a Fabric data app be managed as a software project rather than as a drop-in replacement for low-code reporting?</summary>

Its flexibility makes the team responsible for frontend structure, styling, runtime behavior, testing, maintainability, deployment, and governance. AI agents may accelerate development, but their generated code still requires review and understanding.

</details>

## Further Reading

- [Microsoft Learn: Fabric Apps overview](https://learn.microsoft.com/)
- [Microsoft Learn: Execute Queries REST API for semantic models](https://learn.microsoft.com/)
- [Vega-Lite Documentation](https://vega.github.io/vega-lite/)
- [D3.js Documentation](https://d3js.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
