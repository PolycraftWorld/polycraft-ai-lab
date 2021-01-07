"""Polycraft AI Lab (PAL), a tool to train RL models in novel environments.

Examples can be found in `examples`.
"""
import logging
from datetime import datetime

from polycraft_lab.cli.entrypoint import run_cli
# TODO: Fix this smelly import order
from polycraft_lab.installation import PAL_DEFAULT_PATH
from polycraft_lab.installation.client_tools import launch_polycraft as launch
from polycraft_lab.envs import make

__all__ = ['cli', 'ect', 'envs', 'examples', 'tests', 'run_cli',
           'make', 'launch', ]

LOGGING_FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'

LOGGING_FILE_NAME = str(
    PAL_DEFAULT_PATH /
    f'pal_logs_{datetime.now().strftime("%Y_%m_%d_%H:%M:%S")}.txt'
)

logging.basicConfig(
    format=LOGGING_FORMAT,
    handlers=[
        logging.FileHandler(LOGGING_FILE_NAME, mode='w'),
        logging.StreamHandler(),
    ],
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)
