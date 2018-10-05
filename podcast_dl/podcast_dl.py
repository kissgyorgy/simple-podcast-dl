from pathlib import Path
from urllib.parse import urlparse
import concurrent.futures
import requests
from lxml import etree
from .podcasts import PODCAST_MAP


class Episode:
    def __init__(self, enclosure, filename_parser: callable, download_dir: Path):
        self.url = enclosure.get("url")
        self.length = int(enclosure.get("length"))
        self.filename = filename_parser(self.url)
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


def download_rss(site_url: str):
    print(f"Downloading RSS feed: {site_url} ...", flush=True)
    res = requests.get(site_url)
    return etree.XML(res.content)


def ensure_download_dir(download_dir: Path):
    print("Download directory:", download_dir.resolve(), flush=True)
    download_dir.mkdir(parents=True, exist_ok=True)


def make_episodes(xml_root, filename_parser: callable, download_dir: Path):
    enclosures = xml_root.xpath("//enclosure")
    return (Episode(enc, filename_parser, download_dir) for enc in enclosures)


def find_missing(all_episodes):
    print("Searching missing episodes...", flush=True)

    def printret(episode):
        print("Found missing episode:", episode.filename, flush=True)
        return episode

    return [printret(e) for e in all_episodes if e.is_missing]


def download_episodes(episodes, max_threads: int):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(ep.download) for ep in episodes]
        concurrent.futures.wait(futures)
