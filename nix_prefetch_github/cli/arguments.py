import argparse
import sys
from logging import INFO, WARNING
from typing import Any, Optional, Type

from ..interfaces import PrefetchOptions
from ..logging import LoggingConfiguration
from ..presenter import RenderingFormat


def set_argument(name: str, value: Any) -> Type[argparse.Action]:
    class _SetArgument(argparse.Action):
        def __init__(  # type: ignore
            self,
            option_strings,
            dest,
            nargs=None,
            const=None,
            default=None,
            type=None,
            choices=None,
            required=False,
            help=None,
            metavar=None,
        ) -> None:
            assert nargs is None
            return super().__init__(
                option_strings,
                dest,
                0,
                const,
                default,
                type,
                choices,
                required,
                help,
                metavar,
            )

        def __call__(
            self,
            parser: argparse.ArgumentParser,
            namespace: argparse.Namespace,
            values: Any,
            option_string: Optional[str] = None,
        ) -> None:
            setattr(getattr(namespace, self.dest), name, value)

    return _SetArgument


def get_options_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--fetch-submodules",
        dest="prefetch_options",
        default=PrefetchOptions(),
        action=set_argument("fetch_submodules", True),
    )
    parser.add_argument(
        "--no-fetch-submodules",
        dest="prefetch_options",
        action=set_argument("fetch_submodules", False),
    )
    parser.add_argument(
        "--verbose",
        "-v",
        dest="logging_configuration",
        default=LoggingConfiguration(output_file=sys.stderr, log_level=WARNING),
        action=set_argument("log_level", INFO),
    )
    parser.add_argument(
        "--nix",
        dest="rendering_format",
        default=RenderingFormat.json,
        action="store_const",
        const=RenderingFormat.nix,
    )
    parser.add_argument(
        "--json",
        dest="rendering_format",
        action="store_const",
        const=RenderingFormat.json,
    )
    return parser
