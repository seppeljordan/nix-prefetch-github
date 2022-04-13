import json
from dataclasses import dataclass
from logging import Logger
from typing import List, Optional

from ..command import CommandRunner
from ..interfaces import PrefetchOptions
from ..repository import GithubRepository


@dataclass(frozen=True)
class NixPrefetchUrlHasherImpl:
    command_runner: CommandRunner
    logger: Logger

    def calculate_sha256_sum(
        self,
        repository: GithubRepository,
        revision: str,
        prefetch_options: PrefetchOptions,
    ) -> Optional[str]:
        if self.is_default_prefetch_options(prefetch_options):
            return self.fetch_url(repository=repository, revision=revision)
        else:
            return self.fetch_git(
                repository=repository,
                revision=revision,
                prefetch_options=prefetch_options,
            )

    def fetch_url(self, repository: GithubRepository, revision: str) -> Optional[str]:
        repo_url = f"https://github.com/{repository.owner}/{repository.name}/archive/{revision}.tar.gz"
        _, output = self.command_runner.run_command(
            ["nix-prefetch-url", "--unpack", repo_url],
        )
        return self.calculate_sri_representation(output.strip())

    def fetch_git(
        self,
        repository: GithubRepository,
        revision: str,
        prefetch_options: PrefetchOptions,
    ) -> Optional[str]:
        repo_url = f"https://github.com/{repository.owner}/{repository.name}.git"
        command = (
            ["nix-prefetch-git"]
            + self.prefetch_git_options(prefetch_options)
            + [repo_url, revision]
        )
        _, output = self.command_runner.run_command(command)
        return self.calculate_sri_representation(json.loads(output)["sha256"])

    def calculate_sri_representation(self, sha256: str) -> str:
        _, output = self.command_runner.run_command(
            ["nix", "hash", "to-sri", f"sha256:{sha256}"],
        )
        return output.strip().removeprefix("sha256-")

    def is_default_prefetch_options(self, options: PrefetchOptions) -> bool:
        return options == PrefetchOptions()

    def prefetch_git_options(self, prefetch_options: PrefetchOptions) -> List[str]:
        options: List[str] = []
        if prefetch_options.deep_clone:
            options.append("--deepClone")
        if prefetch_options.leave_dot_git or prefetch_options.deep_clone:
            options.append("--leave-dotGit")
        if prefetch_options.fetch_submodules:
            options.append("--fetch-submodules")
        return options
