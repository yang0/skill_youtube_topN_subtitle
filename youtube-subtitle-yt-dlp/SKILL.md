---
name: youtube-subtitle-yt-dlp
description: Extract subtitle files from YouTube video or playlist links using yt-dlp and authenticated cookies. Use when asked to download manual subtitles or auto captions from YouTube URLs and save them locally as subtitle files (for example .vtt/.srt).
---

# Youtube Subtitle Yt Dlp

## Overview

Use yt-dlp to download subtitle tracks only (no video download).  
Default cookie file is `H:\cookies\youtube.txt`.
Output is written under project root `outputs/YYYY/MM/DD/subtitles/`.

## Install Dependencies

```bash
pip install -U yt-dlp
```

## Run

```bash
python scripts/download_subtitles.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Common examples:

- Manual subtitles only:
```bash
python scripts/download_subtitles.py "<youtube-url>" --mode manual
```

- Auto captions only:
```bash
python scripts/download_subtitles.py "<youtube-url>" --mode auto
```

- Convert to SRT:
```bash
python scripts/download_subtitles.py "<youtube-url>" --convert-to srt
```

- Use a non-default cookie file:
```bash
python scripts/download_subtitles.py "<youtube-url>" --cookies "D:\cookies\youtube.txt"
```

## Output Contract

- Download subtitle files only; do not download media streams.
- Write files under project root `outputs/YYYY/MM/DD/subtitles/` by default.
- Filename template is:
  `%(uploader|unknown)s/YYYYMMDD-%(title).180B [%(id)s].%(ext)s`
- Keep original subtitle format unless `--convert-to` is set.

## Key Options

- `--cookies <path>`: Path to YouTube cookies file. Default: `H:\cookies\youtube.txt`.
- `--sub-langs <expr>`: Subtitle language selector. Default:
  `zh-Hans,zh-Hant,zh-CN,zh-TW,zh,en.*`
- `--mode both|manual|auto`: Download manual subtitles, auto captions, or both.
- `--no-playlist`: Force single-video behavior.
- `--playlist-items <range>`: Select specific playlist items.
- `--extra-arg "<yt-dlp-arg>"`: Pass extra yt-dlp flags.

## Troubleshooting

- Cookie error:
  check that `H:\cookies\youtube.txt` exists, or override with `--cookies`.
- Empty subtitle output:
  rerun with `--mode auto` to force automatic captions.
- Region/login issues:
  pass proxy or geo args through `--extra-arg`, for example
  `--extra-arg "--proxy http://127.0.0.1:7890"`.
- Need to inspect final command only:
  use `--dry-run`.

## Script

- `scripts/download_subtitles.py`: Main entrypoint for subtitle extraction.
