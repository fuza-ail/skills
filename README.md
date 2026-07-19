# yt-research

Claude skill for researching and learning from any YouTube video or channel.

Give it a video URL or a channel handle — it fetches transcripts and metadata, then produces summaries, key insights, and content-pattern analysis.

## What it does

- **Single video** → deep-dive report: TL;DR, key insights, notable details (with timestamps)
- **Channel study** → performance snapshot, content patterns, title formulas, key ideas across videos
- **Topic research** → "what does this channel say about X" across their videos

Data fetching is handled by a bundled script using [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/) and [yt-dlp](https://github.com/yt-dlp/yt-dlp) — dependencies auto-install via [uv](https://docs.astral.sh/uv/) (PEP 723 inline metadata), so there is no setup step.

## Install

```bash
npx skills add fuza-ail/yt-research --skill yt-research
```

Or install globally (available in every project):

```bash
npx skills add fuza-ail/yt-research --skill yt-research -g
```

Manual install (Claude Code):

```bash
git clone https://github.com/fuza-ail/yt-research
cp -r yt-research/skills/yt-research ~/.claude/skills/
```

## Requirements

- [uv](https://docs.astral.sh/uv/) (recommended — zero-setup), or `pip install youtube-transcript-api yt-dlp`

## Usage

Just talk to Claude:

- "Summarize this video: https://youtube.com/watch?v=..."
- "Research @veritasium — what are their content patterns?"
- "What does @ycombinator say about fundraising?"

The skill triggers automatically on YouTube links and channel handles.

## Repo layout

```
skills/yt-research/
├── SKILL.md              # skill instructions
└── scripts/yt_fetch.py   # fetcher: video / channel / transcript subcommands
evals/evals.json          # test prompts for skill development
```
