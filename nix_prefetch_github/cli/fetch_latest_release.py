import argparse
import sys
from typing import List, Optional

from nix_prefetch_github.repository import GithubRepository

from .. import presenter
from ..dependency_injector import DependencyInjector
from ..interfaces import PrefetchedRepository
from .arguments import get_options_argument_parser


def main(args: Optional[List[str]] = None) -> None:
    injector = DependencyInjector()
    arguments = parse_arguments(args)
    repository = GithubRepository(owner=arguments.owner, name=arguments.repo)
    prefetch_options = arguments.prefetch_options
    github_api = injector.get_github_api()
    prefetcher = injector.get_prefetcher()
    prefetched_repository = prefetcher.prefetch_github(
        repository,
        rev=github_api.get_tag_of_latest_release(repository),
        prefetch_options=prefetch_options,
    )
    if isinstance(prefetched_repository, PrefetchedRepository):
        if arguments.nix:
            print(presenter.to_nix_expression(prefetched_repository, prefetch_options))
        else:
            print(presenter.to_json_string(prefetched_repository, prefetch_options))
    else:
        print(presenter.render_prefetch_failure(prefetched_repository), file=sys.stderr)
        sys.exit(1)


def parse_arguments(arguments: Optional[List[str]]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "nix-prefetch-github", parents=[get_options_argument_parser()]
    )
    parser.add_argument("owner")
    parser.add_argument("repo")
    parser.add_argument("--nix", default=False, action="store_true")
    parser.add_argument("--json", dest="nix", action="store_false")
    parser.add_argument("--version", "-V", action="store_true")
    return parser.parse_args(arguments)


if __name__ == "__main__":
    main()
