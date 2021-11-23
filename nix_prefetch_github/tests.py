import os
import unittest
from typing import Optional, Set

from .core import GithubRepository, PrefetchOptions


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
