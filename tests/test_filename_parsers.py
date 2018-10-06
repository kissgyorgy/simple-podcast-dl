import pytest
from lxml.builder import ElementMaker
from podcast_dl import filename_parsers as fipa


# fmt: off
def _make_item(url, title, episode=None):
    episode_ns = "http://www.itunes.com/dtds/podcast-1.0.dtd"
    E = ElementMaker(nsmap={"itunes": episode_ns})
    rss = E.item(
        E.enclosure(url=url, length="1234", type="audio/mpeg"),
        E.title(title)
    )
    if episode is not None:
        rss.append(E("{" + episode_ns + "}episode", str(episode)))
    return fipa.RSSItem(rss)

# fmt: on


@pytest.mark.parametrize(
    "url, title, expected_filename",
    (
        (
            "https://talkpython.fm/episodes/download/0/introducing-the-show.mp3",
            "#0 Introducing the show!",
            "0000-Introducing-the-show.mp3",
        ),
        (
            "https://talkpython.fm/episodes/download/180/what-s-new-in-python-3.7-and-beyond.mp3",
            "#180 What's new in Python 3.7 and beyond",
            "0180-What-s-new-in-Python-3-7-and-beyond.mp3",
        ),
        (
            "https://pythonbytes.fm/episodes/download/95/unleash-the-py-spy.mp3",
            "#95 Unleash the py-spy!",
            "0095-Unleash-the-py-spy.mp3",
        ),
        (
            "https://pythonbytes.fm/episodes/download/3/python-3.6-is-coming-and-it-s-awesome-plus-superior-text-processing-with-pynini.mp3",
            "#3 Python 3.6 is coming, and it's awesome plus superior text processing with Pynini",
            "0003-Python-3-6-is-coming-and-it-s-awesome-plus-superior-text-processing-with-Pynini.mp3",
        ),
    ),
    ids=["ep0", "3-digits", "2-digits", "1-digit"],
)
def test_talkpython(url, title, expected_filename):
    item = _make_item(url, title)
    assert fipa.talkpython(item) == expected_filename


@pytest.mark.parametrize(
    "url, title, episode, expected_filename",
    (
        (
            "https://www.podcastinit.com/podlove/file/79/s/feed/c/mp3/introductory_episode.mp3",
            "Podcast.__init__ - Introduction",
            0,
            "0000-Podcast-init-Introduction.mp3",
        ),
        (
            "https://www.podcastinit.com/podlove/file/78/s/feed/c/mp3/Episode_1_-_Thomas_Hatch.mp3",
            "Thomas Hatch",
            1,
            "0001-Thomas-Hatch.mp3",
        ),
        (
            "https://www.podcastinit.com/podlove/file/69/s/feed/c/mp3/Episode_10_-_Brian_Granger_and_Fernando_Perez_of_the_IPython_Project.mp3",
            "Brian Granger and Fernando Perez of the IPython Project",
            10,
            "0010-Brian-Granger-and-Fernando-Perez-of-the-IPython-Project.mp3",
        ),
        (
            "https://www.podcastinit.com/podlove/file/51/s/feed/c/mp3/Episode_28_-_Kay_Hayen_-_Nuitka.mp3",
            "Kay Hayen on Nuitka",
            28,
            "0028-Kay-Hayen-on-Nuitka.mp3",
        ),
        (
            "https://www.podcastinit.com/podlove/file/50/s/feed/c/mp3/Episode_29__-_Anthony_Scopatz_on_Xonsh.mp3",
            "Anthony Scopatz on Xonsh",
            29,
            "0029-Anthony-Scopatz-on-Xonsh.mp3",
        ),
        (
            "https://www.podcastinit.com/podlove/file/84/s/feed/c/mp3/Episode-80-Sean-Gillies.mp3",
            "Python for GIS with Sean Gillies",
            80,
            "0080-Python-for-GIS-with-Sean-Gillies.mp3",
        ),
        (
            "https://www.podcastinit.com/podlove/file/454/s/feed/c/mp3/Episode-114-Factory-Automation-with-Jonas-Neuberg.mp3",
            "Industrial Automation with Jonas Neuberg",
            114,
            "0114-Industrial-Automation-with-Jonas-Neuberg.mp3",
        ),
        (
            "https://www.podcastinit.com/podlove/file/582/s/feed/c/mp3/Episode-135-Surprise.mp3",
            "Surprise! Recommendation Algorithms with Nicolas Hug",
            135,
            "0135-Surprise-Recommendation-Algorithms-with-Nicolas-Hug.mp3",
        ),
    ),
    ids=[
        "0",
        "first",
        "10",
        "28-underscore-multiple",
        "29-double-underscore-",
        "80-simple",
        "114-dash-only",
        "135-exclamation",
    ],
)
def test_podcastinit(url, title, episode, expected_filename):
    item = _make_item(url, title, episode)
    assert fipa.podcastinit(item) == expected_filename


@pytest.mark.parametrize(
    "url, title, expected_filename",
    (
        (
            "https://cdn.changelog.com/uploads/podcast/1/the-changelog-1.mp3",
            "1: Haml, Sass, Compass",
            "0001-Haml-Sass-Compass.mp3",
        ),
        (
            "https://cdn.changelog.com/uploads/podcast/42/the-changelog-42.mp3",
            "42: Rails 3.1 and SproutCore",
            "0042-Rails-3-1-and-SproutCore.mp3",
        ),
        (
            "https://cdn.changelog.com/uploads/podcast/192/the-changelog-192.mp3",
            "192: Crystal: Fast as C, Slick as Ruby",
            "0192-Crystal-Fast-as-C-Slick-as-Ruby.mp3",
        ),
        (
            "https://cdn.changelog.com/uploads/podcast/317/the-changelog-317.mp3",
            "317: #Hacktoberfest isn’t just about a free shirt",
            "0317-Hacktoberfest-isnt-just-about-a-free-shirt.mp3",
        ),
        (
            "https://cdn.changelog.com/uploads/podcast/afk-jeff-bonus/the-changelog-afk-jeff-bonus.mp3",
            "Jeff Robbins is an actual rockstar",
            "Jeff-Robbins-is-an-actual-rockstar.mp3",
        ),
    ),
    ids=["1-digit", "2-digits", "two-colons", "3-digits", "no-episode"],
)
def test_changelog(url, title, expected_filename):
    item = _make_item(url, title)
    assert fipa.changelog(item) == expected_filename
