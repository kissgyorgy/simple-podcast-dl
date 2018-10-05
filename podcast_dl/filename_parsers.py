"""
URL to filename parsers. They can be generic or entirely site-specific, based on
what type of file names the RSS contains.
"""

import sys


def simple(url):
    episode, original_filename = url.split("/")[-2:]
    episode = int(episode)
    return f"{episode:04}-{original_filename}"


def fallback(url):
    episode, original_filename = url.split("/")[-2:]
    try:
        episode = int(episode)
        return f"{episode:04}-{original_filename}"
    except ValueError:
        print(
            "WARNING: Invalid episode number in filename. The episode "
            f'"{original_filename}" will not have a numeric episode number prefix.',
            file=sys.stderr,
            flush=True,
        )
        return original_filename
