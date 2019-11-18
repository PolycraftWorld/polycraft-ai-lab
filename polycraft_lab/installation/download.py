"""Utility functions for downloading Polycraft Lab resources."""

import logging
import os
import shutil
from pathlib import Path
from urllib import request
from urllib.error import URLError
from zipfile import ZipFile

from installation import PAL_MOD_DIR_NAME, PAL_TEMP_PATH

# TODO: Update repo with actual URL
REPO_URL = 'https://github.com/StephenGss/polycraft/archive/1.8.9AIGym.zip'

MOD_ZIP_NAME = 'polycraft-world-bundle.zip'

log = logging.getLogger('pal').getChild('installer')


def download_and_extract_polycraft(installation_directory: str,
                                   download_directory: str = PAL_TEMP_PATH,
                                   retries: int = 5,
                                   repo_location: str = REPO_URL,
                                   should_cleanup: bool = True):
    """Download and extract the Polycraft World mod to the given directory.

    This downloads the Polycraft World mod to a temporary directory before
    moving its contents to the given directory.

    In the event that files already exist in the given installation_directory,
    they will be overwritten.

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
            download_file_path = Path(download_directory) / MOD_ZIP_NAME
            log.debug('Downloading to %s', download_file_path)
            request.urlretrieve(repo_location, filename=download_file_path)
            with ZipFile(download_file_path, 'r') as zip_ref:
                # Downloading from GitHub should only have one subdirectory
                extracted_name = zip_ref.namelist()[0]
                zip_ref.extractall(path=Path(installation_directory))
            os.chdir(Path(installation_directory).parent)
            os.rename(Path(installation_directory) / extracted_name,
                      Path(PAL_TEMP_PATH) / PAL_MOD_DIR_NAME)
            shutil.rmtree(installation_directory)
            os.rename(Path(PAL_TEMP_PATH) / PAL_MOD_DIR_NAME,
                      installation_directory)
            # TODO: Cache installation of mod to prevent unnecessary downloads
            if should_cleanup:
                shutil.rmtree(PAL_TEMP_PATH)
            return
        except URLError as e:
            log.error('Could not download Polycraft World on attempt %s', attempt)
            raise PolycraftDownloadError(e)
        except OSError as e:
            log.exception('Error when extracting Polycraft World mod')
            raise PolycraftDownloadError(e)
        except Exception as e:
            log.exception('Could not download Polycraft World on attempt %s', attempt)
            raise PolycraftDownloadError(e)
    log.error('Could not download Polycraft World mod.')
    raise PolycraftDownloadError()


class PolycraftDownloadError(Exception):
    """Raised when the Polycraft World mod cannot be downloaded.

    This could result from an IO failure or an internet connection issue.
    """
