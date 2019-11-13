import unittest

from polycraft_lab.installation.download import download_polycraft
from polycraft_lab.tests import POLYCRAFT_TESTS_DIR


class DownloadModTestCase(unittest.TestCase):
    """Verify all download functions work correctly."""

    DOWNLOAD_DIRECTORY = POLYCRAFT_TESTS_DIR / 'polycraftworld-mod'

    INSTALLATION_DIRECTORY = POLYCRAFT_TESTS_DIR / 'polycraftworld-mod'

    def test_mod_download(self):
        download_polycraft(self.DOWNLOAD_DIRECTORY)
        # Check if downloads directory contains files

    def fail_download(self):
        """TODO: Test a network failure when downloading"""


if __name__ == '__main__':
    unittest.main()
