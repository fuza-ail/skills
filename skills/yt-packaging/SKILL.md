---
name: yt-packaging
description: Package a YouTube video before it's made — title options, thumbnail concepts, and ready-to-paste image-generation prompts (Midjourney, Flux, Nano Banana, DALL-E) tuned for CTR. Use this whenever the user has a video idea and needs a title, wants thumbnail ideas or thumbnail prompts, asks "what should I call this video", wants to improve CTR, or is starting work on a new video — packaging comes BEFORE scripting, so also trigger when a user asks for a script but has no title/thumbnail yet.
---

# YouTube Packaging (title + thumbnail)

Packaging decides whether a video gets clicked; the script decides whether it gets watched. Pro creators lock the package **before** writing the script, because the title is a promise and the script's job is to keep it. Hold that order: if the user asks for a script with no package, offer to package first.

## Inputs

1. **The video idea** — one sentence from the user.
2. **`brand.md`** in the working directory — read it if it exists (voice, palette, thumbnail style, art direction, format). If missing, don't block: ask 2 quick questions (niche + faceless/on-camera) and suggest running **yt-brand** later.
3. **Competitor evidence (optional but powerful)** — if `yt_data/` exists from a **yt-research** run, scan the top titles for patterns in this niche. If the user wants stronger grounding, offer to run yt-research on the niche's top channel first.

## Step 1 — Titles

Write **8-10 candidates** across different mechanisms, not 10 variations of one:

- Curiosity gap ("The mistake hiding in every beginner's first table")
- Stakes/negativity ("Stop sanding like this — it's ruining your finish")
- Number/list ("7 tools I regret buying")
- Outcome/transformation ("$40 flea-market chair → showroom piece")
- Authority/contrarian ("Woodworkers are wrong about wood glue")

Rules that matter: under ~60 characters (truncation), front-load the hook words, no clickbait the video can't cash — retention collapses and the algorithm punishes it. Match brand.md voice.

Then **rank them**: pick your top 3 and say why each would win — don't hand the user an unranked list.

## Step 2 — Thumbnail concepts

For the top title(s), give **3 distinct concepts**. Each concept:

```markdown
### Concept <n>: <two-word name>
- Composition: <single focal point, where the eye goes, rule of thirds>
- Text overlay: "<max 4 words>" — must NOT repeat the title; it completes it
- Emotion/story: <what feeling in 200ms at 10% zoom>
- Color: <from brand palette; contrast strategy vs YouTube's white/dark UI>
```

CTR fundamentals: one focal point, high contrast, readable at thumbnail size, faces with strong emotion outperform for on-camera channels, and the title+thumbnail together should raise a question only clicking answers.

## Step 3 — Image-generation prompts

For each concept, write a **ready-to-paste prompt block**. Use brand.md's art direction. Always 16:9.

```markdown
**Midjourney / Flux:**
<subject>, <composition>, <lighting>, <style + art direction keywords>,
<mood>, 16:9 --ar 16:9 <--no text, if text will be added in an editor>

**Nano Banana / DALL-E (natural language):**
<2-3 sentence description: scene, camera, lighting, style. State "leave
clear space at <left/right> for text overlay". 16:9.>
```

Prompt craft: name a lens/camera feel ("shot on 35mm, shallow depth of field"), one strong light source, exaggerate the key element ~20% (thumbnails are seen tiny), and generate text-free — text overlays belong in an editor, AI text still breaks.

## Output

Deliver as one markdown block: ranked titles → concepts → prompts. If working in a project directory, also save to `packaging/<slug>.md` so yt-script can read the locked package later. End by asking which title+concept the user picks, then point them at **yt-script** to write against that promise.
