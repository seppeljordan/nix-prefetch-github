import argparse
import os
import sys
from typing import List, Optional

from ..dependency_injector import DependencyInjector
from .arguments import get_options_argument_parser


def main(args: Optional[List[str]] = None) -> None:
    arguments = parser_arguments(args)
    dependency_injector = DependencyInjector(
        logging_configuration=arguments.logging_configuration,
        rendering_format=arguments.rendering_format,
    )
    presenter = dependency_injector.get_presenter()
    logger = dependency_injector.get_logger()
    repository_detector = dependency_injector.get_repository_detector()
    prefetcher = dependency_injector.get_prefetcher()
    directory = arguments.directory or os.getcwd()
    if repository_detector.is_repository_dirty(directory):
        logger.warning(f"Warning: Git repository at `{directory}` is dirty")
    repository = repository_detector.detect_github_repository(
        directory, remote_name=arguments.remote
    )
    assert repository
    revision = repository_detector.get_current_revision(directory)
    prefetch_options = arguments.prefetch_options
    prefetched_repository = prefetcher.prefetch_github(
        repository, revision, prefetch_options
    )
    sys.exit(presenter.present(prefetched_repository))


def parser_arguments(arguments: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(parents=[get_options_argument_parser()])
    parser.add_argument("--directory")
    parser.add_argument("--remote", default="origin")
    return parser.parse_args(arguments)


if __name__ == "__main__":
    main()
