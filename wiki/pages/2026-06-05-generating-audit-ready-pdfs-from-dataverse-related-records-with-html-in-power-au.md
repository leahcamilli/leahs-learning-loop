---
title: "Generating Audit-Ready PDFs from Dataverse Related Records with HTML in Power Automate"
source: "https://chrismvnro.com/generating-pdfs-of-related-records-in-dataverse-tables-in-power-automate-without-word-templates-for-audit-type-requests/"
date: "2026-06-05"
tags: [power-automate, dataverse, html, pdf, css, audit]
source_type: "web"
topics: [automation-workflows]
kind: "tutorial"
depth: 3
actionability: 2
---

## TL;DR

> Normalize related Dataverse records into one common schema, merge and sort them chronologically, then render the result as styled HTML for PDF conversion. This avoids Word-template maintenance while preserving rich text and giving the flow direct control over audit-ready formatting.

## Key Takeaways

1. Map every source table into common `Date`, `Activity`, `Content`, and `Style` fields so one HTML row template can render all record types.
2. Combine normalized arrays with `union(...)` and sort on `Date` to produce a single chronological audit timeline instead of table-by-table sections.
3. Emit rich-text notes and email bodies directly as HTML inside table cells to preserve their formatting more faithfully than plain-text template fields.
4. Set row styling from record attributes such as email `prioritycode`; CSS class names are cleaner long-term than embedding raw style strings.
5. Build the document from separate CSS, HTML header, table header, generated rows, and closing-tag components so each part can be changed independently.
6. Save the assembled HTML as a file, convert it with an HTML-to-PDF action available in the environment, and then store or send the resulting PDF.
7. Validate chronological ordering, retained rich-text formatting, conditional colors, and malformed source HTML before treating the export as audit-ready.

## Overview

This lesson explains a practical pattern for exporting related Dataverse records—such as emails, notes, cases, and other activities—into a single PDF using Power Automate without relying on Word templates. Instead of pushing data into a document template, the flow builds HTML directly, applies CSS for styling, and then converts the result to PDF.

This approach matters when you need flexible document generation for audit trails, subject access requests, or customer interaction histories. It is especially useful for engineers and Power Platform builders who need to preserve rich text formatting, avoid template maintenance overhead, and keep control over document structure entirely inside the flow logic.

## Key Concepts

- **HTML-first document generation**: Rather than populating a Word or Excel template, the flow constructs a complete HTML document as a string. This gives you direct control over headings, tables, columns, and embedded content, which makes later changes much easier than maintaining document templates.
- **Record normalization**: Different Dataverse tables often have different schemas, even when they represent related timeline data. The flow uses Select actions to map each source type—such as notes and emails—into a common shape with fields like Date, Activity, Content, and Style.
- **Rich text preservation**: Formatted notes and email bodies often contain HTML or rich text that does not survive plain-text template fields well. By emitting HTML directly into table cells, the flow can preserve formatting much more faithfully in the final output.
- **Conditional row styling**: The flow can assign per-row CSS based on record attributes, such as email priority. This lets you visually distinguish records in the exported document, for example by shading high-priority emails in red.
- **Union and chronological sorting**: After each record type is mapped into a common schema, the arrays are merged together and sorted by date. This creates a single chronological dataset suitable for rendering as an audit timeline.
- **HTML-to-PDF conversion pipeline**: Once the HTML document is assembled, the flow saves it as a file, converts that file to PDF, and stores the final PDF. This separates content construction from file generation and makes the output reusable for email, storage, or downstream processing.

## How It Works

The core idea is to treat Power Automate as a document renderer rather than a template filler. The flow is triggered for a Dataverse row, in the example a contact record, and then gathers related records such as emails, notes, activities, or cases. Instead of trying to push these into a Word template with repeating controls, the flow builds an HTML page containing a styled table.

The implementation starts with a few Compose actions that define the HTML shell and styling:

1. **Compose CSS**: define table styling such as fonts, borders, spacing, and optional background colors.
2. **Compose HTML head**: create the opening HTML document, embed the CSS, and start the body and table.
3. **Compose table head**: define table headers such as `Date`, `Activity`, and `Content`.

A minimal structure looks like this:

```html
<!DOCTYPE html>
<html>
<head>
<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}
td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}
</style>
</head>
<body>
<h2>Activity History: Contact Name</h2>
<table>
<thead>
<tr>
<th>Date</th>
<th>Activity</th>
<th>Content</th>
</tr>
</thead>
<tbody>
```

Next, the flow retrieves related Dataverse records. Since each table has different columns, each dataset is transformed independently using a **Select** action. The goal is to emit a standardized object for each row, for example:

```json
{
  "Date": "2026-05-01T10:30:00Z",
  "Activity": "Email",
  "Content": "<p>Email body here</p>",
  "Style": "background-color: #FF474D;"
}
```

This normalization step is what makes the rest of the flow simple. Emails, notes, and other records can all be rendered by the same row template once they share the same shape.

The article highlights conditional styling inside the Select expressions. For example, an email's `prioritycode` can drive the row background color:

```text
if(equals(item()?['prioritycode'],0),outputs('Compose_table_bg-color_normal_priority_email'),'')
if(equals(item()?['prioritycode'],2),outputs('Compose_table_bg-color_low_priority_email'),'')
```

This is a straightforward, if somewhat string-heavy, way to inject visual cues directly into the exported timeline. A cleaner long-term variant would be to emit CSS class names instead of raw style strings, but inline style works well in Power Automate because it keeps each row self-contained.

After each source dataset is normalized, the flow combines them into a single array using `union(...)` and sorts them by date:

```text
sort(union(body('Select_-_notes'),body('Select_-_emails')),'Date')
```

