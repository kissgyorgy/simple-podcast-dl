from podcast_dl.site_parser import parse_site, InvalidSite
import pytest


def test_valid_short_sites():
    for short_name in ("talkpython", "pythonbytes"):
        assert parse_site(short_name) != (None, None)


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
        ("talkpython.fm", "talkpython"),
        ("www.talkpython.fm", "talkpython"),
        ("https://www.podcastinit.com/feed/mp3/", "podcastinit"),
        ("www.podcastinit.com/feed/mp3/", "podcastinit"),
    ),
)
def test_parse_site(site, name):
    assert parse_site(site)[0] == name


def test_parse_site_episode_url_still_returns_site_name():
    url = "https://www.podcastinit.com/managing-application-secrets-with-brian-kelly-episode-181/"
    assert parse_site(url)[0] == "podcastinit"


def test_invalid_sites():
    with pytest.raises(InvalidSite):
        parse_site("not_supported")
