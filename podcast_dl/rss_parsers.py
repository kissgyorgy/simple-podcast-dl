"""
URL to filename parsers. They can be generic or entirely site-specific, based on
what type of file names the RSS contains.
"""
import os
import re
import sys
from lxml import etree
from slugify import slugify


def _slug(string):
    # There are podcasts (e.g. Podcast.__init__) which mix and match underscores and
    # dashes in filenames, but slugify takes care of those also
    return slugify(string, lowercase=False)


class BaseItem:
    NSMAP = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}

    def __init__(self, rss_item: etree.Element):
        self._rss_item = rss_item

    @property
    def url(self):
        # will raise a ValueError if not exactly one element found
        enclosure, = self._rss_item.xpath("enclosure")
        return enclosure.get("url")

    @property
    def title(self):
        return self._rss_item.xpath("title")[0].text

    @property
    def episode(self):
        episode_elem = self._rss_item.xpath("itunes:episode", namespaces=self.NSMAP)
        return episode_elem[0].text.zfill(4) if episode_elem else None

    @property
    def file_ext(self):
        enclosure = self._rss_item.xpath("enclosure")[0]
        url = enclosure.get("url")
        filename = url.split("/")[-1]
        return os.path.splitext(filename)[-1]

    @property
    def filename(self):
        if self.episode is not None:
            return f"{self.episode}-{_slug(self.title)}{self.file_ext}"
        return f"{_slug(self.title)}{self.file_ext}"


class TalkPythonItem(BaseItem):
    @property
    def title(self):
        # Example title: "#95 Unleash the py-spy!"
        return super().title.split(" ", 1)[1]

    @property
    def episode(self):
        # Example title: "#95 Unleash the py-spy!"
        episode = super().title.split(" ", 1)[0]
        return episode.lstrip("#").zfill(4)


class ChangelogItem(BaseItem):
    @property
    def title(self):
        super_title = super().title
        try:
            # Example title: "1: Haml, Sass, Compass"
            return super_title.split(": ", 1)[1]
        except IndexError:
            # The split failed, no episode number in the title
            return super_title

    @property
    def episode(self):
        # Example title: "1: Haml, Sass, Compass"
        try:
            episode, _ = super().title.split(": ", 1)
        except ValueError:
            # The split failed, no episode number in the title
            # e.g. "Jeff Robbins is an actual rockstar"
            return None
        else:
            return episode.zfill(4)
