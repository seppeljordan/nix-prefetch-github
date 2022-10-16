from logging import INFO, WARNING
from typing import Callable, Optional, cast
from unittest import TestCase

from nix_prefetch_github.controller.nix_prefetch_github_latest_release_controller import (
    PrefetchLatestReleaseController,
)
from nix_prefetch_github.interfaces import RenderingFormat
from nix_prefetch_github.tests import FakeLoggerManager, RenderingFormatSelectorImpl
from nix_prefetch_github.use_cases.prefetch_latest_release import Request


class ControllerTests(TestCase):
    def setUp(self) -> None:
        self.logger_manager = FakeLoggerManager()
        self.rendering_format_selector = RenderingFormatSelectorImpl()
        self.fake_use_case = FakeUseCase()
        self.controller = PrefetchLatestReleaseController(
            use_case=self.fake_use_case,
            logger_manager=self.logger_manager,
            rendering_format_selector=self.rendering_format_selector,
        )

    def test_that_correct_owner_is_detected_from_arguments(self) -> None:
        self.controller.process_arguments(["owner", "repo"])
        self.assertRequest(
            lambda r: r.repository.owner == "owner",
            message="Requested repository has wrong owner",
        )

    def test_that_correct_repo_name_is_detected_from_arguments(self) -> None:
        self.controller.process_arguments(["owner", "repo"])
        self.assertRequest(
            lambda r: r.repository.name == "repo",
            message="Requested repository has wrong name",
        )

    def test_log_level_is_detected_from_arguments(self) -> None:
        self.controller.process_arguments(["owner", "repo", "-v"])
        self.logger_manager.assertLoggingConfiguration(lambda c: c.log_level == INFO)

    def test_by_default_log_level_is_set_to_warning(self) -> None:
        self.controller.process_arguments(["owner", "repo"])
        self.logger_manager.assertLoggingConfiguration(lambda c: c.log_level == WARNING)

    def test_that_json_rendering_format_is_seleted_when_json_is_given_as_argument(
        self,
    ) -> None:
        self.controller.process_arguments(["owner", "repo", "--json"])
        self.assertEqual(
            self.rendering_format_selector.selected_output_format,
            RenderingFormat.json,
        )

    def test_that_nix_rendering_format_is_seleted_when_nix_is_given_as_argument(
        self,
    ) -> None:
        self.controller.process_arguments(["owner", "repo", "--nix"])
        self.assertEqual(
            self.rendering_format_selector.selected_output_format,
            RenderingFormat.nix,
        )

    def assertRequest(
        self,
        condition: Optional[Callable[[Request], bool]] = None,
        message: str = "",
    ) -> None:
        self.assertIsNotNone(self.fake_use_case.request)
        if condition:
            self.assertTrue(
                condition(cast(Request, self.fake_use_case.request)), msg=message
            )


class FakeUseCase:
    def __init__(self) -> None:
        self.request: Optional[Request] = None

    def prefetch_latest_release(self, request: Request) -> None:
        assert not self.request
        self.request = request
