#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path
from .site_parser import parse_site, InvalidSite
from .podcasts import PODCAST_MAP
from .podcast_dl import (
    ensure_download_dir,
    download_rss,
    make_episodes,
    find_missing,
    download_episodes,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download podcast episodes to the given directory"
    )
    parser.add_argument(
        "podcast",
        help=(
            "URL or domain or short name for the podcast, "
            "e.g. pythonbytes.fm or talkpython or https://talkpython.fm"
        ),
    )

    parser.add_argument(
        "-d",
        "--download-dir",
        type=Path,
        default=os.environ.get("DOWNLOAD_DIR", "episodes"),
    )

    parser.add_argument(
        "-t", "--max-threads", type=int, default=os.environ.get("MAX_THREADS", 10)
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        podcast = parse_site(args.podcast)
    except InvalidSite:
        supported_podcasts = tuple(PODCAST_MAP.keys())
        print(
            f'The given podcast "{args.podcast}" is not supported or invalid.\n'
            f"Try one of: {supported_podcasts}"
        )
        return 1

    ensure_download_dir(args.download_dir)
    xml_root = download_rss(podcast.rss)
    all_episodes = make_episodes(xml_root, podcast, args.download_dir)
    missing_episodes = find_missing(all_episodes)

    if not missing_episodes:
        print("Every episode is downloaded.", flush=True)
        return 0

    print(f"Found a total of {len(missing_episodes)} missing episodes.", flush=True)
    download_episodes(missing_episodes, args.max_threads)
    return 0


if __name__ == "__main__":
    sys.exit(main())
