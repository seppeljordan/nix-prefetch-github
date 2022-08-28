from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from nix_prefetch_github.interfaces import (
    Alerter,
    GithubRepository,
    Prefetcher,
    PrefetchOptions,
    Presenter,
    RenderingFormat,
)


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
        if not request.prefetch_options.is_safe():
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
