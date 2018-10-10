import sys
from typing import List, Tuple
from pathlib import Path
from urllib.parse import urlparse
from operator import attrgetter
from concurrent.futures import ThreadPoolExecutor, wait
import requests
from lxml import etree
from .podcasts import Podcast
from .rss_parsers import BaseItem
from .utils import grouper


class Episode:
    def __init__(self, item: BaseItem, podcast: Podcast, download_dir: Path):
        self.url = item.url
        self.filename = item.filename
        self.download_dir = download_dir
        self.full_path = self.download_dir / self.filename

    @property
    def is_missing(self):
        return not self.full_path.exists()

    def download(self):
        print(f"Getting episode: {self.url}", flush=True)
        with requests.get(self.url, stream=True) as response:
            self._save_atomic(response)
        print(f"Finished downloading: {self.filename}")

    def _save_atomic(self, response):
        partial_filename = self.full_path.with_suffix(".partial")
        with partial_filename.open("wb") as fp:
            print(f"Writing file: {self.filename}.partial", flush=True)
            for chunk in response.iter_content(chunk_size=None):
                fp.write(chunk)
        partial_filename.rename(self.full_path)


def download_rss(rss_url: str):
    print(f"Downloading RSS feed: {rss_url} ...", flush=True)
    res = requests.get(rss_url)
    return etree.XML(res.content)


def ensure_download_dir(download_dir: Path):
    print("Download directory:", download_dir.resolve(), flush=True)
    download_dir.mkdir(parents=True, exist_ok=True)


def get_all_rss_items(rss_root: etree.Element, rss_parser: BaseItem):
    all_items = (rss_parser(item) for item in rss_root.xpath("//item"))
    return sorted(all_items, key=attrgetter("filename"))


def filter_rss_items(
    all_rss_items: List[BaseItem], episode_numbers: Tuple[List[str], int]
):
    episode_strs, last_n = episode_numbers
    last_index = len(all_rss_items) - last_n

    search_message = "Searching episodes: " + ", ".join(episode_strs)
    if last_n != 0:
        if episode_strs:
            search_message += " and/or "
        search_message += f"last {last_n}."
    print(search_message, flush=True)

    # We can't make this function a generator, need to return a list, so
    # the above output would print before we return from this function
    rv = []

    for n, item in enumerate(all_rss_items):
        if (
            (item.episode in episode_strs)
            or (item.filename.upper() in episode_strs)
            or (item.title.upper() in episode_strs)
            or (last_index <= n)
        ):
            rv.append(item)

    return rv


def find_missing(episodes):
    print("Searching missing episodes...", flush=True)

    def printret(episode):
        print("Found missing episode:", episode.filename, flush=True)
        return episode

    return [printret(e) for e in episodes if e.is_missing]


def download_episodes(episodes, max_threads):
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for episode_group in grouper(episodes, max_threads):
            future_group = [executor.submit(ep.download) for ep in episode_group]
            wait(future_group)
