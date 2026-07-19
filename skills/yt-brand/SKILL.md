---
name: yt-brand
description: Set up or update a YouTube channel's brand profile — niche, audience, voice, format, and visual identity — saved as a brand.md file that other yt-* skills (yt-packaging, yt-script) read automatically. Use this when the user wants to define their channel branding, start a new YouTube channel, set up their channel identity, or when another yt-* skill needs a brand.md that doesn't exist yet. Trigger on "set up my channel", "channel branding", "define my brand", "create brand profile", or any request to establish who a channel is for and how it should look and sound.
---

# YouTube Channel Brand

Create one durable `brand.md` file that captures a channel's identity. Every other yt-* skill reads this file instead of re-asking the user who they are — so the quality of this file compounds across every video they make.

## Where brand.md lives

Write to `brand.md` in the current working directory. Before interviewing, check if it already exists — if so, this is an **update** session: read it, show a short summary, and ask what changed. Never silently overwrite an existing brand.md.

## The interview

Ask in 2-3 batched rounds, not one long form. Skip anything already answered in conversation. If the user is unsure about an answer, propose 2-3 options with reasoning and let them pick — don't leave sections blank.

**Round 1 — the channel:**
- Channel name + niche (specific: "beginner woodworking restorations", not "DIY")
- Who watches: audience, their level, what they want from the channel
- Format: **faceless** (AI/VO + visuals), **on-camera**, or **mixed** — this changes how yt-script writes scripts, so pin it down
- Typical video length target

**Round 2 — voice & positioning:**
- Tone: 3-5 adjectives with an anti-example ("casual but not sloppy")
- The channel's angle: why watch this channel over the top channel in the niche
- 2-3 admired channels — if the user wants, run the **yt-research** skill on one to ground the brand in what actually works in the niche, and record the findings in brand.md

**Round 3 — visual identity:**
- Color palette (3-5 hex values; propose palettes if the user has none)
- Thumbnail style: photoreal / illustrated / bold-text / face-driven; recurring elements
- For faceless channels: the visual world — art direction that image prompts should stay inside (e.g. "cinematic 35mm documentary stills, muted teal-orange")
- Persona/character if any (mascot, narrator identity)

## brand.md format

Use exactly these section headings — yt-packaging and yt-script parse this file by section:

```markdown
# <Channel name> — brand profile
_updated: <date>_

## Niche & audience
<niche, who watches, their level, what they come for>

## Format
<faceless | on-camera | mixed> · target length: <N> min · cadence: <if known>

## Voice
<tone adjectives + anti-example. 1-2 sample sentences written in the voice.>

## Positioning
<the angle vs competitors; admired channels + what to steal/avoid from each>

## Visual identity
palette: <hex values>
thumbnail style: <style + recurring elements + text treatment>
art direction: <for image prompts — style, mood, lens, lighting keywords>

## Do / Don't
<3-5 bullets each — hard rules other skills must respect>
```

## After writing

Show the user the file and tell them the chain: `yt-research` (study the niche) → `yt-brand` (this, once) → `yt-packaging` (per video) → `yt-script` (per video). Suggest the natural next step — usually packaging their first video idea.
