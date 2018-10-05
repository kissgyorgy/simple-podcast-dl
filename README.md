# Simple podcast downloader (podcatcher)

The simplest podcast downloader with no configuration, no tagging, no nothing.  
It simply downloads missing episodes from supported podcasts to a directory.  
*That's it.*

You don't even have to know the URL of the RSS, you can give it a website URL,  
a domain name, or simply the podcast name, it will find out which podcast you want to download.  

It doesn't have a complicated UI or fancy features, it's just a command line application.  
The download folder and the number of threads can be customized.

I use it in a Jenkins job to synchronize all the episodes to [Nextcloud](https://nextcloud.com/),  
so it will be synced to my phone and I can listen the episodes without internet connection.


## Supported podcasts

- Talk Python To Me (https://talkpython.fm/)
- Python Bytes (https://pythonbytes.fm/)
- The Changelog (https://changelog.com/podcast)

## Usage

```plain
usage: podcast-dl [-h] [-d DOWNLOAD_DIR] [-t MAX_THREADS] podcast

Download podcast episodes to the given directory

positional arguments:
  podcast               URL or domain or short name for the podcast, e.g.
                        pythonbytes.fm or talkpython or https://talkpython.fm

optional arguments:
  -h, --help            show this help message and exit
  -d DOWNLOAD_DIR, --download-dir DOWNLOAD_DIR
  -t MAX_THREADS, --max-threads MAX_THREADS
```
