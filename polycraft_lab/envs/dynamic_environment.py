from typing import Tuple

from gym import Env


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
        self.reward = 0

    def step(self, action) -> Tuple[object, float, bool, dict]:
        """Compute a training step.

        Args:
            action: An action in this experiment's action space

        Returns:
            A tuple containing the new observation, reward, done state,
            and info.
        """
        observation = {}
        reward = self._determine_reward(action)
        done = self._is_done
        info = {}  # TODO: Find useful information to put in her
        return observation, reward, done, info

    def reset(self):
        """Prepare the environment for another episode of training."""
        raise NotImplementedError()

    def render(self, mode='human'):
        """Display """
        assert mode in self.metadata['render.modes']
        if mode == 'human':
            pass
        elif mode == 'state_pixels':
            pass
        else:  # mode == rgb_array
            pass
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    @property
    def _is_done(self) -> bool:
        return False

    def _setup_scene(self, scene: str):
        raise NotImplementedError()

    def _determine_reward(self, action):
        raise NotImplementedError()
