"""
List of podcasts and their filename parser types.
"""
from .filename_parsers import simple, fallback, podcastinit


PODCAST_MAP = {
    "talkpython": ("https://talkpython.fm/episodes/rss", simple),
    "pythonbytes": ("https://pythonbytes.fm/episodes/rss", simple),
    "changelog": ("https://changelog.com/podcast/feed", fallback),
    "podcastinit": ("https://www.podcastinit.com/feed/mp3/", podcastinit),
}
