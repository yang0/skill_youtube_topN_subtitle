---
name: youtube-domain-topn-videos
description: Collect top-N YouTube hot videos for any domain from the last 24 hours with Patchright, then output title, intro snippet, metrics, and link. Use when asked for a ranked trend digest in a specific field such as AI, finance, robotics, gaming, cybersecurity, or any other topic.
---

# YouTube Domain TopN Videos

## Overview

Use Patchright to crawl YouTube search results filtered to "Today", generate multi-query candidates from a chosen domain, rank by a recency-adjusted hot score, and export top-N items.

## Run Workflow

1. Install runtime dependencies.
2. Update search queries when needed.
3. Run the scraper.
4. Read JSON/Markdown outputs and continue reporting.

## Install

```bash
pip install patchright
python -m patchright install chromium
```

## Configure Queries

Default query templates are in `references/query_templates.txt`.

- Use `{domain}` placeholder in each line.
- Example line: `{domain} tutorial`
- You can override with `--queries-file` to pass explicit queries.

## Execute

```bash
python scripts/fetch_topn_domain_videos.py --domain "robotics" --top 10 --hours 24 --cookies-file H:/cookies/youtube.txt
```

Useful options:
- `--domain <text>`: Required domain/topic, for example `cybersecurity` or `跨境电商`.
- `--queries-file <path>`: Use explicit query lines directly.
- `--query-templates-file <path>`: Use `{domain}` templates.
- `--cookies-file <path>`: Load YouTube cookies (`Netscape` or `JSON`).
- `--max-results-per-query <n>`: Increase candidate pool before ranking.
- `--gl <country>` and `--hl <lang>`: Control YouTube geo/language.
- `--headed`: Run non-headless for debugging.
- `--output-json <path>` and `--output-md <path>`: Change output files.

Default output layout:
- Project root directory: `outputs/YYYY/MM/DD/`
- Filename pattern: `YYYYMMDD_top{N}_{domain}_{hours}h.json` and `.md`

## Output Contract

Each ranked record includes:
- `title`: Video title.
- `intro`: Description snippet from search card.
- `data`: Channel, views, publish text, age-hours estimate, duration, hot score, domain, matched queries.
- `link`: Canonical YouTube watch link.

## Troubleshooting

- If results are empty, increase `--scroll-rounds` and `--max-results-per-query`.
- If region bias is wrong, set `--gl` explicitly (for example `US`, `JP`, `TW`).
- If YouTube UI changes, update DOM selectors in `scripts/fetch_topn_domain_videos.py`.
