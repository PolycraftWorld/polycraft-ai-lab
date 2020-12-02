"""Polycraft AI Lab (PAL), a tool to train RL models in novel environments.

Examples can be found in `examples`.
"""
from polycraft_lab.cli.entrypoint import run_cli

# from polycraft_lab.envs.core import create_env, get_tasks

__all__ = ['cli', 'ect', 'envs', 'examples', 'tests', 'run_cli'
           # 'get_tasks', 'create_env',
           ]
