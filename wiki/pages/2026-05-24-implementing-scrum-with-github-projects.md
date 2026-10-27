---
title: "Implementing Scrum with GitHub Projects"
source: "https://www.youtube.com/live/hMEdSCrWOTk?si=TAa9JhU8w0kd88Cr"
date: "2026-05-24"
tags: [scrum, github-projects, agile, issue-tracking, workflow, planning]
source_type: "youtube"
channel: "Scrum.org"
published: "2025-06-24"
duration_seconds: 3513
kind: "tutorial"
depth: 2
actionability: 2
---

## TL;DR

> Use GitHub Issues, Pull Requests, and Projects as one lightweight Scrum system that keeps planning directly connected to implementation. A simple workflow with linked artifacts and automated status changes makes the board more accurate while reducing duplicate tracking.

## Key Takeaways

1. Model backlog items as consistently structured GitHub Issues with acceptance criteria, estimates, labels, and clear ownership.
2. Keep the core workflow simple: Backlog, Ready, In Progress, In Review, and Done.
3. Assign every committed issue to an explicit sprint field or milestone so scope changes and carryover remain visible.
4. Link pull requests to issues with keywords such as `Closes #123` to create traceability and automatically close completed work.
5. Maintain several views over the same project data, including a prioritized backlog, current sprint board, personal work queue, and review queue.
6. Automate routine transitions—such as adding new issues, setting default status, and marking merged work Done—to keep the board aligned with code activity.
7. Treat the board as a coordination tool: limit work in progress, define Done clearly, and avoid oversized issues or unused custom statuses.

## Overview

This lesson explains how to use GitHub Projects as a lightweight Scrum system for software teams. Even though the source content is sparse, the topic strongly suggests a practical workflow centered on mapping Scrum artifacts and ceremonies—product backlog, sprint backlog, status tracking, and review cadence—onto GitHub Issues, Pull Requests, Milestones, and Project views.

This matters for engineering teams that already live in GitHub and want to avoid duplicating work across separate planning tools. If you are a developer, tech lead, or engineering manager looking for a pragmatic way to run Scrum close to the code, this lesson shows how to structure boards, fields, automation, and review practices so project tracking stays aligned with actual development activity.

## Key Concepts

- **Scrum artifacts in GitHub**: Scrum relies on a product backlog, sprint backlog, and increment. In GitHub, these are typically represented with Issues for work items, Pull Requests for implementation, and a Project board for planning and status. The main goal is to make planning and delivery visible without forcing engineers to leave the development platform.
- **GitHub Projects as the team board**: GitHub Projects provides table, board, and roadmap-style views over issues and pull requests. Custom fields such as Status, Sprint, Priority, Estimate, and Assignee let teams model their process. Views can then be filtered for planning meetings, daily standups, and sprint reviews.
- **Issues as backlog items**: A Scrum backlog item should be small, clear, and testable. GitHub Issues work well for this when teams use templates, labels, acceptance criteria, and estimates consistently. Epics or larger features can be represented through parent-child relationships, labels, or linked issues.
- **Sprint planning and scope control**: A sprint becomes manageable when work items are explicitly assigned to a sprint field or milestone and filtered into a sprint view. Capacity is controlled by limiting the number and size of issues selected. During the sprint, changes to scope should be visible and intentional rather than hidden in ad hoc issue creation.
- **Workflow automation**: Automation reduces manual status updates and keeps the board trustworthy. GitHub Projects can automatically add new issues, update status when pull requests are opened or merged, and close issues through linked PRs. A reliable board depends on minimizing the gap between code activity and project tracking.
- **Traceability from planning to code**: One of GitHub's advantages is direct linkage between backlog items and implementation artifacts. An issue can contain discussion, design notes, acceptance criteria, references to commits, and the pull request that completes the work. This creates an auditable path from planning decisions to shipped changes.

## How It Works

A practical Scrum setup in GitHub usually starts with three core building blocks:

1. **Issues** for user stories, bugs, chores, and technical tasks.
2. **Pull Requests** for code changes tied to those issues.
3. **GitHub Projects** for organizing and visualizing the work.

From there, you define the minimum data model your team needs. A common setup includes these fields:

- **Status**: Backlog, Ready, In Progress, In Review, Done
- **Sprint**: Sprint 12, Sprint 13, etc.
- **Priority**: P0, P1, P2
- **Estimate**: story points or size bucket
- **Assignee**: who owns execution
- **Type**: feature, bug, chore

The key design principle is to keep the workflow simple enough that engineers will actually maintain it.

### Mapping Scrum ceremonies to GitHub

**Backlog refinement** happens in the issue tracker. Product or engineering leads create and clarify issues, add acceptance criteria, assign labels, and estimate effort. This is where vague ideas become implementation-ready work.

**Sprint planning** happens in a Project table or board view filtered to `Status=Ready`. The team selects a set of issues, assigns them to the next sprint, and ensures the total effort fits capacity. If you use milestones, a sprint milestone can serve as an additional timebox marker.

**Daily standup** uses a board view grouped by Status. Team members quickly review what moved, what is blocked, and what is in review. Because GitHub ties issues to pull requests, discussion can move directly from the board into the relevant code review when needed.

**Sprint review/demo** focuses on issues moved to Done and the PRs merged during the sprint. This gives a concrete record of completed work.

**Retrospective** can reference metrics visible in GitHub, such as carryover issues, review delays, or excessive work-in-progress.

### Example workflow

A common end-to-end flow looks like this:

1. Create an issue from a template:
   - user story or bug description
   - acceptance criteria
   - estimate
   - labels
