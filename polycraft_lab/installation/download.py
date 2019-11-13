import logging
import urllib
from pathlib import Path
from urllib import request
from urllib.error import URLError
from zipfile import ZipFile

REPO_URL = 'https://github.com/StephenGss/polycraft/archive/master.zip'

MOD_ZIP_NAME = 'polycraft-world.zip'

log = logging.Logger(__name__)


def download_polycraft(directory: str, retries: int = 5,
                       repo_location: str = REPO_URL):
    """Download the Polycraft World mod to the given directory.

    This downloads the Polycraft World mod to a temporary directory before
    moving its contents to the given directory

    Args:
        directory (str): The download directory. Files will be copied to the root
            of this directory.
        retries (int): How many times to retry download if it fails.
        repo_location (str): The URL from where to download the Polcraft World
            zip installation.
    """
    for attempt in range(1, retries):
        print(urllib)
        # TODO: Implement exponential backoff
        log.info(f'Downloading Polycraft World mod, attempt #{attempt}')
        try:
            filename = Path(directory) / MOD_ZIP_NAME
            request.urlretrieve(repo_location, filename=filename)
            _extract_polycraft(filename)
            return
        except URLError as e:
            log.error('Could not download', e)
        except Exception as e:
            raise PolycraftDownloadError(e)
    raise PolycraftDownloadError()


class PolycraftDownloadError(Exception):
    """Raised when the Polycraft World mod cannot be downloaded.

    This could result from an IO failure or an internet connection issue.
    """


def _extract_polycraft(location: str):
    with ZipFile(location, 'r') as zip_ref:
        zip_ref.extractall(location)
