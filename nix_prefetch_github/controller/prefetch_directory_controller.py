import argparse
from dataclasses import dataclass
from typing import List, Protocol

from nix_prefetch_github.controller.arguments import get_options_argument_parser
from nix_prefetch_github.logging import LoggerManager
from nix_prefetch_github.use_cases.prefetch_directory import (
    PrefetchDirectoryUseCase,
    Request,
)


class ProcessEnvironment(Protocol):
    def get_cwd(self) -> str:
        ...


@dataclass
class PrefetchDirectoryController:
    logger_manager: LoggerManager
    use_case: PrefetchDirectoryUseCase
    environment: ProcessEnvironment

    def process_arguments(self, arguments: List[str]) -> None:
        parser = argparse.ArgumentParser(parents=[get_options_argument_parser()])
        parser.add_argument("--directory", default=None)
        parser.add_argument("--remote", default="origin")
        args = parser.parse_args(arguments)
        self.logger_manager.set_logging_configuration(
            configuration=args.logging_configuration
        )
        self.use_case.prefetch_directory(
            request=Request(
                prefetch_options=args.prefetch_options,
                rendering_format=args.rendering_format,
                directory=args.directory
                if args.directory
                else self.environment.get_cwd(),
                remote=args.remote,
            )
        )
