"""This module contains tests regarding the github issue #22.

https://github.com/seppeljordan/nix-prefetch-github/issues/22
"""

import os
from unittest import TestCase

from nix_prefetch_github.interfaces import GithubRepository, PrefetchOptions
from nix_prefetch_github.list_remote import ListRemote
from nix_prefetch_github.prefetch import PrefetchedRepository, PrefetcherImpl
from nix_prefetch_github.revision_index import RevisionIndexImpl
from nix_prefetch_github.tests import FakeRevisionIndexFactory, FakeUrlHasher


class Issue22Tests(TestCase):
    @property
    def nixos_secure_factory_ls_remote_output(self) -> ListRemote:
        with open(
            os.path.join(
                os.path.dirname(__file__),
                "jraygauthier_nixos_secure_factory_git_ls_remote.txt",
            )
        ) as handle:
            return ListRemote.from_git_ls_remote_output(handle.read())

    def setUp(self) -> None:
        self.repository = GithubRepository(
            owner="jraygauthier", name="nixos-secure-factory"
        )
        self.url_hasher = FakeUrlHasher()
        self.revision_index_factory = FakeRevisionIndexFactory()
        self.revision_index_factory.revision_index = RevisionIndexImpl(
            self.nixos_secure_factory_ls_remote_output
        )
        self.prefetcher = PrefetcherImpl(
            self.url_hasher,
            self.revision_index_factory,
        )

    def test_issue_22(self) -> None:
        self.url_hasher.hash_sum = "TEST_HASH_SUM"
        result = self.prefetcher.prefetch_github(
            repository=self.repository,
            rev="jrg/mvp",
            prefetch_options=PrefetchOptions(),
        )
        assert isinstance(result, PrefetchedRepository)
        assert result.rev == "ad1a1d1d25870cc70cd7e708a73c874322064d96"
        assert result.sha256 == "TEST_HASH_SUM"
