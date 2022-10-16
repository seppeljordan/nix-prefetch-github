from logging import INFO, WARNING
from typing import List
from unittest import TestCase

from nix_prefetch_github.interfaces import RenderingFormat
from nix_prefetch_github.tests import FakeLoggerManager, RenderingFormatSelectorImpl
from nix_prefetch_github.use_cases.prefetch_directory import Request

from .nix_prefetch_github_directory_controller import PrefetchDirectoryController


class ControllerTests(TestCase):
    def setUp(self) -> None:
        self.logger_manager = FakeLoggerManager()
        self.fake_use_case = FakeUseCase()
        self.environment = FakeEnvironment()
        self.rendering_format_selector = RenderingFormatSelectorImpl()
        self.controller = PrefetchDirectoryController(
            logger_manager=self.logger_manager,
            use_case=self.fake_use_case,
            environment=self.environment,
            rendering_format_selector=self.rendering_format_selector,
        )

    def test_can_set_logging_configuration_via_argument(self) -> None:
        self.controller.process_arguments(["-v"])
        self.logger_manager.assertLoggingConfiguration(lambda c: c.log_level == INFO)

    def test_log_level_is_warning_by_default(self) -> None:
        self.controller.process_arguments([])
        self.logger_manager.assertLoggingConfiguration(lambda c: c.log_level == WARNING)

    def test_that_by_default_directory_is_detected_from_environment(self) -> None:
        expected_directory = "testdir"
        self.environment.set_cwd(expected_directory)
        self.controller.process_arguments([])
        self.assertEqual(
            self.fake_use_case.requests[-1].directory,
            expected_directory,
        )

    def test_can_parse_directory_from_arguments(self) -> None:
        expected_directory = "test/directory"
        self.controller.process_arguments(["--directory", expected_directory])
        self.assertEqual(
            self.fake_use_case.requests[-1].directory,
            expected_directory,
        )

    def test_use_cwd_if_directory_passed_is_empty_string(self) -> None:
        expected_directory = "test/directory"
        self.environment.set_cwd(expected_directory)
        self.controller.process_arguments(["--directory", ""])
        self.assertEqual(
            self.fake_use_case.requests[-1].directory,
            expected_directory,
        )

    def test_remote_is_origin_by_default(self) -> None:
        self.controller.process_arguments([])
        self.assertEqual(
            self.fake_use_case.requests[-1].remote,
            "origin",
        )

    def test_can_specify_origin_via_arguments(self) -> None:
        expected_origin = "upstream"
        self.controller.process_arguments(["--remote", expected_origin])
        self.assertEqual(
            self.fake_use_case.requests[-1].remote,
            expected_origin,
        )

    def test_that_json_rendering_format_is_seleted_when_json_is_given_as_argument(
        self,
    ) -> None:
        self.controller.process_arguments(["--json"])
        self.assertEqual(
            self.rendering_format_selector.selected_output_format,
            RenderingFormat.json,
        )

    def test_that_nix_rendering_format_is_seleted_when_nix_is_given_as_argument(
        self,
    ) -> None:
        self.controller.process_arguments(["--nix"])
        self.assertEqual(
            self.rendering_format_selector.selected_output_format,
            RenderingFormat.nix,
        )

    def test_can_specify_deep_clone_via_arguments(self) -> None:
        self.controller.process_arguments(["--deep-clone"])
        self.assertTrue(
            self.fake_use_case.requests[-1].prefetch_options.deep_clone,
        )


class FakeUseCase:
    def __init__(self) -> None:
        self.requests: List[Request] = []

    def prefetch_directory(self, request: Request) -> None:
        self.requests.append(request)


class FakeEnvironment:
    def __init__(self) -> None:
        self.cwd = "unset/cwd"

    def set_cwd(self, path: str) -> None:
        self.cwd = path

    def get_cwd(self) -> str:
        return self.cwd
