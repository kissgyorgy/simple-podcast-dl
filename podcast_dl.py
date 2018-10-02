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
    def __init__(self, enclosure):
        self.url = enclosure.get("url")
        self.length = int(enclosure.get("length"))
        self.number, original_filename = self.url.split("/")[-2:]
        self.number = int(self.number)
        self.filename = f"{self.number:04}-{original_filename}"

    def download(self, download_path: Path):
        print(f"Getting episode {self.url}", flush=True)
        with requests.get(self.url, stream=True) as r:
            full_path = download_path / self.filename
            with full_path.open("wb") as fp:
                print(f"Writing file {self.filename}", flush=True)
                for chunk in r.iter_content(chunk_size=None):
                    fp.write(chunk)


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


def ensure_download_dir(download_dir: str):
    download_path = Path(download_dir)
    print("Download directory:", download_path.resolve(), flush=True)
    download_path.mkdir(parents=True, exist_ok=True)
    return download_path


def make_episodes(xml_root):
    enclosures = xml_root.xpath("//enclosure")
    return (Episode(enc) for enc in enclosures)


def find_missing(short_name, download_path: Path, episodes):
    rv = []
    for episode in episodes:
        episode_path = download_path / episode.filename
        try:
            existing_file_size = episode_path.stat().st_size
        except FileNotFoundError:
            print("Found missing episode:", episode.filename, flush=True)
            rv.append(episode)
        else:
            # Episode 81 has a wrong file size in the RSS, so we have to explicitly skip it
            if (
                short_name == "talkpython"
                and episode.number == 81
                and existing_file_size == 60_045_698
            ):
                continue
            # it might be partially downloaded, re-encoded or
            # anything wrong with the already downloaded episode
            elif existing_file_size != episode.length:
                print(
                    "Episode size mismatch:",
                    episode.filename,
                    existing_file_size,
                    "!=",
                    episode.length,
                    flush=True,
                )
                rv.append(episode)
    return rv


def download_episodes(download_path: Path, episodes, max_threads):
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for ep in episodes:
            future = executor.submit(ep.download, download_path)
            futures.append(future)
        concurrent.futures.wait(futures)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download podcast episodes to the given dir"
    )
    parser.add_argument(
        "podcast_site",
        metavar="podcast-site",
        help=(
            "URL or domain or short name for the podcast site, "
            "e.g. pythonbytes.fm or talkpython or https://talkpython.fm"
        ),
    )

    parser.add_argument(
        "--download-dir", default=os.environ.get("DOWNLOAD_DIR", "episodes")
    )

    parser.add_argument("--max-threads", default=os.environ.get("MAX_THREADS", 10))
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        short_name, site_url = parse_site(args.podcast_site)
    except InvalidSite:
        supported_sites = tuple(SITE_URL_MAP.keys())
        print(
            f'The given podcast site "{short_name}" is not supported or invalid.\n'
            f"Try one of: {supported_sites}"
        )
        return 1

    download_path = ensure_download_dir(args.download_dir)
    xml_root = download_rss(site_url)
    episodes = make_episodes(xml_root)
    missing_episodes = find_missing(short_name, download_path, episodes)

    if not missing_episodes:
        print("Every episode is downloaded.", flush=True)
        return 0

    print(f"Found a total of {len(missing_episodes)} missing episodes.", flush=True)
    download_episodes(download_path, missing_episodes, args.max_threads)
    return 0


if __name__ == "__main__":
    sys.exit(main())
