from logging import getLogger
from unittest import TestCase

from .command import CommandRunner
from .command_availability_checker import CommandAvailabilityCheckerImpl


class Tests(TestCase):
    def setUp(self) -> None:
        self.command_availability_checker = CommandAvailabilityCheckerImpl(
            command_runner=CommandRunner(getLogger())
        )

    def test_that_fantasy_command_is_not_available(self) -> None:
        self.assertFalse(
            self.command_availability_checker.is_command_available("apwqerasmdf"),
        )

    def test_that_python_command_is_available(self) -> None:
        self.assertTrue(
            self.command_availability_checker.is_command_available("python"),
        )
