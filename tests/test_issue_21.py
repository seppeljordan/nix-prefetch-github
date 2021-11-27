"""This module contains tests regarding the github issue #21.

https://github.com/seppeljordan/nix-prefetch-github/issues/21
"""

import os
from unittest import TestCase

from effect.testing import perform_sequence

from nix_prefetch_github.core import GithubRepository, ListRemote, prefetch_github
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
        self.revision_index_factory = FakeRevisionIndexFactory(
            self.sensu_go_ls_remote_output
        )

    def test_prefetch_sensu_go_5_11(self):
        self.url_hasher.default_hash = "TEST_HASH_SUM"
        effect = prefetch_github(
            self.url_hasher,
            self.revision_index_factory,
            repository=self.repository,
            prefetch=False,
            rev="5.11.0",
        )
        prefetch_result = perform_sequence([], effect)
        assert prefetch_result.rev == "dd8f160a9033ecb5ad0384baf6a9965fa7bd3c17"
        assert prefetch_result.sha256 == "TEST_HASH_SUM"
