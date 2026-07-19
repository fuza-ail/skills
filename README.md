# skills

My collection of Claude/agent skills. Install any of them with [npx skills](https://github.com/vercel-labs/skills):

```bash
# list what's available
npx skills add fuza-ail/skills --list

# install one skill
npx skills add fuza-ail/skills --skill yt-research

# install globally (available in every project)
npx skills add fuza-ail/skills --skill yt-research -g

# install everything
npx skills add fuza-ail/skills --skill '*'
```

## Skills

| Skill | What it does |
|---|---|
| [yt-research](skills/yt-research/SKILL.md) | Research any YouTube video or channel — fetches transcripts + metadata, produces summaries, key insights, and content-pattern analysis |
| [yt-brand](skills/yt-brand/SKILL.md) | One-time channel brand interview → `brand.md` (niche, voice, format, visual identity) that the other yt-* skills read automatically |
| [yt-packaging](skills/yt-packaging/SKILL.md) | Package a video before making it — ranked title options, thumbnail concepts, and ready-to-paste image-gen prompts (Midjourney/Flux/Nano Banana) |
| [yt-script](skills/yt-script/SKILL.md) | Retention-engineered long-form scripts — hook, open loops, chapters, re-hooks, b-roll/scene cues — for faceless or on-camera channels |

**The chain:** `yt-research` (study the niche) → `yt-brand` (once) → `yt-packaging` (per video) → `yt-script` (per video).

### yt-research

Give it a video URL or channel handle:

- **Single video** → deep-dive report: TL;DR, key insights, notable details (with timestamps)
- **Channel study** → performance snapshot, content patterns, title formulas, key ideas across videos
- **Topic research** → "what does this channel say about X" across their videos

Fetching uses [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/) + [yt-dlp](https://github.com/yt-dlp/yt-dlp); dependencies auto-install via [uv](https://docs.astral.sh/uv/) (PEP 723 inline metadata) — no setup step.

Try: *"Research @veritasium — what are their content patterns?"*

## Repo layout

```
skills/
├── yt-research/
│   ├── SKILL.md              # skill instructions (frontmatter: name + description)
│   └── scripts/yt_fetch.py   # bundled fetcher script
├── yt-brand/SKILL.md
├── yt-packaging/SKILL.md
└── yt-script/SKILL.md
evals/                        # test prompts for skill development
```

Each skill is a folder under `skills/` containing a `SKILL.md`. Adding a new skill = adding a new folder.
