from io import StringIO
from logging import ERROR
from unittest import TestCase

from .logging import LoggingConfiguration, get_logger


class GetLoggerTests(TestCase):
    def setUp(self) -> None:
        self.output_handle = StringIO()

    def test_can_specify_file_to_log_to(self) -> None:
        logger = get_logger(LoggingConfiguration(output_file=self.output_handle))
        logger.error("test output")
        self.assertLogged("test output")

    def test_by_default_log_warning_level(self) -> None:
        logger = get_logger(LoggingConfiguration(output_file=self.output_handle))
        logger.warning("test output")
        self.assertLogged("test output")

    def test_can_specify_log_level_via_configuration(self) -> None:
        logger = get_logger(
            LoggingConfiguration(output_file=self.output_handle, log_level=ERROR)
        )
        logger.warning("test output")
        self.assertNotLogged("test output")

    def assertLogged(self, message: str) -> None:
        self.output_handle.seek(0)
        self.assertIn(message, self.output_handle.read())

    def assertNotLogged(self, message: str) -> None:
        self.output_handle.seek(0)
        self.assertNotIn(message, self.output_handle.read())
