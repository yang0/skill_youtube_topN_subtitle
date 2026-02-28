# Project Documentation (English)

## Overview

This repository contains two reusable YouTube automation skills:

1. `youtube-domain-topn-videos`  
Fetch TopN hot videos in the last 24 hours for any domain (title, intro, metrics, link).

2. `youtube-subtitle-yt-dlp`  
Download YouTube subtitles using `yt-dlp` (manual subtitles and/or auto captions).

## Structure

```text
youtube-domain-topn-videos/
youtube-subtitle-yt-dlp/
outputs/                         # Unified runtime outputs (date-based)
```

## Install Dependencies

```bash
pip install patchright yt-dlp
python -m patchright install chromium
```

## Usage

### 1) Fetch domain-specific TopN videos

```bash
python youtube-domain-topn-videos/scripts/fetch_topn_domain_videos.py \
  --domain "AI productivity" \
  --top 10 \
  --hours 24 \
  --cookies-file H:/cookies/youtube.txt
```

### 2) Download subtitles

```bash
python youtube-subtitle-yt-dlp/scripts/download_subtitles.py \
  "https://www.youtube.com/watch?v=VIDEO_ID" \
  --cookies H:/cookies/youtube.txt
```

## Output Convention (Unified)

- All outputs are written to project root `outputs/YYYY/MM/DD/`
- Default TopN output files:
  - `YYYYMMDD_top{N}_{domain}_{hours}h.json`
  - `YYYYMMDD_top{N}_{domain}_{hours}h.md`
- Default subtitle output directory:
  - `outputs/YYYY/MM/DD/subtitles/`
- Subtitle filenames include a date prefix:
  - `YYYYMMDD-%(title)...`

## Privacy and Commit Policy

`.gitignore` now excludes:

- All runtime outputs under `outputs/`
- Subtitle artifacts (`.vtt/.srt/.ass/.lrc`)
- Cookie files and common secret/key files (for example `*cookie*.txt`, `*.pem`, `*.key`)

Recommended commit scope:

- Code under `scripts/`
- Skill configuration (`SKILL.md`, `agents/openai.yaml`, `references/`)
- Documentation only
