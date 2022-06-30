from typing import List, Optional
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
        self.use_case = PrefetchGithubRepositoryUseCaseImpl(
            nix_presenter=self.nix_presenter,
            json_presenter=self.json_presenter,
            prefetcher=self.prefetcher,
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

    def make_request(
        self, rendering_format: RenderingFormat = RenderingFormat.json
    ) -> Request:
        return Request(
            repository=GithubRepository(owner="owner", name="name"),
            revision=None,
            prefetch_options=PrefetchOptions(),
            rendering_format=rendering_format,
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
