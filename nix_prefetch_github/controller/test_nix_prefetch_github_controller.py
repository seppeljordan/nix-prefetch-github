from typing import Optional
from unittest import TestCase

from nix_prefetch_github.controller.nix_prefetch_github_controller import (
    NixPrefetchGithubController,
)
from nix_prefetch_github.interfaces import (
    GithubRepository,
    PrefetchOptions,
    RenderingFormat,
)
from nix_prefetch_github.use_cases.prefetch_github_repository import Request


class ControllerTests(TestCase):
    def setUp(self) -> None:
        self.use_case_mock = UseCaseImpl()
        self.controller = NixPrefetchGithubController(use_case=self.use_case_mock)

    def test_controller_extracts_example_owner_and_repo_from_arguments(self) -> None:
        expected_owner = "owner"
        expected_repo = "repo"
        self.controller.process_arguments([expected_owner, expected_repo])
        self.assertRepository(
            GithubRepository(owner=expected_owner, name=expected_repo),
        )

    def test_controller_extracts_alternative_owner_and_repo_from_arguments(
        self,
    ) -> None:
        expected_owner = "other_owner"
        expected_repo = "other_repo"
        self.controller.process_arguments([expected_owner, expected_repo])
        self.assertRepository(
            GithubRepository(owner=expected_owner, name=expected_repo),
        )

    def test_controller_can_select_nix_renderer_when_argument_is_specified(
        self,
    ) -> None:
        self.controller.process_arguments(["owner", "repo", "--nix"])
        self.assertRenderingFormat(RenderingFormat.nix)

    def test_controller_can_select_json_renderer_when_argument_is_specified(
        self,
    ) -> None:
        self.controller.process_arguments(["owner", "repo", "--json"])
        self.assertRenderingFormat(RenderingFormat.json)

    def test_controller_chooses_json_renderer_by_default(self) -> None:
        self.controller.process_arguments(["owner", "repo"])
        self.assertRenderingFormat(RenderingFormat.json)

    def test_controller_can_handle_rendering_flag_in_front_of_arguments(self) -> None:
        expected_owner = "owner"
        expected_repo = "repo"
        self.controller.process_arguments(["--nix", expected_owner, expected_repo])
        self.assertRepository(
            GithubRepository(owner=expected_owner, name=expected_repo),
        )

    def test_can_extract_revision_from_arguments(self) -> None:
        expected_revision = "test rev"
        self.controller.process_arguments(["owner", "repo", "--rev", expected_revision])
        self.assertRevision(expected_revision)

    def test_can_extract_an_alternative_revision_from_arguments(self) -> None:
        expected_revision = "alternative revision"
        self.controller.process_arguments(["owner", "repo", "--rev", expected_revision])
        self.assertRevision(expected_revision)

    def test_extract_deep_clone_request_from_arguments(self) -> None:
        self.controller.process_arguments(["owner", "repo", "--deep-clone"])
        self.assertPrefetchOptions(PrefetchOptions(deep_clone=True))

    def test_extract_non_deep_clone_request_from_arguments(self) -> None:
        self.controller.process_arguments(["owner", "repo", "--no-deep-clone"])
        self.assertPrefetchOptions(PrefetchOptions(deep_clone=False))

    def test_deep_clone_is_false_by_default(self) -> None:
        self.controller.process_arguments(["owner", "repo"])
        self.assertPrefetchOptions(PrefetchOptions(deep_clone=False))

    def test_extact_leave_dot_git_from_arguments(self) -> None:
        self.controller.process_arguments(["owner", "repo", "--leave-dot-git"])
        self.assertPrefetchOptions(PrefetchOptions(leave_dot_git=True))

    def test_extract_no_leave_dot_git_from_arguments(self) -> None:
        self.controller.process_arguments(["owner", "repo", "--no-leave-dot-git"])
        self.assertPrefetchOptions(PrefetchOptions(leave_dot_git=False))

    def test_extract_fetch_submodules_from_arguments(self) -> None:
        self.controller.process_arguments(["owner", "repo", "--fetch-submodules"])
        self.assertPrefetchOptions(PrefetchOptions(fetch_submodules=True))

    def test_extract_no_fetch_submodules_from_arguments(self) -> None:
        self.controller.process_arguments(["owner", "repo", "--no-fetch-submodules"])
        self.assertPrefetchOptions(PrefetchOptions(fetch_submodules=False))

    def assertPrefetchOptions(self, prefetch_options: PrefetchOptions) -> None:
        assert self.use_case_mock.request
        self.assertEqual(
            self.use_case_mock.request.prefetch_options,
            prefetch_options,
        )

    def assertRevision(self, revision: Optional[str]) -> None:
        assert self.use_case_mock.request
        self.assertEqual(
            self.use_case_mock.request.revision,
            revision,
        )

    def assertRepository(self, repository: GithubRepository) -> None:
        assert self.use_case_mock.request
        self.assertEqual(
            self.use_case_mock.request.repository,
            repository,
        )

    def assertRenderingFormat(self, rendering_format: RenderingFormat) -> None:
        assert self.use_case_mock.request
        self.assertEqual(
            self.use_case_mock.request.rendering_format,
            rendering_format,
        )


class UseCaseImpl:
    def __init__(self) -> None:
        self.request: Optional[Request] = None

    def prefetch_github_repository(self, request: Request) -> None:
        assert not self.request
        self.request = request
