from os import getenv
from typing import Callable, Dict, List, Optional, Tuple
from unittest import TestCase, skipIf

from nix_prefetch_github.interfaces import (
    CommandRunner,
    GithubRepository,
    PrefetchOptions,
    RenderingFormat,
)
from nix_prefetch_github.logging import LoggingConfiguration
from nix_prefetch_github.revision_index import RevisionIndexImpl

_disabled_tests = set(filter(bool, getenv("DISABLED_TESTS", "").split(" ")))
network = skipIf("network" in _disabled_tests, "networking tests are disabled")
requires_nix_build = skipIf(
    "requires_nix_build" in _disabled_tests, "tests requiring nix build are disabled"
)


class BaseTestCase(TestCase):
    pass


class FakeUrlHasher:
    def __init__(self) -> None:
        self.sha256_sum: Optional[str] = None

    def calculate_sha256_sum(
        self,
        repository: GithubRepository,
        revision: str,
        prefetch_options: PrefetchOptions,
    ) -> Optional[str]:
        return self.sha256_sum


class FakeRevisionIndexFactory:
    def __init__(self) -> None:
        self.revision_index: Optional[RevisionIndexImpl] = None

    def get_revision_index(
        self, repository: GithubRepository
    ) -> Optional[RevisionIndexImpl]:
        return self.revision_index


class FakeLoggerManager:
    def __init__(self) -> None:
        self.configuration: Optional[LoggingConfiguration] = None

    def set_logging_configuration(self, configuration: LoggingConfiguration) -> None:
        self.configuration = configuration

    def assertLoggingConfiguration(
        self,
        condition: Optional[Callable[[LoggingConfiguration], bool]] = None,
        message: str = "",
    ) -> None:
        assert self.configuration
        if condition:
            assert condition(self.configuration), message


class CommandRunnerTestImpl:
    def __init__(self, command_runner: CommandRunner):
        self.command_runner = command_runner
        self.commands_issued: List[List[str]] = list()

    def run_command(
        self,
        command: List[str],
        cwd: Optional[str] = None,
        environment_variables: Optional[Dict[str, str]] = None,
        merge_stderr: bool = False,
    ) -> Tuple[int, str]:
        self.commands_issued.append(list(command))
        return self.command_runner.run_command(
            command, cwd, environment_variables, merge_stderr
        )


class RenderingFormatSelectorImpl:
    def __init__(self) -> None:
        self.selected_output_format: Optional[RenderingFormat] = None

    def set_rendering_format(self, rendering_format: RenderingFormat) -> None:
        self.selected_output_format = rendering_format
