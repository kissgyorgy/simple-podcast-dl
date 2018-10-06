"""
URL to filename parsers. They can be generic or entirely site-specific, based on
what type of file names the RSS contains.
"""
import os
import re
import sys


def normalize(filename):
    # These are coming from an URL, so they are already sanitized, but there are
    # podcasts (e.g. Podcast.__init__) which mix and match underscores and dashes
    filename = filename.replace("_", "-")
    return re.sub(r"-+", "-", filename)


def simple(url):
    episode, filename = url.split("/")[-2:]
    episode = int(episode)
    return f"{episode:04}-{normalize(filename)}"


def fallback(url):
    episode, filename = url.split("/")[-2:]
    normalized_filename = normalize(filename)
    try:
        episode = int(episode)
        return f"{episode:04}-{normalized_filename}"
    except ValueError:
        print(
            "WARNING: Invalid episode number in filename. The episode "
            f'"{normalized_filename}" will not have a numeric episode number prefix.',
            file=sys.stderr,
            flush=True,
        )
        return normalized_filename


def podcastinit(url):
    filename = url.split("/")[-1]
    normalized_filename = normalize(filename)
    # This should be the only episode without Episode number in the filename
    if normalized_filename == "introductory-episode.mp3":
        return "0000-introductory-episode.mp3"
    cut_episode = len("Episode-")
    no_episode = normalized_filename[cut_episode:]
    first_dash = no_episode.find("-")
    episode = no_episode[:first_dash]
    episode = int(episode)
    final_filename = no_episode[first_dash + 1 :]
    return f"{episode:04}-{final_filename}"


def changelog(url):
    """Fallback and cut episode number from the end."""
    filename = fallback(url)
    last_dash = filename.rfind("-")
    _, ext = os.path.splitext(filename)
    return filename[:last_dash] + ext
