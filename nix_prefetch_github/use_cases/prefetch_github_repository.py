from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from nix_prefetch_github.interfaces import (
    Alerter,
    GithubRepository,
    Prefetcher,
    PrefetchOptions,
    Presenter,
)


class PrefetchGithubRepositoryUseCase(Protocol):
    def prefetch_github_repository(self, request: Request) -> None: ...


@dataclass
class Request:
    repository: GithubRepository
    revision: Optional[str]
    prefetch_options: PrefetchOptions


@dataclass
class PrefetchGithubRepositoryUseCaseImpl:
    presenter: Presenter
    prefetcher: Prefetcher
    alerter: Alerter

    def prefetch_github_repository(self, request: Request) -> None:
        if not request.prefetch_options.is_safe():
            self.alerter.alert_user_about_unsafe_prefetch_options(
                request.prefetch_options
            )
        prefetch_result = self.prefetcher.prefetch_github(
            repository=request.repository,
            rev=request.revision,
            prefetch_options=request.prefetch_options,
        )
        self.presenter.present(prefetch_result)
