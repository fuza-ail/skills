#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "youtube-transcript-api>=1.0",
#     "yt-dlp",
# ]
# ///
"""Fetch YouTube video/channel metadata and transcripts for research.

Usage:
    uv run yt_fetch.py video <url_or_id> [--out DIR] [--timestamps]
    uv run yt_fetch.py channel <url_or_handle> [--limit N] [--out DIR]
    uv run yt_fetch.py transcript <url_or_id>... [--out DIR] [--timestamps] [--lang en]

Outputs files into --out (default: ./yt_data):
    video    -> <id>.meta.json + <id>.transcript.md
    channel  -> channel.json (metadata + video list, sorted by views)
    transcript -> <id>.transcript.md per video
"""

import argparse
import json
import re
import sys
from pathlib import Path

VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def extract_video_id(url_or_id: str) -> str:
    if VIDEO_ID_RE.match(url_or_id):
        return url_or_id
    patterns = [
        r"(?:v=|/shorts/|/embed/|youtu\.be/|/live/)([A-Za-z0-9_-]{11})",
    ]
    for p in patterns:
        m = re.search(p, url_or_id)
        if m:
            return m.group(1)
    sys.exit(f"error: could not extract video id from: {url_or_id}")


def normalize_channel_url(target: str) -> str:
    if target.startswith("@"):
        return f"https://www.youtube.com/{target}/videos"
    if "youtube.com" in target:
        base = target.rstrip("/")
        if not base.endswith(("/videos", "/streams", "/shorts")):
            base += "/videos"
        return base
    # bare channel name -> treat as handle
    return f"https://www.youtube.com/@{target}/videos"


def fetch_transcript(video_id: str, langs: list[str], timestamps: bool) -> tuple[str, str]:
    """Return (language_code, markdown_text). Tries preferred langs, then any
    available transcript, then auto-translation to the first preferred lang."""
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import NoTranscriptFound

    api = YouTubeTranscriptApi()
    try:
        fetched = api.fetch(video_id, languages=langs)
    except NoTranscriptFound:
        listing = api.list(video_id)
        first = next(iter(listing))
        try:
            fetched = first.translate(langs[0]).fetch() if first.is_translatable else first.fetch()
        except Exception:
            fetched = first.fetch()

    lines = []
    for snip in fetched:
        text = snip.text.replace("\n", " ").strip()
        if not text:
            continue
        if timestamps:
            m, s = divmod(int(snip.start), 60)
            h, m = divmod(m, 60)
            stamp = f"[{h}:{m:02d}:{s:02d}]" if h else f"[{m}:{s:02d}]"
            lines.append(f"{stamp} {text}")
        else:
            lines.append(text)
    joiner = "\n" if timestamps else " "
    return fetched.language_code, joiner.join(lines)


def ydl_opts(extra: dict | None = None) -> dict:
    opts = {"quiet": True, "no_warnings": True, "skip_download": True}
    if extra:
        opts.update(extra)
    return opts


def cmd_video(args):
    import yt_dlp

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    vid = extract_video_id(args.target)
    url = f"https://www.youtube.com/watch?v={vid}"

    with yt_dlp.YoutubeDL(ydl_opts()) as ydl:
        info = ydl.extract_info(url, download=False)

    meta = {
        "id": vid,
        "title": info.get("title"),
        "channel": info.get("channel"),
        "channel_id": info.get("channel_id"),
        "channel_follower_count": info.get("channel_follower_count"),
        "upload_date": info.get("upload_date"),
        "duration_seconds": info.get("duration"),
        "view_count": info.get("view_count"),
        "like_count": info.get("like_count"),
        "comment_count": info.get("comment_count"),
        "tags": info.get("tags", []),
        "categories": info.get("categories", []),
        "chapters": [
            {"title": c["title"], "start": c["start_time"]}
            for c in (info.get("chapters") or [])
        ],
        "description": (info.get("description") or "")[:3000],
    }
    meta_path = out / f"{vid}.meta.json"
    meta_path.write_text(json.dumps(meta, indent=1, ensure_ascii=False))

    try:
        lang, text = fetch_transcript(vid, args.lang.split(","), args.timestamps)
        t_path = out / f"{vid}.transcript.md"
        header = f"# {meta['title']}\nchannel: {meta['channel']} | lang: {lang} | {url}\n\n"
        t_path.write_text(header + text)
        t_note = str(t_path)
    except Exception as e:
        t_note = f"TRANSCRIPT UNAVAILABLE: {type(e).__name__}: {e}"

    print(json.dumps({"meta": str(meta_path), "transcript": t_note,
                      "title": meta["title"], "views": meta["view_count"]}, ensure_ascii=False))


def cmd_channel(args):
    import yt_dlp

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    url = normalize_channel_url(args.target)

    with yt_dlp.YoutubeDL(ydl_opts({"extract_flat": True, "playlist_items": f"1-{args.limit}"})) as ydl:
        info = ydl.extract_info(url, download=False)

    videos = []
    for e in info.get("entries") or []:
        if not e:
            continue
        videos.append({
            "id": e.get("id"),
            "title": e.get("title"),
            "duration_seconds": e.get("duration"),
            "view_count": e.get("view_count"),
        })
    videos.sort(key=lambda v: v.get("view_count") or 0, reverse=True)

    data = {
        "channel": info.get("channel") or info.get("uploader") or info.get("title"),
        "channel_id": info.get("channel_id") or info.get("id"),
        "subscribers": info.get("channel_follower_count"),
        "url": url,
        "videos_fetched": len(videos),
        "videos_by_views": videos,
    }
    path = out / "channel.json"
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False))
    print(json.dumps({"channel_json": str(path), "channel": data["channel"],
                      "videos": len(videos)}, ensure_ascii=False))


def cmd_transcript(args):
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    results = []
    for target in args.targets:
        vid = extract_video_id(target)
        try:
            lang, text = fetch_transcript(vid, args.lang.split(","), args.timestamps)
            path = out / f"{vid}.transcript.md"
            path.write_text(f"# video {vid} | lang: {lang}\n\n{text}")
            results.append({"id": vid, "transcript": str(path), "chars": len(text)})
        except Exception as e:
            results.append({"id": vid, "error": f"{type(e).__name__}: {e}"})
    print(json.dumps(results, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--out", default="yt_data", help="output directory")
    common.add_argument("--timestamps", action="store_true", help="include [mm:ss] timestamps")
    common.add_argument("--lang", default="en", help="comma-separated preferred transcript languages")

    p_video = sub.add_parser("video", parents=[common], help="fetch one video's metadata + transcript")
    p_video.add_argument("target", help="video URL or 11-char id")
    p_video.set_defaults(func=cmd_video)

    p_channel = sub.add_parser("channel", parents=[common], help="fetch channel metadata + video list")
    p_channel.add_argument("target", help="channel URL, @handle, or name")
    p_channel.add_argument("--limit", type=int, default=30, help="max videos to list (default 30)")
    p_channel.set_defaults(func=cmd_channel)

    p_tr = sub.add_parser("transcript", parents=[common], help="fetch transcripts only, batch")
    p_tr.add_argument("targets", nargs="+", help="video URLs or ids")
    p_tr.set_defaults(func=cmd_transcript)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
