import sys
import asyncio
from typing import List, Tuple
from pathlib import Path
from urllib.parse import urlparse
from operator import attrgetter
from concurrent.futures import ThreadPoolExecutor, wait
import click
import aiohttp
from lxml import etree
from .podcasts import Podcast
from .rss_parsers import BaseItem


class Episode:
    def __init__(self, item: BaseItem, download_dir: Path):
        self.url = item.url
        self.number = item.episode
        self.title = item.title
        self.filename = item.filename
        self.download_dir = download_dir
        self.full_path = self.download_dir / self.filename

    @property
    def is_missing(self):
        return not self.full_path.exists()

    async def download(self, http, vprint, semaphore, progressbar):
        async with semaphore:
            vprint(f"Getting episode: {self.url}")
            async with http.get(self.url) as response:
                await self._save_atomic(response, vprint)
            vprint(f"Finished downloading: {self.filename}", fg="green")
            progressbar.update(1)

    async def _save_atomic(self, response, vprint):
        partial_filename = self.full_path.with_suffix(".partial")
        with partial_filename.open("wb") as fp:
            vprint(f"Writing file: {self.filename}.partial")
            async for chunk, _ in response.content.iter_chunks():
                fp.write(chunk)
        partial_filename.rename(self.full_path)


async def download_rss(http, rss_url: str):
    click.echo(f"Downloading RSS feed: {rss_url} ...")
    async with http.get(rss_url) as res:
        return etree.XML(await res.read())


def ensure_download_dir(download_dir: Path):
    click.echo(f"Download directory: {download_dir.resolve()}")
    download_dir.mkdir(parents=True, exist_ok=True)


def get_all_rss_items(rss_root: etree.Element, rss_parser: BaseItem):
    all_items = (rss_parser(item) for item in rss_root.xpath("//item"))
    return sorted(all_items, key=attrgetter("filename"))


def filter_rss_items(all_rss_items, episode_params, last_n):
    search_message = "Searching episodes: " + ", ".join(str(e) for e in episode_params)
    if last_n != 0:
        search_message += " and/or " if episode_params else ""
        search_message += f"last {last_n}."
    click.echo(search_message)

    # We can't make this function a generator, need to return a list, so
    # the above output would print before we return from this function
    filtered_items = []
    episode_params_left = set(episode_params)
    last_index = len(all_rss_items) - last_n

    for n, item in enumerate(all_rss_items):
        if item.episode in episode_params_left:
            episode_params_left.remove(item.episode)
            filtered_items.append(item)

        elif item.filename in episode_params_left:
            episode_params_left.remove(item.filename)
            filtered_items.append(item)

        elif item.title in episode_params_left:
            episode_params_left.remove(item.title)
            filtered_items.append(item)

        elif last_index <= n:
            filtered_items.append(item)

    return filtered_items, sorted(episode_params_left)


def make_episodes(download_dir, rss_items):
    return (Episode(item, download_dir) for item in rss_items)


def find_missing(episodes, vprint):
    click.echo("Searching missing episodes...")
    rv = []

    for ep in episodes:
        if not ep.is_missing:
            continue

        vprint(f"Found missing episode: {ep.filename}")
        if ep.number is None:
            click.secho(
                "WARNING: Episode has no numeric episode number. The filename for "
                f'episode "{ep.title}" will not have a numeric episode prefix.',
                fg="yellow",
                err=True,
            )

        rv.append(ep)

    return rv


async def download_episodes(http, episodes, max_threads, vprint, progressbar):
    click.echo(f"Downloading episodes...")

    semaphore = asyncio.Semaphore(max_threads)

    with progressbar:
        progressbar.update(0)
        coros = [ep.download(http, vprint, semaphore, progressbar) for ep in episodes]
        await asyncio.wait(coros)
