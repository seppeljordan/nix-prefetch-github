from dataclasses import dataclass
from typing import List

from nix_prefetch_github.interfaces import (
    CommandLineView,
    PrefetchFailure,
    PrefetchResult,
    RepositoryRenderer,
    ViewModel,
)
from nix_prefetch_github.prefetch import PrefetchedRepository


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
