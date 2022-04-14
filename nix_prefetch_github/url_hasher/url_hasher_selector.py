from dataclasses import dataclass

from nix_prefetch_github.interfaces import CommandAvailabilityChecker, UrlHasher

from .nix_build import NixBuildUrlHasherImpl
from .nix_prefetch import NixPrefetchUrlHasherImpl


@dataclass
class UrlHasherSelector:
    availability_checker: CommandAvailabilityChecker
    nix_build_implementation: NixBuildUrlHasherImpl
    nix_prefetch_implementation: NixPrefetchUrlHasherImpl

    def get_url_hasher(self) -> UrlHasher:
        if self.availability_checker.is_command_available(
            "nix-prefetch-url"
        ) and self.availability_checker.is_command_available("nix-prefetch-git"):
            return self.nix_prefetch_implementation
        else:
            return self.nix_build_implementation
