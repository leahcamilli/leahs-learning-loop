---
title: "Choosing the Right Variable Type in Power Apps"
source: "https://youtu.be/krhedsvD5tw"
date: "2026-05-20"
tags: [powerapps, variables, power-fx, canvas-apps, state-management]
source_type: "youtube"
channel: "Shane Young"
published: "2026-05-19"
duration_seconds: 2002
topics: []
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> Prefer formulas over stored state, then use the narrowest variable type that fits the need. This avoids duplicate sources of truth and makes Power Apps easier to debug, maintain, and keep synchronized.

## Key Takeaways

1. Use a direct formula when a value can be derived from existing data; Power Apps will recalculate it automatically when dependencies change.
2. Use `UpdateContext()` or navigation context for temporary, screen-local UI state such as an open dialog, selected tab, or detail record.
3. Use `Set()` sparingly for state that genuinely must be shared across multiple screens, such as a user role or app-wide feature flag.
4. Use collections for mutable, in-memory tables such as carts, favorites, cached records, or locally reshaped data—not as the default container for every value.
5. Treat collections as local snapshots: upstream data changes will not appear automatically unless the collection is refreshed and rebuilt.
6. Avoid copying values already available through controls or navigation, such as storing `GalleryCustomers.Selected` in another variable without a clear need.
7. Choose state in this order: control formula, context variable, global variable, then collection when tabular mutation is required.

## Overview

This lesson explains how Power Apps variables work and how to choose the right kind of state for a canvas app. In Power Apps, many bugs and maintenance problems come from using a variable where a formula, control property, or collection would be more appropriate, so understanding the tradeoffs is essential for building reliable apps.

A working engineer building canvas apps, internal tools, or low-code workflows will care because variable choices directly affect readability, recalculation behavior, performance, and app correctness. The goal is to make state explicit: know when to use global variables, context variables, collections, or no variable at all.

## Key Concepts

- **Declarative vs imperative state**: Power Apps is primarily a declarative platform: many values should be derived from formulas instead of being manually stored and updated. Variables introduce imperative state, which can be necessary, but they also create synchronization risk when the source of truth changes and the variable does not.
- **Global variables**: Global variables are created with `Set()` and are available throughout the app. They are useful for app-wide state such as the current user role, a selected record ID that needs to persist across screens, or feature flags, but they should be used sparingly because they can make dependencies harder to trace.
- **Context variables**: Context variables are screen-scoped values created with `UpdateContext()` or passed via `Navigate()`. They are best for temporary UI state local to a screen, such as whether a dialog is open or what tab is selected, because they avoid polluting global app state.
- **Collections**: Collections are in-memory tables created with functions like `Collect()` and `ClearCollect()`. They are appropriate for caching data, shaping records for UI use, or storing a working set of rows, but they should not be treated as the default way to hold every value because they are mutable and do not automatically reflect upstream data changes.
- **Formula-first design**: Before creating a variable, ask whether the value can be expressed directly as a control property formula. Formula-first design reduces state duplication and leverages automatic recalculation, which typically leads to simpler and more predictable apps.
- **Scope and maintainability**: The narrower the scope of a variable, the easier it is to reason about and maintain. Choosing the smallest valid scope—control formula, then context variable, then global variable—helps prevent accidental coupling between screens and features.

## How It Works

When building a canvas app, you generally have four ways to represent a value:

1. **A direct formula** on a control property
2. **A context variable** for screen-local state
3. **A global variable** for app-wide state
4. **A collection** for tabular, mutable, in-memory data

A practical decision process is:

- If the value can be calculated from existing data every time, use a **formula**.
- If the value only matters on one screen, use a **context variable**.
- If multiple screens need to read or update it, consider a **global variable**.
- If you need a table of records you will add to, remove from, or reshape locally, use a **collection**.

### 1. Prefer formulas over variables
A common mistake is storing derived values in variables:

```powerfx
Set(varFullName, FirstNameInput.Text & " " & LastNameInput.Text)
```

This works, but it can get out of sync if either input changes and you forget to update the variable everywhere. A better approach is often to bind the target control directly:

```powerfx
FirstNameInput.Text & " " & LastNameInput.Text
```

This lets Power Apps recalculate automatically whenever dependencies change.

### 2. Use context variables for UI state
Context variables are ideal for local interaction state. For example, a modal dialog on one screen does not need app-wide visibility:

```powerfx
UpdateContext({ showDialog: true })
```

Then a container's `Visible` property can be:

```powerfx
showDialog
```

You can also pass values during screen navigation:

```powerfx
Navigate(DetailScreen, ScreenTransition.Fade, { selectedOrder: ThisItem })
```

This keeps state near the screen that uses it.

### 3. Use global variables when state crosses screens
Global variables created with `Set()` are useful when a value must be shared across the app:

```powerfx
Set(varCurrentUserEmail, User().Email)
Set(varIsAdmin, User().Email in AdminList.Email)
```

These values can then be referenced from any screen. However, because they are accessible everywhere, overusing them makes it harder to understand what changes what. If a value is only needed on one screen, a global variable is usually too broad.

### 4. Use collections for client-side tables
Collections are mutable in-memory tables. They shine when you need to cache data, build a temporary cart, or manipulate rows before saving:

