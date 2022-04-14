from dataclasses import dataclass
from sys import exit

from ..interfaces import (
    GithubAPI,
    GithubRepository,
    Prefetcher,
    PrefetchOptions,
    Presenter,
    RenderingFormat,
)


@dataclass
class Request:
    repository: GithubRepository
    prefetch_options: PrefetchOptions
    rendering_format: RenderingFormat


@dataclass
class PrefetchLatestReleaseUseCase:
    nix_presenter: Presenter
    json_presenter: Presenter
    prefetcher: Prefetcher
    github_api: GithubAPI

    def prefetch_latest_release(self, request: Request) -> None:
        revision = self.github_api.get_tag_of_latest_release(request.repository)
        prefetch_result = self.prefetcher.prefetch_github(
            repository=request.repository,
            rev=revision,
            prefetch_options=request.prefetch_options,
        )
        if request.rendering_format == RenderingFormat.json:
            exit(self.json_presenter.present(prefetch_result))
        else:
            exit(self.nix_presenter.present(prefetch_result))
