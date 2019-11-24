"""Polycraft AI Lab (PAL) environments.

This primarily contains one key environment: the `DynamicExperimentEnv` in
`dynamic_environment.py`. This environment loads configuation data and
automatically creates an environment based on it.
"""

from polycraft_lab.envs.dynamic_environment import DynamicExperimentEnv
from polycraft_lab.envs.helpers import setup_env

__all__ = ['DynamicExperimentEnv', 'setup_env']
