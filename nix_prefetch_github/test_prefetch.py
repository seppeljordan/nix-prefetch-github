from typing import Callable, Optional, cast
from unittest import TestCase

from .interfaces import PrefetchOptions
from .list_remote import ListRemote
from .prefetch import (
    PrefetchedRepository,
    PrefetcherImpl,
    PrefetchFailure,
    PrefetchResult,
)
from .repository import GithubRepository
from .revision_index import RevisionIndex
from .tests import FakeRevisionIndexFactory, FakeUrlHasher


class PrefetcherTests(TestCase):
    def test_when_url_hasher_and_revision_index_fail_then_prefetching_also_fails(
        self,
    ) -> None:
        self.url_hasher.sha256_sum = None
        self.revision_index_factory.revision_index = None
        result = self.prefetch_repository()
        self.assertFailure(result)

    def test_return_hash_that_was_returned_by_url_hasher(self) -> None:
        result = self.prefetch_repository()
        self.assertIsInstance(result, PrefetchedRepository)

    def test_return_expected_hash_from_url_hasher(self) -> None:
        result = self.prefetch_repository()
        self.assertSuccess(result, lambda r: r.sha256 == self.expected_hash)

    def test_return_expected_revision_from_revision_index(self) -> None:
        result = self.prefetch_repository()
        self.assertSuccess(result, lambda r: r.rev == self.expected_revision)

    def test_cannot_prefetch_revision_that_does_not_exist(self) -> None:
        result = self.prefetch_repository(revision="does not exist")
        self.assertFailure(
            result,
            lambda f: f.reason == PrefetchFailure.Reason.unable_to_locate_revision,
        )

    def test_fail_with_correct_reason_when_hash_could_not_be_calculated(self) -> None:
        self.url_hasher.sha256_sum = None
        self.assertFailure(
            self.prefetch_repository(),
            lambda f: f.reason == PrefetchFailure.Reason.unable_to_calculate_sha256,
        )

    def test_can_prefetch_revision_by_its_sha1_id(self) -> None:
        expected_revision = "4840fbf9ebd246d334c11335fc85747013230b05"
        self.assertSuccess(
            self.prefetch_repository(revision=expected_revision),
            lambda result: result.rev == expected_revision,
        )

    def assertSuccess(
        self,
        result: PrefetchResult,
        prop: Callable[[PrefetchedRepository], bool] = lambda _: True,
    ) -> None:
        self.assertIsInstance(result, PrefetchedRepository)
        self.assertTrue(prop(cast(PrefetchedRepository, result)))

    def assertFailure(
        self,
        result: PrefetchResult,
        prop: Callable[[PrefetchFailure], bool] = lambda _: True,
    ) -> None:
        self.assertIsInstance(result, PrefetchFailure)
        self.assertTrue(prop(cast(PrefetchFailure, result)))

    def setUp(self) -> None:
        self.url_hasher = FakeUrlHasher()
        self.revision_index_factory = FakeRevisionIndexFactory()
        self.expected_hash = "test hash"
        self.expected_revision = "test ref"
        self.url_hasher.sha256_sum = self.expected_hash
        self.revision_index_factory.revision_index = RevisionIndex(
            ListRemote(
                symrefs={"HEAD": "refs/heads/master"},
                heads={"master": self.expected_revision},
            )
        )
        self.prefetcher = PrefetcherImpl(
            self.url_hasher,
            self.revision_index_factory,
        )
        self.repository = GithubRepository("test owner", "test name")

    def prefetch_repository(
        self,
        revision: Optional[str] = None,
        options: PrefetchOptions = PrefetchOptions(),
    ) -> PrefetchResult:
        return self.prefetcher.prefetch_github(self.repository, revision, options)
