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


@pytest.mark.parametrize(
    "url, expected",
    (
        (
            "https://www.podcastinit.com/podlove/file/79/s/feed/c/mp3/introductory_episode.mp3",
            "0000-introductory_episode.mp3",
        ),
        (
            "https://www.podcastinit.com/podlove/file/78/s/feed/c/mp3/Episode_1_-_Thomas_Hatch.mp3",
            "0001-Episode_1_-_Thomas_Hatch.mp3",
        ),
        (
            "https://www.podcastinit.com/podlove/file/69/s/feed/c/mp3/Episode_10_-_Brian_Granger_and_Fernando_Perez_of_the_IPython_Project.mp3",
            "0010-Episode_10_-_Brian_Granger_and_Fernando_Perez_of_the_IPython_Project.mp3",
        ),
        (
            "https://www.podcastinit.com/podlove/file/84/s/feed/c/mp3/Episode-80-Sean-Gillies.mp3",
            "0080-Episode-80-Sean-Gillies.mp3",
        ),
        (
            "https://www.podcastinit.com/podlove/file/454/s/feed/c/mp3/Episode-114-Factory-Automation-with-Jonas-Neuberg.mp3",
            "0114-Episode-114-Factory-Automation-with-Jonas-Neuberg.mp3",
        ),
    ),
    ids=[
        "intro",
        "underscore-1-digit",
        "underscore-2-digits",
        "dash-2-digits",
        "dash-3-digits",
    ],
)
def test_podcastinit(url, expected):
    assert fipa.podcastinit(url) == expected
