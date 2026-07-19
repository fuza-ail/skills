---
name: yt-script
description: Write retention-engineered long-form YouTube scripts — hook, open loops, chapters, re-hooks, b-roll or scene-visual cues — adapted to faceless (voiceover + AI visuals) or on-camera channels. Use whenever the user wants a YouTube video script, an outline for a video, help with their video's hook or structure, or to turn research/notes into a script. Trigger on "write my script", "script this video", "video outline", "make a script from this", even if the user doesn't say "long-form".
---

# YouTube Long-Form Script

A script's job: keep the promise the packaging made, minute after minute. Viewers leave the moment a video stops moving toward the payoff — so structure is retention engineering, not decoration.

## Inputs — gather before writing

1. **The package**: locked title + thumbnail concept. Check `packaging/*.md` (from **yt-packaging**) and the conversation. If there's no package at all, offer to run yt-packaging first — scripting without a promise to keep produces unfocused scripts. If the user wants to skip, ask for a working title and proceed.
2. **`brand.md`** in the working directory: voice, format (faceless/on-camera), target length. If missing, ask: format? target minutes? niche?
3. **Substance**: what the user knows/wants covered. If the video needs research, offer **yt-research** on the best competing videos — steal their structure, beat their content.
4. **Length math**: narration runs ~150 words/min. 10 min ≈ 1,500 words. State the word target before writing.

## Structure

Build the script from these blocks:

**Hook (0:00-0:30) — write this last, best.** Restate the title's promise visually/concretely, open the main loop (the question the payoff answers), and give a reason to believe ("by the end you'll…"). Never start with "hey guys, welcome back" or channel intro — earn the intro later or skip it.

**Segments (2-4 min each).** Each segment = one idea, one mini-payoff, and a bridge that opens the next loop ("…which works — until winter. Here's why."). Segment boundaries are chapter markers: chapters are worth real watch-time (viewers who can navigate stay longer).

**Re-hooks every ~2-3 min.** Payoff progress on the main loop or raise stakes. If a stretch of script doesn't advance the promise, cut it — length comes from substance, not padding.

**Payoff.** Answer the title's question explicitly. This is the scene the whole video exists for — spend words here.

**Outro (short).** One next-video pitch tied to what they just watched ("if X surprised you, wait until Y"). No "like and subscribe" essay.

## Format — adapt to brand.md

**Faceless:** full word-for-word voiceover + a visual for every beat:

```markdown
## [CH 2 — 02:10] Why the glue fails
VO: Most glue joints don't fail at the glue. They fail...
[VISUAL: macro shot, glue joint splitting in slow motion — cinematic]
```

`[VISUAL:]` cues follow brand.md art direction. Aim for one cue per beat (~every 5-15 seconds of VO) — these become the shot list. After the script, offer to run **yt-visuals**, which turns every cue into batch-ready image + motion prompts with a locked style block.

**On-camera:** spoken script in the creator's brand.md voice (contractions, natural rhythm — read-aloud test it) + `[B-ROLL:]` cues and `[SCREEN:]` overlays where a visual carries the point.

**Mixed:** on-camera base, `[VISUAL:]` cues for cutaway sections.

## Output format

```markdown
# <title>
target: <N> min ≈ <W> words · format: <faceless|on-camera> · promise: <one line>

## Chapter map
00:00 Hook · 00:30 <ch1> · 02:10 <ch2> · ... (paste-ready for description)

<the script, chapter-headed as above>
```

Deliver the full script, then ask: too dense/too light anywhere? Offer the natural next steps — visual prompts for the cues, or yt-packaging if the package was skipped.
