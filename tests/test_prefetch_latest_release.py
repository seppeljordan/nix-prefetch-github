from effect.testing import perform_sequence
from pytest import fixture, raises

from nix_prefetch_github.core import (
    AbortWithError,
    AbortWithErrorMessage,
    CalculateSha256Sum,
    GetRevisionForLatestRelease,
    GithubRepository,
    TryPrefetch,
    prefetch_latest_release,
    repository_not_found_error_message,
)


def test_prefetch_latest_calculates_the_propper_commit(repository):
    expected_revision = "123"
    expected_sha256 = "456"
    sequence = [
        (
            GetRevisionForLatestRelease(repository=repository),
            lambda _: expected_revision,
        ),
        (
            CalculateSha256Sum(
                repository=repository,
                revision=expected_revision,
                fetch_submodules=False,
            ),
            lambda _: expected_sha256,
        ),
        (
            TryPrefetch(
                repository=repository,
                sha256=expected_sha256,
                rev=expected_revision,
                fetch_submodules=False,
            ),
            lambda _: None,
        ),
    ]
    effect = prefetch_latest_release(repository, prefetch=True, fetch_submodules=False)
    result = perform_sequence(sequence, effect)
    assert result.rev == expected_revision
    assert result.sha256 == expected_sha256


def test_prefetch_latest_release_fails_gracefully_when_no_repository_was_found(
    repository,
):
    sequence = [
        (GetRevisionForLatestRelease(repository=repository), lambda _: None,),
        (
            AbortWithErrorMessage(
                repository_not_found_error_message(repository=repository)
            ),
            lambda _: None,
        ),
    ]
    effect = prefetch_latest_release(repository, prefetch=True, fetch_submodules=False)
    with raises(AbortWithError):
        perform_sequence(sequence, effect)


def test_prefetch_latest_respects_no_prefetching(repository):
    expected_revision = "123"
    expected_sha256 = "456"
    sequence = [
        (
            GetRevisionForLatestRelease(repository=repository),
            lambda _: expected_revision,
        ),
        (
            CalculateSha256Sum(
                repository=repository,
                revision=expected_revision,
                fetch_submodules=False,
            ),
            lambda _: expected_sha256,
        ),
    ]
    effect = prefetch_latest_release(repository, prefetch=False, fetch_submodules=False)
    result = perform_sequence(sequence, effect)
    assert result.rev == expected_revision
    assert result.sha256 == expected_sha256


def test_prefetch_latest_respects_fetching_submodules(repository):
    expected_revision = "123"
    expected_sha256 = "456"
    sequence = [
        (
            GetRevisionForLatestRelease(repository=repository),
            lambda _: expected_revision,
        ),
        (
            CalculateSha256Sum(
                repository=repository,
                revision=expected_revision,
                fetch_submodules=True,
            ),
            lambda _: expected_sha256,
        ),
    ]
    effect = prefetch_latest_release(repository, prefetch=False, fetch_submodules=True)
    result = perform_sequence(sequence, effect)
    assert result.rev == expected_revision
    assert result.sha256 == expected_sha256


@fixture
def repository():
    return GithubRepository(owner="owner", name="repo")
