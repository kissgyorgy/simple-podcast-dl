# Talk Python To Me Podcast downloader script

This script is able to download missing episodes from the [Talk Python website](https://talkpython.fm/)
and [Python Bytes website](https://pythonbytes.fm/) automatically. It check if the file exists or the
file size is different. It checks every episodes [from the talkpython.fm RSSfeed](https://talkpython.fm/episodes/rss) and
[from the pythonbytes.fm RSS feed](https://pythonbytes.fm/episodes/rss). The download folder and
the number of threads can be customized.

I use it in a Jenkins job to synchronize all the episodes to [Nextcloud](https://nextcloud.com/),
so it will be synced to my phone and I can listen the episodes without internet connection.


## Usage

```plain
usage: podcast_dl.py [-h] [--download-dir DOWNLOAD_DIR]
                     [--max-threads MAX_THREADS]
                     podcast-site

Download podcast episodes to the given dir

positional arguments:
  podcast-site          URL or domain or short name for the podcast site, e.g.
                        pythonbytes.fm or talkpython or https://talkpython.fm

optional arguments:
  -h, --help            show this help message and exit
  --download-dir DOWNLOAD_DIR
  --max-threads MAX_THREADS
```
