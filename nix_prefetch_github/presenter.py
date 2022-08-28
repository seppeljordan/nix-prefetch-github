import json
from dataclasses import dataclass
from typing import List, Protocol

from nix_prefetch_github.interfaces import (
    PrefetchFailure,
    PrefetchResult,
    RepositoryRenderer,
)
from nix_prefetch_github.prefetch import PrefetchedRepository
from nix_prefetch_github.templates import output_template


@dataclass
class ViewModel:
    exit_code: int
    stderr_lines: List[str]
    stdout_lines: List[str]


class CommandLineView(Protocol):
    def render_view_model(self, model: ViewModel) -> None:
        ...


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
    view: CommandLineView
    repository_renderer: RepositoryRenderer

    def present(self, prefetch_result: PrefetchResult) -> None:
        stdout_lines: List[str] = []
        stderr_lines: List[str] = []
        return_code: int = 0
        if isinstance(prefetch_result, PrefetchedRepository):
            stdout_lines.append(
                self.repository_renderer.render_prefetched_repository(prefetch_result)
            )
        elif isinstance(prefetch_result, PrefetchFailure):
            stderr_lines.append(self.render_prefetch_failure(prefetch_result))
            return_code = 1
        else:
            raise Exception(f"Renderer received unexpected value {prefetch_result}")
        model = ViewModel(
            exit_code=return_code,
            stderr_lines=stderr_lines,
            stdout_lines=stdout_lines,
        )
        self.view.render_view_model(model)

    def render_prefetch_failure(self, failure: PrefetchFailure) -> str:
        message = (
            f"Prefetch failed: {failure.reason}. {self._explain_error(failure.reason)}"
        )
        return message

    def _explain_error(self, reason: PrefetchFailure.Reason) -> str:
        if reason == PrefetchFailure.Reason.unable_to_locate_revision:
            return "nix-prefetch-github failed to find a matching revision to download from github. Have you spelled the repository owner, repository name and revision name correctly?"
        else:
            return "nix-prefetch-github failed to calculate a sha256 hash for the requested github repository. Do you have nix-prefetch-git, nix-prefetch-url and nix-build in your PATH?"
