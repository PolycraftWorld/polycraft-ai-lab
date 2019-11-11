import codecs
import json
from pathlib import Path
from typing import Dict, List

CONFIG_ACTION_SPACE = 'action_space'

CONFIG_EXPERIMENT_SCENES = 'scenes'


class ExperimentConfig:
    """A wrapper for Polycraft Lab experiment configuration values."""

    def __init__(self, config_path: str):
        """Initialize a new ExperimentConfig object.

        Args:
            config_path (str): The path to the experiment configuration file JSON.
        """
        self._config_path = Path(config_path)
        self.config = self._load_config(config_path)

    @classmethod
    def from_file(cls, config_path: str):
        """Return a new ExperimentConfig.

        Args:
            config_path (str): The path to the experiment configuration file JSON.
        """
        return cls(config_path)

    @staticmethod
    def _load_config(config_path: str) -> dict:
        return json.load(config_path)

    @property
    def action_space(self) -> Dict:
        """Return the Polycraft Lab socket port."""
        return self.config[CONFIG_ACTION_SPACE]

    @action_space.setter
    def action_space(self, new_action_space: dict):
        self.config[CONFIG_ACTION_SPACE] = new_action_space
        with codecs.open(self._config_path, 'r+', encoding='utf-8') as config_file:
            data = json.load(config_file)
            data[CONFIG_ACTION_SPACE] = new_action_space
            config_file.seek(0)
            json.dump(data, config_file, indent=4)
            config_file.truncate()

    @property
    def scenes(self) -> List[str]:
        return self.config[CONFIG_EXPERIMENT_SCENES]

    @scenes.setter
    def scenes(self, new_scenes: List[str]):
        # TODO: Consider if a setter is really needed for this
        self.config[CONFIG_EXPERIMENT_SCENES] = new_scenes
        with codecs.open(self._config_path, 'r+', encoding='utf-8') as config_file:
            data = json.load(config_file)
            data[CONFIG_ACTION_SPACE] = new_scenes
            config_file.seek(0)
            json.dump(data, config_file, indent=4)
            config_file.truncate()