This gives you one chronological event stream across record types. That is the key transformation for audit and SAR scenarios: the export is no longer grouped by source table, but by what happened over time.

The flow then uses **Apply to each** to append each normalized item into a string variable representing the table body. Each array item becomes one `<tr>` row. The article's row template is essentially:

```html
<tr style='@{item()?['Style']}'>
<td style='@{item()?['style']}'>@{formatDateTime(item()?['Date'],'dd-MM-yyyy hh:mm tt')}</td>
<td>@{item()?['Activity']}</td>
<td>@{item()?['Content']}</td>
</tr>
```

A couple of practical observations:

- The same style is applied at both row and cell level in the example; in most cases, applying it at the row level is enough.
- Because `Content` can contain rich text HTML, it can render formatted notes and email bodies directly in the final PDF.
- If source content contains malformed HTML, the final render may need extra cleanup or CSS tuning.

Once the rows are appended, the flow closes the HTML document by adding the remaining `</tbody>`, `</table>`, `</body>`, and `</html>` tags. At that point, you have a complete HTML document string.

The final stage is file handling:

- Create a file containing the HTML.
- Convert the file to PDF using an HTML-to-PDF step available in your environment.
- Create or save the resulting PDF to your target location.

The overall data flow looks like this:

- Trigger on a Dataverse row
- Read the main contact row
- Query related records from multiple Dataverse tables
- Normalize each source into a common schema
- Merge and sort all records by date
- Render rows into an HTML table
- Save HTML and convert to PDF
- Store or send the PDF

Compared with Word-template approaches, the trade-off is that you lose a visual template editor and must manage string-based HTML manually. But in exchange, you gain easier schema changes, better handling of rich text, and more direct control over styling and conditional formatting.

## Training Exercise

Build a small Power Automate flow that exports a contact's notes and emails into a single PDF timeline.

1. **Create a trigger**
   - Use a Dataverse trigger such as **When a row is selected** or **When a row is added, modified or deleted**.
   - Target the `contact` table.

2. **Fetch the primary contact**
   - Add **Get a row by ID** for the selected contact.
   - You will use `fullname` in the HTML heading.

3. **Add CSS Compose actions**
   - Create one Compose for base table CSS.
   - Create two more Compose actions for row colors, for example:

```text
background-color: #E4A0F7;
background-color: #FF474D;
```

4. **Create the HTML header**
   - Add a Compose containing the opening HTML, embedded CSS, title, and opening `<table>` tag.

5. **Create the table header**
   - Add a Compose containing:

```html
<thead>
<tr>
<th>Date</th>
<th>Activity</th>
<th>Content</th>
</tr>
</thead>
<tbody>
```

6. **Query related notes and emails**
   - Add Dataverse list actions to get notes and emails related to the contact.
   - Keep the filters simple for the exercise; the important part is getting two distinct datasets.

7. **Normalize each dataset with Select**
   - For notes, emit objects with `Date`, `Activity`, `Content`, and `Style`.
   - For emails, do the same, and use a conditional expression to set `Style` based on `prioritycode`.

8. **Merge and sort**
   - Add a Compose using an expression like:

```text
sort(union(body('Select_-_notes'), body('Select_-_emails')), 'Date')
```

9. **Render rows**
   - Initialize a string variable named `HtmlRows`.
   - Add **Apply to each** over the sorted array.
   - Append one HTML row per item:

```html
<tr style='@{item()?['Style']}'>
<td>@{formatDateTime(item()?['Date'],'dd-MM-yyyy hh:mm tt')}</td>
<td>@{item()?['Activity']}</td>
<td>@{item()?['Content']}</td>
</tr>
```

10. **Close the HTML**
    - Add a Compose for the closing tags:

```html
</tbody>
</table>
</body>
</html>
```

11. **Assemble the final HTML document**
    - Concatenate the header, table head, row variable, and closing tags.

12. **Create and convert the file**
    - Save the HTML as a file.
    - Use your environment's HTML-to-PDF conversion step.
    - Save the PDF to SharePoint, OneDrive, or another document location.

13. **Validate the result**
    - Confirm that notes retain formatting.
    - Confirm that records are ordered by date.
    - Confirm that priority-based email rows have different background colors.

**Stretch goal:** Replace inline styles with CSS classes such as `priority-high` and `priority-low`, then emit class names from the Select action instead of raw CSS strings. This makes the row rendering cleaner and centralizes styling in one CSS block.

## Test Yourself

<details><summary>Why must notes, emails, and other related records be normalized before rendering?</summary>

Their Dataverse tables use different schemas. Mapping them to shared fields such as `Date`, `Activity`, `Content`, and `Style` allows one sorting step and one HTML row template to handle every record type.

</details>

<details><summary>How does the flow create a unified chronological timeline?</summary>

It combines the normalized arrays with `union(...)` and applies `sort(..., 'Date')`. An Apply to each loop then renders the sorted items as HTML table rows.

</details>

<details><summary>What are the main trade-offs of HTML-first PDF generation compared with Word templates?</summary>

The lesson says HTML provides easier schema changes, stronger rich-text handling, and direct styling control. In return, builders must maintain string-based HTML and CSS without a visual template editor, and may need to clean malformed source HTML.

</details>

## Further Reading

- [Power Automate documentation](https://learn.microsoft.com/power-automate/)
- [Microsoft Dataverse documentation](https://learn.microsoft.com/power-apps/maker/data-platform/data-platform-intro)
- [HTML Tables Tutorial](https://www.w3schools.com/html/html_tables.asp)
- [Use expressions in Power Automate](https://learn.microsoft.com/power-automate/use-expressions-in-conditions)
