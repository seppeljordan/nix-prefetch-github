import json
from dataclasses import dataclass
from typing import TextIO

from nix_prefetch_github.interfaces import (
    PrefetchFailure,
    PrefetchResult,
    RepositoryRenderer,
)
from nix_prefetch_github.prefetch import PrefetchedRepository
from nix_prefetch_github.templates import output_template


class NixRepositoryRenderer:
    def render_prefetched_repository(self, repository: PrefetchedRepository) -> str:
        return output_template(
            owner=repository.repository.owner,
            repo=repository.repository.name,
            rev=repository.rev,
            sha256=repository.sha256,
            fetch_submodules=repository.options.fetch_submodules,
            leave_dot_git=repository.options.leave_dot_git,
            deep_clone=repository.options.deep_clone,
        )


class JsonRepositoryRenderer:
    def render_prefetched_repository(self, repository: PrefetchedRepository) -> str:
        return json.dumps(
            {
                "owner": repository.repository.owner,
                "repo": repository.repository.name,
                "rev": repository.rev,
                "sha256": repository.sha256,
                "fetchSubmodules": repository.options.fetch_submodules,
                "leaveDotGit": repository.options.leave_dot_git,
                "deepClone": repository.options.deep_clone,
            },
            indent=4,
        )


@dataclass
class PresenterImpl:
    result_output: TextIO
    error_output: TextIO
    repository_renderer: RepositoryRenderer

    def present(self, prefetch_result: PrefetchResult) -> int:
        if isinstance(prefetch_result, PrefetchedRepository):
            self.result_output.write(
                self.repository_renderer.render_prefetched_repository(prefetch_result)
            )
            return 0
        elif isinstance(prefetch_result, PrefetchFailure):
            self.error_output.write(self.render_prefetch_failure(prefetch_result))
            return 1
        else:
            raise Exception(f"Renderer received unexpected value {prefetch_result}")

    def render_prefetch_failure(self, failure: PrefetchFailure) -> str:
        return "Prefetch failed: " + str(failure.reason)
