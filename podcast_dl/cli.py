#!/usr/bin/env python3
import os
import sys
from pathlib import Path
import click
from operator import attrgetter
from .site_parser import parse_site, InvalidSite
from .podcasts import PODCASTS, LONGEST_NAME, LONGEST_TITLE
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


def list_podcasts(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("The following podcasts are supported:")
    format_str = "{:<%s}{:<%s}{}" % (LONGEST_NAME + 4, LONGEST_TITLE + 4)
    click.echo(format_str.format("Name", "Title", "Webpage"))
    click.echo(format_str.format("----", "-----", "-------"))
    for podcast in sorted(PODCASTS, key=attrgetter("name")):
        click.echo(format_str.format(podcast.name, podcast.title, podcast.url))
    ctx.exit()


@click.command(help=HELP, context_settings={"help_option_names": ["--help", "-h"]})
@click.argument("podcast_name", metavar="PODCAST", required=False)
@click.option(
    "-d", "--download-dir", type=Path, default="episodes", envvar="DOWNLOAD_DIR"
)
@click.option("-t", "--max-threads", type=int, default=10, envvar="MAX_THREADS")
@click.option(
    "-l",
    "--list-podcasts",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=list_podcasts,
)
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
        print(
            f'The given podcast "{podcast_name}" is not supported or invalid.\n'
            f'See the list of supported podcasts with "{ctx.info_name} --list-podcasts"'
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
