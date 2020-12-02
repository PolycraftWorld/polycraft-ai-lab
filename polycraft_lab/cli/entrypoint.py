"""The CLI wrapper for Polycraft AI Lab.

This can launch the game, manage a Polycraft Lab installation, as well as start
reinforcement learning training experiments.
"""
import os
from pathlib import Path

import fire

from polycraft_lab.installation import PAL_DEFAULT_PATH
from polycraft_lab.installation.client import ClientDidNotStartError, \
    PolycraftClient
from polycraft_lab.installation.config import CONFIG_FILE_NAME, \
    PolycraftLabConfig
from polycraft_lab.installation.manager import PolycraftInstallation

POLYCRAFT_CONFIG_DIR = Path.home() / '.polycraft'

CONFIG_ATTRIBUTE_INSTALLATION = 'installation'


class PolycraftLabCLI:
    """A CLI wrapper for Polycraft AI Lab functionality.

    Usage: python -m polycraft_lab <options>
    """

    def __init__(self):
        """High level commands for the Polycraft Lab CLI."""
        self.config = ConfigGroup()
        self.experiment = RunExperimentGroup()

    def init(self, reinstall: bool = False):
        """Set up Polycraft AI Lab tools.

        This is a guided flow.
        """
        # with CLIContext(): # TODO: Handle Ctrl + C gracefully
        print('Welcome to Polycraft AI Lab.')

        print(f'PAL configuration will be stored in '
              f'{str(self.config.config.location)}')
        # TODO: Save directory
        client = PolycraftInstallation()
        if client.is_installed:
            # TODO: Replace with versioned clients
            should_install = reinstall or _get_bool_input(
                'Client is already installed. Would you like to reinstall the '
                'Polycraft game client?')
            if should_install:
                print('Reinstalling Polycraft World...')
                client.install(force_install=True)
                print('Reinstall complete.')
            else:
                print('Skipping reinstallation')
        else:
            print('Game client is not installed. Installing now.\n')
            client.install()
        should_launch_game = _get_bool_input('Launch game?', default=True)
        if should_launch_game:
            self.launch()

    @staticmethod
    def status():
        """Return the status of the currently running experiment."""
        print('Not yet implemented')

    @staticmethod
    def launch():
        """Launch a Polycraft World instance.

        This also starts the socket connection in the background.
        """
        client = PolycraftInstallation()
        if not client.is_installed:
            print('Polycraft AI Lab has not been initialized')
            print('Please run `pal init` to set up PAL.')
            return

        client = PolycraftClient(
            client.location)  # TODO: Fix this for the love of goodness sake
        print('Starting game...')
        try:
            client.start()
        except ClientDidNotStartError:
            print('Game did not start in time.')

    def turtle(self):
        """Begin an interactive turtle."""
        # TODO: Implement this.
        print('Not yet implemented')


def _get_path(prompt: str) -> Path:
    while True:
        result = input(prompt)
        if os.path.isdir(result):
            path = Path(result)
            return path
        print('That is not a valid path.')


def _get_bool_input(prompt: str, default: bool = None) -> bool:
    while True:
        # TODO: Simplify this if tree
        if default is None:
            prompt_append = '[y/n]'
        elif default:
            prompt_append = '[Y/n]'
        else:
            prompt_append = '[y/N]'
        result = str(input(f'{prompt} {prompt_append} ')).lower()
        if default is None:
            if result == 'y':
                return True
            elif result == 'n':
                return False
            print('A response is required.')
            continue
        elif default:
            if result == 'y' or result == '':
                return True
            elif result == 'n':
                return False

        elif result == 'n':
            return False
        print('That is not a valid response.')


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
