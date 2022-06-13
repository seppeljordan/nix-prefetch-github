import argparse
from typing import List

from nix_prefetch_github.controller.arguments import get_options_argument_parser
from nix_prefetch_github.interfaces import GithubRepository
from nix_prefetch_github.logging import LoggerManager
from nix_prefetch_github.use_cases.prefetch_github_repository import (
    PrefetchGithubRepositoryUseCase,
    Request,
)


class NixPrefetchGithubController:
    def __init__(
        self, use_case: PrefetchGithubRepositoryUseCase, logger_manager: LoggerManager
    ) -> None:
        self._use_case = use_case
        self._logger_manager = logger_manager

    def process_arguments(self, arguments: List[str]) -> None:
        parser = argparse.ArgumentParser(
            "nix-prefetch-github", parents=[get_options_argument_parser()]
        )
        parser.add_argument("owner")
        parser.add_argument("repo")
        parser.add_argument("--rev", default=None)
        args = parser.parse_args(arguments)
        self._logger_manager.set_logging_configuration(args.logging_configuration)
        self._use_case.prefetch_github_repository(
            request=Request(
                repository=GithubRepository(owner=args.owner, name=args.repo),
                revision=args.rev,
                prefetch_options=args.prefetch_options,
                rendering_format=args.rendering_format,
            )
        )
