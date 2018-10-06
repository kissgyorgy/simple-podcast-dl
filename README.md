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
- Podcast.\_\_init__ (https://www.podcastinit.com/)

## Installation

You need at least Python 3.6, then you can simply run:

```bash
$ pip3 install simple-podcast-dl
```

## Usage

```plain
Usage: podcast-dl [OPTIONS] PODCAST

  Download podcast episodes to the given directory

  URL or domain or short name for the PODCAST argument can be specified,
  e.g. pythonbytes.fm or talkpython or https://talkpython.fm

Options:
  -d, --download-dir PATH         Where to save downloaded episodes. Can be
                                  specified by the DOWNLOAD_DIR environment
                                  variable.  [default: ./episodes/]
  -t, --max-threads INTEGER RANGE
                                  Number of threads to start for the download.
                                  Can be specified with the MAX_THREADS
                                  environment variable.  [default: 10]
  -l, --list-podcasts             List of supported podcasts, ordered by name.
  -V, --version                   Show the version and exit.
  -h, --help                      Show this message and exit.
```


## Development

The project have a `Pipfile`, so you can simply install everything needed for development with a single command:

```bash
$ pip install pipenv
$ pipenv install --dev
```

You should format your code with black (it's included in the development requirements):

```bash
$ pipenv run black .
```

You can run the tests with:
```bash
$ pipenv run pytest
```
