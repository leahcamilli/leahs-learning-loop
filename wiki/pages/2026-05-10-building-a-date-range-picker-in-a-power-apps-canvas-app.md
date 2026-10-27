---
title: "Building a Date Range Picker in a Power Apps Canvas App"
source: "https://powerappstools.com/snippet-details/221"
date: "2026-05-10"
tags: [powerapps, canvas-apps, date-picker, power-fx, ui]
source_type: "web"
kind: "tutorial"
depth: 2
actionability: 3
---

## TL;DR

> Build a date range picker from two Date Picker controls, validate that the start is not after the end, and use the result to filter data. For datetime columns, an exclusive upper bound one day after the end date includes the full final day.

## Key Takeaways

1. Default `dpStart` and `dpEnd` to a useful range with `DateAdd(Today(), -7, Days)` and `Today()`.
2. Treat a range as valid only when `dpStart.SelectedDate <= dpEnd.SelectedDate`; show an error and disable Apply when that condition fails.
3. Filter datetime values with `Created >= startDate && Created < DateAdd(endDate, 1, Days)` so records throughout the end date are included.
4. Store dates in context or global variables when users need temporary selections, popup behavior, presets, or an explicit Apply step.
5. After a preset updates variables, reset variable-bound Date Picker controls so they display the new values.
6. Package the controls and logic into a container or component that exposes `StartDate`, `EndDate`, and `IsValid` for reuse.
7. Account for null selections, reverse-order input, UTC-versus-local datetime behavior, and delegation limits on large remote data sources.

## Overview
These notes cover how to build a practical date range picker in a Power Apps canvas app using standard controls and Power Fx formulas. Because canvas apps do not provide a single built-in desktop-style date range picker, the pattern is typically composed from two Date Picker controls, validation logic, optional preset buttons, and filter expressions that drive galleries, reports, or other data-bound controls.

This matters because date-based filtering is a common requirement in business apps, from reporting and dashboards to operational workflows. Treating the date range picker as a small reusable stateful component makes it easier to maintain, validate, and reuse across screens while handling real-world concerns such as datetime fields, delegation, and time zone behavior.

## Key Concepts
- **Canvas app composition**: Power Apps canvas apps are assembled from standard controls such as screens, containers, galleries, labels, buttons, icons, and inputs. A date range picker is usually built from two Date Picker controls plus supporting UI elements rather than a custom all-in-one widget.
- **Date range state**: The pattern requires at least two values: a start date and an end date. These can be stored directly in control values or in context/global variables for more explicit state management.
- **Validation and constraints**: A valid date range usually means the start date is less than or equal to the end date. Additional rules may include min/max dates, blocking future dates, or correcting invalid selections.
- **Power Fx date logic**: Functions like `Today`, `DateAdd`, `DateDiff`, and comparison operators enable default date ranges, quick presets such as Last 7 Days, and filter logic against data sources.
- **Filter integration**: The selected range becomes useful when passed into `Filter` expressions against SharePoint, Dataverse, SQL, or local collections to constrain records by date.
- **Reusable UX patterns**: Encapsulating the behavior in a component or a consistent variable/formula pattern improves reuse across screens, dashboards, and reporting views.

## How It Works
A typical implementation includes two date inputs, optional preset buttons, validation messaging, and a filter formula consumed by a gallery, chart, or table. In Power Apps, the mechanics are declarative: users change one or both dates, formulas evaluate validity, and downstream controls automatically recalculate based on the selected range.

A common basic setup uses two Date Picker controls such as `dpStart` and `dpEnd` with sensible defaults:

```powerfx
dpStart.DefaultDate = DateAdd(Today(), -7, Days)
dpEnd.DefaultDate = Today()
```

Validation can be expressed simply:

```powerfx
If( dpStart.SelectedDate <= dpEnd.SelectedDate, true, false )
```

A label can show an error when the range is invalid:

```powerfx
If( dpStart.SelectedDate > dpEnd.SelectedDate, "Start date must be before or equal to end date", "" )
```

An Apply button can be disabled until the range is valid:

```powerfx
DisplayMode = If( dpStart.SelectedDate > dpEnd.SelectedDate, DisplayMode.Disabled, DisplayMode.Edit )
```

For stronger control over state, initialize screen-level variables instead of referencing controls directly:

```powerfx
UpdateContext({ ctxStartDate: DateAdd(Today(), -7, Days), ctxEndDate: Today() })
```

Then update them from each picker’s `OnChange`:

```powerfx
UpdateContext({ ctxStartDate: dpStart.SelectedDate })
```

```powerfx
UpdateContext({ ctxEndDate: dpEnd.SelectedDate })
```

This is especially useful for popup-style pickers or cases where users should make temporary selections before applying them.

To connect the range to data, a gallery bound to a source with a datetime column such as `Created` can use:

```powerfx
Filter( MyDataSource, Created >= dpStart.SelectedDate && Created < DateAdd(dpEnd.SelectedDate, 1, Days) )
```

Using `< DateAdd(endDate, 1, Days)` is often safer than `<= endDate` when the source contains time values, because it includes the entire end date instead of only midnight values.

Preset buttons improve usability. For example, a Last 30 Days button can set both dates at once:

```powerfx
UpdateContext({ ctxStartDate: DateAdd(Today(), -30, Days), ctxEndDate: Today() })
```

