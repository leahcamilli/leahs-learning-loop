---
title: "Building a Date Range Picker in Power Apps Canvas Apps"
source: "https://linkedin.com/posts/powerappstools_pick-a-date-range-in-power-apps-without-activity-7450635629643759621-RK6Y?rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY"
date: "2026-04-24"
tags: [powerapps, canvas-apps, date-picker, ux, low-code]
source_type: "web"
kind: "tutorial"
depth: 2
actionability: 1
---

## TL;DR

> Build the date range picker as a small state machine using native Canvas App controls and variables. Showing adjacent months, highlighting the interval, and automatically correcting reversed dates makes range selection faster and less error-prone.

## Key Takeaways

1. Track the picker with variables such as `varStartDate`, `varEndDate`, `varLeftMonth`, `varViewMode`, and `varIsOpen`.
2. Derive the right calendar from the left calendar with `DateAdd(varLeftMonth, 1, Months)` so both panels stay synchronized.
3. Set the first clicked date as the start; use the second as the end, automatically swapping the values when the second date is earlier.
4. When both dates are already selected, treat the next click as a new start date and clear the previous end date.
5. Use conditional formatting to give start and end dates a strong accent and dates inside the interval a lighter fill.
6. Provide month and year gallery views so users can jump across large time spans before returning to day selection.
7. Make Okay preserve the selected dates and close the picker; make Cancel clear both dates, restore `varViewMode` to `"Day"`, and close it.

## Overview

These notes describe how to build a custom date range picker in a Power Apps Canvas App using standard UI building blocks like galleries, labels, icons, variables, and conditional formatting. The design focuses on a better user experience than separate start/end date inputs by showing two months side by side, visually highlighting the selected range, and supporting navigation across day, month, and year views.

This pattern matters for business apps where users frequently filter data, choose booking windows, submit leave requests, or work with reporting periods. A well-implemented range picker reduces user mistakes, keeps date selections valid through auto-swap logic, and makes the interaction feel closer to a modern app component even within low-code constraints.

## Key Concepts

- **Dual-calendar range selection**: Two visible month panels let users pick ranges that span adjacent months without repeated navigation. This is especially useful for common business scenarios like monthly reporting and scheduling.
- **Range highlighting**: Dates between the selected start and end values are visually filled so users can quickly confirm the intended interval.
- **Auto-swap date logic**: If a second selected date is earlier than the first, the component swaps them automatically to preserve a valid chronological range.
- **Multi-level calendar views**: Day, month, and year views allow faster navigation across large time spans before returning to exact date selection.
- **Explicit confirmation and reset actions**: Okay preserves the current selection and closes the picker; Cancel clears dates, resets the view mode, and closes the popup.
- **Composable Canvas App UX**: The picker demonstrates how richer controls can be assembled from native Canvas App primitives rather than relying on a single built-in control.

## How It Works

A custom date range picker in Canvas Apps is best treated as a small state machine. Instead of one native control, the experience is driven by a set of variables that track selected dates, the currently displayed months, the active view level, and whether the popup is open.

Typical state variables include:

- `varStartDate`
- `varEndDate`
- `varLeftMonth`
- derived right month as `DateAdd(varLeftMonth, 1, Months)`
- `varViewMode`
- `varIsOpen`

The day-selection flow usually works like this:

1. If no start date exists, the clicked date becomes the start.
2. If a start date exists but no end date exists, the clicked date becomes the end.
3. If the second clicked date is earlier than the start, the two are swapped automatically.
4. If both dates already exist, a new click restarts the selection by setting a fresh start date and clearing the end date.

This creates a forgiving interaction model: users can explore dates without having to manually correct invalid ordering.

Visual feedback is handled through conditional formatting. Each day cell checks whether it is:
- the start date,
- the end date, or
- inside the interval.

Start/end dates usually get a stronger accent color, while dates between them get a lighter fill. This makes the selected range immediately legible, which is a major improvement over two disconnected date fields.

The dual-calendar layout improves usability because users can view adjacent months at once. Navigation buttons only need to shift the left anchor month, while the right calendar is calculated from it. This keeps both calendars synchronized and simplifies implementation.

The month and year views act as acceleration layers. Instead of clicking previous/next month repeatedly, users can switch to a higher-level gallery, jump to a target month or year, and then return to day view. In practice, this is usually implemented by showing and hiding different galleries depending on `varViewMode`.

The action buttons define the UX contract clearly:
- **Okay** closes the picker and keeps the current dates.
- **Cancel** clears `varStartDate`, `varEndDate`, resets `varViewMode` to `"Day"`, and closes the control.

This approach is a strong example of how Power Fx formulas and Canvas App controls can be combined to build reusable, polished components for filtering, scheduling, booking, and date-driven workflows.

## Test Yourself

<details><summary>Why should the right-hand month be derived from `varLeftMonth` instead of stored independently?</summary>

Using `DateAdd(varLeftMonth, 1, Months)` keeps the two calendars synchronized and reduces the amount of state and navigation logic that must be maintained.

</details>

