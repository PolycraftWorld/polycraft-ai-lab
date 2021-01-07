"""Modules used to manage and run the Polycraft World installation."""
import logging
import tempfile
from pathlib import Path

log = logging.getLogger('pal').getChild('installer')
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

PAL_MOD_DIR_NAME = 'polycraft-world'
PAL_LAB_DIR_NAME = 'polycraft-lab'
PAL_DEFAULT_PATH = Path().home() / PAL_LAB_DIR_NAME
PAL_TEMP_PATH = Path(tempfile.gettempdir()) / PAL_LAB_DIR_NAME

__all__ = [
    'client', 'client', 'config', 'manager', 'post_pip_install',
    'PAL_MOD_DIR_NAME', 'PAL_LAB_DIR_NAME', 'PAL_TEMP_PATH', 'PAL_DEFAULT_PATH',
]
