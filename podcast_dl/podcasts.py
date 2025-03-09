"""
List of podcasts and their filename parser types.
"""

import attrs

from . import rss_parsers as rssp


@attrs.define(slots=True, frozen=True)
class Podcast:
    name: str
    title: str
    url: str
    rss: str
    rss_parser: type[rssp.BaseItem]


PODCASTS = [
    Podcast(
        name="talkpython",
        title="Talk Python To Me",
        url="https://talkpython.fm",
        rss="https://talkpython.fm/episodes/rss",
        rss_parser=rssp.TalkPythonItem,
    ),
    Podcast(
        name="pythonbytes",
        title="Python Bytes",
        url="https://pythonbytes.fm/",
        rss="https://pythonbytes.fm/episodes/rss",
        rss_parser=rssp.TalkPythonItem,
    ),
    Podcast(
        name="changelog",
        title="The Changelog",
        url="https://changelog.com/podcast",
        rss="https://changelog.com/podcast/feed",
        rss_parser=rssp.ChangelogItem,
    ),
    Podcast(
        name="podcastinit",
        title="Podcast.__init__",
        url="https://www.podcastinit.com/",
        rss="https://www.podcastinit.com/feed/mp3/",
        rss_parser=rssp.BaseItem,
    ),
    Podcast(
        name="indiehackers",
        title="Indie Hackers",
        url="https://www.indiehackers.com/podcast",
        rss="http://feeds.backtracks.fm/feeds/indiehackers/indiehackers/feed.xml",
        rss_parser=rssp.IndieHackersItem,
    ),
    Podcast(
        name="realpython",
        title="Real Python",
        url="https://realpython.com/podcasts/rpp/",
        rss="https://realpython.com/podcasts/rpp/feed",
        rss_parser=rssp.BaseItem,
    ),
    Podcast(
        name="kubernetespodcast",
        title="Kubernetes Podcast",
        url="https://kubernetespodcast.com/",
        rss="https://kubernetespodcast.com/feeds/audio.xml",
        rss_parser=rssp.BaseItem,
    ),
    Podcast(
        name="corecursive",
        title="CoRecursive - The Stories Behind The Code",
        url="https://corecursive.com/",
        rss="https://corecursive.libsyn.com/feed",
        rss_parser=rssp.CoRecursiveItem,
    ),
]

PODCAST_MAP = {p.name: p for p in PODCASTS}
