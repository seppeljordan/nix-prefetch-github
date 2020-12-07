"""This module provides tests for the implementation of the
CalculateSha256Sum intent"""
from functools import wraps

from effect import Effect, sync_perform

from nix_prefetch_github import CalculateSha256Sum, GithubRepository, dispatcher

from .markers import network, requires_nix_build


def performer_test(f):
    @wraps(f)
    def _wrapped(*args, **kwargs):
        generator = f(*args, **kwargs)
        intent = generator.send(None)
        while True:
            intent_result = sync_perform(dispatcher(), Effect(intent))
            try:
                intent = generator.send(intent_result)
            except StopIteration:
                return

    return _wrapped


@requires_nix_build
@network
@performer_test
def test_fetch_submodules_gives_different_hash_than_without_fetching_submodules():
    repository = GithubRepository(
        owner="git-up",
        name="test-repo-submodules",
    )
    hash_without_submodules = yield CalculateSha256Sum(
        repository=repository,
        revision="5a1dfa807759c39e3df891b6b46dfb2cf776c6ef",
        fetch_submodules=False,
    )
    assert hash_without_submodules
    hash_with_submodules = yield CalculateSha256Sum(
        repository=repository,
        revision="5a1dfa807759c39e3df891b6b46dfb2cf776c6ef",
        fetch_submodules=True,
    )
    assert hash_with_submodules
    assert hash_with_submodules != hash_without_submodules
