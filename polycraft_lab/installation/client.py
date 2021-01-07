"""Classes for managing the runtime clients for Polycraft Lab.

The PolycraftClient should be used to manage the currently running Polycraft
installation and send messages/commands to the client.

This includes the PolycraftModRuntime, which handles starting and stopping the
mod, and PolycraftServerBridge, which is responsible for sending commands to the
currently running game.
"""
import logging
from typing import Callable

from polycraft_lab.installation.comms import ClientDidNotStartError, \
    DEFAULT_HOST, DEFAULT_PORT, PolycraftBridge
from polycraft_lab.installation.game import PolycraftGame

log = logging.getLogger('pal').getChild('client').getChild('core')


class PolycraftClient:
    """A module that manages a running Polycraft World client."""

    def __init__(self, installation_path: str,
                 message_callback: Callable[[str], None] = None):
        self.is_running = False
        # TODO: Fetch values from config
        # config = PolycraftLabConfig.from_installation(installation_path)
        self.game = PolycraftGame(installation_path)
        self.bridge = PolycraftBridge(DEFAULT_HOST, DEFAULT_PORT,
                                      message_callback)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    @property
    def is_alive(self):
        """Return True if the game client can receive commands."""
        return self.game.is_alive

    def start(self):
        """Try starting the game client and message channel."""
        log.debug('Starting game')
        with self.game:
            log.debug('Starting communication bridge')
            try:
                self.bridge.start()
            except ClientDidNotStartError:
                raise
        self.bridge.disconnect()

    def stop(self):
        """Stop the currently running game of Minecraft."""
        self.is_running = False

    def send(self, message: str):
        """Send a message to the server."""
        return self.bridge.send(message)
