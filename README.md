# Talk Python To Me Podcast downloader script

This script is able to download missing episodes from the [Talk Python website](https://talkpython.fm/) automatically. It check if the file exists or the file size is different. It checks every episodes [from the RSS feed](https://talkpython.fm/episodes/rss).
The download folder and the number of threads can be customized.

I use it in a Jenkins job to synchronize all the episodes to [Nextcloud](https://nextcloud.com/), so it will be synced to my phone and I can listen the episodes without internet connection.


## Usage:
```
usage: talkpython.py [-h] [--download-dir DOWNLOAD_DIR]
                     [--max-threads MAX_THREADS]

Download Talk Python To Me podcast episodes to the given dir

optional arguments:
  -h, --help            show this help message and exit
  --download-dir DOWNLOAD_DIR
  --max-threads MAX_THREADS
```
