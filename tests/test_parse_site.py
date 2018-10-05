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
    ),
)
def test_parse_site(site, name):
    assert parse_site(site)[0] == name


def test_invalid_sites():
    with pytest.raises(InvalidSite):
        parse_site("not_supported")
