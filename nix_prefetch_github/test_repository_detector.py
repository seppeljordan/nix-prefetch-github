import shlex
import shutil
import subprocess
import tempfile
from logging import getLogger
from unittest import TestCase

from .command.command_runner import CommandRunnerImpl
from .interfaces import GithubRepository
from .repository_detector import (
    RepositoryDetectorImpl,
    detect_github_repository_from_remote_url,
)


class GitTestCase(TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp()
        self.run_command("git init")
        self.run_command("git config user.name 'test user'")
        self.run_command("git config user.email test@email.test")
        self.detector = RepositoryDetectorImpl(CommandRunnerImpl(getLogger(__name__)))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir)

    def run_command(self, command: str) -> None:
        subprocess.run(shlex.split(command), cwd=self.tmpdir, capture_output=True)


class IsRepositoryDirtyTests(GitTestCase):
    def test_empty_directories_arent_considered_dirty(self) -> None:
        is_dirty = self.detector.is_repository_dirty(directory=self.tmpdir)
        self.assertFalse(is_dirty)

    def test_check_git_repo_is_dirty_works_on_clean_repos(self) -> None:
        self.run_command("touch test.txt")
        self.run_command("git add test.txt")
        self.run_command("git commit -a -m 'test commit'")
        is_dirty = self.detector.is_repository_dirty(directory=self.tmpdir)
        self.assertFalse(is_dirty)

    def test_check_git_repo_is_dirty_works_on_dirty_repos(self) -> None:
        self.run_command("touch test.txt")
        self.run_command("git add test.txt")
        self.run_command("git commit -a -m 'test commit'")
        self.run_command("touch test2.txt")
        self.run_command("git add test2.txt")
        is_dirty = self.detector.is_repository_dirty(directory=self.tmpdir)
        self.assertTrue(is_dirty)


class DetectGithubRepositoryTests(GitTestCase):
    def test_repository_without_remotes_returns_none(self) -> None:
        result = self.detector.detect_github_repository(self.tmpdir, remote_name=None)
        self.assertIsNone(result)

    def test_repository_with_github_remote_as_origin_returns_a_repository(self) -> None:
        self.run_command(
            "git remote add origin git@github.com:seppeljordan/nix-prefetch-github.git"
        )
        result = self.detector.detect_github_repository(self.tmpdir, remote_name=None)
        self.assertIsInstance(result, GithubRepository)

    def test_repository_with_github_remote_with_remote_name_test_returns_a_repository(
        self,
    ) -> None:
        self.run_command(
            "git remote add test git@github.com:seppeljordan/nix-prefetch-github.git"
        )
        result = self.detector.detect_github_repository(self.tmpdir, remote_name="test")
        self.assertIsInstance(result, GithubRepository)


class DetectRevisionTests(GitTestCase):
    def test_for_repo_without_commit_return_none(self) -> None:
        self.assertIsNone(self.detector.get_current_revision(self.tmpdir))

    def test_for_repo_with_commit_return_not_none(self) -> None:
        self.run_command("touch test.txt")
        self.run_command("git add test.txt")
        self.run_command("git commit -a -m 'test commit'")
        self.assertIsNotNone(self.detector.get_current_revision(self.tmpdir))


class DetectGithubRepositoryFromRemoteUrlTests(TestCase):
    def test_can_detect_valid_urls_and_handle_invalid_ones(self) -> None:
        fixture = [
            (
                "git@github.com:seppeljordan/nix-prefetch-github.git",
                GithubRepository(
                    owner="seppeljordan",
                    name="nix-prefetch-github",
                ),
            ),
            (
                "https://github.com/seppeljordan/nix-prefetch-github.git",
                GithubRepository(
                    owner="seppeljordan",
                    name="nix-prefetch-github",
                ),
            ),
            (
                "invalid",
                None,
            ),
        ]
        for url, expected_repository in fixture:
            with self.subTest():
                self.assertEqual(
                    detect_github_repository_from_remote_url(url),
                    expected_repository,
                )
