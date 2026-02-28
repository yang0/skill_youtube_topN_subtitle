# 项目说明（中文）

## 项目简介

本项目包含两个可复用的 YouTube 自动化 skill：

1. `youtube-domain-topn-videos`  
按指定领域抓取近 24 小时 TopN 热门视频（标题、简介、数据、链接）。

2. `youtube-subtitle-yt-dlp`  
使用 `yt-dlp` 下载 YouTube 字幕（手动字幕 / 自动字幕）。

## 目录结构

```text
youtube-domain-topn-videos/
youtube-subtitle-yt-dlp/
outputs/                         # 所有运行产物统一放在这里（按年月日）
```

## 依赖安装

```bash
pip install patchright yt-dlp
python -m patchright install chromium
```

## 用法

### 1) 抓取某领域 TopN 热点视频

```bash
python youtube-domain-topn-videos/scripts/fetch_topn_domain_videos.py \
  --domain "AI 增效" \
  --top 10 \
  --hours 24 \
  --cookies-file H:/cookies/youtube.txt
```

### 2) 下载视频字幕

```bash
python youtube-subtitle-yt-dlp/scripts/download_subtitles.py \
  "https://www.youtube.com/watch?v=VIDEO_ID" \
  --cookies H:/cookies/youtube.txt
```

## 输出规范（已统一）

- 所有输出写入项目根目录下 `outputs/YYYY/MM/DD/`
- TopN skill 默认输出文件：
  - `YYYYMMDD_top{N}_{domain}_{hours}h.json`
  - `YYYYMMDD_top{N}_{domain}_{hours}h.md`
- 字幕 skill 默认输出目录：
  - `outputs/YYYY/MM/DD/subtitles/`
- 字幕文件默认带日期前缀：
  - `YYYYMMDD-%(title)...`

## 隐私与提交规范

`.gitignore` 已配置为默认忽略：

- 所有 `outputs/` 运行产物
- 字幕文件（`.vtt/.srt/.ass/.lrc`）
- cookies 和常见密钥文件（如 `*cookie*.txt`, `*.pem`, `*.key`）

建议仅提交：

- skill 脚本（`scripts/`）
- skill 配置（`SKILL.md`, `agents/openai.yaml`, `references/`）
- 项目文档
