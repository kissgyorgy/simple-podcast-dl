"""
List of podcasts and their filename parser types.
"""
from .filename_parsers import simple, fallback


PODCAST_MAP = {
    "talkpython": ("https://talkpython.fm/episodes/rss", simple),
    "pythonbytes": ("https://pythonbytes.fm/episodes/rss", simple),
    "changelog": ("https://changelog.com/podcast/feed", fallback),
}


def parse_site(site: str):
    if site.startswith("http"):
        parseres = urlparse(site)
        site = parseres.netloc

    if "." in site:
        try:
            short_name = site.split(".")[-2]
        except IndexError:
            raise InvalidSite
    else:
        short_name = site

    try:
        site_url = PODCAST_MAP[short_name][0]
    except KeyError:
        raise InvalidSite

    return short_name, site_url
