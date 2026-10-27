---
title: "Power Apps Patch() Patterns for Create, Update, Bulk Operations, and Upserts"
source: "https://www.linkedin.com/posts/shreyansh-haran_powerapps-powerplatform-lowcode-share-7446146596603465728-tAE5?utm_source=social_share_send&utm_medium=ios_app&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY&utm_campaign=share_via"
date: "2026-05-20"
tags: [powerapps, powerfx, patch, powerplatform, sharepoint]
source_type: "web"
kind: "tutorial"
depth: 3
actionability: 3
---

## TL;DR

> Use Power Fx `Patch()` to create, update, upsert, and connect records while controlling exactly what a Canvas App writes. Capturing its returned record enables dependent writes, while set-oriented bulk patterns may reduce overhead when the connector supports them.

## Key Takeaways

1. Create a record with `Patch(DataSource, Defaults(DataSource), { ...fields... })`.
2. Update only the required fields by passing an existing record or a unique identifier such as `{ ID: 2 }` as the base record.
3. Capture the record returned by `Patch()` when later operations need generated IDs, timestamps, or server-side defaults.
4. For parent-child writes, save the parent first and use the returned parent ID in the child record's `Patch()`.
5. Implement an upsert with `Coalesce(LookUp(...), Defaults(DataSource))` so an existing match is updated and a missing match is created.
6. For bulk changes, the lesson recommends testing `Patch(DataSource, ForAll(...))` instead of `ForAll(..., Patch(...))`; actual batching and performance depend on the connector.
7. For thousands of rows, account for delegation limits, throttling, and backend batch support rather than assuming `Patch()` alone will scale.

## Overview

This lesson explains how the Power Fx `Patch()` function is used in Power Apps to create, update, and coordinate data operations without relying entirely on forms. The source material is a short social post, but the surrounding comments reveal the practical patterns engineers actually use in production: targeted updates, capturing return values, bulk modifications, upserts, and chaining writes across related tables or lists.

If you build Canvas Apps against SharePoint, Dataverse, or similar connectors, `Patch()` is one of the most important tools for taking direct control of persistence logic. Understanding the common patterns—and the performance pitfalls—helps you build apps that are faster, easier to reason about, and better suited for real-world workflows than form-only implementations.

## Key Concepts

- **Patch as direct data control**: `Patch()` writes records to a data source or merges records in memory. In Canvas Apps, it gives you explicit control over what fields are sent and when, which is why developers use it to avoid the rigidity of form-driven save flows.
- **Create vs update semantics**: A new record is usually created with `Patch(DataSource, Defaults(DataSource), { ...fields... })`. An existing record is updated by passing either the existing record itself or a record containing a unique identifier such as `{ID: 2}` along with the changed fields.
- **Returned record from Patch**: `Patch()` returns the created or updated record. This matters when you need generated values such as IDs, timestamps, or server-side defaults so that subsequent operations can reference the newly persisted entity.
- **Bulk operations and performance**: Applying `Patch()` inside `ForAll()` often works but can perform poorly because it executes record-by-record. A more efficient pattern in many cases is shaping a table with `ForAll(...)` and passing that table into `Patch(DataSource, ...)`, reducing overhead and leading to cleaner formulas.
- **Upsert with Coalesce**: An upsert combines update and insert logic into one formula. A common pattern is `Patch(Source, Coalesce(existingRecord, Defaults(Source)), { ... })`, which updates when a matching record exists and creates otherwise.
- **Chained writes across related sources**: Because `Patch()` returns the saved record, you can save to one source, capture its ID, and then use that ID in a second `Patch()` to create related records. This is a common technique for parent-child or lookup-style relationships across SharePoint lists or Dataverse tables.

## How It Works

At a high level, `Patch()` takes three pieces of information:

1. The target data source
2. A base record that says whether you are creating or updating
3. A change record containing the fields to write

The most common create pattern is:

```powerfx
Patch(
    Employees,
    Defaults(Employees),
    {
        FullName: "Ava Patel",
        Role: "Developer"
    }
)
```

Here, `Defaults(Employees)` signals that Power Apps should create a new row using the data source's default schema. The third argument contains the actual values to save.

To update an existing record, you can either pass the full record you already have in memory or identify it directly:

```powerfx
Patch(
    Employees,
    LookUp(Employees, ID = 2),
    {
        Role: "Senior Developer"
    }
)
```

If you already know the identifier, a shorter and often cleaner pattern is:

```powerfx
Patch(
    Employees,
    { ID: 2 },
    {
        Role: "Senior Developer"
    }
)
```

This is useful when you want a targeted field-level update and do not want to round-trip through an edit form.

A major reason `Patch()` is so useful is that it returns the saved record. That enables write-then-use workflows:

```powerfx
Set(
    varCreatedEmployee,
    Patch(
        Employees,
        Defaults(Employees),
        {
            FullName: txtName.Text,
            Role: txtRole.Text
        }
    )
);

Notify("Created employee ID: " & varCreatedEmployee.ID)
```

This pattern becomes even more important when coordinating related data. For example, create a parent record, capture its generated ID, and then create a related child record:

```powerfx
Set(
    varParent,
    Patch(
        Projects,
        Defaults(Projects),
        {
            Title: txtProjectTitle.Text
        }
    )
);

Patch(
    Tasks,
    Defaults(Tasks),
    {
        ProjectID: varParent.ID,
        Title: txtTaskTitle.Text
    }
)
```

The LinkedIn discussion also highlights an important production concern: bulk updates. A naive implementation often looks like this:

```powerfx
ForAll(
    colPendingUpdates,
    Patch(
        Employees,
        { ID: ThisRecord.ID },
        { Role: ThisRecord.NewRole }
    )
)
```

This is straightforward, but it tends to execute one patch per row, which can become slow and noisy against remote data sources. Commenters point out that a better pattern in many scenarios is to build a table of changes and use `Patch(DataSource, ForAll(...))` rather than `ForAll(..., Patch(...))`:

```powerfx
Patch(
    Employees,
    ForAll(
        colPendingUpdates,
        {
            ID: ID,
            Role: NewRole
        }
    )
)
```

The exact connector behavior varies, but the design idea is consistent: shape the updates first, then hand them to `Patch()` in a more set-oriented way when supported. For large datasets, especially thousands of rows, engineers should still be careful about delegation limits, connector throttling, and whether the backend supports true batch behavior.

For mixed create-or-update flows, an upsert pattern avoids branching logic. One common version is:

```powerfx
Patch(
    Employees,
    Coalesce(
        LookUp(Employees, Email = txtEmail.Text),
        Defaults(Employees)
    ),
    {
        Email: txtEmail.Text,
        FullName: txtName.Text,
        Role: txtRole.Text
    }
)
```

If a matching employee exists, the record is updated. If not, a new one is created. This is especially useful in import, synchronization, or idempotent save scenarios.

The source comments also raise an architectural point: `Patch()` is foundational, but it should not automatically carry all business logic. In enterprise apps, validation, approvals, auditing, and reusable workflows are often better distributed across Power Apps, Power Automate, Dataverse business rules, or backend APIs. A practical rule is to use `Patch()` for focused UI-driven data writes, then move cross-cutting or critical business logic into more governable layers as complexity grows.

Finally, note the app model context. In Canvas Apps, `Patch()` is central because the maker controls persistence explicitly. In Model-driven apps, direct `Patch()` usage is less central because forms and Dataverse behaviors often handle data operations through built-in mechanisms.

## Training Exercise

Build a small Canvas App that demonstrates the four most useful `Patch()` patterns: create, update, upsert, and chained writes.

1. **Create two data sources**
   - Use SharePoint lists or Dataverse tables.
   - `Projects`: `Title`
   - `Tasks`: `Title`, `ProjectID`

