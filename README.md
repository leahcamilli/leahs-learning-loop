# Leah's Learning Loop

A calm, practical second brain for turning YouTube recordings into grounded study notes, an AI-focused Forward Deployed Engineer (FDE) roadmap, and hands-on knowledge checks. Start at the [Leah's Learning Loop website](https://leahcamilli.github.io/leahs-learning-loop/).

Inspired by the capture → source evidence → study → searchable knowledge workflow in [Stevie's Second Brain](https://steviesimsii.github.io/Second_Brain/); the application, learning roadmap, content, and assessments here were written independently for this project. The site is a static application; it does not call an AI API, host videos, require an account, or include analytics.

## Get started

1. Open **FDE roadmap** to tailor the default 12-week roadmap to your goal, available study hours, and preferred schedule.
2. In **Library**, select **Capture a video**. Add a YouTube URL, choose a learning category, and write a takeaway, summary, or transcript. You can paste a transcript or load a `.txt`, `.vtt`, or `.srt` file. Timestamped captions become clickable moments.
3. Study the ideas and write a short explanation from memory. Browse or search saved lessons and transcripts.
4. Open **Assessments** to take the five-question, scenario-based quiz for any of the six AI FDE categories. Review source-linked explanations; score at least 80% to pass.
5. Export your private workspace JSON for backup or to move your progress to another browser. Importing replaces the current browser's workspace after confirmation.

## The six roadmap categories

| Stage | Category | Capstone direction |
| --- | --- | --- |
| 1 | Discovery & product | Map a real user's workflow, baseline, and responsible experiment. |
| 2 | Python, APIs & data | Build a tested API backed by a documented public dataset. |
| 3 | LLMs & retrieval | Make a documentation assistant that exposes its evidence. |
| 4 | Agents & tool use | Design an agent with narrow tool permissions and human checkpoints. |
| 5 | Evaluation & safety | Compare versions on representative tasks and relevant risks. |
| 6 | Deployment & delivery | Ship, observe, recover, and hand over an AI-enabled service. |

Reallocate stage weeks proportionally by setting a roadmap length from 6–52 weeks. Planning hours are study-time estimates, not promises of professional proficiency or employment readiness. Begin each stage with a real user problem; follow its suggested resources and practice project.

## What's private; what's public

**The public website** contains the supplied artwork, the six-category curriculum, sample assessments, and entries in `data/recordings.json`. **A recording you publish** becomes part of that shared file, including its URL, transcript, summary, and takeaways. Confirm you have permission to publish each recording's material. The website does not download, re-host, or claim ownership of YouTube videos.

Your saved recording drafts, goals, checked roadmap items, reflections, playback speed, and quiz attempts are stored only in your current browser's local storage. Visitors on other devices do not see them. Download **Export progress** before clearing browser storage. **Import** explicitly replaces the current browser workspace. No login, third-party model/API calls, cookies, or analytics are used.

## Publish a shared recording

Publishing requires GitHub account **write access to this repository**; a shareable Pages URL does not grant write access. In the website's lesson view, select **Publish recording**, copy the JSON, and follow the link to **Actions → Publish a lesson → Run workflow**. Paste the JSON and start the run. The workflow validates the YouTube ID, category, field lengths, timestamps, and evidence, rejects duplicates, and commits the verified lesson to the public library. A Pages deployment runs only after its content checks pass.

The manual workflow accepts up to 65,535 characters. Keep shared transcripts under 45,000 characters; use summarized source notes when a transcript is longer. Alternatively, contribute an entry to `data/recordings.json` through a reviewed pull request. Never commit secrets, account tokens, private notes, copyrighted transcripts without permission, or confidential material.

## Maintain the site

- `index.html`, `styles.css`, and `app.js` are the dependency-free website.
- `data/curriculum.json` contains the six learning stages and source-linked category assessments; update lesson content and tests together.
- `data/recordings.json` is the canonical shared recording library. Empty by design for the initial launch.
- `.github/workflows/pages.yml` validates data, then deploys GitHub Pages on a `main` or `master` push.
- `.github/workflows/publish-recording.yml` accepts and validates intentionally shared lessons from repository writers.
- `tests/` contains standard-library Python content checks; run `python -m unittest discover -s tests -v`.

All external links are optional learning starting points, not a substitute for checking current documentation or exercising judgment in a real environment. The category assessments test baseline familiarity; they are not certifications, job guarantees, or official company guidance.