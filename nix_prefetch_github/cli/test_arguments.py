from logging import INFO, WARNING
from unittest import TestCase

from nix_prefetch_github.cli.arguments import get_options_argument_parser
from nix_prefetch_github.interfaces import PrefetchOptions, RenderingFormat


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

    def test_that_by_default_leave_dot_git_is_disabled(self) -> None:
        parser = get_options_argument_parser()
        arguments = parser.parse_args([])
        self.assertFalse(arguments.prefetch_options.leave_dot_git)

    def test_that_leave_dot_git_can_be_enabled_via_appropriate_cli_option(self) -> None:
        parser = get_options_argument_parser()
        arguments = parser.parse_args(["--leave-dot-git"])
        self.assertTrue(arguments.prefetch_options.leave_dot_git)

    def test_that_leave_dot_git_can_be_disabled_via_appropriate_cli_option(
        self,
    ) -> None:
        parser = get_options_argument_parser()
        arguments = parser.parse_args(["--leave-dot-git", "--no-leave-dot-git"])
        self.assertFalse(arguments.prefetch_options.leave_dot_git)

    def test_that_specifying_deep_clone_sets_prefetch_options_properly(self) -> None:
        parser = get_options_argument_parser()
        arguments = parser.parse_args(["--deep-clone"])
        self.assertTrue(arguments.prefetch_options.deep_clone)

    def test_that_specifying_no_deep_clone_sets_prefetch_options_propery(self) -> None:
        parser = get_options_argument_parser()
        arguments = parser.parse_args(["--deep-clone", "--no-deep-clone"])
        self.assertFalse(arguments.prefetch_options.deep_clone)

    def test_that_deep_clone_is_disabled_by_default(self) -> None:
        parser = get_options_argument_parser()
        arguments = parser.parse_args([])
        self.assertFalse(arguments.prefetch_options.deep_clone)

    def test_that_log_level_is_WARNING_by_default(self) -> None:
        parser = get_options_argument_parser()
        arguments = parser.parse_args([])
        self.assertEqual(arguments.logging_configuration.log_level, WARNING)

    def test_that_verbosity_flag_increases_log_level_to_INFO(self) -> None:
        parser = get_options_argument_parser()
        arguments = parser.parse_args(["--verbose"])
        self.assertEqual(arguments.logging_configuration.log_level, INFO)

    def test_rendering_option_is_json_by_default(self) -> None:
        parser = get_options_argument_parser()
        arguments = parser.parse_args([])
        self.assertEqual(arguments.rendering_format, RenderingFormat.json)

    def test_specifying_nix_sets_rendering_option_to_nix(self) -> None:
        parser = get_options_argument_parser()
        arguments = parser.parse_args(["--nix"])
        self.assertEqual(arguments.rendering_format, RenderingFormat.nix)

    def test_specifying_nix_and_then_json_sets_rendering_option_to_json(self) -> None:
        parser = get_options_argument_parser()
        arguments = parser.parse_args(["--nix", "--json"])
        self.assertEqual(arguments.rendering_format, RenderingFormat.json)
