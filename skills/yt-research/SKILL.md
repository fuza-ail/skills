---
name: yt-research
description: Research and learn from any YouTube video or channel. Fetches transcripts and metadata with bundled scripts, then produces summaries, key insights, and content-pattern analysis. Use this whenever the user shares a YouTube link or channel handle and wants to study, summarize, analyze, or learn from it — including "what does this video say", "research this channel", competitor/creator analysis, extracting a creator's content strategy, or turning video knowledge into notes. Trigger even if the user just pastes a YouTube URL with a vague ask.
---

# YouTube Research

Turn YouTube videos and channels into structured research: summaries, insights, and content-pattern analysis. The bundled script does all fetching — never scrape YouTube pages with a browser, and never guess at video content you haven't fetched.

## Requirements

Scripts declare their own dependencies (PEP 723 inline metadata) and run via `uv`:

```bash
uv run <skill-path>/scripts/yt_fetch.py <command> ...
```

If `uv` is missing, install deps once with `pip install youtube-transcript-api yt-dlp` and run with `python3` instead.

## The fetch script

All data comes from `scripts/yt_fetch.py`. It writes files into `--out` (default `./yt_data`) and prints a small JSON summary with the file paths.

| Command | What it does |
|---|---|
| `video <url_or_id>` | One video: `<id>.meta.json` (title, views, likes, tags, chapters, description) + `<id>.transcript.md` |
| `channel <url_or_handle> [--limit N]` | Channel: `channel.json` with subscriber count and video list sorted by views (default 30 videos) |
| `transcript <id>... [--timestamps]` | Batch transcripts only — use after picking videos from `channel.json` |

Useful flags: `--timestamps` adds `[mm:ss]` markers (use when the user wants to jump to moments); `--lang en,es` sets preferred transcript languages. Non-English videos auto-fall back to any available transcript, translated to the first preferred language when possible.

Put fetched data in a `yt_data/` directory inside the current working directory so the user can inspect and reuse it.

## Workflow

First classify the request:

**A. Single video** ("summarize this video", "what are the takeaways", a pasted watch URL)
1. `uv run .../yt_fetch.py video <url>`
2. Read the transcript file and metadata.
3. Write the **Video deep-dive** report (below).

**B. Channel research** ("study this channel", "how does this creator do it", "@handle")
1. `uv run .../yt_fetch.py channel <handle> --limit 30`
2. Read `channel.json` and show the user a quick overview: subscribers, top videos by views, spread of durations.
3. Pick videos to deep-dive — default to the top 5 by views unless the user names specific ones or a topic (then pick by title match). Say which ones you picked and why.
4. `uv run .../yt_fetch.py transcript <id1> <id2> ...`
5. Read transcripts **one at a time**, and write a 5-10 bullet mini-summary of each before moving to the next — transcripts run 5k-40k characters, and summarizing as you go keeps the analysis grounded when full transcripts no longer fit in memory.
6. Write the **Channel study** report from the mini-summaries + metadata.

**C. Topic within a channel** ("what does this channel say about X") — same as B, but pick videos whose titles/descriptions match the topic, and organize the report around the topic instead of the channel.

## Report formats

Adapt sections to the request — drop what's irrelevant, but keep this shape so reports are comparable across runs.

### Video deep-dive

```markdown
# <title>
<channel> · <views> views · <upload date> · <duration>

## TL;DR
3-5 sentences.

## Key insights
Numbered, each 1-3 sentences. Insights, not chapter recaps — what would
the user want to remember a month from now?

## Notable details
Facts, numbers, names, tools, resources mentioned. With [mm:ss] if
timestamps were fetched.

## Structure & delivery (only if user is studying the craft)
Hook, pacing, how arguments are built, CTA.
```

### Channel study

```markdown
# <channel> — channel study
<subscribers> subs · analyzed <N> of <M> fetched videos

## What this channel is
2-3 sentences: niche, audience, angle.

## Performance snapshot
Small table: top videos, views, duration. Call out outliers —
what over/under-performs and a hypothesis for why.

## Content patterns
Recurring topics, title formulas, video length strategy, hook style.
Pull evidence from the transcripts, not just titles.

## Key ideas across videos
The channel's core claims/teachings, deduplicated across videos.

## Per-video mini-summaries
The 5-10 bullet summaries from the deep-dive step.
```

## Edge cases

- **No transcript** (captions disabled, music, very new upload): the script prints `TRANSCRIPT UNAVAILABLE`. Fall back to metadata — title, description, chapters — and tell the user the analysis is metadata-only.
- **Age-restricted / private / region-locked video**: yt-dlp errors clearly; report it and move on (in channel mode, skip that video and pick the next).
- **Huge channels**: `--limit 30` is the default for a reason — listing is cheap but transcripts are not. Raise the limit only for listing/stats, not for bulk transcript fetching. If the user wants more than ~8 transcripts analyzed, warn that quality per video drops and confirm.
- **Playlists**: `channel` mode works on playlist URLs too — same flat listing.
