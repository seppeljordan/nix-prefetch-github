from typing import Optional

from nix_prefetch_github import GithubRepository, PrefetchOptions


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
