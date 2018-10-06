from itertools import zip_longest


def grouper(iterable, n):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3) --> A,B,C D,E,F G,None,None"
    args = [iter(iterable)] * n
    return zip_longest(*args)
