---
title: "Deep-linking to Specific Records in Power Apps"
source: "https://youtu.be/8JU9fIbxLXY"
date: "2026-05-20"
tags: [powerapps, deeplinking, canvas-apps, power-fx, dataverse]
source_type: "youtube"
channel: "Power Squared"
published: "2026-05-19"
duration_seconds: 564
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> A Power Apps deep-link passes a record’s unique ID in the app URL, reads it with `Param()`, and uses `LookUp()` to open the matching record. This lets users move directly from emails, workflows, dashboards, or QR codes to the item they need.

## Key Takeaways

1. Pass a stable record identifier, such as a Dataverse GUID or SharePoint item ID, in a query parameter like `recordId`.
2. Read the incoming identifier with `Param("recordId")`; URL parameters arrive as text and may require `GUID()` or `Value()` before lookup.
3. Resolve the target record with `LookUp()`, store it in a variable such as `varTargetRecord`, and bind the detail form’s `Item` property to that variable.
4. Navigate to the detail screen when a matching record exists, but preserve the normal browse-screen path when no parameter is supplied.
5. Handle blank, malformed, inaccessible, and nonexistent record IDs with a notification and a safe fallback screen.
6. Use the same target-record variable for deep-links and gallery selections so one app supports both direct entry and ordinary browsing.
7. Treat deep-links as navigation context, not authorization; connector and data-source permissions still determine whether the user can access the record.

## Overview

This lesson explains how deep-linking works in Power Apps Canvas apps, with a practical focus on opening an app directly to a specific record. Deep-links are useful when users launch an app from an email, a workflow, a dashboard, a QR code, or another system and need to land on the exact item they should review rather than starting at a generic home screen.

For engineers and makers building business apps on Microsoft Power Platform, this pattern is important because it improves navigation, reduces clicks, and makes apps easier to integrate into broader business processes. The core technique is to pass identifying information in the app URL, read it inside the app with Power Fx, and use that value to load or navigate to the target record.

## Key Concepts

- **Deep-linking**: Deep-linking means launching an application with enough context in the URL to take the user directly to a specific screen, state, or record. In Power Apps, this is commonly done by appending query-string parameters to the app URL and then reading them at runtime.
- **Param function**: The `Param()` Power Fx function retrieves a value from the app's launch URL. If the link includes something like `&recordId=123`, the app can read it with `Param("recordId")` and use that value in formulas or navigation logic.
- **Record targeting**: To open a specific record, the app needs a stable identifier that can be passed in the URL and looked up in the data source. This is often a Dataverse GUID, a SharePoint list item ID, or another unique key that can be used in a `LookUp()` expression.
- **Startup and navigation logic**: Deep-linking usually requires app startup logic that checks whether a parameter exists and decides where to navigate. This can be placed in `App.OnStart`, `Screen.OnVisible`, or startup formulas, depending on the app design and performance needs.
- **Data retrieval with LookUp**: Once the app has the identifier from the URL, it typically uses `LookUp()` to fetch the matching record from the connected data source. That record can then be assigned to a variable or directly bound to a form or display screen.
- **Integration scenarios**: Deep-links are most valuable when Power Apps participates in a larger workflow. Common examples include links generated from Power Automate, records opened from model-driven apps, notifications sent in Teams or email, and bookmarks to specific business objects.

## How It Works

At a high level, the pattern has three parts:

1. Build an app URL that includes a parameter identifying the target record.
2. Read that parameter when the Canvas app starts.
3. Use the parameter to find the record and navigate to the correct screen.

A typical launch URL looks like this:

```text
https://apps.powerapps.com/play/<app-id>?tenantId=<tenant-id>&recordId=<record-guid>
```

The exact base URL can vary depending on environment and app publishing context, but the important part is the query parameter such as `recordId`. That value is the handoff between the calling system and your app.

Inside the app, Power Fx reads the incoming value with `Param("recordId")`. The app then uses that value to decide whether it was launched normally or via a deep-link. If the parameter is blank, the user can land on the default browse screen. If it exists, the app can immediately fetch the matching record and navigate to a detail or edit screen.

A common implementation uses a global variable in `App.OnStart`:

```powerfx
Set(varRecordId, Param("recordId"));

If(
    !IsBlank(varRecordId),
    Set(
        varTargetRecord,
        LookUp(Accounts, Account = GUID(varRecordId))
    )
)
```

In this example, `Accounts` is the data source and `Account` is the primary key column. For Dataverse, IDs are often GUIDs, so converting the text parameter with `GUID()` is usually required. For SharePoint or SQL, the conversion may instead use `Value()` or remain as text depending on the schema.

After the record is loaded, the app navigates to the appropriate screen:

```powerfx
If(
    !IsBlank(varTargetRecord),
    Navigate(scrAccountDetail, ScreenTransition.None)
)
```

The target screen can bind a display form or edit form directly to the resolved record:

```powerfx
Item = varTargetRecord
```

An alternative pattern is to avoid loading the record globally and instead resolve it on the destination screen. For example, the detail screen's `OnVisible` could run a `LookUp()` using `Param("recordId")`. This can simplify app startup, but it may also repeat queries if the screen is revisited.

There are several practical details engineers should account for:

