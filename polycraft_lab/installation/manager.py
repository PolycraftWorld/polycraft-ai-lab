"""Functionality that enables """
import logging
import os
import platform
import shutil
import subprocess
from pathlib import Path

POLYCRAFT_LAB_DIR = 'polycraft-lab'

POLYCRAFT_MOD_DIR = 'polycraft-world'

log = logging.getLogger(__name__)


class PolycraftInstallation:
    """A module that manages the Polycraft Lab installation."""

    # TODO: Choose more sensible location, like AppData for windows or /opt for Linux
    DEFAULT_DIRECTORY = str(Path().home() / POLYCRAFT_LAB_DIR)

    def __init__(self, installation_directory: str = DEFAULT_DIRECTORY):
        # TODO: Maybe download installation to parent folder of running script
        self._installation_directory = installation_directory

    @property
    def is_installed(self):
        """Currently checks if the game has been built."""
        # TODO: Perform a more thorough check of installation, maybe also with a hash
        # TODO: Find a way to automate ensuring Polycraft is installed
        return (Path(self._installation_directory) / POLYCRAFT_MOD_DIR / 'build').exists()

    @property
    def client_location(self):
        """Return the current Polycraft Lab mod installation location."""
        return f'{self._installation_directory}/{POLYCRAFT_MOD_DIR}'

    def install(self, force_install: bool = False):
        """Installs and builds a development version of Minecraft."""
        if self.is_installed and force_install:
            try:
                self._download_polycraft()
                self._run_setup()
            except InstallationDownloadError as e:
                log.error(f'Could not download Polycraft World mod folder to {self._installation_directory}', e)
                raise
            except InstallationBuildError as e:
                log.info('Could not install and build Polycraft World mod.', e)
                raise
        elif self.is_installed:
            return

    def uninstall(self):
        shutil.rmtree(self._installation_directory, onerror=log.error)

    @staticmethod
    def _download_polycraft():
        # Get from GitHub releases /cloning repo
        try:
            pass
        except Exception:
            raise InstallationDownloadError()

    def _run_setup(self):
        os.chdir(
            Path(self._installation_directory) / POLYCRAFT_MOD_DIR)  # Make sure we're in root directory before running

        gradlew_name = 'gradlew'
        if platform.system() == 'Windows':
            gradlew_name = 'gradlew.bat'
        executable = f'{self._installation_directory}\\{gradlew_name}'
        try:
            logging.info(f'Setting up workspace in {self._installation_directory}...')
            subprocess.run(f'{executable} setupDecompWorkspace --refresh-dependencies'.split())
            logging.info('Starting Minecraft build...')
            logging.info('This may take a while.')
            subprocess.run(f'{executable} build'.split())
        except Exception:
            raise InstallationBuildError()


class InstallationDownloadError(Exception):
    """raised when there is an error during downloading the mod."""


class InstallationBuildError(Exception):
    """Raised during the Gradle build process."""


class InstallationIncompleteError(Exception):
    """Raised if the Polycraft World installation is not complete."""
