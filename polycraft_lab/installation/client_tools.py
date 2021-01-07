import logging

from polycraft_lab.installation import PAL_DEFAULT_PATH, PAL_MOD_DIR_NAME
from polycraft_lab.installation.client import PolycraftClient
from polycraft_lab.installation.game import ClientNotInitializedError
from polycraft_lab.installation.comms import ClientDidNotStartError

log = logging.getLogger('pal').getChild('client')


def launch_polycraft(directory: str = PAL_DEFAULT_PATH / PAL_MOD_DIR_NAME,
                     verbose: bool = False):
    """Launch the default Polycraft World installation."""
    if verbose:
        log.setLevel(logging.DEBUG)

    log.info('Launching Polycraft')
    log.debug(f'Installation directory: {directory}')
    try:
        # TODO: Check that game is installed
        client = PolycraftClient(directory)
        client.start()
        while client.is_alive:
            # TODO: Insert wait and then listen to commands from STDiIN
            # TODO; Send commends from STDIN to client
            pass
    except ClientNotInitializedError as e:
        log.error(f'Game client not found at {directory}')
        raise e
    except ClientDidNotStartError as e:
        log.error('Game did not start in time.', e)
        raise e
    client.stop()
