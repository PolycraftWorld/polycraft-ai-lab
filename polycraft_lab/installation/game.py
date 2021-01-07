import logging
import platform
from pathlib import Path
from subprocess import PIPE, Popen

log = logging.getLogger('pal').getChild('env').getChild('game')


class PolycraftGame:
    """A wrapper for a Polycraft game installation.

    This class can be used to initialize a Polycraft game instance
    and maintain a handle on the process.
    """

    def __init__(self, installation_directory: str):
        self._installation_directory = installation_directory
        # noinspection PyTypeChecker
        self._process: Popen = None
        self.check_installed()

    def check_installed(self):
        # TODO: Find more robust way of doing this
        if not (Path(self._installation_directory) / 'gradlew').exists():
            raise ClientNotInitializedError

    @property
    def is_alive(self):
        return self._process.poll() is None

    def start(self):
        """Attempt to start the game.

        Raises:
            ClientNotInitializedError: If the game has not been properly
            initialized or installed.
        """
        self.check_installed()
        if platform.system() not in ['Windows', 'Linux', 'Darwin']:
            raise Exception('Attempting to start client on an unspported OS.')
        gradlew_name = 'gradlew'
        if platform.system() == 'Windows':
            gradlew_name = 'gradlew.bat'
        cwd = Path(self._installation_directory)
        executable_base = str(cwd / gradlew_name)
        log.info('Starting Minecraft... This may also take a bit.')

        # This should be the last thing
        self._process = Popen(
            [executable_base, 'runClient'],
            stdout=PIPE,
            # shell=True,
            # close_fds=False,
            cwd=cwd,
        )
        log.debug('Polycraft client started')

    def stop(self):
        if self._process is None or not self.is_alive:
            return
        try:
            self._process.terminate()
        except PermissionError as e:
            log.error('Could not correctly terminate game', e)
        else:
            log.debug('Polycraft client terminated')

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


class ClientNotInitializedError(Exception):
    """Indicates that a Polycraft game client runtime has not been set up.

    Catchers of this error should install or reinstall the game client to
    initialize any required files for the client to run..
    """
