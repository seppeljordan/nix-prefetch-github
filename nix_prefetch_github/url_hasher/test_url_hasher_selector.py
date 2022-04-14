from logging import getLogger
from typing import Set
from unittest import TestCase

from nix_prefetch_github.command.command_runner import CommandRunnerImpl

from .nix_build import NixBuildUrlHasherImpl
from .nix_prefetch import NixPrefetchUrlHasherImpl
from .url_hasher_selector import UrlHasherSelector


class NixPrefetchUrlAndGitAvailableTests(TestCase):
    def setUp(self) -> None:
        self.logger = getLogger()
        self.command_runner = CommandRunnerImpl(self.logger)
        self.nix_build_implementation = NixBuildUrlHasherImpl(
            command_runner=self.command_runner,
            logger=self.logger,
        )
        self.nix_prefetch_implementation = NixPrefetchUrlHasherImpl(
            command_runner=self.command_runner,
            logger=self.logger,
        )
        self.availability_checker = FakeCommandAvailabilityChecker()
        self.selector = UrlHasherSelector(
            availability_checker=self.availability_checker,
            nix_build_implementation=self.nix_build_implementation,
            nix_prefetch_implementation=self.nix_prefetch_implementation,
        )
        self.availability_checker.set_as_available("nix-prefetch-url")
        self.availability_checker.set_as_available("nix-prefetch-git")

    def test_that_prefetch_hasher_is_available(self) -> None:
        hasher = self.selector.get_url_hasher()
        self.assertIsInstance(hasher, NixPrefetchUrlHasherImpl)


class NixPrefetchUrlAndGitUnavailableTests(TestCase):
    def setUp(self) -> None:
        self.logger = getLogger()
        self.command_runner = CommandRunnerImpl(self.logger)
        self.nix_build_implementation = NixBuildUrlHasherImpl(
            command_runner=self.command_runner,
            logger=self.logger,
        )
        self.nix_prefetch_implementation = NixPrefetchUrlHasherImpl(
            command_runner=self.command_runner,
            logger=self.logger,
        )
        self.availability_checker = FakeCommandAvailabilityChecker()
        self.selector = UrlHasherSelector(
            availability_checker=self.availability_checker,
            nix_build_implementation=self.nix_build_implementation,
            nix_prefetch_implementation=self.nix_prefetch_implementation,
        )
        self.availability_checker.set_as_unavailable("nix-prefetch-url")
        self.availability_checker.set_as_unavailable("nix-prefetch-git")

        self.availability_checker.set_as_available("nix-build")

    def test_that_prefetch_hasher_is_available(self) -> None:
        hasher = self.selector.get_url_hasher()
        self.assertIsInstance(hasher, NixBuildUrlHasherImpl)


class NixPrefetchUrlIsAvailableAndNixPrefetchGitUnavailableTests(TestCase):
    def setUp(self) -> None:
        self.logger = getLogger()
        self.command_runner = CommandRunnerImpl(self.logger)
        self.nix_build_implementation = NixBuildUrlHasherImpl(
            command_runner=self.command_runner,
            logger=self.logger,
        )
        self.nix_prefetch_implementation = NixPrefetchUrlHasherImpl(
            command_runner=self.command_runner,
            logger=self.logger,
        )
        self.availability_checker = FakeCommandAvailabilityChecker()
        self.selector = UrlHasherSelector(
            availability_checker=self.availability_checker,
            nix_build_implementation=self.nix_build_implementation,
            nix_prefetch_implementation=self.nix_prefetch_implementation,
        )
        self.availability_checker.set_as_unavailable("nix-prefetch-git")

        self.availability_checker.set_as_available("nix-prefetch-url")
        self.availability_checker.set_as_available("nix-build")

    def test_that_prefetch_hasher_is_available(self) -> None:
        hasher = self.selector.get_url_hasher()
        self.assertIsInstance(hasher, NixBuildUrlHasherImpl)


class FakeCommandAvailabilityChecker:
    def __init__(self) -> None:
        self.available_commands: Set[str] = set()

    def set_as_available(self, command: str) -> None:
        self.available_commands.add(command)

    def set_as_unavailable(self, command: str) -> None:
        self.available_commands.discard(command)

    def is_command_available(self, command: str) -> bool:
        return command in self.available_commands