If controls are bound to variables, reset them after applying presets:

```powerfx
Reset(dpStart); Reset(dpEnd)
```

For reuse, place the controls inside a container or custom component and expose output properties such as `StartDate`, `EndDate`, and `IsValid`. This turns the pattern into a reusable date filtering building block.

Important edge cases to consider:
- Empty or null selections
- Users selecting the end date before the start date
- UTC versus local time handling when backends store datetimes
- Delegation limits when filtering large remote datasets

A training exercise in the notes walks through creating a screen with two date pickers, validation, a preset button, and a gallery bound either to sample data or a real source. The resulting pattern is a solid reusable foundation for date-based filtering in canvas apps.

## Test Yourself

<details><summary>Why is `&lt; DateAdd(endDate, 1, Days)` generally preferable to `&lt;= endDate` for a datetime field?</summary>

An end date commonly represents midnight at the start of that day, so `<= endDate` can omit records later that day. Comparing against the next day with an exclusive upper bound includes the entire selected end date.

</details>

<details><summary>When should dates be stored in variables instead of read directly from Date Picker controls?</summary>

Use variables when selections must remain temporary until Apply, when the picker appears in a popup, or when presets need to update both dates as a single state change.

</details>

<details><summary>What should a reusable date range component expose?</summary>

It should expose the selected `StartDate` and `EndDate` plus an `IsValid` value. Downstream galleries, charts, and reports can then consume the range without duplicating its validation logic.

</details>

## Personal Notes
Building a Date Range Picker in a Power Apps Canvas App

Source: https://powerappstools.com/snippet-details/221
Notion page: https://www.notion.so/Building-a-Date-Range-Picker-in-a-Power-Apps-Canvas-App-35c01bb0839a8195980efc03f01639be

Tags: powerapps, canvas-apps, date-picker, power-fx, ui

Overview

A date range picker is a common UI pattern for filtering records, generating reports, and driving time-based workflows. In a Power Apps canvas app, there is no single built-in control that behaves exactly like a desktop-style date range picker, so makers typically compose one from standard controls and Power Fx formulas.

This lesson explains how to think about a date range picker in Power Apps as a small stateful UI component: two selected dates, validation rules, and downstream filtering behavior. It is useful for engineers and app makers who need to build reusable, user-friendly date selection experiences in business apps.

Key Concepts

  *   Canvas app composition: Power Apps canvas apps are built by composing screens, containers, galleries, labels, buttons, and input controls rather than relying on heavy custom widgets. A date range picker is usually assembled from standard controls such as Date Picker inputs, labels, icons, and buttons.
  *   Date range state: A date range picker needs at least two pieces of state: a start date and an end date. In Power Apps, this state is often stored in context variables, global variables, or component properties so formulas elsewhere in the app can reference the selected range.
  *   Validation and constraints: A valid range typically requires the start date to be on or before the end date. Good implementations also enforce optional constraints such as minimum/maximum allowed dates, blocking future dates, or auto-correcting inverted selections.
  *   Power Fx date logic: Power Fx includes date-oriented functions like Today, DateAdd, DateDiff, and comparisons using <= and >=. These functions let you implement default ranges, quick presets like 'Last 7 days', and record filtering logic based on the selected period.
  *   Filter integration: The real value of a date range picker comes from applying it to a dataset. In canvas apps, the selected dates are usually fed into Filter expressions against SharePoint, Dataverse, SQL, or collections to restrict records to the desired time window.
  *   Reusable UX patterns: For maintainability, date range behavior should be encapsulated in a component or at least implemented with consistent variables and formulas. Reusability matters when the same date filter appears across multiple screens, reports, or dashboards.

How It Works

A practical date range picker in a canvas app usually consists of these parts:

1. **Two date inputs**: one for the start date and one for the end date. 2. **Optional preset buttons**: Today, Last 7 Days, This Month, etc. 3. **Validation messaging**: warning text when the selected range is invalid. 4. **A filter formula**: used by a gallery, chart, or table to consume the chosen range.

At a high level, the mechanics are simple: the user changes one or both dates, the app stores those values, validation formulas check whether the range is valid, and downstream controls recalculate automatically because Power Fx is declarative.

A common implementation pattern is:

- Add two **Date Picker** controls, for example `dpStart` and `dpEnd`. - Set sensible defaults: - `dpStart.DefaultDate = DateAdd(Today(), -7, Days)` - `dpEnd.DefaultDate = Today()` - Add a label to show validation status. - Use the selected dates directly in filters or copy them into variables if you want stronger control over state transitions.

Example validation logic:

```powerfx If( dpStart.SelectedDate <= dpEnd.SelectedDate, true, false ) ```

You can drive a message label with:

```powerfx If( dpStart.SelectedDate > dpEnd.SelectedDate, "Start date must be before or equal to end date", "" ) ```

And disable an Apply button with:

```powerfx DisplayMode = If( dpStart.SelectedDate > dpEnd.SelectedDate, DisplayMode.Disabled, DisplayMode.Edit ) ```

If you want explicit app state rather than directly referencing controls, initialize variables on screen load:

```powerfx UpdateContext({ ctxStartDate: DateAdd(Today(), -7, Days), ctxEndDate: Today()
