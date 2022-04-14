import argparse
import os
from typing import List, Optional

from ..dependency_injector import DependencyInjector
from ..use_cases.prefetch_directory import Request
from .arguments import get_options_argument_parser


def main(args: Optional[List[str]] = None) -> None:
    arguments = parser_arguments(args)
    dependency_injector = DependencyInjector(
        logging_configuration=arguments.logging_configuration,
        rendering_format=arguments.rendering_format,
    )
    use_case = dependency_injector.get_prefetch_directory_use_case()
    use_case.prefetch_directory(
        request=Request(
            prefetch_options=arguments.prefetch_options,
            rendering_format=arguments.rendering_format,
            directory=arguments.directory or os.getcwd(),
            remote=arguments.remote,
        )
    )


def parser_arguments(arguments: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(parents=[get_options_argument_parser()])
    parser.add_argument("--directory")
    parser.add_argument("--remote", default="origin")
    return parser.parse_args(arguments)


if __name__ == "__main__":
    main()
