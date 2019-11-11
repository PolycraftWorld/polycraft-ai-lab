"""Functions that run after the Polycraft Lab library is installed."""
from setuptools.command.develop import develop
from setuptools.command.install import install

from polycraft_lab.installation.manager import PolycraftInstallation


class PostDevelopCommand(develop):
    """Sets up this package for development."""

    def run(self):
        """Set up the Polycraft World mod build after library installation."""
        installation_manager = PolycraftInstallation()
        installation_manager.install()
        develop.run(self)


class PostInstallCommand(install):
    """Sets up this package as use for a client."""

    def run(self):
        """Remove the entire Polycraft Lab installation after library uninstallation."""
        installation_manager = PolycraftInstallation()
        installation_manager.install()
        install.run(self)
