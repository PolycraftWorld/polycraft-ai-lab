import logging
from typing import Tuple

from gym import Env

from polycraft_lab.envs.experiment_config import ExperimentConfig
from polycraft_lab.installation.client import PolycraftClient
from polycraft_lab.installation.manager import PolycraftInstallation

log = logging.getLogger(__name__)


class DynamicExperimentEnv(Env):
    """An experiment environment that dynamically loads experiments.

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
    """
    metadata = {'render.modes': ['human, state_pixels, rgb_array', 'ansi']}

    def __init__(self, config_path: str):
        self.config = self._load_experiment_config(config_path)
        log.info('Config fetched.')
        installation = PolycraftInstallation()
        try:
            installation.ensure_polycraft_installed()
            self.client = PolycraftClient(installation.location)
            self.action_space = self.config.action_space
        except Exception:
            raise Exception('Cannot start training. Error during Polycraft runtime installation.')
        self.client.start()
        self.reward = 0

    @staticmethod
    def _load_experiment_config(config_path: str):
        try:
            return ExperimentConfig.from_file(config_path)
        except IOError as e:
            log.error('Could not get config from file.', e)
            raise e

    def step(self, action) -> Tuple[object, float, bool, dict]:
        """Compute a training step.

        Args:
            action: An action in this experiment's action space

        Returns:
            A tuple containing the new observation, reward, done state,
            and info.
        """
        observation = {}
        reward = self._determine_reward(action, observation)
        done = False
        info = {}  # TODO: Find useful information to put in her
        return observation, reward, done, info

    def reset(self):
        """Prepare the environment for another episode of training."""
        # TODO: Provide functionality to put experiments in sequence
        # One episode might consist of multiple scenes in a sequence?
        scenes = self.config.scenes  # Probably domains for now
        self.client.setup_scene(scenes[0])

    def render(self, mode: str = 'human'):
        """Display training output for this environment.

        Args:
            mode (str): How this environment should output information
        """
        assert mode in self.metadata['render.modes']
        if mode == 'human':
            pass
        elif mode == 'state_pixels':
            pass
        elif mode == 'rgb_array':
            pass
        else:  # mode == 'ansi'
            pass
        raise NotImplementedError()

    def close(self):
        """Shutdown this training environment."""
        self.client.stop()

    def _determine_reward(self, state, action):
        raise NotImplementedError()

    def _determine_state(self):
        action_space = self.action_space
        # TODO: Use novelty.
        self.client.send_to_server('GENERATE NOVELTY')  # Okay, not really.
        pass
