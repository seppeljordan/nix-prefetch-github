import json
from dataclasses import dataclass
from logging import Logger
from typing import List, Optional

from nix_prefetch_github.interfaces import (
    CommandRunner,
    GithubRepository,
    HashConverter,
    PrefetchedRessource,
    PrefetchOptions,
)


@dataclass(frozen=True)
class NixPrefetchUrlHasherImpl:
    command_runner: CommandRunner
    logger: Logger
    hash_converter: HashConverter

    def calculate_hash_sum(
        self,
        repository: GithubRepository,
        revision: str,
        prefetch_options: PrefetchOptions,
    ) -> Optional[PrefetchedRessource]:
        if self.is_default_prefetch_options(prefetch_options):
            return self.fetch_url(repository=repository, revision=revision)
        else:
            return self.fetch_git(
                repository=repository,
                revision=revision,
                prefetch_options=prefetch_options,
            )

    def fetch_url(
        self, repository: GithubRepository, revision: str
    ) -> Optional[PrefetchedRessource]:
        repo_url = f"https://github.com/{repository.owner}/{repository.name}/archive/{revision}.tar.gz"
        _, output = self.command_runner.run_command(
            ["nix-prefetch-url", "--unpack", repo_url, "--print-path"],
        )
        try:
            hash_sum, store_path = output.splitlines()
        except ValueError:
            return None
        sri_hash = self.calculate_sri_representation(hash_sum.strip())
        if not sri_hash:
            return None
        else:
            return PrefetchedRessource(
                hash_sum=sri_hash,
                store_path=store_path,
            )

    def fetch_git(
        self,
        repository: GithubRepository,
        revision: str,
        prefetch_options: PrefetchOptions,
    ) -> Optional[PrefetchedRessource]:
        repo_url = f"https://github.com/{repository.owner}/{repository.name}.git"
        command = (
            ["nix-prefetch-git"]
            + self.prefetch_git_options(prefetch_options)
            + [repo_url, revision]
        )
        _, output = self.command_runner.run_command(command)
        command_output_json = json.loads(output)
        sri_hash = self.calculate_sri_representation(command_output_json["sha256"])
        if not sri_hash:
            return None
        else:
            return PrefetchedRessource(
                hash_sum=sri_hash,
                store_path=command_output_json["path"],
            )

    def calculate_sri_representation(self, sha256: str) -> Optional[str]:
        return self.hash_converter.convert_sha256_to_sri(sha256)

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
