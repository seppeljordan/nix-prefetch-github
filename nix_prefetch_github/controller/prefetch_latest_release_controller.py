import argparse
from dataclasses import dataclass
from typing import List

from nix_prefetch_github.cli.arguments import get_options_argument_parser
from nix_prefetch_github.interfaces import GithubRepository
from nix_prefetch_github.logging import LoggerManager
from nix_prefetch_github.use_cases.prefetch_latest_release import (
    PrefetchLatestReleaseUseCase,
    Request,
)


@dataclass
class PrefetchLatestReleaseController:
    use_case: PrefetchLatestReleaseUseCase
    logger_manager: LoggerManager

    def process_arguments(self, arguments: List[str]) -> None:
        parser = argparse.ArgumentParser(
            "nix-prefetch-github-latest-release",
            parents=[get_options_argument_parser()],
        )
        parser.add_argument("owner")
        parser.add_argument("repo")
        args = parser.parse_args(arguments)
        self.logger_manager.set_logging_configuration(args.logging_configuration)
        self.use_case.prefetch_latest_release(
            request=Request(
                repository=GithubRepository(owner=args.owner, name=args.repo),
                prefetch_options=args.prefetch_options,
                rendering_format=args.rendering_format,
            )
        )
