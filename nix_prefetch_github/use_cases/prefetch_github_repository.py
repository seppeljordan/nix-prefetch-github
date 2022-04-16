from dataclasses import dataclass
from sys import exit
from typing import Optional

from nix_prefetch_github.interfaces import (
    GithubRepository,
    Prefetcher,
    PrefetchOptions,
    Presenter,
    RenderingFormat,
)


@dataclass
class Request:
    repository: GithubRepository
    revision: Optional[str]
    prefetch_options: PrefetchOptions
    rendering_format: RenderingFormat


@dataclass
class PrefetchGithubRepositoryUseCase:
    nix_presenter: Presenter
    json_presenter: Presenter
    prefetcher: Prefetcher

    def prefetch_github_repository(self, request: Request) -> None:
        prefetch_result = self.prefetcher.prefetch_github(
            repository=request.repository,
            rev=request.revision,
            prefetch_options=request.prefetch_options,
        )
        if request.rendering_format == RenderingFormat.json:
            exit(self.json_presenter.present(prefetch_result))
        else:
            exit(self.nix_presenter.present(prefetch_result))
