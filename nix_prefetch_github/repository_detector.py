import re
from dataclasses import dataclass
from logging import Logger
from typing import Optional

from nix_prefetch_github.interfaces import CommandRunner, GithubRepository


@dataclass
class RepositoryDetectorImpl:
    command_runner: CommandRunner
    logger: Logger

    def is_repository_dirty(self, directory: str) -> bool:
        returncode, _ = self.command_runner.run_command(
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
        returncode, stdout = self.command_runner.run_command(
            command=["git", "remote", "get-url", remote], cwd=directory
        )
        detected_url = detect_github_repository_from_remote_url(stdout)
        self.logger.info(f"Detected repository '{detected_url}' from '{remote}'")
        return detected_url

    def get_current_revision(self, directory: str) -> Optional[str]:
        exitcode, stdout = self.command_runner.run_command(
            command=["git", "rev-parse", "HEAD"], cwd=directory
        )
        if exitcode != 0:
            return None
        return stdout[:-1]


def detect_github_repository_from_remote_url(url: str) -> Optional[GithubRepository]:
    match = re.match(
        r"(git@github.com:|https://github.com/)(?P<owner>.+)/((?P<repo>.+)\.git|(?P<repo_with_prefix>.+))$",
        url,
    )
    if not match:
        return None
    else:
        owner = match.group("owner")
        name = match.group("repo") or match.group("repo_with_prefix")
        return GithubRepository(
            name=name,
            owner=owner,
        )
