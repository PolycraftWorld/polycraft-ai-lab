"""Classes for managing the runtime clients for Polycraft Lab.

The PolycraftClient should be used to manage the currently running Polycraft
installation and send messages/commands to the client.

This includes the PolycraftModRuntime, which handles starting and stopping the
mod, and PolycraftServerBridge, which is responsible for sending commands to the
currently running game.
"""

import json
import logging
import os
import platform
import signal
import socket
import time
from pathlib import Path
from subprocess import PIPE, Popen

from polycraft_lab.installation.config import PolycraftLabConfig
from polycraft_lab.installation.manager import PolycraftInstallation

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 9000

log = logging.getLogger(__name__)


class ClientDidNotStartError(ConnectionRefusedError):
    """Raised when the client did not start in time to connect."""
    # TODO: Add time waited and number of attempts to message


class PolycraftClient:
    """A module that manages a running Polycraft World client."""

    def __init__(self, installation_path: str):
        self.is_running = False
        # TODO: Fetch values from config
        config = PolycraftLabConfig.from_installation(installation_path)
        self.runtime = _PolycraftModRuntime(installation_path)
        self.server = _PolycraftServerBridge(host=config.lab_server_host,
                                             port=config.lab_server_port)

    def start(self):
        self.runtime.start()
        # TODO: Connect ends
        # TODO: Wait until game is started to start socket

        self.server.start()

    def stop(self):
        """Stop the currently running game of Minecraft."""
        self.is_running = False

    def send_to_server(self, message: str):
        """Send a message to the server."""
        self.server.send(message)

    def setup_scene(self, scene: str):
        """Setup a particular domain training environment.

        Args:
            scene (str): The scene to setup.
        """
        self.send_to_server(f'SETUP {scene}')


class _PolycraftModRuntime:
    """A minimal wrapper for starting and stopping the Polycraft Mod."""

    def __init__(self, installation_path):
        self.installation = PolycraftInstallation(installation_path)
        if not self.installation.is_installed:
            raise
        # noinspection PyTypeChecker
        self.client_process: Popen = None

    def stop(self):
        """Stop the running Minecraft instance if it exists."""
        os.killpg(os.getpgid(self.client_process.pid), signal.SIGTERM)

    def start(self):
        """Start running Minecraft."""
        if platform.system() not in ['Windows', 'Linux', 'Darwin']:
            raise Exception('Attempting to start client on an unspported OS.')
        gradlew_name = 'gradlew'
        if platform.system() == 'Windows':
            gradlew_name = 'gradlew.bat'
        executable_base = str(
            Path(self.installation.client_location) / gradlew_name)
        logging.info('Starting Minecraft...')
        logging.info('This may also take a bit.')
        self.client_process = Popen([executable_base, 'runClient'], stdout=PIPE,
                                    shell=True)


class _PolycraftServerBridge:
    """A bridge between the Polycraft mod and this Python wrapper.

    This uses sockets to send commands in Python to trigger specific actions
    in the reinforcement learning training loop.
    """

    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
        self.host = host
        self.port = port
        self._should_stop = False

    def start(self, max_attempts=4):
        """Start the Polycraft Lab to Polycraft World communication bridge.

        Note: This will crash if Polycraft World is not running.
        TODO: Fail more softly.
        """
        log.info('Waiting for client to start')
        backoff = 10  # 10 seconds
        for attempt in range(max_attempts):
            try:
                self._start_server()
                return
            except ConnectionRefusedError:
                log.debug(f'Attempt {attempt} to start server failed')
                time.sleep(backoff)
                backoff *= 2  # Exponential backoff

    def finish(self):
        """Stop the communication bridge.

        This shuts down the internal socket used for communication.
        """
        self._should_stop = True

    def setup_scene(self, scene):
        self.send('RESET ' + scene)

    def send(self, command: str):
        """Send a command to the connected socket."""
        self.api_socket.send(bytes(command))
        self.api_socket.close()

    def _start_server(self):
        self.api_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.api_socket.connect((self.host, self.port))
        while not self._should_stop:
            recieved = self.api_socket.recv(10240).decode()
            data = json.loads(recieved)
            print(data)
        self.api_socket.close()
