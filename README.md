# Simple podcast downloader (podcatcher)

The simplest podcast downloader with no configuration, no tagging, no nothing.  
It simply downloads missing episodes from supported podcasts to a directory.  
_That's it._

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
- Podcast.\_\_init\_\_ (https://www.podcastinit.com/)
- Indie Hackers (https://www.indiehackers.com/podcast)
- Real Python (https://realpython.com/podcasts/rpp/)
- Kubernetes Podcast (https://kubernetespodcast.com/)

## Installation

You need at least Python 3.6, then you can simply run:

```
$ pip3 install simple-podcast-dl
```

## Getting started

It is as simple as running the command:

```
$ podcast-dl talkpython.fm
```

And the podcast will be downloaded to the "talkpython.fm" directory.  
You can change the download directory by specifying the `--directory`
(or `-d`) option:

```
$ podcast-dl talkpython.fm -d talkpython-podcast
```

You can list the supported podcast sites with the `--list-podcasts`
(or `-l`) option:

```
$ podcast-dl --list-podcasts
```

You can specify which episodes to download with the `--episodes`
(or `-e`) option:

```
$ podcast-dl --episodes 1,2,3 talkpython
```

You can use the "last" or "last:n" keyword to select the last or last n number
of episodes to download:

```
$ podcast-dl --episodes last:3 talkpython
```

You can list the podcast episodes sorted by episode number with
`--show-episodes` or (`-s`):

```
$ podcast-dl --show-episodes talkpython
```

Or you can even combine it with selecting episodes:

```
$ podcast-dl --show-episodes -e 1-5 talkpython
```

It can show a progress bar with the `--progress` or (`-p`) option:

```
$ podcast-dl -p talkpython
Found a total of 182 missing episodes.
  [##########--------------------------]   28%  00:03:16
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
                                  variable.  [default: name of PODCAST]
  -e, --episodes EPISODELIST      Episodes to download.
  -s, --show-episodes             Show the list of episodes for PODCAST.
  -l, --list-podcasts             List of supported podcasts, ordered by name.
  -p, --progress                  Show progress bar instead of detailed
                                  messages during download.
  -t, --max-threads INTEGER RANGE
                                  The maximum number of simultaneous
                                  downloads. Can be specified with the
                                  MAX_THREADS environment variable.  [default:
                                  10]
  -v, --verbose                   Show detailed informations during download.
  -V, --version                   Show the version and exit.
  -h, --help                      Show this message and exit.
```

## Development

The project have a `, so you can simply install everything needed for development with a single command:

```
$ pip install pipenv
$ poetry install
```

You should format your code with black (it's included in the development requirements):

```
$ poetry run black .
```

You can run the tests with:

```
$ poetry run pytest
```
