from unittest import TestCase

from effect.testing import perform_sequence

from ..tests import FakeUrlHasher
from .effects import (
    AbortWithErrorMessage,
    GetListRemote,
    GetRevisionForLatestRelease,
    TryPrefetch,
)
from .error import AbortWithError
from .list_remote import ListRemote
from .prefetch import (
    is_sha1_hash,
    prefetch_github,
    prefetch_latest_release,
    repository_not_found_error_message,
    revision_not_found_errormessage,
)
from .repository import GithubRepository


class PrefetchGithubTests(TestCase):
    def setUp(self) -> None:
        self.url_hasher = FakeUrlHasher()
        self.pypi2nix_list_remote = ListRemote.from_git_ls_remote_output(
            "\n".join(
                [
                    "ref: refs/heads/master\tHEAD",
                    "1234\trefs/heads/dev",
                    "5678\trefs/heads/master",
                    "1234\trefs/tags/v1.0",
                ]
            )
        )

    def test_prefetch_github_actual_prefetch(self):
        repository = GithubRepository(
            owner="seppeljordan",
            name="pypi2nix",
        )
        seq = [
            (
                GetListRemote(repository=repository),
                lambda i: self.pypi2nix_list_remote,
            ),
            (
                TryPrefetch(
                    repository=repository,
                    rev=self.pypi2nix_list_remote.branch("master"),
                    sha256="TEST_ACTUALHASH",
                    fetch_submodules=True,
                ),
                lambda i: None,
            ),
        ]
        eff = prefetch_github(
            url_hasher=self.url_hasher, repository=repository, prefetch=True
        )
        prefetch_result = perform_sequence(seq, eff)
        self.assertEqual(
            prefetch_result.rev, self.pypi2nix_list_remote.branch("master")
        )
        self.assertEqual(prefetch_result.sha256, "TEST_ACTUALHASH")

    def test_can_prefetch_from_tag_given_as_rev(self):
        repository = GithubRepository(owner="seppeljordan", name="pypi2nix")
        seq = [
            (
                GetListRemote(repository=repository),
                lambda i: self.pypi2nix_list_remote,
            ),
        ]
        eff = prefetch_github(
            url_hasher=self.url_hasher,
            repository=repository,
            prefetch=False,
            rev="v1.0",
        )
        prefetch_result = perform_sequence(seq, eff)
        self.assertEqual(prefetch_result.rev, self.pypi2nix_list_remote.tag("v1.0"))
        self.assertEqual(prefetch_result.sha256, "TEST_ACTUALHASH")

    def test_prefetch_github_no_actual_prefetch(self):
        repository = GithubRepository(owner="seppeljordan", name="pypi2nix")
        seq = [
            (
                GetListRemote(repository=repository),
                lambda i: self.pypi2nix_list_remote,
            ),
        ]
        eff = prefetch_github(
            url_hasher=self.url_hasher, repository=repository, prefetch=False
        )
        prefetch_result = perform_sequence(seq, eff)
        self.assertEqual(
            prefetch_result.rev, self.pypi2nix_list_remote.branch("master")
        )
        self.assertEqual(prefetch_result.sha256, "TEST_ACTUALHASH")

    def test_prefetch_github_rev_given(self):
        repository = GithubRepository(owner="seppeljordan", name="pypi2nix")
        commit_hash = "50553a665d2700c353ac41ab28c23b1027b7c1f0"
        eff = prefetch_github(
            url_hasher=self.url_hasher,
            repository=repository,
            prefetch=False,
            rev=commit_hash,
        )
        prefetch_result = perform_sequence([], eff)
        self.assertEqual(prefetch_result.rev, commit_hash)
        self.assertEqual(prefetch_result.sha256, "TEST_ACTUALHASH")

    def test_prefetch_aborts_when_rev_is_not_found(self):
        repository = GithubRepository(owner="seppeljordan", name="pypi2nix")
        sequence = [
            (
                GetListRemote(repository=repository),
                lambda _: self.pypi2nix_list_remote,
            ),
            (
                AbortWithErrorMessage(
                    revision_not_found_errormessage(
                        repository=repository, revision="does-not-exist"
                    )
                ),
                lambda _: None,
            ),
        ]
        effect = prefetch_github(
            url_hasher=self.url_hasher, repository=repository, rev="does-not-exist"
        )
        with self.assertRaises(AbortWithError):
            perform_sequence(sequence, effect)

    def test_that_prefetch_github_understands_full_ref_names(self):
        repository = GithubRepository(owner="seppeljordan", name="pypi2nix")
        sequence = [
            (
                GetListRemote(repository=repository),
                lambda i: self.pypi2nix_list_remote,
            ),
        ]
        effect = prefetch_github(
            url_hasher=self.url_hasher,
            repository=repository,
            prefetch=False,
            rev="refs/heads/master",
        )
        prefetch_result = perform_sequence(sequence, effect)
        self.assertEqual(
            prefetch_result.rev, self.pypi2nix_list_remote.branch("master")
        )
        self.assertEqual(prefetch_result.sha256, "TEST_ACTUALHASH")

    def test_that_prefetch_github_understands_fetch_submodules(self):
        repository = GithubRepository(owner="seppeljordan", name="pypi2nix")
        sequence = [
            (
                GetListRemote(repository=repository),
                lambda i: self.pypi2nix_list_remote,
            ),
        ]
        effect = prefetch_github(
            url_hasher=self.url_hasher,
            repository=repository,
            prefetch=False,
            fetch_submodules=True,
        )
        prefetch_info = perform_sequence(sequence, effect)
        assert prefetch_info.fetch_submodules

    def test_that_prefetch_github_without_submodules_is_understood_and_respected(self):
        repository = GithubRepository(owner="seppeljordan", name="pypi2nix")
        sequence = [
            (
                GetListRemote(repository=repository),
                lambda i: self.pypi2nix_list_remote,
            ),
        ]
        effect = prefetch_github(
            url_hasher=self.url_hasher,
            repository=repository,
            prefetch=False,
            fetch_submodules=False,
        )
        prefetch_info = perform_sequence(sequence, effect)
        assert not prefetch_info.fetch_submodules


