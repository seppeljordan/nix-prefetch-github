import logging
from io import StringIO
from unittest import TestCase

from nix_prefetch_github.command.command_runner import CommandRunnerImpl


class CommandRunnerTests(TestCase):
    def setUp(self) -> None:
        self.stream = StringIO()
        self.handler = logging.StreamHandler(self.stream)
        self.log = logging.getLogger("mylogger")
        self.log.setLevel(logging.DEBUG)
        for handler in self.log.handlers:
            self.log.removeHandler(handler)
        self.log.addHandler(self.handler)
        self.command_runner = CommandRunnerImpl(
            logger=self.log,
        )

    def test_that_for_command_without_stderr_output_only_command_call_is_logged(
        self,
    ) -> None:
        self.command_runner.run_command(
            command=["python", "-c", "print('test' 'string')"]
        )
        self.assertNotInLogs("teststring")

    def test_that_for_command_with_stderr_output_also_the_command_output_is_logged(
        self,
    ) -> None:
        self.command_runner.run_command(
            command=[
                "python",
                "-c",
                "import sys; print('test' 'string', file=sys.stderr)",
            ]
        )
        self.assertInLogs("teststring")

    def test_that_stdout_is_logged_if_it_is_merged_with_stderr(
        self,
    ) -> None:
        self.command_runner.run_command(
            command=[
                "python",
                "-c",
                "print('test' 'string')",
            ],
            merge_stderr=True,
        )
        self.assertInLogs("teststring")

    def test_that_empty_string_is_not_logged_if_no_stderr_is_produced(self) -> None:
        self.command_runner.run_command(
            command=[
                "python",
                "-c",
                "print('test' 'string')",
            ],
        )
        self.assertNotInLogs("\n\n")

    def test_that_empty_string_is_not_logged_if_no_stderr_is_produced_and_stdout_is_merged(
        self,
    ) -> None:
        self.command_runner.run_command(
            command=[
                "python",
                "-c",
                "pass",
            ],
            merge_stderr=True,
        )
        self.assertNotInLogs("\n\n")

    def assertInLogs(self, log_output: str) -> None:
        self.stream.seek(0)
        output = self.stream.read()
        self.assertIn(log_output, output)

    def assertNotInLogs(self, log_output: str) -> None:
        self.stream.seek(0)
        output = self.stream.read()
        self.assertNotIn(log_output, output)
