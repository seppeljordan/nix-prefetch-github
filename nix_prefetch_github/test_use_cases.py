import shutil
import tempfile
from typing import Callable, Optional, cast
from unittest import TestCase

from .interfaces import PrefetchedRepository, PrefetchOptions, PrefetchResult
from .repository import GithubRepository
from .use_cases import PrefetchLocalRepositoryResult, PrefetchLocalRepositoryUseCase

FOO_REPOSITORY = GithubRepository(
    owner="test owner",
    name="test repo",
)
BAR_REPOSITORY = GithubRepository(
    owner="bar owner",
    name="bar repo",
)


class PrefetchLocalRepositoryTests(TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.mkdtemp()
        self.prefetch_options = PrefetchOptions()
        self.repository_detector = RepositoryDetectorTestImpl()
        self.prefetcher = PrefetcherTestImpl()
        self.use_case = PrefetchLocalRepositoryUseCase(
            self.repository_detector, self.prefetcher
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.directory)

    def test_when_detecting_foo_repository_then_foo_repository_is_prefetched(
        self,
    ) -> None:
        self.checkProperRepository(FOO_REPOSITORY)

    def test_when_detecting_bar_repository_then_bar_repository_is_prefetched(
        self,
    ) -> None:
        self.checkProperRepository(BAR_REPOSITORY)

    def test_when_detecting_no_repository_then_prefetch_failure_is_returned(
        self,
    ) -> None:
        self.repository_detector.repository = None
        prefetch_result = self.use_case.prefetch_local_repository(
            self.directory, self.prefetch_options
        )
        self.assertFailure(prefetch_result)

    def checkProperRepository(self, repository: GithubRepository) -> None:
        self.repository_detector.repository = repository
        prefetch_result = self.use_case.prefetch_local_repository(
            self.directory, self.prefetch_options
        )
        self.assertSuccess(prefetch_result, lambda repo: repo.repository == repository)

    def assertSuccess(
        self,
        result: PrefetchLocalRepositoryResult,
        condition: Callable[[PrefetchedRepository], bool] = lambda _: True,
    ) -> None:
        self.assertIsInstance(result, PrefetchedRepository)
        self.assertTrue(condition(cast(PrefetchedRepository, result)))

    def assertFailure(self, result: PrefetchLocalRepositoryResult) -> None:
        self.assertNotIsInstance(result, PrefetchedRepository)


class RepositoryDetectorTestImpl:
    def __init__(self) -> None:
        self.repository: Optional[GithubRepository] = None

    def detect_github_repository(
        self, directory: str, remote_name: Optional[str]
    ) -> Optional[GithubRepository]:
        return self.repository

    def is_repository_dirty(self, directory: str) -> bool:
        return False

    def get_current_revision(self, directory: str) -> Optional[str]:
        return "129fbd58473749a5b5474e3e65f60d1e3416aca8"


class PrefetcherTestImpl:
    def prefetch_github(
        self,
        repository: GithubRepository,
        rev: Optional[str],
        prefetch_options: PrefetchOptions,
    ) -> PrefetchResult:
        return PrefetchedRepository(
            repository=repository,
            rev="test rev",
            sha256="test sha256",
            fetch_submodules=prefetch_options.fetch_submodules,
        )
