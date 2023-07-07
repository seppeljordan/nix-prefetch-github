"""This module contains tests regarding the github issue #21.

https://github.com/seppeljordan/nix-prefetch-github/issues/21
"""

import os
from unittest import TestCase

from nix_prefetch_github.interfaces import GithubRepository, PrefetchOptions
from nix_prefetch_github.list_remote import ListRemote
from nix_prefetch_github.prefetch import PrefetchedRepository, PrefetcherImpl
from nix_prefetch_github.revision_index import RevisionIndexImpl
from nix_prefetch_github.tests import FakeRevisionIndexFactory, FakeUrlHasher


class TestIssue21(TestCase):
    @property
    def sensu_go_ls_remote_output(self) -> ListRemote:
        with open(
            os.path.join(os.path.dirname(__file__), "sensu_go_git_ls_remote.txt")
        ) as handle:
            return ListRemote.from_git_ls_remote_output(handle.read())

    def setUp(self) -> None:
        self.url_hasher = FakeUrlHasher()
        self.repository = GithubRepository(
            owner="sensu",
            name="sensu-go",
        )
        self.revision_index_factory = FakeRevisionIndexFactory()
        self.prefetcher = PrefetcherImpl(self.url_hasher, self.revision_index_factory)

    def test_prefetch_sensu_go_5_11(self) -> None:
        self.url_hasher.hash_sum = "TEST_HASH_SUM"
        self.revision_index_factory.revision_index = RevisionIndexImpl(
            self.sensu_go_ls_remote_output
        )
        result = self.prefetcher.prefetch_github(
            repository=self.repository,
            rev="5.11.0",
            prefetch_options=PrefetchOptions(),
        )
        assert isinstance(result, PrefetchedRepository)
        assert result.rev == "dd8f160a9033ecb5ad0384baf6a9965fa7bd3c17"
        assert result.hash_sum == "TEST_HASH_SUM"
