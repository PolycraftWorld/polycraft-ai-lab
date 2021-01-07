"""Some helper functions for various Polycraft AI Lab tasks."""
import logging

from polycraft_lab.envs import PolycraftEnv

log = logging.getLogger('pal').getChild('env')

DEFAULT_MISSION_PATH = '../available_tests/pogo_nonov.json'


def make(env_name: str = None, **kwargs):
    """Create a new PolycraftEnv."""
    if 'mission_path' in kwargs:
        mission_path = kwargs['mission_path']
    elif env_name is 'pogo_stick':
        # TODO: Don't hardcode this
        mission_path = DEFAULT_MISSION_PATH
    else:
        mission_path = DEFAULT_MISSION_PATH

    return PolycraftEnv(mission_path=mission_path)
