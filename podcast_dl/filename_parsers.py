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


def podcastinit(url):
    original_filename = url.split("/")[-1]
    # This should be the only episode without Episode number in the filename
    if original_filename == "introductory_episode.mp3":
        return "0000-introductory_episode.mp3"
    # There are filnames which contains underscores in them, but later, they use
    # only dashes, so we normalize to contain only dashes.
    normalized_filename = original_filename.replace("_", "-")
    cut_episode = len("Episode-")
    no_episode = normalized_filename[cut_episode:]
    first_dash = no_episode.find("-")
    episode = no_episode[:first_dash]
    episode = int(episode)
    return f"{episode:04}-{original_filename}"
