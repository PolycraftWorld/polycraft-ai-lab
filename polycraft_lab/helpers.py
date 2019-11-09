"""Some helper functions for various Polycraft AI Lab tasks."""

import gym
from gym.envs.registration import register

DYNAMIC_ENV_ID = 'PALDynamicEnv-v0'

register(
    id=DYNAMIC_ENV_ID,
    entry_point='polycraft_lab.envs.dynamic_environment:DynamicExperimentEnv',
)


def setup_env(config_path: str, env_name: str = DYNAMIC_ENV_ID) -> gym.core.Env:
    """Create a dynamic Polycraft AI Lab environment.

    This is used to register an environment in OpenAI Gym before

    Args:
        config_path (str): The path to the
        env_name (str): By default, 'PALDynamicEnv-0', the standard Polycraft
                        dynamic experiment environment. This is used to load
                        custom experiment environments.
    """
    if env_name is not DYNAMIC_ENV_ID:  # Prevent duplicate registration
        register(
            id=env_name,
            kwargs={'config_path': config_path}
        )
    env = gym.make(env_name, config_path=config_path)  # Only create env after registration
    return env
