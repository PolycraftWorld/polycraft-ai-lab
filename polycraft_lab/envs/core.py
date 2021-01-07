import logging
from typing import Tuple

import numpy as np

from polycraft_lab import PAL_DEFAULT_PATH
from polycraft_lab.installation.client import PolycraftClient

log = logging.getLogger('pal').getChild('env').getChild('core')


class PolycraftEnv:
    """A reinforcement learning environment for the Polycraft World mod."""

    def __init__(self, mission_path: str):
        """Creates a new Polycraft environment.

        TODO:
        This environment relies upon a config file used to dictate everything about
        an experiment, including action space, reward signals, in-game environment
        setup, and novelty generation.

        If mode is:
        - human: render Minecraft client to window for human consumption.
        - state_pixels: Render Minecraft client to window without certain
          special effects.
        - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
          representing RGB values for an x-by-y pixel image, suitable
          for turning into a video.
        - ansi: Return a string (str) or StringIO.StringIO containing a
          terminal-style text representation. The text can include newlines
          and ANSI escape sequences (e.g. for colors).

        Args:
            mission_path: The location of the configuration file.
        """
        self._mission = mission_path
        installation_path = PAL_DEFAULT_PATH  # TODO: Fetch from config
        self._client = PolycraftClient(installation_path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            log.error('Error during exit', exc_tb)
        self._client.stop()

    def set_mission(self, mission_path: str):
        self._mission = mission_path

    def reset(self):
        """Reset the environment and get an initial observation"""
        self._client.send('START')
        self._client.send(f'RESET -d {self._mission}')

    def step(self, action: str) -> Tuple[object, int, bool, dict]:
        # TODO: Get client to send consistent data format
        # observation = self._client.send('SENSE_ALL')
        reward = 0
        done = not self._client.is_alive
        info = {}
        # if action == 'break_block':
        observation = self._client.send(action)

        return observation, reward, done, info

    def render(self, mode: str = 'human'):
        """Display training output for this environment.

        Args:
            mode (str): How this environment should output information
        """
        # assert mode in self.metadata['render.modes']
        if mode == 'human':
            pass
        elif mode == 'state_pixels':
            pass
        elif mode == 'rgb_array':
            pass
        else:  # mode == 'ansi'
            pass
        raise NotImplementedError()
