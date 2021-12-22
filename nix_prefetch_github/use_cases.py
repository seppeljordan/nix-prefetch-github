import enum
from dataclasses import dataclass
from typing import Union

from .interfaces import (
    PrefetchedRepository,
    Prefetcher,
    PrefetchOptions,
    PrefetchResult,
    RepositoryDetector,
)


class RepositoryDetectionFailure(enum.Enum):
    unabled_to_detect_github_repository = enum.auto()


PrefetchLocalRepositoryResult = Union[PrefetchResult, RepositoryDetectionFailure]


@dataclass
class PrefetchLocalRepositoryUseCase:
    repository_detector: RepositoryDetector
    prefetcher: Prefetcher

    def prefetch_local_repository(
        self, directory: str, prefetch_options: PrefetchOptions
    ) -> PrefetchLocalRepositoryResult:
        repository = self.repository_detector.detect_github_repository(directory, None)
        if repository is None:
            return RepositoryDetectionFailure.unabled_to_detect_github_repository
        return PrefetchedRepository(
            repository=repository,
            rev="",
            sha256="",
            fetch_submodules=True,
        )
