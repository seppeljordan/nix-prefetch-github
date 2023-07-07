from dataclasses import dataclass
from typing import Optional

from nix_prefetch_github.interfaces import (
    CommandAvailabilityChecker,
    GithubRepository,
    PrefetchOptions,
    UrlHasher,
)


@dataclass
class UrlHasherSelector:
    availability_checker: CommandAvailabilityChecker
    nix_build_implementation: UrlHasher
    nix_prefetch_implementation: UrlHasher

    def _get_url_hasher(self, prefetch_options: PrefetchOptions) -> UrlHasher:
        # There is currently a bug in `nix-prefetch-git` that produces
        # the wrong hash if --deepClone is specified but not
        # --leave-dotGit.  See
        # https://github.com/NixOS/nixpkgs/issues/168147 for details.
        if prefetch_options.deep_clone and not prefetch_options.leave_dot_git:
            return self.nix_build_implementation
        if self.availability_checker.is_command_available(
            "nix-prefetch-url"
        ) and self.availability_checker.is_command_available("nix-prefetch-git"):
            return self.nix_prefetch_implementation
        else:
            return self.nix_build_implementation

    def calculate_hash_sum(
        self,
        repository: GithubRepository,
        revision: str,
        prefetch_options: PrefetchOptions,
    ) -> Optional[str]:
        hasher = self._get_url_hasher(prefetch_options)
        return hasher.calculate_hash_sum(
            repository=repository,
            revision=revision,
            prefetch_options=prefetch_options,
        )
