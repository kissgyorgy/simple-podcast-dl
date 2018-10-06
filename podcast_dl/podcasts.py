"""
List of podcasts and their filename parser types.
"""
from .filename_parsers import simple, changelog, podcastinit
import attr


@attr.s(slots=True, frozen=True)
class Podcast:
    name = attr.ib(type=str)
    title = attr.ib(type=str)
    url = attr.ib(type=str)
    rss = attr.ib(type=str)
    filename_parser = attr.ib(type=callable)


PODCASTS = [
    Podcast(
        name="talkpython",
        title="Talk Python To Me",
        url="https://talkpython.fm",
        rss="https://talkpython.fm/episodes/rss",
        filename_parser=simple,
    ),
    Podcast(
        name="pythonbytes",
        title="Python Bytes",
        url="https://pythonbytes.fm/",
        rss="https://pythonbytes.fm/episodes/rss",
        filename_parser=simple,
    ),
    Podcast(
        name="changelog",
        title="The Changelog",
        url="https://changelog.com/podcast",
        rss="https://changelog.com/podcast/feed",
        filename_parser=changelog,
    ),
    Podcast(
        name="podcastinit",
        title="Podcast.__init__",
        url="https://www.podcastinit.com/",
        rss="https://www.podcastinit.com/feed/mp3/",
        filename_parser=podcastinit,
    ),
]

PODCAST_MAP = {p.name: p for p in PODCASTS}

LONGEST_NAME = max(len(p.name) for p in PODCASTS)
LONGEST_TITLE = max(len(p.title) for p in PODCASTS)
