import argparse
from typing import List, Optional

from ..dependency_injector import DependencyInjector
from ..interfaces import GithubRepository
from ..use_cases.prefetch_github_repository import Request
from .arguments import get_options_argument_parser

PREFETCH_DEFAULT = True
NIX_DEFAULT = False
FETCH_SUBMODULES_DEFAULT = True
REV_DEFAULT = None


def main(argv: Optional[List[str]] = None) -> None:
    arguments = parse_arguments(argv)
    injector = DependencyInjector(
        logging_configuration=arguments.logging_configuration,
        rendering_format=arguments.rendering_format,
    )
    use_case = injector.get_prefetch_github_repository_use_case()
    prefetch_options = arguments.prefetch_options
    use_case.prefetch_github_repository(
        request=Request(
            repository=GithubRepository(arguments.owner, arguments.repo),
            revision=arguments.rev,
            prefetch_options=prefetch_options,
            rendering_format=arguments.rendering_format,
        )
    )


def parse_arguments(arguments: Optional[List[str]]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "nix-prefetch-github", parents=[get_options_argument_parser()]
    )
    parser.add_argument("owner")
    parser.add_argument("repo")
    parser.add_argument("--rev", default=REV_DEFAULT)
    return parser.parse_args(arguments)


if __name__ == "__main__":
    main()
