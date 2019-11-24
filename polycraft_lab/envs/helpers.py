"""Some helper functions for various Polycraft AI Lab tasks."""
import logging

import gym
from gym.envs.registration import EnvRegistry, register

DYNAMIC_ENV_ID = 'PALDynamicEnv-v0'

# Account for possibility of multiple imports
registry = EnvRegistry()
if DYNAMIC_ENV_ID not in registry.env_specs:
    register(
        id=DYNAMIC_ENV_ID,
        entry_point='polycraft_lab.envs.dynamic_environment:DynamicExperimentEnv',
)

log = logging.getLogger('pal')


def setup_env(config_path: str, env_name: str = DYNAMIC_ENV_ID) -> gym.core.Env:
    """Create a dynamic Polycraft AI Lab environment.

    This is used to automatically register an environment in OpenAI Gym before
    instantiating an instance of it.

    Args:
        config_path (str): The path to the experiment's configuration file
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
    log.info('Registered new environment %s using config at %s', env_name, config_path)
    return env
