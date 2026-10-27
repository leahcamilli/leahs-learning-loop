# Leah's Learning Loop Operations

## Permanent Host

Run the Telegram bot only on the Mac mini. The GitHub repository remains the shared source of truth across machines.

Initial setup:

```bash
cd ~/leahs-learning-loop
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -r ingest/requirements.txt
npm install -g @openai/codex
codex login
cp .env.example .env.local
```

When you run `codex login`, choose **Sign in with ChatGPT** so usage bills against your ChatGPT monthly plan. Do not paste an OpenAI Platform API key.

Copy Telegram and GitHub values from the retired `LinkToNotionLessons` `.env.local`. Do **not** copy `OPENAI_API_KEY`, Notion, or Gmail settings; they are unused.

Confirm ChatGPT-managed auth:

```bash
AUTH_FILE="${CODEX_HOME:-$HOME/.codex}/auth.json"
jq '{auth_mode, has_refresh_token: ((.tokens.refresh_token // "") != "")}' "$AUTH_FILE"
```

Expect `auth_mode` of `"chatgpt"` (or equivalent ChatGPT-managed mode) and a refresh token.

## launchd

The checked-in example is `deploy/com.leah.learningloop.plist.example`.

Install it:

```bash
cp deploy/com.leah.learningloop.plist.example ~/Library/LaunchAgents/com.leah.learningloop.plist
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.leah.learningloop.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.leah.learningloop.plist
```

If migrating an existing capture bot that uses the same Telegram token, stop it before bootstrapping this service; two processes cannot poll the same token.

The launch agent needs `HOME` set (so Codex finds `~/.codex/auth.json`) and a `PATH` that includes the `codex` binary. The example plist sets `HOME` and includes `/opt/homebrew/bin` and `/usr/local/bin`. If you install Codex through nvm, append that node bin directory to the plist `PATH` before bootstrapping.

Check it:

```bash
launchctl list | grep com.leah.learningloop
tail -f ~/Library/Logs/LeahsLearningLoop.err.log
```

## Updating the Bot

```bash
cd ~/leahs-learning-loop
git pull --ff-only
source .venv/bin/activate
python -m pip install -r ingest/requirements.txt
launchctl kickstart -k gui/$(id -u)/com.leah.learningloop
```

If Codex returns auth errors after a long idle period, run `codex login` again on the Mac mini under the same OS user that owns the launch agent, then restart the service.

## Upgrading Existing Lessons

Older lessons predate video metadata and the TL;DR/takeaways layer. Upgrade them in
place from the Mac mini (it has YouTube access and Codex auth):

```bash
cd ~/leahs-learning-loop
git pull --ff-only
source .venv/bin/activate

# 1. Video length, channel, and publish date (fast, no Codex usage)
python -m ingest.backfill --metadata-only

# 2. Preview the summary upgrade on a few pages, then run it for real
python -m ingest.backfill --summaries-only --limit 3 --dry-run
python -m ingest.backfill --summaries-only --limit 25

git add wiki/pages && git commit -m "backfill: summaries and video metadata" && git push
```

With `TYPESAFE_API_KEY` in `.env.local`, add canonical topics and the lesson profile
to every page. It's quick and uses no Codex:

```bash
python -m ingest.backfill --jev-only --limit 5 --dry-run
python -m ingest.backfill --jev-only
```

After changing a topic's description or threshold in `ingest/topics.py`, re-judge
just the pages that currently carry it:

```bash
python -m ingest.backfill --retopic software-engineering --limit 5 --dry-run
python -m ingest.backfill --retopic software-engineering
```

The summary step also runs Jev (when configured) to drop takeaways and key moments the
source does not support.

Every step is idempotent, so run the summary step in batches and pick up where the
last one stopped. It processes newest pages first. When a transcript is available it
also adds timestamped key moments; use `--no-transcripts` to summarize from the lesson
text only. `--match <text>` limits the run to matching filenames.

## Safe Development

- Use a separate development Telegram bot token.
- Use a fine-grained GitHub token limited to this repository.
- Run tests before restarting the service.
- Keep `.env.local` and `~/.codex/auth.json` only on the host; never commit them.
- Do not share one `auth.json` across concurrent machines or jobs.
- Do not delete the old repository until the new service has processed several real links successfully.

## Recovery

Captures are idempotent after migration. A normalized URL fingerprint is included in every new filename. If a request fails before publishing, send it again. If it already published, the bot returns the existing article instead of paying for another generation.
