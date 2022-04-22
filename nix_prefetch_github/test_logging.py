from io import StringIO
from logging import ERROR, WARNING
from unittest import TestCase

from nix_prefetch_github.logging import LoggerFactoryImpl, LoggingConfiguration


class LoggerFactoryTests(TestCase):
    def setUp(self) -> None:
        self.output_handle = StringIO()
        self.factory = LoggerFactoryImpl()

    def test_can_specify_file_to_log_to(self) -> None:
        self.factory.set_logging_configuration(
            LoggingConfiguration(output_file=self.output_handle)
        )
        logger = self.factory.get_logger()
        logger.error("test output")
        self.assertLogged("test output")

    def test_by_default_log_warning_level(self) -> None:
        self.factory.set_logging_configuration(
            LoggingConfiguration(output_file=self.output_handle)
        )
        logger = self.factory.get_logger()
        logger.warning("test output")
        self.assertLogged("test output")

    def test_can_specify_log_level_via_configuration(self) -> None:
        self.factory.set_logging_configuration(
            LoggingConfiguration(output_file=self.output_handle, log_level=ERROR)
        )
        logger = self.factory.get_logger()
        logger.warning("test output")
        self.assertNotLogged("test output")

    def test_can_get_logger_without_specifying_configuration(self) -> None:
        self.factory.get_logger()

    def test_default_logging_configuration_is_respected_for_newly_constructed_loggers(
        self,
    ) -> None:
        self.factory.set_logging_configuration(
            LoggingConfiguration(
                output_file=self.output_handle,
                log_level=WARNING,
            )
        )
        logger = self.factory.get_logger()
        logger.warning("test message")
        self.assertLogged("test message")

    def assertLogged(self, message: str) -> None:
        self.output_handle.seek(0)
        self.assertIn(message, self.output_handle.read())

    def assertNotLogged(self, message: str) -> None:
        self.output_handle.seek(0)
        self.assertNotIn(message, self.output_handle.read())
