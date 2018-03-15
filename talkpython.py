#!/usr/bin/env python3.6
import os
import sys
import argparse
from pathlib import Path
import concurrent.futures
import requests
from lxml import etree


RSS_URL = 'https://talkpython.fm/episodes/rss'


class Episode:
    def __init__(self, enclosure):
        self.url = enclosure.get('url')
        self.length = int(enclosure.get('length'))
        self.number, original_filename = self.url.split('/')[-2:]
        self.number = int(self.number)
        self.filename = f'{self.number}-{original_filename}'

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
    download_path = Path(download_dir)
    print('Download directory:', download_path.resolve(), flush=True)
    download_path.mkdir(parents=True, exist_ok=True)
    return download_path


def make_episodes(xml_root):
    enclosures = xml_root.xpath('//enclosure')
    return (Episode(enc) for enc in enclosures)


def find_missing(download_path: Path, episodes):
    rv = []
    for episode in episodes:
        episode_path = download_path / episode.filename
        try:
            existing_file_size = episode_path.stat().st_size
        except FileNotFoundError:
            print('Found missing episode:', episode.filename, flush=True)
            rv.append(episode)
        else:
            # Episode 81 has a wrong file size in the RSS, so we have to explicitly skip it
            if episode.number == 81 and existing_file_size == 60045698:
                continue
            # it might be partially downloaded, re-encoded or
            # anything wrong with the already downloaded episode
            elif existing_file_size != episode.length:
                print('Episode size mismatch:', episode.filename, existing_file_size, '!=', episode.length, flush=True)
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
    parser = argparse.ArgumentParser(description='Download Talk Python To Me podcast episodes to the given dir')
    parser.add_argument('--download-dir', default=os.environ.get('DOWNLOAD_DIR', 'episodes'))
    parser.add_argument('--max-threads', default=os.environ.get('MAX_THREADS', 10))
    return parser.parse_args()


def main():
    args = parse_args()
    download_path = ensure_download_dir(args.download_dir)
    xml_root = download_rss()
    episodes = make_episodes(xml_root)
    missing_episodes = find_missing(download_path, episodes)
    if not missing_episodes:
        print('Every episode is downloaded.')
        return 0
    download_episodes(download_path, missing_episodes, args.max_threads)
    return 0


if __name__ == '__main__':
    sys.exit(main())
