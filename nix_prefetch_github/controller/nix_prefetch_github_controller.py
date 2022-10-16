import argparse
from typing import List

from nix_prefetch_github.controller.arguments import get_options_argument_parser
from nix_prefetch_github.interfaces import GithubRepository, RenderingFormatSelector
from nix_prefetch_github.logging import LoggerManager
from nix_prefetch_github.use_cases.prefetch_github_repository import (
    PrefetchGithubRepositoryUseCase,
    Request,
)


class NixPrefetchGithubController:
    def __init__(
        self,
        use_case: PrefetchGithubRepositoryUseCase,
        logger_manager: LoggerManager,
        rendering_format_selector: RenderingFormatSelector,
    ) -> None:
        self._use_case = use_case
        self._logger_manager = logger_manager
        self._rendering_format_selector = rendering_format_selector

    def process_arguments(self, arguments: List[str]) -> None:
        parser = get_argument_parser()
        args = parser.parse_args(arguments)
        self._logger_manager.set_logging_configuration(args.logging_configuration)
        self._rendering_format_selector.set_rendering_format(args.rendering_format)
        self._use_case.prefetch_github_repository(
            request=Request(
                repository=GithubRepository(owner=args.owner, name=args.repo),
                revision=args.rev,
                prefetch_options=args.prefetch_options,
            )
        )


# Unfortunately this needs to be a free standing function so that
# sphinx-argparse can generate documentation for it.
def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        "nix-prefetch-github", parents=[get_options_argument_parser()]
    )
    parser.add_argument("owner")
    parser.add_argument("repo")
    parser.add_argument("--rev", default=None)
    return parser
