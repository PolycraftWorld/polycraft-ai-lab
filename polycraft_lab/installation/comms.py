import json
import logging
import socket
import time
from typing import Callable

log = logging.getLogger('pal').getChild('client').getChild('comms')

DEFAULT_PORT = 9000
DEFAULT_HOST = '127.0.0.1'
DEFAULT_BUFF_SIZE = 4096  # 4 KiB


class PolycraftBridge:
    """A communication channel to a Polycraft game"""

    def __init__(self, host: str, port: int,
                 message_callback: Callable[[str], None],
                 buffer_size: int = DEFAULT_BUFF_SIZE):
        """

        Args:
            host:
            port:
            message_callback: A function that receives results from commands
            buffer_size:
        """
        self._host = host
        self._port = port
        self._callback = message_callback
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._buffer_size = buffer_size
        self._should_disconnect = False

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def start(self):
        time.sleep(30)  # TODO: Maybe not delay this?
        self._attempt_connection()

    def _attempt_connection(self, max_attempts: int = 4):
        """Start the Polycraft Lab to Polycraft World communication bridge.

        Note: This will crash if Polycraft World is not running.
        TODO: Fail more softly.
        """
        log.info('Waiting for client to start')
        backoff = 15  # seconds
        for attempt in range(max_attempts):
            try:
                self._socket.connect((self._host, self._port))
                # TODO: Pipe output to a stream
                print('Game client connected.')
                log.debug('Game client connected.')
                return
            except ConnectionRefusedError:
                log.debug(f'Attempt {attempt} to start server failed')
                log.debug(f'Waiting {backoff} seconds before trying again')
                time.sleep(backoff)
                backoff *= 2  # Exponential backoff
        raise ClientDidNotStartError

    def disconnect(self):
        log.info('Shutting down communication with game')
        self._socket.close()
        log.debug('Socket closed')

    def send(self, command: str):
        """Send commands to Minecraft."""

        log.debug(f'Sending command {command}')
        self._socket.send(str.encode(command + '\n'))

        data = b''
        while True:
            part = self._socket.recv(self._buffer_size)
            data += part
            time.sleep(0.001)
            if len(part) < self._buffer_size:
                # either 0 or end of data
                break
        log.debug('Received data:\n' + str(data))
        data_dict = json.loads(data)
        if self._callback is not None:
            self._callback(str(data))
        return data_dict


class ClientDidNotStartError(ConnectionRefusedError):
    """Raised when the client did not start in time to connect."""

    # TODO: Add time waited and number of attempts to message

    def __init__(self, **kwargs):
        super(ClientDidNotStartError, self).__init__(kwargs)
