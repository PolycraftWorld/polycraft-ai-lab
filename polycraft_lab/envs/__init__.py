"""Polycraft AI Lab (PAL) environments.

This primarily contains one key environment: the `PolycraftEnv` in `core.py`.
This environment loads configuration data and automatically creates an OpenAI
Gym-like environment based on the config.

The `setup_env` helper function should be used to create a new environment
instead of instantiating a `PolycraftEnv` directly.
"""

from polycraft_lab.envs.core import PolycraftEnv
from polycraft_lab.envs.helpers import make

__all__ = ['PolycraftEnv', 'make']
