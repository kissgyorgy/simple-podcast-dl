from lxml import etree
from podcast_dl.rss_parsers import BaseItem, ChangelogItem, TalkPythonItem
import pytest


ITUNES_XMLNS = 'xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"'


@pytest.fixture(scope="module")
def changelog_item():
    return etree.XML(
        f"""
        <item {ITUNES_XMLNS}>
          <title>315: Join the federation?! Mastodon awaits...</title>
          <enclosure url="https://cdn.changelog.com/uploads/podcast/315/the-changelog-315.mp3" length="121018247" type="audio/mpeg" />
        </item>
        """
    )


@pytest.fixture(scope="module")
def podcastinit_item():
    return etree.XML(
        f"""
        <item {ITUNES_XMLNS}>
          <title>Continuous Delivery For Complex Systems Using Zuul with Monty Taylor</title>
          <enclosure url="https://www.podcastinit.com/podlove/file/761/s/feed/c/mp3/Episode-172-Zuul.mp3" length="75198559" type="audio/mpeg"/>
          <itunes:episode>172</itunes:episode>
        </item>
        """
    )


@pytest.fixture(scope="module")
def talkpython_item():
    return etree.XML(
        f"""
        <item {ITUNES_XMLNS}>
          <title>#178 Coverage.py</title>
          <enclosure url="https://talkpython.fm/episodes/download/178/coverage.py.mp3"
                     length="43380149"
                     type="audio/mpeg"/>
          <itunes:episode>178</itunes:episode>
        </item>
        """
    )


class TestBaseItem:
    def test_changelog(self, changelog_item):
        rss_item = BaseItem(changelog_item)
        assert rss_item.episode is None
        assert rss_item.title == "315: Join the federation?! Mastodon awaits..."
        assert rss_item.file_ext == ".mp3"
        # This is NOT the episode number (it doesn't know about that,
        # so it's just the original slugify-ed title)
        assert rss_item.filename == "315-Join-the-federation-Mastodon-awaits.mp3"

    def test_podcastinit(self, podcastinit_item):
        rss_item = BaseItem(podcastinit_item)
        assert rss_item.episode == "0172"
        assert (
            rss_item.title
            == "Continuous Delivery For Complex Systems Using Zuul with Monty Taylor"
        )
        assert rss_item.file_ext == ".mp3"
        assert (
            rss_item.filename
            == "0172-Continuous-Delivery-For-Complex-Systems-Using-Zuul-with-Monty-Taylor.mp3"
        )

    def test_talkpython(self, talkpython_item):
        rss_item = BaseItem(talkpython_item)
        assert rss_item.episode == "0178"
        assert rss_item.title == "#178 Coverage.py"
        assert rss_item.file_ext == ".mp3"
        # This is NOT talkpython specific item
        assert rss_item.filename == "0178-178-Coverage-py.mp3"


def test_changelog(changelog_item):
    rss_item = ChangelogItem(changelog_item)
    assert rss_item.episode == "0315"
    assert rss_item.title == "Join the federation?! Mastodon awaits..."
    assert rss_item.file_ext == ".mp3"
    assert rss_item.filename == "0315-Join-the-federation-Mastodon-awaits.mp3"


def test_talkpython(talkpython_item):
    rss_item = TalkPythonItem(talkpython_item)
    assert rss_item.episode == "0178"
    assert rss_item.title == "Coverage.py"
    assert rss_item.file_ext == ".mp3"
    assert rss_item.filename == "0178-Coverage-py.mp3"
