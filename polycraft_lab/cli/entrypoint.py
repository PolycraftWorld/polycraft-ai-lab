"""The CLI wrapper for Polycraft AI Lab.

This can launch the game, manage a Polycraft Lab installation, as well as start
reinforcement learning training experiments.
"""
import logging
from pathlib import Path
import fire

from polycraft_lab.cli.console_utils import _get_bool_input
from polycraft_lab.installation import PAL_DEFAULT_PATH
from polycraft_lab.installation.game import ClientNotInitializedError
from polycraft_lab.installation.comms import ClientDidNotStartError
from polycraft_lab.installation.client_tools import launch_polycraft
from polycraft_lab.installation.config import CONFIG_FILE_NAME, \
    PolycraftLabConfig
from polycraft_lab.installation.manager import PolycraftInstallation

POLYCRAFT_CONFIG_DIR = Path.home() / '.polycraft'

CONFIG_ATTRIBUTE_INSTALLATION = 'installation'

log = logging.getLogger('pal').getChild('cli')


class CLIContext:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_type, KeyboardInterrupt):
            print('')


class PolycraftLabCLI:
    """A CLI wrapper for Polycraft AI Lab functionality.

    Usage: python -m polycraft_lab <options>
    """

    def __init__(self, verbose: bool = False):
        """High level commands for the Polycraft Lab CLI."""
        self.config = ConfigGroup()
        self.experiment = RunExperimentGroup()
        self.verbose = verbose

        if verbose:
            log.setLevel(logging.DEBUG)

        log.debug('Starting CLI')

    def init(self, reinstall: bool = False):
        """Set up Polycraft AI Lab tools.

        This is a guided flow.
        """
        # with CLIContext(): # TODO: Handle Ctrl + C gracefully
        log.debug('Init command selected')
        print('Welcome to Polycraft AI Lab.')

        print(f'PAL configuration will be stored in '
              f'{str(self.config.config.location)}')
        # TODO: Save directory
        game = PolycraftInstallation()
        if game.is_installed:
            # TODO: Replace with versioned clients
            should_install = reinstall or _get_bool_input(
                'Client is already installed. Would you like to reinstall the '
                'Polycraft game client?')
            if should_install:
                print('Reinstalling Polycraft World...')
                game.install(force_install=True)
                print('Reinstall complete.')
            else:
                print('Skipping reinstallation')
        else:
            print('Game client is not installed. Installing now.\n')
            game.install()
        should_launch_game = _get_bool_input('Launch game?', default=True)
        if should_launch_game:
            self.launch()

    @staticmethod
    def status():
        """Return the status of the currently running experiment."""
        log.debug('Status command selected')
        print('Not yet implemented')

    def launch(self):
        """Launch a Polycraft World instance.

        This also starts the socket connection in the background. Once this
        command is run, the process continues until it is killed with Ctrl + C.
        """
        log.debug('Launch command selected')
        try:
            print('Starting Polycraft...')
            launch_polycraft(verbose=self.verbose)
        except ClientNotInitializedError:
            print('The game has not been initialized.'
                  'Please run pal init to set up the game.')
        except ClientDidNotStartError:
            print('Oops, something went wrong. The game did not start.')
            # TODO: Provide instructions to post logs
            print('Open an issue at'
                  'https://github.com/PolycraftWorld/polycraft-ai-lab/issues'
                  'containing information from your log files.')
        log.debug('Exiting CLI')

    def turtle(self):
        """Begin an interactive turtle."""
        # TODO: Implement this.
        log.debug('Turtle command selected')
        print('Valid commands: [quit]')
        last_input = input('>>> ')
        while True:
            log.debug(f'Given command: {last_input}')
            if last_input.lower() is 'quit':
                break
        log.debug('Exiting CLI')


class ConfigGroup:
    """Manage Polycraft Lab configuration."""

    def __init__(self, config_name: str = CONFIG_FILE_NAME):
        config_location = Path(PAL_DEFAULT_PATH) / config_name
        self.config = PolycraftLabConfig.from_file(str(config_location))

    @staticmethod
    def update(attribute, arg: str = None):
        """Update a configuration value for Polycraft AI Lab."""
        if attribute == 'installation':
            if arg is None:
                # print('Installation directory is required.')
                return
            # TODO: Check installation directory
        else:
            raise Exception('Unknown option')
        print('Not yet implemented')


class RunExperimentGroup:
    """Run baselines and custom experiments"""

    def __init__(self, experiment_name: str = None):
        """"""
        if experiment_name:
            pass
        else:
            # Run experiment in current directory
            pass

    def launch(self, config_path):
        print('Not yet implemented')

    def test(self):
        """Test a task"""
        print('Not yet implemented')

    def create(self):
        """Create a new experiment"""
        print('Not yet implemented')


def run_cli():
    """Trigger the Polycraft World command line interface."""
    fire.Fire(PolycraftLabCLI)


if __name__ == '__main__':
    run_cli()
