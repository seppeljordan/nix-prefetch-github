import argparse
import os
import sys
from typing import List, Optional

from .. import presenter
from ..dependency_injector import DependencyInjector
from ..interfaces import PrefetchedRepository
from .arguments import get_options_argument_parser


def main(args: Optional[List[str]] = None) -> None:
    dependency_injector = DependencyInjector()
    arguments = parser_arguments(args)
    repository_detector = dependency_injector.get_repository_detector()
    prefetcher = dependency_injector.get_prefetcher()
    directory = arguments.directory or os.getcwd()
    if repository_detector.is_repository_dirty(directory):
        print(f"Warning: Git repository at `{directory}` is dirty", file=sys.stderr)
    repository = repository_detector.detect_github_repository(
        directory, remote_name=arguments.remote
    )
    assert repository
    revision = repository_detector.get_current_revision(directory)
    prefetch_options = arguments.prefetch_options
    prefetched_repository = prefetcher.prefetch_github(
        repository, revision, prefetch_options
    )
    if isinstance(prefetched_repository, PrefetchedRepository):
        if arguments.nix:
            print(presenter.to_nix_expression(prefetched_repository, prefetch_options))
        else:
            print(presenter.to_json_string(prefetched_repository, prefetch_options))
    else:
        print(presenter.render_prefetch_failure(prefetched_repository), file=sys.stderr)
        sys.exit(1)


def parser_arguments(arguments: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(parents=[get_options_argument_parser()])
    parser.add_argument("--directory")
    parser.add_argument(
        "--nix",
        action="store_true",
        default=False,
        help="Format output as Nix expression",
    )
    parser.add_argument("--json", dest="nix", action="store_false")
    parser.add_argument("--remote", default="origin")
    return parser.parse_args(arguments)


if __name__ == "__main__":
    main()
