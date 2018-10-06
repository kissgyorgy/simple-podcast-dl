import pytest
from podcast_dl.utils import grouper


@pytest.mark.parametrize(
    "group, n, result",
    (
        ("ABCDEF", 0, []),
        ("", 2, []),
        ("", 0, []),
        ([], 0, []),
        ("ABCDEF", 2, [("A", "B"), ("C", "D"), ("E", "F")]),
        ("ABCDE", 2, [("A", "B"), ("C", "D"), ("E", None)]),
        ("A", 2, [("A", None)]),
    ),
)
def test_grouper(group, n, result):
    assert list(grouper(group, n)) == result
