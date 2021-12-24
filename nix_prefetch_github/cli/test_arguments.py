from unittest import TestCase

from ..interfaces import PrefetchOptions
from .arguments import get_options_argument_parser


class TestGetOptionsArgumentParser(TestCase):
    def test_that_prefetch_options_is_present_in_namespace_when_parsing_arguments(
        self,
    ) -> None:
        parser = get_options_argument_parser()
        arguments = parser.parse_args([])
        self.assertIsInstance(arguments.prefetch_options, PrefetchOptions)

    def test_that_fetch_submodules_can_enabled_by_specifying_appropriate_cli_option(
        self,
    ) -> None:
        parser = get_options_argument_parser()
        arguments = parser.parse_args(["--fetch-submodules"])
        self.assertTrue(arguments.prefetch_options.fetch_submodules)

    def test_that_fetch_submodules_can_be_disabled_by_specifying_appropriate_cli_option(
        self,
    ) -> None:
        parser = get_options_argument_parser()
        arguments = parser.parse_args(["--fetch-submodules", "--no-fetch-submodules"])
        self.assertFalse(arguments.prefetch_options.fetch_submodules)
