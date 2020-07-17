"""
List of podcasts and their filename parser types.
"""
from .rss_parsers import BaseItem, TalkPythonItem, ChangelogItem, IndieHackersItem
import attr


@attr.s(slots=True, frozen=True)
class Podcast:
    name = attr.ib(type=str)
    title = attr.ib(type=str)
    url = attr.ib(type=str)
    rss = attr.ib(type=str)
    rss_parser = attr.ib(type=BaseItem)


PODCASTS = [
    Podcast(
        name="talkpython",
        title="Talk Python To Me",
        url="https://talkpython.fm",
        rss="https://talkpython.fm/episodes/rss",
        rss_parser=TalkPythonItem,
    ),
    Podcast(
        name="pythonbytes",
        title="Python Bytes",
        url="https://pythonbytes.fm/",
        rss="https://pythonbytes.fm/episodes/rss",
        rss_parser=TalkPythonItem,
    ),
    Podcast(
        name="changelog",
        title="The Changelog",
        url="https://changelog.com/podcast",
        rss="https://changelog.com/podcast/feed",
        rss_parser=ChangelogItem,
    ),
    Podcast(
        name="podcastinit",
        title="Podcast.__init__",
        url="https://www.podcastinit.com/",
        rss="https://www.podcastinit.com/feed/mp3/",
        rss_parser=BaseItem,
    ),
    Podcast(
        name="indiehackers",
        title="Indie Hackers",
        url="https://www.indiehackers.com/podcast",
        rss="http://feeds.backtracks.fm/feeds/indiehackers/indiehackers/feed.xml",
        rss_parser=IndieHackersItem,
    ),
    Podcast(
        name="realpython",
        title="Real Python",
        url="https://realpython.com/podcasts/rpp/",
        rss="https://realpython.com/podcasts/rpp/feed",
        rss_parser=BaseItem,
    ),
]

PODCAST_MAP = {p.name: p for p in PODCASTS}
