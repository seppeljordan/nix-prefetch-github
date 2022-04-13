import argparse
import sys
from typing import List, Optional

from nix_prefetch_github.repository import GithubRepository

from ..dependency_injector import DependencyInjector
from .arguments import get_options_argument_parser


def main(args: Optional[List[str]] = None) -> None:
    arguments = parse_arguments(args)
    injector = DependencyInjector(
        logging_configuration=arguments.logging_configuration,
        rendering_format=arguments.rendering_format,
    )
    presenter = injector.get_presenter()
    repository = GithubRepository(owner=arguments.owner, name=arguments.repo)
    prefetch_options = arguments.prefetch_options
    github_api = injector.get_github_api()
    prefetcher = injector.get_prefetcher()
    prefetched_repository = prefetcher.prefetch_github(
        repository,
        rev=github_api.get_tag_of_latest_release(repository),
        prefetch_options=prefetch_options,
    )
    sys.exit(presenter.present(prefetched_repository))


def parse_arguments(arguments: Optional[List[str]]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "nix-prefetch-github-latest-release", parents=[get_options_argument_parser()]
    )
    parser.add_argument("owner")
    parser.add_argument("repo")
    parser.add_argument("--version", "-V", action="store_true")
    return parser.parse_args(arguments)


if __name__ == "__main__":
    main()
