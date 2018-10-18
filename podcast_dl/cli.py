#!/usr/bin/env python3
import os
import re
import sys
import functools
from pathlib import Path
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor
from operator import attrgetter
import click
from .site_parser import parse_site, InvalidSite
from .podcasts import PODCASTS
from .podcast_dl import (
    Episode,
    ensure_download_dir,
    download_rss,
    get_all_rss_items,
    filter_rss_items,
    find_missing,
    download_episodes,
    download_episodes_with_progressbar,
)
from .utils import noprint


HELP = """
Download podcast episodes to the given directory

URL or domain or short name for the PODCAST argument can be specified,
e.g. pythonbytes.fm or talkpython or https://talkpython.fm
"""


@functools.total_ordering
class EpisodeParam:
    def __init__(self, original: str):
        self.original = original
        self._spec = original.upper()

    def __hash__(self):
        return hash(self._spec)

    def __eq__(self, other: str):
        """Case insensitive equality."""
        if self.__class__ is not other.__class__:
            return self._spec == other.upper()
        return self._spec == other._spec

    def __lt__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented
        return self._spec < other._spec

    def __str__(self):
        return self.original

    def __repr__(self):
        return repr(self.original)


class EpisodeList(click.ParamType):
    name = "episodelist"

    def convert(self, value, param=None, ctx=None) -> Tuple[List[EpisodeParam], int]:
        biggest_last_n = 0
        episodes = set()
        episode_range_re = re.compile(r"^([0-9]{1,4})-([0-9]{1,4})$")

        for param in value.split(","):
            spec = param.upper()

            if spec.isnumeric():
                episodes.add(EpisodeParam(spec.zfill(4)))
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
                episodes |= set(EpisodeParam(f"{e:04}") for e in range(start, end))
                continue

            if spec:
                episodes.add(EpisodeParam(param))

        return sorted(episodes), biggest_last_n


def list_podcasts(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("The following podcasts are supported:")

    longest_name = max(len(p.name) for p in PODCASTS)
    longest_title = max(len(p.title) for p in PODCASTS)
    format_str = "{:<%s}{:<%s}{}" % (longest_name + 4, longest_title + 4)

    click.echo(format_str.format("Name", "Title", "Webpage"))
    click.echo(format_str.format("----", "-----", "-------"))

    for podcast in sorted(PODCASTS, key=attrgetter("name")):
        click.echo(format_str.format(podcast.name, podcast.title, podcast.url))

    ctx.exit()


@click.command(help=HELP, context_settings={"help_option_names": ["--help", "-h"]})
@click.argument("podcast_name", metavar="PODCAST", required=False)
@click.option(
    "-d",
    "--download-dir",
    type=Path,
    default=None,
    envvar="DOWNLOAD_DIR",
    help=(
        "Where to save downloaded episodes. Can be specified by the "
        "DOWNLOAD_DIR environment variable.  [default: name of PODCAST]"
    ),
)
@click.option(
    "-e",
    "--episodes",
    "episodes_param",
    help="Episodes to download.",
    type=EpisodeList(),
)
@click.option(
    "-s", "--show-episodes", help="Show the list of episodes for PODCAST.", is_flag=True
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
    "-p",
    "--progress",
    is_flag=True,
    help="Show progress bar instead of detailed messages during download.",
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
    "-v", "--verbose", is_flag=True, help="Show detailed informations during download."
)
@click.version_option(None, "-V", "--version")
@click.pass_context
def main(
    ctx,
    podcast_name,
    download_dir,
    max_threads,
    episodes_param,
    show_episodes,
    progress,
    verbose,
):
    if len(sys.argv) == 1:
        help_text = ctx.command.get_help(ctx)
        click.echo(help_text)
        return 0

    # We have to handle this because it's not required,
    # to be able to show help when run without arguments
    if podcast_name is None:
        raise click.UsageError('Missing argument "PODCAST".', ctx=ctx)

    try:
        podcast = parse_site(podcast_name)
    except InvalidSite:
        raise click.BadArgumentUsage(
            f'The given podcast "{podcast_name}" is not supported or invalid.\n'
            f'See the list of supported podcasts with "{ctx.info_name} --list-podcasts"',
            ctx=ctx,
        )
        return 1

    if download_dir is None:
        download_dir = Path(podcast.name)

    vprint = click.secho if verbose else noprint

    ensure_download_dir(download_dir)
    rss_root = download_rss(podcast.rss)
    all_rss_items = get_all_rss_items(rss_root, podcast.rss_parser)

    if episodes_param is not None:
        episode_params, last_n = episodes_param
        rss_items, unknown_episodes = filter_rss_items(
            all_rss_items, episode_params, last_n
        )
        if unknown_episodes:
            click.secho(
                "WARNING: Unknown episode numbers:"
                + ", ".join(str(e) for e in unknown_episodes),
                fg="yellow",
                err=True,
            )
    else:
        rss_items = all_rss_items

    if show_episodes:
        click.echo("List of episodes:")
        for item in rss_items:
            episodenum = item.episode or " N/A"
            click.echo(f"{episodenum} - {item.title}")
        return 0

    episodes = (Episode(item, podcast, download_dir) for item in rss_items)
    missing_episodes = find_missing(episodes, vprint)

    if not missing_episodes:
        click.secho("Every episode is downloaded.", fg="green")
        return 0

    click.echo(f"Found a total of {len(missing_episodes)} missing episodes.")
    try:
        if progress:
            download_episodes_with_progressbar(missing_episodes, max_threads)
        else:
            download_episodes(missing_episodes, max_threads, vprint)
    except KeyboardInterrupt:
        click.secho(
            "CTRL-C caught, finishing incomplete downloads...\n"
            "Press one more time if you want to stop prematurely.",
            fg="yellow",
            err=True,
        )
        return 1

    click.secho("Done.", fg="green")
    return 0
