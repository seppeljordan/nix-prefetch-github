from os import getenv
from typing import Optional
from unittest import skipIf

from .interfaces import PrefetchOptions
from .repository import GithubRepository
from .revision_index import RevisionIndex

_disabled_tests = set(filter(bool, getenv("DISABLED_TESTS", "").split(" ")))
network = skipIf("network" in _disabled_tests, "networking tests are disabled")
requires_nix_build = skipIf(
    "requires_nix_build" in _disabled_tests, "tests requiring nix build are disabled"
)


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
        self.revision_index: Optional[RevisionIndex] = None

    def get_revision_index(
        self, repository: GithubRepository
    ) -> Optional[RevisionIndex]:
        return self.revision_index
