from __future__ import annotations

from dataclasses import dataclass
from logging import Logger
from typing import Protocol

from nix_prefetch_github.interfaces import (
    Prefetcher,
    PrefetchOptions,
    Presenter,
    RepositoryDetector,
)


class PrefetchDirectoryUseCase(Protocol):
    def prefetch_directory(self, request: Request) -> None:
        ...


@dataclass
class Request:
    prefetch_options: PrefetchOptions
    directory: str
    remote: str


@dataclass
class PrefetchDirectoryUseCaseImpl:
    presenter: Presenter
    prefetcher: Prefetcher
    repository_detector: RepositoryDetector
    logger: Logger

    def prefetch_directory(self, request: Request) -> None:
        if self.repository_detector.is_repository_dirty(request.directory):
            self.logger.warning(f"Git repository at `{request.directory}` is dirty")
        repository = self.repository_detector.detect_github_repository(
            request.directory, remote_name=request.remote
        )
        revision = self.repository_detector.get_current_revision(request.directory)
        assert repository
        prefetch_result = self.prefetcher.prefetch_github(
            repository=repository,
            rev=revision,
            prefetch_options=request.prefetch_options,
        )
        self.presenter.present(prefetch_result)