<details><summary>What should happen when the second selected date is earlier than the first?</summary>

The component should automatically swap the two values so `varStartDate` remains earlier than `varEndDate`, preserving a valid chronological range without requiring manual correction.

</details>

<details><summary>How do day, month, and year views work together?</summary>

Month and year galleries provide faster navigation across long time spans. After choosing the target period, the picker returns to day view for exact date selection.

</details>

## Personal Notes

Building a Date Range Picker in Power Apps Canvas Apps

Source: https://www.linkedin.com/posts/powerappstools_pick-a-date-range-in-power-apps-without-activity-7450635629643759621-RK6Y?utm_source=share&utm_medium=member_ios&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY
Notion page: https://www.notion.so/Building-a-Date-Range-Picker-in-Power-Apps-Canvas-Apps-34c01bb0839a81d3aff8e8b0a2b95cc0

Tags: powerapps, canvas-apps, date-picker, ux, low-code

Overview

This lesson explains the design and behavior of a custom date range picker for Power Apps Canvas Apps. Instead of relying on awkward multi-control workarounds, the component provides a more polished interaction: two calendars shown side by side, a clearly highlighted date interval, and navigation across day, month, and year views.

This matters for makers and engineers building business apps where users frequently filter reports, bookings, requests, or records by date. A well-designed date range picker improves usability, reduces selection errors, and gives users a more modern scheduling and filtering experience inside a Canvas App.

Key Concepts

  *   Dual-calendar range selection: The picker displays two months side by side so users can choose a start and end date without excessive month navigation. This is especially useful when the desired range crosses a month boundary, which is a common case in reporting and planning scenarios.
  *   Range highlighting: Once a start and end date are chosen, all dates between them are visually highlighted. This makes the selected interval easy to verify at a glance and reduces ambiguity compared with using two independent date inputs.
  *   Auto-swap date logic: If the user selects an end date that is earlier than the current start date, the control automatically swaps the values. This ensures the internal state always maintains a valid chronological range and avoids forcing the user to start over.
  *   Multi-level calendar views: The picker supports day, month, and year views to make navigation faster. Users can drill up to larger time units to jump across long periods, then drill back down to select exact dates.
  *   State reset and confirmation actions: The control includes explicit Okay and Cancel actions. Okay confirms the current selection and closes the picker, while Cancel clears start date, end date, and view state so the component returns to a clean baseline.
  *   Canvas app UX composition: In Power Apps Canvas Apps, sophisticated controls are often built by composing galleries, labels, icons, variables, and conditional formatting. The date range picker is a practical example of turning basic building blocks into an app-like interactive component.

How It Works

A custom date range picker in Canvas Apps is typically built as a stateful UI component rather than a single native control. The LinkedIn post describes the behavior of such a component: two visible month panels, date range highlighting, month navigation, view switching, and confirmation or cancellation actions.

At a high level, the component needs to manage several pieces of state:

- `StartDate`: the first selected date - `EndDate`: the second selected date - `LeftMonth`: the month shown in the left calendar - `RightMonth`: the month shown in the right calendar, usually one month after `LeftMonth` - `ViewMode`: whether the user is choosing by `Day`, `Month`, or `Year` - `IsOpen`: whether the picker is visible

A common Canvas Apps implementation uses galleries for each visual layer:

- A **day gallery** for each visible month - A **month gallery** when the user switches to month selection - A **year gallery** when the user switches to year selection - Icons or buttons for left/right navigation - Action buttons for **Okay** and **Cancel**

In day view, each date cell computes three kinds of behavior:

1. **Display logic** - Show the day number. - Optionally gray out dates outside the active month. - Mark today's date with a special style.

2. **Selection logic** - If no `StartDate` exists, clicking a date sets `StartDate`. - If `StartDate` exists and `EndDate` is blank, clicking a date sets `EndDate`. - If both already exist, many implementations restart selection by setting a new `StartDate` and clearing `EndDate`.

3. **Normalization logic** - If the second chosen date is earlier than the first, swap them. - This keeps the range valid without extra user correction.

In Power Fx terms, the click behavior often resembles this pattern:

```powerfx If( IsBlank(varStartDate), Set(varStartDate, ThisItem.Date), IsBlank(varEndDate), If( ThisItem.Date < varStartDate, Set(varEndDate, varStartDate); Set(varStartDate, ThisItem.Date), Set(varEndDate, ThisItem.Date) ), Set(varStartDate, ThisItem.Date); Set(varEndDate, Blank()) ) ```

The highlighted range is then produced with conditional formatting. Each date cell checks whether its date is equal to `StartDate` or `EndDate`, or falls between them. For example:

```powerfx If( !IsBlank(varStartDate) && !IsBlank(varEndDate) && ThisItem.Date >= varStartDate && ThisItem.Date <= varEndDate, ColorValue("#DCEBFF"), Color.White ) ```

The two-month side-by-side layout improves usability because users can select ranges spanning adjacent months without repeatedly paging back and forth. Navigation arrows update the anchor month, and the second calendar
