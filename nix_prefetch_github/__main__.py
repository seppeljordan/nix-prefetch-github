import argparse
import sys
from typing import List, Optional

from .cli.arguments import get_options_argument_parser
from .dependency_injector import DependencyInjector
from .repository import GithubRepository
from .version import VERSION_STRING

PREFETCH_DEFAULT = True
NIX_DEFAULT = False
FETCH_SUBMODULES_DEFAULT = True
REV_DEFAULT = None


def main(argv: Optional[List[str]] = None) -> None:
    arguments = parse_arguments(argv)
    if arguments.version:
        print_version_info()
        return None
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


def print_version_info() -> None:
    print(f"nix-prefetch-github {VERSION_STRING}")


def parse_arguments(arguments: Optional[List[str]]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "nix-prefetch-github", parents=[get_options_argument_parser()]
    )
    parser.add_argument("owner")
    parser.add_argument("repo")
    parser.add_argument("--rev", default=REV_DEFAULT)
    parser.add_argument("--version", "-V", action="store_true")
    return parser.parse_args(arguments)


if __name__ == "__main__":
    main()