class IsSha1HashTests(TestCase):
    def test_is_sha1_hash_detects_actual_hash(self):
        text = "5a484700f1006389847683a72cd88bf7057fe772"
        self.assertTrue(is_sha1_hash(text))

    def test_is_sha1_hash_returns_false_for_string_to_short(self):
        text = "5a484700f1006389847683a72cd88bf7057fe77"
        self.assertTrue(len(text) < 40)
        self.assertFalse(is_sha1_hash(text))


class ErrorMessageTests(TestCase):
    def setUp(self) -> None:
        self.repository = GithubRepository(owner="test_owner", name="test_repo")
        self.error_message = revision_not_found_errormessage(
            repository=self.repository, revision="test_revision"
        )

    def test_revision_not_found_errormessage_contains_owner_repo_and_revision(self):
        assert "test_owner" in self.error_message
        assert "test_repo" in self.error_message
        assert "test_revision" in self.error_message


class TestPrefetchLatest(TestCase):
    def setUp(self) -> None:
        self.repository = GithubRepository(owner="owner", name="repo")
        self.url_hasher = FakeUrlHasher()

    def test_prefetch_latest_calculates_the_propper_commit(self):
        expected_revision = "123"
        expected_sha256 = "456"
        self.url_hasher.default_hash = expected_sha256
        sequence = [
            (
                GetRevisionForLatestRelease(repository=self.repository),
                lambda _: expected_revision,
            ),
            (
                TryPrefetch(
                    repository=self.repository,
                    sha256=expected_sha256,
                    rev=expected_revision,
                    fetch_submodules=False,
                ),
                lambda _: None,
            ),
        ]
        effect = prefetch_latest_release(
            self.url_hasher, self.repository, prefetch=True, fetch_submodules=False
        )
        result = perform_sequence(sequence, effect)
        assert result.rev == expected_revision
        assert result.sha256 == expected_sha256

    def test_prefetch_latest_release_fails_gracefully_when_no_repository_was_found(
        self,
    ):
        sequence = [
            (
                GetRevisionForLatestRelease(repository=self.repository),
                lambda _: None,
            ),
            (
                AbortWithErrorMessage(
                    repository_not_found_error_message(repository=self.repository)
                ),
                lambda _: None,
            ),
        ]
        effect = prefetch_latest_release(
            self.url_hasher, self.repository, prefetch=True, fetch_submodules=False
        )
        with self.assertRaises(AbortWithError):
            perform_sequence(sequence, effect)

    def test_prefetch_latest_respects_no_prefetching(self):
        expected_revision = "123"
        expected_sha256 = "456"
        self.url_hasher.default_hash = expected_sha256
        sequence = [
            (
                GetRevisionForLatestRelease(repository=self.repository),
                lambda _: expected_revision,
            ),
        ]
        effect = prefetch_latest_release(
            self.url_hasher, self.repository, prefetch=False, fetch_submodules=False
        )
        result = perform_sequence(sequence, effect)
        assert result.rev == expected_revision
        assert result.sha256 == expected_sha256

    def test_prefetch_latest_respects_fetching_submodules(self):
        expected_revision = "123"
        expected_sha256 = "456"
        self.url_hasher.default_hash = expected_sha256
        sequence = [
            (
                GetRevisionForLatestRelease(repository=self.repository),
                lambda _: expected_revision,
            ),
        ]
        effect = prefetch_latest_release(
            self.url_hasher, self.repository, prefetch=False, fetch_submodules=True
        )
        result = perform_sequence(sequence, effect)
        assert result.rev == expected_revision
        assert result.sha256 == expected_sha256
