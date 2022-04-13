from dataclasses import dataclass
from typing import Protocol

from nix_prefetch_github.interfaces import UrlHasher

from .nix_build import NixBuildUrlHasherImpl
from .nix_prefetch import NixPrefetchUrlHasherImpl


class CommandAvailabilityChecker(Protocol):
    def is_command_available(self, command: str) -> bool:
        ...


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
