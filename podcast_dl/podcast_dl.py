import asyncio
from pathlib import Path
from operator import attrgetter
import click
import httpx
from lxml import etree
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

    async def download(self, http: httpx.AsyncClient, vprint):
        vprint(f"Getting episode: {self.url}")
        async with http.stream("GET", self.url) as response:
            await self._save_atomic(response, vprint)
        vprint(f"Finished downloading: {self.filename}", fg="green")

    async def _save_atomic(self, response, vprint):
        partial_filename = self.full_path.with_suffix(".partial")
        with partial_filename.open("wb") as fp:
            vprint(f"Writing file: {self.filename}.partial")
            async for chunk in response.aiter_bytes():
                fp.write(chunk)
        partial_filename.rename(self.full_path)


async def download_rss(http: httpx.AsyncClient, rss_url: str):
    click.echo(f"Downloading RSS feed: {rss_url} ...")
    res = await http.get(rss_url)
    return etree.XML(res.content)


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
            warning_message = (
                "WARNING: Episode has no numeric episode number. The filename for "
                f'episode "{ep.title}" will not have a numeric episode prefix.'
            )
            click.secho(warning_message, fg="yellow", err=True)

        rv.append(ep)

    return rv


async def download_episodes(http, episodes, max_threads, vprint, progressbar):
    click.echo(f"Downloading episodes...")

    semaphore = asyncio.Semaphore(max_threads)

    async def with_progressbar(coro):
        async with semaphore:
            await coro
            progressbar.update(1)

    with progressbar:
        progressbar.update(0)
        coros = [with_progressbar(ep.download(http, vprint)) for ep in episodes]
        await asyncio.wait(coros)
