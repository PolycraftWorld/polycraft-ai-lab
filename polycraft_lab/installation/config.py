"""Classes for managing the Polycraft Lab installation configuration."""
import codecs
import json
from pathlib import Path

CONFIG_LAB_SERVER_PORT = 'lab.server.port'

CONFIG_LAB_SERVER_HOST = 'lab.server.host'

CONFIG_FILE_NAME = 'lab_config.json'


class PolycraftLabConfig:
    """A wrapper for various Polycraft Lab installation configuration values."""

    def __init__(self, config_path: str):
        self._config_path = Path(config_path)
        self.config = self._load_config(config_path)

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
    def lab_server_port(self):
        """Return the Polycraft Lab socket port."""
        return self.config['lab']['server']['port']

    @lab_server_port.setter
    def lab_server_port(self, new_port: int):
        """Set the new Polycraft Lab socket port."""
        self.config[CONFIG_LAB_SERVER_PORT] = new_port
        with codecs.open(self._config_path, 'r+', encoding='utf-8') as config_file:
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
        with codecs.open(self._config_path, 'r+', encoding='utf-8') as config_file:
            data = json.load(config_file)
            data['lab']['server']['host'] = new_host
            config_file.seek(0)
            json.dump(data, config_file, indent=4)
            config_file.truncate()