- **Type conversion matters**: URL parameters arrive as text. If your key is numeric or GUID-based, convert it before lookup.
- **Missing or invalid IDs**: Always handle the case where `Param()` is blank or `LookUp()` returns no record.
- **Permissions still apply**: A deep-link does not bypass connector or data-source security. If the user lacks access, the app should fail gracefully.
- **Startup timing**: If your app relies on collections or data preloading, make sure the deep-link logic runs after or alongside the necessary data initialization.
- **Source integration**: If the link is generated by Power Automate, ensure the flow passes the correct app URL and record identifier.

A more defensive startup flow might look like this:

```powerfx
Set(varRecordId, Param("recordId"));

If(
    IsBlank(varRecordId),
    Navigate(scrHome, ScreenTransition.None),
    Set(varTargetRecord, LookUp(Accounts, Account = GUID(varRecordId)));
    If(
        IsBlank(varTargetRecord),
        Notify("The requested record could not be found.", NotificationType.Error);
        Navigate(scrHome, ScreenTransition.None),
        Navigate(scrAccountDetail, ScreenTransition.None)
    )
)
```

Conceptually, the data flow is simple:

- External system or user clicks a URL.
- Power Apps receives query parameters.
- The app parses the parameters with `Param()`.
- The app resolves the record with `LookUp()`.
- The app navigates to a detail or edit experience for that record.

This pattern scales well because the same app can support both standard navigation and context-aware entry points. Instead of creating multiple apps or forcing users through browse screens, you let the URL carry business context into the app.

## Training Exercise

Build a small Canvas app that opens directly to a chosen record when launched with a URL parameter.

1. **Create or open a Canvas app** connected to a table or list.
   - Good options: Dataverse table, SharePoint list, or Excel test data.
   - Ensure the table has a unique identifier column, such as `ID` or a GUID primary key.

2. **Add two screens**:
   - `scrBrowse`: a gallery listing records.
   - `scrDetail`: a display form showing one selected record.

3. **Configure the detail form**:
   - Set the form's `DataSource` to your table.
   - Set the form's `Item` property to a variable:

```powerfx
varTargetRecord
```

4. **Add startup logic** in `App.OnStart`.
   - For a numeric ID:

```powerfx
Set(varRecordId, Param("recordId"));
If(
    !IsBlank(varRecordId),
    Set(varTargetRecord, LookUp(MyList, ID = Value(varRecordId)))
)
```

   - For a Dataverse GUID:

```powerfx
Set(varRecordId, Param("recordId"));
If(
    !IsBlank(varRecordId),
    Set(varTargetRecord, LookUp(MyTable, MyPrimaryKey = GUID(varRecordId)))
)
```

5. **Add navigation logic**.
   - In `App.OnStart` or the first screen's `OnVisible`, navigate when a target record exists:

```powerfx
If(
    !IsBlank(varTargetRecord),
    Navigate(scrDetail, ScreenTransition.None)
)
```

6. **Support normal in-app browsing**.
   - In the gallery's `OnSelect`, set the same variable and navigate:

```powerfx
Set(varTargetRecord, ThisItem);
Navigate(scrDetail, ScreenTransition.None)
```

7. **Publish the app** and copy its play URL.

8. **Test a deep-link** by manually appending a parameter:
   - Example for numeric IDs:

```text
https://apps.powerapps.com/play/<app-id>?tenantId=<tenant-id>&recordId=5
```

   - Example for GUIDs:

```text
https://apps.powerapps.com/play/<app-id>?tenantId=<tenant-id>&recordId=6f1d2b8e-1d54-4b9b-9f4e-3dc1f8d3d2aa
```

9. **Add error handling**.
   - Show a message if the record does not exist:

```powerfx
If(
    IsBlank(varTargetRecord),
    Notify("Record not found", NotificationType.Error)
)
```

10. **Stretch goal**: Generate deep-links from a Power Automate flow.
   - Trigger on record creation.
   - Send yourself an email containing the app URL with the new record's ID.
   - Click the link and verify the app opens directly to the created record.

By the end of the exercise, you should have one app that supports both standard browse navigation and parameter-driven direct record access.

## Test Yourself

<details><summary>What are the three core steps in opening a specific Power Apps record from a deep-link?</summary>

Add the record identifier to the app URL, read it with `Param()`, and use it to find the record with `LookUp()`. If the record is found, navigate to the appropriate detail or edit screen.

</details>

<details><summary>Why might `Param(&quot;recordId&quot;)` need to be wrapped in `GUID()` or `Value()`?</summary>

Query-string parameters arrive as text. The value must match the data source key’s type, so Dataverse GUIDs commonly require `GUID()` and numeric IDs commonly require `Value()`.

</details>

<details><summary>How should an app respond when a deep-link contains no ID or an invalid ID?</summary>

With no ID, it should follow the normal startup path, such as opening the browse or home screen. If the ID is present but no accessible record is found, it should notify the user and navigate to a safe fallback screen.

</details>

## Further Reading

- [Power Fx formula reference](https://learn.microsoft.com/power-platform/power-fx/)
- [Param function in Power Apps](https://learn.microsoft.com/power-platform/power-fx/reference/function-param)
- [Navigate function in Power Apps](https://learn.microsoft.com/power-platform/power-fx/reference/function-navigate)
- [LookUp function in Power Apps](https://learn.microsoft.com/power-platform/power-fx/reference/function-filter-lookup)
- [Power Apps Canvas apps documentation](https://learn.microsoft.com/power-apps/maker/canvas-apps/)