2. Add the issue to the GitHub Project.
3. During sprint planning, set:
   - `Sprint = Sprint 8`
   - `Status = Ready`
   - priority and assignee
4. When work starts, move the issue to `In Progress`.
5. Open a pull request with text like `Closes #123` to link implementation to the issue.
6. Move the issue to `In Review` while the PR is under review.
7. Merge the PR; GitHub closes the issue automatically.
8. Automation or manual update moves the item to `Done`.

### Recommended project views

A strong GitHub Scrum setup usually includes multiple views over the same data:

- **Backlog view**: all unplanned issues, sorted by priority
- **Current sprint board**: only issues for the active sprint, grouped by Status
- **My work**: filtered by assignee = current user
- **Bugs view**: filtered by label `bug`
- **Review queue**: pull requests or items in `In Review`
- **Roadmap**: larger initiatives across multiple sprints

This is important because Scrum needs different perspectives at different times. Planning requires priority ordering, standups require flow visibility, and leadership may want timeline or milestone views.

### Automation patterns

To keep the process lightweight, use built-in automation where possible:

- Automatically add newly created issues with certain labels to the project.
- Set default status to `Backlog`.
- Move items to `In Progress` when assigned or when a branch/PR is created.
- Move items to `Done` when the linked pull request is merged.
- Auto-close issues from PR descriptions using keywords like:

```text
Closes #45
Fixes #78
Resolves #91
```

If built-in automation is not enough, GitHub Actions can extend the workflow. For example, an action can update project fields when a PR is opened, apply labels, or notify Slack when sprint items are blocked.

### What good implementation looks like

A solid Scrum implementation in GitHub has a few traits:

- backlog items are consistently structured
- every sprint item is visible in one active sprint view
- there is a clear definition of done
- pull requests are linked to issues
- work-in-progress is limited
- the board reflects reality with minimal manual effort

### Common failure modes

Teams often struggle when they over-model the process or under-define the work. Typical problems include:

- too many custom statuses that nobody uses consistently
- large issues that cannot finish in one sprint
- no clear link between issue and PR
- using the board as a reporting tool rather than a coordination tool
- updating project state manually long after code activity has changed

The fix is usually to simplify the workflow, standardize issue templates, and automate status transitions where possible.

## Training Exercise

Set up a small Scrum workflow for a sample repository using GitHub Issues and GitHub Projects.

### Goal
Create a backlog, plan a one-week sprint, and simulate work moving from planning to merged code.

### Step 1: Create a repository
Create a test repository such as `scrum-demo`.

### Step 2: Define issue templates
Add two issue templates:

- **User Story**
- **Bug Report**

Example user story template:

```md
## Summary
As a user, I want ...

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Notes
Additional implementation details.
```

### Step 3: Create a GitHub Project
Create a new project and add these custom fields:

- Status
- Sprint
- Priority
- Estimate
- Type

Suggested Status options:

- Backlog
- Ready
- In Progress
- In Review
- Done

### Step 4: Seed the backlog
Create at least 6 issues:

- 3 user stories
- 2 bugs
- 1 chore

For each issue, set:

- labels
- estimate
- priority
- type
- status = Backlog

### Step 5: Create views
Create these views in the project:

1. **Backlog**: filter `Status:Backlog`
2. **Sprint Board**: filter on the active sprint and group by Status
3. **My Work**: filter by your GitHub username

### Step 6: Plan a sprint
Choose 3 issues for `Sprint 1`. Update their status to `Ready` and assign owners.

### Step 7: Simulate implementation
Pick one sprint issue and create a branch and PR for it. In the PR description, include:

```text
Closes #<issue-number>
```

Move the issue through these states:

- Ready
- In Progress
- In Review
- Done

### Step 8: Add one automation
Use either built-in project automation or GitHub Actions to reduce manual work. If using GitHub Actions, try a simple workflow triggered on pull request events.

Example starter workflow:

```yaml
name: PR Event Demo
on:
  pull_request:
    types: [opened, closed]

jobs:
  log-event:
    runs-on: ubuntu-latest
    steps:
      - name: Print event info
        run: |
          echo "PR action: ${{ github.event.action }}"
          echo "PR title: ${{ github.event.pull_request.title }}"
```

### Step 9: Review the sprint board
Answer these questions:

- Which issues are ready but unassigned?
- Which items are in progress at the same time?
- Which PRs are linked to sprint issues?
- Did any work skip the board entirely?

### Stretch goal
Add a `Blocked` label or field and create a saved view showing only blocked sprint work. This helps surface impediments during standup.

## Test Yourself

<details><summary>How can the main Scrum artifacts be represented in GitHub?</summary>

Use Issues for product and sprint backlog items, Pull Requests for their implementation, and a GitHub Project for planning and status visibility. The completed, merged work represents the increment.

</details>

<details><summary>What makes a sprint&#x27;s scope visible and controllable in GitHub Projects?</summary>

Assign selected issues to an explicit sprint field or milestone, then show them in a filtered sprint view grouped by status. Limit the number and size of selected issues to fit team capacity, and make mid-sprint additions visible.

</details>

<details><summary>Why should pull requests be linked to their corresponding issues?</summary>

Linking creates a traceable path from requirements and acceptance criteria to code review and completion. Keywords such as `Closes #123` can also close the issue automatically when the pull request is merged.

</details>

## Further Reading

- [GitHub Projects documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects)
- [About issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues)
- [Linking a pull request to an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)
- [Automating Projects using built-in workflows](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations)
- [The Scrum Guide](https://scrumguides.org/scrum-guide.html)
