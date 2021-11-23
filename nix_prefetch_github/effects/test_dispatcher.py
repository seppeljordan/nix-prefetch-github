import shutil
import subprocess
import tempfile
from unittest import TestCase

from effect import Effect

from nix_prefetch_github.core import (
    CheckGitRepoIsDirty,
    GetListRemote,
    GetRevisionForLatestRelease,
    GithubRepository,
    TryPrefetch,
    is_sha1_hash,
)
from nix_prefetch_github.effects import perform_effects

from ..tests import network, requires_nix_build


class DispatcherTests(TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        subprocess.run(["git", "init"], cwd=self.tmpdir)
        subprocess.run(["git", "config", "user.name", "test user"], cwd=self.tmpdir)
        subprocess.run(
            ["git", "config", "user.email", "test@email.test"], cwd=self.tmpdir
        )

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    @network
    def test_get_list_remote_retrieves_correct_tags(self):
        repository = GithubRepository(owner="seppeljordan", name="nix-prefetch-github")
        remote = perform_effects(Effect(GetListRemote(repository=repository)))
        self.assertEqual(remote.tag("v2.3"), "e632ce77435a4ab269c227c3ebcbaeaf746f8627")

    @network
    def test_get_list_remote_returns_none_for_none_existing_repos(self):
        repository = GithubRepository(
            owner="seppeljordan", name="non-existing-repo-123"
        )
        with self.assertRaises(SystemExit):
            perform_effects(Effect(GetListRemote(repository=repository)))

    @network
    @requires_nix_build
    def test_try_prefetch_returns_errorcode_when_fetching_with_invalid_sha256(self):
        repository = GithubRepository(owner="seppeljordan", name="nix-prefetch-github")
        returncode, _ = perform_effects(
            Effect(
                TryPrefetch(
                    repository=repository,
                    sha256="abc",
                    rev="e632ce77435a4ab269c227c3ebcbaeaf746f8627",
                    fetch_submodules=True,
                )
            )
        )
        self.assertTrue(returncode)

    @network
    @requires_nix_build
    def test_try_prefetch_actually_fetches_proper_commits_with_correct_hash(self):
        repository = GithubRepository(owner="seppeljordan", name="nix-prefetch-github")
        returncode, _ = perform_effects(
            Effect(
                TryPrefetch(
                    repository=repository,
                    sha256="sAXKffNUTfepcMfgOZahs7hofkMpsxI9NRhT2L17UCw=",
                    rev="e632ce77435a4ab269c227c3ebcbaeaf746f8627",
                    fetch_submodules=True,
                )
            )
        )
        self.assertFalse(returncode)

    @network
    def test_get_latest_revision(self):
        repository = GithubRepository(owner="seppeljordan", name="nix-prefetch-github")
        revision_hash = perform_effects(
            Effect(GetRevisionForLatestRelease(repository=repository))
        )
        self.assertTrue(is_sha1_hash(revision_hash))

    @network
    def test_get_revision_for_latest_release_raises_HTTPError_when_repo_not_found(self):
        repository = GithubRepository(
            owner="seppeljordan", name="repository-does-not-exist"
        )
        commit = perform_effects(
            Effect(GetRevisionForLatestRelease(repository=repository))
        )
        self.assertFalse(commit)

    def test_check_git_repo_is_dirty_raises_on_empty_repositories(self):
        with self.assertRaises(Exception):
            perform_effects(Effect(CheckGitRepoIsDirty(directory=self.tmpdir)))

    def test_check_git_repo_is_dirty_works_on_clean_repos(self):
        subprocess.run(["touch", "test.txt"], cwd=self.tmpdir)
        subprocess.run(["git", "add", "test.txt"], cwd=self.tmpdir)
        subprocess.run(["git", "commit", "-a", "-m" "test commit"], cwd=self.tmpdir)
        is_dirty = perform_effects(Effect(CheckGitRepoIsDirty(directory=self.tmpdir)))
        self.assertFalse(is_dirty)

    def test_check_git_repo_is_dirty_works_on_dirty_repos(self):
        subprocess.run(["touch", "test.txt"], cwd=self.tmpdir)
        subprocess.run(["git", "add", "test.txt"], cwd=self.tmpdir)
        subprocess.run(["git", "commit", "-a", "-m" "test commit"], cwd=self.tmpdir)
        subprocess.run(["touch", "test2.txt"], cwd=self.tmpdir)
        subprocess.run(["git", "add", "test2.txt"], cwd=self.tmpdir)
        is_dirty = perform_effects(Effect(CheckGitRepoIsDirty(directory=self.tmpdir)))
        self.assertTrue(is_dirty)
