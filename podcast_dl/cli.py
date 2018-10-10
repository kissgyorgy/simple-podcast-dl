#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor
from operator import attrgetter
import click
from .site_parser import parse_site, InvalidSite
from .podcasts import PODCASTS, LONGEST_NAME, LONGEST_TITLE
from .podcast_dl import (
    Episode,
    ensure_download_dir,
    download_rss,
    get_all_rss_items,
    filter_rss_items,
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

    def convert(self, value, param=None, ctx=None) -> Tuple[List[str], int]:
        biggest_last_n = 0
        episodes = set()
        episode_range_re = re.compile(r"([0-9]{1,4})-([0-9]{1,4})")

        for spec in value.upper().split(","):
            if spec.isnumeric():
                episodes.add(spec.zfill(4))
                continue

            if spec == "LAST":
                biggest_last_n = max(biggest_last_n, 1)
                continue

            if spec.startswith("LAST:"):
                # will be added at the end once, when we know the biggest n value
                n = int(spec.split(":")[1])
                biggest_last_n = max(biggest_last_n, n)
                continue

            m = episode_range_re.match(spec)
            if m:
                first, last = m.group(1, 2)
                start, end = int(first), int(last) + 1
                episodes |= set(f"{e:04}" for e in range(start, end))
                continue

            if spec:
                episodes.add(spec)

        return sorted(episodes), biggest_last_n


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
    show_default="name of PODCAST",
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
    rss_items = get_all_rss_items(rss_root, podcast.rss_parser)

    if episode_numbers is not None:
        rss_items = filter_rss_items(rss_items, episode_numbers)

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
