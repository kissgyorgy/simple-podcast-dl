import pytest
from podcast_dl import Episode


@pytest.mark.parametrize(
    "url, expected",
    (
        (
            "https://cdn.changelog.com/uploads/podcast/afk-jeff-bonus/the-changelog-afk-jeff-bonus.mp3",
            "the-changelog-afk-jeff-bonus.mp3",
        ),
        (
            "https://cdn.changelog.com/uploads/podcast/310/the-changelog-310.mp3",
            "0310-the-changelog-310.mp3",
        ),
        (
            "https://talkpython.fm/episodes/download/180/what-s-new-in-python-3.7-and-beyond.mp3",
            "0180-what-s-new-in-python-3.7-and-beyond.mp3",
        ),
    ),
    ids=["no-number", "with-number", "with-number"],
)
def test_episode_number(url, expected):
    filename = Episode._parse_filename(url)
    assert filename == expected
