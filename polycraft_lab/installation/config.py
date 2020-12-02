"""Classes for managing the Polycraft Lab installation configuration."""
import codecs
import json
import os
from pathlib import Path

from polycraft_lab.installation import PAL_DEFAULT_PATH

CONFIG_LAB_SERVER_PORT = 'lab.server.port'

CONFIG_LAB_SERVER_HOST = 'lab.server.host'

CONFIG_FILE_NAME = 'lab_config.json'


class ConfigLoadingError(Exception):
    """An error raised when a config at the current location could not be loaded.

    This normally means that the given file does not exist.
    """


class ConfigInvalidFormatError(ConfigLoadingError):
    """Raised when a config file cannot be loaded """


CONFIG_TEMPLATE = '''{
  "lab": {
    "server": {
      "host": "127.0.0.1",
      "port": 9000
    }
  }
}
'''


def _init_lab_config(installation_path: Path = PAL_DEFAULT_PATH):
    """Create and write a config file from template.

    This overwrites the existing config file at the given location.
    Args:
        installation_path (Path): The location of the PAL config file
    """
    # TODO: Consolidate directory management and fix this hack
    installation_path.mkdir(parents=True, exist_ok=True)
    with (installation_path / CONFIG_FILE_NAME).open('w+') as f:
        f.write(CONFIG_TEMPLATE)
        # TODO: Actually initialize config


class PolycraftLabConfig:
    """A wrapper for various Polycraft Lab installation configuration values."""

    def __init__(self, config_path: str, create_file=True):
        self._config_path = Path(config_path)
        try:
            # TODO: Check if path actually exists
            if not os.path.isfile(config_path):
                if not create_file:
                    raise ConfigLoadingError()
                # Create new file if it doesn't exist
                _init_lab_config()
            self.config = self._load_config(config_path)
        except ValueError as e:
            # TODO: Log error
            raise ConfigInvalidFormatError

    @classmethod
    def from_file(cls, path: str):
        # Check if file exists
        return cls(path)

    @classmethod
    def from_installation(cls, installation_dir: str):
        """Initialize a new PolycraftLab object.

        Args:
            installation_dir (str): The path to the Polycraft Installation.
        """
        return cls(str(Path(installation_dir) / CONFIG_FILE_NAME))

    @staticmethod
    def _load_config(config_path: str) -> dict:
        """Return a new ExperimentConfig.

        Args:
            config_path (str): The path to the experiment configuration file JSON.
        """
        with codecs.open(config_path) as file:
            return json.load(file)

    @property
    def location(self) -> Path:
        return self._config_path

    @property
    def lab_server_port(self):
        """Return the Polycraft Lab socket port."""
        return self.config['lab']['server']['port']

    @lab_server_port.setter
    def lab_server_port(self, new_port: int):
        """Set the new Polycraft Lab socket port."""
        self.config[CONFIG_LAB_SERVER_PORT] = new_port
        with codecs.open(self._config_path, 'r+',
                         encoding='utf-8') as config_file:
            data = json.load(config_file)
            data['lab']['server']['port'] = new_port
            config_file.seek(0)
            json.dump(data, config_file, indent=4)
            config_file.truncate()

    @property
    def lab_server_host(self) -> str:
        """Return the Polycraft Lab socket host.

        Example: '127.0.0.1'
        """
        return self.config['lab']['server']['host']

    @lab_server_host.setter
    def lab_server_host(self, new_host):
        """Set the new Polycraft Lab socket port.

        Example: 9000
        """
        self.config[CONFIG_LAB_SERVER_PORT] = new_host
        with codecs.open(self._config_path, 'r+',
                         encoding='utf-8') as config_file:
            data = json.load(config_file)
            data['lab']['server']['host'] = new_host
            config_file.seek(0)
            json.dump(data, config_file, indent=4)
            config_file.truncate()
