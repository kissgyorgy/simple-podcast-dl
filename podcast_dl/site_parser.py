from urllib.parse import urlparse
from .podcasts import PODCAST_MAP


class InvalidSite(Exception):
    """Raised when an invalid site is specified."""


def parse_site(site: str):
    if site.startswith("http"):
        site = urlparse(site).netloc

    if "." in site:
        site = _parse_domain(site)

    site_url, filename_parser = _get_site_data(site)
    print(f"Specified podcast: {site}")
    return site, site_url, filename_parser


def _parse_domain(domain):
    try:
        return domain.split(".")[-2]
    except IndexError:
        raise InvalidSite


def _get_site_data(name):
    try:
        return PODCAST_MAP[name]
    except KeyError:
        raise InvalidSite
