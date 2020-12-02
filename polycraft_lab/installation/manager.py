"""Classes that manage the Polycraft Lab installation."""
import logging
import os
import platform
import shutil
import stat
import subprocess
from pathlib import Path

from polycraft_lab.installation import PAL_DEFAULT_PATH, PAL_LAB_DIR_NAME, \
    PAL_MOD_DIR_NAME
from polycraft_lab.installation.download import download_and_extract_polycraft
from polycraft_lab.installation.releases import UnknownVersionError, get_release

log = logging.getLogger('pal').getChild('installer')


class PolycraftInstallation:
    """A module that manages the Polycraft Lab installation."""

    # TODO: Choose more sensible location, like AppData for windows or /opt for Linux
    DEFAULT_DIRECTORY = str(Path().home() / PAL_LAB_DIR_NAME)

    def __init__(self, installation_directory: str = PAL_DEFAULT_PATH):
        # TODO: Maybe download installation to parent folder of running script
        self._installation_directory = installation_directory

    @property
    def is_installed(self):
        """Currently checks if the game has been built."""
        # TODO: Perform a more thorough check of installation, maybe also with a hash
        # TODO: Find a way to automate ensuring Polycraft is installed
        # TODO: Differentiate between if client is installed vs installed and built
        return (Path(
            self._installation_directory) / PAL_MOD_DIR_NAME
                # / 'build'
                ).exists()

    @property
    def location(self):
        """Return the current Poylcraft Lab installation location."""
        return self._installation_directory

    @property
    def client_location(self):
        """Return the current Polycraft World mod installation location.

        This is different from the Polycraft AI Lab installation, which contains
        PAL configuration files in addition to mod installation.
        """
        return str(Path(self._installation_directory) / PAL_MOD_DIR_NAME)

    def install(self, force_install: bool = False, version: str = 'newest'):
        """Installs and builds a development version of Minecraft.

        Args:
            force_install (bool): Will overwrite the existing Polycraft World
                installation when True, False by default.
            version (str): The version of Polycraft World to install.

        Raises:
            UnknownVersionError when the given version does not exist.
        """
        # TODO: Allow specific version of mod to be chosen
        if not self.is_installed or force_install:
            if force_install:
                log.info('Forcing re-installation of Polycraft World')
            try:
                log.debug('Now downloading Polycraft')
                self._download_polycraft(version)
                log.debug('Launching setup...')
                self._run_setup()
            except UnknownVersionError:
                log.exception(
                    'Attempted to install unknown version of Polycraft: %s',
                    version)
            except InstallationDownloadError:
                log.exception(
                    f'Could not download Polycraft World mod folder to'
                    f'{self.client_location}')
                raise
            except InstallationBuildError:
                log.exception(
                    'Could not install and build Polycraft World mod.')
                raise
        elif self.is_installed:
            log.info(
                'Polycraft World is installed and `force_install` is false, '
                'so not installing mod.')
            return

    def ensure_polycraft_installed(self):
        """Ensures a Polycraft World installation will exist after calling, or fail.

        If Polycraft World is installed, it will be downloaded and then
        installed. Otherwise, this is a no-op.

        This should be preferred to manually checking if the client is installed
        and calling then calling the installer.
        """
        # TODO: Attempt re-installation
        if not self.is_installed:  # Just in case pip install didn't work
            self.install()

    def uninstall(self):
        """Removes the entire Polycraft Lab installation."""
        shutil.rmtree(self._installation_directory, onerror=log.error)

    def _download_polycraft(self, version: str):
        """Downloads and extracts specified version of Polycraft World."""
        try:
            # TODO: Handle retries
            release = get_release(version)
            download_and_extract_polycraft(self.client_location,
                                           bundle_location=release.download_url)
        except Exception:
            raise InstallationDownloadError()

    def _run_setup(self):
        os.chdir(Path(self._installation_directory) / PAL_MOD_DIR_NAME)

        system = platform.system()
        if system == 'Windows':
            gradlew_name = 'gradlew.bat'
        elif system == 'Linux':
            gradlew_name = 'gradlew'
        else:
            raise RuntimeError('OS not supported for Polycraft Lab: %s', system)
        executable = str(Path(self.client_location) / gradlew_name)
        if system == 'Linux':
            # Ensure gradlew is executable
            st = os.stat(str(executable))
            os.chmod(str(executable), st.st_mode | stat.S_IEXEC)
        # TODO: Ensure java executable exists
        try:
            log.info(f'Setting up workspace in {self.client_location}...')
            subprocess.run(
                f'{executable} setupDecompWorkspace --refresh-dependencies'.split())
            log.info('Starting Minecraft build...')
            log.info('This may take a while.')
            subprocess.run(f'{executable} build'.split())
        except Exception:
            raise InstallationBuildError()


class InstallationDownloadError(Exception):
    """raised when there is an error during downloading the mod."""


class InstallationBuildError(Exception):
    """Raised during the Gradle build process."""


class InstallationIncompleteError(Exception):
    """Raised if the Polycraft World installation is not complete."""
