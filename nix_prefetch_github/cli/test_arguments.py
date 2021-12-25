from logging import INFO, WARNING
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

    def test_that_log_level_is_WARNING_by_default(self) -> None:
        parser = get_options_argument_parser()
        arguments = parser.parse_args([])
        self.assertEqual(arguments.logging_configuration.log_level, WARNING)

    def test_that_verbosity_flag_increases_log_level_to_INFO(self) -> None:
        parser = get_options_argument_parser()
        arguments = parser.parse_args(["--verbose"])
        self.assertEqual(arguments.logging_configuration.log_level, INFO)
