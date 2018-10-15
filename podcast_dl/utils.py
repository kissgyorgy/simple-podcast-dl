import math
from itertools import islice


def grouper(iterator, n):
    if n == 0:
        return []

    it = iter(iterator)

    num_groups = math.ceil(len(iterator) / n)
    for _ in range(num_groups):
        yield islice(it, n)


def noprint(*args, **kwargs):
    """Do nothing with the arguments. Used for suppressing print output."""
