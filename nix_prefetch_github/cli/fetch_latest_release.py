import argparse
from typing import List, Optional

from nix_prefetch_github.cli.arguments import get_options_argument_parser
from nix_prefetch_github.dependency_injector import DependencyInjector
from nix_prefetch_github.interfaces import GithubRepository
from nix_prefetch_github.use_cases.prefetch_latest_release import Request


def main(args: Optional[List[str]] = None) -> None:
    arguments = parse_arguments(args)
    injector = DependencyInjector(
        logging_configuration=arguments.logging_configuration,
        rendering_format=arguments.rendering_format,
    )
    use_case = injector.get_prefetch_latest_release_use_case()
    use_case.prefetch_latest_release(
        request=Request(
            repository=GithubRepository(owner=arguments.owner, name=arguments.repo),
            prefetch_options=arguments.prefetch_options,
            rendering_format=arguments.rendering_format,
        )
    )


def parse_arguments(arguments: Optional[List[str]]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "nix-prefetch-github-latest-release", parents=[get_options_argument_parser()]
    )
    parser.add_argument("owner")
    parser.add_argument("repo")
    return parser.parse_args(arguments)


if __name__ == "__main__":
    main()
