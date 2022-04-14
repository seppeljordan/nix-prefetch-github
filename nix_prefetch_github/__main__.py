import argparse
import sys
from typing import List, Optional

from .cli.arguments import get_options_argument_parser
from .dependency_injector import DependencyInjector
from .repository import GithubRepository

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
    presenter = injector.get_presenter()
    prefetcher = injector.get_prefetcher()
    prefetch_options = arguments.prefetch_options
    prefetch_result = prefetcher.prefetch_github(
        GithubRepository(arguments.owner, arguments.repo),
        arguments.rev,
        prefetch_options=prefetch_options,
    )
    sys.exit(presenter.present(prefetch_result))


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