2. **Add controls to a screen**
   - Text input: `txtProjectTitle`
   - Text input: `txtTaskTitle`
   - Text input: `txtExistingProjectId`
   - Button: `btnCreateProject`
   - Button: `btnUpdateProject`
   - Button: `btnUpsertProject`
   - Button: `btnCreateProjectAndTask`

3. **Implement create**
   Set `btnCreateProject.OnSelect` to:

```powerfx
Set(
    varProject,
    Patch(
        Projects,
        Defaults(Projects),
        {
            Title: txtProjectTitle.Text
        }
    )
)
```

4. **Implement targeted update**
   Set `btnUpdateProject.OnSelect` to:

```powerfx
Patch(
    Projects,
    { ID: Value(txtExistingProjectId.Text) },
    {
        Title: txtProjectTitle.Text
    }
)
```

5. **Implement upsert**
   Add a new text input `txtUniqueTitle` and set `btnUpsertProject.OnSelect` to:

```powerfx
Patch(
    Projects,
    Coalesce(
        LookUp(Projects, Title = txtUniqueTitle.Text),
        Defaults(Projects)
    ),
    {
        Title: txtUniqueTitle.Text
    }
)
```

6. **Implement chained writes**
   Set `btnCreateProjectAndTask.OnSelect` to:

```powerfx
Set(
    varNewProject,
    Patch(
        Projects,
        Defaults(Projects),
        {
            Title: txtProjectTitle.Text
        }
    )
);

Patch(
    Tasks,
    Defaults(Tasks),
    {
        Title: txtTaskTitle.Text,
        ProjectID: varNewProject.ID
    }
)
```

7. **Test each flow**
   - Create a new project and verify the row appears.
   - Update an existing project by ID.
   - Run the upsert twice with the same title and confirm it updates rather than duplicates.
   - Create a project and related task, then confirm the task contains the project ID.

8. **Stretch goal: bulk update**
   - Create a collection of test rows:

```powerfx
ClearCollect(
    colProjectUpdates,
    { ID: 1, Title: "Project A - Updated" },
    { ID: 2, Title: "Project B - Updated" }
)
```

   - Try both approaches and compare behavior:

```powerfx
ForAll(
    colProjectUpdates,
    Patch(Projects, { ID: ID }, { Title: Title })
)
```

   and

```powerfx
Patch(
    Projects,
    ForAll(
        colProjectUpdates,
        {
            ID: ID,
            Title: Title
        }
    )
)
```

   Record which one is easier to maintain and whether your connector shows any performance difference.

## Test Yourself

<details><summary>How does the base-record argument distinguish a create from an update?</summary>

`Defaults(DataSource)` tells `Patch()` to create a new record. Passing an existing record or a record with a unique identifier, such as `{ ID: 2 }`, targets an existing record for update.

</details>

<details><summary>Why should an app capture the record returned by `Patch()`?</summary>

The returned record can contain generated values such as an ID, timestamp, or server default. The app can then use those values in notifications or subsequent writes, including creating related child records.

</details>

<details><summary>How does the lesson implement an upsert, and what limitation should be considered?</summary>

It uses `Coalesce(LookUp(DataSource, matchCondition), Defaults(DataSource))` as the base record, updating a match or creating a new record when none exists. The matching field should be reliably unique, and connector delegation or concurrency behavior may affect production use.

</details>

## Further Reading

- [Microsoft Learn: Patch function in Power Apps](https://learn.microsoft.com/power-platform/power-fx/reference/function-patch)
- [Microsoft Learn: ForAll function in Power Apps](https://learn.microsoft.com/power-platform/power-fx/reference/function-forall)
- [Microsoft Learn: Defaults, LookUp, and Coalesce functions in Power Fx](https://learn.microsoft.com/power-platform/power-fx/formula-reference)
- [Power Platform Tip: ForAll + Patch optimization in Power Apps](https://www.powerplatformtip.com/article/powerplatformtip/powerplatformtip-131-forall-patch-optimization-in-powerapps)
