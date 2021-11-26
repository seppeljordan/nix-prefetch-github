from unittest import TestCase

from effect.testing import perform_sequence

from ..tests import FakeListRemoteFactory, FakeUrlHasher
from . import (
    CheckGitRepoIsDirty,
    DetectGithubRepository,
    DetectRevision,
    GithubRepository,
    PrefetchedRepository,
    RevisionIndex,
    ShowWarning,
    TryPrefetch,
    prefetch_directory,
)


class PrefetchDirectoryTests(TestCase):
    def setUp(self) -> None:
        self.url_hasher = FakeUrlHasher()
        self.list_remote_factory = FakeListRemoteFactory()
        self.revision_index = RevisionIndex(self.list_remote_factory)

    def test_prefetch_directory_with_clean_working_directory(self):
        repo_directory = "/directory"
        github_repo = GithubRepository(name="name", owner="owner")
        remote_name = "remote"
        current_revision = "0e416e798d49a075a9747ad868c2832e03b3b2e5"
        sha256_sum = "123"
        self.url_hasher.default_hash = sha256_sum
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
                TryPrefetch(
                    repository=github_repo,
                    rev=current_revision,
                    fetch_submodules=True,
                    sha256=sha256_sum,
                ),
                lambda _: None,
            ),
        ]
        effect = prefetch_directory(
            self.url_hasher,
            self.revision_index,
            directory=repo_directory,
            remote=remote_name,
        )
        prefetch_result = perform_sequence(sequence, effect)
        assert prefetch_result == expected

    def test_prefetch_directory_with_dirty_working_directory(self):
        repo_directory = "/directory"
        github_repo = GithubRepository(name="name", owner="owner")
        remote_name = "remote"
        current_revision = "0e416e798d49a075a9747ad868c2832e03b3b2e5"
        sha256_sum = "123"
        self.url_hasher.default_hash = sha256_sum
        expected = PrefetchedRepository(
            repository=github_repo,
            rev=current_revision,
            sha256=sha256_sum,
            fetch_submodules=True,
        )
        sequence = [
            (CheckGitRepoIsDirty(directory=repo_directory), lambda _: True),
            (ShowWarning(message="Repository at /directory dirty"), lambda _: None),
            (
                DetectGithubRepository(directory=repo_directory, remote=remote_name),
                lambda _: github_repo,
            ),
            (DetectRevision(directory=repo_directory), lambda _: current_revision),
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
        effect = prefetch_directory(
            self.url_hasher,
            self.revision_index,
            directory=repo_directory,
            remote=remote_name,
        )
        prefetch_result = perform_sequence(sequence, effect)
        assert prefetch_result == expected
