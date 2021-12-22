import re
from typing import Optional

from .command import run_command
from .repository import GithubRepository


class RepositoryDetectorImpl:
    def is_repository_dirty(self, directory: str) -> bool:
        returncode, _ = run_command(
            command=["git", "diff", "HEAD", "--quiet"],
            cwd=directory,
        )
        return returncode != 128 and returncode != 0

    def detect_github_repository(
        self, directory: str, remote_name: Optional[str]
    ) -> Optional[GithubRepository]:
        if remote_name is None:
            remote = "origin"
        else:
            remote = remote_name
        returncode, stdout = run_command(
            command=["git", "remote", "get-url", remote], cwd=directory
        )
        return detect_github_repository_from_remote_url(stdout)

    def get_current_revision(self, directory: str) -> Optional[str]:
        exitcode, stdout = run_command(
            command=["git", "rev-parse", "HEAD"], cwd=directory
        )
        if exitcode != 0:
            return None
        return stdout[:-1]


def detect_github_repository_from_remote_url(url: str) -> Optional[GithubRepository]:
    match = re.match("(git@github.com:|https://github.com/)(.+)/(.+).git", url)
    if not match:
        return None
    else:
        owner = match.group(2)
        name = match.group(3)
        return GithubRepository(
            name=name,
            owner=owner,
        )
