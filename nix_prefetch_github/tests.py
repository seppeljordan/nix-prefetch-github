import os
import unittest
from typing import Dict, Optional, Set

from .core import GithubRepository, ListRemote, PrefetchOptions


def get_disabled_tests() -> Set[str]:
    return set(os.getenv("DISABLED_TESTS", "").split())


disabled_tests = get_disabled_tests()


requires_nix_build = unittest.skipIf(
    "requires_nix_build" in disabled_tests, "disabled via configuration"
)
network = unittest.skipIf("network" in disabled_tests, "disabled via configuration")


class FakeUrlHasher:
    def __init__(self) -> None:
        self.default_hash = "TEST_ACTUALHASH"

    def calculate_sha256_sum(
        self,
        repository: GithubRepository,
        revision: str,
        prefetch_options: PrefetchOptions,
    ) -> Optional[str]:
        return self.default_hash


class FakeListRemoteFactory:
    def __init__(self) -> None:
        self._remotes: Dict[GithubRepository, ListRemote] = dict()

    def get_remote_list(self, repository: GithubRepository) -> Optional[ListRemote]:
        return self._remotes.get(repository)

    def __setitem__(self, key: GithubRepository, value: ListRemote) -> None:
        self._remotes[key] = value
