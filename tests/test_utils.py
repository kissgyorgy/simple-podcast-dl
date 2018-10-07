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
        ("ABCDE", 2, [("A", "B"), ("C", "D"), ("E",)]),
        ("A", 2, [("A",)]),
        ("A", 1, [("A",)]),
        ("ABC", 10, [("A", "B", "C")]),
    ),
)
def test_grouper(group, n, result):
    assert [tuple(g) for g in grouper(group, n)] == result
