"""
URL to filename parsers. They can be generic or entirely site-specific, based on
what type of file names the RSS contains.
"""
import os
import re
import sys
from lxml import etree
from slugify import slugify


class RSSItem:
    NSMAP = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}

    def __init__(self, item: etree.Element):
        enclosure = item.xpath("enclosure")[0]
        url = enclosure.get("url")
        self.title = item.xpath("title")[0].text
        self.episode = self._parse_episode(item)
        filename = url.split("/")[-1]
        _, self.file_ext = os.path.splitext(filename)

    def _parse_episode(self, item):
        try:
            episode_elem = item.xpath("itunes:episode", namespaces=self.NSMAP)[0]
        except IndexError:
            # XML has no <itunes:episode> element
            return None

        return episode_elem.text


def _slug(string):
    # There are podcasts (e.g. Podcast.__init__) which mix and match underscores and
    # dashes in filenames, but slugify takes care of those also
    return slugify(string, lowercase=False)


def talkpython(item: RSSItem):
    # Example title: "#95 Unleash the py-spy!"
    episode, title = item.title.split(" ", 1)
    episode = int(episode.lstrip("#"))
    return f"{episode:04}-{_slug(title)}{item.file_ext}"


def podcastinit(item: RSSItem):
    episode = int(item.episode)
    return f"{episode:04}-{_slug(item.title)}{item.file_ext}"


def changelog(item: RSSItem):
    try:
        episode, title = item.title.split(": ", 1)
    except ValueError:
        print(
            "WARNING: Episode has no numeric episode number. The filename for episode "
            f'"{item.title}" will not have a numeric episode number prefix.',
            file=sys.stderr,
            flush=True,
        )
        # The split failed, no episode number in the title
        return f"{_slug(item.title)}{item.file_ext}"
    else:
        episode = int(episode)
    return f"{episode:04}-{_slug(title)}{item.file_ext}"
