from podcast_dl.site_parser import parse_site, InvalidSite
import pytest


@pytest.mark.parametrize(
    "site,name",
    (
        ("http://talkpython.fm", "talkpython"),
        ("https://talkpython.fm", "talkpython"),
        ("http://pythonbytes.fm", "pythonbytes"),
        ("https://pythonbytes.fm", "pythonbytes"),
        ("https://talkpython.fm/episodes/rss", "talkpython"),
        ("https://changelog.com/podcast/", "changelog"),
        ("talkpython", "talkpython"),
        ("pythonbytes", "pythonbytes"),
        ("talkpython.fm", "talkpython"),
        ("www.talkpython.fm", "talkpython"),
        ("https://www.podcastinit.com/feed/mp3/", "podcastinit"),
        ("www.podcastinit.com/feed/mp3/", "podcastinit"),
    ),
)
def test_parse_site(site, name):
    assert parse_site(site).name == name


def test_parse_site_episode_url_still_returns_site_name():
    url = "https://www.podcastinit.com/managing-application-secrets-with-brian-kelly-episode-181/"
    assert parse_site(url).name == "podcastinit"


def test_invalid_sites():
    with pytest.raises(InvalidSite):
        parse_site("not_supported")
