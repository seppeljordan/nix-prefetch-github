from effect.testing import perform_sequence

from nix_prefetch_github.core import (
    CalculateSha256Sum,
    CheckGitRepoIsDirty,
    DetectGithubRepository,
    DetectRevision,
    GithubRepository,
    PrefetchedRepository,
    TryPrefetch,
    prefetch_directory,
)


def test_prefetch_directory_with_clean_working_directory():
    repo_directory = "/directory"
    github_repo = GithubRepository(name="name", owner="owner")
    remote_name = "remote"
    current_revision = "0e416e798d49a075a9747ad868c2832e03b3b2e5"
    sha256_sum = "123"
    expected = PrefetchedRepository(
        repository=github_repo,
        rev=current_revision,
        sha256=sha256_sum,
        fetch_submodules=True,
    )
    sequence = [
        (CheckGitRepoIsDirty(directory=repo_directory), lambda _: False),
        (
            DetectGithubRepository(directory=repo_directory, remote=remote_name),
            lambda _: github_repo,
        ),
        (DetectRevision(directory=repo_directory), lambda _: current_revision),
        (
            CalculateSha256Sum(
                repository=github_repo,
                revision=current_revision,
                fetch_submodules=True,
            ),
            lambda _: sha256_sum,
        ),
        (
            TryPrefetch(
                repository=github_repo,
                rev=current_revision,
                fetch_submodules=True,
                sha256=sha256_sum,
            ),
            lambda _: None,
        ),
    ]
    effect = prefetch_directory(directory=repo_directory, remote=remote_name)
    prefetch_result = perform_sequence(sequence, effect)
    assert prefetch_result == expected
