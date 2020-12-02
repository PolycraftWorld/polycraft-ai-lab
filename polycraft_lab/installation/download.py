"""Utility functions for downloading Polycraft Lab resources."""

import logging
import os
import random
import shutil
import time
import urllib
from pathlib import Path
from urllib import request
from urllib.error import URLError
from zipfile import ZipFile

from tqdm import tqdm

from polycraft_lab.installation import PAL_MOD_DIR_NAME, PAL_TEMP_PATH

# TODO: Update repo with actual URL once public
REPO_URL = 'https://github.com/StephenGss/polycraft/archive/master.zip'

MOD_ZIP_NAME = 'polycraft-world-bundle.zip'

log = logging.getLogger('pal').getChild('installer')


def download_and_extract_polycraft(installation_directory: str,
                                   download_directory: str = PAL_TEMP_PATH,
                                   retries: int = 5,
                                   bundle_location: str = REPO_URL,
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
        bundle_location (str): The URL from where to download the Polycraft World
            zip installation.
        should_cleanup (bool): True if the downloaded file should be deleted after
            installation 
    """
    for attempt in range(1, retries):
        # TODO: Perform in separate thread
        log.info('Downloading Polycraft World mod, attempt #%s', attempt)
        _backoff(attempt)
        try:
            # Ensure the directory exists
            Path(download_directory).mkdir(parents=True, exist_ok=True)
            bundle_path = Path(download_directory) / MOD_ZIP_NAME
            log.debug('Downloading to %s', bundle_path)

            _download_url(bundle_location, bundle_path)
            # TODO: Cache installation of mod based on version to prevent unnecessary downloads
            _extract_polycraft(bundle_path, installation_directory,
                               should_cleanup)
            return
        except URLError as e:
            log.error('Could not download Polycraft World on attempt %s',
                      attempt)
            raise PolycraftDownloadError(e)
        except OSError as e:
            log.exception('Error when extracting Polycraft World mod')
            raise PolycraftDownloadError(e)
        except Exception as e:
            log.exception('Could not download Polycraft World on attempt %s',
                          attempt)
            raise PolycraftDownloadError(e)
    log.error('Could not download Polycraft World mod.')
    raise PolycraftDownloadError()


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def _download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path,
                                   reporthook=t.update_to)


def _extract_polycraft(bundle_path: str, dest_dir: str,
                       should_cleanup: bool = True):
    """Extract a Polycraft World bundle to a given location.

    Args:
        bundle_path (str): The location to the zip file containing the
            Polycraft World installation
        dest_dir (str): The destination directory to extract Pol
        should_cleanup (str):
    """
    with ZipFile(bundle_path, 'r') as zip_ref:
        # Downloading from GitHub should only have one subdirectory
        extracted_name = zip_ref.namelist()[0]
        zip_ref.extractall(path=Path(dest_dir))
    os.chdir(Path(dest_dir).parent)
    os.rename(Path(dest_dir) / extracted_name,
              Path(PAL_TEMP_PATH) / PAL_MOD_DIR_NAME)
    shutil.rmtree(dest_dir)
    os.rename(Path(PAL_TEMP_PATH) / PAL_MOD_DIR_NAME,
              dest_dir)
    if should_cleanup:
        shutil.rmtree(PAL_TEMP_PATH)


class PolycraftDownloadError(Exception):
    """Raised when the Polycraft World mod cannot be downloaded.

    This could result from an IO failure or an internet connection issue.
    """


def _backoff(attempt: int, wait_time: int = 2):
    """Perform exponential backoff based on the given attempt.

    Args:
        attempt (int): The n-th time an operation has been tried
        wait_time (int): The amount of seconds to wait
    """
    time.sleep(wait_time ** attempt + random.randint(0, 1_000) / 1_000)
