from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from nix_prefetch_github.interfaces import (
    GithubRepository,
    Prefetcher,
    PrefetchOptions,
    Presenter,
    RenderingFormat,
)


class Alerter(Protocol):
    def alert_user_about_unsafe_prefetch_options(
        self, prefetch_options: PrefetchOptions
    ) -> None:
        ...


class PrefetchGithubRepositoryUseCase(Protocol):
    def prefetch_github_repository(self, request: Request) -> None:
        ...


@dataclass
class Request:
    repository: GithubRepository
    revision: Optional[str]
    prefetch_options: PrefetchOptions
    rendering_format: RenderingFormat


@dataclass
class PrefetchGithubRepositoryUseCaseImpl:
    nix_presenter: Presenter
    json_presenter: Presenter
    prefetcher: Prefetcher
    alerter: Alerter

    def prefetch_github_repository(self, request: Request) -> None:
        if (
            request.prefetch_options.leave_dot_git
            or request.prefetch_options.deep_clone
        ):
            self.alerter.alert_user_about_unsafe_prefetch_options(
                request.prefetch_options
            )
        prefetch_result = self.prefetcher.prefetch_github(
            repository=request.repository,
            rev=request.revision,
            prefetch_options=request.prefetch_options,
        )
        if request.rendering_format == RenderingFormat.json:
            self.json_presenter.present(prefetch_result)
        else:
            self.nix_presenter.present(prefetch_result)
