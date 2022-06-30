from typing import Callable, List, Optional, cast
from unittest import TestCase

from nix_prefetch_github.interfaces import (
    GithubRepository,
    PrefetchedRepository,
    PrefetchOptions,
    PrefetchResult,
    RenderingFormat,
)
from nix_prefetch_github.use_cases.prefetch_github_repository import (
    PrefetchGithubRepositoryUseCaseImpl,
    Request,
)


class UseCaseTests(TestCase):
    def setUp(self) -> None:
        self.prefetcher = FakePrefetcher()
        self.nix_presenter = FakePresenter()
        self.json_presenter = FakePresenter()
        self.alerter = FakeAlerter()
        self.use_case = PrefetchGithubRepositoryUseCaseImpl(
            nix_presenter=self.nix_presenter,
            json_presenter=self.json_presenter,
            prefetcher=self.prefetcher,
            alerter=self.alerter,
        )

    def test_that_repository_is_prefetched_successfully_if_prefetcher_succeeds(
        self,
    ) -> None:
        request = self.make_request()
        self.use_case.prefetch_github_repository(request)
        self.assert_is_success()

    def test_that_json_result_is_presented_if_json_rendering_is_requested(self) -> None:
        request = self.make_request(rendering_format=RenderingFormat.json)
        self.use_case.prefetch_github_repository(request)
        self.assert_json_result()

    def test_that_nix_result_is_presented_if_nix_rendering_is_requested(self) -> None:
        request = self.make_request(rendering_format=RenderingFormat.nix)
        self.use_case.prefetch_github_repository(request)
        self.assert_nix_result()

    def test_that_user_is_alerted_if_leave_dot_git_option_is_requested(self) -> None:
        request = self.make_request(
            prefetch_options=PrefetchOptions(leave_dot_git=True)
        )
        self.use_case.prefetch_github_repository(request)
        self.assert_alerted_user()

    def test_that_user_is_alerted_if_deep_clone_option_is_requested(self) -> None:
        request = self.make_request(prefetch_options=PrefetchOptions(deep_clone=True))
        self.use_case.prefetch_github_repository(request)
        self.assert_alerted_user()

    def test_that_user_is_alerted_with_correct_prefetch_options(self) -> None:
        expected_options = PrefetchOptions(deep_clone=True)
        request = self.make_request(prefetch_options=expected_options)
        self.use_case.prefetch_github_repository(request)
        self.assert_alert_options(
            lambda options: options == expected_options,
        )

    def test_that_user_is_not_alerted_if_leave_dot_git_and_deep_clone_are_false(
        self,
    ) -> None:
        request = self.make_request(
            prefetch_options=PrefetchOptions(leave_dot_git=False, deep_clone=False)
        )
        self.use_case.prefetch_github_repository(request)
        self.assert_not_alerted_user()

    def make_request(
        self,
        rendering_format: RenderingFormat = RenderingFormat.json,
        prefetch_options: PrefetchOptions = PrefetchOptions(),
    ) -> Request:
        return Request(
            repository=GithubRepository(owner="owner", name="name"),
            revision=None,
            prefetch_options=prefetch_options,
            rendering_format=rendering_format,
        )

    def assert_alerted_user(self) -> None:
        self.assertEqual(
            self.alerter.alert_count,
            1,
            "Expected the user to be alerted once but they were not alerted",
        )

    def assert_not_alerted_user(self) -> None:
        self.assertFalse(
            self.alerter.alert_count,
            f"Expected the user to NOT be alerted but they were alerted {self.alerter.alert_count} times.",
        )

    def assert_alert_options(
        self,
        condition: Callable[[PrefetchOptions], bool],
        message: Optional[str] = None,
    ) -> None:
        self.assertIsNotNone(self.alerter.last_alert_options)
        self.assertTrue(
            condition(cast(PrefetchOptions, self.alerter.last_alert_options)),
            msg=message,
        )

    def assert_is_success(self) -> None:
        results = self.nix_presenter.results + self.json_presenter.results
        self.assertTrue(results)
        self.assertIsInstance(
            results[-1],
            PrefetchedRepository,
        )

    def assert_json_result(self) -> None:
        self.assertFalse(self.nix_presenter.results)
        self.assertTrue(self.json_presenter)

    def assert_nix_result(self) -> None:
        self.assertTrue(self.nix_presenter.results)
        self.assertFalse(self.json_presenter.results)


class FakeAlerter:
    def __init__(self) -> None:
        self.alert_count: int = 0
        self.last_alert_options: Optional[PrefetchOptions] = None

    def alert_user_about_unsafe_prefetch_options(
        self, prefetch_options: PrefetchOptions
    ) -> None:
        self.alert_count += 1
        self.last_alert_options = prefetch_options


class FakePrefetcher:
    def prefetch_github(
        self,
        repository: GithubRepository,
        rev: Optional[str],
        prefetch_options: PrefetchOptions,
    ) -> PrefetchResult:
        return PrefetchedRepository(
            repository=repository,
            rev="",
            sha256="",
            options=prefetch_options,
        )


class FakePresenter:
    def __init__(self) -> None:
        self.results: List[PrefetchResult] = []

    def present(self, prefetch_result: PrefetchResult) -> None:
        self.results.append(prefetch_result)
