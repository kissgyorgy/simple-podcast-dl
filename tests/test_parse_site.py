from podcast_dl.podcast_dl import parse_site, InvalidSite
import pytest


def test_valid_short_sites():
    for short_name in ("talkpython", "pythonbytes"):
        assert parse_site(short_name) != (None, None)


def test_valid_site_urls():
    valid_urls = [
        "http://talkpython.fm",
        "https://talkpython.fm",
        "http://pythonbytes.fm",
        "https://pythonbytes.fm",
    ]
    for site_url in valid_urls:
        assert parse_site(site_url) != (None, None)


def test_valid_domains():
    for site_domain in ("pythonbytes.fm", "talkpython.fm"):
        assert parse_site(site_domain) != (None, None)


def test_invalid_site():
    with pytest.raises(InvalidSite):
        parse_site("not_supported")
