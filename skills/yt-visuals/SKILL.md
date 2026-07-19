---
name: yt-visuals
description: Turn a faceless YouTube script's [VISUAL:] cues into a complete, batch-ready visual prompt sheet — numbered image-generation prompts (Midjourney, Flux, Nano Banana) plus image-to-video motion prompts (Runway, Kling, Sora, Hailuo, Pika) with a locked style block for scene-to-scene consistency. Use whenever the user has a script or scene list and needs the visuals made: "generate the prompts for my script", "make the visuals", "image prompts for each scene", "turn this script into AI video prompts", or after yt-script finishes a faceless script. Also use to build a reusable character/style sheet for a channel.
---

# YouTube Visuals (faceless prompt pipeline)

A faceless video lives or dies on visual consistency. Fifty beautiful scenes in fifty styles read as amateur; fifty scenes in one style read as a channel. This skill converts a script into a production-ready prompt sheet where consistency is engineered in, not hoped for.

## Inputs

1. **The script** — from **yt-script** (has `[VISUAL:]` cues with chapter timestamps) or any script/scene list the user provides. If cues are missing, derive one visual per beat (~every 5-15 seconds of VO) yourself and show the scene list for approval before writing prompts.
2. **`brand.md`** — the `art direction` line under Visual identity is the seed of the style block. If missing, ask for 3 reference adjectives + one film/photographer whose look to borrow, and suggest **yt-brand**.
3. **Targets** — which image tool and which video tool the user actually uses. Ask once, then only emit those formats (emitting all five is noise).

## Step 1 — Lock the style block

Write ONE style block and reuse it verbatim in every prompt. This is the consistency mechanism — never restyle per scene.

```markdown
STYLE: <medium, e.g. cinematic 35mm film still>, <palette from brand.md>,
<lighting, e.g. single-source, soft shadows>, <mood>, <lens/DoF>,
<grain/texture> --ar 16:9
NEGATIVE: text, watermark, logo, extra fingers, distorted face
```

If the channel has recurring characters, add a **character sheet**: name, one locked physical description (reused word-for-word), wardrobe. Tell the user to generate the character once, then use image-reference / seed features (`--cref` in Midjourney, reference images in Flux/Kling) for every scene containing them.

## Step 2 — The prompt sheet

One entry per `[VISUAL:]` cue, numbered to match script chapters, in script order:

```markdown
### 014 · [CH 3 — 04:32] glue joint failing
VO context: "…they fail at the wood fibers around it."
**Image (Flux):** macro shot of a wooden joint splitting apart, fibers
tearing in half-light, {STYLE}
**Motion (Kling):** slow push-in as the crack propagates, dust particles
drift, subtle camera shake at the snap. 4s.
```

Rules that keep the batch usable:
- Every image prompt ends with `{STYLE}` expanded verbatim — no per-scene drift.
- One subject, one action per scene. If a cue packs two ideas, split into two numbered scenes.
- Motion prompts describe **camera + one motion**, 3-6 seconds; image-to-video tools fail on complex choreography.
- Vary shot sizes deliberately (wide establisher → medium → macro detail) so the edit has rhythm — flag runs of 3+ identical shot sizes.
- No text in images (AI text breaks; overlays belong in the editor).

## Step 3 — Deliver

Save to `visuals/<slug>.md`: style block + character sheet at top, then all scenes. Tell the user the workflow: generate the style block's test scene first, adjust the block until it matches their taste, THEN batch the rest — fixing style after 50 generations is expensive.

Offer next steps: regenerate any scene's prompt on feedback, or thumbnail prompts via **yt-packaging** if not done yet.
