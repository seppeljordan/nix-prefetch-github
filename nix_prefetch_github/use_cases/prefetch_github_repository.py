from dataclasses import dataclass
from sys import exit
from typing import Optional

from ..interfaces import GithubRepository, Prefetcher, PrefetchOptions, Presenter


@dataclass
class Request:
    repository: GithubRepository
    revision: Optional[str]
    prefetch_options: PrefetchOptions


@dataclass
class PrefetchGithubRepositoryUseCase:
    presenter: Presenter
    prefetcher: Prefetcher

    def prefetch_github_repository(self, request: Request) -> None:
        prefetch_result = self.prefetcher.prefetch_github(
            repository=request.repository,
            rev=request.revision,
            prefetch_options=request.prefetch_options,
        )
        exit(self.presenter.present(prefetch_result))
