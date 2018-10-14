from urllib.parse import urlparse
import click
from .podcasts import Podcast, PODCAST_MAP


class InvalidSite(Exception):
    """Raised when an invalid site is specified."""


def parse_site(site: str):
    if site.startswith("http"):
        site = urlparse(site).netloc

    if "." in site:
        site = _parse_domain(site)

    podcast = _get_podcast(site)
    click.echo(f"Specified podcast: {podcast.name} - {podcast.title} ({podcast.url})")
    return podcast


def _parse_domain(domain):
    try:
        return domain.split(".")[-2]
    except IndexError:
        raise InvalidSite


def _get_podcast(name) -> Podcast:
    try:
        return PODCAST_MAP[name]
    except KeyError:
        raise InvalidSite
