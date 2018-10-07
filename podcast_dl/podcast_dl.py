import sys
from pathlib import Path
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, wait
import requests
from lxml import etree
from .podcasts import Podcast
from .filename_parsers import RSSItem
from .utils import grouper


class Episode:
    def __init__(self, item: RSSItem, podcast: Podcast, download_dir: Path):
        self.url = item.url
        self.filename = podcast.filename_parser(item)
        self.download_dir = download_dir
        self.full_path = self.download_dir / self.filename

    @property
    def is_missing(self):
        return not self.full_path.exists()

    def download(self):
        print(f"Getting episode: {self.url}", flush=True)
        with requests.get(self.url, stream=True) as response:
            self._save_atomic(response)
        print(f"Finished downloading: {self.full_path}")

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


def get_rss_items(rss_root: etree.Element, episode_numbers=None):
    all_rss_items = (RSSItem(item) for item in rss_root.xpath("//item"))
    if episode_numbers is None:
        return all_rss_items
    else:
        print("Searching episodes:", ", ".join(episode_numbers))
        return (item for item in all_rss_items if item.episode in episode_numbers)


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
