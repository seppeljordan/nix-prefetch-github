import argparse
import sys
from typing import List, Optional

from . import presenter
from .cli.arguments import get_options_argument_parser
from .dependency_injector import DependencyInjector
from .prefetch import PrefetchedRepository
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
    injector = DependencyInjector()
    prefetcher = injector.get_prefetcher()
    prefetch_options = arguments.prefetch_options
    prefetch_result = prefetcher.prefetch_github(
        GithubRepository(arguments.owner, arguments.repo),
        arguments.rev,
        prefetch_options=prefetch_options,
    )
    if isinstance(prefetch_result, PrefetchedRepository):
        if arguments.nix:
            output_to_user = presenter.to_nix_expression(
                prefetch_result, prefetch_options
            )
        else:
            output_to_user = presenter.to_json_string(prefetch_result, prefetch_options)
        print(output_to_user, end="")
    else:
        print(presenter.render_prefetch_failure(prefetch_result), file=sys.stderr)
        sys.exit(1)


def print_version_info() -> None:
    print(f"nix-prefetch-github {VERSION_STRING}")


def parse_arguments(arguments: Optional[List[str]]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "nix-prefetch-github", parents=[get_options_argument_parser()]
    )
    parser.add_argument("owner")
    parser.add_argument("repo")
    parser.add_argument("--rev", default=REV_DEFAULT)
    parser.add_argument("--nix", default=NIX_DEFAULT, action="store_true")
    parser.add_argument("--json", dest="nix", action="store_false")
    parser.add_argument("--version", "-V", action="store_true")
    return parser.parse_args(arguments)


if __name__ == "__main__":
    main()
