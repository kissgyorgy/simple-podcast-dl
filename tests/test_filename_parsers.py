import pytest
from podcast_dl import filename_parsers as fipa


@pytest.mark.parametrize(
    "url, expected",
    (
        (
            "https://talkpython.fm/episodes/download/0/introducing-the-show.mp3",
            "0000-introducing-the-show.mp3",
        ),
        (
            "https://talkpython.fm/episodes/download/180/what-s-new-in-python-3.7-and-beyond.mp3",
            "0180-what-s-new-in-python-3.7-and-beyond.mp3",
        ),
        (
            "https://pythonbytes.fm/episodes/download/95/unleash-the-py-spy.mp3",
            "0095-unleash-the-py-spy.mp3",
        ),
        (
            "https://pythonbytes.fm/episodes/download/3/python-3.6-is-coming-and-it-s-awesome-plus-superior-text-processing-with-pynini.mp3",
            "0003-python-3.6-is-coming-and-it-s-awesome-plus-superior-text-processing-with-pynini.mp3",
        ),
    ),
    ids=["ep0", "3-digits", "2-digits", "1-digit"],
)
def test_simple(url, expected):
    assert fipa.simple(url) == expected


@pytest.mark.parametrize(
    "url, expected",
    (
        (
            "https://cdn.changelog.com/uploads/podcast/1/the-changelog-1.mp3",
            "0001-the-changelog-1.mp3",
        ),
        (
            "https://cdn.changelog.com/uploads/podcast/afk-jeff-bonus/the-changelog-afk-jeff-bonus.mp3",
            "the-changelog-afk-jeff-bonus.mp3",
        ),
        (
            "https://cdn.changelog.com/uploads/podcast/310/the-changelog-310.mp3",
            "0310-the-changelog-310.mp3",
        ),
        (
            "https://cdn.changelog.com/uploads/podcast/bonus-153/the-changelog-bonus-153.mp3",
            "the-changelog-bonus-153.mp3",
        ),
    ),
    ids=["1", "no-number", "with-number", "no-number"],
)
def test_fallback(url, expected):
    assert fipa.fallback(url) == expected
