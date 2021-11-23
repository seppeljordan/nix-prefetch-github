"""This module contains tests regarding the github issue #21.

https://github.com/seppeljordan/nix-prefetch-github/issues/21
"""

import os
from unittest import TestCase

from effect.testing import perform_sequence

from nix_prefetch_github.core import (
    GetListRemote,
    GithubRepository,
    ListRemote,
    prefetch_github,
)
from nix_prefetch_github.tests import FakeUrlHasher


class TestIssue21(TestCase):
    @property
    def sensu_go_ls_remote_output(self):
        with open(
            os.path.join(os.path.dirname(__file__), "sensu_go_git_ls_remote.txt")
        ) as handle:
            return ListRemote.from_git_ls_remote_output(handle.read())

    def setUp(self) -> None:
        self.url_hasher = FakeUrlHasher()

    def test_prefetch_sensu_go_5_11(self):
        self.url_hasher.default_hash = "TEST_HASH_SUM"
        repository = GithubRepository(
            owner="sensu",
            name="sensu-go",
        )
        sequence = [
            (
                GetListRemote(repository=repository),
                lambda _: self.sensu_go_ls_remote_output,
            ),
        ]
        effect = prefetch_github(
            self.url_hasher, repository=repository, prefetch=False, rev="5.11.0"
        )
        prefetch_result = perform_sequence(sequence, effect)
        assert prefetch_result.rev == "dd8f160a9033ecb5ad0384baf6a9965fa7bd3c17"
        assert prefetch_result.sha256 == "TEST_HASH_SUM"
