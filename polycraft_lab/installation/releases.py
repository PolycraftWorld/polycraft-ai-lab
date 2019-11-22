"""Functions for fetching releases of the Polycraft World mod.

The `get_release` function should be used to get specific Polycraft World
release data.
"""

import json
from datetime import datetime
from typing import List

import requests

RELEASES_ENDPOINT = 'https://api.github.com/repos/PolycraftWorld/polycraft-world/releases'


class PolycraftWorldRelease:
    """A data wrapper for Polycraft release information.

    Attributes:
        version (str): The primary identifier for a release
        download_url (str): Where a zip file of this release can be downloaded
        release_date (str): An ISO 8601 timestamp of when this release was created
    """

    def __init__(self, version: str, download_url: str, release_date: str):
        self.version = version
        self.download_url = download_url
        self.release_date = release_date


def get_release(version: str) -> PolycraftWorldRelease:
    """Fetch specific Polycraft World mod release info.

    Args:
        version (str): The version of the mod to release.

    Returns:
        A PolycraftWorldRelease containing info about the requested release.

    Raises:
        UnknownVersionError if the given version does not exist.
    """
    response = requests.get(f'{RELEASES_ENDPOINT}/{version}')
    if not response.ok:
        raise UnknownVersionError('Version not found')
    content = response.content.decode()
    release: dict = json.loads(content)
    return PolycraftWorldRelease(
        release['name'],
        release['zipball_url'],
        release['created_at'],
    )


def get_release_list(released_after: str = None) -> List[PolycraftWorldRelease]:
    """
    Args:
        released_after (str): The

    Returns:
        A list of Polycraft World releases
    """
    response = requests.get(RELEASES_ENDPOINT)
    if not response.ok:
        raise Exception('Error when fetching releases')
    content = response.content.decode()
    releases: List[dict] = json.loads(content)
    releases_result = []
    for release in releases:
        version = release['name']
        download_url = release['zipball_url']
        release_date = release['created_at']
        release_date_timestamp = datetime.fromisoformat(release_date).timestamp()
        released_after_timestamp = datetime.fromisoformat(released_after).timestamp()
        if release_date_timestamp < released_after_timestamp:
            continue
        releases_result.append(PolycraftWorldRelease(
            version,
            download_url,
            release_date,
        ))
    return releases_result


class UnknownVersionError(Exception):
    """Raised when a given version does not exist.

    This is a checked exception and should not end the program.
    """