```powerfx
ClearCollect(colCart, { ProductId: 101, Qty: 1 })
Collect(colCart, { ProductId: 202, Qty: 3 })
RemoveIf(colCart, ProductId = 101)
```

Collections are especially useful for galleries and repeated UI elements because they naturally model rows. But they come with a tradeoff: once loaded, a collection is just local app state. If the source data changes externally, the collection will not automatically stay synchronized unless you refresh and rebuild it.

### 5. Think about source of truth
The central engineering idea is to avoid multiple sources of truth. If the selected item is already available through a gallery selection or navigation context, storing it again in a second variable may be unnecessary. Every copied value creates maintenance overhead.

For example, instead of:

```powerfx
Set(varSelectedCustomer, GalleryCustomers.Selected)
```

you may be able to reference:

```powerfx
GalleryCustomers.Selected
```

or pass it directly on navigation:

```powerfx
Navigate(CustomerDetail, ScreenTransition.None, { customer: GalleryCustomers.Selected })
```

### 6. A practical rule of thumb
Use the smallest and least mutable tool that solves the problem:

- **Formula** for derived values
- **Context variable** for local screen state
- **Global variable** for app-wide shared state
- **Collection** for in-memory tables and client-side record manipulation

That approach leads to apps that are easier to debug, easier to extend, and less likely to break when UI or data dependencies change.

## Training Exercise

Build a small two-screen canvas app and implement the same feature using different variable strategies, then compare maintainability.

### Goal
Create an app that:
- Shows a list of customers on Screen 1
- Opens a detail view on Screen 2
- Allows toggling a local popup
- Maintains a small favorites list

### Steps
1. **Create the data**
   - Add a simple table or use a collection in `App.OnStart`:

```powerfx
ClearCollect(
    colCustomers,
    { Id: 1, Name: "Adele Vance", City: "Seattle" },
    { Id: 2, Name: "Diego Chen", City: "Austin" },
    { Id: 3, Name: "Priya Nair", City: "London" }
)
```

2. **Build ScreenBrowse**
   - Add a gallery bound to `colCustomers`.
   - Add a button or icon in each row.
   - First implement navigation using a **global variable**:

```powerfx
Set(varSelectedCustomer, ThisItem);
Navigate(ScreenDetail)
```

3. **Build ScreenDetail**
   - Show labels for:

```powerfx
varSelectedCustomer.Name
varSelectedCustomer.City
```

4. **Refactor to use a context variable instead**
   - Replace the browse button formula with:

```powerfx
Navigate(ScreenDetail, ScreenTransition.None, { ctxCustomer: ThisItem })
```

   - Update detail labels to use:

```powerfx
ctxCustomer.Name
ctxCustomer.City
```

5. **Add local UI state with a context variable**
   - On ScreenDetail, add a popup container.
   - Add a button with:

```powerfx
UpdateContext({ showNotes: true })
```

   - Set popup `Visible` to:

```powerfx
showNotes
```

   - Add a close button:

```powerfx
UpdateContext({ showNotes: false })
```

6. **Add a collection for favorites**
   - Add an "Add to Favorites" button on ScreenDetail:

```powerfx
Collect(colFavorites, ctxCustomer)
```

   - Add another gallery bound to `colFavorites` on a third screen or below the detail area.

7. **Replace one stored value with a formula**
   - Add a label with:

```powerfx
ctxCustomer.Name & " - " & ctxCustomer.City
```

   - Do not store this combined text in a variable.

### What to observe
- Which version is easiest to trace?
- Which values are truly shared across screens?
- Which values are only UI state?
- Which values are derived and should not be stored?
- What happens if you rename a control or change navigation flow?

### Stretch task
Create a short decision table for your app with columns:
- Value name
- Needed where?
- Changes how often?
- Tabular or scalar?
- Best storage choice

Use it to justify each variable or formula you introduced.

## Test Yourself

<details><summary>Why is a direct formula usually better than storing a derived value in a variable?</summary>

A formula recalculates automatically when its dependencies change. A stored copy must be updated manually and can become a second, stale source of truth.

</details>

<details><summary>When should you choose a context variable instead of a global variable?</summary>

Choose a context variable when the value is only needed on one screen, such as popup visibility or a record passed to a detail screen. Its narrower scope reduces accidental coupling across the app.

</details>

<details><summary>What makes a collection appropriate, and what synchronization risk does it introduce?</summary>

A collection is appropriate for a mutable client-side table whose rows need to be added, removed, cached, or reshaped. It does not automatically reflect changes in its upstream data source, so it must be refreshed and rebuilt when synchronization matters.

</details>

## Further Reading

- [Power Fx formula reference](https://learn.microsoft.com/power-platform/power-fx/formula-reference)
- [Set function in Power Apps](https://learn.microsoft.com/power-platform/power-fx/reference/function-set)
- [UpdateContext function in Power Apps](https://learn.microsoft.com/power-platform/power-fx/reference/function-updatecontext)
- [Collect, Clear, and ClearCollect functions](https://learn.microsoft.com/power-platform/power-fx/reference/function-clear-collect-clearcollect)
- [Variables in canvas apps](https://learn.microsoft.com/power-apps/maker/canvas-apps/working-with-variables)
