"""This module contains tests regarding the github issue #22.

https://github.com/seppeljordan/nix-prefetch-github/issues/22
"""

import os
from unittest import TestCase

from effect.testing import perform_sequence

from nix_prefetch_github.core import GithubRepository, ListRemote, prefetch_github
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
        self.revision_index_factory = FakeRevisionIndexFactory(
            self.nixos_secure_factory_ls_remote_output
        )

    def test_issue_22(self) -> None:
        self.url_hasher.default_hash = "TEST_HASH_SUM"
        effect = prefetch_github(
            self.url_hasher,
            self.revision_index_factory,
            repository=self.repository,
            prefetch=False,
            rev="jrg/mvp",
        )
        prefetch_result = perform_sequence([], effect)
        assert prefetch_result.rev == "ad1a1d1d25870cc70cd7e708a73c874322064d96"
        assert prefetch_result.sha256 == "TEST_HASH_SUM"
