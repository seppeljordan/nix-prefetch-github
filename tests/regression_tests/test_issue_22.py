"""This module contains tests regarding the github issue #22.

https://github.com/seppeljordan/nix-prefetch-github/issues/22
"""

import os

import pytest
from effect.testing import perform_sequence

from nix_prefetch_github import GetListRemote, GithubRepository, ListRemote
from nix_prefetch_github.core import prefetch_github


@pytest.fixture
def nixos_secure_factory_ls_remote_output():
    with open(
        os.path.join(
            os.path.dirname(__file__),
            "jraygauthier_nixos_secure_factory_git_ls_remote.txt",
        )
    ) as handle:
        return ListRemote.from_git_ls_remote_output(handle.read())


def test_prefetch_sensu_go_5_11(url_hasher, nixos_secure_factory_ls_remote_output):
    url_hasher.default_hash = "TEST_HASH_SUM"
    repository = GithubRepository(owner="jraygauthier", name="nixos-secure-factory")
    sequence = [
        (
            GetListRemote(repository=repository),
            lambda _: nixos_secure_factory_ls_remote_output,
        ),
    ]
    effect = prefetch_github(
        url_hasher, repository=repository, prefetch=False, rev="jrg/mvp"
    )
    prefetch_result = perform_sequence(sequence, effect)
    assert prefetch_result.rev == "ad1a1d1d25870cc70cd7e708a73c874322064d96"
    assert prefetch_result.sha256 == "TEST_HASH_SUM"
