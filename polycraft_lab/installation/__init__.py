"""Modules used to manage and run the Polycraft World installation."""
import logging
import tempfile
from pathlib import Path

__all__ = [
    'client', 'client', 'config', 'manager', 'post_pip_install',
    'PAL_MOD_DIR_NAME', 'PAL_LAB_DIR_NAME', 'PAL_TEMP_PATH'
]

log = logging.getLogger('pal').getChild('installer')
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

PAL_TEMP_PATH = Path(tempfile.gettempdir()) / 'polycraft'
PAL_MOD_DIR_NAME = 'polycraft-world'
PAL_LAB_DIR_NAME = 'polycraft-lab'
