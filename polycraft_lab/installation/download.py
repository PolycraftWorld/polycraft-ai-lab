import logging
import os
import tempfile
from pathlib import Path
from urllib import request
from urllib.error import URLError
from zipfile import ZipFile

REPO_URL = 'https://github.com/StephenGss/polycraft/archive/1.8.9AIGym.zip'

MOD_ZIP_NAME = 'polycraft-world.zip'

log = logging.Logger(__name__)


def download_and_extract_polycraft(installation_directory: str,
                                   download_directory: str = tempfile.gettempdir(),
                                   retries: int = 5,
                                   repo_location: str = REPO_URL,
                                   should_cleanup: bool = True):
    """Download and extract the Polycraft World mod to the given directory.

    This downloads the Polycraft World mod to a temporary directory before
    moving its contents to the given directory.

    In the event that files already exist, they will be overwritten.

    Args:
        installation_directory (str): Where Polycraft World mod files will be
            copied to the root.
        download_directory (str): The location where the Polycraft World zip
            will be downloaded, a temporary directory by default
        retries (int): How many times to retry download if it fails.
        repo_location (str): The URL from where to download the Polcraft World
            zip installation.
        should_cleanup (bool): True if the downloaded file should be deleted after
            installation 
    """
    for attempt in range(1, retries):
        # TODO: Perform in separate thread
        # TODO: Implement exponential backoff
        log.info('Downloading Polycraft World mod, attempt #%s', attempt)
        try:
            Path(download_directory).mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
            download_file_path = f'{download_directory}/{MOD_ZIP_NAME}'
            log.debug('Downloading to %s', download_file_path)
            request.urlretrieve(repo_location, filename=download_file_path)
            with ZipFile(download_file_path, 'r') as zip_ref:
                extracted_name = zip_ref.namelist()[0]  # GitHub should only have one directory
                zip_ref.extractall(path=Path(installation_directory).parent)
                os.rename(Path(installation_directory).parent / extracted_name,
                          installation_directory)
            return
        except URLError as e:
            log.error('Could not download Polycraft World', e)
            raise PolycraftDownloadError(e)
        except Exception as e:
            log.error('Could not download Polycraft World', e)
            raise PolycraftDownloadError(e)
    raise PolycraftDownloadError()


class PolycraftDownloadError(Exception):
    """Raised when the Polycraft World mod cannot be downloaded.

    This could result from an IO failure or an internet connection issue.
    """
