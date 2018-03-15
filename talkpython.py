#!/usr/bin/env python3.6
import os
import sys
import argparse
from pathlib import Path
import requests
from lxml import etree


RSS_URL = 'https://talkpython.fm/episodes/rss'


class Episode:
    def __init__(self, enclosure):
        self.url = enclosure.get('url')
        self.length = enclosure.get('length')
        episode_number, original_filename = self.url.split('/')[-2:]
        self.filename = f'{episode_number}-{original_filename}'

    def download(self, download_path: Path):
        print(f'Getting episode {self.url}', flush=True)
        with requests.get(self.url, stream=True) as r:
            full_path = download_path / self.filename
            with full_path.open('wb') as fp:
                print(f'Writing file {self.filename}', flush=True)
                for chunk in r.iter_content(chunk_size=None):
                    fp.write(chunk)


def download_rss():
    print('Downloading RSS...', flush=True)
    res = requests.get(RSS_URL)
    return etree.XML(res.content)


def ensure_download_dir(download_dir: str):
    print('Download directory:', download_dir, flush=True)
    download_path = Path(download_dir)
    download_path.mkdir(parents=True, exist_ok=True)
    return download_path


def make_episodes(xml_root):
    enclosures = xml_root.xpath('//enclosure')
    return (Episode(enc) for enc in enclosures)


def find_missing(download_path: Path, episodes):
    for episode in episodes:
        episode_path = download_path / episode.filename
        try:
            existing_file_size = episode_path.stat().st_size
        except FileNotFoundError:
            print('Found missing episode:', episode.filename, flush=True)
            yield episode
        else:
            # it might be partially downloaded, re-encoded or
            # anything wrong with the already downloaded episode
            if existing_file_size != episode.length:
                print('Episode size mismatch:', episode.filename, flush=True)
                yield episode


def download_episodes(download_path: Path, episodes):
    for ep in episodes:
        ep.download(download_path)


def parse_args():
    parser = argparse.ArgumentParser(description='Download Talk Python To Me podcast episodes to the given dir')
    parser.add_argument('--download-dir', default=os.environ.get('DOWNLOAD_DIR', 'episodes'))
    return parser.parse_args()


def main():
    args = parse_args()
    download_path = ensure_download_dir(args.download_dir)
    xml_root = download_rss()
    episodes = make_episodes(xml_root)
    missing_episodes = find_missing(download_path, episodes)
    download_episodes(download_path, missing_episodes)
    return 0


if __name__ == '__main__':
    sys.exit(main())
