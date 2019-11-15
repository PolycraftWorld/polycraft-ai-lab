import socket
import unittest

from polycraft_lab.installation.download import download_and_extract_polycraft
from polycraft_lab.tests import POLYCRAFT_TESTS_DIR


class DownloadModTestCase(unittest.TestCase):
    """Verify all download functions work correctly."""

    DOWNLOAD_DIRECTORY = POLYCRAFT_TESTS_DIR / 'polycraft-download'

    INSTALLATION_DIRECTORY = POLYCRAFT_TESTS_DIR / 'polycraft'

    TEST_REPO_LOCATION = 'https://filebin.net/p5rcppoqfxiipiak/polycraft-1.8.9AIGym.zip?t=01f0elf7'

    def test_mod_download(self):
        """
        Should download Polycraft zip to DOWNLOAD_DIRECTORY and extract files to
        INSTALLATION_DIRECTORY
        """
        download_and_extract_polycraft(self.INSTALLATION_DIRECTORY,
                                       download_directory=self.DOWNLOAD_DIRECTORY,
                                       repo_location=self.TEST_REPO_LOCATION)
        # Check if downloads directory contains files

    def fail_download(self):
        """TODO: Test a network failure when downloading"""
        guard = lambda: exec('raise Exception(\'No network connection\')')
        socket.socket = guard
        with self.assertRaises(Exception) as context:
            download_and_extract_polycraft(self.INSTALLATION_DIRECTORY,
                                           download_directory=self.DOWNLOAD_DIRECTORY)
        self.assertTrue(context.exception)


if __name__ == '__main__':
    unittest.main()
