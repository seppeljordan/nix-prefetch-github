from typing import Set
from unittest import TestCase

from nix_prefetch_github.interfaces import GithubRepository, PrefetchOptions
from nix_prefetch_github.tests import FakeUrlHasher
from nix_prefetch_github.url_hasher.url_hasher_selector import UrlHasherSelector


class NixPrefetchUrlAndGitAvailableTests(TestCase):
    def setUp(self) -> None:
        self.nix_build_hasher = FakeUrlHasher()
        self.nix_prefetch_hasher = FakeUrlHasher()
        self.availability_checker = FakeCommandAvailabilityChecker()
        self.selector = UrlHasherSelector(
            availability_checker=self.availability_checker,
            nix_build_implementation=self.nix_build_hasher,
            nix_prefetch_implementation=self.nix_prefetch_hasher,
        )
        self.availability_checker.set_as_available("nix-prefetch-url")
        self.availability_checker.set_as_available("nix-prefetch-git")
        self.nix_build_hasher.sha256_sum = "nix build hash"
        self.nix_prefetch_hasher.sha256_sum = "nix prefetch hash"
        self.repository = GithubRepository(owner="test", name="test")
        self.revision = "test"

    def test_that_prefetch_hasher_is_used(self) -> None:
        hash_sum = self.selector.calculate_sha256_sum(
            repository=self.repository,
            revision=self.revision,
            prefetch_options=PrefetchOptions(),
        )
        self.assertEqual(hash_sum, "nix prefetch hash")

    def test_that_nix_build_hasher_is_used_with_deep_clone_and_not_leave_dot_git(
        self,
    ) -> None:
        hash_sum = self.selector.calculate_sha256_sum(
            repository=self.repository,
            revision=self.revision,
            prefetch_options=PrefetchOptions(deep_clone=True, leave_dot_git=False),
        )
        self.assertEqual(hash_sum, "nix build hash")


class NixPrefetchUrlAndGitUnavailableTests(TestCase):
    def setUp(self) -> None:
        self.nix_build_hasher = FakeUrlHasher()
        self.nix_prefetch_hasher = FakeUrlHasher()
        self.availability_checker = FakeCommandAvailabilityChecker()
        self.selector = UrlHasherSelector(
            availability_checker=self.availability_checker,
            nix_build_implementation=self.nix_build_hasher,
            nix_prefetch_implementation=self.nix_prefetch_hasher,
        )
        self.availability_checker.set_as_unavailable("nix-prefetch-url")
        self.availability_checker.set_as_unavailable("nix-prefetch-git")
        self.nix_build_hasher.sha256_sum = "nix build hash"
        self.nix_prefetch_hasher.sha256_sum = "nix prefetch hash"
        self.repository = GithubRepository(owner="test", name="test")
        self.revision = "test"

    def test_that_nix_build_hasher_is_used(self) -> None:
        hash_sum = self.selector.calculate_sha256_sum(
            repository=self.repository,
            revision=self.revision,
            prefetch_options=PrefetchOptions(),
        )
        self.assertEqual(hash_sum, "nix build hash")


class NixPrefetchUrlIsAvailableAndNixPrefetchGitUnavailableTests(TestCase):
    def setUp(self) -> None:
        self.nix_build_hasher = FakeUrlHasher()
        self.nix_prefetch_hasher = FakeUrlHasher()
        self.availability_checker = FakeCommandAvailabilityChecker()
        self.selector = UrlHasherSelector(
            availability_checker=self.availability_checker,
            nix_build_implementation=self.nix_build_hasher,
            nix_prefetch_implementation=self.nix_prefetch_hasher,
        )
        self.availability_checker.set_as_unavailable("nix-prefetch-url")
        self.availability_checker.set_as_available("nix-prefetch-git")
        self.nix_build_hasher.sha256_sum = "nix build hash"
        self.nix_prefetch_hasher.sha256_sum = "nix prefetch hash"
        self.repository = GithubRepository(owner="test", name="test")
        self.revision = "test"

    def test_that_nix_build_hasher_is_used(self) -> None:
        hash_sum = self.selector.calculate_sha256_sum(
            repository=self.repository,
            revision=self.revision,
            prefetch_options=PrefetchOptions(),
        )
        self.assertEqual(hash_sum, "nix build hash")


class FakeCommandAvailabilityChecker:
    def __init__(self) -> None:
        self.available_commands: Set[str] = set()

    def set_as_available(self, command: str) -> None:
        self.available_commands.add(command)

    def set_as_unavailable(self, command: str) -> None:
        self.available_commands.discard(command)

    def is_command_available(self, command: str) -> bool:
        return command in self.available_commands
