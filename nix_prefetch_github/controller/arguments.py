import argparse
import sys
from logging import WARNING
from typing import Any, Optional, Type

from nix_prefetch_github.interfaces import PrefetchOptions, RenderingFormat
from nix_prefetch_github.logging import LoggingConfiguration
from nix_prefetch_github.version import VERSION_STRING


def set_argument(name: str, value: Any) -> Type[argparse.Action]:
    class _SetArgument(argparse.Action):
        def __init__(
            self, option_strings: Any, dest: Any, nargs: Any = None, **kwargs: Any
        ) -> None:
            assert nargs is None, "Setting nargs is not allowed"
            super().__init__(option_strings, dest, nargs=0, **kwargs)

        def __call__(
            self,
            parser: argparse.ArgumentParser,
            namespace: argparse.Namespace,
            values: Any,
            option_string: Optional[str] = None,
        ) -> None:
            setattr(getattr(namespace, self.dest), name, value)

    return _SetArgument


class increase_log_level(argparse.Action):
    def __init__(
        self, option_strings: Any, dest: Any, nargs: Any = None, **kwargs: Any
    ) -> None:
        assert nargs is None, "Setting nargs is not allowed"
        super().__init__(option_strings, dest, nargs=0, **kwargs)

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Any,
        option_string: Optional[str] = None,
    ) -> None:
        configuration = getattr(namespace, self.dest)
        configuration.increase_log_level()


class decrease_log_level(argparse.Action):
    def __init__(
        self, option_strings: Any, dest: Any, nargs: Any = None, **kwargs: Any
    ) -> None:
        assert nargs is None, "Setting nargs is not allowed"
        super().__init__(option_strings, dest, nargs=0, **kwargs)

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Any,
        option_string: Optional[str] = None,
    ) -> None:
        configuration = getattr(namespace, self.dest)
        configuration.decrease_log_level()


def get_options_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--fetch-submodules",
        dest="prefetch_options",
        default=PrefetchOptions(),
        action=set_argument("fetch_submodules", True),
        help="Include git submodules in the output derivation",
    )
    parser.add_argument(
        "--no-fetch-submodules",
        dest="prefetch_options",
        action=set_argument("fetch_submodules", False),
        help="Don't include git submodules in output derivation",
    )
    parser.add_argument(
        "--leave-dot-git",
        dest="prefetch_options",
        action=set_argument("leave_dot_git", True),
        help="Include .git folder in output derivation. Use this if you need repository data, e.g. current commit hash, for the build process.",
    )
    parser.add_argument(
        "--no-leave-dot-git",
        dest="prefetch_options",
        action=set_argument("leave_dot_git", False),
        help="Don't include .git folder in output derivation.",
    )
    parser.add_argument(
        "--deep-clone",
        dest="prefetch_options",
        action=set_argument("deep_clone", True),
        help="Include all of the repository history in the output derivation. This option implies --leave-dot-git.",
    )
    parser.add_argument(
        "--no-deep-clone",
        dest="prefetch_options",
        action=set_argument("deep_clone", False),
        help="Don't include the repository history in the output derivation.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        dest="logging_configuration",
        default=LoggingConfiguration(output_file=sys.stderr, log_level=WARNING),
        action=increase_log_level,
        help="Print additional information about the programs execution. This is useful if you want to issue a bug report.",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        dest="logging_configuration",
        action=decrease_log_level,
        help="Print less information about the programs execution.",
    )
    parser.add_argument(
        "--nix",
        dest="rendering_format",
        default=RenderingFormat.json,
        action="store_const",
        const=RenderingFormat.nix,
        help="Output the results as valid nix code.",
    )
    parser.add_argument(
        "--json",
        dest="rendering_format",
        action="store_const",
        const=RenderingFormat.json,
        help="Output the results in the JSON format",
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s " + VERSION_STRING
    )
    return parser
