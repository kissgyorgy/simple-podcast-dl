#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path
from urllib.parse import urlparse
import concurrent.futures
import requests
from lxml import etree


SITE_URL_MAP = {
    "talkpython": "https://talkpython.fm/episodes/rss",
    "pythonbytes": "https://pythonbytes.fm/episodes/rss",
}


class InvalidSite(Exception):
    """Raised when an invalid site is specified."""


class Episode:
    def __init__(self, enclosure, download_dir: Path):
        self.url = enclosure.get("url")
        self.length = int(enclosure.get("length"))
        self.number, original_filename = self.url.split("/")[-2:]
        self.number = int(self.number)
        self.download_dir = download_dir
        self.filename = f"{self.number:04}-{original_filename}"
        self.full_path = self.download_dir / self.filename

    @property
    def is_missing(self):
        return not self.full_path.exists()

    def download(self):
        print(f"Getting episode {self.url}", flush=True)
        with requests.get(self.url, stream=True) as response:
            self._save_atomic(response)

    def _save_atomic(self, response):
        partial_filename = self.full_path.with_suffix(".partial")
        with partial_filename.open("wb") as fp:
            print(f"Writing file {self.filename}.partial", flush=True)
            for chunk in response.iter_content(chunk_size=None):
                fp.write(chunk)
        partial_filename.rename(self.full_path)


def parse_site(site: str):
    if site.startswith("http"):
        parseres = urlparse(site)
        site = parseres.netloc

    if "." in site:
        try:
            short_name = site.split(".")[-2]
        except IndexError:
            raise InvalidSite
    else:
        short_name = site

    try:
        site_url = SITE_URL_MAP[short_name]
    except KeyError:
        raise InvalidSite

    return short_name, site_url


def download_rss(site_url: str):
    print("Downloading RSS...", flush=True)
    res = requests.get(site_url)
    return etree.XML(res.content)


def ensure_download_dir(download_dir: Path):
    print("Download directory:", download_dir.resolve(), flush=True)
    download_dir.mkdir(parents=True, exist_ok=True)


def make_episodes(xml_root, download_dir: Path):
    enclosures = xml_root.xpath("//enclosure")
    return (Episode(enc, download_dir) for enc in enclosures)


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


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download podcast episodes to the given directory"
    )
    parser.add_argument(
        "podcast",
        help=(
            "URL or domain or short name for the podcast, "
            "e.g. pythonbytes.fm or talkpython or https://talkpython.fm"
        ),
    )

    parser.add_argument(
        "-d",
        "--download-dir",
        type=Path,
        default=os.environ.get("DOWNLOAD_DIR", "episodes"),
    )

    parser.add_argument(
        "-t", "--max-threads", type=int, default=os.environ.get("MAX_THREADS", 10)
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        podcast, site_url = parse_site(args.podcast)
    except InvalidSite:
        supported_podcasts = tuple(SITE_URL_MAP.keys())
        print(
            f'The given podcast "{podcast}" is not supported or invalid.\n'
            f"Try one of: {supported_podcasts}"
        )
        return 1

    ensure_download_dir(args.download_dir)
    xml_root = download_rss(site_url)
    all_episodes = make_episodes(xml_root, args.download_dir)
    missing_episodes = find_missing(all_episodes)

    if not missing_episodes:
        print("Every episode is downloaded.", flush=True)
        return 0

    print(f"Found a total of {len(missing_episodes)} missing episodes.", flush=True)
    download_episodes(missing_episodes, args.max_threads)
    return 0


if __name__ == "__main__":
    sys.exit(main())
