#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from operator import attrgetter
import click
from .site_parser import parse_site, InvalidSite
from .podcasts import PODCASTS, LONGEST_NAME, LONGEST_TITLE
from .podcast_dl import (
    Episode,
    ensure_download_dir,
    download_rss,
    get_rss_items,
    find_missing,
    download_episodes,
)

HELP = """
Download podcast episodes to the given directory

URL or domain or short name for the PODCAST argument can be specified,
e.g. pythonbytes.fm or talkpython or https://talkpython.fm
"""


class EpisodeList(click.ParamType):
    name = "episodelist"

    def convert(self, value, param, ctx):
        return sorted([e.zfill(4) for e in value.split(",")])


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


def podcast_name_argument():
    ctx = click.get_current_context()
    return ctx.params["podcast_name"]


@click.command(help=HELP, context_settings={"help_option_names": ["--help", "-h"]})
@click.argument("podcast_name", metavar="PODCAST", required=False)
@click.option(
    "-d",
    "--download-dir",
    type=Path,
    default=podcast_name_argument,
    envvar="DOWNLOAD_DIR",
    help=(
        "Where to save downloaded episodes. Can be specified by the "
        "DOWNLOAD_DIR environment variable."
    ),
    show_default="specified PODCAST",
)
@click.option(
    "-t",
    "--max-threads",
    type=click.IntRange(0, 10),
    default=10,
    envvar="MAX_THREADS",
    help=(
        "Number of threads to start for the download. Can be specified"
        " with the MAX_THREADS environment variable."
    ),
    show_default=True,
)
@click.option(
    "-l",
    "--list-podcasts",
    help="List of supported podcasts, ordered by name.",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=list_podcasts,
)
@click.option(
    "-e",
    "--episodes",
    "episode_numbers",
    help="Episodes to download.",
    type=EpisodeList(),
)
@click.version_option(None, "-V", "--version")
@click.pass_context
def main(ctx, podcast_name, download_dir, max_threads, episode_numbers):
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
    rss_root = download_rss(podcast.rss)
    rss_items = get_rss_items(rss_root, podcast.rss_parser, episode_numbers)
    episodes = (Episode(item, podcast, download_dir) for item in rss_items)
    missing_episodes = find_missing(episodes)

    if not missing_episodes:
        print("Every episode is downloaded.", flush=True)
        return 0

    print(f"Found a total of {len(missing_episodes)} missing episodes.", flush=True)
    try:
        download_episodes(missing_episodes, max_threads)
    except KeyboardInterrupt:
        print(
            "CTRL-C caught, finishing incomplete downloads...\n",
            "Press one more time if you want to stop prematurely.",
            file=sys.stderr,
            flush=True,
        )

    return 0
