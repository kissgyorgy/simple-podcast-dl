#!/usr/bin/env python3
import os
import sys
from pathlib import Path
import click
from .site_parser import parse_site, InvalidSite
from .podcasts import PODCAST_MAP
from .podcast_dl import (
    ensure_download_dir,
    download_rss,
    make_episodes,
    find_missing,
    download_episodes,
)

HELP = """
Download podcast episodes to the given directory

URL or domain or short name for the PODCAST argument can be specified,
e.g. pythonbytes.fm or talkpython or https://talkpython.fm
"""


@click.command(help=HELP, context_settings={"help_option_names": ["--help", "-h"]})
@click.argument("podcast_name", metavar="PODCAST", required=False)
@click.option(
    "-d", "--download-dir", type=Path, default="episodes", envvar="DOWNLOAD_DIR"
)
@click.option("-t", "--max-threads", type=int, default=10, envvar="MAX_THREADS")
@click.version_option(None, "-V", "--version")
@click.pass_context
def main(ctx, podcast_name, download_dir, max_threads):
    if len(sys.argv) == 1:
        help_text = ctx.command.get_help(ctx)
        click.echo(help_text)
        return 0

    try:
        podcast = parse_site(podcast_name)
    except InvalidSite:
        supported_podcasts = tuple(PODCAST_MAP.keys())
        print(
            f'The given podcast "{podcast_name}" is not supported or invalid.\n'
            f"Try one of: {supported_podcasts}"
        )
        return 1

    ensure_download_dir(download_dir)
    xml_root = download_rss(podcast.rss)
    all_episodes = make_episodes(xml_root, podcast, download_dir)
    missing_episodes = find_missing(all_episodes)

    if not missing_episodes:
        print("Every episode is downloaded.", flush=True)
        return 0

    print(f"Found a total of {len(missing_episodes)} missing episodes.", flush=True)
    download_episodes(missing_episodes, max_threads)
    return 0
