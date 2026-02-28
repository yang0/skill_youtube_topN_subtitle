#!/usr/bin/env python3
"""Download YouTube subtitle files with yt-dlp."""

from __future__ import annotations

import argparse
import shlex
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List

DEFAULT_COOKIES = Path(r"H:\cookies\youtube.txt")
DEFAULT_SUB_LANGS = "zh-Hans,zh-Hant,zh-CN,zh-TW,zh,en.*"
DEFAULT_SUB_FORMAT = "best"
SCRIPT_FILE = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_FILE.parents[2]


def build_default_output_dir(run_time: datetime) -> Path:
    return (
        PROJECT_ROOT
        / "outputs"
        / f"{run_time.year:04d}"
        / f"{run_time.month:02d}"
        / f"{run_time.day:02d}"
        / "subtitles"
    )


def build_output_template(date_label: str) -> str:
    return f"%(uploader|unknown)s/{date_label}-%(title).180B [%(id)s].%(ext)s"


DEFAULT_OUTPUT_DIR = build_default_output_dir(datetime.now())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download subtitle files for YouTube URLs using yt-dlp."
    )
    parser.add_argument("urls", nargs="+", help="YouTube video/playlist URLs")
    parser.add_argument(
        "--cookies",
        default=str(DEFAULT_COOKIES),
        help=f"Path to cookies.txt (default: {DEFAULT_COOKIES})",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help=(
            "Directory to store subtitle files "
            f"(default: {DEFAULT_OUTPUT_DIR})"
        ),
    )
    parser.add_argument(
        "--mode",
        choices=("both", "manual", "auto"),
        default="both",
        help="Subtitle source: manual subtitles, auto captions, or both (default: both)",
    )
    parser.add_argument(
        "--sub-langs",
        default=DEFAULT_SUB_LANGS,
        help=f"yt-dlp --sub-langs value (default: {DEFAULT_SUB_LANGS})",
    )
    parser.add_argument(
        "--sub-format",
        default=DEFAULT_SUB_FORMAT,
        help=f"yt-dlp --sub-format value (default: {DEFAULT_SUB_FORMAT})",
    )
    parser.add_argument(
        "--convert-to",
        default="none",
        help="Convert subtitle format via --convert-subs, e.g. srt/vtt/ass/lrc (default: none)",
    )
    parser.add_argument(
        "--yt-dlp-bin",
        default="yt-dlp",
        help="yt-dlp binary or command (default: yt-dlp)",
    )
    parser.add_argument(
        "--no-playlist",
        action="store_true",
        help="Only process a single video even if URL points to a playlist",
    )
    parser.add_argument(
        "--playlist-items",
        help="Only process selected playlist items, e.g. 1,3,5-8",
    )
    parser.add_argument(
        "--extra-arg",
        action="append",
        default=[],
        help="Extra raw yt-dlp argument (repeatable), e.g. --extra-arg \"--proxy http://127.0.0.1:7890\"",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the final yt-dlp command without running it",
    )
    return parser.parse_args()


def resolve_yt_dlp_command(raw_command: str) -> List[str]:
    parsed = shlex.split(raw_command)
    if not parsed:
        raise ValueError("--yt-dlp-bin cannot be empty")

    if len(parsed) == 1 and parsed[0] == "yt-dlp":
        if shutil.which("yt-dlp"):
            return ["yt-dlp"]
        return [sys.executable, "-m", "yt_dlp"]

    return parsed


def ensure_cookie_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(
            f"Cookie file not found: {path}\n"
            "Provide --cookies <path>. For this skill, expected default is H:\\cookies\\youtube.txt."
        )


def build_command(args: argparse.Namespace) -> List[str]:
    run_time = datetime.now()
    date_label = run_time.strftime("%Y%m%d")

    cookies = Path(args.cookies).expanduser()
    ensure_cookie_file(cookies)

    output_dir = Path(args.output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_template = build_output_template(date_label)

    cmd = resolve_yt_dlp_command(args.yt_dlp_bin)
    cmd.extend(
        [
            "--skip-download",
            "--ignore-errors",
            "--newline",
            "--paths",
            str(output_dir),
            "--output",
            output_template,
            "--cookies",
            str(cookies),
            "--sub-langs",
            args.sub_langs,
            "--sub-format",
            args.sub_format,
        ]
    )

    if args.mode in ("both", "manual"):
        cmd.append("--write-subs")
    if args.mode in ("both", "auto"):
        cmd.append("--write-auto-subs")

    if args.convert_to.lower() != "none":
        cmd.extend(["--convert-subs", args.convert_to])

    if args.no_playlist:
        cmd.append("--no-playlist")
    if args.playlist_items:
        cmd.extend(["--playlist-items", args.playlist_items])

    for extra in args.extra_arg:
        cmd.extend(shlex.split(extra))

    cmd.extend(args.urls)
    return cmd


def main() -> int:
    args = parse_args()

    try:
        cmd = build_command(args)
    except Exception as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 2

    print(f"[info] Running: {shlex.join(cmd)}")
    if args.dry_run:
        return 0

    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except FileNotFoundError as exc:
        print(
            f"[error] Unable to run yt-dlp command: {exc}\n"
            "Install yt-dlp first: pip install -U yt-dlp",
            file=sys.stderr,
        )
        return 127


if __name__ == "__main__":
    raise SystemExit(main())
