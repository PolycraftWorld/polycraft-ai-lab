"""Functions that run after the Polycraft Lab library is installed."""
from setuptools.command.develop import develop
from setuptools.command.install import install


class PostDevelopCommand(develop):
    """Sets up this package for development."""

    def run(self):
        # """Set up the Polycraft World mod build after library installation."""
        # TODO: Figure out how to handle setting up development environment
        # installation_manager = PolycraftInstallation()
        # installation_manager.install()
        develop.run(self)


class PostInstallCommand(install):
    """Sets up this package as use for a client."""

    def run(self):
        # """Remove the entire Polycraft Lab installation after library uninstallation."""
        # installation_manager = PolycraftInstallation()
        # installation_manager.install()
        print('To finish Polycraft AI Lab setup, run "pal init" on the command '
              'line.')
        install.run(self)
