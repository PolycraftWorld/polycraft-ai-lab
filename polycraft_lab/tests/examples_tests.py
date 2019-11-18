from unittest import TestCase, TestSuite, TextTestRunner

from polycraft_lab.examples.pogo_stick import main


class PogoStickEnvTest(TestCase):
    """A test for the Pogo Stick domain."""

    def setUp(self) -> None:
        # TODO: Mock the pip installation
        pass

    def tearDown(self) -> None:
        # TODO: Mock pip uninstallation
        pass

    @staticmethod
    def test_pogo_stick_challenge():
        main()


if __name__ == '__main__':
    suite = TestSuite()
    suite.addTest(PogoStickEnvTest())
    runner = TextTestRunner()
    runner.run(suite)
